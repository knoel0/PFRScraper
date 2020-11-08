import pandas as pd
import requests, bs4
import re
from datetime import datetime

teamDict = {
    'ARI': {
        'abbrNameForUrl': 'crd',
        'fullName': 'Arizona Cardinals'
    },
    'ATL': {
        'abbrNameForUrl': 'atl',
        'fullName': 'Atlanta Falcons'
    },
    'BAL': {
        'abbrNameForUrl': 'rav',
        'fullName': 'Baltimore Ravens'
    },
    'BUF': {
        'abbrNameForUrl': 'buf',
        'fullName': 'Buffalo Bills'
    },
    'CAR': {
        'abbrNameForUrl': 'car',
        'fullName': 'Carolina Panthers'
    },
    'CHI': {
        'abbrNameForUrl': 'chi',
        'fullName': 'Chicago Bears'
    },
    'CIN': {
        'abbrNameForUrl': 'cin',
        'fullName': 'Cincinnati Bengals'
    },
    'CLE': {
        'abbrNameForUrl': 'cle',
        'fullName': 'Cleveland Browns'
    },
    'DAL': {
        'abbrNameForUrl': 'dal',
        'fullName': 'Dallas Cowboys'
    },
    'DEN': {
        'abbrNameForUrl': 'den',
        'fullName': 'Denver Broncos'
    },
    'DET': {
        'abbrNameForUrl': 'det',
        'fullName': 'Detroit Lions'
    },
    'GB': {
        'abbrNameForUrl': 'gnb',
        'fullName': 'Green Bay Packers'
    },
    'HOU': {
        'abbrNameForUrl': 'htx',
        'fullName': 'Houston Texans'
    },
    'IND': {
        'abbrNameForUrl': 'clt',
        'fullName': 'Indianapolis Colts'
    },
    'JAX': {
        'abbrNameForUrl': 'jax',
        'fullName': 'Jacksonville Jaguars'
    },
    'KC': {
        'abbrNameForUrl': 'kan',
        'fullName': 'Kansas City Chiefs'
    },
    'LAC': {
        'abbrNameForUrl': 'sdg',
        'fullName': 'Los Angeles Chargers'
    },
    'LAR': {
        'abbrNameForUrl': 'ram',
        'fullName': 'Los Angeles Rams'
    },
    'LV': {
        'abbrNameForUrl': 'rai',
        'fullName': 'Las Vegas Raiders'
    },
    'MIA': {
        'abbrNameForUrl': 'mia',
        'fullName': 'Miami Dolphins'
    },
    'MIN': {
        'abbrNameForUrl': 'min',
        'fullName': 'Minnesota Vikings'
    },
    'NE': {
        'abbrNameForUrl': 'nwe',
        'fullName': 'New England Patriots'
    },
    'NO': {
        'abbrNameForUrl': 'nor',
        'fullName': 'New Orleans Saints'
    },
    'NYG': {
        'abbrNameForUrl': 'nyg',
        'fullName': 'New York Giants'
    },
    'NYJ': {
        'abbrNameForUrl': 'nyj',
        'fullName': 'New York Jets'
    },
    'PHI': {
        'abbrNameForUrl': 'phi',
        'fullName': 'hiladelphia Eagles'
    },
    'PIT': {
        'abbrNameForUrl': 'pit',
        'fullName': 'Pittsburgh Steelers'
    },
    'SEA': {
        'abbrNameForUrl': 'sea',
        'fullName': 'Seattle Seahawks'
    },
    'SF': {
        'abbrNameForUrl': 'sfo',
        'fullName': 'San Francisco 49ers'
    },
    'TB': {
        'abbrNameForUrl': 'tam',
        'fullName': 'Tampa Bay Buccaneers'
    },
    'TEN': {
        'abbrNameForUrl': 'oti',
        'fullName': 'Tennessee Titans'
    },
    'WAS': {
        'abbrNameForUrl': 'was',
        'fullName': 'Washington Football Team'
    }
}

monthsDict = {
    'January' : '01',
    'February': '02',
    'March' : '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12' 
}  

def getGameScoresResult(hometeam_abbr: str, awayteam_abbr: str, week: str) -> dict:

    scoresResult = {
        'homePoints': None,
        'awayPoints': None,
        'winner': None,
        'loser': None,
        'tie': None
    }

    urlAbbr = teamDict[hometeam_abbr]["abbrNameForUrl"]
    url = 'https://www.pro-football-reference.com/teams/' + urlAbbr + '/2020/gamelog/'
    df = getTable(url, 'gamelog2020', header=True)
    
    row = df.loc[df['Week'] == week]
    if row.iloc[0,6] == '@':
        scoresResult['homePoints'] = row.iloc[0,9]
        scoresResult['awayPoints'] = row.iloc[0,8]
    else:
        scoresResult['homePoints'] = row.iloc[0,8]
        scoresResult['awayPoints'] = row.iloc[0,9]
    if row.iloc[0,4] == 'W':
        scoresResult['winner'] = hometeam_abbr
        scoresResult['loser'] = awayteam_abbr
        scoresResult['tie'] = False
    elif row.iloc[0,4] == 'L':
        scoresResult['winner'] = awayteam_abbr
        scoresResult['loser'] = hometeam_abbr
        scoresResult['tie'] = False
    elif row.iloc[0,4] == 'T':
        scoresResult['tie'] = True

    return scoresResult 

def getGameStats(hometeam_abbr: str, year: str, month: str, day: str) -> dict:
    urlAbbr = teamDict[hometeam_abbr]["abbrNameForUrl"]
    url = "https://www.pro-football-reference.com/boxscores/" + year + month + day + '0' + urlAbbr + '.htm'

    #pull player data

def getGames() -> df:
    
    df = getTable('https://www.pro-football-reference.com/years/2020/games.htm', 'games', header=True)

    start = []
    home_team = []
    away_team = []
    for i in range(0, df.shape[0]):
        start.append('')
        home_team.append('')
        away_team.append('')
    df['Start'] = start
    df['HomeTeam'] = home_team
    df['AwayTeam'] = away_team

    df.rename(columns={'Winner/tie': 'W', 'Loser/tie': 'L'}, inplace=True)
    df.apply(add_Start_HomeTeam_AwayTeam, axis=1)
    df.drop(columns=['Day', 'Date', 'Time', 'W', 'L', 'PtsW', 'PtsL', 'YdsW', 'TOW', 'YdsL', 'TOL', 'Month', 'TimeTemp', ''])

    def add_Start_HomeTeam_AwayTeam(series):
        if getMonth(series) == '01':
            series.Start = '2021-' + getMonth(series) + '-' + getDay(series) + ' ' + standardToMilitary(series)
        else:
            series.Start = '2020-' + getMonth(series) + '-' + getDay(series) + ' ' + standardToMilitary(series)
        
        #x = any(series == '@')
        #if x == True:

        if any(series == '@'):
            series.HomeTeam = longNametoAbbr(series.L)
            series.AwayTeam = longNametoAbbr(series.W)
        else:
            series.HomeTeam = longNametoAbbr(series.W)
            series.AwayTeam = longNametoAbbr(series.W)

        def standardToMilitary(ser) -> str:
            ser.Time.strip()
            hr = ser.Time.split(':')[0]
            min = ser.Time.split(':')[1]
            meridiem = min[-2:]
            min = min[:-2]
            if meridiem == 'PM' and hr != '12':
                hr = int(hr)
                hr += 12
                hr = str(hr)
            elif meridiem == 'AM' and hr == '12':
                hr = int(hr)
                hr += 12
                hr = str(hr)
            if len(hr) == 1:
                hr = '0' + hr
            return(hr + ':' + min + ':00')
        def getMonth(ser) -> str:
            return monthsDict.get(ser.Date.split()[0])
        def getDay(ser) -> str:
            if ser.Date.split()[1] == '1':
                return '0' + ser.Date.split()[1]
            else:
                return ser.Date.split()[1]
        def longNametoAbbr(longname: str) -> str:
            for abbr, nestedDict in teamDict.items():
                for key, value in nestedDict.items():
                    if value == longname:
                        return abbr

def getTeamRoster(abbr: str) -> df:
    url = 'https://www.pro-football-reference.com/teams/' + teamDict[abbr]["abbrNameForUrl"] + '/2020_roster.htm'
    df = getTable(url, "games_played_team", header=True)
        
    teamList = []
    qbList = []
    rbList = []
    wrList = []
    teList = []
    kList = []
    dstList = []
        
    dfRowCount = df.shape[0]
    for i in range(0, dfRowCount):
        teamList.append(abbr)
        qbList.append(0)
        rbList.append(0)
        wrList.append(0)
        teList.append(0)
        kList.append(0)
        dstList.append(0)

    df['Team'] = teamList
    df['QB'] = qbList
    df['RB'] = rbList
    df['WR'] = wrList
    df['TE'] = teList
    df['K'] = kList
    df['D/ST'] = dstList

    df.loc[df['Pos'] == 'QB', 'QB'] = 1
    df.loc[(df['Pos'] == 'RB') | (df['Pos'] == 'FB'), 'RB'] = 1
    df.loc[df['Pos'] == 'WR', 'WR'] = 1
    df.loc[df['Pos'] == 'TE', 'TE'] = 1
    df.loc[df['Pos'] == 'K', 'K'] = 1
    df.loc[df['Pos'] == 'QB/TE', 'QB'] = 1
    df.loc[df['Pos'] == 'QB/TE', 'TE'] = 1
    df.loc[df['Pos'] == 'LS/TE', 'TE'] = 1

    df = df.drop(df[(df.Pos == 'OL') | (df.Pos == 'OT') | (df.Pos == '') | (df.Pos == 'T') | (df.Pos == 'G') | (df.Pos == 'OG') | (df.Pos == 'C') | (df.Pos == 'DL') | (df.Pos == 'DE') | (df.Pos == 'LS') | (df.Pos == 'DT') | (df.Pos == 'LOLB') | (df.Pos == 'OLB') | (df.Pos == 'ILB') | (df.Pos == 'SS')| (df.Pos == 'LILB') | (df.Pos == 'MLB') | (df.Pos == 'LB') | (df.Pos == 'CB') | (df.Pos == 'DB') | (df.Pos == 'LT') | (df.Pos == 'LG') | (df.Pos == 'FS') | (df.Pos == 'S') | (df.Pos == 'P') | (df.Pos == 'EDGE') | (df.Pos == 'LG') | (df.Pos == 'NT') | (df.Pos == 'RILB')].index)

    df = df.drop(columns=['G', 'GS', 'BirthDate', 'AV', 'Drafted (tm/rnd/yr)', 'Salary'])

    return df

def getAllTeamRosters() -> list:
    dfList = []
    for team in teamDict:
        dfList.append(getTeamRoster(team))
    return dfList

def getTable(url: str, tableID: str, header=True) -> df:
    res = requests.get(url)
    
    ## Work around comments
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    
    table = soup.find('table', id = tableID)
    table_body = table.find('tbody')
    rows = table_body.findAll('tr')
    data_list = [
        [td.getText() for td in rows[i].findAll(['th', 'td'])]
        for i in range(len(rows))
    ]
    data = pd.DataFrame(data_list)

    if header == True:
        column_names = table.find('thead')
        column_names = column_names.find('tr', {'class': None})
        column_names = column_names.findAll('th')
        column_names_list = []
        for i in range(len(data.columns)):
            column_names_list.append(column_names[i].getText())
        data.columns = column_names_list
        data = data.loc[data[column_names_list[0]] != column_names_list[0]]
    data = data.reset_index(drop = True)
    return(data)
