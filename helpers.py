import requests.auth
import requests
import sys
import os
from dotenv import load_dotenv
load_dotenv()

OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID')
OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET')
ACCOUNT_USERNAME = os.getenv('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.getenv('ACCOUNT_PASSWORD')


def get_token():
    client_auth = requests.auth.HTTPBasicAuth(
        username=OAUTH_CLIENT_ID, password=OAUTH_CLIENT_SECRET)
    post_data = {'grant_type': 'password',
                 'username': ACCOUNT_USERNAME, 'password': ACCOUNT_PASSWORD}
    headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}

    response = None
    try:
        response = requests.post('https://www.reddit.com/api/v1/access_token',
                                 auth=client_auth, headers=headers, data=post_data)
    except Exception as error:
        print(f'Error getting token: {error}')
        sys.exit()
    return response.json()['access_token']


def get_subreddits(headers):
    response = None
    try:
        response = requests.get(
            'https://oauth.reddit.com/subreddits/popular', params={
                'limit': 10,
            }, headers=headers)
        response.raise_for_status()
    except Exception as error:
        print(f'Error getting subreddits: {error}')
        sys.exit()
    listing = response.json()
    subreddits = listing['data']['children']
    return subreddits
