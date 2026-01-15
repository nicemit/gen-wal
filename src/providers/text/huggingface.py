import requests
from src.interfaces import TextProvider

class HuggingFaceTextProvider(TextProvider):
    def __init__(self, model: str = "Qwen/Qwen2.5-7B-Instruct", api_key: str = None):
        self.model = model
        self.api_key = api_key

    def generate_text(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        if not self.api_key:
             return "Visual Description: Abstract geometric shapes."

        url = f"https://api-inference.huggingface.co/models/{self.model}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Simple Instruct Format
        full_prompt = f"[INST] {system_prompt}\n\n{prompt} [/INST]"
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 100,
                "return_full_text": False,
                "temperature": 0.7
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and 'generated_text' in data[0]:
                return data[0]['generated_text'].strip()
            
            return "Abstract Nebula."
            
        except Exception as e:
            print(f"HF Text Gen Error: {e}")
            return "Abstract Nebula."
