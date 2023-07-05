import data_retrieval as dr
import webscrapers as ws
import numpy as np
import player_info

"""
File primarily responsible for processing the data pulled from nba_api. Function
outputs are meant to be used as model training features after proper scaling.
"""

def getlastNGamesAvg(player_id, stat_type, numGames):
    """
    Returns the average value of a statistics type of a player over recent games.
    """
    gamelog = dr.getGameLog(player_id, numGames)
    try:
        stat_col = gamelog[stat_type]
    except KeyError:
        raise Exception("Invalid statistics type")
    
    return np.mean(np.array(stat_col))

def getSeasonAvg(player_id, stat_type):
    """
    Returns the average value of a statistics type of a player over the entire current season.
    """
    gamelog = dr.getGameLog(player_id, stat_type)
    try:
        stat_col = gamelog[stat_type]
    except KeyError:
        raise Exception("Invalid statistics type")
    
    return np.mean(np.array(stat_col))

def getMatchupAvg(player_id, stat_type, opp_team):
    """
    Returns the average value of a statistics type of a player in games against a specific team.
    """
    gamelog = dr.getPrevMatchupLog(player_id, opp_team)
    try:
        stat_col = gamelog[stat_type]
    except KeyError:
        raise Exception("Invalid statistics type")
    
    return np.mean(np.array(stat_col))

def getRecentUsageRate(player_id, numGames):
    """
    Returns the usage rate of a player over recent games. 
    """
    gamelog = dr.getGameLog(player_id, numGames)
    list = []
    for entry in gamelog['Game_ID']:
        list.append(dr.getAdvancedBoxScore(player_id,entry)['USG_PCT'])

    return np.mean(np.array(list))

def getMissingLineupStrength(team):
    """
    Returns the calculated line-up strength. The line-up strength is calculated according
    to the [usg_pct sum of injured players]. 

    Ex. If Nikola Jokic (usg_pct = .25) and Jamal Murray (usg_pct = .15) are injured, the
    missing line-up strength is 0.40
    """
    injuredlist = ws.getInjuryReport(team)
    usg_sum = 0
    for player in injuredlist:
        split = player.split()
        player_obj = player_info.Player(firstName=split[0], lastName=split[1], active=True, team=team)
        usg_sum += getRecentUsageRate(player_obj.player_id,4)
    
    return usg_sum

def getOppDefRating(team_id):
    pass