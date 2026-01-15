import requests
from src.interfaces import QuoteProvider

class HuggingFaceQuoteProvider(QuoteProvider):
    def __init__(self, model: str = "Qwen/Qwen2.5-7B-Instruct", api_key: str = None, prompt_template: str = None):
        self.model = model
        self.api_key = api_key
        self.prompt_template = prompt_template or """
        [INST] You are a motivational coach. Based on the following profile, generate a single, short, punchy, direct motivational quote (max 20 words).
        Do not explain. Do not use quotes around the text.
        
        PROFILE:
        {profile_content}
        [/INST]
        """

    def get_quote(self, profile_content: str) -> str:
        if not self.api_key:
             return "Error: Hugging Face API Token required."

        url = f"https://api-inference.huggingface.co/models/{self.model}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        prompt = self.prompt_template.format(profile_content=profile_content)
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 50,
                "return_full_text": False,
                "temperature": 0.7
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and 'generated_text' in data[0]:
                return data[0]['generated_text'].strip().replace('"', '')
            elif isinstance(data, dict) and 'error' in data:
                 print(f"HF Error: {data['error']}")
                 return "Resilience is key."
            return str(data)
            
        except Exception as e:
            print(f"Hugging Face API Error: {e}")
            return "Discipline equals freedom."
