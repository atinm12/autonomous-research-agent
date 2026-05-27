from duckduckgo_search import DDGS

from tools.utils import cache_result, rate_limit


@cache_result
@rate_limit(seconds=2)
def web_search(query):

    results = []

    with DDGS() as ddgs:

        search_results = ddgs.text(query, max_results=5)

        for result in search_results:

            results.append({
                "title": result["title"],
                "link": result["href"]
            })

    return results