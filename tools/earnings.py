import yfinance as yf

from tools.utils import cache_result, rate_limit


@cache_result
@rate_limit(seconds=2)
def get_earnings_transcript(ticker):

    stock = yf.Ticker(ticker)

    news = stock.news

    if not news:
        return "No earnings/news data found."

    results = []

    for item in news[:5]:

        results.append({
            "title": item.get("title"),
            "publisher": item.get("publisher"),
            "link": item.get("link")
        })

    return results