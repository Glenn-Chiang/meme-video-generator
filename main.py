import os
from dotenv import load_dotenv
load_dotenv()
import requests
import requests.auth

OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID')
OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET')
ACCOUNT_USERNAME = os.getenv('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.getenv('ACCOUNT_PASSWORD')

def get_token():
    client_auth = requests.auth.HTTPBasicAuth(username=OAUTH_CLIENT_ID, password=OAUTH_CLIENT_SECRET)
    post_data = {'grant_type': 'password', 'username': ACCOUNT_USERNAME, 'password': ACCOUNT_PASSWORD}
    headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, headers=headers, data=post_data)
    token_payload = response.json()    
    return token_payload['access_token']

def main():
    token = None
    try:
        token = get_token()
        print(token)
    except Exception as error:
        print(f'Error getting token: {error}')

    

if __name__=='__main__':
    main()