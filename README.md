# meme-video-generator
This python script uses the Reddit API to fetch trending image posts from target subreddits, compiles them into a video and uploads the video to my youtube channel using the Youtube API. Target subreddits can be selected by passing them as a list of command line arguments.
# Getting started
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
4. Create an output folder. Make sure this folder is at the root of the project directory.  
The generated video file will be located in this folder.
```
mkdir output
```
## Get credentials for Reddit API usage
1. Go to https://reddit.com/prefs/apps and follow the steps to register for usage of the reddit API
2. Obtain a reddit client ID and client secret.
3. Create a `.env` file and fill in the keys REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET with the values obtained above. You can refer to `.env.example`.
## Manage audio files
When the script is run, you will be prompted to select a file from the /audio folder to use as the background audio for the video. Add any audio files you may want to use under this folder. 
## Usage
```
python src/main.py
```

## Using Docker
Build image
```
docker build -t meme-gen .
```
Create volume to store output videos
```

```
Run container
```
docker run --rm -it --env-file .env -v .\output\:/app/output meme-gen
```
