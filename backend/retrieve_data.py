import player_info
import pandas as pd
from nba_api.stats.endpoints import playergamelog as plg
from nba_api.stats.endpoints import boxscoreadvancedv2 as bsa

"""
File primarily responsible for pulling raw data from nba_api. Minimal data processing is
performed. Data pulled includes player game logs, game logs for specific matchups, 
advanced box score statistics, ...
"""

def getGameLog(player_id, numGames = 82):
    """
    Returns a modified data frame containing the game log of the specified player. 
    Irrelevant columns are removed. Only retrieves games of the current season.
    """
    gamelog = plg.PlayerGameLog(player_id=player_id).get_data_frames()[0].head(numGames)
    gamelog = gamelog.drop(['SEASON_ID','Player_ID','GAME_DATE','VIDEO_AVAILABLE'], axis=1)
    return gamelog

def getPrevMatchupLog(player_id, opp_team):
    """
    Returns a modified data frame containing the game log of the specified player
    against a specific team. Irrelavent columns are removed.
    """
    gamelog = getGameLog(player_id)
    selected_games = gamelog[gamelog['MATCHUP'].str.contains(opp_team)]
    return selected_games

def getAdvancedBoxScore(player_id, game_id):
    """
    Returns the advanced statisitics for a specific player in a specific game.
    """
    boxscore = bsa.BoxScoreAdvancedV2(game_id = game_id).get_data_frames()[0]
    selected_line = boxscore[boxscore['PLAYER_ID'] == player_id]
    return selected_line

def get