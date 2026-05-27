from tools.tool_registry import ToolRegistry
from tools.implementations import sec_filing_search

registry = ToolRegistry()

sec_schema = {
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

registry.register_tool(
    "sec_filing_search",
    sec_schema,
    sec_filing_search
)

print("Registered tools:")
print(registry.list_tools())

print("\nVALID INPUT TEST:")

result = registry.execute_tool(
    "sec_filing_search",
    {
        "ticker": "AAPL",
        "filing_type": "10-K"
    }
)

print(result)