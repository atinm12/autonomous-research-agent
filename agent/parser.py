import re


def parse_llm_response(response_text):
    """
    Parse one LLM turn into either a tool call or a final answer.

    If the LLM writes a planning block that contains both Action/Action Input
    AND a Final Answer in the same response, we extract the FIRST tool call
    (its position in the text comes before Final Answer:) so tools are
    actually executed rather than skipped.
    """
    action_match = re.search(r"Action:\s*(.+)", response_text)
    input_match  = re.search(r"Action Input:\s*(.+)", response_text)
    final_pos    = response_text.find("Final Answer:")

    # If there is a tool call whose Action: marker appears before Final Answer:
    # (or there is no Final Answer at all), execute the tool.
    if action_match and input_match:
        if final_pos == -1 or action_match.start() < final_pos:
            return {
                "type":  "tool",
                "tool":  action_match.group(1).strip(),
                "input": input_match.group(1).strip(),
            }

    # Only reach here when Final Answer comes before any Action block
    # (or there are no Action blocks at all).
    if final_pos != -1:
        return {
            "type":    "final",
            "content": response_text[final_pos + len("Final Answer:"):].strip(),
        }

    return {
        "type":    "error",
        "content": "Could not parse LLM response",
    }