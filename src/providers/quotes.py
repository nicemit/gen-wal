import json
import csv
import yaml
import requests
import random
from typing import List, Dict, Any
from src.interfaces import QuoteProvider

class ZenQuotesProvider(QuoteProvider):
    def get_quote(self, profile_content: str) -> str:
        try:
            response = requests.get("https://zenquotes.io/api/random")
            data = response.json()
            return f"{data[0]['q']} - {data[0]['a']}"
        except Exception as e:
            return "Discipline is doing what needs to be done, even if you don't want to do it."

class CsvQuoteProvider(QuoteProvider):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_quote(self, profile_content: str) -> str:
        try:
            with open(self.file_path, 'r') as f:
                reader = csv.reader(f)
                quotes = list(reader)
                if not quotes:
                    return "No quotes found in CSV."
                # Assume quote is in the first column
                return random.choice(quotes)[0]
        except Exception as e:
            return f"Error reading CSV: {e}"

class YamlQuoteProvider(QuoteProvider):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_quote(self, profile_content: str) -> str:
        try:
            with open(self.file_path, 'r') as f:
                data = yaml.safe_load(f)
                if isinstance(data, list):
                    # List of strings or objects?
                    item = random.choice(data)
                    if isinstance(item, str):
                        return item
                    elif isinstance(item, dict) and 'text' in item:
                        return item['text']
                    else:
                         return str(item)
                return "Invalid YAML format. Expected a list."
        except Exception as e:
             return f"Error reading YAML: {e}"

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
        
        # Adjust endpoint for standard OpenAI compatible API
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        # Merge extra params (users can override stream, max_tokens, temperature etc)
        payload.update(self.request_params)

        try:
            # Handle local ollama vs generic OpenAI compatible
            # Try OpenAI format first
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=600)
                
                if response.status_code == 404 and "localhost" in self.base_url:
                     # Fallback to Ollama Native API
                     # print("Fallback to Ollama Native API")
                     url = f"{self.base_url.replace('/v1', '')}/api/chat"
                     # Payload is same for Ollama /api/chat
                     response = requests.post(url, headers=headers, json=payload, timeout=600)
                     response.raise_for_status()
                     data = response.json()
                     # Ollama native response format: { "message": { "content": "..." } }
                     return data['message']['content'].strip()
                
                response.raise_for_status()
                data = response.json()
                return data['choices'][0]['message']['content'].strip()

            except Exception as e:
                # If fallback also failed or some other error, try to get more info
                error_msg = str(e)
                if 'response' in locals() and hasattr(response, 'text'):
                     error_msg += f" | Body: {response.text}"
                print(f"LLM Error Details: {error_msg}")
                raise e
        
        except Exception as e:
            # Fallback for raw completion if chat fails (older APIs)
            return f"Stay Hard. (LLM Error: {e})"

class PollinationsQuoteProvider(QuoteProvider):
    def __init__(self, model: str = "openai", api_key: str = None, prompt_template: str = None, request_params: dict = None):
        self.model = model
        self.api_key = api_key
        # Default prompt template if none provided
        self.prompt_template = prompt_template or """
        You are a motivational coach. Based on the following profile, generate a single, short, punchy, direct motivational quote (max 20 words).
        Do not explain. Do not use quotes around the text.
        
        PROFILE:
        {profile_content}
        """

    def _call_pollinations(self, prompt: str) -> str:
        # Use POST to avoid URL length limits with large profiles
        url = "https://text.pollinations.ai" # No trailing slash
        
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
             headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."}, # System instruction could go here but simple is fine
                {"role": "user", "content": prompt}
            ],
            "model": self.model,
            "seed": random.randint(0, 1000)
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            # Pollinations POST returns the message object directly: {"role": "assistant", "content": "..."}
            try:
                data = response.json()
                if isinstance(data, dict) and 'content' in data:
                    return data['content'].strip()
                # Fallback if structure is different (e.g. OpenAI format)
                if 'choices' in data and len(data['choices']) > 0:
                    return data['choices'][0]['message']['content'].strip()
            except ValueError:
                pass
            
            return response.text.strip()
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
