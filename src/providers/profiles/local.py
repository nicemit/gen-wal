import os
import yaml
from src.interfaces import ProfileProvider, ProfileData

class LocalFileProfileProvider(ProfileProvider):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_profile(self) -> ProfileData:
        if not os.path.exists(self.file_path):
             # Return error in content, empty metadata
             return ProfileData(content=f"Profile not found at {self.file_path}. Please check configuration.")
        
        try:
            with open(self.file_path, 'r') as f:
                content = f.read()

            metadata = {}
            profile_text = content

            # Check for Frontmatter (starts and ends with ---)
            if content.startswith("---"):
                try:
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        # parts[0] is empty, parts[1] is yaml, parts[2] is content
                        frontmatter_str = parts[1]
                        profile_text = parts[2].strip()
                        metadata = yaml.safe_load(frontmatter_str) or {}
                except Exception as e:
                    print(f"Warning: Failed to parse profile frontmatter: {e}")
            
            return ProfileData(content=profile_text, metadata=metadata)

        except Exception as e:
            return ProfileData(content=f"Error reading profile: {e}")
