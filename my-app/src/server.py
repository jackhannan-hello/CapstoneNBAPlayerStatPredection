from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from randForestPredict import get_prediction  # Import get_predition
from predictStats import get_input  # Import get_input

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

@app.route("/get-prediction", methods=["GET"])
def fetch_prediction():
    try:
        result_df = get_prediction()  # Call the function
        result_json = result_df.to_json(orient="records")  # Convert DataFrame to JSON
        return jsonify({"predictions": result_json})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-input", methods=["GET"])
def fetch_input():
    try:
        result_df = get_input()  # Call get_input function
        result_json = result_df.to_json(orient="records")  # Convert DataFrame to JSON
        return jsonify({"input_data": result_json})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)