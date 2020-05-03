class DataProducer:

    def __init__(self):
        super().__init__()

    def get_match(self,match_id):
        raise NotImplementedError()

    def get_player(self,player_id):
        raise NotImplementedError()

    def get_public_matches_ids(self):
        raise NotImplementedError()

    def get_public_matches_data(self,match_ids):
        raise NotImplementedError()