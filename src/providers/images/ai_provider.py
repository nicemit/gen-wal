import os
import importlib
from src.providers.base import ImageProvider, register_provider, get_provider
from src.ai_prompt import build_prompt
from PIL import Image

class AIImageProvider(ImageProvider):
    def __init__(self, config):
        self.config = config

    @classmethod
    def name(cls):
        return "ai"

    def generate(self, seed: int, env: dict, theme_hints: dict, width: int, height: int):
        # 1. Build prompt
        quote = env.get("quote", "Silent reflection.")
        palette = env.get("palette", {})
        prompt = build_prompt(quote, palette, theme_hints)

        # 2. Determine backend
        ai_config = self.config.get("ai", {}) if "ai" in self.config else self.config
        backend = ai_config.get("backend", "openai")
        
        # Check cache first
        from src.config import XDG_CACHE_HOME
        ai_cache_dir = os.path.join(XDG_CACHE_HOME, 'genwal', 'ai')
        os.makedirs(ai_cache_dir, exist_ok=True)
        cache_path = os.path.join(ai_cache_dir, f"{seed}_{backend}.jpg")
        
        if os.path.exists(cache_path):
            print(f"  ➜ Loading cached AI image from {cache_path}")
            try:
                return Image.open(cache_path)
            except Exception as e:
                print(f"  ➜ Failed to load cached image: {e}")
        
        try:
            # 3. Import backend module dynamically
            try:
                mod = importlib.import_module(f"src.providers.images.ai.{backend}")
            except ImportError as e:
                raise ValueError(f"Failed to load AI backend '{backend}': {e}")
                
            if not hasattr(mod, "generate_image"):
                raise ValueError(f"AI backend '{backend}' is missing generate_image function.")

            # 4. Call backend
            img = mod.generate_image(prompt, seed, ai_config, width, height)
            
            # Save to cache
            img.convert("RGB").save(cache_path, "JPEG", quality=95)
            return img
            
        except Exception as e:
            print(f"⚠️ AI Image Generation Failed: {e}. Falling back to 'mesh' provider.")
            fallback_prov = get_provider('image', 'mesh', self.config)
            return fallback_prov.generate(seed, env, theme_hints, width, height)

# Explictly register with origin "ai"
register_provider("image", AIImageProvider, origin="ai")
