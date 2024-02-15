import os
from typing import List, Tuple
import cv2
import requests
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
from PIL import Image


def decode_img_from_url(image_url: str):
    res = requests.get(image_url)
    image_arr = np.asarray(bytearray(res.content), dtype=np.uint8)
    img = cv2.imdecode(image_arr, -1)
    return img


def compose_images_to_video(images: List[np.ndarray], video_size: Tuple[int, int], seconds_per_frame: int, output_path: str):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 1 / seconds_per_frame

    writer = cv2.VideoWriter(output_path, fourcc, fps, video_size)

    for image in images:
        writer.write(image=image)


def create_video(image_urls: List[str], seconds_per_frame: int, video_filepath: str, audio_filepath: str, final_video_filepath: str):
    video_size = (1080, 1920)

    print('Decoding images from urls...')
    original_images = [decode_img_from_url(url) for url in image_urls]

    print('Processing images...')
    processed_images = []
    # Resize each image to fit window. If error, skip to next image.
    for idx, img in enumerate(original_images):
        try:
            cv2.imwrite(f'{idx}.png', img=img)
            processed_img = pad_image(img, video_size)
            processed_images.append(processed_img)
        except Exception as error:
            print(f'Error processing img {idx}: {error}')
            continue

    print('Writing video...')
    compose_images_to_video(
        processed_images, video_size, seconds_per_frame, output_path=video_filepath)

    print('Adding music...')
    video = VideoFileClip(video_filepath)
    audio = AudioFileClip(audio_filepath)
    final_video: VideoFileClip = video.set_audio(audio)
    final_video.write_videofile(final_video_filepath)

    # Remove the video file without the audio
    os.remove(video_filepath)


def pad_image(image: np.ndarray, video_size: Tuple[int, int]):
    video_height, video_width = video_size
    original_height, original_width, channels = image.shape
    print(original_height, original_width)

    # Aspect ratio of original image
    aspect_ratio = round(original_width / original_height, 2)
    print(aspect_ratio)

    final_height = video_height if original_height > original_width else int(video_width // aspect_ratio)
    final_width =  video_width if original_width > original_height else int(video_height * aspect_ratio)
    print(final_height, final_width)

    x_padding = (video_width - final_width) // 2
    y_padding = (video_height - final_height) // 2
    print(x_padding, y_padding)

    processed_image = cv2.copyMakeBorder(
        src=image, top=y_padding, bottom=y_padding, left=x_padding, right=x_padding, borderType=cv2.BORDER_CONSTANT)

    return processed_image


def main():
    video_size = (1920, 1080)
    image_files = os.listdir('images')
    for image_file in image_files:
        # image = cv2.imread(f'images/{image_file}')
        # padded_image = pad_image(image, video_size)
        # break
        image = Image.open(f'images/{image_file}')
        image.thumbnail(video_size, Image.LANCZOS)
        image.save(f'output/{image_file}')
        # padded_image = pad_image(np.asarray(image), video_size)
        # cv2.imwrite(f'output/{image_file}', padded_image)


if __name__ == '__main__':
    main()
