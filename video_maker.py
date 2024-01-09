from typing import List
import cv2
import requests
import numpy as np


def decode_img_from_url(image_url: str):
    res = requests.get(image_url)
    image_arr = np.asarray(bytearray(res.content), dtype=np.uint8)
    img = cv2.imdecode(image_arr, -1)
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    return img


def create_video(images: List[np.ndarray]):
    output_path = "output/video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 0.5
    height, width, _ = images[0].shape

    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for image in images:
        writer.write(image=image)

    print('Done')


def main():
    image_urls = ['https://i.redd.it/3w7j7zit57bc1.jpeg', 'https://i.redd.it/emhtpd0nk1bc1.png',
                  'https://i.redd.it/1i26k8vly6bc1.jpeg']
    images = [decode_img_from_url(url) for url in image_urls]
    create_video(images)


if __name__ == '__main__':
    main()
