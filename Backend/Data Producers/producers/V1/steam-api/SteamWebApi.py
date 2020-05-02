import requests
import json
import os
import sys
sys.path.append('../')
from DataProducer import DataProducer
from dotenv import load_dotenv

def load_env_variables():
    load_dotenv()
    return os.getenv('STEAMKEY')



class SteamWebApiWrapper(DataProducer):

    def __init__(self,steam_api_key):
        super().__init__()
        self.key = steam_api_key

    def get_match(self,match_id):

        endpoint_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1?match_id={}&key={}'.format(match_id,self.key)
        response = requests.get(endpoint_url)
        response_json = response.json()
        return response_json

    def get_player(self,player_id):

        endpoint_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1?match_id={}&key={}'.format(player_id,self.key)

        response = requests.get(endpoint_url)
        response_json = response.json()
        return response_json

steam_key = load_env_variables()
producer = SteamWebApiWrapper(steam_key)
result = producer.get_match(5379124052)
#result = producer.get_public_matches_ids()
#result = producer.get_public_matches_data(result)
print(json.dumps(result,indent=1))