from PIL import Image, ImageDraw, ImageFilter
import random
import math
from src.providers.base import ImageProvider, register_provider

class AuroraImageProvider(ImageProvider):
    def __init__(self, config):
        pass
        
    @classmethod
    def name(cls):
        return "aurora"
        
    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        rng = random.Random(seed)
        
        palette = env.get("palette", {})
        bg_hex = palette.get("background", "#0d1117")
        accent_hex = palette.get("accent", "#58a6ff")
        sec_hex = palette.get("secondary", "#21262d")
        
        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            
        bg_col = hex_to_rgb(bg_hex)
        accent_col = hex_to_rgb(accent_hex)
        sec_col = hex_to_rgb(sec_hex)
        
        # Blend an intermediate color
        third_col = (
            int((bg_col[0] + accent_col[0]) / 2),
            int((bg_col[1] + accent_col[1]) / 2),
            int((bg_col[2] + accent_col[2]) / 2)
        )
        
        colors = [accent_col, sec_col, third_col]
        
        # 1. Base color (deep background)
        img = Image.new('RGB', (width, height), bg_col)
        draw = ImageDraw.Draw(img)
        
        # 2. Draw 3-6 extremely large shapes scattered across canvas
        num_blobs = rng.randint(3, 6)
        
        for _ in range(num_blobs):
            col = rng.choice(colors)
            blob_radius = rng.randint(int(width * 0.3), int(width * 0.8))
            
            # Place centers randomly, allowing them to hang off edges
            cx = rng.randint(int(-width * 0.2), int(width * 1.2))
            cy = rng.randint(int(-height * 0.2), int(height * 1.2))
            
            x0 = cx - blob_radius
            y0 = cy - blob_radius
            x1 = cx + blob_radius
            y1 = cy + blob_radius
            
            draw.ellipse([x0, y0, x1, y1], fill=col)
            
        # 3. Apply a massive Gaussian Blur to melt them together into the "Aurora/Mesh" effect
        # The larger the radius, the smoother the blobs blend. 
        # (This is why macOS wallpapers look like pure gradients without edges)
        blur_radius = rng.randint(int(width * 0.2), int(width * 0.4))
        img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # 4. Apply a subtle static overlay film grain
        patch_size = 256
        noise_patch = Image.new('L', (patch_size, patch_size))
        pixels = [rng.randint(0, 30) for _ in range(patch_size * patch_size)]
        noise_patch.putdata(pixels)
        noise_scaled = noise_patch.resize((width, height), Image.Resampling.BILINEAR)
        img = Image.blend(img, noise_scaled.convert('RGB'), alpha=0.08)
        
        return img

register_provider('image', AuroraImageProvider)
