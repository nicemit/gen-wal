from src.providers.base import PaletteProvider, register_provider
import random

class SystemThemePaletteProvider(PaletteProvider):
    def __init__(self, config):
        pass
        
    @classmethod
    def name(cls):
        return "system_theme"
        
    def generate(self, seed: int, env: dict, theme_hints: dict) -> dict:
        rng = random.Random(seed)
        
        # Override with theme hints if present
        theme = theme_hints.get('palette_hint', env.get('system_theme', 'dark'))
        
        if theme == 'light':
            return {
                "text_color": (30, 30, 30),
                "shadow_color": (255, 255, 255),
                "accent_color": (rng.randint(50, 200), rng.randint(50, 200), rng.randint(50, 200))
            }
        elif theme == 'hacker':
             return {
                "text_color": (0, 255, 0),
                "shadow_color": (0, 50, 0),
                "accent_color": (0, 200, 0)
            }
        else: # dark default
            return {
                "text_color": (240, 240, 240),
                "shadow_color": (10, 10, 10),
                "accent_color": (rng.randint(100, 255), rng.randint(100, 255), rng.randint(100, 255))
            }

register_provider('palette', SystemThemePaletteProvider)
