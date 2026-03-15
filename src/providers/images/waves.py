from PIL import Image, ImageDraw, ImageFilter
import random
import math
from src.providers.base import ImageProvider, register_provider
from src.seed import derive_seed


class WavesImageProvider(ImageProvider):
    def __init__(self, config):
        pass

    @classmethod
    def name(cls):
        return "waves"

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

        bg_col = hex_to_rgb(bg_hex)
        accent_col = hex_to_rgb(accent_hex)
        sec_col = hex_to_rgb(sec_hex)
        hl_col = hex_to_rgb(hl_hex)

        # Build a color pool from palette for wave fills
        wave_palette = [accent_col, sec_col]
        blend_rng = random.Random(derive_seed(seed, "wave_colors"))
        for _ in range(3):
            c1, c2 = blend_rng.sample([bg_col, accent_col, sec_col, hl_col], 2)
            t = blend_rng.uniform(0.25, 0.75)
            wave_palette.append((
                int(c1[0] * t + c2[0] * (1 - t)),
                int(c1[1] * t + c2[1] * (1 - t)),
                int(c1[2] * t + c2[2] * (1 - t)),
            ))

        # 1. Create gradient base (top to bottom)
        base = Image.new('RGB', (width, height))
        base_draw = ImageDraw.Draw(base)
        for y in range(height):
            t = y / height
            t = t * t * (3 - 2 * t)  # smoothstep
            r = int(bg_col[0] * (1 - t) + sec_col[0] * t)
            g = int(bg_col[1] * (1 - t) + sec_col[1] * t)
            b = int(bg_col[2] * (1 - t) + sec_col[2] * t)
            base_draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 2. Seed-derived wave parameters
        param_rng = random.Random(derive_seed(seed, "wave_params"))
        wave_count = param_rng.randint(4, 8)

        waves = []
        for i in range(wave_count):
            # Each wave sits at a different vertical position (spread across canvas)
            base_y = height * (0.25 + 0.65 * (i / max(wave_count - 1, 1)))
            waves.append({
                'base_y': base_y,
                'amplitude': param_rng.uniform(height * 0.02, height * 0.08),
                'frequency': param_rng.uniform(0.003, 0.012),
                'phase': param_rng.uniform(0, math.pi * 2),
                'secondary_amp': param_rng.uniform(height * 0.005, height * 0.025),
                'secondary_freq': param_rng.uniform(0.008, 0.025),
                'secondary_phase': param_rng.uniform(0, math.pi * 2),
                'color': rng.choice(wave_palette),
            })

        # 3. Draw wave layers back-to-front (topmost first so lower waves overlay)
        for wave in waves:
            layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            layer_draw = ImageDraw.Draw(layer)

            # Compute wave curve: y = base_y + amp*sin(freq*x + phase) + secondary harmonic
            points_top = []
            for x in range(width):
                y = wave['base_y']
                y += wave['amplitude'] * math.sin(wave['frequency'] * x + wave['phase'])
                y += wave['secondary_amp'] * math.sin(wave['secondary_freq'] * x + wave['secondary_phase'])
                points_top.append((x, y))

            # Build polygon: wave curve on top, bottom of image on bottom
            polygon = list(points_top)
            polygon.append((width, height))
            polygon.append((0, height))

            col = wave['color']
            alpha = rng.randint(140, 210)
            layer_draw.polygon(polygon, fill=(col[0], col[1], col[2], alpha))

            base.paste(Image.alpha_composite(
                base.convert('RGBA'), layer
            ).convert('RGB'))
            base = base.convert('RGB')

        # 4. Gentle blur for soft blending
        blur_rng = random.Random(derive_seed(seed, "wave_blur"))
        blur_radius = blur_rng.uniform(1.0, 3.0)
        base = base.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        return base


register_provider('image', WavesImageProvider)
