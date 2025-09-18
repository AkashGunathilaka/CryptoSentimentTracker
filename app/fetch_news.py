import os
import json
import requests
import praw
from dotenv import load_dotenv
from app.sentiment import analyze_post

load_dotenv()

def get_reddit_posts(subreddit="CryptoCurrency", limit=10):
    """Fetch raw Reddit posts (title, text, upvotes, comments)."""
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = "CryptoSentimentApp"

    if not client_id or not client_secret:
        print("No Reddit credentials provided - running in Demo Mode.")
        with open("app/sample_data.json", "r") as f:
            return json.load(f)

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
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


def get_news_posts():
    """Fetch raw news articles (title, description, content, source, url)."""
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=(crypto OR cryptocurrency OR bitcoin OR ethereum)"
        f"&language=en"
        f"&sortBy=publishedAt"
        f"&pageSize=20"
        f"&apiKey={os.getenv('NEWS_API_KEY')}"
    )
    response = requests.get(url)
    return response.json()


def get_processed_reddit_posts(subreddit="CryptoCurrency", limit=10):
    """Fetch + analyze Reddit posts (skip empties)."""
    raw_posts = get_reddit_posts(subreddit=subreddit, limit=limit)
    processed = [analyze_post(p) for p in raw_posts]
    return [p for p in processed if p is not None]


def get_processed_news_posts():
    """Fetch + analyze News posts (skip empties)."""
    news_response = get_news_posts()
    processed = []
    if news_response.get("status") == "ok":
        for article in news_response.get("articles", []):
            news_post = {
                "title": article.get("title"),
                "text": article.get("description") or article.get("content") or "",
                "source": article.get("source", {}).get("name"),
                "url": article.get("url"),
            }
            analyzed = analyze_post(news_post)
            if analyzed:
                processed.append(analyzed)
    return processed
