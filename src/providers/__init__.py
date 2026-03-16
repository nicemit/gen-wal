import os
import glob
import importlib
import importlib.util
from src.config import PROVIDERS_DIR

# Ensure the submodules are imported so the decorators/registration run
_imported = False

def auto_register():
    global _imported
    if _imported:
        return
        
    import src.providers.base as base_module
    
    # 1. Discover Built-In Providers
    base_module._CURRENT_REGISTER_ORIGIN = "builtin"
    base_dir = os.path.dirname(__file__)
    for cat in ['palettes', 'images', 'quotes']:
        cat_dir = os.path.join(base_dir, cat)
        if os.path.isdir(cat_dir):
            for file in os.listdir(cat_dir):
                if file.endswith('.py') and not file.startswith('__'):
                    mod_name = f"src.providers.{cat}.{file[:-3]}"
                    try:
                        importlib.import_module(mod_name)
                    except Exception as e:
                        print(f"Warning: Failed to load built-in provider {mod_name} - {e}")
                        
    # 2. Discover User Providers
    base_module._CURRENT_REGISTER_ORIGIN = "user"
    for cat in ['palettes', 'images', 'quotes']:
        user_cat_dir = os.path.join(PROVIDERS_DIR, cat)
        if os.path.isdir(user_cat_dir):
            for file in os.listdir(user_cat_dir):
                if file.endswith('.py') and not file.startswith('__'):
                    file_path = os.path.join(user_cat_dir, file)
                    mod_name = f"user_plugin_{cat}_{file[:-3]}"
                    try:
                        spec = importlib.util.spec_from_file_location(mod_name, file_path)
                        if spec and spec.loader:
                            mod = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(mod)
                    except Exception as e:
                        print(f"Warning: Failed to load user provider {file_path} - {e}")

    # Reset origin to builtin just in case
    base_module._CURRENT_REGISTER_ORIGIN = "builtin"
    _imported = True

# Also export the base classes and registry functions
from .base import (
    BaseProvider, ImageProvider, QuoteProvider, PaletteProvider, 
    register_provider, get_provider, list_registered_providers
)
