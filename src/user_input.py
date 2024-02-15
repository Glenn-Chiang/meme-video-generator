import re
import os


def get_subreddit():
    subreddit = None
    while True:
        subreddit = input("Target subreddit (without 'r/'): ")
        if subreddit.startswith('r'):
            print("Do not include the 'r/' prefix")
        if " " in subreddit:
            print("Subreddit name cannot include spaces")
        else:
            break
    return subreddit


def get_title():
    maxLength = 25
    restrictedChars = ['\\', '/', ':', '*', '?', '"', '>', '<', '|', ' ']
    pattern = f"[{''.join(restrictedChars)}]"

    title = None
    while True:
        title = input('Set a title for your video: ').strip()
        if len(title) > maxLength:
            print('Title cannot be more than 25 characters')
        elif bool(re.search(pattern=pattern, string=title)):
            print('Title contains invalid characters')
        elif title.endswith('.'):
            print('Title cannot end with "."')
        else:
            break

    return title


def get_audio_file():
    files = os.listdir('audio')

    while True:
        print('Audio files:')
        for index, file in enumerate(files):
            print(f"{index + 1}: {file}")
        choice = input(
            'Select the index number of the audio file you want to use: ')
        if (not choice.isdigit() or int(choice) < 1 or int(choice) > len(files)):
            print(f'Enter a digit from 1 to {len(files)}')
        else:
            break
    
    return f'audio/{files[int(choice) - 1]}'
