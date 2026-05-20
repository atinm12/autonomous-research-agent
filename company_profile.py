import yfinance as yf

from tools.utils import cache_result, rate_limit


@cache_result
@rate_limit(seconds=2)
def get_company_profile(ticker):

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "company": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "employees": info.get("fullTimeEmployees"),
        "website": info.get("website"),
        "market_cap": info.get("marketCap"),
        "country": info.get("country"),
        "summary": info.get("longBusinessSummary")
    }