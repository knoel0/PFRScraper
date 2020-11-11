from helpermodule import get_table, months, longname_to_abbr
from datetime import datetime
import pandas as pd

def add_start_home_away(game: pd.Series):

    def standard_to_military(g: pd.Series) -> str:
        
        g.Time.strip()
        hr = g.Time.split(':')[0]
        min = g.Time.split(':')[1]
        meridiem = min[-2:]
        min = min[:-2]
        
        if meridiem == 'PM' and g.Time.split(':')[0] != '12':
            hr = int(hr)
            hr += 12
            hr = str(hr)
        elif meridiem == 'AM' and hr == '12':
            hr = int(hr)
            hr += 12
            hr = str(hr)

        if len(hr) == 1:
            hr = '0' + hr        

        return hr + ':' + min + ':00'
        
    def get_month(g: pd.Series) -> str:
        
        return months.get(g.Date.split()[0])
    
    def get_day(g: pd.Series) -> str:
        
        if len(g.Date.split()[1]) == 1:
            return '0' + g.Date.split()[1]
        else:
            return g.Date.split()[1]

    if get_month(game) == '01':
        game.Start = '2021-' + get_month(game) + '-' + get_day(game) + ' ' + standard_to_military(game)
    else:
        game.Start = '2020-' + get_month(game) + '-' + get_day(game) + ' ' + standard_to_military(game)

    if any(game == '@'):
        game.Home = longname_to_abbr(game.L)
        game.Away = longname_to_abbr(game.W)
    else:
        game.Home = longname_to_abbr(game.W)
        game.Away = longname_to_abbr(game.W)

df = get_table('https://www.pro-football-reference.com/years/2020/games.htm', 'games', header=True)

l = [''] * df.shape[0]

df['Start'] = df['Home'] = df['Away'] = l

df.rename(columns={'Winner/tie': 'W', 'Loser/tie': 'L'}, inplace=True)
df.apply(add_start_home_away, axis=1)
df = df.drop(columns=['Day', 'Date', 'Time', 'W', 'L', 'PtsW', 'PtsL', 'YdsW', 'TOW', 'YdsL', 'TOL', ''], axis=1)
    
#add season to path
path = r'/Users/kanemnoel/Desktop/portfolio-projects/fantasy-fb-app-scrapes/games/' + datetime.today().strftime('%Y%m%d-%H%M%S') + '.csv'
df.to_csv(path, index=False, header=True)