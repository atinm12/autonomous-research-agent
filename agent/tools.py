"""
Tool registry — all 12 distinct tools registered and described.
Aliases are retained for backward compatibility but clearly marked.
"""

from tools.sec_edgar import search_sec_filings
from tools.financial_api import get_financial_metrics
from tools.web_search import web_search
from tools.news_sentiment import company_news_sentiment
from tools.earnings import get_earnings_transcript
from tools.company_profile import get_company_profile
from tools.peer_comparison import compare_peers
from tools.fact_checker import fact_check
from tools.calculator import calculation_engine
from tools.report_gen import generate_report


# -------------------------------------------------------------------
# Vector DB tool wrappers (forward to memory layer)
# -------------------------------------------------------------------

def _vector_db_search(query: str) -> dict:
    """Search long-term vector memory for relevant stored research."""
    try:
        from memory.vector_store import search_memory
        results = search_memory(str(query).strip().strip('"\''), n_results=5)
        docs = results.get("documents", [[]])[0]
        return {
            "query": query,
            "results": [{"document": d, "similarity_score": 0.9 - i * 0.05} for i, d in enumerate(docs)],
        }
    except Exception as e:
        return {"query": query, "results": [], "error": str(e)}


def _vector_db_store(input_val: str) -> dict:
    """Store a document in long-term vector memory."""
    try:
        from memory.vector_store import store_memory
        result = store_memory(str(input_val)[:3000])
        return {"status": "success", "detail": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _report_generator(input_val: str) -> str:
    """Format collected findings into a structured markdown report."""
    title = "Research Report"
    findings = [line.strip() for line in str(input_val).split("\n") if line.strip()]
    return generate_report(title, findings)


# -------------------------------------------------------------------
# TOOL REGISTRY  (12 distinct tools)
# -------------------------------------------------------------------

TOOL_REGISTRY = {
    # Core research tools
    "financial_data_api":   get_financial_metrics,
    "sec_filing_search":    search_sec_filings,
    "earnings_transcript":  get_earnings_transcript,
    "web_search":           web_search,
    "peer_comparison":      compare_peers,
    "calculation_engine":   calculation_engine,

    # Supporting tools
    "news_sentiment":       company_news_sentiment,
    "company_profile":      get_company_profile,
    "fact_checker":         fact_check,

    # Memory-integrated tools
    "vector_db_search":     _vector_db_search,
    "vector_db_store":      _vector_db_store,

    # Report generation
    "report_generator":     _report_generator,
}


# -------------------------------------------------------------------
# TOOL DESCRIPTIONS
# -------------------------------------------------------------------

TOOL_DESCRIPTIONS = {
    "financial_data_api": (
        "Retrieve stock prices, revenue, market cap, valuation metrics, "
        "growth metrics, and company financial statistics for any public ticker."
    ),
    "sec_filing_search": (
        "Search and retrieve SEC filings including 10-K annual reports, "
        "10-Q quarterly reports, earnings filings, and official company disclosures."
    ),
    "earnings_transcript": (
        "Retrieve recent earnings call news and management commentary "
        "from public companies via ticker symbol."
    ),
    "web_search": (
        "Search recent public web information, industry developments, "
        "company news, and general internet sources."
    ),
    "peer_comparison": (
        "Compare companies against each other using financial metrics, "
        "valuation ratios, growth trends, and market performance. "
        "Accepts tickers (AMZN,MSFT,GOOGL) or cloud division names."
    ),
    "calculation_engine": (
        "Perform financial calculations: growth rate, profit margin, "
        "DCF valuation, and market share. "
        "Example: 'growth rate 411 321', 'margin 125 411', 'dcf 50 0.15 0.10'."
    ),
    "news_sentiment": (
        "Analyze recent financial news headlines for a company and return "
        "positive/neutral/negative sentiment scores."
    ),
    "company_profile": (
        "Retrieve company background including headquarters, sector, "
        "industry, business model, and overview."
    ),
    "fact_checker": (
        "Cross-reference claims against multiple sources to verify "
        "accuracy and flag contradictions."
    ),
    "vector_db_search": (
        "Search the long-term vector memory database for research findings "
        "stored from previous queries. Use for Challenge 7 (sector analysis)."
    ),
    "vector_db_store": (
        "Store a document or research finding in the long-term vector "
        "memory database for future retrieval."
    ),
    "report_generator": (
        "Format collected research findings into a structured markdown report "
        "with proper headings and bullet points."
    ),
}
