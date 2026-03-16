from .openai_compatible import generate_image as compat_generate_image

def generate_image(prompt: str, seed: int, config: dict, width: int, height: int):
    # Just an alias wrapper for semantics if explicitly selected
    # Users will typically just use "openai_compatible" explicitly, but this is here for clarity
    cfg = config.copy()
    cfg.setdefault("base_url", "http://localhost:11434/v1") # Ollama default compatible endpoint
    cfg.setdefault("model", "llama3") # Needs an image capable model though 
    
    return compat_generate_image(prompt, seed, cfg, width, height)
