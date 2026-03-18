import requests
from io import BytesIO
from PIL import Image
from src.providers.base import ImageProvider, register_provider
import random

class PollinationsImageProvider(ImageProvider):
    def __init__(self, config):
        self.config = config
        
    @classmethod
    def name(cls):
        return "pollinations"
        
    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        rng = random.Random(seed)
        
        # Read from config with fallbacks
        pollinations_cfg = self.config.get("image", {}) if isinstance(self.config, dict) else {}
        if not pollinations_cfg and hasattr(self, 'config') and isinstance(self.config, dict):
            pollinations_cfg = self.config
            
        api_key = pollinations_cfg.get("api_key", "sk_DEmGllK96evE5ipYzFxpDAvkofGjbQaZ")
        
        # Support list of models or a single model string
        model_cfg = pollinations_cfg.get("model", ["flux", "gptimage"])
        if isinstance(model_cfg, list):
            selected_model = rng.choice(model_cfg)
        else:
            selected_model = model_cfg
            
        nologo = pollinations_cfg.get("nologo", True)
        
        # Load profile_content from full config
        from src.config import load_config
        full_cfg = load_config()
        profile_path = full_cfg.get('profile_path', 'profiles/examples/stoic.md')
        
        if isinstance(profile_path, list):
            profile_path = rng.choice(profile_path)
            
        profile_content = ""
        try:
            import os
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as f:
                    profile_content = f.read()
                    if profile_content.startswith("---"):
                        parts = profile_content.split("---", 2)
                        if len(parts) >= 3:
                            profile_content = parts[2].strip()
        except Exception as e:
            print(f"Warning: Failed to load profile for pollinations image: {e}")

        quote = env.get("quote", "abstract concept")
        palette = env.get("palette", {})
        
        # Highly detailed prompt profile template from config
        template = full_cfg.get("prompts", {}).get("image_description", "")
        
        if not template:
            # Fallback that actually incorporates profile and quote descriptively
            template = (
                "Create a beautiful, abstract background image. "
                "The scene should interpret the vibe of this profile conceptually: '{profile_content}'. "
                "Tone inspired by: '{quote}'. "
                "Creative, modern composition. Do NOT include any text or watermarks in the image."
            )
            
        if template:
            try:
                base_prompt = template.format(quote=quote, profile_content=profile_content)
            except Exception:
                base_prompt = f"{template}\n\nQUOTE: {quote}\n\nPROFILE:\n{profile_content}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        url = "https://gen.pollinations.ai/v1/images/generations"
        
        payload = {
            "model": selected_model,
            "prompt": base_prompt,
            "width": width,
            "height": height,
            "nologo": nologo,
            "seed": seed % 2147483647
        }
        
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=45)
            if res.status_code == 200:
                import base64
                data = res.json()["data"][0]
                b64_img = data.get("b64_json")
                if b64_img:
                    return Image.open(BytesIO(base64.b64decode(b64_img))).convert('RGB')
                raise Exception("No image data returned")
            else:
                print(f"Warning: Pollinations image POST returned {res.status_code}: {res.text[:100]}")
                raise Exception(f"API Error {res.status_code}")
        except Exception as e:
            print(f"Warning: Pollinations image failed ({e}), falling back to gradient...")
            from src.providers.images.gradient import GradientImageProvider
            fallback = GradientImageProvider({})
            return fallback.generate(seed, env, theme_hints, width, height)

register_provider('image', PollinationsImageProvider)
