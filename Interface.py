"""
File: Interface.py
Author: Danyal Mohaddes
Description: This file contains classes for interfacing LLMs.
"""

import openai
import os

class Interface:
    """Singleton class for interacting with LLM via OpenAI's API"""

    def __init__(self, temperature_ = 1.0, model_ = "gpt-4") -> None:
        """Initialization method for Interface."""

        self.last_output = []

        # OpenAI and LLM settings
        self._model = "gpt-4" if model_ is None else model_
        self._temperature = 1.0 if temperature_ is None else temperature_
        openai.organization = os.getenv("OPENAI_ORG_KEY")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def send_prompt(self, memories_):
        """Send a prompt to the LLM, store the object in `self.last_output` and return the result as text."""
        
        self.last_output = openai.ChatCompletion.create(
            model=self._model,
            messages=memories_,
            temperature=self._temperature
        )

        return self._llm_output_to_text(self.last_output)
    
    @staticmethod
    def _llm_output_to_text(output_) -> str:
        """Parse the object returned by the LLM's API to get the LLM's output text"""
        
        return output_["choices"][0]["message"]["content"]

