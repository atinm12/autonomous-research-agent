from tools.sec_edgar import search_sec_filings
from tools.financial_api import get_financial_metrics
from tools.web_search import web_search
from tools.news_sentiment import company_news_sentiment

from tools.earnings import get_earnings_transcript
from tools.company_profile import get_company_profile
from tools.peer_comparison import compare_peers
from tools.fact_checker import fact_check


# -----------------------------------
# TOOL REGISTRY
# -----------------------------------

TOOL_REGISTRY = {

    "sec_search": search_sec_filings,

    "financial_metrics": get_financial_metrics,

    "web_search": web_search,

    "news_sentiment": company_news_sentiment,

    "earnings_transcript": get_earnings_transcript,

    "company_profile": get_company_profile,

    "peer_comparison": compare_peers,

    "fact_checker": fact_check
}


# -----------------------------------
# TOOL DESCRIPTIONS
# -----------------------------------

TOOL_DESCRIPTIONS = {

    "sec_search": (
        "Retrieve SEC filings including "
        "10-K, 10-Q, earnings filings, "
        "and official company disclosures."
    ),

    "financial_metrics": (
        "Retrieve stock prices, revenue, "
        "market cap, valuation metrics, "
        "growth metrics, and company "
        "financial statistics."
    ),

    "web_search": (
        "Search recent public web information, "
        "industry developments, company news, "
        "and general internet sources."
    ),

    "news_sentiment": (
        "Analyze recent financial news coverage "
        "and estimate positive, neutral, or "
        "negative sentiment toward a company."
    ),

    "earnings_transcript": (
        "Retrieve earnings call transcripts "
        "and management commentary from "
        "public companies."
    ),

    "company_profile": (
        "Retrieve company background information "
        "including headquarters, sector, industry, "
        "business model, and corporate overview."
    ),

    "peer_comparison": (
        "Compare a company against industry peers "
        "using financial metrics, valuation ratios, "
        "growth trends, and market performance."
    ),

    "fact_checker": (
        "Cross-reference claims against multiple "
        "sources to verify accuracy and identify "
        "contradictory information."
    )
}