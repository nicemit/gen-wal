import os
import random
from src.interfaces import ImageProvider

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
