import time
import requests
import random
from src.interfaces import QuoteProvider

class PollinationsQuoteProvider(QuoteProvider):
    """
    Pollinations Quote Provider Configuration:
    - Endpoint: https://gen.pollinations.ai/v1/chat/completions
    - Models: Expected to be explicitly passed (default 'gpt-5')
    - Retries: Up to 3 attempts with exponential backoff for transient failures
    """
    def __init__(self, model: str = "gpt-5", api_key: str = None, prompt_template: str = None, request_params: dict = None):
        self.model = model or "gpt-5"
        self.api_key = api_key
        self.prompt_template = prompt_template or """
        You are a motivational coach. Based on the following profile, generate a single, short, punchy, direct motivational quote (max 20 words).
        Do not explain. Do not use quotes around the text.
        
        PROFILE:
        {profile_content}
        """

    def _call_pollinations(self, prompt: str) -> str:
        url = "https://gen.pollinations.ai/v1/chat/completions"

        headers = {"Content-Type": "application/json"}
        if self.api_key:
             headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "model": self.model,
            "stream": False,
            "seed": random.randint(0, 1000000)
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=60)
                response.raise_for_status()
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            except Exception as e:
                msg = str(e)
                if 'response' in locals() and hasattr(response, 'text'):
                    msg += f" | Body: {response.text}"
                elif hasattr(e, 'response') and e.response:
                    msg += f" | Body: {e.response.text}"
                print(f"Pollinations API Error (Attempt {attempt + 1}/{max_retries}): {msg}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)

    def get_quote(self, profile_content: str) -> str:
        prompt = self.prompt_template.format(profile_content=profile_content)
        try:
            return self._call_pollinations(prompt)
        except:
             return "Discipline equals freedom."
