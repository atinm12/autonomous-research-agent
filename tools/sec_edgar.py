import json
import requests

from tools.utils import cache_result, rate_limit


def _parse_query(input_val):
    """
    Accept a plain string ("Amazon Web Services") or a JSON dict
    with a "query", "company_name", or "ticker" key.
    Returns a plain query string.
    """
    text = str(input_val).strip().strip('"\'')
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return (
                parsed.get("query")
                or parsed.get("company_name")
                or parsed.get("company")
                or parsed.get("ticker")
                or text
            )
    except (json.JSONDecodeError, ValueError):
        pass
    return text


@cache_result
@rate_limit(seconds=2)
def search_sec_filings(input_val):
    """
    Search SEC EDGAR full-text search for 10-K / 10-Q filings.
    Uses a GET request to the correct EFTS endpoint.
    Accepts a plain company name or a JSON dict with a "query" key.
    """
    query = _parse_query(input_val)

    # Correct endpoint: GET with query params, NOT POST with JSON body
    url = "https://efts.sec.gov/LATEST/search-index"
    params = {
        "q": f'"{query}"',
        "forms": "10-K,10-Q",
        "dateRange": "custom",
        "startdt": "2022-01-01",
        "enddt": "2025-12-31",
    }
    headers = {
        "User-Agent": "atinmathur12@gmail.com",
        "Accept": "application/json",
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            return {"message": "No filings found", "query": query}

        results = []
        for hit in hits[:5]:
            src = hit.get("_source", {})
            results.append({
                "company": src.get("entity_name"),
                "form_type": src.get("file_type"),
                "period": src.get("period_of_report"),
                "filed_at": src.get("file_date"),
                "accession_no": src.get("accession_no"),
                "description": src.get("form_type"),
            })
        return results

    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP {e.response.status_code}", "query": query}
    except Exception as e:
        return {"error": str(e), "query": query}
