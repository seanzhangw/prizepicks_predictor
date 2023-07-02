import player_info
import pandas as pd
from nba_api.stats.endpoints import playerdashboardbylastngames as pdlng

def lastNGames(games, measureType, opponent, player):
    """
    """
    params = {
        'player_id' : player,
        'last_n_games' : games,
        'measure_type_detailed' : measureType,
        'opponent_team_id' : opponent
    }
    test = pdlng.PlayerDashboardByLastNGames(**params)
    test_df = test.get_data_frames()[0]


lastNGames(5,'base',1610612766,302999)