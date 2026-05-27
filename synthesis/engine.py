# -------------------------
# SOURCE RELIABILITY SCORES
# -------------------------

SOURCE_WEIGHTS = {

    "sec_filing": 1.0,

    "company_report": 0.9,

    "financial_api": 0.85,

    "major_news": 0.8,

    "web_search": 0.6,

    "social_media": 0.3
}


# -------------------------
# GET SOURCE WEIGHT
# -------------------------

def get_source_weight(source_type):

    return SOURCE_WEIGHTS.get(
        source_type,
        0.5
    )


# -------------------------
# SYNTHESIZE SOURCES
# -------------------------

def synthesize_sources(source_data):

    ranked = sorted(
        source_data,
        key=lambda x: get_source_weight(
            x["source_type"]
        ),
        reverse=True
    )

    return ranked
# -------------------------
# QUANTITATIVE TRIANGULATION
# -------------------------

def triangulate_numbers(values):

    if not values:
        return None

    average = sum(values) / len(values)

    minimum = min(values)

    maximum = max(values)

    spread = maximum - minimum

    return {
        "average": average,
        "minimum": minimum,
        "maximum": maximum,
        "spread": spread
    }