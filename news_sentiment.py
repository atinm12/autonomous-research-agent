import feedparser
from textblob import TextBlob


def company_news_sentiment(company):
    url = f"https://news.google.com/rss/search?q={company}"

    feed = feedparser.parse(url)

    articles = feed.entries[:5]

    results = []

    for article in articles:
        title = article.title

        sentiment = TextBlob(title).sentiment.polarity

        results.append({
            "title": title,
            "sentiment_score": sentiment
        })

    return results