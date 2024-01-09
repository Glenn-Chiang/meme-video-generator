from typing import List, Tuple
import cv2
import requests
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip


def decode_img_from_url(image_url: str):
    res = requests.get(image_url)
    image_arr = np.asarray(bytearray(res.content), dtype=np.uint8)
    img = cv2.imdecode(image_arr, -1)
    return img


def compose_images_to_video(images: List[np.ndarray], video_size: Tuple[int, int], output_path):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 0.25

    writer = cv2.VideoWriter(output_path, fourcc, fps, video_size)
    
    for image in images:
        writer.write(image=image)


def create_video(image_urls, title):
    video_size = (800, 800)

    print('Decoding images from urls...')
    original_images = [decode_img_from_url(url) for url in image_urls]

    print('Processing images...')
    processed_images = []
    # Resize each image to fit window. If error, skip to next image.
    for idx, img in enumerate(original_images):
        try:
            processed_img = cv2.resize(img, video_size)
            processed_images.append(processed_img)
        except Exception as error:
            print(f'Error processing img {idx}: {error}')
            continue

    # for idx, image in enumerate(processed_images):
    #     cv2.imwrite(f'output/image_{idx}.png', img=image)

    print('Writing video...')
    video_filepath = f'tmp/{title}.mp4'
    compose_images_to_video(
        processed_images, video_size, output_path=video_filepath)
    
    print('Adding music...')
    video = VideoFileClip(video_filepath)
    audio = AudioFileClip('assets/MILF_fnf.mp3') 
    final_video: VideoFileClip = video.set_audio(audio)
    final_video.write_videofile(f'tmp/{title}_final.mp4')

    print('Done')


if __name__ == '__main__':
    create_video()


# TODO: Fit audio and video to 1min20s, i.e. 20 videos at 4 seconds per video