from reddit_service import RedditService
from video_maker import create_video
from moviepy.editor import AudioFileClip
from video_uploader import upload_video
import os
import sys
from dotenv import load_dotenv
load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')


def main():
    # Get settings chosen by user
    target_subreddit = input('Which subreddit do you want to scrape from? ')

    print('Authenticating with reddit...')
    reddit_service = RedditService(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)

    video_filepath = 'output/video.mp4'
    audio_filepath = 'assets/music.mp3'
    audio = AudioFileClip(audio_filepath)
    final_video_filepath = 'output/video_final.mp4'

    video_length = audio.duration  # Video length will be equal to audio duration
    seconds_per_frame = 5
    # Number of images required to fit the length of the video if each image is displayed for given number of seconds
    num_images_required = video_length // 4
    print('Number of images required:', num_images_required)
    image_urls = []
    print(f'Getting posts for r/{target_subreddit}...')

    # How many posts to fetch from the subreddit each time
    batch_size = num_images_required
    # How many posts (including skipped non-image posts) scraped from the subreddit so far
    total_posts_scraped = 0

    while (len(image_urls) < num_images_required):
        posts = []
        try:
            posts = reddit_service.get_subreddit_posts(
                subreddit_name=target_subreddit, limit=batch_size)
            # Every time we fetch a batch of posts, update the total number of posts fetched so far
            total_posts_scraped += batch_size
        except Exception as error:
            print(f'Error getting posts for r/{target_subreddit}: {error}')
            sys.exit()

        # If we fetch 0 posts from a batch, we assume there are no more posts in the subreddit and stop trying to fetch more
        if not posts:
            break

        for post_meta in posts:
            post = post_meta['data']
            image_url: str = post['url']

            # Skip non-image posts
            if post['domain'] != 'i.redd.it' or image_url.endswith('gif'):
                continue

            image_urls.append(image_url)
            print(image_url)
            if len(image_urls) >= num_images_required:
                break

    # If we are unable to fetch a single post from the given subreddit name, we assume that this subreddit does not exist and exit the program
    if total_posts_scraped == 0:
        print(f'Error getting posts for r/{target_subreddit}')
        sys.exit()

    print('Images:', len(image_urls))
    create_video(image_urls=image_urls, video_filepath=video_filepath, audio_filepath=audio_filepath,
                 seconds_per_frame=seconds_per_frame, final_video_filepath=final_video_filepath)


if __name__ == '__main__':
    main()
