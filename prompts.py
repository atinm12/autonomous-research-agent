from agent.tools import TOOL_REGISTRY


def build_system_prompt():
    tool_descriptions = []

    for tool_name in TOOL_REGISTRY.keys():
        tool_descriptions.append(f"- {tool_name}")

    tools_text = "\n".join(tool_descriptions)

    prompt = f"""
You are an autonomous financial research agent.

You can use the following tools:

{tools_text}

When solving a task, always follow this format:

Thought: explain what you need
Action: tool_name
Action Input: input for tool

OR

Final Answer: your completed response

Only use available tools.
"""

    return prompt