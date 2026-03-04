import os
import glob
import importlib

# Ensure the submodules are imported so the decorators/registration run
_imported = False

def auto_register():
    global _imported
    if _imported:
        return
        
    base_dir = os.path.dirname(__file__)
    
    # Import all modules in palettes, images, quotes
    for cat in ['palettes', 'images', 'quotes']:
        cat_dir = os.path.join(base_dir, cat)
        if os.path.isdir(cat_dir):
            for file in os.listdir(cat_dir):
                if file.endswith('.py') and not file.startswith('__'):
                    mod_name = f"src.providers.{cat}.{file[:-3]}"
                    try:
                        importlib.import_module(mod_name)
                    except Exception as e:
                        print(f"Warning: Failed to load provider module {mod_name} - {e}")
                        
    _imported = True

# Also export the base classes and registry functions
from .base import (
    BaseProvider, ImageProvider, QuoteProvider, PaletteProvider, 
    register_provider, get_provider, list_registered_providers
)
