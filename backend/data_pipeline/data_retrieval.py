import player_info
import constants
from nba_api.stats.endpoints import (
    playergamelog as plg,
    boxscoreadvancedv2 as bsa,
    commonteamroster as ctr,
    playergamelogs as plgs,
)
from nba_api.stats.library.parameters import SeasonAll

"""
File primarily responsible for pulling raw data from nba_api. Some, but minimal data processing is
performed. Data pulled includes player game logs, game logs for specific matchups, 
advanced box score statistics, ...

Parameters:
player_id: int that corresponds with the requested player
game_id: int that corresponds with the requested game
numGames: int that corresponds to the number of games requested
team: three-letter uppercase abbreviation that corresponds to the requested team
opp_team: three-letter uppercase abbreviation that corresponds to the opposing team
"""

def getGameLog(player_id, numGames = 82, start_date = None, end_date = None):
    """
    Returns a modified data frame containing the game log of the specified player. 
    Irrelevant columns are removed. Only retrieves games of the current season. If no
    start_date and end_date are specified, the game log pulls the most recent games. 
    """
    # If a specific time period is specified (typically for training the model)
    if start_date and end_date:
        gamelog = plg.PlayerGameLog(player_id=player_id, date_from_nullable=start_date, date_to_nullable=end_date, season=SeasonAll.all).get_data_frames()[0].head(numGames)
        gamelog = gamelog.drop(['SEASON_ID','Player_ID','VIDEO_AVAILABLE'], axis=1)
        return gamelog
    # If only the most recent games are requested
    else:
        gamelog = plg.PlayerGameLog(player_id=player_id, season=SeasonAll.all).get_data_frames()[0].head(numGames)
        gamelog = gamelog.drop(['SEASON_ID','Player_ID','VIDEO_AVAILABLE'], axis=1)
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

def getTeamRoster(team):
    """
    Returns the current roster of the specified team as a list of player ids. 
    """
    roster = ctr.CommonTeamRoster(team_id = constants.abbrev_to_id[team])
    return roster.get_data_frames()[0]['PLAYER_ID'].tolist()
