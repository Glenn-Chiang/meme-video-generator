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

## Register to use the Reddit API
1. Go to https://reddit.com/prefs/apps and follow the steps to register for usage of the Reddit API
2. Obtain a reddit client ID and client secret

## Installation and setup

1. Clone the repository and navigate to the project directory

```
git clone https://github.com/Glenn-Chiang/meme-video-generator.git
cd meme-video-generator
```

2. Create a `.env` file and fill in the keys `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` with the corresponding credentials you obtained in [the earlier step](#prerequisites). You can refer to `.env.example`.

3. (optional) Add audio files to the `/audio` folder. When the script is run, you will be prompted to choose an audio file from this folder. By default, this folder already contains some sample .mp3 files.

4. Create an `/output` folder at the root of the project directory. The generated video files will be located in this folder.

```
mkdir output
```

5. Create a virtual environment and install dependencies

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

> Alternatively, build a docker image

```
docker build -t image_name .
```

## Usage
```
python src/main.py
```

If you are using docker:

```
docker run -it --env-file .env -v .\audio\:/app/audio -v .\output\:/app/output image_name
```

# Uploading to Youtube
The videos you generated with the main script can be automatically uploaded to your own youtube channel by running `video_uploader.py`.

## Obtain Youtube credentials
1. Create a `auth` folder in the root directory
2. Create a project in the [Google Cloud console](https://console.cloud.google.com)
3. Navigate to APIs & Services > [Credentials](https://console.cloud.google.com/apis/credentials). Obtain a OAuth client ID and save the JSON file containing the client secret as `youtube_credentials.json` under the `auth` folder.
4. [Enable the youtube API](https://console.cloud.google.com/apis/library/youtube.googleapis.com)
5. [Configure a OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
  - Add your google account to the testers list
  - Add the following scopes:
  ```  
  https://www.googleapis.com/auth/youtube.upload
  ```
6. The first time you run the script, you will be redirected to a browser page displaying the OAuth consent screen. Proceed to authenticate yourself.
7. Once you are authenticated, the script saves a `token.json` file under the `auth` folder. This file will be reused to maintain your authentication status so that you no longer have to reauthenticate yourself on subsequent runs.

## Usage
Run the script
```
python src/video_uploader.py
```
When the script is run, you will be prompted to select a video from the `output` folder, as well as set a title and description for the video.

