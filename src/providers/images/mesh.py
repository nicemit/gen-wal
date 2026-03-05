from PIL import Image, ImageDraw, ImageFilter
import random
from src.providers.base import ImageProvider, register_provider

class MeshImageProvider(ImageProvider):
    def __init__(self, config):
        pass
        
    @classmethod
    def name(cls):
        return "mesh"
        
    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        rng = random.Random(seed)
        
        palette = env.get("palette", {})
        bg_hex = palette.get("background", "#1e1e2e")
        accent_hex = palette.get("accent", "#cba6f7")
        sec_hex = palette.get("secondary", "#89b4fa")
        hl_hex = palette.get("highlight", "#f38ba8")
        
        def hex_to_rgb(h):
            if not h: return (0,0,0)
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            
        bg_col = hex_to_rgb(bg_hex)
        colors = [hex_to_rgb(accent_hex), hex_to_rgb(sec_hex), hex_to_rgb(hl_hex)]
        
        # 1. Base Canvas
        img = Image.new('RGB', (width, height), bg_col)
        draw = ImageDraw.Draw(img)
        
        # 2. Draw 4-7 large color blobs
        blob_count = rng.randint(4, 7)
        
        for _ in range(blob_count):
            col = rng.choice(colors)
            # Make radius absolutely massive to prevent defined circle edges
            radius = rng.randint(int(width * 0.3), int(width * 1.0))
            
            # Allow them to spawn dramatically off-screen
            cx = rng.randint(int(-width * 0.5), int(width * 1.5))
            cy = rng.randint(int(-height * 0.5), int(height * 1.5))
            
            x0 = cx - radius
            y0 = cy - radius
            x1 = cx + radius
            y1 = cy + radius
            
            draw.ellipse([x0, y0, x1, y1], fill=col)
            
        # 3. Apply heavy gaussian blur
        # We run it multiple times for extra smoothness, bridging the gaps into a mesh.
        blur_strength = rng.randint(150, 250)
        img = img.filter(ImageFilter.GaussianBlur(radius=blur_strength))
        # A second smaller pass natively smooths the gradient banding
        img = img.filter(ImageFilter.GaussianBlur(radius=int(blur_strength/2)))
        
        return img

register_provider('image', MeshImageProvider)
