from reddit_api_methods import get_token, get_subreddit_posts
from video_maker import create_video


def main():
    print('Authenticating...')
    token = get_token()
    print('Obtained token')

    headers = {'Authorization': f'bearer {token}',
               'User-Agent': 'script:scraper:0.1 (by /u/DarthKnight024)'}

    # target_subreddits = ['programminghorror','ProgrammerHumor']
    target_subreddits = ['anime_irl', 'animemes']
    image_urls = []

    for subreddit in target_subreddits:
        print(f'Getting posts for r/{subreddit}...')
        posts = get_subreddit_posts(
            subreddit_name=subreddit, headers=headers, count=10)
        for post_with_kind in posts:
            post = post_with_kind['data']
            image_url = post['url']
            print(image_url)
            if post['media']: # Skip video posts; only use images
                continue
            image_urls.append(image_url)
        print('')

    create_video(image_urls=image_urls)


if __name__ == '__main__':
    main()
