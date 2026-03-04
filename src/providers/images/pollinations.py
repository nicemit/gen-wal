import urllib.request
import urllib.parse
from io import BytesIO
from PIL import Image
from src.providers.base import ImageProvider, register_provider

class PollinationsImageProvider(ImageProvider):
    def __init__(self, config):
        self.config = config
        
    @classmethod
    def name(cls):
        return "pollinations:image"
        
    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080) -> Image.Image:
        style = theme_hints.get('palette_hint', 'dark abstract')
        
        # We need a prompt for the image. 
        # For a truly extensible system, we might chain providers,
        # but for now we generate a prompt based on the theme hint.
        base_prompt = f"Abstract beautiful subtle wallpaper background. {style}. high quality, 4k."
        prompt = urllib.parse.quote(base_prompt)
        
        url = f"https://image.pollinations.ai/prompt/{prompt}?width={width}&height={height}&nologo=true&seed={seed}"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Gen-Wal/1.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                img_data = response.read()
                return Image.open(BytesIO(img_data)).convert('RGB')
        except Exception as e:
            print(f"Warning: Pollinations image failed ({e}), falling back to gradient...")
            from src.providers.images.gradient import GradientImageProvider
            fallback = GradientImageProvider({})
            return fallback.generate(seed, env, theme_hints, width, height)

register_provider('image', PollinationsImageProvider)
