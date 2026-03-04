from PIL import Image, ImageDraw
import os
from src.renderer import load_font, clean_text, wrap_text, draw_text_with_shadow, apply_overlay

class CenteredLayout:
    def __init__(self, config):
        pass
        
    @classmethod
    def name(cls):
        return "centered"

    def compose(self, background: Image.Image, quote: str, palette: dict, resolution: tuple) -> Image.Image:
        # Resize background if needed
        if background.size != resolution:
            background = background.resize(resolution, Image.Resampling.LANCZOS)
            
        background = apply_overlay(background, color=(0, 0, 0, 100))
        
        draw = ImageDraw.Draw(background)
        quote = clean_text(quote)
        
        font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'fonts', 'Inter.ttf')
        font_size = 48
        font = load_font(font_path, font_size)
        
        max_width = int(resolution[0] * 0.6) # Centered layouts can span a bit more
        
        lines = wrap_text(quote, font, max_width)
        total_height = len(lines) * (font_size * 1.5)
        
        # Center horizontally and vertically
        current_y = (resolution[1] - total_height) / 2
        
        text_color = palette.get('text_color', (255, 255, 255))
        shadow_color = palette.get('shadow_color', (0, 0, 0, 150))
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            
            x = (resolution[0] - line_width) / 2
            draw_text_with_shadow(draw, line, x, current_y, font, text_color, shadow_color)
            current_y += (font_size * 1.5)
            
        return background
