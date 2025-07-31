from fastapi import FastAPI
from app.fetch_news import get_reddit_posts
from app.sentiment import analyze_sentiment
from app.deduplication import is_duplicate

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/crypto-news")
def crypto_sentiment():
    raw_posts = get_reddit_posts()
    seen_titles = []
    analyzed_posts = []

    for post in raw_posts:
        if is_duplicate(post['title'], seen_titles):
            continue
        seen_titles.append(post['title'])
        score = analyze_sentiment(post['text'] + " " + post['text'])
        post["sentimet"] = score
        analyzed_posts.append(post)

        analyzed_posts.sort(key=lambda x: (x["sentiment"], x["upvotes"] + x["comments"]), reverse=True)
        return analyzed_posts
