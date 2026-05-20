from tools.web_search import web_search


def fact_check(claim):

    results = web_search(claim)

    if not results:
        return "No supporting sources found."

    verified_sources = []

    for result in results:

        verified_sources.append({
            "title": result.get("title"),
            "link": result.get("link")
        })

    return {
        "claim": claim,
        "sources": verified_sources
    }