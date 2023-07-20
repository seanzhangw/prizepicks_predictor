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