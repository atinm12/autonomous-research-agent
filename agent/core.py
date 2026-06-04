"""
Core autonomous research agent implementation.

Implements the ReAct (Reason + Act) loop with:
  - Three-layer memory integration (short-term, long-term vector DB, episodic)
  - Multi-source synthesis engine
  - Error handling with exponential-backoff retry and fallback chains
  - Circuit breaker protection on every tool call
"""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI

from agent.prompts import build_system_prompt
from agent.parser import parse_llm_response
from agent.tools import TOOL_REGISTRY
from agent.error_handler import retry_with_backoff
from agent.fallback_chains import execute_with_fallbacks
from agent.circuit_breaker import CircuitBreaker

from memory.context_manager import ContextManager
from memory.vector_store import store_memory, search_memory
from memory.episodic import log_episode

from synthesis.engine import synthesize_sources, triangulate_numbers
from synthesis.conflict_resolver import resolve_conflicts

load_dotenv()


REQUIRED_TOOLS = {
    "financial_data_api", "sec_filing_search", "earnings_transcript",
    "web_search", "peer_comparison", "calculation_engine",
}


class ResearchAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.max_iterations = 14

        # Short-term memory
        self._context = ContextManager()

        # Per-tool circuit breakers
        self._breakers: dict[str, CircuitBreaker] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_breaker(self, tool_name: str) -> CircuitBreaker:
        if tool_name not in self._breakers:
            self._breakers[tool_name] = CircuitBreaker(
                failure_threshold=3, recovery_timeout=30
            )
        return self._breakers[tool_name]

    @retry_with_backoff(retries=3, base_delay=1)
    def _call_tool_direct(self, tool_name: str, tool_input: str):
        """Execute a registered tool directly with retry protection."""
        return TOOL_REGISTRY[tool_name](tool_input)

    def _call_tool(self, tool_name: str, tool_input: str):
        """
        Execute a tool with the full protection stack:
        circuit breaker → direct call (retry inside) → fallback chain.
        """
        breaker = self._get_breaker(tool_name)
        result = breaker.call(self._call_tool_direct, tool_name, tool_input)

        # If circuit breaker returns an error dict, try fallback chain
        if isinstance(result, dict) and "error" in result:
            print(f"  [Fallback] Primary tool '{tool_name}' failed: {result['error']}")
            fallback = execute_with_fallbacks(tool_name, tool_input)
            if fallback.get("success"):
                print(f"  [Fallback] Recovered via {fallback['tool_used']}")
                return fallback["result"], True   # (result, used_fallback)
            return str(result), False

        return result, False   # (result, used_fallback)

    def _retrieve_relevant_memory(self, query: str) -> str:
        """Search long-term vector store for relevant past research."""
        try:
            results = search_memory(query, n_results=3)
            docs = results.get("documents", [[]])[0]
            if docs:
                return "Relevant prior research:\n" + "\n".join(docs[:3])
        except Exception:
            pass
        return ""

    def _store_tool_result(self, tool_name: str, tool_result: str, query: str) -> None:
        """Persist tool result in long-term vector store."""
        try:
            store_memory(
                str(tool_result)[:2000],
                metadata={"tool": tool_name, "query": query[:200]}
            )
        except Exception:
            pass

    def _synthesize_observations(self, observations: list[dict]) -> str:
        """Run multi-source synthesis over collected tool results."""
        if not observations:
            return ""
        ranked = synthesize_sources(observations)
        numeric_values = []
        for obs in observations:
            content = str(obs.get("content", ""))
            import re
            nums = [float(n) for n in re.findall(r"\b\d+\.?\d*\b", content)]
            numeric_values.extend(nums[:5])

        summary_lines = ["[Synthesis] Source ranking by reliability:"]
        for i, src in enumerate(ranked[:3], 1):
            summary_lines.append(f"  {i}. {src.get('source_type','?')}: {str(src.get('content',''))[:120]}")

        if numeric_values:
            tri = triangulate_numbers(numeric_values[:20])
            if tri:
                summary_lines.append(
                    f"[Triangulation] avg={tri['average']:.1f}  "
                    f"min={tri['minimum']:.1f}  max={tri['maximum']:.1f}  "
                    f"spread={tri['spread']:.1f}"
                )
        return "\n".join(summary_lines)

    # ------------------------------------------------------------------
    # Main ReAct reasoning loop
    # ------------------------------------------------------------------

    def run(self, query: str) -> str:
        start_time = time.time()

        # --- Short-term memory reset for this query ---
        self._context.clear()
        self._context.add(f"Query: {query}")

        # --- Check long-term memory for relevant prior context ---
        prior_context = self._retrieve_relevant_memory(query)
        if prior_context:
            print(f"\n[Memory] Retrieved relevant prior research context.")

        messages = [
            {
                "role": "system",
                "content": build_system_prompt(list(TOOL_REGISTRY.keys()))
            },
            {
                "role": "user",
                "content": (
                    (f"Context from prior research:\n{prior_context}\n\n" if prior_context else "")
                    + query
                )
            }
        ]

        called_tools: set[str] = set()
        observations: list[dict] = []   # for synthesis engine
        error_count = 0
        recovered_count = 0
        iteration = 0

        while iteration < self.max_iterations:
            print(f"\n--- Iteration {iteration + 1} ---")

            # --- LLM call ---
            response = self.client.chat.completions.create(
                max_tokens=6000,
                temperature=0.2,
                model="gpt-4o-mini",
                messages=messages
            )
            llm_output = response.choices[0].message.content

            print("\nLLM OUTPUT:")
            print(llm_output)

            parsed = parse_llm_response(llm_output)

            # ---- FINAL ANSWER ----
            if parsed["type"] == "final":
                missing_tools = REQUIRED_TOOLS - called_tools
                if not missing_tools:
                    # Run synthesis over all collected observations
                    synth_summary = self._synthesize_observations(observations)
                    if synth_summary:
                        print(f"\n{synth_summary}")

                    final_answer = parsed["content"]

                    # Store final answer in long-term memory
                    self._store_tool_result("final_report", final_answer, query)

                    # Log this episode to episodic memory
                    elapsed = round(time.time() - start_time, 1)
                    log_episode(
                        query=query,
                        outcome="success",
                        strategy=(
                            f"Tools used: {', '.join(sorted(called_tools))}. "
                            f"Elapsed: {elapsed}s. "
                            f"Errors: {error_count}, Recovered: {recovered_count}."
                        )
                    )

                    return final_answer

                missing_list = ", ".join(sorted(missing_tools))
                messages.append({"role": "assistant", "content": llm_output})
                messages.append({
                    "role": "user",
                    "content": (
                        f"ERROR: You tried to write your Final Answer before calling all "
                        f"required tools. You have NOT yet called: {missing_list}. "
                        "You MUST call each of those tools first. "
                        "Call the next required tool now using Action / Action Input format."
                    )
                })

            # ---- TOOL EXECUTION ----
            elif parsed["type"] == "tool":
                tool_name = parsed["tool"]
                tool_input = parsed["input"]

                if tool_name not in TOOL_REGISTRY:
                    return f"Tool '{tool_name}' not found."

                print(f"\nRunning Tool: {tool_name}")
                print(f"Tool Input: {tool_input}")

                tool_result, used_fallback = self._call_tool(tool_name, tool_input)

                if used_fallback:
                    error_count += 1
                    recovered_count += 1

                print("\nTOOL RESULT:")
                print(tool_result)

                called_tools.add(tool_name)

                # Determine source type for synthesis
                source_type_map = {
                    "sec_filing_search": "sec_filing",
                    "sec_search":        "sec_filing",
                    "financial_data_api":"financial_api",
                    "financial_metrics": "financial_api",
                    "web_search":        "web_search",
                    "news_sentiment":    "major_news",
                    "earnings_transcript":"company_report",
                    "peer_comparison":   "financial_api",
                    "calculation_engine":"financial_api",
                    "company_profile":   "company_report",
                    "fact_checker":      "major_news",
                }
                observations.append({
                    "source_type": source_type_map.get(tool_name, "web_search"),
                    "content": str(tool_result)[:500],
                    "tool": tool_name,
                })

                # Store result in long-term memory
                self._store_tool_result(tool_name, str(tool_result), query)

                # Update short-term context
                self._context.add(f"[{tool_name}]: {str(tool_result)[:200]}")

                missing_tools = REQUIRED_TOOLS - called_tools

                messages.append({"role": "assistant", "content": llm_output})
                messages.append({
                    "role": "user",
                    "content": f"Observation: {tool_result}"
                })

                if not missing_tools:
                    messages.append({
                        "role": "user",
                        "content": (
                            "You have now called all required tools and gathered "
                            "sufficient data. DO NOT call any more tools. "
                            "Write your complete Final Answer NOW — the full "
                            "4000-5000 word analytical report using all the data "
                            "from the Observations above. "
                            "Start your response with exactly: Final Answer:"
                        )
                    })
                elif iteration >= 10:
                    missing_list = ", ".join(sorted(missing_tools))
                    messages.append({
                        "role": "user",
                        "content": (
                            f"NOTE: You have not yet called {missing_list}. "
                            "However you have reached the iteration limit. "
                            "Write your complete Final Answer NOW using all data "
                            "collected so far. Start with exactly: Final Answer:"
                        )
                    })
                elif iteration >= 6:
                    missing_list = ", ".join(sorted(missing_tools))
                    messages.append({
                        "role": "user",
                        "content": (
                            f"You still need to call these required tools before writing "
                            f"your report: {missing_list}. Call the next one now."
                        )
                    })

            # ---- PARSE FAILURE ----
            else:
                log_episode(
                    query=query,
                    outcome="parse_error",
                    strategy=f"Iteration {iteration}: parser failed."
                )
                return f"Parser Error:\n{parsed['content']}"

            iteration += 1

        # Max iterations reached without final answer
        log_episode(
            query=query,
            outcome="max_iterations",
            strategy=f"Stopped at {self.max_iterations} iterations. Tools called: {sorted(called_tools)}."
        )
        return "Agent stopped: max iterations reached."
