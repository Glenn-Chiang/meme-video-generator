# meme-video-generator
This python script uses the Reddit API to fetch trending image posts from target subreddits, compiles them into a video and uploads the video to my youtube channel using the Youtube API. Target subreddits can be selected by passing them as a list of command line arguments.
# Getting started
## Installation
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
## Get credentials for Reddit API usage
1. Go to https://reddit.com/prefs/apps and follow the steps to register for usage of the reddit API
2. Obtain a CLIENT_ID and CLIENT_SECRET
## Usage
Specify 1 or more subreddits as a space-delimited list of command line arguments.  
Note that subreddit names are case-sensitive.
```
python main.py <subreddit_name_1> <subreddit_name_2>
```
Example usage:
```
python main.py ProgrammerHumor anime_irl
```
If 1 or more of the subreddit names are invalid or non-existent, the script will exit.
