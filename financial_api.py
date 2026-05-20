import yfinance as yf

from tools.utils import cache_result, rate_limit


@cache_result
@rate_limit(seconds=2)
def get_financial_metrics(ticker):

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "company": info.get("longName"),
        "market_cap": info.get("marketCap"),
        "revenue": info.get("totalRevenue"),
        "profit_margin": info.get("profitMargins"),
        "pe_ratio": info.get("trailingPE")
    }