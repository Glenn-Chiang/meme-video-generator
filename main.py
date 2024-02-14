from reddit_service import RedditService
from video_maker import create_video
from moviepy.editor import AudioFileClip
from video_uploader import upload_video
from get_image_urls import get_image_urls
import os
import sys
from dotenv import load_dotenv
load_dotenv()
import prompts

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')


def main():
    target_subreddit = prompts.get_subreddit()
    video_title = prompts.get_title()
  
    print('Authenticating with reddit...')
    reddit_service = RedditService(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)

    video_filepath = 'output/video.mp4'
    audio_filepath = 'audio/music.mp3'
    audio = AudioFileClip(audio_filepath)
    final_video_filepath = f'output/{video_title}.mp4'

    video_length = audio.duration  # Video length will be equal to audio duration
    seconds_per_frame = 5
    # Number of images required to fit the length of the video if each image is displayed for given number of seconds
    num_images_required = video_length // seconds_per_frame
    print('Number of images required:', num_images_required)
    
    print(f'Getting posts for r/{target_subreddit}...')
    image_urls = get_image_urls(reddit_service, target_subreddit, num_images_required)


    if len(image_urls) == 0:
        print(f'Unable to get any images from r/{target_subreddit}')
        return

    print('Images:', len(image_urls))
    create_video(image_urls=image_urls, video_filepath=video_filepath, audio_filepath=audio_filepath,
                 seconds_per_frame=seconds_per_frame, final_video_filepath=final_video_filepath)


if __name__ == '__main__':
    main()
