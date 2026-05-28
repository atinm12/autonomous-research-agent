import re
import yfinance as yf

from tools.utils import cache_result, rate_limit


# Default peer groups for single-ticker lookups
PEER_GROUPS = {
    "MSFT": ["AAPL", "GOOGL", "AMZN"],
    "NVDA": ["AMD", "INTC", "QCOM"],
    "JPM": ["BAC", "GS", "MS"],
    # Cloud division comparison group
    "AMZN": ["MSFT", "GOOGL"],
    "GOOGL": ["MSFT", "AMZN"],
}

# Map common cloud/company name variants to tickers
NAME_TO_TICKER = {
    "aws": "AMZN",
    "amazon": "AMZN",
    "amzn": "AMZN",
    "azure": "MSFT",
    "microsoft": "MSFT",
    "msft": "MSFT",
    "gcp": "GOOGL",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "googl": "GOOGL",
}


def _fetch_ticker_data(ticker):
    """Fetch financial metrics for a single ticker via yfinance."""
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker": ticker,
        "company": info.get("longName"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "revenue": info.get("totalRevenue"),
        "revenue_growth": info.get("revenueGrowth"),
        "profit_margin": info.get("profitMargins"),
        "operating_margin": info.get("operatingMargins"),
        "gross_margin": info.get("grossMargins"),
        "ebitda_margin": info.get("ebitdaMargins"),
        "forward_pe": info.get("forwardPE"),
        "price_to_sales": info.get("priceToSalesTrailing12Months"),
        "sector": info.get("sector"),
    }


@cache_result
@rate_limit(seconds=2)
def compare_peers(input_str):
    """
    Compare a company against peers.

    Accepts:
      - A single ticker string:         "AMZN"
      - A comma-separated ticker list:  "AMZN,MSFT,GOOGL"
      - A cloud division name:          "AWS" or "Azure"
      - A mixed name string:            "AWS vs Azure vs GCP"
    """
    text = str(input_str).strip()

    # Resolve any cloud/name aliases to tickers
    resolved = []
    for token in re.split(r"[,\s/|]+", text):
        token_lower = token.lower().strip()
        if token_lower in NAME_TO_TICKER:
            resolved.append(NAME_TO_TICKER[token_lower])
        elif token.upper() in ("AMZN", "MSFT", "GOOGL", "AAPL", "NVDA",
                                "AMD", "INTC", "QCOM", "JPM", "BAC", "GS", "MS"):
            resolved.append(token.upper())

    # De-duplicate while preserving order
    seen = set()
    tickers = [t for t in resolved if not (t in seen or seen.add(t))]

    # If nothing resolved, try treating the whole string as a single ticker
    # and fall back to hardcoded peer group
    if not tickers:
        primary = text.upper()
        peers = PEER_GROUPS.get(primary, [])
        if not peers:
            return f"No peer group found for '{input_str}'. Try passing tickers directly, e.g. 'AMZN,MSFT,GOOGL'."
        tickers = [primary] + peers

    results = []
    for ticker in tickers:
        try:
            results.append(_fetch_ticker_data(ticker))
        except Exception as e:
            results.append({"ticker": ticker, "error": str(e)})

    return results