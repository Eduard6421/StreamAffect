import requests
import json
import sys
sys.path.append('../')
from DataProducer import DataProducer

class OpenDotaWrapper(DataProducer):

    def __init__(self,proxy_ip,proxy_port):
        super().__init__()
        self.proxies = {
            "http" : "{}:{}".format(proxy_ip,proxy_port),
        }

    def get_match(self,match_id):
        endpoint_url = 'https://api.opendota.com/api/matches/{}'.format(match_id)
        response = requests.get(endpoint_url,proxies=self.proxies)
        response_json = response.json()
        return response_json

    def get_player(self,player_id):
        endpoint_url = 'https://api.opendota.com/api/players/{}'.format(player_id)
        print(endpoint_url)
        response = requests.get(endpoint_url,proxies=self.proxies)
        response_json = response.json()
        return response_json

    def get_public_matches_ids(self):
        endpoint_url = 'https://api.opendota.com/api/publicMatches'
        response = requests.get(endpoint_url,proxies=self.proxies)
        response_json = response.json()
        response_json = {
            'match_ids': list(map(lambda x:x['match_id'],response_json))
            }
        return response_json

    def get_public_matches_data(self,match_ids):
        match_ids = match_ids['match_ids']
        matches = []
        for idx,match_id in enumerate(match_ids):
            matches.append(self.get_match(match_id))
        
        matches_json = json.loads(json.dumps(matches))
        return matches_json

proxy_ip = "94.130.179.24"
proxy_port = "8020"

producer = OpenDotaWrapper(proxy_ip,proxy_port)
result = producer.get_public_matches_ids()
result = producer.get_public_matches_data(result)
print(result[0])