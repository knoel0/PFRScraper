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
        'fullName': 'Philadelphia Eagles'
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

def urlAbbrToAbbr(urlAbbr: str):
    for abbr, nestedDict in teamDict.items():
        for key, value in nestedDict.items():
            if value == urlAbbr:
                return abbr

def longNameToAbbr(longname: str):
    for abbr, nestedDict in teamDict.items():
        for key, value in nestedDict.items():
            if value == longname:
                return abbr

def subStringToAbbr(subString: str):
    for abbr, nestedDict in teamDict.items():
        for key, value in nestedDict.items():
            if subString in value:
                return abbr

def getGameScoresResult(hometeam_abbr: str, awayteam_abbr: str, week: str):

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

def getGameStats(hometeam_abbr: str, year: str, month: str, day: str):
    
    urlAbbr = teamDict[hometeam_abbr]["abbrNameForUrl"]
    url = "https://www.pro-football-reference.com/boxscores/" + year + month + day + '0' + urlAbbr + '.htm'

    column_names = ['Name', 'Team', 'Pass Yds', 'Pass Tds', 'Pass Ints', 'Rush Yds', 'Rush Tds', 'Rec Yds', 'Rec Tds', '2 Point Conversions', 'Fumbles Lost', 'Fumbles Recovered For Tds', 'Pat Made', 'FG Made 0to49', 'FG Made 50 Plus', 'Sacks', 'Def Ints', 'Fumbles Recovered', 'Safeties', 'Def Tds', 'Kick Punt Return Tds', '2 Point Conversion Returns', 'Pnts All 0', 'Pnts All 1to6', 'Pnts All 7to13', 'Pnts All 14to20', 'Pnts All 21to27', 'Pnts All 28to34', 'Pnts All 35 Plus']
    
    dfStats = pd.DataFrame(columns=column_names)

    dfOffense = getTable(url, 'player_offense', header=True)
    dfDefense = getTable(url, "player_defense", header=True)
    dfScoring = getTable(url, "scoring", header=True)
    dfReturn = getTable(url, "returns", header=True)
    dfKickers = getTable(url, "kicking", header=True)

    statsDictTemplate = {
        'name': '',
        'team': '',
        'passYards': 0,
        'passTds': 0,
        'passInts': 0,
        'rushYds': 0,
        'rushTds': 0,
        'recYds': 0,
        'recTds': 0,
        'twoPntConvs': 0,
        'fumbLost': 0,
        'fumbRecTd': 0,
        'patMade': 0,
        'fgMade0To49': 0,
        'fgMade50Plus': 0,
        'sacks': 0,
        'defInts': 0,
        'defFumbRec': 0,
        'safeties': 0,
        'defTds': 0,
        'kickPuntRetTds': 0,
        'twoPntConvRet': 0,
        'pntsAll0': 0,
        'pntsAll1To6': 0,
        'pntsAll7To13': 0,
        'pntsAll14To20': 0,
        'pntsAll21To27': 0,
        'pntsAll28To34': 0,
        'pntsAll35Plus': 0
    }

    # -- OFF
    # 2oint conv

    playerList = []

    ## Offense
    for row in dfOffense.itertuples():
        playerStatsOff = statsDictTemplate.copy()
        playerStatsOff['name'] = row[1].strip()
        if row[2] in teamDict:
            playerStatsOff['team'] = row[2]
        else:    
            playerStatsOff['team'] = urlAbbrToAbbr(row[2].lower())
        playerStatsOff['passYards'] = row[5]
        playerStatsOff['passTds'] = row[6]
        playerStatsOff['passInts'] = row[7]
        playerStatsOff['rushYds'] = row[13]
        playerStatsOff['rushTds'] = row[14]
        playerStatsOff['recYds'] = row[18]
        playerStatsOff['recTds'] = row[19]
        playerStatsOff['fumbLost'] = row[22]
        playerList.append(list(playerStatsOff.values()))

    ## Kickers
    for row in dfKickers.itertuples():
        playerStatsK = statsDictTemplate.copy()
        playerStatsK['name'] = row[1].strip()
        if row[2] in teamDict:
            playerStatsK['team'] = row[2]
        else:    
            playerStatsK['team'] = urlAbbrToAbbr(row[2].lower())
        if len(row[3]) > 0:
            playerStatsK['patMade'] = row[3]
        dfDefense_ForFgs = dfScoring[dfScoring['Detail'].str.contains('field goal')]
        if (len(dfDefense_ForFgs)) > 0:
            for i in range(len(dfDefense_ForFgs)):
                def addFg(series):
                    strSplit = series.Detail.split()
                    kickerName = strSplit[0] + ' ' + strSplit[1]
                    if kickerName == playerStatsK['name']:
                        if int(strSplit[2]) > 50:
                            playerStatsK['fgMade50Plus'] += 1
                        elif int(strSplit[2]) < 50:
                            playerStatsK['fgMade0To49'] += 1
                dfDefense_ForFgs.apply(addFg, axis=1)
        playerList.append(list(playerStatsK.values()))    

    ## Defense/Special Teams
    if len(teamDict[hometeam_abbr]["fullName"].split()) == 3:
        homeName = teamDict[hometeam_abbr]["fullName"].split()[2]
    else:
        homeName = teamDict[hometeam_abbr]["fullName"].split()[1]
    homeTeam = hometeam_abbr
    homeInts = homeTds = homeFumbRec = 0
    homeSacks = 0.0
    awayName = ''
    awayTeam = ''
    awayInts = awayTds = awayFumbRec = 0
    awaySacks = 0.0

    playerStatsDefHome = statsDictTemplate.copy()
    playerStatsDefAway = statsDictTemplate.copy()

    awayTeamSet = False
    for row in dfDefense.itertuples():
        if (row[2].lower()) == urlAbbr:
            homeInts += int(row[3])
            homeTds += (int(row[5]) + int(row[16]))
            homeSacks += float(row[8])
            homeFumbRec += int(row[14])
        else:
            while not awayTeamSet:
                if len(teamDict[urlAbbrToAbbr(row[2].lower())]['fullName'].split()) == 3:
                    awayName = teamDict[urlAbbrToAbbr(row[2].lower())]['fullName'].split()[2]
                else:
                    awayName = teamDict[urlAbbrToAbbr(row[2].lower())]['fullName'].split()[1]
                awayTeam = urlAbbrToAbbr(row[2].lower())
                awayTeamSet = True
            awayInts += int(row[3])
            awayTds += (int(row[5]) + int(row[16]))
            awaySacks += float(row[8])
            awayFumbRec += int(row[14])

    def addSafety(series):
        team = subStringToAbbr(series.Tm)
        if team == homeTeam:
            playerStatsDefHome['safeties'] += 1
        else:
            playerStatsDefAway['safeties'] += 1

    def addXPReturn(series):
        team = subStringToAbbr(series.Tm)
        if team == homeTeam:
            playerStatsDefHome['twoPntConvRet'] += 1
        else:
            playerStatsDefAway['twoPntConvRet'] += 1

    dfScoring_Safety = dfScoring[dfScoring['Detail'].str.contains('Safety')]
    dfScoring_XPReturn = dfScoring[dfScoring['Detail'].str.contains('extra point return')]
    
    if (len(dfScoring_Safety)) > 0:
        dfScoring_Safety.apply(addSafety, axis=1)
    if (len(dfScoring_XPReturn)) > 0:
        dfScoring_XPReturn.apply(addXPReturn, axis=1)    

    for row in dfReturn.itertuples():
        if row[2] == hometeam_abbr:
            playerStatsDefHome['kickPuntRetTds'] += (int(row[6]) + int(row[11]))
        else:
            playerStatsDefAway['kickPuntRetTds'] += (int(row[6]) + int(row[11]))

    if int(getTagTextByClass(url, 'div', 'score', multiple=True)[1]) == 0:
        playerStatsDefHome['pntsAll0'] = 1
    elif 1 <= int(getTagTextByClass(url, 'div', 'score', multiple=True)[1]) <= 6:
        playerStatsDefHome['pntsAll1To6'] = 1
    elif 7 <= int(getTagTextByClass(url, 'div', 'score', multiple=True)[1]) <= 13:
        playerStatsDefHome['pntsAll7To13'] = 1
    elif 14 <= int(getTagTextByClass(url, 'div', 'score', multiple=True)[1]) <= 20:
        playerStatsDefHome['pntsAll14To20'] = 1
    elif 21 <= int(getTagTextByClass(url, 'div', 'score', multiple=True)[1]) <= 27:
        playerStatsDefHome['pntsAll21To27'] = 1
    elif 28 <= int(getTagTextByClass(url, 'div', 'score', multiple=True)[1]) <= 34:
        playerStatsDefHome['pntsAll28To34'] = 1
    elif int(getTagTextByClass(url, 'div', 'score', multiple=True)[1]) > 35:
        playerStatsDefHome['pntsAll35Plus'] = 1
    if int(getTagTextByClass(url, 'div', 'score', multiple=True)[0]) == 0:
        playerStatsDefAway['pntsAll0'] = 1
    elif 1 <= int(getTagTextByClass(url, 'div', 'score', multiple=True)[0]) <= 6:
        playerStatsDefAway['pntsAll1To6'] = 1
    elif 7 <= int(getTagTextByClass(url, 'div', 'score', multiple=True)[0]) <= 13:
        playerStatsDefAway['pntsAll7To13'] = 1
    elif 14 <= int(getTagTextByClass(url, 'div', 'score', multiple=True)[0]) <= 20:
        playerStatsDefAway['pntsAll14To20'] = 1
    elif 21 <= int(getTagTextByClass(url, 'div', 'score', multiple=True)[0]) <= 27:
        playerStatsDefAway['pntsAll21To27'] = 1
    elif 28 <= int(getTagTextByClass(url, 'div', 'score', multiple=True)[0]) <= 34:
        playerStatsDefAway['pntsAll28To34'] = 1
    elif int(getTagTextByClass(url, 'div', 'score', multiple=True)[0]) > 35:
        playerStatsDefAway['pntsAll35Plus'] = 1

    playerStatsDefHome['name'] = homeName
    playerStatsDefHome['team'] = homeTeam
    playerStatsDefHome['defInts'] = homeInts
    playerStatsDefHome['defTds'] = homeTds
    playerStatsDefHome['defFumbRec'] = homeFumbRec
    playerStatsDefHome['sacks'] = homeSacks
    playerStatsDefAway['name'] = awayName
    playerStatsDefAway['team'] = awayTeam
    playerStatsDefAway['defInts'] = awayInts
    playerStatsDefAway['defTds'] = awayTds
    playerStatsDefAway['defFumbRec'] = awayFumbRec
    playerStatsDefAway['sacks'] = awaySacks

    playerList.append(list(playerStatsDefHome.values()))
    playerList.append(list(playerStatsDefAway.values()))    

    #for item in playerList:
    #    print(item)
    
    path = r'/Users/kanemnoel/Desktop/fantasy-fb-app/game_stats_csv/' + hometeam_abbr + year + month + day + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + '.csv'
    pd.DataFrame(playerList, columns=column_names).to_csv(path, index = False, header=True)
    
def getGames():
    
    gamesDF = getTable('https://www.pro-football-reference.com/years/2020/games.htm', 'games', header=True)

    start = []
    home_team = []
    away_team = []
    for i in range(0, gamesDF.shape[0]):
        start.append('')
        home_team.append('')
        away_team.append('')
    gamesDF['Start'] = start
    gamesDF['HomeTeam'] = home_team
    gamesDF['AwayTeam'] = away_team

    def add_Start_HomeTeam_AwayTeam(series):

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

        if getMonth(series) == '01':
            series.Start = '2021-' + getMonth(series) + '-' + getDay(series) + ' ' + standardToMilitary(series)
        else:
            series.Start = '2020-' + getMonth(series) + '-' + getDay(series) + ' ' + standardToMilitary(series)
        
        #x = any(series == '@')
        #if x == True:

        if any(series == '@'):
            series.HomeTeam = longNameToAbbr(series.L)
            series.AwayTeam = longNameToAbbr(series.W)
        else:
            series.HomeTeam = longNameToAbbr(series.W)
            series.AwayTeam = longNameToAbbr(series.W)

    gamesDF.rename(columns={'Winner/tie': 'W', 'Loser/tie': 'L'}, inplace=True)
    gamesDF.apply(add_Start_HomeTeam_AwayTeam, axis=1)
    #gamesDF.drop(columns=['Day', 'Date', 'Time', 'W', 'L', 'PtsW', 'PtsL', 'YdsW', 'TOW', 'YdsL', 'TOL', 'Month', 'TimeTemp', ''], axis=1)
    
    path = r'/Users/kanemnoel/Desktop/fantasy-fb-app/games_csv/' + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + '.csv'
    gamesDF.to_csv(path, index = False, header=True)
        
def getTeamRoster(abbr: str):
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

def getAllTeamRosters():
    
    for team in teamDict:
        path = r'/Users/kanemnoel/Desktop/fantasy-fb-app/team_roster_csv/' + team + '/' + team + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + '.csv'
        getTeamRoster(team).to_csv(path, index = False, header=True)

def getTable(url: str, tableID: str, header=True):
    
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    
    table = soup.find('table', id=tableID)
    table_body = table.find('tbody')
    rows = table_body.findAll('tr', {'class': None})
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
    
    return data

def getTagTextByClass(url: str, tagType: str, tagClass: str, multiple=False):

    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')

    if multiple:
        tags = soup.findAll(tagType, {'class': tagClass})
        tagList = []
        for tag in tags:
            tagList.append(tag.text)
        return tagList    

    return soup.find(tagType, {'class': tagClass}).text

getAllTeamRosters()
getGames()
getGameStats('TB', '2020', '11', '08')