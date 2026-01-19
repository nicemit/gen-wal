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
    # Detect Desktop Environment
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
    
    # GNOME / Unity / Ubuntu
    if "GNOME" in desktop or "Unity" in desktop or "ubuntu" in desktop.lower():
        uri = f"file://{os.path.abspath(image_path)}"
        try:
            # Force options to 'zoom' to ensure rendering
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-options", "zoom"], check=True)
            
            # Check current URI to force refresh if identical
            current_uri = subprocess.check_output(
                ["gsettings", "get", "org.gnome.desktop.background", "picture-uri"], 
                text=True
            ).strip().strip("'")
            
            if current_uri == uri:
                # Toggle to empty to force a reload event
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", ""], check=True)
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", ""], check=True)
            
            # Set for both light and dark themes
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri], check=True)
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri], check=True)
            
            print(f"Wallpaper set to: {uri} (DE: {desktop})")
        except Exception as e:
            print(f"Error setting wallpaper: {e}")
    else:
        # Fallback (Future: Add feh/nitrogen support)
        print(f"Desktop '{desktop}' not fully supported yet. Wallpaper generated at: {image_path}")
