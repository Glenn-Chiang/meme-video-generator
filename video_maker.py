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


def compose_images_to_video(images: List[np.ndarray], video_size: Tuple[int, int], seconds_per_video: int, output_path: str):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 1 / seconds_per_video

    writer = cv2.VideoWriter(output_path, fourcc, fps, video_size)

    for image in images:
        writer.write(image=image)


def create_video(image_urls: List[str], video_filepath: str, audio_filepath: str, seconds_per_video: int):
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

    print('Writing video...')
    compose_images_to_video(
        processed_images, video_size, seconds_per_video, output_path=video_filepath)

    print('Adding music...')
    video = VideoFileClip(video_filepath)
    audio = AudioFileClip(audio_filepath)
    audio = audio.cutout(video.duration, audio.duration)  # Cut excess audio
    final_video: VideoFileClip = video.set_audio(audio)
    final_video.write_videofile(video_filepath)

    print('Done')


if __name__ == '__main__':
    create_video()


# Song length: 124s. Take first 64 - 80 seconds?
# 16 - 20 images, 4 seconds per image
