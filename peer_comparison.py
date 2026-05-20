import yfinance as yf

from tools.utils import cache_result, rate_limit


PEER_GROUPS = {
    "MSFT": ["AAPL", "GOOGL", "AMZN"],
    "NVDA": ["AMD", "INTC", "QCOM"],
    "JPM": ["BAC", "GS", "MS"]
}


@cache_result
@rate_limit(seconds=2)
def compare_peers(ticker):

    peers = PEER_GROUPS.get(ticker.upper())

    if not peers:
        return "No peer group found."

    results = []

    for peer in peers:

        stock = yf.Ticker(peer)

        info = stock.info

        results.append({
            "ticker": peer,
            "company": info.get("longName"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "revenue_growth": info.get("revenueGrowth")
        })

    return results