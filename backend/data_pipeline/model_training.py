import pickle
import data_processing as dp
import data_retrieval as dr
import pandas as pd
import math
import time 
import random as rand
"""
Features: lastNGamesAvg, seasonAvg, matchupAvg, recentUsgRate, missingLineUpStrength, OppDefRating, bettingLine

Outputs: 0 (under), 1 (over)

TODO:
1. For training the model, a function that scrapes player stat totals and either adds N or subtracts N and records that number as the betting line.
If +, the function adds a 0 to the results list. If -, the function adds a 1 to the results list. Ideally, this function would
take the game_ID as the input. This way, we can just loop through one player's games.

NOTE:
Look into training a Linear Regression model to find the quantitative PPG/stat values instead of a binary classification from the Logistic Regression

"""
def getFeatures(player_id, team, stat_type, numGames, id, opp_team,game_features):
        """
        Modifies the list game_features to add all the features. Returns true if offset is positive, 
        false if offset is negative.
        """
        opp_team = dp.getOppTeamAbbrev(game_id=id, team=team)
        # Adding the avg of the last N games
        game_features.append(dp.getlastNGamesAvg(player_id, stat_type, numGames, game_id=id))

        # Adding the season avg
        game_features.append(dp.getSeasonAvg(player_id, stat_type, game_id=id))

        # Adding the matchup avg
        game_features.append(dp.getMatchupAvg(player_id, stat_type, opp_team, game_id=id))

        # Adding the length of the matchup log (Greater length means more weight should be placed on Matchup Avg)
        game_features.append(dp.getPrevMatchupLogLength(player_id, opp_team))

        # Adding the recent usage rate
        game_features.append(dp.getRecentUsageRate(player_id, numGames, game_id=id))
        
        time.sleep(0.5)

        # Adding the past lineup strength
        try:
            game_features.append(dp.getPastMissingLineupStrength(team, player_id, id))
        except Exception as e:
            game_features.append(0)     

        # Adding the betting line
        offset = 0
        while offset == 0:
            offset = rand.randint(-4,4)
        betting_line = dp.getPointsScored(player_id,game_id=id).values + offset
        print(betting_line)
        game_features.append(betting_line[0])

        print(game_features)

        if offset > 0:
            return True
        else: 
            return False

def train_player_pts_model_2022_2023(player_id, team, numGames):
    """
    params:
    player_id : int that corresponds to a specific player
    team: string with the three letter abbreviation for the specified player's NBA team 
    numGames: int that specifies the number of games to train the model on
    """
    gamelog = dr.getGameLog(player_id, numGames=82)
    game_id_list = gamelog["Game_ID"].values
    game_id_list = game_id_list[20:]
    accum = 0 # Temp for testing purposes
    model_input = [[],[]]

    for id in game_id_list:
        opp_team = dp.getOppTeamAbbrev(game_id=id, team=team)

        accum+=1
        print(accum)

        game_features = []
        under = getFeatures(player_id=player_id,team=team,numGames=numGames,stat_type="PTS",id=id,opp_team=opp_team,game_features=game_features)
        print("HERE DUMBASS")
        # Delay to stop nba.com from refusing requests
        time.sleep(0.5)

        if under:
            result = 0 # Under b/c the offset made the line too high (adding a positive)
        else:
            result = 1 # Over b/c the offset made the line too low (adding a negative)

        # Get rid of any nan instances (occurs when there are no prev. matchup data etc.)
        if not any(math.isnan(feature) for feature in game_features):
            model_input[0].append(game_features)
            model_input[1].append(result)
    
    print(model_input)

train_player_pts_model_2022_2023(player_id=203999, team="DEN", numGames = 5)