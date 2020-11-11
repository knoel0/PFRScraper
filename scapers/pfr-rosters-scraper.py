from helpermodule import teams, get_table, abbr_to_teamname_end
import pandas as pd
from datetime import datetime

def getTeamRoster(abbr: str) -> pd.DataFrame:
    
    url = 'https://www.pro-football-reference.com/teams/' + teams[abbr]["Abbr Url"] + '/2020_roster.htm'
    df = get_table(url, "games_played_team", header=True)
    df.columns = df.columns.str.strip()
        
    team_list = [abbr] * df.shape[0]
    pos_list = [0] * df.shape[0]

    df['Team'] = team_list
    df['QB'] = df['RB'] = df['WR'] = df['TE'] = df['K'] = df['DST'] = pos_list

    df.loc[df['Pos'] == 'QB', 'QB'] = 1
    df.loc[(df['Pos'] == 'RB') | (df['Pos'] == 'FB'), 'RB'] = 1
    df.loc[df['Pos'] == 'WR', 'WR'] = 1
    df.loc[df['Pos'] == 'TE', 'TE'] = 1
    df.loc[df['Pos'] == 'K', 'K'] = 1
    df.loc[df['Pos'] == 'QB/TE', 'QB'] = 1
    df.loc[df['Pos'] == 'QB/TE', 'TE'] = 1
    df.loc[df['Pos'] == 'LS/TE', 'TE'] = 1

    df = df.drop(df[(df.Pos == 'OL') | (df.Pos == 'OT') | (df.Pos == '') | (df.Pos == 'T') | (df.Pos == 'G') | (df.Pos == 'OG') | (df.Pos == 'C') | (df.Pos == 'DL') | (df.Pos == 'DE') | (df.Pos == 'LS') | (df.Pos == 'DT') | (df.Pos == 'LOLB') | (df.Pos == 'OLB') | (df.Pos == 'ILB') | (df.Pos == 'SS')| (df.Pos == 'LILB') | (df.Pos == 'MLB') | (df.Pos == 'LB') | (df.Pos == 'CB') | (df.Pos == 'DB') | (df.Pos == 'LT') | (df.Pos == 'LG') | (df.Pos == 'FS') | (df.Pos == 'S') | (df.Pos == 'P') | (df.Pos == 'EDGE') | (df.Pos == 'LG') | (df.Pos == 'NT') | (df.Pos == 'RILB')].index)
    df = df.drop(columns=['G', 'GS', 'BirthDate', 'AV', 'Drafted (tm/rnd/yr)', 'Salary', 'Pos'])

    df.loc[len(df.index)] = ['', abbr_to_teamname_end(abbr), '', '', '', '', '', abbr, 0, 0, 0, 0, 0, 1]

    df.reset_index(drop=True, inplace=True)

    return df

for team in teams:
    path = r'/Users/kanemnoel/Desktop/portfolio-projects/fantasy-fb-app-scrapes/rosters/' + team + '/' + datetime.today().strftime('%Y%m%d-%H%M%S') + '-' + team + '.csv'
    getTeamRoster(team).to_csv(path, index=False, header=True)