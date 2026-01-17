import os
import time
import random
import requests
import urllib.parse
from src.interfaces import ImageProvider

class PollinationsImageProvider(ImageProvider):
    def __init__(self, model: str = None, nologo: bool = True, api_key: str = None, seed: int = None):
        self.model = model
        self.nologo = nologo
        self.api_key = api_key
        self.seed = seed

    def get_image(self, prompt: str, width: int, height: int) -> str:
        
        cache_dir = os.path.expanduser("~/.cache/gen-wal")
        os.makedirs(cache_dir, exist_ok=True)
        filename = os.path.join(cache_dir, f"raw_bg_{int(time.time())}.jpg")
        
        safe_prompt = urllib.parse.quote(prompt)
        seed = self.seed if self.seed is not None else random.randint(0, 1000000)
        
        if self.api_key:
            url = f"https://gen.pollinations.ai/image/{safe_prompt}"
        else:
            url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
        
        params = {
            "width": width,
            "height": height,
            "seed": seed,
            "nologo": str(self.nologo).lower()
        }
        
        if self.model:
            params["model"] = self.model
            
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=120)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
        except Exception as e:
            print(f"Error fetching image: {e}")
            return ""
