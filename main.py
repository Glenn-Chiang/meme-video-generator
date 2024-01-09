from helpers import get_token, get_subreddit_posts


def main():
    print('Authenticating...')
    token = get_token()
    print('Obtained token')

    headers = {'Authorization': f'bearer {token}',
               'User-Agent': 'script:scraper:0.1 (by /u/DarthKnight024)'}

    target_subreddits = ['ProgrammerHumor', 'programminghorror']

    for subreddit in target_subreddits:
        posts = get_subreddit_posts(subreddit_name=subreddit, headers=headers)
        for post_with_kind in posts:
            post = post_with_kind['data']
            image_url = post['url']
            print(image_url)

if __name__ == '__main__':
    main()
