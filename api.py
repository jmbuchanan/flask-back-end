import requests
from requests.auth import HTTPBasicAuth


class ApiGateway:

    """
    Class to interact with Blizzard API.
    """

    base_api_url = "https://us.api.blizzard.com"

    def __init__(self):
        pass

    @property
    def access_token(self):
        """
        Posts credentials to Blizzard and receives an access token as a response.
        This token is used as authentication when making requests to the 
        Blizzard API.
        """
        
        base_token_url = "https://us.battle.net/oauth/token"
        #TODO Need a better way to handle username and pass
        username = xxxxxxxx
        password = xxxxxxxx
        grant_type = {"grant_type": "client_credentials"}


        token_response = requests.post(base_token_url, 
                auth=HTTPBasicAuth(username, password),
                data=grant_type, verify=False)

        access_token = token_response.json()['access_token']

        return access_token

    def get_auction_data(self):
        """
        Queries the Blizzard API to get the latest auction data from Korgath. 
        This method contains two requests: the first requests the url for the 
        latest auction data and the second uses this url to request the actual 
        auction data.
        """
        
        params = {'access_token': self.access_token}

        #First request 
        auction_url = requests.get(self.base_api_url + "/wow/auction/data/korgath",
                params=params, verify=False)

        auction_url = auction_url.json()['files'][0]['url']


        #Second request
        auction_data = requests.get(auction_url, verify=False).json()['auctions']


        #Renaming key values in JSON response. auc -> auction_id, item -> item_id
        auction_data = [{'auction_id':index['auc'],
                         'item_id':index['item'],
                         'owner':index['owner'],
                         'bid':index['bid'],
                         'buyout':index['buyout'],
                         'quantity':index['quantity']}
                        for index in auction_data]

        return auction_data


