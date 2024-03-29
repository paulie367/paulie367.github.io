import requests
from bs4 import BeautifulSoup
import pandas as pd

year=input("Which NBA season are you interested in?: ")
player=input("For which player do you want to get stats?: ")

def get_NBA_stats():
    url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'.format(year)

    r = requests.get(url, verify=False)
    #원래는 r = requests.get(url)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')
    table=soup.find_all(class_="full_table")
    """ Extracting List of column names"""

    head=soup.find(class_="thead")
    column_names_raw=[head.text for item in head][0]
    column_names_polished=column_names_raw.replace("\n",",").split(",")[2:-1]

    #print(column_names_polished)

    """Extracting full list of player_data"""
    players=[]
        
    for i in range(len(table)):
            
        player_=[]
            
        for td in table[i].find_all("td"):
            player_.append(td.text)
        
        players.append(player_)


    df=pd.DataFrame(players, columns=column_names_polished).set_index("Player")

    #cleaning the player's name from occasional special characters
    df.index=df.index.str.replace('*', '')
    print(df.loc[player])

if __name__ == "__main__":
    get_NBA_stats()
