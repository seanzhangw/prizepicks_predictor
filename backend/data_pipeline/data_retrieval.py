import constants 
from nba_api.stats.endpoints import (
    playergamelog as plg,
    boxscoreadvancedv2 as bsa,
    commonteamroster as ctr,
    boxscoretraditionalv2 as bst
)
import pandas as pd
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

def getGameLog(player_id, numGames = 82, game_id = None):
    """
    Returns a modified data frame containing the game log of the specified player. 
    Irrelevant columns are removed. Only retrieves games of the current season. If a
    game_id is entered, only games before game_id are returned (inclusive)
    """
    if game_id:
        full_log = plg.PlayerGameLog(player_id=player_id).get_data_frames()[0]
        filtered_df = full_log[full_log['Game_ID'] < game_id].head(numGames).drop(['SEASON_ID','Player_ID','VIDEO_AVAILABLE'], axis=1)
        return filtered_df
    else:
        gamelog = plg.PlayerGameLog(player_id=player_id).get_data_frames()[0].head(numGames)
        gamelog = gamelog.drop(['SEASON_ID','Player_ID','VIDEO_AVAILABLE'], axis=1)
        return gamelog

def getPrevMatchupLog(player_id, opp_team, game_id = None):
    """
    Returns a modified data frame containing the game log of the specified player
    against a specific team. Irrelavent columns are removed.
    """
    gamelog = getGameLog(player_id = player_id, game_id = game_id)
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

def getTraditionalBoxScore(game_id):
    """
    """
    return bst.BoxScoreTraditionalV2(game_id=game_id).get_data_frames()[0]

# def getGameDate(game_id):
#     lgf_df = lgf.LeagueGameFinder(player_or_team_abbreviation="DEN", game_id_nullable = game_id).get_data_frames()
#     game_date = lgf_df[0]['GAME_DATE'].values[0]

#     return game_date
# print(getGameDate('0022201126'))

# # print(getGameLog(203999))

