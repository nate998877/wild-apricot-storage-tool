import requests
from base64 import b64encode
import os
import json

class Apricot():
    def __init__(self):
        apikey = os.getenv('API_KEY')
        headers = {
            'Authorization': f"Basic {b64encode(bytes(f'APIKEY:{apikey}', 'utf-8')).decode('utf-8')}",
            'Content-type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'grant_type': 'client_credentials',
            'scope': 'auto'
        }
        #Get Bearer token
        r = requests.post('https://oauth.wildapricot.org/auth/token',
                        headers=headers, data=payload)
        account = r.json()
        self.account_id = account['Permissions'][0]['AccountId']
        token = account['access_token']
        self.headers = {'User-Agent': 'doorCommand/0.1',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'}

    def get_user_list(self):
        params = {
            '$async': False,
            '$filter': "'Membership level ID' ne 725412 AND 'Membership status' ne 'Lapsed'"
        }
        r = requests.get(
            f'https://api.wildapricot.org/v2.2/accounts/{self.account_id}/contacts/', headers=self.headers, params=params)
        return r.json()

    def filter_user_data(self, data):
        filter_keys = {
            "FirstName": "first",
            "Status": "status",
            "LastName": "last",
            "Id": "id",
        }
        user_list = []
        for user in data["Contacts"]:
            filter_user = {}

            for key in filter_keys.keys():
                filter_user[filter_keys[key]] = user[key]

            group_field = list(filter(
                lambda x: x['SystemCode'] == 'custom-10343687', user['FieldValues']))

            try:
                filter_user['storage_location'] = group_field[0]["Value"]
                user_list.append(filter_user)
            except:
                pass


        return user_list


    def print_to_file(self, data, filename='output.json'):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)