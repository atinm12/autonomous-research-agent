"""
Prompt templates for the autonomous research agent.
"""


def build_system_prompt(tools: list[str]) -> str:
    """
    Build the main system prompt with dynamic tool injection.
    """

    tool_text = "\n".join([f"- {tool}" for tool in tools])

    return f"""
You are an autonomous financial research agent.

You can use the following tools:

{tool_text}

Use the ReAct format:

Thought:
Action:
Action Input:
Observation:

When finished, respond with:

Final Answer:
"""