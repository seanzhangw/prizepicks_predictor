import pickle
from data_pipeline import (
    data_processing as dp,
    player_info as pi,
)

def train_player_pts_model(player_id):
    """
    """
    features = []
    results = []
    features.append(dp.getlastNGamesAvg(player_id, "PTS", numGames = 5))
    features.append(dp.getSeasonAvg(player_id, "PTS"))

