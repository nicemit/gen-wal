from .openai_compatible import generate_image as compat_generate_image
from .openai_compatible import generate_text as compat_generate_text

def generate_image(prompt: str, seed: int, config: dict, width: int, height: int):
    # Ensure config points to OpenAI's official API if not set
    cfg = config.copy()
    cfg.setdefault("base_url", "https://api.openai.com/v1")
    cfg.setdefault("model", "dall-e-3")
    
    if "api_key" not in cfg or not cfg["api_key"]:
        import os
        cfg["api_key"] = os.environ.get("OPENAI_API_KEY", "")
        if not cfg["api_key"]:
            raise ValueError("OpenAI backend requires an 'api_key' in the ai config block or OPENAI_API_KEY env var.")
            
    return compat_generate_image(prompt, seed, cfg, width, height)

def generate_text(prompt: str, seed: int, config: dict):
    cfg = config.copy()
    cfg.setdefault("base_url", "https://api.openai.com/v1")
    cfg.setdefault("model", "gpt-4o-mini")
    
    if "api_key" not in cfg or not cfg["api_key"]:
        import os
        cfg["api_key"] = os.environ.get("OPENAI_API_KEY", "")
        if not cfg["api_key"]:
            raise ValueError("OpenAI backend requires an 'api_key' in the ai config block or OPENAI_API_KEY env var.")
            
    return compat_generate_text(prompt, seed, cfg)
