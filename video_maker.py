from typing import List, Tuple
import cv2
import requests
import numpy as np


def decode_img_from_url(image_url: str):
    res = requests.get(image_url)
    image_arr = np.asarray(bytearray(res.content), dtype=np.uint8)
    img = cv2.imdecode(image_arr, -1)
    return img


def resize_and_pad_image(image: np.ndarray, window_size=Tuple[int, int]):
    return cv2.resize(image, window_size)
    win_height, win_width = window_size
    img_height, img_width, channels = image.shape

    x_pos = (win_width - img_width) // 2  # top-left corner x
    y_pos = (win_height - img_height) // 2  # top-left corner y

    processed_image = np.zeros(
        (win_height, win_width, channels), dtype=np.uint8)
    processed_image[y_pos: y_pos + img_height,
                    x_pos:x_pos + img_width, :] = image[:, :, :]
    return processed_image


def compile_images_to_video(images: List[np.ndarray], video_size: Tuple[int, int], output_path):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 0.25

    writer = cv2.VideoWriter(output_path, fourcc, fps, video_size)

    for image in images:
        writer.write(image=image)


def create_video(image_urls):
    video_size = (800, 800)
    
    original_images = [decode_img_from_url(url) for url in image_urls]
    processed_images = []

    for idx, img in enumerate(original_images):
        try:
            processed_image = resize_and_pad_image(img, window_size=video_size)
            processed_images.append(processed_image)
        except Exception as error:
            print(f'Error processing img {idx}: {error}')
            continue

    for idx, image in enumerate(processed_images):
        cv2.imwrite(f'output/image_{idx}.png', img=image)

    compile_images_to_video(processed_images, video_size, 'output/test.mp4')
    print('Done')


if __name__ == '__main__':
    create_video()
