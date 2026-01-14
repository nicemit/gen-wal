import requests
from src.interfaces import TextProvider

class LLMTextProvider(TextProvider):
    def __init__(self, base_url: str, api_key: str, model: str, request_params: dict = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.model = model
        self.request_params = request_params or {}

    def generate_text(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        payload.update(self.request_params)

        try:
            # Handle local ollama vs generic OpenAI compatible
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=120)
                
                # Check for 404 on localhost -> Ollama Native fallback
                if response.status_code == 404 and "localhost" in self.base_url:
                     fallback_url = f"{self.base_url.replace('/v1', '')}/api/chat"
                     response = requests.post(fallback_url, headers=headers, json=payload, timeout=120)
                     response.raise_for_status()
                     data = response.json()
                     return data['message']['content'].strip()
                
                response.raise_for_status()
                data = response.json()
                return data['choices'][0]['message']['content'].strip()

            except Exception as e:
                # If fallback also failed or some other error, log it
                error_msg = str(e)
                if 'response' in locals() and hasattr(response, 'text'):
                     error_msg += f" | Body: {response.text}"
                print(f"LLM Text Gen Error: {error_msg}")
                raise e
        
        except Exception as e:
            raise e

class PollinationsTextProvider(TextProvider):
    def __init__(self, model: str = "openai", api_key: str = None):
        self.model = model
        self.api_key = api_key

    def generate_text(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        import urllib.parse
        safe_prompt = urllib.parse.quote(prompt)
        url = f"https://gen.pollinations.ai/text/{safe_prompt}"
        
        headers = {}
        if self.api_key:
             headers["Authorization"] = f"Bearer {self.api_key}"

        params = {
            "model": self.model,
            "seed": 42,
            "system": system_prompt,
            "json": "true" 
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=60)
            response.raise_for_status()
            return response.text.strip()
            
        except Exception as e:
            print(f"Pollinations Text Gen Error: {e}")
            raise e
