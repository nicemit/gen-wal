import math
from src.providers.base import ImageProvider, register_provider
from PIL import Image, ImageDraw

class SpiralProvider(ImageProvider):
    def __init__(self, config):
        self.config = config

    @classmethod
    def name(cls):
        """The name used in config under image_provider"""
        return "spiral"

    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080):
        """
        A minimal example provider that draws a generative spiral.
        To install this, copy this file into: 
        ~/.local/share/genwal/providers/images/
        """
        # 1. Get colors from the active palette
        palette = env.get("palette", {})
        bg_hex = palette.get("background", "#1e1e2e")
        fg_hex = palette.get("accent", "#f5e0dc")
        
        # 2. Setup image
        img = Image.new("RGB", (width, height), bg_hex)
        draw = ImageDraw.Draw(img)
        
        # 3. Use the seed to control the spiral
        # (This ensures the wallpaper stays the same all day, but changes tomorrow)
        import random
        rng = random.Random(seed)
        
        center_x = width // 2
        center_y = height // 2
        
        max_radius = min(width, height) * 0.8
        turns = rng.randint(5, 15)
        points = []
        
        for i in range(1000):
            t = i / 1000.0
            angle = turns * 2 * math.pi * t
            radius = max_radius * t
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
            
        # Draw the lines
        if len(points) > 1:
            draw.line(points, fill=fg_hex, width=rng.randint(2, 6))
            
        return img

# IMPORTANT: Always register your provider!
register_provider("image", SpiralProvider, origin="user")
