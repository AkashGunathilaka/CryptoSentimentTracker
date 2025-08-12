from fastapi import FastAPI
from app.fetch_news import get_reddit_posts
from app.sentiment import analyze_sentiment
from app.deduplication import is_duplicate
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")



@app.get("/")
def crypto_sentiment(request: Request):
    raw_posts = get_reddit_posts()
    seen_titles = []
    analyzed_posts = []

    for post in raw_posts:
        if is_duplicate(post['title'], seen_titles):
            continue
        seen_titles.append(post['title'])
        score = analyze_sentiment(post['text'] + " " + post['text'])
        post["sentiment"] = score
        analyzed_posts.append(post)

    analyzed_posts.sort(key=lambda x: (x["sentiment"], x["upvotes"] + x["comments"]), reverse=True)
    return templates.TemplateResponse("crypto_news.html", {"request": request, "posts": analyzed_posts})



