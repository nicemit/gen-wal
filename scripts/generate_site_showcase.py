#!/usr/bin/env python3
import os
import sys
import shutil

# Make sure we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import run_pipeline
import src.pipeline
from src.config import load_config
import src.wallpaper

def main():
    providers = [
        "mesh", 
        "flow", 
        "voronoi", 
        "reaction", 
        "waves", 
        "aurora", 
        "gradient", 
        "noise", 
        "ribbons", 
        "pollinations"
    ]
    
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'images', 'carousel'))
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"🖼️ Generating site showcase wallpapers in {out_dir}...")
    
    # Store the original function to restore it later
    original_set_wallpaper = src.wallpaper.set_wallpaper
    
    for p in providers:
        print(f"\n→ Generating for provider: {p}")
        
        # We define a custom set_wallpaper just for this iteration
        def custom_set(img_path):
            # Save it as {provider}.jpg or {provider}.png
            # For consistency with the site, we'll convert to jpg or just use jpg
            dest = os.path.join(out_dir, f"{p}.jpg")
            
            # The generated img_path might be .png, so we should convert it if needed
            # Using PIL to ensure it is saved as JPEG
            try:
                from PIL import Image
                with Image.open(img_path) as img:
                    # Convert to RGB if it has alpha channel (like PNG)
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    img.save(dest, "JPEG", quality=85)
                print(f"  ✅ Saved {dest}")
            except Exception as e:
                print(f"  ⚠️ Could not convert image to JPEG: {e}")
                # Fallback to copy
                dest_fallback = os.path.join(out_dir, f"{p}_fallback.jpg")
                shutil.copy(img_path, dest_fallback)
                print(f"  ✅ Copied {dest_fallback}")

        # Monkeypatch!
        # src.pipeline imports `set_wallpaper` directly (from src.wallpaper import set_wallpaper), 
        # so we must patch it directly in src.pipeline's namespace.
        src.pipeline.set_wallpaper = custom_set
        try:
            # We explicitly ask to not preview to avoid popups if any,
            run_pipeline(preview=False, overrides={
                'image_provider': p, 
                'quote_provider': 'pollinations:text',
                'seed': 'random', 
                'color_mode': 'vibrant',
                # Restructure to match exact provider name keys
                'pollinations:text': {
                    'api_key': 'sk_DEmGllK96evE5ipYzFxpDAvkofJGbQaZ',
                    'model': ['gemini-fast']
                },
                'pollinations': {
                    'image': {
                        'api_key': 'sk_DEmGllK96evE5ipYzFxpDAvkofJGbQaZ',
                        'model': ['flux', 'gptimage'],
                        'nologo': True
                    }
                }
            })
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            
    # Restore
    src.pipeline.set_wallpaper = original_set_wallpaper
    print(f"\n✅ Showcase generation complete!")

if __name__ == "__main__":
    main()
