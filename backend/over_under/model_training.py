import pickle
import data_processing as dp
import data_retrieval as dr
import math
import time 
import random as rand
import csv
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
import numpy as np
"""
Features: lastNGamesAvg, seasonAvg, matchupAvg, recentUsgRate, missingLineUpStrength, OppDefRating, bettingLine

Outputs: 0 (under), 1 (over)

TODO:
1. For training the model, a function that scrapes player stat totals and either adds N or subtracts N and records that number as the betting line.
If +, the function adds a 0 to the results list. If -, the function adds a 1 to the results list. Ideally, this function would
take the game_ID as the input. This way, we can just loop through one player's games.

NOTE:
Notable models:
7/19/23 
2022-2023 NBA season player points model trained with Joel Embiid (203594), Nikola Jokic (203999), and Lebron James (2544)
- Logistic Regression, "saga" algorithim, c hyperparameter = 0.13, LASSO ("l1") regression achieved 0.60 accuracy. 
- Features include lastNGamesAvg, seasonAvg, matchupAvg, prevMatchupLogLength, recentUsageRate. 
- Betting lines were established with a plus_minus of 4, so an average of two points from the actual line.

7/21/23
2022-2023 NBA season player points model trained with Joel Embiid (203594), Nikola Jokic (203999), and Lebron James (2544)
- Logistic Regression, "saga" algorithim, c hyperparameter = 0.45, lASSO ("l1") regression achieved 0.68333 accuracy.
- Features include everything from 7/19 model plus missingLineupStrength.
- Betting lines were established with a plus_minus of 4. So an average of two points frmo the actual line.

"""
def getFeatures(player_id, team, stat_type, numGames, id, opp_team, plus_minus, game_features):
    """
    Modifies the list game_features to add all the features. Returns true if offset is positive, 
    false if offset is negative.

    params:
    player_id : integer that corresponds to a specific NBA player
    team : string that contains the three-letter abbreviation that corresponds to a specific NBA team
    stat_type : string that contains the three-letter abbreviation that corresponds to a statistic
    numGames : integer that contains the number of games back used to calculate features such as lastNGames
    opp_team : string that contains the three-letter abbreviation that corresponds to a specific NBA team (may be redundant)
    plus_minus : integer that corresponds to the range above and below the actual statistic that will establish the betting line
    game_features : list containing the list of features to append to
    """
    # Adding the avg of the last N games
    game_features.append(dp.getlastNGamesAvg(player_id, stat_type, numGames, game_id=id))
    time.sleep(2)
    # Adding the season avg
    game_features.append(dp.getSeasonAvg(player_id, stat_type, game_id=id))
    time.sleep(2)
    # Adding the matchup avg
    game_features.append(dp.getMatchupAvg(player_id, stat_type, opp_team, game_id=id))
    time.sleep(2)
    # Adding the length of the matchup log (Greater length means more weight should be placed on Matchup Avg)
    game_features.append(dp.getPrevMatchupLogLength(player_id, opp_team))
    time.sleep(2)
    # Adding the recent usage rate
    game_features.append(dp.getRecentUsageRate(player_id, numGames, game_id=id))
    time.sleep(2)
    # Adding the past lineup strength
    try:
        game_features.append(dp.getPastMissingLineupStrength(team, player_id, id))
    except Exception as e:
        game_features.append(0)     
    # Adding the betting line
    offset = 0
    while offset == 0:
        offset = rand.randint(-plus_minus,plus_minus)
    betting_line = dp.getPointsScored(player_id,game_id=id).values + offset
    game_features.append(betting_line[0])
    print(game_features)
    time.sleep(2)

    if offset > 0:
        return True
    else: 
        return False
    
def get_trained_model_from_csv(filename, penalty, solver, c_penalty):
    """
    Returns the trained over_under model. Dumps the model into the models directory for ease of reuse. 

    params:
    filename : string containing the name of the file with the training data
    penalty : string being either "l2", "l1" or None. Specifies the type of model regularization
    solver : string containing the type of algorithim used for logistic regression. See sklearn Logistic Regression documentation.
    c_penalty : integer hyperparameter specifying how strong regularization should be. Higher c_penalty values correspond to simpler models (less complex) and vice versa.
    """
    path = "prizepicks_predictor/backend/over_under/processed_data/" + filename 
    
    # Reading test data from the test data csv
    features = []
    results = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = list(map(float, row))
            # Split the row into features and result and append them to respective lists
            features.append(row[:-1])
            results.append(row[-1])

    # Model creation and fitting to the test data
    model = LogisticRegression(penalty=penalty,C=c_penalty,solver=solver)
    model.fit(features,results)

    # Storing the model as a pkl file in the models directory
    pickle.dump(model, open('prizepicks_predictor/backend/models/over_under.pkl', 'wb'))
    return model

def test_model(test_filename, model_obj = None):
    """
    Returns the accuracy of the model after testing the model on the test data csv. 

    params:
    test_filename : string containing the name of the file with the test data
    model_obj : a trained model object
    """
    path = "prizepicks_predictor/backend/over_under/processed_data/" + test_filename
    features = []
    true_results = []

    # Loading the model. It can either be passed into the function or loaded from the models directory
    if model_obj:
        model = model_obj
    else:
        model = pickle.load(open('prizepicks_predictor/backend/models/over_under.pkl','rb'))

    # Reading the test data and extracting the features for prediction and the real results for comparison
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = list(map(float, row))
            # Split the row into features and result and append them to respective lists
            features.append(row[:-1])
            true_results.append(row[-1])

    # Obtaining the test results for comparison with the real results
    test_results = model.predict(features)
    probabilities = model.predict_proba(features)
    total_elements = len(test_results)
    total_matches = 0
    correct_prob = []
    incorrect_prob = []
    # Comparing model test results and real results
    for i in range(total_elements):
        if test_results[i] == true_results[i]:
            print("correct: " + str(probabilities[i]))
            correct_prob.append(max(probabilities[i]))
            total_matches += 1
        else:
            print("incorrect: " + str(probabilities[i]))
            incorrect_prob.append(max(probabilities[i]))

    print("mean correct: " + str(np.mean(correct_prob)))
    print("mean incorrect: " + str(np.mean(incorrect_prob)))
 
    return total_matches/total_elements


print(test_model("test_data_normalized_2.csv"))
    
#get_trained_model_from_csv(filename="training_data_no_normalization.csv", penalty="l2",c_penalty=1,solver="lbfgs")
def prep_data_pts_model(filename, player_list, numGames):
    """
    Creates one csv file that contains the training data and one csv file that contains the test data.

    params:
    player_list : list of player ids that the model is trained on
    numGames: int that specifies the number of games to train the model on
    """
    path = "prizepicks_predictor/backend/over_under/processed_data/" + filename

    data = {"features" : [], "results" : []}

    for player_id in player_list:
        print("NEW PLAYER: " + str(player_id))
        gamelog = dr.getGameLog(player_id, numGames=82)
        game_id_list = gamelog["Game_ID"].values
        game_id_list = game_id_list[:20]
        team = dr.get_player_team(player_id=player_id)
        time.sleep(30)
        for id in game_id_list:
            opp_team = dp.getOppTeamAbbrev(game_id=id, team=team)
            print(id)
            game_features = []
            under = getFeatures(player_id=player_id,team=team,numGames=numGames,stat_type="PTS",id=id,opp_team=opp_team,plus_minus=4,game_features=game_features)
            time.sleep(1) # Delay to stop nba.com from refusing requests
            if under:
                result = 0 # Under b/c the offset made the line too high (adding a positive)
            else:
                result = 1 # Over b/c the offset made the line too low (adding a negative)

            # Get rid of any nan instances (occurs when there are no prev. matchup data etc.)
            if not any(math.isnan(feature) for feature in game_features):
                data["results"].append(result)
                data["features"].append(game_features)
        
    scaler = MinMaxScaler()
    scaler.fit(data["features"])
    data["features"] = scaler.transform(data["features"])
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(data['features'])):
            row = np.concatenate((data["features"][i], [data["results"][i]]))
            writer.writerow(row)

#prep_data_pts_model(filename="test_data_normalized_2.csv",player_list = [203954, 203999,2544], numGames = 5)