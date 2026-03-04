import urllib.request
import urllib.parse
from src.providers.base import QuoteProvider, register_provider

class PollinationsTextProvider(QuoteProvider):
    def __init__(self, config):
        self.config = config
        
    @classmethod
    def name(cls):
        return "pollinations:text"
        
    def generate(self, seed: int, env: dict, theme_hints: dict) -> str:
        style = theme_hints.get('quote_style', 'concise philosophical')
        prompt = f"Write a single, short, profound quote about {style}. Maximum 15 words. No quotes marks."
        
        # Pollinations text generation endpoint
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}?seed={seed}"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Gen-Wal/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8').strip().strip('"')
        except Exception as e:
            print(f"Warning: Pollinations text failed ({e}), falling back...")
            return "The impediment to action advances action."

register_provider('quote', PollinationsTextProvider)
