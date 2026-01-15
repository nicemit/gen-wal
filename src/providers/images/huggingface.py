import os
import time
import requests
from src.interfaces import ImageProvider

class HuggingFaceImageProvider(ImageProvider):
    def __init__(self, model: str = "stabilityai/stable-diffusion-2-1", api_key: str = None, seed: int = None):
        self.model = model
        self.api_key = api_key
        self.seed = seed

    def get_image(self, prompt: str, width: int, height: int) -> str:
        cache_dir = os.path.expanduser("~/.cache/gen-wal")
        os.makedirs(cache_dir, exist_ok=True)
        filename = os.path.join(cache_dir, f"raw_bg_{int(time.time())}.jpg")

        if not self.api_key:
             print("Error: Hugging Face API Token required for images.")
             return ""

        url = f"https://api-inference.huggingface.co/models/{self.model}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # HF Inference API usually expects payload for text-to-image
        payload = {"inputs": prompt}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            # Check if it returned an error JSON
            if response.headers.get("content-type") == "application/json":
                print(f"HF Image Error: {response.json()}")
                return ""
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
            
        except Exception as e:
            print(f"Hugging Face Image Gen Error: {e}")
            return ""
