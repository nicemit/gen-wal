from abc import ABC, abstractmethod
from typing import Optional

class QuoteProvider(ABC):
    @abstractmethod
    def get_quote(self, profile_content: str) -> str:
        """Generates or fetches a quote based on the user profile."""
        pass

class ProfileProvider(ABC):
    @abstractmethod
    def get_profile(self) -> str:
        """Fetches the user profile content as a string."""
        pass

class ImageProvider(ABC):
    @abstractmethod
    def get_image(self, prompt: str, width: int, height: int) -> str:
        """Generates or fetches an image based on the prompt. Returns file path."""
        pass

class TextProvider(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        pass
