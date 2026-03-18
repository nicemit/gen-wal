import os
import json

# XDG Paths
XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
CONFIG_DIR = os.path.join(XDG_CONFIG_HOME, 'genwal')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.json')

XDG_DATA_HOME = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
THEMES_DIR = os.path.join(XDG_DATA_HOME, 'genwal', 'themes')

XDG_CACHE_HOME = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
HISTORY_DIR = os.path.join(XDG_CACHE_HOME, 'genwal', 'history')

PROVIDERS_DIR = os.path.join(XDG_DATA_HOME, 'genwal', 'providers')
# PROFILES_DIR deprecated and merged into THEMES_DIR

def ensure_provider_dirs():
    os.makedirs(os.path.join(PROVIDERS_DIR, 'images'), exist_ok=True)
    os.makedirs(os.path.join(PROVIDERS_DIR, 'palettes'), exist_ok=True)
    os.makedirs(os.path.join(PROVIDERS_DIR, 'quotes'), exist_ok=True)

def ensure_xdg_dirs():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(THEMES_DIR, exist_ok=True)
    os.makedirs(HISTORY_DIR, exist_ok=True)
    # PROFILES_DIR makedirs removed
    ensure_provider_dirs()

def load_config():
    ensure_xdg_dirs()
    if not os.path.exists(CONFIG_PATH):
        # Return fallback zero-key defaults
        return {
            "theme": "minimal",
            "layout": "minimal",
            "seed": "auto",
            "resolution": {"width": 1920, "height": 1080},
            "palette_provider": "system_theme",
            "image_provider": "mesh",
            "quote_provider": "csv"
        }
    with open(CONFIG_PATH, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def update_config(key, value):
    ensure_xdg_dirs()
    config = load_config()
    config[key] = value
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    return True
