import pandas as pd
import requests, bs4
import re
from datetime import datetime

teamdict = {
    'ARI': 'crd',
    'ATL': 'atl',
    'BAL': 'rav',
    'BUF': 'buf',
    'CAR': 'car',
    'CHI': 'chi',
    'CIN': 'cin',
    'CLE': 'cle',
    'DAL': 'dal',
    'DEN': 'den',
    'DET': 'det',
    'GB': 'gnb',
    'HOU': 'htx',
    'IND': 'clt',
    'JAX': 'jax',
    'KC': 'kan',
    'LAC': 'sdg',
    'LAR': 'ram',
    'LV': 'rai',
    'MIA': 'mia',
    'MIN': 'min',
    'NE': 'nwe',
    'NO': 'nor',
    'NYG': 'nyg',
    'NYJ': 'nyj',
    'PHI': 'phi',
    'PIT': 'pit',
    'SEA': 'sea',
    'SF': 'sfo',
    'TB': 'tam',
    'TEN': 'oti',
    'WAS': 'was'
}

teamdict2 = {
    'ARI': 'Arizona Cardinals',
    'ATL': 'Atlanta Falcons',
    'BAL': 'Baltimore Ravens',
    'BUF': 'Buffalo Bills',
    'CAR': 'Carolina Panthers',
    'CHI': 'Chicago Bears',
    'CIN': 'Cincinnati Bengals',
    'CLE': 'Cleveland Browns',
    'DAL': 'Dallas Cowboys',
    'DEN': 'Denver Broncos',
    'DET': 'Detroit Lions',
    'GB': 'Green Bay Packers',
    'HOU': 'Houston Texans',
    'IND': 'Indianapolis Colts',
    'JAX': 'Jacksonville Jaguars',
    'KC': 'Kansas City Chiefs',
    'LAC': 'Los Angeles Chargers',
    'LAR': 'Los Angeles Rams',
    'LV': 'Las Vegas Raiders',
    'MIA': 'Miami Dolphins',
    'MIN': 'Minnesota Vikings',
    'NE': 'New England Patriots',
    'NO': 'New Orleans Saints',
    'NYG': 'New York Giants',
    'NYJ': 'New York Jets',
    'PHI': 'Philadelphia Eagles',
    'PIT': 'Pittsburgh Steelers',
    'SEA': 'Seattle Seahawks',
    'SF': 'San Francisco 49ers',
    'TB': 'Tampa Bay Buccaneers',
    'TEN': 'Tennessee Titans',
    'WAS': 'Washington Football Team'
}

def standardToMilitary(series):
    def update(time):
        time.strip()
        hour = time.split(':')[0]
        minute = time.split(':')[1]
        amOrPm = minute[-2:]
        minute = minute[:-2]
        if amOrPm == 'PM':
            if hour != '12':
                hour = int(hour)
                hour += 12
                hour = str(hour)
        elif amOrPm =='AM':
            if hour == '12':
                hour = int(hour)
                hour += 12
                hour = str(hour)
        if len(hour) == 1:
            hour = '0' + hour  
        return(hour + ':' + minute + ':00')

        series.TimeTemp = update(series.Time)

def monthToNum(series):
        months = {
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
        month = series.Date.split()[0]
        day = series.Date.split()[1]
        series.Month = months.get(month)
        series.Day = day

def addStart(series):
    if series.Month == '01':
        series.Start = '2021-' + series.Month + '-' + series.Day + ' ' + series.TimeTemp
    else:
        series.Start = '2020-' + series.Month + '-' + series.Day + ' ' + series.TimeTemp

def addHomeAway(series):
    x = any(series == '@')
    if x == True:
        series.HomeTeam = list(teamdict2.keys())[list(teamdict2.values()).index(series.L)]
        series.AwayTeam = list(teamdict2.keys())[list(teamdict2.values()).index(series.W)]
    else:
        series.HomeTeam = list(teamdict2.keys())[list(teamdict2.values()).index(series.W)]
        series.AwayTeam = list(teamdict2.keys())[list(teamdict2.values()).index(series.L)]        

def scrapeGameScoresAndResult(series):
    x = series.HomeTeam
    hometeam = teamdict.get(x)
    print(x)
    print(hometeam)
    url = 'https://www.pro-football-reference.com/teams/' + hometeam + '/2020/gamelog/'
    df = pullTable(url, 'gamelog2020', header=True)

    print(df)

    #mask = df['Week'] == series.Week

    #if df.loc[df['Week'] == series.Week]:


def scrapeGames():
    df = pullTable('https://www.pro-football-reference.com/years/2020/games.htm', 'games', header=True)

    start = []
    month = []
    day = []
    time = []
    home_team = []
    away_team = []
    home_points = []
    away_points = []
    winner = []
    loser = []
    tie1 = []
    tie2 = []

    count_row = df.shape[0]
    for i in range(0, count_row):
        start.append('')
        month.append('')
        day.append('')
        time.append('')
        home_team.append('')
        away_team.append('')
        home_points.append(0)
        away_points.append(0)
        winner.append('')
        loser.append('')
        tie1.append('')
        tie2.append('')

    df['Start'] = start
    df['Month'] = month
    df['Day'] = day
    df['TimeTemp'] = time
    df['HomeTeam'] = home_team
    df['AwayTeam'] = away_team
    df['HomePoints'] = home_points
    df['AwayPoints'] = away_points
    #df['Winner'] = winner
    #df['Loser'] = loser
    #df['Tie1'] = tie1
    #df['Tie2'] = tie2

    df.rename(columns={'Winner/tie': 'W', 'Loser/tie': 'L'}, inplace=True)
    df.apply(standardToMilitary, axis=1)
    df.apply(monthToNum, axis=1)
    df.apply(addStart, axis=1)
    df.apply(addHomeAway, axis=1)
    #df.apply(scrapeGameScoresAndResult, axis=1)
    print(df)

    df.to_csv (r'./games-scrape/games.csv')

def pullRosters():
    for key, value in teamdict.items():
        url = 'https://www.pro-football-reference.com/teams/' + value + '/2020_roster.htm'
        df = pullTable(url, "games_played_team", header=True)
        
        id_arr = []
        team_arr = []
        qb_arr = []
        rb_arr = []
        wr_arr = []
        te_arr = []
        k_arr = []
        dst_arr = []
        
        count_row = df.shape[0]
        for i in range(0, count_row):
            id_arr.append('')
            team_arr.append(key)
            qb_arr.append(0)
            rb_arr.append(0)
            wr_arr.append(0)
            te_arr.append(0)
            k_arr.append(0)
            dst_arr.append(0)

        df['ID'] = id_arr
        df['Team'] = team_arr
        df['QB'] = qb_arr
        df['RB'] = rb_arr
        df['WR'] = wr_arr
        df['TE'] = te_arr
        df['K'] = k_arr
        df['D/ST'] = dst_arr

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

        df.to_csv (r'./team-roster-scrapes/' + key + '.csv')

def findTables(url):
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    divs = soup.findAll('div', id = "content")
    divs = divs[0].findAll("div", id = re.compile("^all"))
    ids = []
    for div in divs:
        searchme = str(div.findAll("table"))
        x = searchme[searchme.find("id") + 3: searchme.find(">")]
        x = x.replace("\"", "")
        if len(x) > 0:
            ids.append(x)
    return(ids)

def pullTable(url, tableID, header = True):
    res = requests.get(url)
    ## Work around comments
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    tables = soup.findAll('table', id = tableID)
    data_rows = tables[0].findAll('tr')
    game_data = [[td.getText() for td in data_rows[i].findAll(['th', 'td'])]
        for i in range(len(data_rows))
        ]
    data = pd.DataFrame(game_data)
    if header == True:
        data_header = tables[0].findAll('thead')
        data_header = data_header[0].findAll('tr')
        data_header = data_header[0].findAll('th')
        header = []
        for i in range(len(data.columns)):
                header.append(data_header[i].getText())
        data.columns = header
        data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    return(data)

scrapeGames()