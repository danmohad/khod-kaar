import tiktoken

class Memory():
    """Singleton class containing the full conversation history of LLM inputs, LLM outputs and code execution outputs in the `memories` attribute."""
    
    def __init__(self):
        """Initialization method for Memory"""
        self.memories = []

    def memorize(self, memory_: str, role_: str) -> None:
        """Add event to memory, keeping track of `role` and `content` attributes."""

        self.memories += [{'role': role_, 'content': memory_}]
    
    def show_memory(self) -> None:
        """Output current state of memory to console."""

        print(self.memories)

    def forget_memory(self) -> None:
        """Clear memory."""

        self.memories = []

    def token_count(self, model_: str) -> int:
        """Get current token count."""

        encoding = tiktoken.encoding_for_model(model_)
        string_ = ""
        for m in self.memories:
            string_ += m['content'] + "\n" 
        num_tokens = len(encoding.encode(string_))
        return num_tokens
