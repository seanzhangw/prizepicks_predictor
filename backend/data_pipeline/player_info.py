import json
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo as cpi

class Player():

    def __init__(self, firstName = None, lastName = None, active = None, team = None):
        self.first_name = firstName
        self.last_name = lastName
        self.active = active
        self.team = team
        self.player_id = self.getPlayerID(firstName, lastName, active, team)
        self.age = self.getPlayerAge(self.player_id)

    def _findIDs(self, firstName = None, lastName = None, active = None):
        """
        Returns a list of IDs that correspond to the selected parameters. The IDs are selected according to firstName,
        lastName filters. Created as a helper for getPlayerID.
        """
        playerList = []

        if firstName and lastName: # The first and last name are specified
            playerList = players.find_players_by_full_name(firstName + " " + lastName)
        elif firstName: # The first name is specified
            playerList = players.find_players_by_first_name(firstName)
        elif lastName: # The last name is specified
            playerList = players.find_players_by_last_name(lastName)

        if active:
            return [entry['id'] for entry in playerList if entry['is_active'] == active]
        else:
            return [entry['id'] for entry in playerList]
        
    #TODO: Add more filters to ensure only one player is found
    def getPlayerID(self, firstName = None, lastName = None, active = None, team = None):
        """
        Returns an integer that corresponds to the ID of the selected player. The ID is selected according to
        firstName, lastName, teams played, and active status filters.
        """
        filteredList = []
        idList = self._findIDs(firstName, lastName, active)

        # Only one player with the specified first and last name
        if len(idList) == 1: return idList[0]
        # No players with the specified first and last name
        if len(idList) == 0: raise Exception("Player with the specified name does not exist (Case Sensitive)")
        # Multiple players with the specified first and last name
        else:
            for id in idList:
                playerInfo = json.loads(cpi.CommonPlayerInfo(player_id = id).get_json())
                # Filtering by the specified team. Team expected in abbreviation format (Ex. 'GSW')
                playerTeam = playerInfo['resultSets'][0]['rowSet'][0][20]
                
                if team == playerTeam:
                    filteredList.append(id)

        return filteredList[0]
    
    #TODO:
    def getPlayerAge(self, player_id):
        pass

