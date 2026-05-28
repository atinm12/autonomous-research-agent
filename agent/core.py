"""
Core autonomous research agent implementation.

This module contains the primary ReAct reasoning loop,
tool orchestration, and LLM interaction logic.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

from agent.prompts import build_system_prompt
from agent.parser import parse_llm_response
from agent.tools import TOOL_REGISTRY

load_dotenv()


class ResearchAgent:
    def __init__(self):

        self.client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
        )

        # Prevent infinite loops
        self.max_iterations = 10

    # Main ReAct reasoning loop
    def run(self, query: str) -> str:

        messages = [
            {
                "role": "system",
                "content": build_system_prompt(
                    list(TOOL_REGISTRY.keys())
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]

        iteration = 0

        while iteration < self.max_iterations:

            print(f"\n--- Iteration {iteration + 1} ---")

            # Call OpenAI model
            response = self.client.chat.completions.create(
                max_tokens=5000,
                temperature=0.2,
                model="gpt-4o-mini",
                messages=messages
            )

            llm_output = response.choices[0].message.content

            print("\nLLM OUTPUT:")
            print(llm_output)

            # Parse the LLM output
            parsed = parse_llm_response(llm_output)

            # -------------------------
            # FINAL ANSWER
            # -------------------------
            if parsed["type"] == "final":
                return parsed["content"]

            # -------------------------
            # TOOL EXECUTION
            # -------------------------
            elif parsed["type"] == "tool":

                tool_name = parsed["tool"]
                tool_input = parsed["input"]

                # Verify tool exists
                if tool_name not in TOOL_REGISTRY:
                    return f"Tool '{tool_name}' not found."

                print(f"\nRunning Tool: {tool_name}")
                print(f"Tool Input: {tool_input}")

                # Execute tool
                tool_result = TOOL_REGISTRY[tool_name](tool_input)

                print("\nTOOL RESULT:")
                print(tool_result)

                # Add assistant response
                messages.append({
                    "role": "assistant",
                    "content": llm_output
                })

                # Add observation
                messages.append({
                    "role": "user",
                    "content": f"Observation: {tool_result}"
                })

            # -------------------------
            # PARSE FAILURE
            # -------------------------
            else:
                return f"Parser Error:\n{parsed['content']}"

            iteration += 1

        return "Agent stopped: max iterations reached."