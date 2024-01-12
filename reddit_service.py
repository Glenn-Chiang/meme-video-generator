import requests.auth
import requests
import sys
import os
from dotenv import load_dotenv
load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')


def get_token():
    client_auth = requests.auth.HTTPBasicAuth(
        username=REDDIT_CLIENT_ID, password=REDDIT_CLIENT_SECRET)
    post_data = {'grant_type': 'client_credentials'}
    response = None
    try:
        response = requests.post('https://www.reddit.com/api/v1/access_token',
                                 auth=client_auth, data=post_data)
    except Exception as error:
        print(f'Error getting token: {error}')
        sys.exit()
    return response.json()['access_token']


def get_subreddit_metadata(subreddit):
    name = subreddit['display_name']
    recent_active_users = subreddit['accounts_active']
    subscribers = subreddit['subscribers']
    title = subreddit['title']
    url = subreddit['url']
    return (name, subscribers, title, url)


def get_subreddit_posts(subreddit_name, headers, limit, after):
    response = None
    try:
        response = requests.get(
            f'https://oauth.reddit.com/r/{subreddit_name}/top', params={'limit': limit, 'after': after}, headers=headers)
    except Exception as error:
        print(f'Error getting posts for r/{subreddit_name}: {error}')

    posts = response.json()['data']['children']
    last_post_id: str = response.json()['data']['after']
    return posts, last_post_id
