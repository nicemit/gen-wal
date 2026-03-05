from PIL import Image, ImageDraw
import random
import math
from src.providers.base import ImageProvider, register_provider

class GradientImageProvider(ImageProvider):
    def __init__(self, config):
        pass
        
    @classmethod
    def name(cls):
        return "gradient"
        
    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        rng = random.Random(seed)
        
        # Get palette colors or generate random fallbacks
        palette = env.get("palette", {})
        bg_hex = palette.get("background", "#0e1116")
        accent_hex = palette.get("accent", "#c8a15a")
        sec_hex = palette.get("secondary", "#2d333b")
        
        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            
        c1 = hex_to_rgb(bg_hex)
        c2 = hex_to_rgb(sec_hex)
        c3 = hex_to_rgb(accent_hex)
        
        # We will create a diagonal gradient
        base = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(base)
        
        # Decide orientation deterministically
        orientation = rng.choice(["vertical", "horizontal", "diagonal_down", "diagonal_up"])
        
        for y in range(height):
            for x in range(width):
                if orientation == "vertical":
                    ratio = y / height
                elif orientation == "horizontal":
                    ratio = x / width
                elif orientation == "diagonal_down":
                    ratio = (x + y) / (width + height)
                else: # diagonal_up
                    ratio = (x + (height - y)) / (width + height)
                    
                # Smoothstep blending
                ratio = ratio * ratio * (3 - 2 * ratio)
                
                # Blend 3 colors
                if ratio < 0.5:
                    r2 = ratio * 2
                    r = int(c1[0] * (1 - r2) + c2[0] * r2)
                    g = int(c1[1] * (1 - r2) + c2[1] * r2)
                    b = int(c1[2] * (1 - r2) + c2[2] * r2)
                else:
                    r2 = (ratio - 0.5) * 2
                    r = int(c2[0] * (1 - r2) + c3[0] * r2)
                    g = int(c2[1] * (1 - r2) + c3[1] * r2)
                    b = int(c2[2] * (1 - r2) + c3[2] * r2)
                    
                draw.point((x, y), fill=(r, g, b))
                
        return base

register_provider('image', GradientImageProvider)
