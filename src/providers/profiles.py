import os
from src.interfaces import ProfileProvider

class LocalFileProfileProvider(ProfileProvider):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_profile(self) -> str:
        if not os.path.exists(self.file_path):
             return f"Profile not found at {self.file_path}. Please check configuration."
        
        try:
            with open(self.file_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading profile: {e}"
