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
        
        # Load profile_content from full config
        from src.config import load_config
        full_cfg = load_config()
        profile_path = full_cfg.get('profile_path', 'profiles/examples/stoic.md')
        
        if isinstance(profile_path, list):
            profile_path = rng.choice(profile_path)
            
        profile_content = ""
        quote_prompt_template = ""
        try:
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as f:
                    content_raw = f.read()
                    if content_raw.startswith("---"):
                        parts = content_raw.split("---", 2)
                        if len(parts) >= 3:
                            yaml_text = parts[1].strip()
                            profile_content = parts[2].strip()
                            # Basic string parsing for template since full yaml may not be imported
                            for line in yaml_text.split("\n"):
                                if "quote_prompt_template:" in line:
                                    quote_prompt_template = line.split("quote_prompt_template:", 1)[1].strip().strip('"')
                    else:
                        profile_content = content_raw
        except Exception as e:
            print(f"Warning: Failed to load profile for pollinations text: {e}")

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
