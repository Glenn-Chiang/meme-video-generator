from reddit_service import RedditService
from video_maker import create_video
from moviepy.editor import AudioFileClip
from video_uploader import upload_video
import os

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')


def main():
    print('Authenticating with reddit...')
    reddit_service = RedditService(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)

    target_subreddits = ['ProgrammerHumor']
    # target_subreddits = ['animemes', 'anime_irl']

    video_filepath = 'tmp/video.mp4'
    audio_filepath = 'assets/music.mp3'
    audio = AudioFileClip(audio_filepath)
    final_video_filepath = 'tmp/video_final.mp4'
    video_title = 'r/' + target_subreddits[0]

    video_length = audio.duration  # Video length will be equal to song duration
    seconds_per_video = 4
    # Number of images required to fill video
    num_images_required = video_length // 4

    image_urls = []
    last_post_ids = [None for _ in range(len(target_subreddits))]

    while len(image_urls) < num_images_required:
        for i, subreddit in enumerate(target_subreddits):
            print(f'Getting posts for r/{subreddit}...')
            posts, last_post_id = reddit_service.get_subreddit_posts(
                subreddit_name=subreddit, limit=10, after=last_post_ids[i])
            last_post_ids[i] = last_post_id

            for post_with_kind in posts:
                post = post_with_kind['data']
                image_url: str = post['url']
                # Skip non-image posts
                if post['domain'] != 'i.redd.it' or image_url.endswith('gif'):
                    continue
                image_urls.append(image_url)
                print(image_url)
                if len(image_urls) >= num_images_required:
                    break

            print('')

    print('Images:', len(image_urls))
    create_video(image_urls=image_urls, video_filepath=video_filepath, audio_filepath=audio_filepath,
                 seconds_per_video=seconds_per_video, final_video_filepath=final_video_filepath)
    print('Uploading video...')
    upload_video(video_filepath=final_video_filepath,
                 title=video_title, description='test')


if __name__ == '__main__':
    main()
