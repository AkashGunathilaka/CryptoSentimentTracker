from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> float | None:
    """
    Return compound sentiment score (-1 to 1).
    Returns None if text is empty/whitespace.
    """
    if not text or not text.strip():
        return None
    score = analyzer.polarity_scores(text)
    return score['compound']


def analyze_post(post: dict) -> dict | None:
    """
    Attach sentiment score to a post.
    Works for both Reddit (post['text']) and News (post['description'] or post['content']).
    Returns None if no valid text is found.
    """
    # Prefer 'text', then 'description', then 'content'
    text = post.get("text") or post.get("description") or post.get("content") or ""
    sentiment = analyze_sentiment(text)

    if sentiment is None:
        return None  # skip empty posts

    post["sentiment"] = sentiment
    return post
