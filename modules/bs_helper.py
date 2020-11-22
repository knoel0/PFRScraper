import pandas as pd
import requests, bs4
import re

def get_table(url: str, table_id: str, header=True) -> pd.DataFrame:
    
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    
    table = soup.find('table', id=table_id)
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
    data.columns = data.columns.str.strip()
    
    return data

def get_tagtext_by_class(url: str, tag_type: str, tag_class: str) -> str:

    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml') 

    return soup.find(tag_type, {'class': tag_class}).text    

def get_all_tagtext_by_class(url: str, tag_type: str, tag_class: str) -> list: 
    
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')

    tags = soup.findAll(tag_type, {'class': tag_class})
    tag_list = []
    for tag in tags:
        tag_list.append(tag.text)
    
    return tag_list