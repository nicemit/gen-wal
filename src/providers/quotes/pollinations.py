import requests
from src.providers.base import QuoteProvider, register_provider
import random
import os

class PollinationsTextProvider(QuoteProvider):
    def __init__(self, config):
        self.config = config
        
    @classmethod
    def name(cls):
        return "pollinations:text"
        
    def generate(self, seed: int, env: dict, theme_hints: dict) -> str:
        rng = random.Random(seed)
        style = theme_hints.get('quote_style', 'concise philosophical')
        
        # Read from config with fallbacks
        pollinations_cfg = self.config.get("text", {}) if isinstance(self.config, dict) else {}
        if not pollinations_cfg and hasattr(self, 'config') and isinstance(self.config, dict):
            # Safe boundary
            pollinations_cfg = self.config
            
        api_key = pollinations_cfg.get("api_key", "sk_DEmGllK96evE5ipYzFxpDAvkofJGbQaZ")
        model_cfg = pollinations_cfg.get("model", ["claude-airforce", "openai-seraphyn"])
        if isinstance(model_cfg, list):
            selected_model = rng.choice(model_cfg)
        else:
            selected_model = model_cfg
        
        # Load content from full config (Theme body description)
        from src.config import load_config
        full_cfg = load_config()
        profile_content = full_cfg.get('description', '')
        quote_prompt_template = full_cfg.get('quote_prompt_template', '')

        # Highly detailed prompt profile template from config fallback
        template = quote_prompt_template or full_cfg.get("prompts", {}).get("quote", (
            f"You are a profound philosopher. Generate a single deep quote about '{style}' philosophy. "
            f"Maximum 15 words. Just the quote text."
        ))
        
        prompt = template
        if "{profile_content}" in template and profile_content:
            prompt = template.format(profile_content=profile_content)
        elif profile_content:
            # Fallback append
            prompt = f"{template}\n\nPROFILE:\n{profile_content}"
            
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        url = "https://gen.pollinations.ai/v1/chat/completions"
        
        payload = {
            "model": selected_model,
            "messages": [{"role": "user", "content": prompt}],
            "seed": seed % 2147483647  # Safely within INT32 bounds for vertex-ai
        }
        
        res = requests.post(url, headers=headers, json=payload, timeout=20)
        if res.status_code == 200:
            data = res.json()
            content = data["choices"][0]["message"]["content"]
            if content:
                return content.strip().strip('"')
                
        raise Exception(f"Failed to generate quote via {selected_model} on Pollinations (Status {res.status_code})")

register_provider('quote', PollinationsTextProvider)
