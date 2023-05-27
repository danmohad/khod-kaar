import openai
import os

class Interface:
    """Singleton class for interacting with LLM via OpenAI's API"""

    def __init__(self, temperature_ = 1.0) -> None:
        """Initialization method for Interface."""

        self.last_output = []

        # OpenAI and LLM settings
        self.model = "gpt-4"
        self._temperature = temperature_
        self.tokens_used = 0
        openai.organization = os.getenv("OPENAI_ORG_KEY")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def send_prompt(self, memories_):
        """Send a prompt to the LLM, store the object in `self.last_output` and return the result as text."""
        
        self.last_output = openai.ChatCompletion.create(
            model=self.model,
            messages=memories_,
            temperature=self._temperature
        ) # TODO dump "memories" to memory and read from file in case of API connection failure

        self.tokens_used = self._get_token_count(self.last_output)

        return self._llm_output_to_text(self.last_output)
    
    @staticmethod
    def _llm_output_to_text(output_) -> str:
        """Parse the object returned by the LLM's API to get the LLM's output text"""
        
        return output_["choices"][0]["message"]["content"]

    @staticmethod
    def _get_token_count(output_) -> int:
        """Parse the object returned by the LLM's API to get the LLM's total token usage"""

        return output_["usage"]["total_tokens"]
