import praw
import random
import os
from credentials import get_credentials


reddit = praw.Reddit(
    client_id = get_credentials('REDDIT_API_CLIENT_ID'), #os.getenv("CLIENT_ID"),
    client_secret =  get_credentials('REDDIT_API_CLIENT_SECRET'), #os.getenv("SECRET"),
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
