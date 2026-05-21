from synthesis.engine import get_source_weight


def resolve_conflicts(claims):

    if not claims:
        return None

    ranked = sorted(
        claims,
        key=lambda x: get_source_weight(
            x["source_type"]
        ),
        reverse=True
    )

    best_claim = ranked[0]

    return {
        "resolved_claim": best_claim,
        "all_claims": ranked
    }