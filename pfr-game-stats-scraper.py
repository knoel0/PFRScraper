import os
import json
from helper import teams, urlabbr_to_abbr, substring_to_abbr, get_table, get_all_tagtext_by_class, stats_template
import pandas as pd
from datetime import datetime

config = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '/config.json'))

def addFg(player: pd.Series):
    
    strSplit = player.Detail.split()
    kickerName = strSplit[0] + ' ' + strSplit[1]
    
    if kickerName == kicker_stats['name']:
        if int(strSplit[2]) > 50:
            kicker_stats['fgMade50Plus'] += 1
        elif int(strSplit[2]) < 50:
            kicker_stats['fgMade0To49'] += 1

def addSafety(player: pd.Series):
    
    team = substring_to_abbr(player.Tm)
    
    if team == home_team:
        homedef_player_stats['safeties'] += 1
    else:
        awaydef_player_stats['safeties'] += 1

def addXPReturn(player: pd.Series):
    
    team = substring_to_abbr(player.Tm)
    
    if team == home_team:
        homedef_player_stats['twoPntConvRet'] += 1
    else:
        awaydef_player_stats['twoPntConvRet'] += 1            

home_abbr = input("Enter the home team's abbreviation: ")
away_abbr = input("Enter the away team's abbreviation: ")
year = input("Enter the year of the game (XXXX): ")
month = input("Enter the month of the game (XX): ")
day = input("Enter the day of the game (XX): ")

url_abbr = teams[home_abbr]["Abbr Url"]
url = "https://www.pro-football-reference.com/boxscores/" + year + month + day + '0' + url_abbr + '.htm'

column_names = ['Name', 'Team', 'Pass Yds', 'Pass Tds', 'Pass Ints', 'Rush Yds', 'Rush Tds', 'Rec Yds', 'Rec Tds', '2 Point Conversions', 'Fumbles Lost', 'Fumbles Recovered For Tds', 'Pat Made', 'FG Made 0to49', 'FG Made 50 Plus', 'Sacks', 'Def Ints', 'Fumbles Recovered', 'Safeties', 'Def Tds', 'Kick Punt Return Tds', '2 Point Conversion Returns', 'Pnts All 0', 'Pnts All 1to6', 'Pnts All 7to13', 'Pnts All 14to20', 'Pnts All 21to27', 'Pnts All 28to34', 'Pnts All 35 Plus']
    
df = pd.DataFrame(columns=column_names)

df_offense = get_table(url, 'player_offense', header=True)
df_defense = get_table(url, "player_defense", header=True)
df_scoring = get_table(url, "scoring", header=True)
df_returns = get_table(url, "returns", header=True)
df_kicking = get_table(url, "kicking", header=True)

players = []

## Offense
for player in df_offense.itertuples():
    player_stats_off = stats_template.copy()
    player_stats_off['name'] = player[1].strip()
    if player[2] in teams:
        player_stats_off['team'] = player[2]
    else:    
        player_stats_off['team'] = urlabbr_to_abbr(player[2].lower())
    player_stats_off['passYards'] = player[5]
    player_stats_off['passTds'] = player[6]
    player_stats_off['passInts'] = player[7]
    player_stats_off['rushYds'] = player[13]
    player_stats_off['rushTds'] = player[14]
    player_stats_off['recYds'] = player[18]
    player_stats_off['recTds'] = player[19]
    player_stats_off['fumbLost'] = player[22]
    ## add 2 point conv
    players.append(list(player_stats_off.values()))

## Kickers
for player in df_kicking.itertuples():
    kicker_stats = stats_template.copy()
    kicker_stats['name'] = player[1].strip()
    if player[2] in teams:
        kicker_stats['team'] = player[2]
    else:    
        kicker_stats['team'] = urlabbr_to_abbr(player[2].lower())
    if len(player[3]) > 0:
        kicker_stats['patMade'] = player[3]
    df_defense_fgs = df_scoring[df_scoring['Detail'].str.contains('field goal')]
    if (len(df_defense_fgs)) > 0:
        for i in range(len(df_defense_fgs)):
            df_defense_fgs.apply(addFg, axis=1)
    players.append(list(kicker_stats.values()))    

## Defense/Special Teams
if len(teams[home_abbr]["Full Name"].split()) == 3:
    home_name = teams[home_abbr]["Full Name"].split()[2]
else:
    home_name = teams[home_abbr]["Full Name"].split()[1]
home_team = home_abbr
home_ints = home_tds = home_fumbrec = 0
home_sacks = 0.0

away_name = away_team = ''
away_ints = away_tds = away_fumbrec = 0
away_sacks = 0.0

homedef_player_stats = stats_template.copy()
awaydef_player_stats = stats_template.copy()

away_team_isset = False
for player in df_defense.itertuples():
    if (player[2].lower()) == url_abbr:
        home_ints += int(player[3])
        home_tds += (int(player[5]) + int(player[16]))
        home_sacks += float(player[8])
        home_fumbrec += int(player[14])
    else:
        while not away_team_isset:
            if len(teams[urlabbr_to_abbr(player[2].lower())]['Full Name'].split()) == 3:
                away_name = teams[urlabbr_to_abbr(player[2].lower())]['Full Name'].split()[2]
            else:
                away_name = teams[urlabbr_to_abbr(player[2].lower())]['Full Name'].split()[1]
            away_team = urlabbr_to_abbr(player[2].lower())
            away_team_isset = True
        away_ints += int(player[3])
        away_tds += (int(player[5]) + int(player[16]))
        away_sacks += float(player[8])
        away_fumbrec += int(player[14])

df_scoring_safeties = df_scoring[df_scoring['Detail'].str.contains('Safety')]
df_scoring_xpreturns = df_scoring[df_scoring['Detail'].str.contains('extra point return')]
    
if (len(df_scoring_safeties)) > 0:
    df_scoring_safeties.apply(addSafety, axis=1)
if (len(df_scoring_xpreturns)) > 0:
    df_scoring_xpreturns.apply(addXPReturn, axis=1)    

for player in df_returns.itertuples():
    if player[2] == home_abbr:
        homedef_player_stats['kickPuntRetTds'] += (int(player[6]) + int(player[11]))
    else:
        awaydef_player_stats['kickPuntRetTds'] += (int(player[6]) + int(player[11]))

if int(get_all_tagtext_by_class(url, 'div', 'score')[1]) == 0:
    homedef_player_stats['pntsAll0'] = 1
elif 1 <= int(get_all_tagtext_by_class(url, 'div', 'score')[1]) <= 6:
    homedef_player_stats['pntsAll1To6'] = 1
elif 7 <= int(get_all_tagtext_by_class(url, 'div', 'score')[1]) <= 13:
    homedef_player_stats['pntsAll7To13'] = 1
elif 14 <= int(get_all_tagtext_by_class(url, 'div', 'score')[1]) <= 20:
    homedef_player_stats['pntsAll14To20'] = 1
elif 21 <= int(get_all_tagtext_by_class(url, 'div', 'score')[1]) <= 27:
    homedef_player_stats['pntsAll21To27'] = 1
elif 28 <= int(get_all_tagtext_by_class(url, 'div', 'score')[1]) <= 34:
    homedef_player_stats['pntsAll28To34'] = 1
elif int(get_all_tagtext_by_class(url, 'div', 'score')[1]) > 35:
    homedef_player_stats['pntsAll35Plus'] = 1
if int(get_all_tagtext_by_class(url, 'div', 'score')[0]) == 0:
    awaydef_player_stats['pntsAll0'] = 1
elif 1 <= int(get_all_tagtext_by_class(url, 'div', 'score')[0]) <= 6:
    awaydef_player_stats['pntsAll1To6'] = 1
elif 7 <= int(get_all_tagtext_by_class(url, 'div', 'score')[0]) <= 13:
    awaydef_player_stats['pntsAll7To13'] = 1
elif 14 <= int(get_all_tagtext_by_class(url, 'div', 'score')[0]) <= 20:
    awaydef_player_stats['pntsAll14To20'] = 1
elif 21 <= int(get_all_tagtext_by_class(url, 'div', 'score')[0]) <= 27:
    awaydef_player_stats['pntsAll21To27'] = 1
elif 28 <= int(get_all_tagtext_by_class(url, 'div', 'score')[0]) <= 34:
    awaydef_player_stats['pntsAll28To34'] = 1
elif int(get_all_tagtext_by_class(url, 'div', 'score')[0]) > 35:
    awaydef_player_stats['pntsAll35Plus'] = 1

homedef_player_stats['name'] = home_name
homedef_player_stats['team'] = home_team
homedef_player_stats['defInts'] = home_ints
homedef_player_stats['defTds'] = home_tds
homedef_player_stats['defFumbRec'] = home_fumbrec
homedef_player_stats['sacks'] = home_sacks
awaydef_player_stats['name'] = away_name
awaydef_player_stats['team'] = away_team
awaydef_player_stats['defInts'] = away_ints
awaydef_player_stats['defTds'] = away_tds
awaydef_player_stats['defFumbRec'] = away_fumbrec
awaydef_player_stats['sacks'] = away_sacks

players.append(list(homedef_player_stats.values()))
players.append(list(awaydef_player_stats.values()))

path = "{p}{t}/vs{a}{d}-{t}.csv".format(p=config['path_gamestats'], t=home_abbr, a=away_abbr, d=datetime.today().strftime('%Y%m%d-%H%M%S'))
pd.DataFrame(players, columns=column_names).to_csv(path, index=False, header=True)