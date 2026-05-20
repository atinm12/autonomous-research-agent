import requests

from tools.utils import cache_result, rate_limit


@cache_result
@rate_limit(seconds=2)
def search_sec_filings(company_name):

    url = "https://efts.sec.gov/LATEST/search-index"

    payload = {
        "keys": company_name,
        "category": "custom",
        "forms": ["10-K", "10-Q"]
    }

    headers = {
        "User-Agent": "atinmathur12@gmail.com"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    return response.json()