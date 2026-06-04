"""
Unit tests for the multi-source synthesis engine and conflict resolver.
"""

import pytest
from synthesis.engine import synthesize_sources, triangulate_numbers, get_source_weight
from synthesis.conflict_resolver import resolve_conflicts
from synthesis.narrative import build_narrative


class TestSourceReliability:
    def test_sec_filing_highest_weight(self):
        assert get_source_weight("sec_filing") == 1.0

    def test_unknown_source_gets_default(self):
        weight = get_source_weight("unknown_source_xyz")
        assert 0.0 < weight <= 1.0

    def test_web_search_lower_than_sec(self):
        assert get_source_weight("web_search") < get_source_weight("sec_filing")

    def test_financial_api_lower_than_sec(self):
        assert get_source_weight("financial_api") < get_source_weight("sec_filing")


class TestSynthesizeSources:
    def setup_method(self):
        self.sources = [
            {"source_type": "web_search",    "content": "Article about revenue."},
            {"source_type": "sec_filing",    "content": "Official 10-K revenue figure."},
            {"source_type": "major_news",    "content": "Reuters revenue analysis."},
        ]

    def test_returns_sorted_list(self):
        ranked = synthesize_sources(self.sources)
        assert isinstance(ranked, list)
        assert len(ranked) == 3

    def test_sec_filing_is_first(self):
        ranked = synthesize_sources(self.sources)
        assert ranked[0]["source_type"] == "sec_filing"

    def test_web_search_is_last(self):
        ranked = synthesize_sources(self.sources)
        assert ranked[-1]["source_type"] == "web_search"

    def test_empty_input(self):
        assert synthesize_sources([]) == []


class TestTriangulateNumbers:
    def test_basic_triangulation(self):
        result = triangulate_numbers([100, 105, 98, 102])
        assert result["average"] == pytest.approx(101.25)
        assert result["minimum"] == 98
        assert result["maximum"] == 105
        assert result["spread"] == 7

    def test_single_value(self):
        result = triangulate_numbers([50])
        assert result["average"] == 50
        assert result["spread"] == 0

    def test_empty_returns_none(self):
        assert triangulate_numbers([]) is None


class TestConflictResolver:
    def setup_method(self):
        self.claims = [
            {"source_type": "web_search",    "claim": "Revenue growth is 9%"},
            {"source_type": "financial_api", "claim": "Revenue growth is 14%"},
            {"source_type": "sec_filing",    "claim": "Revenue growth is 13%"},
        ]

    def test_resolves_to_most_reliable_source(self):
        result = resolve_conflicts(self.claims)
        assert result["resolved_claim"]["source_type"] == "sec_filing"

    def test_returns_all_claims(self):
        result = resolve_conflicts(self.claims)
        assert len(result["all_claims"]) == 3

    def test_empty_claims(self):
        result = resolve_conflicts([])
        assert result is None

    def test_single_claim(self):
        result = resolve_conflicts([self.claims[0]])
        assert result["resolved_claim"]["claim"] == "Revenue growth is 9%"


class TestNarrativeBuilder:
    def test_builds_narrative_from_list(self):
        points = [
            "Microsoft continues to expand cloud operations.",
            "AI investments remain a major strategic focus.",
        ]
        narrative = build_narrative(points)
        assert "Microsoft" in narrative
        assert "AI" in narrative

    def test_empty_input(self):
        assert build_narrative([]) == ""

    def test_each_point_appears_once(self):
        points = ["Point A", "Point B", "Point C"]
        narrative = build_narrative(points)
        for p in points:
            assert p in narrative
