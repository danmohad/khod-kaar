class Memory():
    """Singleton class containing the full conversation history of LLM inputs, LLM outputs and code execution outputs in the `memories` attribute."""
    
    def __init__(self):
        """Initialization method for Memory"""
        self.memories = []

    def memorize(self, memory_: str, role_: str) -> None:
        """Add event to memory, keeping track of `role` and `content` attributes."""

        self.memories += [{'role': role_, 'content': memory_}]

    def forget_memory(self) -> None:
        """Clear memory."""

        self.memories = []

