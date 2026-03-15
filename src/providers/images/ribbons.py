from PIL import Image, ImageDraw, ImageFilter
import random
import math
from src.providers.base import ImageProvider, register_provider
from src.seed import derive_seed


class RibbonsImageProvider(ImageProvider):
    def __init__(self, config):
        pass

    @classmethod
    def name(cls):
        return "ribbons"

    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        rng = random.Random(seed)

        palette = env.get("palette", {})
        bg_hex = palette.get("background", "#0d1117")
        accent_hex = palette.get("accent", "#58a6ff")
        sec_hex = palette.get("secondary", "#21262d")
        hl_hex = palette.get("highlight", "#ffffff")

        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        bg_col = hex_to_rgb(bg_hex)
        ribbon_colors = [hex_to_rgb(accent_hex), hex_to_rgb(sec_hex), hex_to_rgb(hl_hex)]

        # Add blended variants
        blend_rng = random.Random(derive_seed(seed, "ribbon_colors"))
        for _ in range(2):
            c1, c2 = blend_rng.sample(ribbon_colors, 2)
            t = blend_rng.uniform(0.3, 0.7)
            ribbon_colors.append((
                int(c1[0] * t + c2[0] * (1 - t)),
                int(c1[1] * t + c2[1] * (1 - t)),
                int(c1[2] * t + c2[2] * (1 - t)),
            ))

        # Seed-derived parameters
        param_rng = random.Random(derive_seed(seed, "ribbon_params"))
        curve_count = param_rng.randint(8, 20)
        step_size = param_rng.uniform(2.0, 5.0)
        curvature_scale = param_rng.uniform(0.002, 0.006)
        thickness_base = param_rng.randint(4, 20)

        # Build vector field using layered sin/cos
        field_rng = random.Random(derive_seed(seed, "ribbon_field"))
        num_layers = field_rng.randint(2, 4)
        field_layers = []
        for _ in range(num_layers):
            field_layers.append({
                'fx': field_rng.uniform(0.5, 3.0),
                'fy': field_rng.uniform(0.5, 3.0),
                'px': field_rng.uniform(0, math.pi * 2),
                'py': field_rng.uniform(0, math.pi * 2),
                'w': field_rng.uniform(0.3, 1.0),
            })

        def get_angle(x, y):
            angle = 0.0
            tw = 0.0
            for fl in field_layers:
                nx = x * curvature_scale * fl['fx']
                ny = y * curvature_scale * fl['fy']
                angle += fl['w'] * (math.sin(nx + fl['px']) + math.cos(ny + fl['py']))
                tw += fl['w']
            return (angle / tw) * math.pi

        # Create base image
        base = Image.new('RGBA', (width, height), bg_col + (255,))

        # Max steps per curve to ensure it spans a reasonable distance
        max_steps = max(width, height) // int(step_size) + 50

        for _ in range(curve_count):
            # Start points: spread across canvas with some randomness
            sx = rng.uniform(-width * 0.1, width * 1.1)
            sy = rng.uniform(-height * 0.1, height * 1.1)

            col = rng.choice(ribbon_colors)
            alpha = rng.randint(80, 180)
            thickness = thickness_base + rng.randint(-3, 5)
            thickness = max(2, thickness)

            # Integrate curve through the vector field
            points = []
            x, y = sx, sy
            for _ in range(max_steps):
                points.append((x, y))
                angle = get_angle(x, y)
                x += math.cos(angle) * step_size
                y += math.sin(angle) * step_size

                # Stop if far off canvas
                if x < -width * 0.3 or x > width * 1.3 or y < -height * 0.3 or y > height * 1.3:
                    break

            if len(points) < 3:
                continue

            # Draw ribbon as a thick semi-transparent line
            ribbon_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            ribbon_draw = ImageDraw.Draw(ribbon_layer)

            ribbon_draw.line(points, fill=(col[0], col[1], col[2], alpha), width=thickness, joint="curve")

            base = Image.alpha_composite(base, ribbon_layer)

        # Convert to RGB and apply gentle blur
        result = base.convert('RGB')
        blur_rng = random.Random(derive_seed(seed, "ribbon_blur"))
        blur_radius = blur_rng.uniform(0.8, 2.5)
        result = result.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        return result


register_provider('image', RibbonsImageProvider)
