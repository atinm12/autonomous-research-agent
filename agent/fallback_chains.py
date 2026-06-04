"""
Fallback chains — every primary tool has at least 2 fallback options.
When a tool fails, the agent automatically tries each fallback in order.
"""

from tools.company_profile import get_company_profile
from tools.financial_api import get_financial_metrics
from tools.web_search import web_search
from tools.sec_edgar import search_sec_filings
from tools.news_sentiment import company_news_sentiment
from tools.earnings import get_earnings_transcript
from tools.peer_comparison import compare_peers
from tools.fact_checker import fact_check
from tools.calculator import calculation_engine


# -------------------------------------------------------------------
# FALLBACK MAP  (at least 2 fallbacks per primary tool)
# -------------------------------------------------------------------

FALLBACK_CHAINS: dict[str, list] = {

    "financial_data_api": [
        get_financial_metrics,     # retry primary
        search_sec_filings,        # extract financials from SEC filing
        web_search,                # search financial summary sites
    ],

    "sec_filing_search": [
        search_sec_filings,        # retry
        web_search,                # web search for SEC document
        get_financial_metrics,     # fall back to financial API
    ],

    "earnings_transcript": [
        get_earnings_transcript,   # retry
        web_search,                # search for earnings summary
        company_news_sentiment,    # news coverage as proxy
    ],

    "web_search": [
        web_search,                # retry
        company_news_sentiment,    # news feeds as alternative
        search_sec_filings,        # official filings as last resort
    ],

    "peer_comparison": [
        compare_peers,             # retry
        get_financial_metrics,     # fetch metrics individually
        web_search,                # search for peer comparison data
    ],

    "calculation_engine": [
        calculation_engine,        # retry
        web_search,                # search for pre-computed metrics
        get_financial_metrics,     # raw data for manual calc
    ],

    "news_sentiment": [
        company_news_sentiment,    # retry
        web_search,                # search news directly
        get_earnings_transcript,   # management tone as proxy
    ],

    "company_profile": [
        get_company_profile,       # retry
        web_search,                # search company website / Wikipedia
        search_sec_filings,        # extract from SEC company page
    ],

    "fact_checker": [
        fact_check,                # retry
        web_search,                # cross-reference via web
        search_sec_filings,        # verify against SEC filings
    ],

    "vector_db_search": [
        web_search,                # fall back to live web search
        search_sec_filings,        # fall back to SEC
    ],
}


# -------------------------------------------------------------------
# EXECUTE FALLBACK CHAIN
# -------------------------------------------------------------------

def execute_with_fallbacks(tool_name: str, query) -> dict:
    """
    Attempt each tool in the fallback chain for tool_name.
    Returns {"success": True, "tool_used": name, "result": ...}
    or {"success": False, "error": ...} if all fallbacks fail.
    """
    chain = FALLBACK_CHAINS.get(tool_name, [])

    for tool_fn in chain:
        try:
            print(f"  [Fallback] Trying: {tool_fn.__name__}")
            result = tool_fn(query)
            if result:
                return {
                    "success": True,
                    "tool_used": tool_fn.__name__,
                    "result": result,
                }
        except Exception as e:
            print(f"  [Fallback] Failed: {e}")

    return {
        "success": False,
        "error": f"All fallbacks exhausted for '{tool_name}'.",
    }
