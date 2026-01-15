import requests
from src.interfaces import QuoteProvider

class LLMQuoteProvider(QuoteProvider):
    def __init__(self, base_url: str, api_key: str, model: str, prompt_template: str = None, request_params: dict = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.model = model
        self.request_params = request_params or {}
        self.prompt_template = prompt_template or """
        You are a motivational coach. Based on the following profile, generate a single, short, punchy, direct motivational quote (max 20 words).
        Do not explain. Do not use quotes around the text.
        
        PROFILE:
        {profile_content}
        """

    def get_quote(self, profile_content: str) -> str:
        prompt = self.prompt_template.format(profile_content=profile_content)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        payload.update(self.request_params)

        try:
            try:
                # OpenAI format
                response = requests.post(url, headers=headers, json=payload, timeout=600)
                
                if response.status_code == 404 and "localhost" in self.base_url:
                     # Fallback to Ollama Native API
                     url = f"{self.base_url.replace('/v1', '')}/api/chat"
                     response = requests.post(url, headers=headers, json=payload, timeout=600)
                     response.raise_for_status()
                     data = response.json()
                     return data['message']['content'].strip()
                
                response.raise_for_status()
                data = response.json()
                return data['choices'][0]['message']['content'].strip()

            except Exception as e:
                error_msg = str(e)
                if 'response' in locals() and hasattr(response, 'text'):
                     error_msg += f" | Body: {response.text}"
                print(f"LLM Error Details: {error_msg}")
                raise e
        
        except Exception as e:
            return f"Stay Hard. (LLM Error: {e})"
