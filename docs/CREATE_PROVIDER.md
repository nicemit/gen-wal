# Creating User Providers (BYOA)

Gen-Wal supports **Bring Your Own Algorithm (BYOA)**. You can easily add your own algorithms to generate wallpapers, color palettes, or quotes by simply placing a `.py` file into the plugin directories.

## Installation Location

genwal automatically discovers user providers placed in standard XDG data directories:

- Images: `~/.local/share/genwal/providers/images/`
- Palettes: `~/.local/share/genwal/providers/palettes/`
- Quotes: `~/.local/share/genwal/providers/quotes/`

## Creating a Provider

The easiest way to start is using the CLI to scaffold a template:

```bash
# Creates an image provider template named 'nebula'
genwal provider create image nebula

# Creates a quote provider template named 'myquotes'
genwal provider create quote myquotes
```

This will generate a fully runnable `.py` file in the correct directory. You can test your new provider immediately:

```bash
genwal preview --provider nebula
```

## Provider Interface

All providers inherit from base classes (`ImageProvider`, `PaletteProvider`, `QuoteProvider`) and implement two main methods.

### Example: Image Provider

```python
from src.providers.base import ImageProvider, register_provider
from PIL import Image

class NebulaProvider(ImageProvider):
    def __init__(self, config):
        # Save config if needed for later
        self.config = config

    @classmethod
    def name(cls):
        # This is the string used in config keys and CLI arguments
        return "nebula"

    def generate(self, seed: int, env: dict, theme_hints: dict, width: int = 1920, height: int = 1080):
        """
        Generate your visual here. 
        You must return a PIL Image object.
        """
        # env['palette'] contains the generated color palette for this run
        bg_color = env.get('palette', {}).get('background', '#000000')
        
        # ... logic using PRNG seeded with the `seed` argument ...
        
        img = Image.new('RGB', (width, height), color=bg_color)
        return img

# IMPORTANT: Always register your provider at the bottom of the file!
register_provider("image", NebulaProvider, origin="user")
```

## Available Context

When your `generate()` method is called, Gen-Wal passes context to ensure your provider reacts smoothly to the user's environment and themes.

- **`seed`**: A deterministic integer. If you use `random` or noise functions, seed them with this value to ensure the wallpaper stays the same all day but changes tomorrow!
- **`env`**: A dictionary containing signals, including the active `palette` generated just moments before your image provider was called.
- **`theme_hints`**: High-level configuration options defined by the active theme (e.g., `"palette_hint": "dark"`, `"noise.opacity": 0.5`). 

## Minimal Example Provider

To see a complete, minimal example, check out `examples/providers/spiral.py` in the repository.

You can copy this file directly into your user provider directory to try it out:

```bash
cp examples/providers/spiral.py ~/.local/share/genwal/providers/images/
genwal preview --provider spiral
```
