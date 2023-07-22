import requests
from bs4 import BeautifulSoup
import io
import requests
import PyPDF2
import constants as constants
import time


""" 
File that scrapes web data from ESPN.com and NBA.com. Seperated from nba_api data retrieval.

Params:
date: string with the date of the game in the format (year+month+day). Feb 11th, 2023 -> 20230211
visiting_team: the three-letter abbreviation for the visiting team
home_team: the three-letter abbreviation for the home team
requested_team: the three-letter abbreviation for the team from which the injury report is requested
"""

def getInjuryReport(team):
    """
    Returns a list with all the players that are listed as injured according 
    to the ESPN injury report. This function is meant to be used to access the 
    current/updated injury report (model inputs)
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

def getPastInjuryReport(date, visiting_team, home_team, requested_team):
    """
    Returns a list with all the players that are listed as injured
    according to NBA.com. This function is meant to be used to access the 
    injury report for past games (training the model)
    """
    url = 'https://statsdmz.nba.com/pdfs/' + date + '/' + date + '_' + visiting_team + home_team + '.pdf'
    #print(url)
    response = requests.get(url)

    # Read the content of the PDF into a file-like object
    pdf_file = io.BytesIO(response.content)

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract the text from each page of the PDF
    all_text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        all_text += page_text

    lines = all_text.split('\n')
    injury_line = ""
    first_line = False
    ended = False
    # Cutting out some useless data
    for line in lines[400:]:
        # Conditionals to account for line spillover
        if first_line and "Points" in line:
            break
        if first_line and "Inactive" in line:
            ended = True        
        if first_line and ended == False:
            injury_line += line        
        if "Inactive" in line and constants.abbrev_to_nickname[requested_team] in line:
            injury_line += line
            first_line = True
        else:
            pass

    # print("injury_line: " + injury_line)
    
    return _getPastInjuryReportHelper(injury_line)

def _getPastInjuryReportHelper(string):
    """
    Extracts the last names out of the PDF line.
    """
    # Remove unnecessary text at the beginning
    start_index = string.find('-') + 1
    string = string[start_index:]

    # Remove parentheses and their contents
    while '(' in string:
        opening_index = string.find('(')
        closing_index = string.find(')')
        if closing_index > opening_index:
            string = string[:opening_index] + string[closing_index+1:]
    # Split the remaining string by commas
    names_list = [name.strip() for name in string.split(',')]
    return names_list

#TODO: Determine suitable website to pull data from that is updated daily. May need to wait until the NBA season starts
def getDefensiveRating(opp_team):
    """
    Returns the most recent defensive rating of the specified team. This function is meant to be called for actual predictions

    params:
    opp_team : string containing the three-letter abbreviation of the requested team
    """
    pass

def getPastDefensiveRating(date, opp_team):
    """
    Returns the defensive rating of the specified team up until the specified date. This function is meant to be called for training
    a model

    params:
    date : 
    opp_team : string containing the three-letter abbreviation of the requested team
    """
    url = "https://www.teamrankings.com/nba/stat/defensive-efficiency?date=" + date[:4] + "-" + date[4:6] + "-" + date[6:8]
    # print(url)
    response = requests.get(url)

    # Create a beautiful soup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the container that holds the injury information
    container = soup.find("table")

    # Get table headers and rows
    headers = [th.getText() for th in container.find_all('tr')[0].find_all('th')]
    rows = container.find_all('tr')[1:]

    # Extract the data for the specific team
    for row in rows:
        team_row = {headers[i]: td.getText() for i, td in enumerate(row.find_all('td'))}
        if team_row.get('Team') in constants.abbrev_to_city[opp_team]:
            try:
                float(team_row.get('2022'))
            except ValueError:
                return None
            return float(team_row.get('2022'))

# print(getPastDefensiveRating("20230118","BOS"))