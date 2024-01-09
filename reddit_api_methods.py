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

    subreddits = response.json()['data']['children']
    return subreddits


def get_subreddit_metadata(subreddit):
    name = subreddit['display_name']
    recent_active_users = subreddit['accounts_active']
    subscribers = subreddit['subscribers']
    title = subreddit['title']
    url = subreddit['url']
    return (name, subscribers, title, url)


def get_subreddit_posts(subreddit_name, headers, count):
    response = None
    try:
        response = requests.get(
            f'https://oauth.reddit.com/r/{subreddit_name}/top', params={'limit': count}, headers=headers)
    except Exception as error:
        print(f'Error getting posts for r/{subreddit_name}: {error}')

    posts = response.json()['data']['children']
    return posts
