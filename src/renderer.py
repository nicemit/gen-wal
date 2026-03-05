from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import textwrap

def load_font(font_path: str = None, size: int = 40) -> ImageFont.FreeTypeFont:
    """Loads a font, defaulting to system fonts or a local asset if provided."""
    if font_path and os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
        
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
            
    # Absolute fallback
    return ImageFont.load_default()

def clean_text(text: str) -> str:
    """Removes basic markdown or wrapper quotes."""
    import re
    clean = re.sub(r'(\*\*|__)', '', text)
    clean = re.sub(r'(\*|_)', '', clean)
    clean = clean.strip()
    if (clean.startswith('"') and clean.endswith('"')) or (clean.startswith("'") and clean.endswith("'")):
        clean = clean[1:-1]
    return clean.strip()

def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list:
    """Wraps text to fit within a specific pixel width."""
    # Rough estimation
    avg_char_width = font.size * 0.5
    if avg_char_width <= 0: avg_char_width = 10
    chars_per_line = max(int(max_width / avg_char_width), 10)
    
    # Could be more precise with textbbox in a loop, but textwrap is usually sufficient
    return textwrap.wrap(text, width=chars_per_line)

def draw_text_with_shadow(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, font: ImageFont.FreeTypeFont, text_color: tuple, shadow_color: tuple = (0, 0, 0, 200), offset: int = 2):
    """Draws text with a drop shadow."""
    # Shadow
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
    # Main text
    draw.text((x, y), text, font=font, fill=text_color)
    
def apply_overlay(img: Image.Image, color: tuple = (0, 0, 0, 100)) -> Image.Image:
    """Applies a full-screen semi-transparent overlay."""
    overlay = Image.new('RGBA', img.size, color)
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
def apply_grain(img: Image.Image, seed: int, strength: int = 8) -> Image.Image:
    """Introduces subtle film grain to prevent banding and add texture."""
    import random
    rng = random.Random(seed)
    
    width, height = img.size
    
    # Generate smaller patch and scale up for softer grain (film style)
    patch_size = 256
    noise_patch = Image.new('L', (patch_size, patch_size))
    pixels = [rng.randint(0, int(2.55 * strength)) for _ in range(patch_size * patch_size)]
    noise_patch.putdata(pixels)
    
    noise_scaled = noise_patch.resize((width, height), Image.Resampling.BILINEAR)
    
    # Overlay the noise lightly using alpha blend
    return Image.blend(img.convert('RGB'), noise_scaled.convert('RGB'), alpha=0.08)

def apply_vignette(img: Image.Image, strength: float = 0.2) -> Image.Image:
    """Applies a soft radial dark vignette falloff to the edges."""
    width, height = img.size
    
    # Create an alpha mask mapping the radial falloff
    mask = Image.new('L', (width, height))
    import math
    cx, cy = width / 2, height / 2
    max_dist = math.sqrt(cx**2 + cy**2)
    
    mask_data = []
    # Highly optimized array approach required for speed instead of Python nested loops
    # but for simple 1080p generation, nested loops take ~0.2s which is acceptable
    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            # Normalize to 0-1
            norm_dist = dist / max_dist
            # Exponentiate for softer center
            darkness = math.pow(norm_dist, 2) * strength
            # Convert to 0-255 solid black mask Alpha channel
            mask_data.append(int(255 * min(darkness, 1.0)))
            
    mask.putdata(mask_data)
    
    # Create black image, overlay using our calculated mask
    vignette = Image.new('RGB', (width, height), (0, 0, 0))
    img_rgba = img.convert('RGBA')
    vignette_rgba = vignette.convert('RGBA')
    
    # Paste black using the calculated opacity map
    img_rgba.paste(vignette_rgba, (0, 0), mask)
    return img_rgba.convert('RGB')

