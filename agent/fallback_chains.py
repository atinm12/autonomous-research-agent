from tools.company_profile import (
    get_company_profile
)

from tools.financial_api import (
    get_financial_metrics
)

from tools.web_search import (
    web_search
)

from tools.sec_edgar import (
    search_sec_filings
)


# -----------------------------------
# TOOL FALLBACK MAP
# -----------------------------------

FALLBACK_CHAINS = {

    "company_profile": [

        get_company_profile,

        web_search,

        search_sec_filings
    ],

    "financial_metrics": [

        get_financial_metrics,

        web_search,

        search_sec_filings
    ]
}


# -----------------------------------
# EXECUTE FALLBACK CHAIN
# -----------------------------------

def execute_with_fallbacks(
    tool_name,
    query
):

    chain = FALLBACK_CHAINS.get(
        tool_name,
        []
    )

    for tool in chain:

        try:

            print(
                f"\nTrying: {tool.__name__}"
            )

            result = tool(query)

            if result:

                return {
                    "success": True,
                    "tool_used": tool.__name__,
                    "result": result
                }

        except Exception as e:

            print(
                f"Failed: {e}"
            )

    return {
        "success": False,
        "error": (
            f"All fallbacks failed "
            f"for {tool_name}"
        )
    }