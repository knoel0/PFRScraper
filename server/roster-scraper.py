import pandas as pd
import requests, bs4
import re

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
        
        count_row = df.shape[0]
        for i in range(0, count_row):
            id_arr.append('')
            team_arr.append(key)
            qb_arr.append(0)
            rb_arr.append(0)
            wr_arr.append(0)
            te_arr.append(0)
            k_arr.append(0)

        df['ID'] = id_arr
        df['Team'] = team_arr
        df['QB'] = qb_arr
        df['RB'] = rb_arr
        df['WR'] = wr_arr
        df['TE'] = te_arr
        df['K'] = k_arr

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
    print(ids)
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

pullRosters()