import json
import yfinance as yf

from tools.utils import cache_result, rate_limit


def _parse_ticker(input_val):
    """Extract a plain ticker string from a plain string or JSON dict."""
    text = str(input_val).strip().strip("\"'")
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return (
                parsed.get("ticker")
                or parsed.get("symbol")
                or text
            ).strip().upper()
    except (json.JSONDecodeError, ValueError):
        pass
    return text.upper()


@cache_result
@rate_limit(seconds=2)
def get_earnings_transcript(input_val):
    """
    Retrieve recent earnings-related news and management commentary
    for a company via yfinance.
    Accepts a plain ticker string or a JSON dict with a "ticker" key.
    """
    ticker = _parse_ticker(input_val)
    stock  = yf.Ticker(ticker)

    news = []

    # Try stock.news (works in most yfinance versions)
    try:
        raw = stock.news
        if raw:
            news = list(raw)
    except Exception:
        pass

    # Fallback: try get_news() (added in yfinance 0.2.x)
    if not news:
        try:
            raw = stock.get_news()
            if raw:
                news = list(raw)
        except Exception:
            pass

    if not news:
        return {
            "ticker": ticker,
            "message": "No recent earnings news found via yfinance.",
            "note": (
                f"Use web_search to find latest earnings call commentary for {ticker}."
            )
        }

    results = []
    for item in news[:6]:
        # yfinance >= 1.0 wraps the article under item["content"]
        content = item.get("content") or item
        results.append({
            "title": content.get("title") or item.get("title"),
            "publisher": (
                (content.get("provider") or {}).get("displayName")
                or item.get("publisher")
            ),
            "link": (
                content.get("canonicalUrl", {}).get("url")
                or item.get("link")
                or item.get("url")
            ),
            "summary": content.get("summary") or "",
        })

    return {"ticker": ticker, "news_items": results}
