import os
import time
import random
import requests
import urllib.parse
from src.interfaces import ImageProvider

class PollinationsImageProvider(ImageProvider):
    """
    Pollinations Image Provider Configuration:
    - Endpoint: https://gen.pollinations.ai/image/{prompt}
    - Prompt Strategy: URL-safe, seed passed as query parameter
    - Retries: Up to 3 attempts with exponential backoff
    - Models: default 'flux'
    """
    def __init__(self, model: str = "flux", nologo: bool = True, api_key: str = None, seed: int = None):
        self.model = model or "flux"
        self.nologo = nologo
        self.api_key = api_key
        self.seed = seed

    def get_image(self, prompt: str, width: int, height: int) -> str:
        
        cache_dir = os.path.expanduser("~/.cache/gen-wal")
        os.makedirs(cache_dir, exist_ok=True)
        filename = os.path.join(cache_dir, f"raw_bg_{int(time.time())}.jpg")
        
        seed = self.seed if self.seed is not None else random.randint(0, 1000000)
        
        # Ensure prompt is URL-safe encoded, seed passed as query param (not in prompt)
        safe_prompt = urllib.parse.quote(prompt)
        
        url = f"https://gen.pollinations.ai/image/{safe_prompt}"
        
        params = {
            "width": width,
            "height": height,
            "seed": seed,
            "nologo": str(self.nologo).lower(),
            "model": self.model
        }
            
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=params, headers=headers, timeout=120)
                response.raise_for_status()
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return filename
            except Exception as e:
                msg = str(e)
                if 'response' in locals() and hasattr(response, 'text'):
                    msg += f" | Body: {response.text}"
                elif hasattr(e, 'response') and e.response:
                    msg += f" | Body: {e.response.text}"
                print(f"Error fetching image (Attempt {attempt + 1}/{max_retries}): {msg}")
                if attempt == max_retries - 1:
                    return ""
                time.sleep(2 ** attempt)

        return ""
