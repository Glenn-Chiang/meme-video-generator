import os
import googleapiclient.discovery
from googleapiclient.discovery import Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

CREDENTIALS_FILE = './youtube_credentials.json'
TOKEN_FILE = './token.json'


# Only need to run this function the first time you authenticate with google to obtain a refresh token
# The token will be saved and used to authenticate all subsequent requests
def obtain_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    credentials = flow.run_local_server(port=0)
    # Save the credentials for future runs
    with open(TOKEN_FILE, 'w') as token:
        token.write(credentials.to_json())


def get_youtube_service():
    if not os.path.exists(TOKEN_FILE):
        obtain_token()
    credentials = Credentials.from_authorized_user_file(
        TOKEN_FILE, scopes=SCOPES)
    credentials.refresh(Request())

    return googleapiclient.discovery.build(
        serviceName=YOUTUBE_API_SERVICE_NAME, version=YOUTUBE_API_VERSION, credentials=credentials)


def upload_video(video_filepath, title, description):
    youtube: Resource = get_youtube_service()
    video_metadata = {
        'snippet': {
            'title': title,
            'description': description,
            'categoryId': '23'
        }
    }
    request = youtube.videos().insert(body=video_metadata, media_body=MediaFileUpload(
        video_filepath), part="contentDetails,snippet")
    response = request.execute()
    print(response)


if __name__ == '__main__':
    upload_video(title='test title', description='test description', video_filepath='tmp/video_final.mp4')
