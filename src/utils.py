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

def list_profiles(profiles_dir):
    """List available profile files."""
    profiles = []
    if os.path.exists(profiles_dir):
        for root, _, files in os.walk(profiles_dir):
            for file in files:
                if file.endswith(".md"):
                    # Create a relative path prompt name (e.g. examples/stoic)
                    rel_path = os.path.relpath(os.path.join(root, file), profiles_dir)
                    name = os.path.splitext(rel_path)[0]
                    profiles.append(name)
    return sorted(profiles)

def update_config(config_path, key, value):
    """Update a specific key in the config file."""
    if not os.path.exists(config_path):
        print(f"Error: Config not found at {config_path}")
        return False

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
        
        # Handle nested keys if needed (simple for now)
        config[key] = value
        
        with open(config_path, 'w') as f:
            yaml.safe_dump(config, f, default_flow_style=False)
            
        return True
    except Exception as e:
        print(f"Error updating config: {e}")
        return False
