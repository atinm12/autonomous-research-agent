from tools.utils import cache_result, rate_limit


# duckduckgo_search was renamed to ddgs in v9+; support both
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


def _run_ddgs(query: str, max_results: int = 8) -> list:
    """Run a single DuckDuckGo search; return list of result dicts."""
    ddgs = DDGS()
    results = []
    for result in ddgs.text(query, max_results=max_results):
        results.append({
            "title":   result.get("title", ""),
            "link":    result.get("href") or result.get("url", ""),
            "snippet": result.get("body", "")[:400],
        })
    return results


@cache_result
@rate_limit(seconds=2)
def web_search(query):
    """
    Search the web using DuckDuckGo.
    Accepts a plain string or a quoted string from the LLM.
    Returns a list of {title, link, snippet} dicts.
    Retries with a shorter query if the first attempt returns nothing.
    """
    clean_query = str(query).strip().strip('"\'')

    try:
        results = _run_ddgs(clean_query)
        if not results:
            # Retry with a shorter version (first 6 words) to avoid over-specificity
            short_query = " ".join(clean_query.split()[:6])
            if short_query != clean_query:
                results = _run_ddgs(short_query)
        return results if results else [{"message": "No results found", "query": clean_query}]
    except Exception as e:
        return [{"error": str(e), "query": clean_query}]
