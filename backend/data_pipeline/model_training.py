import pickle
import data_processing as dp
import data_retrieval as dr
import pandas as pd
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
def train_player_pts_model(player_id):
    """

    """
    gamelog = dr.getGameLog(player_id, numGames=82)
    game_id_list = gamelog["Game_ID"].values
    # print(game_id_list)
    features = []
    results = []
    features.append(dp.getlastNGamesAvg(player_id, "PTS", numGames = 5))
    features.append(dp.getSeasonAvg(player_id, "PTS"))
    print(features)

train_player_pts_model(203999)