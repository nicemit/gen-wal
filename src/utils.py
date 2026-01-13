import os
import yaml
import subprocess

def load_config(path="config.yaml"):
    if not os.path.exists(path):
        # Fallback to looking in parent directory or current directory if path is relative
        pass # Assume explicit path or current dir for now
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def set_wallpaper(image_path):
    # GNOME / Ubuntu
    uri = f"file://{os.path.abspath(image_path)}"
    try:
        # Set for both light and dark themes
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri], check=True)
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri], check=True)
        print(f"Wallpaper set to: {uri}")
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
