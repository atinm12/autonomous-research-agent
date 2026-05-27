from agent.query_analyzer import (
    analyze_query
)


# -----------------------------------
# DISAMBIGUATION LOGIC
# -----------------------------------

def disambiguate_query(query):

    analysis = analyze_query(query)

    ambiguity = analysis["ambiguity"]


    # -----------------------------------
    # HIGH AMBIGUITY
    # -----------------------------------

    if ambiguity == "high":

        return {

            "status": "clarification_needed",

            "message": (
                f"The query '{query}' is ambiguous. "
                f"Please clarify the exact focus "
                f"of the research request."
            )
        }


    # -----------------------------------
    # MEDIUM AMBIGUITY
    # -----------------------------------

    elif ambiguity == "medium":

        return {

            "status": "assumption_made",

            "message": (
                f"The system assumed the query "
                f"refers to the most common "
                f"financial interpretation."
            )
        }


    # -----------------------------------
    # LOW AMBIGUITY
    # -----------------------------------

    return {

        "status": "clear",

        "message": (
            "Query sufficiently clear."
        )
    }
# -----------------------------------
# EDGE CASE HANDLING
# -----------------------------------

def detect_edge_cases(company_data):

    issues = []


    # -----------------------------------
    # PRIVATE COMPANY
    # -----------------------------------

    if not company_data.get(
        "has_sec_filings",
        True
    ):

        issues.append(
            "Private company detected. "
            "SEC filing data unavailable."
        )


    # -----------------------------------
    # NEW IPO
    # -----------------------------------

    if company_data.get(
        "years_public",
        10
    ) < 2:

        issues.append(
            "Limited public history "
            "detected due to recent IPO."
        )


    # -----------------------------------
    # LIMITED DATA
    # -----------------------------------

    if company_data.get(
        "financial_data_points",
        10
    ) < 3:

        issues.append(
            "Limited financial data available."
        )


    return issues
# -----------------------------------
# TEMPORAL SENSITIVITY DETECTION
# -----------------------------------

def detect_temporal_sensitivity(text):

    keywords = [

        "acquisition",
        "merger",
        "bankruptcy",
        "investigation",
        "lawsuit",
        "earnings release",
        "breaking",
        "developing"
    ]

    detected = []

    text_lower = text.lower()

    for keyword in keywords:

        if keyword in text_lower:

            detected.append(keyword)

    if detected:

        return {

            "temporal_sensitivity": True,

            "detected_topics": detected,

            "warning": (
                "Rapidly changing circumstances "
                "detected. Information may "
                "change quickly."
            )
        }

    return {

        "temporal_sensitivity": False
    }