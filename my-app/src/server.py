from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from randForestPredict import get_player_rf_prediction
from predictStats import get_player_prediction
import sys

# Import prediction functions - try/except to provide better error messages
try:
    from predictStats import get_player_prediction
    from randForestPredict import get_player_rf_prediction
except ImportError as e:
    print(f"Error importing prediction modules: {str(e)}")
    print("Make sure all required packages are installed and files are in the correct location.")
    sys.exit(1)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for frontend communication

# Test endpoint to verify server is running properly
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "NBA prediction server is running"})

def calculate_accuracy_metrics(result_df):
    """
    Calculate accuracy metrics for prediction results
    
    Args:
        result_df: DataFrame with actual and predicted values
        
    Returns:
        Dictionary of accuracy metrics
    """
    try:
        if result_df.empty:
            return {}
        
        # Get the most recent prediction row
        last_game = result_df.iloc[0].to_dict()
        
        # Calculate metrics for each stat
        metrics = {}
        
        for stat in ["PTS", "AST", "TRB"]:
            actual_val = last_game[stat]
            pred_val = last_game[f"Predicted_{stat}"]
            
            # Calculate absolute error
            abs_error = abs(actual_val - pred_val)
            
            # Calculate percentage error
            perc_error = (abs_error / actual_val) * 100 if actual_val != 0 else 0
            # Calculate accuracy percentage (100 - percentage error, bounded at 0)
            accuracy = max(0, 100 - perc_error)
            
            metrics[stat] = {
                "absolute_error": round(abs_error, 2),
                "percentage_error": round(perc_error, 2),
                "accuracy": round(accuracy, 2)
            }
        
        # Calculate overall accuracy (average of individual accuracies)
        overall_accuracy = sum([metrics[stat]["accuracy"] for stat in ["PTS", "AST", "TRB"]]) / 3
        metrics["overall"] = round(overall_accuracy, 2)

        metrics_df = pd.DataFrame(metrics).T.reset_index()
        metrics_df.columns = ["Stat", "Absolute Error", "Percentage Error", "Accuracy"]
        
        return metrics_df.to_dict(orient="records")
    except Exception as e:
        print(f"Error calculating accuracy metrics: {str(e)}")
        return {
            "PTS": {"accuracy": 0, "absolute_error": 0, "percentage_error": 0},
            "AST": {"accuracy": 0, "absolute_error": 0, "percentage_error": 0},
            "TRB": {"accuracy": 0, "absolute_error": 0, "percentage_error": 0},
            "overall": 0
        }

@app.route("/get-prediction", methods=["GET"])
def fetch_prediction():
    try:
        """result_df = get_prediction()  # Call the function
        result_json = result_df.to_json(orient="records")  # Convert DataFrame to JSON
        return jsonify({"predictions": result_json})
    except Exception as e:
        return jsonify({"error": str(e)}), 500"""
        player_name = request.args.get('player', 'sga')  # Default to sga if not provided
        print(f"Received request for player: {player_name}")
        result_df = get_player_rf_prediction(player_name)  # Pass player name to prediction function
        #accuracy_metrics = calculate_accuracy_metrics(result_df) # Extract the accuracy metrics
        #accuracy_json = accuracy_metrics.to_json(orient="records")  # Convert accuracy metrics to JSON
        result_json = result_df.to_json(orient="records")  # Convert DataFrame to JSON
        # overall_accuracy = accuracy_metrics.get("overall", 0)  # Get overall accuracy from metrics
        # overall_json = overall_accuracy.to_json(orient="records")  # Convert overall accuracy to JSON
        print(f"Prediction result: {result_json}")
        response = jsonify({
            "predictions": result_json
        }) # Return both the predictions and accuracy metrics
        print(f"Response: {response}")
        print(f"predictions: {result_json}")
        return response
    except Exception as e:
        #return jsonify({"error": str(e)}), 500
        print(f"Error in fetch_prediction: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "error": str(e), 
            "predictions": "[]",
            "accuracy_metrics": {}
        }), 500

@app.route("/get-input", methods=["GET"])
def fetch_input():
    try:
        """result_df = get_input()  # Call get_input function
        result_json = result_df.to_json(orient="records")  # Convert DataFrame to JSON
        return jsonify({"input_data": result_json})
    except Exception as e:
        return jsonify({"error": str(e)}), 500"""
        player_name = request.args.get('player', 'sga')  # Default to sga if not provided
        print(f"Received input request for player: {player_name}")
        result_df = get_player_prediction(player_name)  # Pass player name to prediction function
        #accuracy_metrics = calculate_accuracy_metrics(result_df) # Extract the accuracy metrics
        #accuracy_json = accuracy_metrics.to_json(orient="records")  # Convert accuracy metrics to JSO
        result_json = result_df.to_json(orient="records")  # Convert DataFrame to JSON
        # overall_accuracy = accuracy_metrics.get("overall", 0)  # Get overall accuracy from metrics
        # overall_json = overall_accuracy.to_json(orient="records")  # Convert overall accuracy to JSON
        response = jsonify({
            "input_data": result_json
        }) # Return both the input data and accuracy metrics
        print(f"Response: {response}")
        print(f"predictions: {result_json}")
        return response
    except Exception as e:
        print(f"Error in fetch_input: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "error": str(e), 
            "input_data": "[]",
            "accuracy_metrics": {}
        }), 500

if __name__ == "__main__":
    print("Starting NBA prediction server on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)