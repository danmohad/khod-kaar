"""
File: Memory.py
Author: Danyal Mohaddes
Description: This file contains the Memory class.
"""

import os
import json
import tiktoken

class Memory():
    """Singleton class containing the full conversation history of LLM inputs, LLM outputs and code execution outputs in the `memories` attribute."""
    
    def __init__(self, model_, output_dir_):
        """Initialization method for Memory"""
        
        self._model = model_
        
        # Creation of output directory, if necessary
        os.makedirs(output_dir_, exist_ok=True)
        
        long_term_memory_ = os.path.join(output_dir_, "long_term_memory.json")
        self._long_term_memory = long_term_memory_
        
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

    def short_to_long_term(self) -> None:
        """Save memory (short term) to disk (long term)."""

        # Overwrites any existing long-term memory file on disk
        with open(self._long_term_memory, 'w') as fout:
            json.dump(self.memories, fout)

    def long_to_short_term(self) -> None:
        # TODO implement long_to_short_term to read from file in case of API connection failure
        pass
