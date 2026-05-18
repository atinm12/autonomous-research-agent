import yfinance as yf


def get_financial_metrics(ticker):
    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "market_cap": info.get("marketCap"),
        "revenue": info.get("totalRevenue"),
        "profit_margin": info.get("profitMargins")
    }