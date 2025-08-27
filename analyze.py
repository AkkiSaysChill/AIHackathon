
import pandas as pd

df = pd.read_csv('csgo_games.csv')
import sys

team_1_list = df['team_1'].unique().tolist()
team_2_list = df['team_2'].unique().tolist()
all_teams = sorted(list(set(team_1_list + team_2_list)))

if len(sys.argv) > 1:
    selected_team = sys.argv[1]
    if selected_team in all_teams:
        team_matches = df[(df['team_1'] == selected_team) | (df['team_2'] == selected_team)]
        wins = team_matches[((team_matches['winner'] == 't1') & (team_matches['team_1'] == selected_team)) | ((team_matches['winner'] == 't2') & (team_matches['team_2'] == selected_team))]
        win_rate = len(wins) / len(team_matches)
        print(f"\nWin rate for {selected_team}: {win_rate:.2%}")
    else:
        print("\nInvalid team name.")
else:
    print("Available teams:")
    for team in all_teams:
        print(team)
    print("\nUsage: python3 analyze.py \"<team_name>\"")


