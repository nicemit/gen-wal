import os
import glob
from src.config import HISTORY_DIR
from src.wallpaper import set_wallpaper

def get_history():
    """Returns a sorted list of generated wallpaper absolute paths."""
    if not os.path.exists(HISTORY_DIR):
        return []
        
    files = glob.glob(os.path.join(HISTORY_DIR, "*.jpg"))
    files.sort(key=os.path.getmtime, reverse=True)
    return files

def list_history():
    files = get_history()
    if not files:
        print("No generation history found.")
        return
        
    print(f"Recent generations (latest first):")
    for i, path in enumerate(files):
        filename = os.path.basename(path)
        print(f"  [{i}] {filename}")

def apply_history(index: int):
    files = get_history()
    if index < 0 or index >= len(files):
        print(f"❌ Invalid history index. Max is {len(files)-1}.")
        return False
        
    target_file = files[index]
    print(f"Re-applying wallpaper from history: {os.path.basename(target_file)}")
    set_wallpaper(target_file)
    return True
