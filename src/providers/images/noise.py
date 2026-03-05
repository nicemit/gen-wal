from PIL import Image, ImageFilter
import random
from src.providers.base import ImageProvider, register_provider

class NoiseImageProvider(ImageProvider):
    def __init__(self, config):
        self.config = config
        
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
        sec_color = hex_to_rgb(palette.get("secondary", "#333333"))
        acc_color = hex_to_rgb(palette.get("accent", "#ffffff"))
        
        # Create base color
        img = Image.new('RGB', (width, height), bg_color)
        
        # Read user-configuration or use sensible defaults
        p_cfg = self.config.get('noise', {})
        scale = p_cfg.get('scale', 10)           # 1 = tiny tv static, 50 = huge blocks
        opacity = p_cfg.get('opacity', 0.25)     # 0.0 - 1.0 visiblity
        style = p_cfg.get('style', 'smooth')     # "smooth" or "blocky"
        
        # We start by generating a smaller patch of noise based on the scale parameter
        # So if scale is 10, the patch is 1/10th the width
        # The smaller the patch, the larger the noise gets when scaled up
        patch_w = max(1, int(width / scale))
        patch_h = max(1, int(height / scale))
        
        noise_patch = Image.new('RGB', (patch_w, patch_h))
        
        pixels = []
        for _ in range(patch_w * patch_h):
            # Softly mix the colors
            choice = rng.random()
            if choice < 0.6:
                pixels.append(bg_color)
            elif choice < 0.9:
                pixels.append(sec_color)
            else:
                pixels.append(acc_color)
                
        noise_patch.putdata(pixels)
        
        resample_filter = Image.Resampling.BILINEAR if style == 'smooth' else Image.Resampling.NEAREST
        noise_scaled = noise_patch.resize((width, height), resample_filter)
        
        # Blend it according to the requested opacity
        img = Image.blend(img, noise_scaled, alpha=opacity)
        
        # Add a secondary high-frequency static noise layer on top for texture
        static_patch = Image.new('L', (width // 2, height // 2))
        static_pixels = [rng.randint(0, 150) for _ in range((width // 2) * (height // 2))]
        static_patch.putdata(static_pixels)
        static_scaled = static_patch.resize((width, height), Image.Resampling.NEAREST)
        
        # Blend the high-frequency static texture very lightly
        img = Image.blend(img, static_scaled.convert('RGB'), alpha=min(opacity * 0.3, 0.15))
        
        # Apply a very gentle blur just to take the sharpest digital edge off the pixel art
        img = img.filter(ImageFilter.GaussianBlur(radius=rng.randint(2, 6)))
        
        return img

register_provider('image', NoiseImageProvider)
