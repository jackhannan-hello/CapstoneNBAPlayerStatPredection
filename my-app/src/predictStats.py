import csv
import pandas as pd
import numpy as np
from scipy import optimize

def get_player_average(name):
    recent_data = name + "P5G.csv"
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
    return team_avg, season_avg, recent_avg, opponent_avg

def calc_next_game_stat(weights, team_val, season_val, recent_val, opponent_val):
    """return [
        round((team['PTS'].mean() + season['PTS'].mean() + recent['PTS'].mean() + opponent['PTS'].mean()) / 4, 2),
        round((team['AST'].mean() + season['AST'].mean() + recent['AST'].mean() + opponent['AST'].mean()) / 4, 2),
        round((team['TRB'].mean() + season['TRB'].mean() + recent['TRB'].mean() + opponent['TRB'].mean()) / 4, 2),
    ]"""
    """Calculate next game stats using weighted average of different factors
    
    Args:
        weights: Array of weights for [team, season, recent, opponent]
        team, season, recent, opponent: Series of stats
    
    Returns:
        Predicted stats based on weighted averages
    """
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
    """Find optimal weights to minimize prediction error
    
    Args:
        team, season, recent, opponent: Series of stats
        actual: Series of actual stats to compare against
    
    Returns:
        Optimized weights
    """
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

if __name__ == '__main__':
    get_input()
    