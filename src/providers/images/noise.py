from PIL import Image, ImageFilter
import random
from src.providers.base import ImageProvider, register_provider

class NoiseImageProvider(ImageProvider):
    def __init__(self, config):
        pass
        
    @classmethod
    def name(cls):
        return "noise"
        
    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        rng = random.Random(seed)
        
        palette = env.get("palette", {})
        bg_hex = palette.get("background", "#1a1b26")
        
        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            
        bg_color = hex_to_rgb(bg_hex)
        
        # Create base color
        img = Image.new('RGB', (width, height), bg_color)
        
        # We need fast noise, Python loops are too slow for 1920x1080 per pixel, 
        # so we generate a small noise patch and tile/resize it.
        patch_size = 256
        noise_patch = Image.new('L', (patch_size, patch_size))
        pixels = [rng.randint(0, 40) for _ in range(patch_size * patch_size)]
        noise_patch.putdata(pixels)
        
        # Scale to fit (which naturally blurs it slightly into film-like grain)
        noise_scaled = noise_patch.resize((width, height), Image.Resampling.BILINEAR)
        
        # Composite grain over the subtle background
        img = Image.blend(img, noise_scaled.convert('RGB'), alpha=0.15)
        
        return img

register_provider('image', NoiseImageProvider)
