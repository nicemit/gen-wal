from PIL import Image, ImageDraw
import random
import math
from src.providers.base import ImageProvider, register_provider

class VoronoiImageProvider(ImageProvider):
    def __init__(self, config):
        pass
        
    @classmethod
    def name(cls):
        return "voronoi"
        
    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        rng = random.Random(seed)
        
        palette = env.get("palette", {})
        bg_hex = palette.get("background", "#000000")
        accent_hex = palette.get("accent", "#555555")
        sec_hex = palette.get("secondary", "#333333")
        
        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            
        colors = [hex_to_rgb(bg_hex), hex_to_rgb(accent_hex), hex_to_rgb(sec_hex)]
        
        # Add random intermediate colors based on palette to make it richer
        for _ in range(3):
            c1, c2 = rng.sample(colors, 2)
            blend_ratio = rng.random()
            colors.append((
                int(c1[0] * blend_ratio + c2[0] * (1 - blend_ratio)),
                int(c1[1] * blend_ratio + c2[1] * (1 - blend_ratio)),
                int(c1[2] * blend_ratio + c2[2] * (1 - blend_ratio))
            ))
            
        num_cells = rng.randint(20, 50)
        
        # Generate random points and assign colors
        # To avoid points clumping, we place them on a loose grid
        points = []
        grid_dim = int(math.sqrt(num_cells))
        cell_w, cell_h = width / grid_dim, height / grid_dim
        
        for r in range(grid_dim):
            for c in range(grid_dim):
                cx = cell_w * c + rng.uniform(0, cell_w)
                cy = cell_h * r + rng.uniform(0, cell_h)
                points.append((cx, cy, rng.choice(colors)))
                
        # Generate the Voronoi diagram on downscaled resolution for performance
        scale = 0.25 # Compute voronoi map at 25% resolution, then scale up blocky
        v_width, v_height = int(width * scale), int(height * scale)
        
        img = Image.new('RGB', (v_width, v_height))
        
        # Convert points relative to downscaled size
        points_scaled = [(x * scale, y * scale, col) for x, y, col in points]
        
        # Brute force (since it's downscaled and few points)
        # For each pixel, find closest point
        pixels = []
        for py in range(v_height):
            for px in range(v_width):
                min_dist = float('inf')
                min_col = (0, 0, 0)
                
                for px2, py2, col in points_scaled:
                    dist = (px - px2)**2 + (py - py2)**2
                    if dist < min_dist:
                        min_dist = dist
                        min_col = col
                pixels.append(min_col)
                
        img.putdata(pixels)
        
        # Scale back up using NEAREST to maintain sharp geometric edges
        return img.resize((width, height), Image.Resampling.NEAREST)

register_provider('image', VoronoiImageProvider)
