from PIL import Image, ImageDraw, ImageFilter
import random
import math
from src.providers.base import ImageProvider, register_provider
from src.seed import derive_seed


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
        hl_hex = palette.get("highlight", "#ffffff")

        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        bg_col = hex_to_rgb(bg_hex)
        trail_colors = [hex_to_rgb(accent_hex), hex_to_rgb(sec_hex), hex_to_rgb(hl_hex)]

        img = Image.new('RGB', (width, height), bg_col)
        draw = ImageDraw.Draw(img)

        # Seed-derived parameters
        param_rng = random.Random(derive_seed(seed, "flow_params"))
        particle_count = param_rng.randint(800, 2000)
        trail_length = param_rng.randint(30, 120)
        noise_scale = param_rng.uniform(0.002, 0.008)
        line_width_base = param_rng.randint(1, 3)

        # Build a procedural vector field using layered sin/cos
        field_rng = random.Random(derive_seed(seed, "flow_field"))
        num_octaves = field_rng.randint(2, 4)
        octaves = []
        for _ in range(num_octaves):
            octaves.append({
                'freq_x': field_rng.uniform(0.5, 3.0),
                'freq_y': field_rng.uniform(0.5, 3.0),
                'phase_x': field_rng.uniform(0, math.pi * 2),
                'phase_y': field_rng.uniform(0, math.pi * 2),
                'weight': field_rng.uniform(0.3, 1.0),
            })

        def get_angle(x, y):
            """Compute vector field angle at (x, y) using layered sin/cos."""
            angle = 0.0
            total_weight = 0.0
            for o in octaves:
                nx = x * noise_scale * o['freq_x']
                ny = y * noise_scale * o['freq_y']
                angle += o['weight'] * (math.sin(nx + o['phase_x']) + math.cos(ny + o['phase_y']))
                total_weight += o['weight']
            return (angle / total_weight) * math.pi

        # Spawn particles and trace trails
        for _ in range(particle_count):
            x = rng.uniform(0, width)
            y = rng.uniform(0, height)

            col = rng.choice(trail_colors)
            # Slight color variation per particle
            col_varied = (
                max(0, min(255, col[0] + rng.randint(-25, 25))),
                max(0, min(255, col[1] + rng.randint(-25, 25))),
                max(0, min(255, col[2] + rng.randint(-25, 25))),
            )

            lw = line_width_base if rng.random() > 0.3 else line_width_base + 1
            step_size = rng.uniform(1.5, 3.0)

            points = [(x, y)]
            for _ in range(trail_length):
                angle = get_angle(x, y)
                x += math.cos(angle) * step_size
                y += math.sin(angle) * step_size

                # Stop if particle leaves canvas (with margin)
                if x < -50 or x > width + 50 or y < -50 or y > height + 50:
                    break

                points.append((x, y))

            if len(points) >= 2:
                draw.line(points, fill=col_varied, width=lw)

        # Gentle blur for organic softness
        blur_radius = rng.uniform(0.3, 1.2)
        return img.filter(ImageFilter.GaussianBlur(radius=blur_radius))


register_provider('image', FlowImageProvider)
