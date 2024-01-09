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


def create_video(images: List[np.ndarray], video_size: Tuple[int, int], output_path):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 0.25

    writer = cv2.VideoWriter(output_path, fourcc, fps, video_size)

    for image in images:
        writer.write(image=image)


def main():
    video_size = (800, 800)
    image_urls = ['https://i.redd.it/hmx0q06oh8bc1.jpeg',
                  'https://i.redd.it/ghqvhf063abc1.jpeg',
                  'https://i.redd.it/btpa4n4ie7bc1.jpeg',
                  'https://i.redd.it/3w7j7zit57bc1.jpeg',
                  'https://i.redd.it/emhtpd0nk1bc1.png',
                  'https://i.redd.it/1i26k8vly6bc1.jpeg',
                  'https://i.redd.it/h41jkoe4wabc1.jpeg',
                  'https://i.redd.it/itgb2tlcg8bc1.png',
                  'https://i.redd.it/fe226bi827bc1.jpeg',
                  'https://i.redd.it/s7a4g1rsj9bc1.png',
                  'https://i.redd.it/5xrgtxys3bbc1.png']

    original_images = [decode_img_from_url(url) for url in image_urls]
    processed_images = [resize_and_pad_image(
        img, window_size=video_size) for img in original_images]

    # for idx, image in enumerate(processed_images):
    #     # cv2.imwrite(f'output/image_{idx}.png', img=image)

    create_video(processed_images, video_size, 'output/video.mp4')
    print('Done')


if __name__ == '__main__':
    main()
