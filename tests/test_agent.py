"""
Unit tests for the core agent module.
Tests the ReAct loop components without making real LLM/API calls.
"""

import pytest
from unittest.mock import patch, MagicMock

from agent.parser import parse_llm_response
from agent.prompts import build_system_prompt
from agent.tools import TOOL_REGISTRY, TOOL_DESCRIPTIONS


class TestParser:
    def test_parses_tool_call(self):
        text = "Thought: I need data\nAction: web_search\nAction Input: AAPL earnings"
        result = parse_llm_response(text)
        assert result["type"] == "tool"
        assert result["tool"] == "web_search"
        assert result["input"] == "AAPL earnings"

    def test_parses_final_answer(self):
        text = "Final Answer: Apple reported strong earnings."
        result = parse_llm_response(text)
        assert result["type"] == "final"
        assert "Apple" in result["content"]

    def test_prefers_tool_before_final_answer(self):
        text = "Action: web_search\nAction Input: Tesla\nFinal Answer: Done."
        result = parse_llm_response(text)
        assert result["type"] == "tool"

    def test_returns_error_on_unparseable(self):
        result = parse_llm_response("This has neither action nor final answer.")
        assert result["type"] == "error"


class TestPrompts:
    def test_build_system_prompt_includes_tools(self):
        tools = ["web_search", "sec_filing_search", "financial_data_api"]
        prompt = build_system_prompt(tools)
        for tool in tools:
            assert tool in prompt

    def test_build_system_prompt_contains_react_instructions(self):
        prompt = build_system_prompt(["web_search"])
        assert "Thought" in prompt
        assert "Action" in prompt
        assert "Observation" in prompt


class TestToolRegistry:
    def test_registry_has_minimum_10_distinct_tools(self):
        assert len(TOOL_REGISTRY) >= 10, (
            f"Expected ≥10 distinct tools, got {len(TOOL_REGISTRY)}"
        )

    def test_all_registered_tools_are_callable(self):
        for name, fn in TOOL_REGISTRY.items():
            assert callable(fn), f"Tool '{name}' is not callable"

    def test_all_tools_have_descriptions(self):
        for name in TOOL_REGISTRY:
            assert name in TOOL_DESCRIPTIONS, f"No description for tool '{name}'"
            assert len(TOOL_DESCRIPTIONS[name]) > 10

    def test_required_tools_present(self):
        required = {
            "financial_data_api", "sec_filing_search", "earnings_transcript",
            "web_search", "peer_comparison", "calculation_engine",
            "news_sentiment", "company_profile", "fact_checker",
            "vector_db_search", "vector_db_store", "report_generator",
        }
        for tool in required:
            assert tool in TOOL_REGISTRY, f"Required tool '{tool}' missing from registry"


class TestAgentCore:
    def test_agent_initializes(self):
        from agent.core import ResearchAgent
        with patch("agent.core.OpenAI"):
            agent = ResearchAgent()
            assert agent.max_iterations == 14

    def test_agent_returns_string(self):
        from agent.core import ResearchAgent
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            "Action: web_search\nAction Input: MSFT\n"
        )
        with patch("agent.core.OpenAI") as MockOpenAI:
            MockOpenAI.return_value.chat.completions.create.return_value = mock_response
            with patch("agent.core.store_memory"):
                with patch("agent.core.search_memory", return_value={"documents": [[]]}):
                    with patch("agent.core.log_episode"):
                        agent = ResearchAgent()
                        # Patch tool to avoid real API call
                        with patch.dict("agent.core.TOOL_REGISTRY",
                                        {"web_search": lambda q: "mock result"}):
                            agent.max_iterations = 1
                            result = agent.run("Test query")
                            assert isinstance(result, str)
