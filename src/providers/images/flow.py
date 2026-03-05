from PIL import Image, ImageDraw, ImageFilter
import random
import math
from src.providers.base import ImageProvider, register_provider

class FlowImageProvider(ImageProvider):
    def __init__(self, config):
        pass
        
    @classmethod
    def name(cls):
        return "flow"
        
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
        
        img = Image.new('RGB', (width, height), bg_col)
        draw = ImageDraw.Draw(img)
        
        # Very simple vector flow field
        # Break space into grid
        grid_size = rng.randint(40, 80)
        cols = width // grid_size + 2
        rows = height // grid_size + 2
        
        # Seeded pseudo-Perlin angles (simple approximation using noise map)
        angles = [[rng.uniform(0, math.pi * 2) for _ in range(cols)] for _ in range(rows)]
        
        # Smooth the angles slightly for flow effect
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                avg_angle = (angles[r-1][c] + angles[r+1][c] + angles[r][c-1] + angles[r][c+1]) / 4
                angles[r][c] = (angles[r][c] + avg_angle) / 2

        num_lines = rng.randint(500, 1500)
        
        for _ in range(num_lines):
            x = rng.uniform(0, width)
            y = rng.uniform(0, height)
            
            line_len = rng.randint(20, 100)
            col = rng.choice([accent_col, sec_col])
            
            # Fade colors safely
            col_mapped = (
                max(0, col[0] - rng.randint(0, 40)),
                max(0, col[1] - rng.randint(0, 40)),
                max(0, col[2] - rng.randint(0, 40)),
            )
            
            points = [(x, y)]
            for _ in range(line_len):
                grid_x = max(0, min(cols-1, int(x // grid_size)))
                grid_y = max(0, min(rows-1, int(y // grid_size)))
                
                angle = angles[grid_y][grid_x]
                x += math.cos(angle) * 2
                y += math.sin(angle) * 2
                points.append((x, y))
                
            draw.line(points, fill=col_mapped, width=rng.randint(1, 3))
            
        # Optional: Deep flow usually looks good with a slight blur
        return img.filter(ImageFilter.GaussianBlur(radius=rng.uniform(0.5, 1.5)))

register_provider('image', FlowImageProvider)
