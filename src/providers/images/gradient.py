from PIL import Image, ImageDraw
import random
import os
from src.providers.base import ImageProvider, register_provider

class GradientImageProvider(ImageProvider):
    def __init__(self, config):
        pass
        
    @classmethod
    def name(cls):
        return "gradient"
        
    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        rng = random.Random(seed)
        
        # Base colors driven by seed
        color1 = (rng.randint(20, 100), rng.randint(20, 100), rng.randint(20, 100))
        color2 = (rng.randint(20, 100), rng.randint(20, 100), rng.randint(20, 100))
        
        # Very simple vertical gradient
        base = Image.new('RGB', (width, height), color1)
        top = Image.new('RGB', (width, height), color2)
        mask = Image.new('L', (width, height))
        mask_data = []
        for y in range(height):
            mask_data.extend([int(255 * (y / height))] * width)
        mask.putdata(mask_data)
        
        base.paste(top, (0, 0), mask)
        
        # Save temp and return path or Image?
        # Architecture implies layout composes on the image path or object. 
        # Using PIL Image directly saves tmp I/O.
        return base

register_provider('image', GradientImageProvider)
