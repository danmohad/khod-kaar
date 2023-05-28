import tiktoken

class Memory():
    """Singleton class containing the full conversation history of LLM inputs, LLM outputs and code execution outputs in the `memories` attribute."""
    
    def __init__(self, model_ = "gpt-4"):
        """Initialization method for Memory"""
        self._model = "gpt-4" if model_ is None else model_
        self.memories = []
        self.total_token_count = 0

    def memorize(self, memory_: str, role_: str) -> None:
        """Add event to memory, keeping track of `role` and `content` attributes."""

        self.memories += [{'role': role_, 'content': memory_}]
        self._update_token_count()

    def forget_memory(self) -> None:
        """Clear memory."""

        self.memories = []

    def _update_token_count(self) -> None:
        """Get current token count."""

        encoding = tiktoken.encoding_for_model(self._model)
        string_ = ""
        for m in self.memories:
            string_ += m['content'] + "\n" 
        self.total_token_count = len(encoding.encode(string_))
