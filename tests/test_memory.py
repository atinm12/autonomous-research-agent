from memory.vector_store import (
    store_memory,
    search_memory
)

from memory.context_manager import ContextManager

from memory.episodic import log_episode


# -------------------------
# VECTOR MEMORY TEST
# -------------------------

print("\n--- VECTOR STORE TEST ---")

store_memory(
    "Microsoft Azure is a major cloud computing platform.",
    metadata={"company": "Microsoft"}
)

results = search_memory("cloud computing")

print(results)


# -------------------------
# CONTEXT MANAGER TEST
# -------------------------

print("\n--- CONTEXT MANAGER TEST ---")

context = ContextManager()

context.add("User asked about Microsoft.")
context.add("Retrieved financial metrics.")

print(context.get_context())


# -------------------------
# EPISODIC MEMORY TEST
# -------------------------

print("\n--- EPISODIC MEMORY TEST ---")

result = log_episode(
    query="Microsoft company profile",
    outcome="Success",
    strategy="Used financial metrics and SEC filings."
)

print(result)