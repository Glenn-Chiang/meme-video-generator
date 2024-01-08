from helpers import get_token, get_subreddits

def main():
    print('Authenticating...')
    token = get_token()
    print('Obtained token')

    headers = {'Authorization': f'bearer {token}',
               'User-Agent': 'script:scraper:0.1 (by /u/DarthKnight024)'}

    print('Getting subreddits...')
    subreddits = get_subreddits(headers)
    for subreddit_metadata in subreddits:
        subreddit = subreddit_metadata['data']
        display_name = subreddit['display_name']
        recent_active_users = subreddit['accounts_active']
        subscribers = subreddit['subscribers']
        title = subreddit['title']
        url = subreddit['url']
        print(display_name, subscribers, title, url)

if __name__ == '__main__':
    main()
