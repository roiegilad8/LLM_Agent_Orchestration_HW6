import os
from openai import OpenAI

class OpenAIClient:
    """
    A simple client for the OpenAI API.
    """

    def __init__(self, api_key: str = None):
        """
        Initializes the OpenAI client.

        Args:
            api_key: The OpenAI API key. If not provided, it will be read from the OPENAI_API_KEY environment variable.
        """
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=api_key)

    def query(self, prompt: str) -> str:
        """
        Sends a query to the OpenAI API.

        Args:
            prompt: The prompt to send to the API.

        Returns:
            The response from the API.
        """
        try:
            response = self.client.completions.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"An error occurred: {e}"
