import requests.auth
import requests
import sys


class RedditService():
    def __init__(self, client_id, client_secret):
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._user_agent = 'scraper-script:1.0'
        self.authenticate()

    def authenticate(self):
        client_auth = requests.auth.HTTPBasicAuth(
            username=self._client_id, password=self._client_secret)
        post_data = {'grant_type': 'client_credentials'}
        response = None
        try:
            response = requests.post('https://www.reddit.com/api/v1/access_token',
                                     auth=client_auth, data=post_data, headers={'User-Agent': self._user_agent})
            response.raise_for_status()
        except Exception as error:
            print(f'Error getting token: {error}')
            sys.exit()
        token = response.json()['access_token']
        self.request_headers = {'Authorization': f'bearer {token}',
                                'User-Agent': self._user_agent}

    def get_subreddit_posts(self, subreddit_name, limit):
        response = None
        try:
            response = requests.get(
                f'https://oauth.reddit.com/r/{subreddit_name}/top', params={'limit': limit}, headers=self.request_headers)
            response.raise_for_status()
        except Exception:
            raise
        posts = response.json()['data']['children']
        return posts
