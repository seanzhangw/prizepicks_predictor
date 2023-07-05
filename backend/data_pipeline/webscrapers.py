import requests
from bs4 import BeautifulSoup

def getInjuryReport(team):
    """
    Returns a list with all the players that are listed as injured according 
    to the ESPN injury report
    """
    injurylist = []
    # Send a GET request to the URL
    url = 'https://www.espn.com/nba/team/injuries/_/name/' + team.lower()
    response = requests.get(url)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the container that holds the injury information
    container = soup.find(class_='Wrapper Card__Content')

    player_names = soup.find_all('span', class_='Athlete__PlayerName')
    for player in player_names:
        player_name = player.text.strip()
        injurylist.append(player_name)
    
    return injurylist

