import re


def parse_llm_response(response_text):
    if "Final Answer:" in response_text:
        final_answer = response_text.split("Final Answer:")[1].strip()

        return {
            "type": "final",
            "content": final_answer
        }

    action_match = re.search(r"Action:\s*(.*)", response_text)
    input_match = re.search(r"Action Input:\s*(.*)", response_text)

    if action_match and input_match:
        return {
            "type": "tool",
            "tool": action_match.group(1).strip(),
            "input": input_match.group(1).strip()
        }

    return {
        "type": "error",
        "content": "Could not parse LLM response"
    }