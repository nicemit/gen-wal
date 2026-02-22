import time
import requests
import random
from src.interfaces import TextProvider

class PollinationsTextProvider(TextProvider):
    """
    Pollinations Text Provider Configuration:
    - Endpoint: https://gen.pollinations.ai/v1/chat/completions
    - Models: Expected to be explicitly passed (default 'gpt-5')
    - Retries: Up to 3 attempts with exponential backoff for transient failures
    """
    def __init__(self, model: str = "gpt-5", api_key: str = None):
        self.model = model or "gpt-5"
        self.api_key = api_key

    def generate_text(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        url = "https://gen.pollinations.ai/v1/chat/completions"
        
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
             headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
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
                print(f"Pollinations Text Gen Error (Attempt {attempt + 1}/{max_retries}): {msg}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)
