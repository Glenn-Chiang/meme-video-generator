import re


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
