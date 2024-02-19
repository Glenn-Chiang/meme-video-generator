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

CREDENTIALS_FILE = './auth/youtube_credentials.json'
TOKEN_FILE = './auth/token.json'


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
    return response


def main():
    video_folder = 'output'
    video_files = os.listdir(video_folder)

    while True:
        print('Videos:')
        for index, video_file in enumerate(video_files):
            print(f'{index + 1}: {video_file}')
        selected_option = input('Enter the number of the video that you want to upload: ')
        if not selected_option.isdigit():
            print('Enter a number\n')
        elif int(selected_option) not in range(1, len(video_files) + 1):
            print(f'Enter a number between 1 and {len(video_files)}\n')
        else:
            break

    video_filepath = os.path.join(video_folder, video_files[int(selected_option) - 1]) 

    title_limit = 50
    description_limit = 2500
    while True:
        title = input('Enter a title for your video: ')
        if len(title) > title_limit:
            print(f'Title cannot be more than {title_limit} characters')
        else:
            break
    while True:
        description = input('Enter a description for your video: ')
        if len(description) > description_limit:
            print(f'Description cannot be more than {description_limit} characters')
        else:
            break

    response = upload_video(title=title, description=description, video_filepath=video_filepath)
    print(response)


if __name__ == '__main__':
    main()