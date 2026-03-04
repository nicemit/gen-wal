import os
import subprocess

def set_wallpaper(image_path: str):
    """Sets the OS wallpaper. (Simplified from existing utils.py)"""
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
    
    if "GNOME" in desktop or "Unity" in desktop or "ubuntu" in desktop.lower():
        uri = f"file://{os.path.abspath(image_path)}"
        try:
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-options", "zoom"], check=True)
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri], check=True)
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri], check=True)
            print(f"✅ OS Wallpaper updated: {uri}")
        except Exception as e:
            print(f"❌ Error setting OS wallpaper: {e}")
    else:
        print(f"⚠️ OS '{desktop}' wallpaper setting not fully supported yet.")
