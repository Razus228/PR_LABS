from player import Player



class PlayerFactory:
    def to_json(self, players):
        player_dicts = []
        for player in players : 
            player_dict = {
                "nickname" : player.nickname,
                "email" : player.email,
                "date_of_birth" : player.date_of_birth.strftime("%Y-%m-%d"),
                "xp" : player.xp,
                "cls" : player.cls
            }
            player_dicts.append(player_dict)
        return player_dicts
        pass

    def from_json(self, list_of_dict):
        '''
            This function should transform a list of dictionaries into a list with Player objects.
        '''
        pass

    def from_xml(self, xml_string):
        '''
            This function should transform a XML string into a list with Player objects.
        '''
        pass

    def to_xml(self, list_of_players):
        '''
            This function should transform a list with Player objects into a XML string.
        '''
        pass

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''
        pass

    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects intoa binary protobuf string.
        '''
        pass
