import requests
import random
from src.interfaces import TextProvider

class PollinationsTextProvider(TextProvider):
    def __init__(self, model: str = "openai", api_key: str = None):
        self.model = model
        self.api_key = api_key

    def generate_text(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        if self.api_key:
            url = "https://gen.pollinations.ai/v1/chat/completions"
        else:
            url = "https://text.pollinations.ai/openai/v1/chat/completions"
        
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
            # If using free tier, model might be ignored or need specific value, but passing self.model is safe
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
            print(f"Pollinations Text Gen Error: {msg}")
            raise e
