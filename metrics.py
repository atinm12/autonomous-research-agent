import re


# -----------------------------------
# NUMERICAL ACCURACY
# -----------------------------------

def numerical_accuracy_score(
    generated,
    benchmark
):

    generated_numbers = re.findall(
        r"\d+",
        generated
    )

    benchmark_numbers = re.findall(
        r"\d+",
        benchmark
    )

    if not benchmark_numbers:
        return 1.0

    matches = 0

    for num in generated_numbers:

        if num in benchmark_numbers:

            matches += 1

    return round(
        matches / len(benchmark_numbers),
        2
    )


# -----------------------------------
# CITATION VALIDATOR
# -----------------------------------

def citation_score(text):

    citations = re.findall(
        r"\[.*?\]",
        text
    )

    if len(citations) == 0:

        return 0.0

    return min(
        1.0,
        len(citations) / 5
    )


# -----------------------------------
# HALLUCINATION DETECTOR
# -----------------------------------

def hallucination_score(
    generated,
    benchmark
):

    generated_words = set(
        generated.lower().split()
    )

    benchmark_words = set(
        benchmark.lower().split()
    )

    unsupported = generated_words - benchmark_words

    ratio = len(unsupported) / max(
        1,
        len(generated_words)
    )

    return round(
        1 - ratio,
        2
    )


# -----------------------------------
# TOOL EFFICIENCY
# -----------------------------------

def tool_efficiency_score(
    tool_calls,
    successful_calls
):

    if tool_calls == 0:
        return 0

    return round(
        successful_calls / tool_calls,
        2
    )


# -----------------------------------
# INSIGHT DENSITY
# -----------------------------------

def insight_density_score(text):

    sentences = text.split(".")

    insight_keywords = [

        "growth",
        "risk",
        "opportunity",
        "competition",
        "strategy",
        "valuation",
        "advantage"
    ]

    insight_count = 0

    for sentence in sentences:

        if any(
            keyword in sentence.lower()
            for keyword in insight_keywords
        ):

            insight_count += 1

    return round(
        insight_count / max(1, len(sentences)),
        2
    )


# -----------------------------------
# LOGICAL FLOW SCORE
# -----------------------------------

def logical_flow_score(text):

    transition_words = [

        "however",
        "therefore",
        "additionally",
        "meanwhile",
        "furthermore"
    ]

    count = 0

    for word in transition_words:

        if word in text.lower():

            count += 1

    return round(
        min(1.0, count / 3),
        2
    )


# -----------------------------------
# EXECUTIVE SUMMARY QUALITY
# -----------------------------------

def executive_summary_score(text):

    keywords = [

        "company",
        "growth",
        "risk",
        "market",
        "strategy"
    ]

    score = 0

    for keyword in keywords:

        if keyword in text.lower():

            score += 1

    return round(
        score / len(keywords),
        2
    )