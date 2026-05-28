from tools.utils import cache_result, rate_limit


# duckduckgo_search was renamed to ddgs in v9+; support both
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


@cache_result
@rate_limit(seconds=2)
def web_search(query):
    """
    Search the web using DuckDuckGo.
    Accepts a plain string or a quoted string from the LLM.
    Returns a list of {title, link, snippet} dicts.
    """
    # Strip surrounding quotes the LLM sometimes adds
    clean_query = str(query).strip().strip('"\'')

    results = []
    try:
        ddgs = DDGS()
        search_results = ddgs.text(clean_query, max_results=8)
        for result in search_results:
            results.append({
                "title": result.get("title", ""),
                "link": result.get("href") or result.get("url", ""),
                "snippet": result.get("body", "")[:400],
            })
    except Exception as e:
        return [{"error": str(e), "query": clean_query}]

    return results
