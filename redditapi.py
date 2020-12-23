import praw
import random
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("SECRET"),
    user_agent = 'chintubot',
)
def memes(subreddit):
    memes = reddit.subreddit(subreddit)
    top = memes.top(limit = 100)
    all_memes = []
    for meme in  top:
        all_memes.append(meme)
    meme = random.choice(all_memes)
    meme_title = meme.title
    meme_url = meme.url
    return meme_title,meme_url
print(memes('ProgrammerHumor'))