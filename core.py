import os
from openai import OpenAI
from agent.prompts import build_system_prompt
from agent.parser import parse_llm_response
from agent.tools import TOOL_REGISTRY


class ResearchAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.max_iterations = 5

    def run(self, user_query):
        messages = [
            {
                "role": "system",
                "content": build_system_prompt()
            },
            {
                "role": "user",
                "content": user_query
            }
        ]

        iteration = 0

        while iteration < self.max_iterations:
            print(f"\n--- Iteration {iteration + 1} ---")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            llm_output = response.choices[0].message.content
            print("LLM Output:")
            print(llm_output)

            parsed = parse_llm_response(llm_output)

            if parsed["type"] == "final":
                return parsed["content"]

            elif parsed["type"] == "tool":
                tool_name = parsed["tool"]
                tool_input = parsed["input"]

                if tool_name not in TOOL_REGISTRY:
                    return f"Error: Tool {tool_name} not found"

                tool_result = TOOL_REGISTRY[tool_name](tool_input)

                print("\nTool Result:")
                print(tool_result)

                messages.append({
                    "role": "assistant",
                    "content": llm_output
                })

                messages.append({
                    "role": "user",
                    "content": f"Observation: {tool_result}"
                })

            iteration += 1

        return "Agent stopped: max iterations reached."