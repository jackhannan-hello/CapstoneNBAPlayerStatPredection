import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import numpy as np
import os

# Player name mapping for file access
PLAYER_MAPPING = {
    'sga': 'sga',
    'jayson_tatum': 'jaysontatum',
    'josh_hart': 'joshhart',
    'devin_booker': 'devinbooker',
    'lebron_james': 'lebronjames',
    'steph_curry': 'stephcurry',
    'giannis': 'giannisantetokounmpo',
    'jaylen_brown': 'jaylenbrown',
    'austin_reaves': 'austinreaves',
    'lamelo_ball': 'lameloball',
    'bam_adebayo': 'bamadebayo',
    'payton_pritchard': 'paytonpritchard',
    'jalen_brunson': 'jalenbrunson',
    'kevin_durant': 'kevindurant',
    'draymond_green': 'draymondgreen',
    'andrew_wiggins': 'andrewwiggins',
    'jamal_murray': 'jamalmurray',
    'russell_westbrook': 'russellwestbrook',
    'tyler_herro': 'tylerherro',
    'rudy_gobert': 'rudygobert',
    'anthony_edwards': 'anthonyedwards',
    'nikola_jokic': 'nikolajokic',
}

# Map to display names
DISPLAY_NAMES = {
    'sga': 'Shai Gilgeous-Alexander',
    'jayson_tatum': 'Jayson Tatum',
    'josh_hart': 'Josh Hart',
    'devin_booker': 'Devin Booker',
    'lebron_james': 'LeBron James',
    'steph_curry': 'Stephen Curry',
    'giannis': 'Giannis Antetokounmpo',
    'jaylen_brown': 'Jaylen Brown',
    'austin_reaves': 'Austin Reaves',
    'lamelo_ball': 'LaMelo Ball',
    'bam_adebayo': 'Bam Adebayo',
    'payton_pritchard': 'Payton Pritchard',
    'jalen_brunson': 'Jalen Brunson',
    'kevin_durant': 'Kevin Durant',
    'draymond_green': 'Draymond Green',
    'andrew_wiggins': 'Andrew Wiggins',
    'jamal_murray': 'Jamal Murray',
    'russell_westbrook': 'Russell Westbrook',
    'tyler_herro': 'Tyler Herro',
    'rudy_gobert': 'Rudy Gobert',
    'anthony_edwards': 'Anthony Edwards',
    'nikola_jokic': 'Nikola Jokic',
}

def calculate_accuracy_metrics(actual, predicted):
    """Calculate accuracy metrics for predictions"""
    
    # Calculate metrics for each stat
    metrics = {}
    
    for stat in ["PTS", "AST", "TRB"]:
        actual_val = actual[stat]
        pred_val = predicted[f"Predicted_{stat}"]
        
        # Calculate absolute error
        abs_error = abs(actual_val - pred_val)
        
        # Calculate percentage error
        perc_error = (abs_error / actual_val) * 100 if actual_val != 0 else float('inf')
        
        # Calculate accuracy percentage (100 - percentage error, bounded at 0)
        accuracy = max(0, 100 - perc_error)
        
        metrics[stat] = {
            "absolute_error": round(abs_error, 2),
            "percentage_error": round(perc_error, 2),
            "accuracy": round(accuracy, 2)
        }
    
    # Calculate overall accuracy (average of individual accuracies)
    overall_accuracy = np.mean([metrics[stat]["accuracy"] for stat in ["PTS", "AST", "TRB"]])
    metrics["overall"] = round(overall_accuracy, 2)
    
    return metrics

def load_and_preprocess_data(file_path):
    """Load and preprocess data from the given file path."""
    df = pd.read_csv(file_path)
    try:
        df = df = df[["Rk", "Gcar", "Gtm", "Team", "AWAY", "Opp", "PTS", "AST", "TRB"]]
    except KeyError:
        print("Warning: Some columns not found in the dataset")
    df = df.dropna()
    return df

def train_random_forest_model(X_train, y_train):
    """Train a Random Forest model."""
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def get_prediction():
    file_path = "sgaFullStats.csv"
    #df = pd.read_csv(file_path)
    df = load_and_preprocess_data(file_path)

    #df = df.drop(columns=["Date", "Unnamed: 6", "G", "Age", "GS", "MP", "FG", "FGA",
    #                      "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB",
    #                      "STL", "BLK", "TOV", "PF", "GmSc", "+/-"])
    #df = df.dropna()

    X = df.drop(columns=["PTS", "AST", "TRB"])
    y = df[["PTS", "AST", "TRB"]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=45)

    #scaler = StandardScaler()
    #X_train = scaler.fit_transform(X_train)
    #X_test = scaler.transform(X_test)

    #model = RandomForestRegressor(n_estimators=100, random_state=42)
    #model.fit(X_train, y_train)

    model = train_random_forest_model(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error: {mae} for model\n\n")

    #plt.figure(figsize=(20, 10))
    #plot_tree(model.estimators_[0], feature_names=X.columns, filled=True, rounded=True, fontsize=10)
    #plt.show()

    recent = df.tail(5)
    actual_recent = recent[["PTS", "AST", "TRB"]]
    test_recent = recent.drop(columns=["PTS", "AST", "TRB"])
    recent_pred = model.predict(test_recent)


    #plt.figure(figsize=(20, 13))
    #plot_tree(model.estimators_[0], feature_names=test_recent.columns, filled=True, rounded=True, fontsize=10)
    #plt.show()

    predicted_df = pd.DataFrame(recent_pred, columns=["Predicted_PTS", "Predicted_AST", "Predicted_TRB"]).round(2)

    combined_df = pd.concat([actual_recent.reset_index(drop=True), predicted_df], axis=1)

    print("Actual stats compared to predicted stats for recent games")
    print(combined_df)

    recent_mae = mean_absolute_error(test_recent, recent_pred)
    print(f"Mean Absolute Error: {recent_mae}")

    return combined_df

def get_player_rf_prediction(player_key):
    """Get Random Forest prediction for a specific player"""
    try:
        # Get the player's file prefix
        player_prefix = PLAYER_MAPPING.get(player_key, player_key)
        print(player_prefix)
        
        # File path
        file_path = os.path.join("playerStats", f"{player_prefix}FullStats.csv")
        print(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            # Use default stats file as fallback
            file_path = os.path.join("playerStats", "sgaFullStats.csv")
            print(f"Full stats for {player_key} not found, using default stats")
        
        # Load data
        #df = pd.read_csv(file_path)
        df = load_and_preprocess_data(file_path)
        
        # Preprocess data
        #try:
        #    df = df.drop(columns=["Date", "Unnamed: 6", "G", "Age", "GS", "MP", "FG", "FGA",
        #                         "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB",
        #                         "STL", "BLK", "TOV", "PF", "GmSc", "+/-"])
        #except KeyError:
            # If some columns don't exist, just proceed with what we have
        #    print("Warning: Some columns not found in the dataset")

        #df = df.dropna()
        
        # If dataframe is empty after dropping NAs, return default prediction
        if df.empty:
            return pd.DataFrame({
                'PTS': [20],
                'AST': [5],
                'TRB': [5],
                'Predicted_PTS': [20],
                'Predicted_AST': [5],
                'Predicted_TRB': [5]
            })
        
        # Prepare data for model
        X = df.drop(columns=["PTS", "AST", "TRB"])
        y = df[["PTS", "AST", "TRB"]]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=45)
        
        # Train model
        #model = RandomForestRegressor(n_estimators=100, random_state=42)
        #model.fit(X_train, y_train)
        model = train_random_forest_model(X_train, y_train)
        
        # Get recent data for prediction
        recent = df.tail(5)
        actual_recent = recent[["PTS", "AST", "TRB"]]
        test_recent = recent.drop(columns=["PTS", "AST", "TRB"])
        
        # Make prediction
        recent_pred = model.predict(test_recent)
        
        # Prepare result
        predicted_df = pd.DataFrame(recent_pred, columns=["Predicted_PTS", "Predicted_AST", "Predicted_TRB"]).round(2)
        combined_df = pd.concat([actual_recent.reset_index(drop=True), predicted_df], axis=1)
        
        # Return last game prediction
        return combined_df.tail(1)

    except Exception as e:
        # Return empty dataframe with error message
        print(f"Error predicting stats with Random Forest for {player_key}: {str(e)}")
        return pd.DataFrame({
            'PTS': [0],
            'AST': [0],
            'TRB': [0],
            'Predicted_PTS': [0],
            'Predicted_AST': [0],
            'Predicted_TRB': [0]
        })
        empty_df.attrs['accuracy_metrics'] = {
            "PTS": {"accuracy": 0, "absolute_error": 0, "percentage_error": 0},
            "AST": {"accuracy": 0, "absolute_error": 0, "percentage_error": 0},
            "TRB": {"accuracy": 0, "absolute_error": 0, "percentage_error": 0},
            "overall": 0
        }
        return empty_df

if __name__ == '__main__':
     # Test with default player
    result = get_player_rf_prediction('sga')
    print(result)