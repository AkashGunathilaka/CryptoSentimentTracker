from nltk.sentiment import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)
    return score['compound']

# VADER is a rule based sentiment analysis tool specifically designed for social media texts like tweets, Reddit posts, or comments
# It uses a lexicon of words with preassigned sentiment scores, it looks at the text you provide and breaks it down into words or phrases, and scores each based on the lexicon