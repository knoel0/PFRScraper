import os
import json
from helper import teams, get_table, abbr_to_teamname_end
import pandas as pd
from datetime import datetime

config = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '/config.json'))

def get_roster(abbr: str) -> pd.DataFrame:
    
    url = "https://www.pro-football-reference.com/teams/{}/2020_roster.htm".format(teams[abbr]['Abbr Url'])
    df = get_table(url, 'games_played_team', header=True)
        
    team_list = [abbr] * df.shape[0]
    pos_list = [0] * df.shape[0]
    df['Team'] = team_list
    df['QB'] = df['RB'] = df['WR'] = df['TE'] = df['K'] = df['DST'] = pos_list

    df.loc[df['Pos'] == "QB", 'QB'] = 1
    df.loc[(df['Pos'] == "RB") | (df['Pos'] == "FB"), 'RB'] = 1
    df.loc[df['Pos'] == "WR", 'WR'] = 1
    df.loc[df['Pos'] == "TE", 'TE'] = 1
    df.loc[df['Pos'] == "K", 'K'] = 1
    df.loc[df['Pos'] == "QB/TE", 'QB'] = 1
    df.loc[df['Pos'] == "QB/TE", 'TE'] = 1
    df.loc[df['Pos'] == "LS/TE", 'TE'] = 1

    df = df.drop(df[(df.Pos == 'OL') | (df.Pos == 'OT') | (df.Pos == '') | (df.Pos == 'T') | (df.Pos == 'G') | (df.Pos == 'OG') | (df.Pos == 'C') | (df.Pos == 'DL') | (df.Pos == 'DE') | (df.Pos == 'LS') | (df.Pos == 'DT') | (df.Pos == 'LOLB') | (df.Pos == 'OLB') | (df.Pos == 'ILB') | (df.Pos == 'SS')| (df.Pos == 'LILB') | (df.Pos == 'MLB') | (df.Pos == 'LB') | (df.Pos == 'CB') | (df.Pos == 'DB') | (df.Pos == 'LT') | (df.Pos == 'LG') | (df.Pos == 'FS') | (df.Pos == 'S') | (df.Pos == 'P') | (df.Pos == 'EDGE') | (df.Pos == 'LG') | (df.Pos == 'NT') | (df.Pos == 'RILB')].index)
    df = df.drop(columns=['G', 'GS', 'BirthDate', 'AV', 'Drafted (tm/rnd/yr)', 'Salary', 'Pos'])

    # CREATE "DST" player
    df.loc[len(df.index)] = ['', abbr_to_teamname_end(abbr), '', '', '', '', '', abbr, 0, 0, 0, 0, 0, 1]

    df.reset_index(drop=True, inplace=True)
    
    print("\n{}".format(df))
    return df

while True:
    try:
        inp = input("\nAll rosters? [Y/N]: ")
    except ValueError:
        print("Sorry, didn't understand that.")
        continue
    
    inp = inp.upper()
    if inp[0] not in {"Y", "N"}:
        print("Sorry, your input must be yes or no.")
    else:
        break

if inp == "Y":
    for team in teams:
        path = "{p}{t}/{d}-{t}.csv".format(p=config['path_rosters'], t=team, d=datetime.today().strftime('%Y%m%d-%H%M%S'))
            
        get_roster(team).to_csv(path, index=False, header=True)
        print("\nCSV successfully saved to..\n{}".format(path))      
else:
    while True:
        try:
            inp_team = input("Enter the team's abbreviation: ")
        except ValueError:
            print("Sorry, didn't understand that.")
            continue
        
        inp_team = inp_team.upper()
        if inp_team not in teams:
            print("Sorry, your input must be a NFL team's valid abbreviation.")
        else:
            break

    path = "{p}{t}/{d}-{t}.csv".format(p=config['path_rosters'], t=inp_team, d=datetime.today().strftime('%Y%m%d-%H%M%S'))
        
    get_roster(inp_team).to_csv(path, index=False, header=True)
    print("\nCSV successfully saved to..\n{}".format(path))