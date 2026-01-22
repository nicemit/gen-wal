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

    def _clean_text(self, text: str) -> str:
        """Removes markdown formatting and surrounding quotes for cleaner wallpaper text."""
        import re
        # Remove bold/italic markers
        clean = re.sub(r'(\*\*|__)', '', text)
        clean = re.sub(r'(\*|_)', '', clean)
        
        # Remove surrounding quotes if they exist
        clean = clean.strip()
        if (clean.startswith('"') and clean.endswith('"')) or (clean.startswith("'") and clean.endswith("'")):
            clean = clean[1:-1]
            
        return clean.strip()

    def compose(self, image_path: str, text: str, output_path: str, position: str = "center", padding: int = 100, target_size: tuple = None, watermark_config: dict = None):
        # Clean text first
        text = self._clean_text(text)
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
                
            # 4. Draw Watermark
            if watermark_config and watermark_config.get('enabled', False):
                wm_text = watermark_config.get('text', '')
                if wm_text:
                    wm_size = watermark_config.get('font_size', 20)
                    wm_dpos = watermark_config.get('position', 'bottom_right')
                    wm_opacity = watermark_config.get('opacity', 150)
                    # wm_color is ignoring for now, defaulting to white with alpha
                    
                    try:
                        wm_font = ImageFont.truetype(self.font_path, wm_size)
                    except:
                        wm_font = ImageFont.load_default()
                        
                    wm_bbox = draw.textbbox((0, 0), wm_text, font=wm_font)
                    wm_width = wm_bbox[2] - wm_bbox[0]
                    wm_height = wm_bbox[3] - wm_bbox[1]
                    
                    wm_x, wm_y = 0, 0
                    wm_padding = 40 # Padding from edge
                    
                    if 'bottom' in wm_dpos:
                        wm_y = img.height - wm_height - wm_padding
                    elif 'top' in wm_dpos:
                        wm_y = wm_padding
                    else: # center y
                        wm_y = (img.height - wm_height) / 2
                        
                    if 'right' in wm_dpos:
                        wm_x = img.width - wm_width - wm_padding
                    elif 'left' in wm_dpos:
                        wm_x = wm_padding
                    else: # center x
                        wm_x = (img.width - wm_width) / 2
                    
                    # Draw Rounded Background
                    box_padding = 10
                    box_x0 = wm_x - box_padding
                    box_y0 = wm_y - box_padding
                    box_x1 = wm_x + wm_width + box_padding
                    box_y1 = wm_y + wm_height + (box_padding * 0.5) # Slight optical adjustment
                    
                    # Create overlay for the box to handle transparency
                    box_overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
                    box_draw = ImageDraw.Draw(box_overlay)
                    
                    # Background color: White with very low opacity (e.g. 10-20% of text opacity)
                    # Or same opacity as requested? User asked for "same transparency".
                    # Let's use the provided opacity for the border/fill.
                    
                    # Draw rounded rect
                    box_draw.rounded_rectangle(
                        [(box_x0, box_y0), (box_x1, box_y1)], 
                        radius=4, 
                        fill=(0, 0, 0, int(wm_opacity * 0.5)), # darker background, 50% of text opacity
                        outline=(255, 255, 255, int(wm_opacity * 0.3)), # faint border
                        width=1
                    )
                    
                    # Composite the box
                    img = Image.alpha_composite(img, box_overlay)
                    
                    # Re-create draw object for text on top of new layer
                    draw = ImageDraw.Draw(img)

                    # Draw Watermark Text
                    draw.text((wm_x, wm_y), wm_text, font=wm_font, fill=(255, 255, 255, wm_opacity))

            img = img.convert("RGB")
            img.save(output_path, "JPEG")
            return output_path
            
        except Exception as e:
            print(f"Error rendering image: {e}")
            return None
