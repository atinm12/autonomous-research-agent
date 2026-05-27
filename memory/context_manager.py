MAX_CONTEXT_ITEMS = 10


# -----------------------------------
# CONTEXT SUMMARIZATION
# -----------------------------------

def summarize_context(context):

    words = context.split()

    # If context is already small,
    # return it unchanged
    if len(words) < 300:

        return context

    # Keep:
    # - beginning
    # - ending
    # Remove:
    # - middle overflow

    summary = (

        " ".join(words[:150])

        + "\n...\n"

        + " ".join(words[-100:])
    )

    return summary


# -----------------------------------
# CONTEXT MANAGER
# -----------------------------------

class ContextManager:

    def __init__(self):

        self.memory = []

    def add(self, item):

        self.memory.append(item)

        # Remove oldest items if memory grows too large
        if len(self.memory) > MAX_CONTEXT_ITEMS:

            self.memory.pop(0)

    def get_context(self):

        full_context = "\n".join(
            self.memory
        )

        summarized = summarize_context(
            full_context
        )

        return summarized

    def clear(self):

        self.memory = []