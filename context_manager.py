MAX_CONTEXT_ITEMS = 10


class ContextManager:

    def __init__(self):

        self.memory = []

    def add(self, item):

        self.memory.append(item)

        # Summarize/remove old context
        if len(self.memory) > MAX_CONTEXT_ITEMS:

            self.memory.pop(0)

    def get_context(self):

        return "\n".join(self.memory)

    def clear(self):

        self.memory = []