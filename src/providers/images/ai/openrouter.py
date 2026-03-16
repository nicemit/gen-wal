from .openai_compatible import generate_image as compat_generate_image

def generate_image(prompt: str, seed: int, config: dict, width: int, height: int):
    cfg = config.copy()
    cfg.setdefault("base_url", "https://openrouter.ai/api/v1")
    return compat_generate_image(prompt, seed, cfg, width, height)
