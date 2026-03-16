import importlib
from src.providers.base import QuoteProvider, register_provider, get_provider

class AIQuoteProvider(QuoteProvider):
    def __init__(self, config):
        self.config = config

    @classmethod
    def name(cls):
        return "ai"

    def generate(self, seed: int, env: dict, theme_hints: dict):
        try:
            # 1. Build prompt
            style_desc = theme_hints.get("quote_style", "abstract")
            prompt = f"Generate a short motivational quote. Style: {style_desc}. Tone: concise. Length: one sentence."

            # 2. Determine backend from the global AI config block
            # (We assume the config passed here is the main config so we extract ["ai"])
            ai_config = self.config.get("ai", {})
            backend = ai_config.get("backend", "openai")
            
            # 3. Import backend module dynamically from the images/ai directory
            try:
                mod = importlib.import_module(f"src.providers.images.ai.{backend}")
            except ImportError as e:
                raise ValueError(f"Failed to load AI text backend '{backend}': {e}")
                
            if not hasattr(mod, "generate_text"):
                raise ValueError(f"AI backend '{backend}' is missing generate_text function.")
                
            return mod.generate_text(prompt, seed, ai_config)

        except Exception as e:
            print(f"⚠️ AI Quote Generation Failed: {e}. Falling back to CSV provider.")
            fallback_prov = get_provider('quote', 'csv', self.config)
            return fallback_prov.generate(seed, env, theme_hints)

# Explicitly register with origin "ai"
register_provider("quote", AIQuoteProvider, origin="ai")
