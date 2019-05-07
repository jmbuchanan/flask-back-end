import requests
from requests.auth import HTTPBasicAuth


class ApiGateway:

    base_api_url = "https://us.api.blizzard.com"

    def __init__(self):
        pass

    @property
    def access_token(self):

        base_token_url = "https://us.battle.net/oauth/token"
        username = "xxxxxxxxxxxxxxxxxxxxxxxx"
        password = "xxxxxxxxxxxxxxxxxxxxxxxx"
        grant_type = {"grant_type": "client_credentials"}


        token_response = requests.post(base_token_url, 
                auth=HTTPBasicAuth(username, password),
                data=grant_type, verify=False)

        access_token = token_response.json()['access_token']

        return access_token

    def get_auction_data(self):
        

        params = {'access_token': self.access_token}

        auction_url = requests.get(self.base_api_url + "/wow/auction/data/korgath",
                params=params, verify=False)

        auction_url = auction_url.json()['files'][0]['url']

        auction_data = requests.get(auction_url, verify=False).json()['auctions']

        auction_data = [{'auction_id':index['auc'],
                         'item_id':index['item'],
                         'owner':index['owner'],
                         'bid':index['bid'],
                         'buyout':index['buyout'],
                         'quantity':index['quantity']}
                        for index in auction_data]

        return auction_data


