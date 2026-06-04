import json
import requests

from tools.utils import cache_result, rate_limit


# Zero-padded CIK numbers from SEC EDGAR
TICKER_TO_CIK = {
    "AMZN":  "0001018724",
    "MSFT":  "0000789019",
    "GOOGL": "0001652044",
    "GOOG":  "0001652044",
    "AAPL":  "0000320193",
    "NVDA":  "0001045810",
    "META":  "0001326801",
}

TICKER_TO_COMPANY = {
    "AMZN":  "Amazon",
    "MSFT":  "Microsoft",
    "GOOGL": "Alphabet",
    "GOOG":  "Alphabet",
    "AAPL":  "Apple",
    "NVDA":  "NVIDIA",
    "META":  "Meta Platforms",
}


def _parse_query(input_val):
    """
    Accept a plain string ("Amazon" / "AMZN") or a JSON dict with a
    "query", "company_name", or "ticker" key.
    Returns the resolved string in UPPER CASE.
    """
    text = str(input_val).strip().strip('"\'')
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            raw = (
                parsed.get("query")
                or parsed.get("company_name")
                or parsed.get("company")
                or parsed.get("ticker")
                or text
            )
            text = str(raw).strip()
    except (json.JSONDecodeError, ValueError):
        pass
    return text.upper()


@cache_result
@rate_limit(seconds=2)
def search_sec_filings(input_val):
    """
    Retrieve recent 10-K and 10-Q filings for a company using the SEC EDGAR
    submissions API (data.sec.gov/submissions/CIK{cik}.json).
    Accepts a ticker symbol, company name, or JSON dict.
    """
    query = _parse_query(input_val)

    # Resolve to CIK
    cik = TICKER_TO_CIK.get(query)
    if not cik:
        # Partial name match (e.g. "AMAZON" → AMZN)
        for ticker, name in TICKER_TO_COMPANY.items():
            if query in name.upper() or name.upper() in query:
                cik = TICKER_TO_CIK[ticker]
                break

    if not cik:
        return {
            "message": (
                f"No CIK mapping for '{query}'. "
                "Try a ticker such as AMZN, MSFT, or GOOGL."
            ),
            "query": query,
        }

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {
        "User-Agent": "atinmathur12@gmail.com",
        "Accept": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        company_name = data.get("name", query)
        recent      = data.get("filings", {}).get("recent", {})
        forms       = recent.get("form", [])
        dates       = recent.get("filingDate", [])
        periods     = recent.get("reportDate", [])
        accessions  = recent.get("accessionNumber", [])

        results = []
        for i, form in enumerate(forms):
            if form in ("10-K", "10-Q") and len(results) < 5:
                results.append({
                    "company":      company_name,
                    "form_type":    form,
                    "period":       periods[i] if i < len(periods) else None,
                    "filed_at":     dates[i] if i < len(dates) else None,
                    "accession_no": accessions[i] if i < len(accessions) else None,
                    "description":  f"{form} filing — {company_name}",
                })

        if not results:
            return {
                "message": "No 10-K or 10-Q filings found in recent history",
                "company": company_name,
            }
        return results

    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP {e.response.status_code}", "query": query}
    except Exception as e:
        return {"error": str(e), "query": query}
