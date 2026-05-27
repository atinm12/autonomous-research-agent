# -----------------------------------
# QUERY ANALYZER
# -----------------------------------

def analyze_query(query):

    query_lower = query.lower()

    complexity = "low"

    ambiguity = "low"

    query_type = "general"


    # -----------------------------------
    # DETECT COMPLEXITY
    # -----------------------------------

    if any(word in query_lower for word in [

        "compare",
        "analysis",
        "sector",
        "forecast",
        "valuation",
        "research",
        "industry"

    ]):

        complexity = "medium"


    if any(word in query_lower for word in [

        "multi-year",
        "macroeconomic",
        "geopolitical",
        "five years",
        "comprehensive",
        "deep"

    ]):

        complexity = "high"


    # -----------------------------------
    # DETECT QUERY TYPE
    # -----------------------------------

    if "compare" in query_lower:

        query_type = "comparison"

    elif "valuation" in query_lower:

        query_type = "financial_analysis"

    elif "sector" in query_lower:

        query_type = "sector_analysis"

    elif "news" in query_lower:

        query_type = "news_analysis"


    # -----------------------------------
    # DETECT AMBIGUITY
    # -----------------------------------

    ambiguous_terms = [

        "apple",
        "amazon",
        "meta",
        "google"
    ]

    if any(
        term == query_lower.strip()
        for term in ambiguous_terms
    ):

        ambiguity = "high"

    elif len(query.split()) <= 2:

        ambiguity = "medium"


    return {

        "query": query,

        "query_type": query_type,

        "complexity": complexity,

        "ambiguity": ambiguity
    }