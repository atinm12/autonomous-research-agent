"""
Evaluation framework — 22 quality metrics across 5 categories.

Categories:
  FA — Factual Accuracy     (FA-1 … FA-5)
  CO — Completeness         (CO-1 … CO-4)
  AD — Analytical Depth     (AD-1 … AD-4)
  CS — Coherence/Structure  (CS-1 … CS-4)
  AB — Agent Behaviour      (AB-1 … AB-5)
"""

import re
import time


# =============================================================================
# CATEGORY 1: FACTUAL ACCURACY
# =============================================================================

def numerical_accuracy_score(generated: str, benchmark: str) -> float:
    """FA-1: % of numerical claims that match authoritative sources."""
    generated_numbers = re.findall(r"\d+\.?\d*", generated)
    benchmark_numbers = re.findall(r"\d+\.?\d*", benchmark)
    if not benchmark_numbers:
        return 1.0
    matches = sum(1 for n in generated_numbers if n in benchmark_numbers)
    return round(matches / len(benchmark_numbers), 2)


def citation_score(text: str) -> float:
    """FA-2: Citation presence and density score."""
    citations = re.findall(r"\[.*?\]|\((?:SEC|10-K|10-Q|Reuters|Bloomberg|FT|AP)[^)]*\)", text)
    if len(citations) == 0:
        return 0.0
    return min(1.0, round(len(citations) / 5, 2))


def temporal_accuracy_score(text: str) -> float:
    """FA-3: Whether time periods (quarters/years) are explicitly identified."""
    temporal_patterns = re.findall(
        r"Q[1-4]\s*20\d{2}|FY\s*20\d{2}|fiscal\s*year|year[- ]over[- ]year|YoY|TTM",
        text, re.IGNORECASE
    )
    return min(1.0, round(len(temporal_patterns) / 3, 2))


def entity_accuracy_score(text: str, expected_entities: list | None = None) -> float:
    """FA-4: Whether company/executive/product names are referenced accurately."""
    if expected_entities:
        found = sum(1 for e in expected_entities if e.lower() in text.lower())
        return round(found / len(expected_entities), 2)
    # Heuristic: presence of proper financial entity patterns
    entity_patterns = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc\.|Corp\.|Ltd\.|LLC|PLC)", text)
    return min(1.0, round(len(entity_patterns) / 3, 2))


def hallucination_score(generated: str, benchmark: str) -> float:
    """FA-5: Inverse of the ratio of unsupported words vs benchmark vocabulary."""
    generated_words = set(generated.lower().split())
    benchmark_words = set(benchmark.lower().split())
    unsupported = generated_words - benchmark_words
    ratio = len(unsupported) / max(1, len(generated_words))
    return round(1 - ratio, 2)


# =============================================================================
# CATEGORY 2: COMPLETENESS
# =============================================================================

REQUIRED_SECTIONS = [
    "executive summary",
    "financial",
    "risk",
    "competitive",
    "outlook",
]


def section_coverage_score(text: str) -> float:
    """CO-1: Fraction of required report sections present."""
    text_lower = text.lower()
    found = sum(1 for s in REQUIRED_SECTIONS if s in text_lower)
    return round(found / len(REQUIRED_SECTIONS), 2)


def source_diversity_score(source_types: list | None = None, text: str = "") -> float:
    """CO-2: Number of distinct source types used (target ≥ 4)."""
    if source_types is not None:
        distinct = len(set(source_types))
        return min(1.0, round(distinct / 4, 2))
    # Heuristic from text
    markers = {
        "sec": r"10-K|10-Q|SEC|EDGAR",
        "earnings": r"earnings call|transcript|CEO|CFO said",
        "news": r"Reuters|Bloomberg|FT|WSJ|news",
        "financial_api": r"\$[\d,.]+[BbMm]|\d+%|\bP/E\b|revenue",
    }
    found = sum(1 for m in markers.values() if re.search(m, text, re.IGNORECASE))
    return min(1.0, round(found / 4, 2))


def temporal_coverage_score(text: str, min_years: int = 3) -> float:
    """CO-3: Whether historical data spans at least min_years."""
    years = re.findall(r"20\d{2}", text)
    unique_years = set(years)
    if len(unique_years) >= min_years:
        return 1.0
    return round(len(unique_years) / min_years, 2)


def risk_factor_coverage_score(text: str) -> float:
    """CO-4: Coverage of material risk factor categories."""
    risk_categories = [
        "regulatory",
        "competitive",
        "financial risk",
        "operational",
        "macroeconomic",
        "technology",
        "market",
    ]
    text_lower = text.lower()
    found = sum(1 for r in risk_categories if r in text_lower)
    return round(found / len(risk_categories), 2)


# =============================================================================
# CATEGORY 3: ANALYTICAL DEPTH
# =============================================================================

def insight_density_score(text: str) -> float:
    """AD-1: Non-obvious analytical observations per page (proxy)."""
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    insight_keywords = [
        "growth", "risk", "opportunity", "competition", "strategy",
        "valuation", "advantage", "however", "despite", "although",
    ]
    insight_count = sum(
        1 for s in sentences
        if any(k in s.lower() for k in insight_keywords)
    )
    return round(min(1.0, insight_count / max(1, len(sentences))), 2)


def cross_source_synthesis_score(text: str) -> float:
    """AD-2: Number of multi-source synthesis instances (target ≥ 5)."""
    synthesis_patterns = re.findall(
        r"(?:however|despite|in contrast|while|although|yet|on the other hand|"
        r"corroborated|confirms|contradicts|consistent with|at odds with)",
        text, re.IGNORECASE
    )
    return min(1.0, round(len(synthesis_patterns) / 5, 2))


def quantitative_reasoning_score(text: str) -> float:
    """AD-3: Original calculations present (growth rates, margins, ratios)."""
    calc_patterns = re.findall(
        r"\d+\.?\d*\s*%|\bCAGR\b|\bP/E\b|\bEBITDA\b|margin\s+of\s+\d|"
        r"grew\s+(?:by\s+)?\d+|increased\s+(?:by\s+)?\d+|declined\s+(?:by\s+)?\d+",
        text, re.IGNORECASE
    )
    return min(1.0, round(len(calc_patterns) / 10, 2))


def forward_looking_score(text: str) -> float:
    """AD-4: Whether the report includes forward-looking analysis."""
    forward_patterns = re.findall(
        r"forecast|projection|outlook|next\s+(?:year|quarter)|going forward|"
        r"anticipated|expected to|will likely|scenario|2025|2026|2027|2028",
        text, re.IGNORECASE
    )
    return min(1.0, round(len(forward_patterns) / 4, 2))


# =============================================================================
# CATEGORY 4: COHERENCE AND STRUCTURE
# =============================================================================

def logical_flow_score(text: str) -> float:
    """CS-1: Presence of logical transition words indicating structured reasoning."""
    transition_words = [
        "however", "therefore", "additionally", "meanwhile",
        "furthermore", "consequently", "as a result", "in conclusion",
        "in contrast", "nevertheless",
    ]
    count = sum(1 for w in transition_words if w in text.lower())
    return round(min(1.0, count / 5), 2)


def internal_consistency_score(text: str) -> float:
    """CS-2: Absence of self-contradictions (heuristic: contradiction signal words)."""
    contradiction_signals = re.findall(
        r"(?:is both|simultaneously|yet also|but also says|contradicts itself)",
        text, re.IGNORECASE
    )
    return 1.0 if len(contradiction_signals) == 0 else max(0.0, round(1 - len(contradiction_signals) * 0.25, 2))


def executive_summary_score(text: str) -> float:
    """CS-3: Executive summary quality — key themes present."""
    keywords = ["company", "growth", "risk", "market", "strategy", "revenue", "competitive"]
    score = sum(1 for k in keywords if k in text.lower())
    return round(score / len(keywords), 2)


def professional_formatting_score(text: str) -> float:
    """CS-4: Structural formatting quality (headers, tables, length)."""
    score = 0.0
    if re.search(r"#{1,3}\s+\w+|^[A-Z][A-Z\s]+$", text, re.MULTILINE):
        score += 0.3
    if re.search(r"\|.*\||\+[-+]+\+", text):
        score += 0.3
    word_count = len(text.split())
    if word_count >= 500:
        score += 0.4
    return round(min(1.0, score), 2)


# =============================================================================
# CATEGORY 5: AGENT BEHAVIOUR
# =============================================================================

def tool_efficiency_score(tool_calls: int, successful_calls: int) -> float:
    """AB-1: Ratio of useful tool calls to total tool calls."""
    if tool_calls == 0:
        return 0.0
    return round(successful_calls / tool_calls, 2)


def error_recovery_rate_score(total_errors: int, recovered_errors: int) -> float:
    """AB-2: % of tool errors the agent recovered from via fallback."""
    if total_errors == 0:
        return 1.0
    return round(recovered_errors / total_errors, 2)


def planning_quality_score(plan_steps: list | None = None, text: str = "") -> float:
    """AB-3: Whether the agent's plan covers necessary research steps."""
    if plan_steps is not None:
        required = {"financial", "sec", "earnings", "web", "comparison"}
        covered = sum(1 for r in required if any(r in str(s).lower() for s in plan_steps))
        return round(covered / len(required), 2)
    # Heuristic from reasoning trace
    planning_markers = re.findall(
        r"(?:I will|I need to|First|Next|Then|Step \d|Plan:)",
        text, re.IGNORECASE
    )
    return min(1.0, round(len(planning_markers) / 5, 2))


def memory_utilization_score(memory_hits: int, total_api_calls: int) -> float:
    """AB-4: Ratio of memory hits to total API calls (higher = better memory use)."""
    if total_api_calls == 0:
        return 0.0
    return round(min(1.0, memory_hits / total_api_calls), 2)


def latency_score(elapsed_seconds: float, target_seconds: float = 300.0) -> float:
    """AB-5: Time-based score; full marks if under target, decays linearly above."""
    if elapsed_seconds <= target_seconds:
        return 1.0
    return round(max(0.0, 1 - (elapsed_seconds - target_seconds) / target_seconds), 2)


# =============================================================================
# AGGREGATE SCORER
# =============================================================================

ALL_METRIC_IDS = [
    "FA-1", "FA-2", "FA-3", "FA-4", "FA-5",
    "CO-1", "CO-2", "CO-3", "CO-4",
    "AD-1", "AD-2", "AD-3", "AD-4",
    "CS-1", "CS-2", "CS-3", "CS-4",
    "AB-1", "AB-2", "AB-3", "AB-4", "AB-5",
]


def score_report(
    generated: str,
    benchmark: str = "",
    tool_calls: int = 6,
    successful_calls: int = 6,
    total_errors: int = 0,
    recovered_errors: int = 0,
    memory_hits: int = 0,
    total_api_calls: int = 6,
    elapsed_seconds: float = 60.0,
    source_types: list | None = None,
) -> dict:
    """Run all 22 metrics against a generated report and return a score dict."""
    return {
        "FA-1_numerical_accuracy":      numerical_accuracy_score(generated, benchmark),
        "FA-2_citation_score":          citation_score(generated),
        "FA-3_temporal_accuracy":       temporal_accuracy_score(generated),
        "FA-4_entity_accuracy":         entity_accuracy_score(generated),
        "FA-5_hallucination_score":     hallucination_score(generated, benchmark),
        "CO-1_section_coverage":        section_coverage_score(generated),
        "CO-2_source_diversity":        source_diversity_score(source_types, generated),
        "CO-3_temporal_coverage":       temporal_coverage_score(generated),
        "CO-4_risk_factor_coverage":    risk_factor_coverage_score(generated),
        "AD-1_insight_density":         insight_density_score(generated),
        "AD-2_cross_source_synthesis":  cross_source_synthesis_score(generated),
        "AD-3_quantitative_reasoning":  quantitative_reasoning_score(generated),
        "AD-4_forward_looking":         forward_looking_score(generated),
        "CS-1_logical_flow":            logical_flow_score(generated),
        "CS-2_internal_consistency":    internal_consistency_score(generated),
        "CS-3_executive_summary":       executive_summary_score(generated),
        "CS-4_professional_formatting": professional_formatting_score(generated),
        "AB-1_tool_efficiency":         tool_efficiency_score(tool_calls, successful_calls),
        "AB-2_error_recovery_rate":     error_recovery_rate_score(total_errors, recovered_errors),
        "AB-3_planning_quality":        planning_quality_score(text=generated),
        "AB-4_memory_utilization":      memory_utilization_score(memory_hits, total_api_calls),
        "AB-5_latency":                 latency_score(elapsed_seconds),
    }
