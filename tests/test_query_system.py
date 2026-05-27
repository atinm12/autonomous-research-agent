from agent.query_analyzer import (
    analyze_query
)

from agent.disambiguation import (

    disambiguate_query,

    detect_edge_cases,

    detect_temporal_sensitivity
)


print("\n========================")
print("QUERY SYSTEM TEST")
print("========================\n")


# -----------------------------------
# QUERY ANALYSIS
# -----------------------------------

query = (
    "Compare Microsoft and Google "
    "cloud growth"
)

analysis = analyze_query(query)

print("\n--- QUERY ANALYSIS ---\n")

print(analysis)


# -----------------------------------
# AMBIGUOUS QUERY
# -----------------------------------

ambiguous = disambiguate_query(
    "Apple"
)

print("\n--- DISAMBIGUATION ---\n")

print(ambiguous)


# -----------------------------------
# EDGE CASES
# -----------------------------------

private_company = {

    "has_sec_filings": False,

    "years_public": 0,

    "financial_data_points": 1
}

edge_cases = detect_edge_cases(
    private_company
)

print("\n--- EDGE CASES ---\n")

print(edge_cases)


# -----------------------------------
# TEMPORAL SENSITIVITY
# -----------------------------------

text = (
    "The company is currently "
    "under acquisition discussions "
    "during a developing lawsuit."
)

temporal = detect_temporal_sensitivity(
    text
)

print("\n--- TEMPORAL SENSITIVITY ---\n")

print(temporal)


print("\n========================")
print("ALL QUERY TESTS COMPLETE")
print("========================\n")