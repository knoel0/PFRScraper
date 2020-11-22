teams = {
    'ARI': {
        'Abbr Url': 'crd',
        'Full Name': 'Arizona Cardinals'
    },
    'ATL': {
        'Abbr Url': 'atl',
        'Full Name': 'Atlanta Falcons'
    },
    'BAL': {
        'Abbr Url': 'rav',
        'Full Name': 'Baltimore Ravens'
    },
    'BUF': {
        'Abbr Url': 'buf',
        'Full Name': 'Buffalo Bills'
    },
    'CAR': {
        'Abbr Url': 'car',
        'Full Name': 'Carolina Panthers'
    },
    'CHI': {
        'Abbr Url': 'chi',
        'Full Name': 'Chicago Bears'
    },
    'CIN': {
        'Abbr Url': 'cin',
        'Full Name': 'Cincinnati Bengals'
    },
    'CLE': {
        'Abbr Url': 'cle',
        'Full Name': 'Cleveland Browns'
    },
    'DAL': {
        'Abbr Url': 'dal',
        'Full Name': 'Dallas Cowboys'
    },
    'DEN': {
        'Abbr Url': 'den',
        'Full Name': 'Denver Broncos'
    },
    'DET': {
        'Abbr Url': 'det',
        'Full Name': 'Detroit Lions'
    },
    'GB': {
        'Abbr Url': 'gnb',
        'Full Name': 'Green Bay Packers'
    },
    'HOU': {
        'Abbr Url': 'htx',
        'Full Name': 'Houston Texans'
    },
    'IND': {
        'Abbr Url': 'clt',
        'Full Name': 'Indianapolis Colts'
    },
    'JAX': {
        'Abbr Url': 'jax',
        'Full Name': 'Jacksonville Jaguars'
    },
    'KC': {
        'Abbr Url': 'kan',
        'Full Name': 'Kansas City Chiefs'
    },
    'LAC': {
        'Abbr Url': 'sdg',
        'Full Name': 'Los Angeles Chargers'
    },
    'LAR': {
        'Abbr Url': 'ram',
        'Full Name': 'Los Angeles Rams'
    },
    'LV': {
        'Abbr Url': 'rai',
        'Full Name': 'Las Vegas Raiders'
    },
    'MIA': {
        'Abbr Url': 'mia',
        'Full Name': 'Miami Dolphins'
    },
    'MIN': {
        'Abbr Url': 'min',
        'Full Name': 'Minnesota Vikings'
    },
    'NE': {
        'Abbr Url': 'nwe',
        'Full Name': 'New England Patriots'
    },
    'NO': {
        'Abbr Url': 'nor',
        'Full Name': 'New Orleans Saints'
    },
    'NYG': {
        'Abbr Url': 'nyg',
        'Full Name': 'New York Giants'
    },
    'NYJ': {
        'Abbr Url': 'nyj',
        'Full Name': 'New York Jets'
    },
    'PHI': {
        'Abbr Url': 'phi',
        'Full Name': 'Philadelphia Eagles'
    },
    'PIT': {
        'Abbr Url': 'pit',
        'Full Name': 'Pittsburgh Steelers'
    },
    'SEA': {
        'Abbr Url': 'sea',
        'Full Name': 'Seattle Seahawks'
    },
    'SF': {
        'Abbr Url': 'sfo',
        'Full Name': 'San Francisco 49ers'
    },
    'TB': {
        'Abbr Url': 'tam',
        'Full Name': 'Tampa Bay Buccaneers'
    },
    'TEN': {
        'Abbr Url': 'oti',
        'Full Name': 'Tennessee Titans'
    },
    'WAS': {
        'Abbr Url': 'was',
        'Full Name': 'Washington Football Team'
    }
}

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

stats_template = {
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

def urlabbr_to_abbr(urlabbr: str) -> str:
    for abbr, nestedDict in teams.items():
        for key, value in nestedDict.items():
            if value == urlabbr:
                return abbr

def longname_to_abbr(longname: str) -> str:
    for abbr, nestedDict in teams.items():
        for key, value in nestedDict.items():
            if value == longname:
                return abbr

def substring_to_abbr(substring: str) -> str:
    for abbr, nestedDict in teams.items():
        for key, value in nestedDict.items():
            if substring in value:
                return abbr

def abbr_to_teamname_end(abbr: str) -> str:
    if len(teams[abbr]["Full Name"].split()) == 3:
        return teams[abbr]["Full Name"].split()[2]
    else:
        return teams[abbr]["Full Name"].split()[1]