from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import os

class WallpaperRenderer:
    def __init__(self, font_path: str = None, font_size: int = 60):
        self.font_path = font_path or self._find_default_font()
        self.font_size = font_size

    def _find_default_font(self) -> str:
        # Common linux paths
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return "arial.ttf" # Fallback, might fail if not present but PIL default is tiny

    def compose(self, image_path: str, text: str, output_path: str, position: str = "center", padding: int = 100, target_size: tuple = None):
        try:
            img = Image.open(image_path).convert("RGBA")
            
            # Resize if target_size is provided and doesn't match
            if target_size and img.size != target_size:
                print(f"Resizing image from {img.size} to {target_size}")
                img = img.resize(target_size, Image.Resampling.LANCZOS)
            
            # 2. Add Dark Overlay for readability
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 100)) # Semi-transparent black
            img = Image.alpha_composite(img, overlay)
            
            # 3. Draw Text
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype(self.font_path, self.font_size)
            except IOError:
                font = ImageFont.load_default()
                # print("Warning: Could not load font, using default.")

            # Wrap text
            # Estimate chars per line based on width (very rough)
            # Use a slightly narrower width for corner positions to look better
            available_width = img.width - (2 * padding)
            
            # Aesthetic choice: Don't let text span more than 70% of width usually
            max_aesthetic_width = img.width * 0.7
            available_width = min(available_width, max_aesthetic_width)
            
            # Rough estimation of char width (0.6 of font size is a common heuristic)
            avg_char_width = self.font_size * 0.5
            chars_per_line = int(available_width / avg_char_width)
            
            lines = textwrap.wrap(text, width=chars_per_line)
            
            # Calculate total text height
            line_height = self.font_size * 1.5
            total_text_height = len(lines) * line_height
            
            # Calculate Starting Y based on position
            start_y = 0
            if "top" in position:
                start_y = padding
            elif "bottom" in position:
                start_y = img.height - padding - total_text_height
            else: # center
                start_y = (img.height - total_text_height) / 2
                
            current_y = start_y
            
            for line in lines:
                # Calculate X based on position
                text_bbox = draw.textbbox((0, 0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                
                x = 0
                if "left" in position:
                    x = padding
                elif "right" in position:
                    x = img.width - padding - text_width
                else: # center or top/bottom center
                    x = (img.width - text_width) / 2
                
                # Draw Shadow/Outline
                
                # Draw Shadow/Outline
                shadow_offset = 2
                draw.text((x+shadow_offset, current_y+shadow_offset), line, font=font, fill=(0,0,0,200))
                
                # Draw Text
                draw.text((x, current_y), line, font=font, fill=(255, 255, 255, 255))
                
                current_y += line_height
                
            img = img.convert("RGB")
            img.save(output_path, "JPEG")
            return output_path
            
        except Exception as e:
            print(f"Error rendering image: {e}")
            return None
