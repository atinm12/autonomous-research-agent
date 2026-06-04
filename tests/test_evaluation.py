"""
Unit tests for the evaluation framework — all 22 quality metrics.
"""

import pytest
from evaluation.metrics import (
    # FA
    numerical_accuracy_score,
    citation_score,
    temporal_accuracy_score,
    entity_accuracy_score,
    hallucination_score,
    # CO
    section_coverage_score,
    source_diversity_score,
    temporal_coverage_score,
    risk_factor_coverage_score,
    # AD
    insight_density_score,
    cross_source_synthesis_score,
    quantitative_reasoning_score,
    forward_looking_score,
    # CS
    logical_flow_score,
    internal_consistency_score,
    executive_summary_score,
    professional_formatting_score,
    # AB
    tool_efficiency_score,
    error_recovery_rate_score,
    planning_quality_score,
    memory_utilization_score,
    latency_score,
    # Aggregate
    score_report,
    ALL_METRIC_IDS,
)

SAMPLE_REPORT = """
## Executive Summary
Microsoft Corporation (NASDAQ: MSFT) reported strong financial results in Q3 FY2024.
Revenue grew 17% year-over-year to $61.9B. Azure cloud revenue increased 31% YoY.
However, the company faces regulatory risks in the EU related to antitrust concerns.
Despite competitive pressure, Microsoft's strategic positioning in AI remains strong.

## Financial Analysis
According to the 10-K filing (SEC EDGAR), Microsoft reported FY2023 revenue of $211.9B,
a 7% increase from FY2022. Intelligent Cloud segment revenue reached $87.9B (Reuters).
Operating margin improved to 42% due to scalable cloud infrastructure.
Revenue CAGR of 11% over the past 3 years (2021, 2022, 2023) reflects consistent growth.
Furthermore, gross margin expanded to 69.4%.

## Risk Assessment
Key regulatory risks include the EU Digital Markets Act and DOJ antitrust investigation.
Macroeconomic risks from rising interest rates and enterprise IT spending slowdown.
Competitive risks from AWS and Google Cloud. Operational risk from cybersecurity threats.
Financial risk tied to rising capital expenditure for AI infrastructure.

## Competitive Positioning
Microsoft Azure holds approximately 22% cloud market share, however AWS leads at 32%.
Therefore Azure's growth rate outpaces AWS in recent quarters. As a result, Microsoft
is gaining enterprise customers. In contrast, Google Cloud has 11% market share.
Additionally, Microsoft's Copilot AI strategy provides differentiation.

## Outlook
Revenue forecasts for FY2025 project 15-20% growth, expected to continue through 2026.
Management anticipates Azure will maintain 25-30% growth going forward.
Scenario analysis suggests EPS of $12-14 by 2026 if AI monetization proceeds as planned.
"""


class TestFactualAccuracy:
    def test_fa1_numerical_accuracy_with_matching_numbers(self):
        score = numerical_accuracy_score("revenue 100 growth 15", "revenue 100 growth 15")
        assert score == 1.0

    def test_fa1_numerical_accuracy_with_no_benchmark(self):
        score = numerical_accuracy_score("some text 42", "")
        assert score == 1.0

    def test_fa2_citation_score_with_citations(self):
        text = "Revenue grew [SEC 10-K] and margins improved (Reuters)."
        score = citation_score(text)
        assert score > 0

    def test_fa2_citation_score_no_citations(self):
        assert citation_score("No citations here.") == 0.0

    def test_fa2_citation_score_bounded(self):
        text = " ".join([f"[cite{i}]" for i in range(20)])
        assert citation_score(text) <= 1.0

    def test_fa3_temporal_accuracy_with_quarters(self):
        text = "Q1 2024 revenue grew 13% YoY compared to Q1 2023."
        score = temporal_accuracy_score(text)
        assert score > 0

    def test_fa3_temporal_accuracy_empty(self):
        assert temporal_accuracy_score("no temporal data") == 0.0

    def test_fa4_entity_accuracy_with_expected_entities(self):
        score = entity_accuracy_score("Microsoft and Apple reported results.", ["Microsoft", "Apple"])
        assert score == 1.0

    def test_fa4_entity_accuracy_partial(self):
        score = entity_accuracy_score("Only Microsoft mentioned.", ["Microsoft", "Apple"])
        assert score == 0.5

    def test_fa5_hallucination_identical(self):
        text = "Microsoft revenue grew"
        assert hallucination_score(text, text) == 1.0

    def test_fa5_hallucination_empty_benchmark(self):
        score = hallucination_score("Microsoft revenue grew strongly", "")
        assert 0.0 <= score <= 1.0


class TestCompleteness:
    def test_co1_section_coverage_full(self):
        score = section_coverage_score(SAMPLE_REPORT)
        assert score >= 0.8

    def test_co1_section_coverage_empty(self):
        assert section_coverage_score("") == 0.0

    def test_co2_source_diversity_with_list(self):
        types = ["sec_filing", "financial_api", "major_news", "web_search"]
        assert source_diversity_score(source_types=types) == 1.0

    def test_co2_source_diversity_from_text(self):
        score = source_diversity_score(text=SAMPLE_REPORT)
        assert score > 0

    def test_co3_temporal_coverage_multi_year(self):
        text = "In 2021, 2022, and 2023 revenue grew consistently."
        assert temporal_coverage_score(text) == 1.0

    def test_co3_temporal_coverage_single_year(self):
        score = temporal_coverage_score("In 2023 revenue grew.", min_years=3)
        assert score < 1.0

    def test_co4_risk_factor_coverage(self):
        score = risk_factor_coverage_score(SAMPLE_REPORT)
        assert score >= 0.5


class TestAnalyticalDepth:
    def test_ad1_insight_density_informative_text(self):
        score = insight_density_score(SAMPLE_REPORT)
        assert score > 0

    def test_ad2_cross_source_synthesis(self):
        score = cross_source_synthesis_score(SAMPLE_REPORT)
        assert score > 0

    def test_ad2_no_synthesis_keywords(self):
        assert cross_source_synthesis_score("Revenue is high. Growth is good.") == 0.0

    def test_ad3_quantitative_reasoning(self):
        text = "Revenue grew 15%. Operating margin of 42%. CAGR of 11% over 3 years."
        score = quantitative_reasoning_score(text)
        assert score > 0

    def test_ad4_forward_looking(self):
        text = "Revenue is expected to grow 20% in 2025 and 2026. Outlook is positive."
        score = forward_looking_score(text)
        assert score > 0

    def test_ad4_no_forward_looking(self):
        assert forward_looking_score("Historical results show past revenue.") == 0.0


class TestCoherenceStructure:
    def test_cs1_logical_flow_with_transitions(self):
        score = logical_flow_score(SAMPLE_REPORT)
        assert score > 0

    def test_cs1_logical_flow_no_transitions(self):
        assert logical_flow_score("Revenue is high. Margins are good.") == 0.0

    def test_cs2_internal_consistency_clean_text(self):
        assert internal_consistency_score(SAMPLE_REPORT) == 1.0

    def test_cs3_executive_summary_quality(self):
        score = executive_summary_score(SAMPLE_REPORT)
        assert score >= 0.5

    def test_cs4_professional_formatting_with_headers(self):
        text = "## Executive Summary\nRevenue grew.\n\n## Risk\nSome risks.\n" * 100
        score = professional_formatting_score(text)
        assert score >= 0.3


class TestAgentBehaviour:
    def test_ab1_tool_efficiency_all_useful(self):
        assert tool_efficiency_score(6, 6) == 1.0

    def test_ab1_tool_efficiency_none_useful(self):
        assert tool_efficiency_score(6, 0) == 0.0

    def test_ab1_tool_efficiency_zero_calls(self):
        assert tool_efficiency_score(0, 0) == 0.0

    def test_ab2_error_recovery_no_errors(self):
        assert error_recovery_rate_score(0, 0) == 1.0

    def test_ab2_error_recovery_full_recovery(self):
        assert error_recovery_rate_score(3, 3) == 1.0

    def test_ab2_error_recovery_partial(self):
        score = error_recovery_rate_score(4, 2)
        assert score == 0.5

    def test_ab3_planning_quality_from_plan_steps(self):
        steps = ["financial analysis", "sec filing search", "earnings call review",
                 "web search", "peer comparison"]
        score = planning_quality_score(plan_steps=steps)
        assert score >= 0.8

    def test_ab4_memory_utilization_ratio(self):
        score = memory_utilization_score(memory_hits=3, total_api_calls=10)
        assert score == pytest.approx(0.3)

    def test_ab4_memory_utilization_zero_calls(self):
        assert memory_utilization_score(0, 0) == 0.0

    def test_ab5_latency_under_target(self):
        assert latency_score(60, target_seconds=300) == 1.0

    def test_ab5_latency_over_target(self):
        score = latency_score(600, target_seconds=300)
        assert 0.0 <= score < 1.0

    def test_ab5_latency_very_slow(self):
        score = latency_score(3000, target_seconds=300)
        assert score == 0.0


class TestAggregateScorer:
    def test_score_report_returns_all_22_metrics(self):
        scores = score_report(SAMPLE_REPORT, benchmark="Microsoft revenue risk market strategy")
        assert len(scores) == 22

    def test_score_report_all_values_in_range(self):
        scores = score_report(SAMPLE_REPORT, benchmark="Microsoft revenue risk market strategy")
        for key, val in scores.items():
            assert 0.0 <= val <= 1.0, f"Metric {key} out of [0,1] range: {val}"

    def test_all_metric_ids_defined(self):
        assert len(ALL_METRIC_IDS) == 22
        expected_prefixes = {"FA", "CO", "AD", "CS", "AB"}
        for mid in ALL_METRIC_IDS:
            prefix = mid.split("-")[0]
            assert prefix in expected_prefixes
