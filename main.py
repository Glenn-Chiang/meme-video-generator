from reddit_api_methods import get_token, get_subreddit_posts
from video_maker import create_video


def main():
    print('Authenticating...')
    token = get_token()
    print('Obtained token')

    headers = {'Authorization': f'bearer {token}',
               'User-Agent': 'script:scraper:0.1 (by /u/DarthKnight024)'}

    target_subreddits = ['animemes', 'anime_irl']

    video_filepath = 'tmp/video.mp4'
    audio_filepath = 'assets/music.mp3'
    
    image_urls = []

    for subreddit in target_subreddits:
        print(f'Getting posts for r/{subreddit}...')
        posts = get_subreddit_posts(
            subreddit_name=subreddit, headers=headers, count=20)
        for post_with_kind in posts:
            post = post_with_kind['data']
            if post['domain'] != 'i.redd.it': # Skip non-image posts
                continue
            image_url = post['url']
            image_urls.append(image_url)
            print(image_url)
        print('')


    create_video(image_urls=image_urls, video_filepath=video_filepath, audio_filepath=audio_filepath)


if __name__ == '__main__':
    main()
