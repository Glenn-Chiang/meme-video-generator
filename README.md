# meme-video-generator

This python script generates a meme compilation video by scraping posts from your chosen subreddit and overlaying it with your chosen background music.

# How it works
1. Prompts the user to specify the subreddit they want to scrape from
2. Prompts the user to specify the audio file they want to scrape from
3. Computes the number of images required to create a video that matches the duration of the audio file, assuming that each image is displayed for x number of seconds
4. Fetches the required number of images from the specified subreddit using the reddit API
5. Combines the images into a video using the `opencv` and `moviepy` libraries
6. Overlays the video with the user's chosen audio file to produce the finished video
7. Outputs the finished video to the output directory

# Getting started

## Prerequisites
### Register to use the Reddit API
1. Go to https://reddit.com/prefs/apps and follow the steps to register for usage of the Reddit API
2. Obtain a reddit client ID and client secret

## Installation and setup

1. Clone the repository and navigate to the project directory

```
git clone https://github.com/Glenn-Chiang/meme-video-generator.git
cd meme-video-generator
```

2. Create a virtual environment

```
python -m venv venv
```

3. Install dependencies

```
pip install -r requirements.txt

```
4. Create a `.env` file and fill in the keys REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET with the corresponding credentials you obtained in [the earlier step](#prerequisites). You can refer to `.env.example`.

5. (optional) Add audio files to the `/audio` folder. When the script is run, you will be prompted to choose an audio file from this folder. By default, this folder already contains a sample .mp3 file.

6. Create an `/output' folder at the root of the project directory. The generated video files will be located in this folder.

```
mkdir output
```

## Usage

```
python src/main.py
```

# Getting started with Docker

1. Clone the repository and navigate to the project directory

```
git clone https://github.com/Glenn-Chiang/meme-video-generator.git
cd meme-video-generator
```

2. Build the image

```
docker build -t meme-gen .
```

3. Run the container

```
docker run --rm -it --env-file .env -v .\audio\:/app/audio -v .\output\:/app/output meme-gen
```
