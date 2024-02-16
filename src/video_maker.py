import os
from typing import List, Tuple
import cv2
import requests
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip


def decode_img_from_url(image_url: str):
    res = requests.get(image_url)
    image_arr = np.asarray(bytearray(res.content), dtype=np.uint8)
    img = cv2.imdecode(image_arr, -1)
    return img


def create_video(image_urls: List[str], seconds_per_frame: int, video_filepath: str, audio_filepath: str, final_video_filepath: str):
    video_size = (1080, 1920)

    print('Decoding images from urls...')
    original_images = [decode_img_from_url(url) for url in image_urls]

    print('Processing images...')
    processed_images = []
    # Resize each image to fit window. If error, skip to next image.
    for idx, image in enumerate(original_images):
        try:
            processed_image = pad_and_resize_image(image, video_size)
            processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            processed_images.append(processed_image)
        except Exception as error:
            print(f'Error processing img {idx}: {error}')
            continue

    print('Writing video...')
    image_sequence_clip = ImageSequenceClip(processed_images, fps=1/seconds_per_frame)
    image_sequence_clip.write_videofile(video_filepath)    

    print('Adding music...')
    video = VideoFileClip(video_filepath)
    audio = AudioFileClip(audio_filepath)
    final_video: VideoFileClip = video.set_audio(audio)
    final_video.write_videofile(final_video_filepath)

    # Remove the video file without the audio
    os.remove(video_filepath)


def pad_and_resize_image(image: np.ndarray, video_size: Tuple[int, int]):
    video_height, video_width = video_size
    video_aspect_ratio = video_width / video_height
    original_height, original_width, channels = image.shape

    # Aspect ratio of original image
    image_aspect_ratio = original_width / original_height

    final_height = video_height if image_aspect_ratio < video_aspect_ratio else int(video_width // image_aspect_ratio)
    final_width = video_width if image_aspect_ratio >= video_aspect_ratio else int(video_height * image_aspect_ratio)

    resized_image = cv2.resize(image, dsize=(final_width, final_height))

    left_padding = (video_width - final_width) // 2
    right_padding = video_width - final_width - left_padding
    top_padding = (video_height - final_height) // 2
    bottom_padding = video_height - final_height - top_padding

    processed_image = cv2.copyMakeBorder(
        src=resized_image, top=top_padding, bottom=bottom_padding, left=left_padding, right=right_padding, borderType=cv2.BORDER_CONSTANT)

    return processed_image

