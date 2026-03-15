from PIL import Image, ImageFilter
import random
import math
from src.providers.base import ImageProvider, register_provider
from src.seed import derive_seed


class VoronoiImageProvider(ImageProvider):
    def __init__(self, config):
        pass

    @classmethod
    def name(cls):
        return "voronoi"

    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        rng = random.Random(seed)

        palette = env.get("palette", {})
        bg_hex = palette.get("background", "#0e1116")
        accent_hex = palette.get("accent", "#c8a15a")
        sec_hex = palette.get("secondary", "#2d333b")
        hl_hex = palette.get("highlight", "#ffffff")

        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        base_colors = [hex_to_rgb(bg_hex), hex_to_rgb(accent_hex), hex_to_rgb(sec_hex)]
        edge_color = hex_to_rgb(hl_hex)

        # Generate blended palette variants
        color_rng = random.Random(derive_seed(seed, "voronoi_colors"))
        extended_colors = list(base_colors)
        for _ in range(4):
            c1, c2 = color_rng.sample(base_colors, 2)
            t = color_rng.uniform(0.2, 0.8)
            extended_colors.append((
                int(c1[0] * t + c2[0] * (1 - t)),
                int(c1[1] * t + c2[1] * (1 - t)),
                int(c1[2] * t + c2[2] * (1 - t)),
            ))

        # Seed-derived parameters
        param_rng = random.Random(derive_seed(seed, "voronoi_params"))
        cell_count = param_rng.randint(30, 80)
        edge_blur = param_rng.uniform(0.5, 2.0)
        shade_strength = param_rng.uniform(0.1, 0.35)

        # Generate seed points on a jittered grid to avoid clumping
        grid_dim = int(math.sqrt(cell_count))
        if grid_dim < 1:
            grid_dim = 1
        cell_w = width / grid_dim
        cell_h = height / grid_dim

        points = []
        for r in range(grid_dim + 1):
            for c in range(grid_dim + 1):
                cx = cell_w * c + rng.uniform(cell_w * 0.1, cell_w * 0.9)
                cy = cell_h * r + rng.uniform(cell_h * 0.1, cell_h * 0.9)
                col = rng.choice(extended_colors)
                points.append((cx, cy, col))

        # Compute at reduced resolution for performance
        scale = 0.2
        v_width = max(1, int(width * scale))
        v_height = max(1, int(height * scale))

        # Scale points
        points_scaled = [(x * scale, y * scale, col) for x, y, col in points]

        pixels = []
        for py in range(v_height):
            for px in range(v_width):
                # Find closest and second-closest point
                min_dist = float('inf')
                min_dist2 = float('inf')
                min_col = (0, 0, 0)

                for sx, sy, col in points_scaled:
                    dist = (px - sx) ** 2 + (py - sy) ** 2
                    if dist < min_dist:
                        min_dist2 = min_dist
                        min_dist = dist
                        min_col = col
                    elif dist < min_dist2:
                        min_dist2 = dist

                # Distance shading: darken pixels closer to cell center
                d = math.sqrt(min_dist) if min_dist > 0 else 0
                d2 = math.sqrt(min_dist2) if min_dist2 > 0 else 1

                # Edge detection: pixels near border between two cells
                edge_ratio = d / (d2 + 0.001)

                # Apply distance-based shading
                shade = 1.0 - shade_strength * (1.0 - min(d / (cell_w * scale * 0.5), 1.0))

                r_out = int(min_col[0] * shade)
                g_out = int(min_col[1] * shade)
                b_out = int(min_col[2] * shade)

                # Blend toward edge color near cell boundaries
                if edge_ratio > 0.85:
                    edge_t = (edge_ratio - 0.85) / 0.15
                    edge_t = min(edge_t * 0.6, 0.6)
                    r_out = int(r_out * (1 - edge_t) + edge_color[0] * edge_t)
                    g_out = int(g_out * (1 - edge_t) + edge_color[1] * edge_t)
                    b_out = int(b_out * (1 - edge_t) + edge_color[2] * edge_t)

                pixels.append((
                    max(0, min(255, r_out)),
                    max(0, min(255, g_out)),
                    max(0, min(255, b_out)),
                ))

        img = Image.new('RGB', (v_width, v_height))
        img.putdata(pixels)

        # Upscale with slight smoothing
        img = img.resize((width, height), Image.Resampling.LANCZOS)

        # Optional edge blur for softer cell boundaries
        if edge_blur > 1.0:
            img = img.filter(ImageFilter.GaussianBlur(radius=edge_blur))

        return img


register_provider('image', VoronoiImageProvider)
