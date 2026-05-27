from synthesis.engine import (
    synthesize_sources,
    triangulate_numbers
)

from synthesis.conflict_resolver import (
    resolve_conflicts
)

from synthesis.narrative import (
    build_narrative
)


print("\n========================")
print("SYNTHESIS ENGINE TEST")
print("========================\n")


# -----------------------------------
# SOURCE SYNTHESIS TEST
# -----------------------------------

sources = [

    {
        "source_type": "web_search",
        "content": "Microsoft AI investment article."
    },

    {
        "source_type": "sec_filing",
        "content": "Official Microsoft filing."
    },

    {
        "source_type": "major_news",
        "content": "Reuters analysis."
    }
]

ranked = synthesize_sources(sources)

print("\n--- RANKED SOURCES ---\n")

print(ranked)


# -----------------------------------
# CONFLICT RESOLUTION TEST
# -----------------------------------

claims = [

    {
        "source_type": "web_search",
        "claim": "Revenue growth is 9%"
    },

    {
        "source_type": "financial_api",
        "claim": "Revenue growth is 14%"
    },

    {
        "source_type": "sec_filing",
        "claim": "Revenue growth is 13%"
    }
]

resolved = resolve_conflicts(claims)

print("\n--- RESOLVED CLAIM ---\n")

print(resolved)


# -----------------------------------
# TRIANGULATION TEST
# -----------------------------------

numbers = [100, 105, 98, 102]

triangulated = triangulate_numbers(numbers)

print("\n--- TRIANGULATION ---\n")

print(triangulated)


# -----------------------------------
# NARRATIVE TEST
# -----------------------------------

narrative = build_narrative([

    "Microsoft continues to expand cloud operations.",

    "AI investments remain a major strategic focus.",

    "Financial growth remains strong across segments."
])

print("\n--- NARRATIVE ---\n")

print(narrative)


print("\n========================")
print("ALL SYNTHESIS TESTS COMPLETE")
print("========================\n")