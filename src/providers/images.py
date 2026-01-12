import os
import random
import requests
import time
from src.interfaces import ImageProvider

class PollinationsImageProvider(ImageProvider):
    def __init__(self, model: str = None, nologo: bool = True, api_key: str = None):
        self.model = model
        self.nologo = nologo
        self.api_key = api_key

    def get_image(self, prompt: str, width: int, height: int) -> str:
        # Encode prompt slightly? Pollinations handles raw text well.
        # We want to save the image to cache
        cache_dir = os.path.expanduser("~/.cache/gen-wal")
        os.makedirs(cache_dir, exist_ok=True)
        filename = os.path.join(cache_dir, f"raw_bg_{int(time.time())}.jpg")
        
        # Pollinations API: https://image.pollinations.ai/prompt/{prompt}?width={width}&height={height}
        # Ideally we should clean the prompt to be URL safe-ish, butrequests handles most
        # Add random seed to ensure freshness even with same prompt
        seed = random.randint(0, 1000000)
        url = f"https://image.pollinations.ai/prompt/{prompt}?width={width}&height={height}&seed={seed}"
        if self.nologo:
            url += "&nologo=true"
        if self.model:
            url += f"&model={self.model}"
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}" # Assuming Bearer token standard
        
        try:
            response = requests.get(url, headers=headers, timeout=120)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
        except Exception as e:
            print(f"Error fetching image: {e}")
            return ""

class LocalDirImageProvider(ImageProvider):
    def __init__(self, directory: str):
        self.directory = directory

    def get_image(self, prompt: str, width: int, height: int) -> str:
        if not os.path.exists(self.directory):
             return ""
        
        valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        images = [
            os.path.join(self.directory, f) 
            for f in os.listdir(self.directory) 
            if os.path.splitext(f)[1].lower() in valid_extensions
        ]
        
        if not images:
            return ""
            
        return random.choice(images)
