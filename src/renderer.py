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
