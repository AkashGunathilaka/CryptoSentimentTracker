import dotenv
import praw
import os
from dotenv import load_dotenv
import json



load_dotenv()

def get_reddit_posts(subreddit="CryptoCurrency", limit=10):
    client_id=os.getenv("REDDIT_CLIENT_ID")
    client_secret=os.getenv("REDDIT_CLIENT_SECRET")
    user_agent="CryptoSentimentApp"


    if not client_id or not client_secret:
        print("No Reddit credentials provided - running in Demo Mode. if you want to run this application with the most upto date data please create a env file and add reddit credentials")
        with open("app/sample_data.json", "r") as f:
            return json.load(f)


    try:
        reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent
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

    except Exception as e:
        print(f"Error connecting to Reddit API: {e}")
        print("Running in Demo Mode using sample data.")
        with open("app/sample_data.json", "r") as f:
            return json.load(f)
