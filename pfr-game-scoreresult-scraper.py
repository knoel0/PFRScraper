import sys
sys.path.insert(0, '/Users/kanemnoel/Desktop/portfolio-projects/pfr-scraper/modules')
from bs_helper import get_table
from pfrscraper_helper import teams

def get_game_scoreresult(hometeam_abbr: str, awayteam_abbr: str, week: str):

    scoreresult = {
        'Home Points': None,
        'Away Points': None,
        'Winner': None,
        'Loser': None,
        'Tie': None
    }

    url_abbr = teams[hometeam_abbr]["Abbr Url"]
    url = 'https://www.pro-football-reference.com/teams/' + url_abbr + '/2020/gamelog/'
    df = get_table(url, 'gamelog2020', header=True)
    
    row = df.loc[df['Week'] == week]
    if row.iloc[0,6] == '@':
        scoreresult['Home Points'] = row.iloc[0,9]
        scoreresult['Away Points'] = row.iloc[0,8]
    else:
        scoreresult['Home Points'] = row.iloc[0,8]
        scoreresult['Away Points'] = row.iloc[0,9]
    if row.iloc[0,4] == 'W':
        scoreresult['Winner'] = hometeam_abbr
        scoreresult['Loser'] = awayteam_abbr
        scoreresult['Tie'] = False
    elif row.iloc[0,4] == 'L':
        scoreresult['Winner'] = awayteam_abbr
        scoreresult['Loser'] = hometeam_abbr
        scoreresult['Tie'] = False
    elif row.iloc[0,4] == 'T':
        scoreresult['Tie'] = True

    return scoreresult