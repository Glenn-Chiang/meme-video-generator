import os
import googleapiclient.discovery
from googleapiclient.discovery import Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport import Request


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

CREDENTIALS_FILE = './youtube_credentials.json'
TOKEN_FILE = './token.json'


# Do not run this in production
def get_auth_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    credentials = flow.run_local_server(port=0)
    # Save the credentials for future runs
    with open(TOKEN_FILE, 'w') as token:
        token.write(credentials.to_json())


def get_youtube_service():
    credentials = Credentials.from_authorized_user_file(
        TOKEN_FILE, scopes=SCOPES)

    return googleapiclient.discovery.build(
        serviceName=YOUTUBE_API_SERVICE_NAME, version=YOUTUBE_API_VERSION, credentials=credentials)


def main():
    youtube: Resource = get_youtube_service()
    request = youtube.channels().list(
        mine=True, part='snippet,contentDetails,statistics')
    response = request.execute()
    print(response)


if __name__ == '__main__':
    main()
