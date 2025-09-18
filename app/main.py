import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.fetch_news import get_processed_reddit_posts, get_processed_news_posts
from app.deduplication import is_duplicate  # keep if you still need deduping

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
    # Fetch + analyze Reddit + News posts
    reddit_posts = get_processed_reddit_posts()
    news_posts = get_processed_news_posts()

    # Deduplicate Reddit posts if needed
    seen_titles = []
    deduped_reddit = []
    for post in reddit_posts:
        if is_duplicate(post["title"], seen_titles):
            continue
        seen_titles.append(post["title"])
        deduped_reddit.append(post)

    # Sort Reddit posts
    deduped_reddit.sort(
        key=lambda x: (x["sentiment"], x.get("upvotes", 0) + x.get("comments", 0)),
        reverse=True,
    )

    return templates.TemplateResponse(
        "crypto_news.html",
        {"request": request, "posts": deduped_reddit, "news_posts": news_posts},
    )


@app.get("/api/sentiment")
def get_sentiment():
    reddit_posts = get_processed_reddit_posts()
    news_posts = get_processed_news_posts()

    # Combine and dedupe Reddit posts
    seen_titles = []
    deduped_reddit = []
    for post in reddit_posts:
        if is_duplicate(post["title"], seen_titles):
            continue
        seen_titles.append(post["title"])
        deduped_reddit.append(post)

    all_posts = deduped_reddit + news_posts

    # Sort combined list
    all_posts.sort(
        key=lambda x: (x["sentiment"], x.get("upvotes", 0) + x.get("comments", 0)),
        reverse=True,
    )
    return all_posts  # ✅ JSON response
