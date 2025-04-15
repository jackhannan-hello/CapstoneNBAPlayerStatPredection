import csv
import pandas as pd
import numpy as np
from scipy import optimize
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

def get_player_average(player_key):
    """recent_data = name + "P5G.csv"
    rd = pd.read_csv(recent_data)
    curr_team = rd.Team[4]
    career_data = name + ".csv"
    cd = pd.read_csv(career_data)
    opp = pd.read_csv("sgaVMEM.csv")
    recent_season = cd.loc[cd['Season'].isin(["2024-25"])]
    team_data = cd.loc[cd['Team'].isin([curr_team])]
    #team_data["PTS"].mean()  #[team_data['PTS'].mean(), team_data['AST'].mean(), team_data['TRB'].mean()]
    #print(f"{cd[["PTS", "AST", "TRB"]].groupby("Team").mean(numeric_only=True)}")
    #print(team_data[["PTS", "AST", "TRB"]])
    season_avg = recent_season[["PTS", "AST", "TRB"]]
    team_avg = team_data[["PTS", "AST", "TRB"]].mean()
    recent_avg = rd[["PTS", "AST", "TRB"]].mean()
    opponent_avg = opp[["PTS", "AST", "TRB"]].mean()
    return team_avg, season_avg, recent_avg, opponent_avg"""
    # Get the player's file prefix
    player_prefix = PLAYER_MAPPING.get(player_key, player_key)

    print(player_prefix)
    
    # File paths
    base_dir = r"c:\Users\Jack Hannan\source\repos\CapstoneNBAPlayerStatPredection\my-app\src"
    recent_data = os.path.join(base_dir, "playerStats", f"{player_prefix}FullStats.csv")
    career_data = os.path.join(base_dir, "playerStats", f"{player_prefix}.csv")

    print(recent_data)
    print(career_data)
    
    #Check if files exist
    if not os.path.exists(recent_data) or not os.path.exists(career_data):
        #raise FileNotFoundError(f"Stats files for {DISPLAY_NAMES.get(player_key, player_key)} not found")
        recent_data = os.path.join("playerStats", "sgaFullStats.csv")
        career_data = os.path.join("playerStats", "sga.csv")
        print(f"Stats files for {DISPLAY_NAMES.get(player_key, player_key)} not found, using default stats")
    
    # Load data
    td = pd.read_csv(recent_data) #total data
    cd = pd.read_csv(career_data)
    
    rd = td.iloc[-6:-1]

    # Get team and opponent data
    curr_team = td.Team.iloc[0] if 'Team' in td.columns else 'Unknown'
    oppent = td.Opponent.iloc[0] if 'Opponent' in td.columns else 'Unknown'
    #oppent_data = os.path.join("playerStats", f"{player_prefix}VMEM.csv")
    #op = pd.read_csv(oppent_data)
    #oppent = op.Opponent.iloc[0] if 'Opponent' in op.columns else 'Unknown'
    
    # Load opponent data (using generic opponent data for now)
    # In a full implementation, you'd have specific opponent data for each player
    #opp_data = pd.DataFrame({'PTS': [25.0], 'AST': [6.0], 'TRB': [6.0]})
    opp_data = td[td['Opponent'] == oppent].iloc[:-1] if 'Opponent' in td.columns else td
    
    # Get recent season data
    recent_season = cd[cd['Season'] == '2024-25'] if 'Season' in cd.columns else cd.head(1)
    
    # Get team data
    team_data = cd[cd['Team'] == curr_team] if 'Team' in cd.columns else cd
    
    # Calculate averages
    season_avg = recent_season[["PTS", "AST", "TRB"]] if not recent_season.empty else pd.DataFrame({'PTS': [0], 'AST': [0], 'TRB': [0]})
    team_avg = team_data[["PTS", "AST", "TRB"]].mean() if not team_data.empty else pd.Series({'PTS': 0, 'AST': 0, 'TRB': 0})
    recent_avg = rd[["PTS", "AST", "TRB"]].mean()
    opponent_avg = opp_data[["PTS", "AST", "TRB"]].mean()
    
    return team_avg, season_avg, recent_avg, opponent_avg

def calc_next_game_stat(weights, team_val, season_val, recent_val, opponent_val):
    # Normalize weights to sum to 1
    weights = np.array(weights) / np.sum(weights)
    
    # Calculate weighted average
    return round(
        weights[0] * team_val + 
        weights[1] * season_val + 
        weights[2] * recent_val + 
        weights[3] * opponent_val, 
        2
    )

def optimize_weights_for_stat(team_val, season_val, recent_val, opponent_val, actual_val):
    # Initial guess (equal weights)
    initial_weights = np.array([0.25, 0.25, 0.25, 0.25])
    
    # Constraint: weights must sum to 1
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    
    # Bounds: each weight between 0 and 1
    bounds = [(0, 1) for _ in range(4)]

    # Objective function: squared error between prediction and actual for single stat
    def objective(weights):
        prediction = calc_next_game_stat(weights, team_val, season_val, recent_val, opponent_val)
        return (prediction - actual_val)**2
    
    # Run optimization
    result = optimize.minimize(
        objective, 
        initial_weights, 
        constraints=constraints,
        bounds=bounds,
        method='SLSQP'  # Sequential Least Squares Programming
    )
    
    return result.x
"""optimal_weights = optimize_weights(team, season, recent, opponent, actual)
    print(f"Optimized weights: [Team: {optimal_weights[0]:.3f}, Season: {optimal_weights[1]:.3f}, "
          f"Recent: {optimal_weights[2]:.3f}, Opponent: {optimal_weights[3]:.3f}]")
    #next_game_stats = calc_next_game(team, season, recent, opponent)
    #print(f"team average: {team}")
    #print(f"recent average: {recent}")

    # Calculate prediction with optimized weights
    optimized_prediction = calc_next_game(optimal_weights, team, season, recent, opponent)

    # Calculate prediction with default equal weights
    default_prediction = calc_next_game([0.25, 0.25, 0.25, 0.25], team, season, recent, opponent)"""
def get_input():
    #user_input = input("Enter Player Name: ")
    #player = user_input.replace(" ", "")
    #player = player.lower()
    team, season, recent, opponent = get_player_average("sga") #come back to and change to variable
    actual = pd.read_csv("sgaFullStats.csv").tail(1)[["PTS", "AST", "TRB"]].iloc[0]
    #actual = actual.reset_index(drop=True)

    optimized_prediction = {}
    weights_by_stat = {}

    for stat in ["PTS", "AST", "TRB"]:
        # Get the specific stat values
        team_val = team[stat]
        season_val = season[stat].mean() if isinstance(season[stat], pd.Series) else season[stat]
        recent_val = recent[stat]
        opponent_val = opponent[stat]
        actual_val = actual[stat]
        
        # Find optimal weights for this specific stat
        opt_weights = optimize_weights_for_stat(
            team_val, season_val, recent_val, opponent_val, actual_val
        )
        weights_by_stat[stat] = opt_weights
        
        # Calculate prediction with optimized weights
        optimized_prediction[stat] = calc_next_game_stat(
            opt_weights, team_val, season_val, recent_val, opponent_val
        )
    
    # Create DataFrame for displaying in frontend
    result_df = pd.DataFrame({
        'PTS': [actual['PTS']],
        'AST': [actual['AST']],
        'TRB': [actual['TRB']],
        'Predicted_PTS': [optimized_prediction['PTS']],
        'Predicted_AST': [optimized_prediction['AST']],
        'Predicted_TRB': [optimized_prediction['TRB']]
    })
    
    print(result_df)
    return result_df

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

def get_player_prediction(player_key):
    """Get prediction for a specific player"""
    try:
        # Get player averages
        team, season, recent, opponent = get_player_average(player_key)
        
        # For this implementation, we'll use the recent average as the "actual" value
        # In a real implementation, you'd use actual game data
        """actual = pd.Series({
            'PTS': recent['PTS'] * 1.05,  # Just adding 5% for demonstration
            'AST': recent['AST'] * 0.95,  # Just reducing 5% for demonstration
            'TRB': recent['TRB'] * 1.02   # Just adding 2% for demonstration
        })"""
        player_prefix = PLAYER_MAPPING.get(player_key, player_key)
        base_dir = r"c:\Users\Jack Hannan\source\repos\CapstoneNBAPlayerStatPredection\my-app\src"
        actual_data = os.path.join(base_dir, "playerStats", f"{player_prefix}FullStats.csv")
                             
        if not os.path.exists(actual_data):
            #raise FileNotFoundError(f"Stats files for {DISPLAY_NAMES.get(player_key, player_key)} not found")
            actual_data = os.path.join("playerStats", "sgaFullStats.csv")
            print(f"Stats files for {DISPLAY_NAMES.get(player_key, player_key)} not found, using default stats hello")

        actual = pd.read_csv(actual_data).tail(1)[["PTS", "AST", "TRB"]].iloc[0]

        optimized_prediction = {}
        weights_by_stat = {}

        for stat in ["PTS", "AST", "TRB"]:
            # Get the specific stat values
            team_val = team[stat]
            season_val = season[stat].mean() if isinstance(season[stat], pd.Series) else season[stat]
            recent_val = recent[stat]
            opponent_val = opponent[stat]
            actual_val = actual[stat]
            
            # Default weights for prediction
            opt_weights = [0.25, 0.25, 0.35, 0.15]  # Team, Season, Recent, Opponent
            
            # Calculate prediction with optimized weights
            #opt_weights = optimize_weights_for_stat(
             #   team_val, season_val, recent_val, opponent_val, actual_val
            #)

            weights_by_stat[stat] = opt_weights

            optimized_prediction[stat] = calc_next_game_stat(
            opt_weights, team_val, season_val, recent_val, opponent_val
    )
        
        # Create DataFrame for displaying in frontend
        result_df = pd.DataFrame({
            'PTS': [actual['PTS']],
            'AST': [actual['AST']],
            'TRB': [actual['TRB']],
            'Predicted_PTS': [optimized_prediction['PTS']],
            'Predicted_AST': [optimized_prediction['AST']],
            'Predicted_TRB': [optimized_prediction['TRB']]
        })
        
        return result_df

    except Exception as e:
        # Return empty dataframe with error message
        print(f"Error predicting stats for {player_key}: {str(e)}")
        return pd.DataFrame({
            'PTS': [0],
            'AST': [0],
            'TRB': [0],
            'Predicted_PTS': [0],
            'Predicted_AST': [0],
            'Predicted_TRB': [0]
        })

if __name__ == '__main__':
    # Test with default player
    result = get_player_prediction('sga')
    print(result)
