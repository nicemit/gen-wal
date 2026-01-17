import requests
import random
from src.interfaces import QuoteProvider

class PollinationsQuoteProvider(QuoteProvider):
    def __init__(self, model: str = "openai", api_key: str = None, prompt_template: str = None, request_params: dict = None):
        self.model = model
        self.api_key = api_key
        self.prompt_template = prompt_template or """
        You are a motivational coach. Based on the following profile, generate a single, short, punchy, direct motivational quote (max 20 words).
        Do not explain. Do not use quotes around the text.
        
        PROFILE:
        {profile_content}
        """

    def _call_pollinations(self, prompt: str) -> str:
        if self.api_key:
            url = "https://gen.pollinations.ai/v1/chat/completions"
        else:
             url = "https://text.pollinations.ai/openai/v1/chat/completions"

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

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        except Exception as e:
            msg = str(e)
            if 'response' in locals() and hasattr(response, 'text'):
                msg += f" | Body: {response.text}"
            print(f"Pollinations API Error: {msg}")
            raise e

    def get_quote(self, profile_content: str) -> str:
        prompt = self.prompt_template.format(profile_content=profile_content)
        try:
            return self._call_pollinations(prompt)
        except:
             return "Discipline equals freedom."
