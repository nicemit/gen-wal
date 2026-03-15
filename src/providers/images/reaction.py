from PIL import Image, ImageFilter
import random
import numpy as np
from src.providers.base import ImageProvider, register_provider
from src.seed import derive_seed


class ReactionImageProvider(ImageProvider):
    def __init__(self, config):
        pass

    @classmethod
    def name(cls):
        return "reaction"

    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        rng = random.Random(seed)
        np_rng = np.random.RandomState(seed % (2**31))

        palette = env.get("palette", {})
        bg_hex = palette.get("background", "#0e1116")
        accent_hex = palette.get("accent", "#c8a15a")
        sec_hex = palette.get("secondary", "#2d333b")
        hl_hex = palette.get("highlight", "#ffffff")

        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        bg_col = np.array(hex_to_rgb(bg_hex), dtype=np.float64)
        accent_col = np.array(hex_to_rgb(accent_hex), dtype=np.float64)
        sec_col = np.array(hex_to_rgb(sec_hex), dtype=np.float64)
        hl_col = np.array(hex_to_rgb(hl_hex), dtype=np.float64)

        # Seed-derived simulation parameters
        # Classic Gray-Scott parameter sets that produce interesting patterns:
        # Spots: f=0.035, k=0.065  |  Worms: f=0.040, k=0.060
        # Waves: f=0.014, k=0.045  |  Coral: f=0.055, k=0.062
        param_rng = random.Random(derive_seed(seed, "reaction_params"))
        presets = [
            (0.035, 0.065),  # spots / dots
            (0.040, 0.060),  # worm-like structures
            (0.055, 0.062),  # coral / branching
            (0.030, 0.062),  # maze-like patterns
            (0.025, 0.060),  # soliton waves
        ]
        feed_rate, kill_rate = param_rng.choice(presets)
        # Small perturbation for variety
        feed_rate += param_rng.uniform(-0.002, 0.002)
        kill_rate += param_rng.uniform(-0.001, 0.001)

        # Simulation grid
        sim_h = 160
        sim_w = int(sim_h * (width / height))

        # Standard Gray-Scott diffusion coefficients
        D_a = 0.21
        D_b = 0.105

        # 1. Initialize chemical grids
        A = np.ones((sim_h, sim_w), dtype=np.float64)
        B = np.zeros((sim_h, sim_w), dtype=np.float64)

        # Seed the B grid with random circular patches
        noise_rng = random.Random(derive_seed(seed, "reaction_noise"))
        num_patches = noise_rng.randint(6, 16)
        for _ in range(num_patches):
            cx = noise_rng.randint(0, sim_w - 1)
            cy = noise_rng.randint(0, sim_h - 1)
            radius = noise_rng.randint(2, max(3, sim_h // 12))

            # Circular seeding
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= radius * radius:
                        ny = (cy + dy) % sim_h
                        nx = (cx + dx) % sim_w
                        B[ny, nx] = 1.0
                        A[ny, nx] = 0.5

        # Add slight perturbation
        A += np_rng.uniform(-0.01, 0.01, (sim_h, sim_w))
        B += np_rng.uniform(-0.01, 0.01, (sim_h, sim_w))
        A = np.clip(A, 0, 1)
        B = np.clip(B, 0, 1)

        # 2. Run Gray-Scott simulation (~200 iterations)
        for _ in range(200):
            # Laplacian via 5-point stencil (toroidal boundary)
            LA = (
                np.roll(A, 1, axis=0) + np.roll(A, -1, axis=0) +
                np.roll(A, 1, axis=1) + np.roll(A, -1, axis=1) -
                4 * A
            )
            LB = (
                np.roll(B, 1, axis=0) + np.roll(B, -1, axis=0) +
                np.roll(B, 1, axis=1) + np.roll(B, -1, axis=1) -
                4 * B
            )

            ABB = A * B * B
            A_new = A + D_a * LA - ABB + feed_rate * (1 - A)
            B_new = B + D_b * LB + ABB - (kill_rate + feed_rate) * B

            A = np.clip(A_new, 0, 1)
            B = np.clip(B_new, 0, 1)

        # 3. Convert B grid to color map using vectorized palette gradient
        b_min = B.min()
        b_max = B.max()
        if b_max - b_min > 1e-6:
            B_norm = (B - b_min) / (b_max - b_min)
        else:
            B_norm = np.zeros_like(B)

        # 4-stop gradient: bg -> sec -> accent -> highlight (fully vectorized)
        color_img = np.zeros((sim_h, sim_w, 3), dtype=np.float64)

        mask1 = B_norm < 0.33
        t1 = np.where(mask1, B_norm / 0.33, 0)
        for c in range(3):
            color_img[:, :, c] += mask1 * (bg_col[c] * (1 - t1) + sec_col[c] * t1)

        mask2 = (B_norm >= 0.33) & (B_norm < 0.66)
        t2 = np.where(mask2, (B_norm - 0.33) / 0.33, 0)
        for c in range(3):
            color_img[:, :, c] += mask2 * (sec_col[c] * (1 - t2) + accent_col[c] * t2)

        mask3 = B_norm >= 0.66
        t3 = np.where(mask3, (B_norm - 0.66) / 0.34, 0)
        for c in range(3):
            color_img[:, :, c] += mask3 * (accent_col[c] * (1 - t3) + hl_col[c] * t3)

        color_img = np.clip(color_img, 0, 255).astype(np.uint8)

        # 4. Create PIL image, upscale, and smooth
        img = Image.fromarray(color_img, 'RGB')
        img = img.resize((width, height), Image.Resampling.BILINEAR)

        # Smooth upscaling artifacts
        img = img.filter(ImageFilter.GaussianBlur(radius=2.5))

        return img


register_provider('image', ReactionImageProvider)
