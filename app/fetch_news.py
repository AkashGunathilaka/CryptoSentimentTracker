import dotenv
import praw
import os
from dotenv import load_dotenv


load_dotenv()

def get_reddit_posts(subreddit="CryptoCurrency", limit=10):
    reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                         client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                         user_agent="CryptoSentimentApp"
                         )

    posts = []
    for post in reddit.subreddit(subreddit).hot(limit=limit):
        posts.append({
            "title": post.title,
            "text": post.selftext,
            "upvotes": post.ups,
            "comments": post.num_comments,
        })

    return posts
