import csv
import pandas as pd

def get_player_average(name):
    recent_data = name + "P5G.csv"
    rd = pd.read_csv(recent_data)
    curr_team = rd.Team[4]
    career_data = name + ".csv"
    cd = pd.read_csv(career_data)
    team_data = cd.loc[cd['Team'].isin([curr_team])]
    #team_data["PTS"].mean()  #[team_data['PTS'].mean(), team_data['AST'].mean(), team_data['TRB'].mean()]
    #print(f"{cd[["PTS", "AST", "TRB"]].groupby("Team").mean(numeric_only=True)}")
    #print(team_data[["PTS", "AST", "TRB"]])
    team_avg = team_data[["PTS", "AST", "TRB"]].mean()
    recent_avg = rd[["PTS", "AST", "TRB"]].mean()

    return team_avg, recent_avg

def calc_next_game(team, recent):
    next_game = (2 * team) - recent
    return next_game.round()

if __name__ == '__main__':
    user_input = input("Enter Player Name: ")
    player = user_input.replace(" ", "")
    team, recent = get_player_average(player)
    print(f"team average: {team}")
    print(f"recent average: {recent}")
    next_game_stats = calc_next_game(team, recent)
    print(f"{user_input}'s next game stats will be:")
    print(next_game_stats)