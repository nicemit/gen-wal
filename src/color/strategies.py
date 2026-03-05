import random
import colorsys

def hex_to_hsv(hex_color: str):
    """Convert hex to HSV (Hue 0-1, Saturation 0-1, Value(Brightness) 0-1)."""
    hex_color = hex_color.lstrip('#')
    if not hex_color:
        return (0.0, 0.0, 0.0)
    rgb = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return colorsys.rgb_to_hsv(*rgb)

def hsv_to_hex(h, s, v):
    """Convert HSV back to Hex."""
    rgb = colorsys.hsv_to_rgb(h, s, v)
    return "#{:02x}{:02x}{:02x}".format(
        int(max(0, min(1.0, rgb[0])) * 255),
        int(max(0, min(1.0, rgb[1])) * 255),
        int(max(0, min(1.0, rgb[2])) * 255)
    )

def apply_strategy(palette: dict, strategy: str, seed: int) -> dict:
    """Transforms a palette using a color theory strategy safely bounded by a deterministic seed."""
    rng = random.Random(seed)
    
    # We base the transformations roughly on the dominant 'background' or 'accent' color.
    base_hex = palette.get("background", "#0e1116")
    base_h, base_s, base_v = hex_to_hsv(base_hex)
    
    new_palette = palette.copy()
    
    # Randomly shift the base hue for the day based on the seed so it's not always the same color
    base_h = (base_h + rng.random()) % 1.0
    
    # Ensure the background has at least SOME saturation and brightness so colors show through
    bg_s = max(0.15, min(1.0, base_s + rng.uniform(-0.1, 0.3)))
    bg_v = max(0.15, min(1.0, base_v + rng.uniform(-0.1, 0.3)))
    
    work_s = max(0.4, bg_s + 0.3)
    work_v = max(0.4, bg_v + 0.3)
    
    if strategy == "monochrome":
        # Keep hue, vary saturation and brightness heavily
        new_palette['background'] = hsv_to_hex(base_h, rng.uniform(0.1, 0.4), rng.uniform(0.1, 0.3))
        new_palette['secondary'] = hsv_to_hex(base_h, rng.uniform(0.3, 0.7), rng.uniform(0.3, 0.6))
        new_palette['accent'] = hsv_to_hex(base_h, rng.uniform(0.5, 1.0), rng.uniform(0.6, 1.0))
        
    elif strategy == "analogous":
        # Shift hue within ±30 degrees (±0.08 in 0-1 range)
        shift1 = rng.uniform(0.02, 0.08)
        shift2 = rng.uniform(-0.08, -0.02)
        new_palette['background'] = hsv_to_hex(base_h, bg_s, bg_v)
        new_palette['secondary'] = hsv_to_hex((base_h + shift1) % 1.0, work_s, min(1.0, work_v + 0.2))
        new_palette['accent'] = hsv_to_hex((base_h + shift2) % 1.0, min(1.0, work_s + 0.2), min(1.0, work_v + 0.4))
        
    elif strategy == "complementary":
        # Accent is precisely on the opposite side of the color wheel (180 deg / +0.5)
        new_palette['background'] = hsv_to_hex(base_h, bg_s, bg_v)
        new_palette['secondary'] = hsv_to_hex(base_h, work_s, min(1.0, work_v * 1.5))
        new_palette['accent'] = hsv_to_hex((base_h + 0.5) % 1.0, max(0.6, work_s), max(0.7, work_v + 0.3))
        
    elif strategy == "triadic":
        # Three colors spaced evenly (120 deg / +0.33)
        new_palette['background'] = hsv_to_hex(base_h, bg_s, bg_v)
        new_palette['secondary'] = hsv_to_hex((base_h + 0.33) % 1.0, work_s, min(1.0, work_v + 0.3))
        new_palette['accent'] = hsv_to_hex((base_h + 0.66) % 1.0, work_s, min(1.0, work_v + 0.4))
        
    elif strategy == "accent":
        # Desaturate backgrounds into neutral grays, punch up the accent heavily
        new_palette['background'] = hsv_to_hex(base_h, 0.05, rng.uniform(0.1, 0.2))
        new_palette['secondary'] = hsv_to_hex(base_h, 0.1, rng.uniform(0.2, 0.4))
        # Pure random hue for the punchy accent
        new_palette['accent'] = hsv_to_hex(rng.random(), rng.uniform(0.7, 1.0), rng.uniform(0.8, 1.0))
        
    return new_palette

def compute_color_strategy(color_mode: str, seed: int) -> str:
    """Mapper determining which strategy to employ based on user's config mode."""
    rng = random.Random(seed)
    
    mode_map = {
        "minimal": ["monochrome", "analogous"],
        "balanced": ["analogous", "accent", "complementary"],
        "vibrant": ["triadic", "complementary"],
        "wild": ["monochrome", "analogous", "complementary", "triadic", "accent"]
    }
    
    strategies = mode_map.get(color_mode.lower(), mode_map["balanced"])
    return rng.choice(strategies)
