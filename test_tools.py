import unittest

from tools.tool_registry import ToolRegistry
from tools.implementations import (
    sec_filing_search,
    web_search,
    financial_data_api
)


class TestToolRegistry(unittest.TestCase):

    def setUp(self):
        """
        Runs before every test
        Creates fresh registry
        """

        self.registry = ToolRegistry()

        self.sec_schema = {
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string"
                    },
                    "filing_type": {
                        "type": "string"
                    }
                },
                "required": ["ticker", "filing_type"]
            }
        }

        self.web_schema = {
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    }
                },
                "required": ["query"]
            }
        }

        self.financial_schema = {
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string"
                    }
                },
                "required": ["ticker"]
            }
        }

        self.registry.register_tool(
            "sec_filing_search",
            self.sec_schema,
            sec_filing_search
        )

        self.registry.register_tool(
            "web_search",
            self.web_schema,
            web_search
        )

        self.registry.register_tool(
            "financial_data_api",
            self.financial_schema,
            financial_data_api
        )

    def test_tool_registration(self):
        tools = self.registry.list_tools()

        self.assertIn("sec_filing_search", tools)
        self.assertIn("web_search", tools)
        self.assertIn("financial_data_api", tools)

    def test_valid_tool_execution(self):
        result = self.registry.execute_tool(
            "sec_filing_search",
            {
                "ticker": "AAPL",
                "filing_type": "10-K"
            }
        )

        self.assertEqual(result["ticker"], "AAPL")
        self.assertEqual(result["filing_type"], "10-K")

    def test_invalid_input_validation(self):
        with self.assertRaises(ValueError):
            self.registry.execute_tool(
                "sec_filing_search",
                {
                    "ticker": "AAPL"
                }
            )


class TestToolImplementations(unittest.TestCase):

    def test_web_search(self):
        result = web_search(
            {
                "query": "Apple earnings"
            }
        )

        self.assertEqual(
            result["query"],
            "Apple earnings"
        )

        self.assertTrue(
            len(result["results"]) > 0
        )

    def test_financial_data_api(self):
        result = financial_data_api(
            {
                "ticker": "AAPL"
            }
        )

        self.assertEqual(
            result["ticker"],
            "AAPL"
        )

        self.assertIn(
            "revenue",
            result
        )

    def test_sec_filing_search(self):
        result = sec_filing_search(
            {
                "ticker": "AAPL",
                "filing_type": "10-K"
            }
        )

        self.assertEqual(
            result["ticker"],
            "AAPL"
        )

        self.assertEqual(
            result["filing_type"],
            "10-K"
        )


if __name__ == "__main__":
    unittest.main()