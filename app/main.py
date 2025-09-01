import uvicorn
from fastapi import FastAPI
from app.fetch_news import get_reddit_posts, get_news_posts
from app.sentiment import analyze_sentiment
from app.deduplication import is_duplicate
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

#fetch news posts
    news_response = get_news_posts()
    news_posts = []

    if news_response.get("status") == "ok":
        for article in news_response.get("articles", []):
            news_post = {
                "title": article.get("title"),
                "text": article.get("description") or article.get("content") or "",
                "source": article.get("source", {}).get("name"),
                "url": article.get("url"),
            }
            news_post["sentiment"] = analyze_sentiment(news_post["text"])
            news_posts.append(news_post)


    analyzed_posts.sort(key=lambda x: (x["sentiment"], x["upvotes"] + x["comments"]), reverse=True)
    return templates.TemplateResponse("crypto_news.html", {"request": request, "posts": analyzed_posts, "news_posts": news_posts})


@app.get("/api/sentiment")
def get_sentiment():
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

    news_response = get_news_posts()
    if news_response.get("status") == "ok":
        for article in news_response.get("articles", []):
            news_post = {
                "title": article.get("title"),
                "text": article.get("description") or article.get("content") or "",
                "source": article.get("source", {}).get("name"),
                "url": article.get("url"),
            }
            news_post["sentiment"] = analyze_sentiment(news_post["text"])
            analyzed_posts.append(news_post)

    # Sort posts by sentiment/upvotes/comments
    analyzed_posts.sort(key=lambda x: (x["sentiment"], x.get("upvotes",0) + x.get("comments",0)), reverse=True)
    return analyzed_posts  # ✅ return JSON instead of template




