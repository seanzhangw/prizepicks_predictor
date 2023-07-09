import constants as constants
import data_retrieval as dr
import data_scrappers as ws
import pandas as pd
import numpy as np
import player_info as player_info


"""
File primarily responsible for processing the data pulled from nba_api. Function
outputs are meant to be used as model training features after proper scaling.

Parameters:
player_id: int that corresponds with the requested player
stat_type: string that corresponds with the requested statistic (abbreviated)
numGames: int that corresponds to the number of games requested
team: three-letter uppercase abbreviation that corresponds to the requested team
opp_team: three-letter uppercase abbreviation that corresponds to the opposing team
game_id: string that corresponds to the requested game
"""

def getlastNGamesAvg(player_id, stat_type, numGames, game_id = None):
    """
    Returns the average value of a statistics type of a player over recent games.
    """
    gamelog = dr.getGameLog(player_id, numGames, game_id=game_id)
    try:
        stat_col = gamelog[stat_type]
    except KeyError:
        raise Exception("Invalid statistics type")
    
    return np.mean(np.array(stat_col))

# print(getlastNGamesAvg(203999, 'PTS', 5))

def getSeasonAvg(player_id, stat_type, game_id = None):
    """
    Returns the average value of a statistics type of a player over the entire current season.
    """
    gamelog = dr.getGameLog(player_id, game_id = game_id)
    try:
        stat_col = gamelog[stat_type]
    except KeyError:
        raise Exception("Invalid statistics type")
    
    return np.mean(np.array(stat_col))

def getMatchupAvg(player_id, stat_type, opp_team, game_id = None):
    """
    Returns the average value of a statistics type of a player in games against a specific team.
    """
    gamelog = dr.getPrevMatchupLog(player_id, opp_team, game_id)
    try:
        stat_col = gamelog[stat_type]
    except KeyError:
        raise Exception("Invalid statistics type")
    
    return np.mean(np.array(stat_col))

def getRecentUsageRate(player_id, numGames = 82, game_id = None):
    """
    Returns the usage rate of a player over recent games. 
    """
    gamelog = dr.getGameLog(player_id, numGames,game_id=game_id)
    list = []
    for entry in gamelog['Game_ID']:
        list.append(dr.getAdvancedBoxScore(player_id,entry)['USG_PCT'])

    return np.mean(np.array(list))

def _getPastUsageRate(player_id, numGames, game_date):
    """
    Returns the usage rate of a player before the game specified by game_id
    """
    gamelog = dr.getGameLog(player_id)
    if not gamelog.empty:
        list = []
        for index, row in gamelog.iterrows():
            date_value = row["GAME_DATE"]
            date_obj = pd.to_datetime(date_value, format="%b %d, %Y")
            formatted_date = date_obj.strftime("%Y%m%d")
            if formatted_date < game_date:
                list.append(dr.getAdvancedBoxScore(player_id,row["Game_ID"])['USG_PCT'])
                if len(list) == numGames:
                    break

        return np.mean(np.array(list))

def getMissingLineupStrength(team):
    """
    Returns the calculated line-up strength. The line-up strength is calculated according
    to the [usg_pct sum of injured players]. This function is meant to access the current/
    updated injury report (Model inputs)

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

def getPastMissingLineupStrength(team, player_id, game_id):
    """
    Returns the calculated line-up strength. The line-up strength is calculated according
    to the [usg_pct sum of injured players]. This function is meant to access past injury reports 
    (training the model)

    Ex. If Nikola Jokic (usg_pct = .25) and Jamal Murray (usg_pct = .15) are injured, the
    missing line-up strength is 0.40
    """
    gamelog = dr.getGameLog(player_id)
    #print(gamelog)
    selected_game = gamelog[gamelog['Game_ID'].str.contains(game_id)]

    # Extract the right date
    date_value = selected_game["GAME_DATE"].values[0]
    date_obj = pd.to_datetime(date_value, format="%b %d, %Y")
    formatted_date = date_obj.strftime("%Y%m%d")

    # Extract the visiting and home team
    matchup_line = selected_game["MATCHUP"].values[0]
    if "@" in matchup_line:
        visiting_team=matchup_line[:3]
        home_team=matchup_line[matchup_line.index("@")+2:]
    else:
        home_team = matchup_line[:3]
        visiting_team=matchup_line[matchup_line.index(".")+2:]
  
    injured_list = ws.getPastInjuryReport(date=formatted_date, visiting_team=visiting_team, home_team=home_team,requested_team=team)

    usg_sum = 0
    for player in injured_list:
        player_obj = player_info.Player(lastName=player, active=True, team=team)
        sum = _getPastUsageRate(player_obj.player_id, 2, formatted_date)
        if sum:
            usg_sum += sum

    return usg_sum

def getOppDefRating(team_id):
    pass