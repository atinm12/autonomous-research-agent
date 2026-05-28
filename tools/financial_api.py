import json
import yfinance as yf

from tools.utils import cache_result, rate_limit


def _parse_tickers(input_val):
    """
    Accepts any of:
      - plain string:               "AMZN"
      - quoted string:              '"AMZN"'
      - JSON single ticker:         '{"ticker": "AMZN"}'
      - JSON multi-ticker:          '{"tickers": ["AMZN", "MSFT", "GOOGL"]}'
      - JSON with segment keys:     '{"tickers": [...], "segments": [...]}'
      - Python list string:         '["AMZN", "MSFT"]'
    Returns a list of uppercase ticker strings.
    """
    if isinstance(input_val, list):
        return [str(t).strip().upper() for t in input_val]

    text = str(input_val).strip().strip('"\'')

    # Try JSON parse
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(t).strip().upper() for t in parsed]
        if isinstance(parsed, dict):
            tickers = parsed.get("tickers") or parsed.get("ticker") or parsed.get("symbols")
            if isinstance(tickers, list):
                return [str(t).strip().upper() for t in tickers]
            if isinstance(tickers, str):
                return [tickers.strip().upper()]
    except (json.JSONDecodeError, ValueError):
        pass

    # Plain comma-separated or single ticker
    if "," in text:
        return [t.strip().upper() for t in text.split(",") if t.strip()]

    return [text.upper()]


def _fetch_one(ticker):
    """Fetch financial metrics for a single ticker via yfinance."""
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker": ticker,
        "company": info.get("longName"),
        "market_cap": info.get("marketCap"),
        "revenue": info.get("totalRevenue"),
        "revenue_growth": info.get("revenueGrowth"),
        "profit_margin": info.get("profitMargins"),
        "operating_margin": info.get("operatingMargins"),
        "gross_margin": info.get("grossMargins"),
        "ebitda": info.get("ebitda"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "sector": info.get("sector"),
    }


@cache_result
@rate_limit(seconds=2)
def get_financial_metrics(input_val):
    """
    Retrieve financial metrics for one or more tickers.
    Accepts a plain ticker string ("AMZN"), a comma-separated list,
    or a JSON object with a "ticker" or "tickers" key.
    """
    tickers = _parse_tickers(input_val)

    if len(tickers) == 1:
        return _fetch_one(tickers[0])

    return [_fetch_one(t) for t in tickers]
