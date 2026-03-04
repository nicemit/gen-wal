import os
from datetime import datetime
from src.config import load_config, HISTORY_DIR
from src.themes import load_theme
from src.env import collect_env_signals
from src.seed import generate_daily_seed
from src.providers import auto_register, get_provider
from src.layouts import get_layout
from src.wallpaper import set_wallpaper

def run_pipeline(preview=False):
    """Executes the deterministic wallpaper generation pipeline."""
    print("🚀 Starting Gen-Wal Pipeline...")
    
    # 1. Setup
    config = load_config()
    
    theme_name = config.get('theme', 'minimal')
    theme_hints, _ = load_theme(theme_name)
    
    env = collect_env_signals()
    seed_cfg = config.get('seed', 'auto')
    deterministic_seed = generate_daily_seed(theme_name, seed_cfg)
    
    print(f"  ➜ Theme: {theme_name}")
    print(f"  ➜ Seed : {deterministic_seed}")

    width = config.get('resolution', {}).get('width', 1920)
    height = config.get('resolution', {}).get('height', 1080)
    resolution = (width, height)

    # 2. Generation
    auto_register()
    
    palette_name = config.get('palette_provider', 'system_theme')
    quote_name = config.get('quote_provider', 'csv')
    image_name = config.get('image_provider', 'gradient')
    
    palette_prov = get_provider('palette', palette_name, config)
    quote_prov = get_provider('quote', quote_name, config)
    image_prov = get_provider('image', image_name, config)
    
    print("🎨 Generating Palette...")
    palette = palette_prov.generate(deterministic_seed, env, theme_hints)
    
    print("📝 Fetching Quote...")
    quote = quote_prov.generate(deterministic_seed, env, theme_hints)
    print(f"    > \"{quote}\"")
    
    print("🖼️  Generating Image...")
    # Some providers might need resolution
    base_image = image_prov.generate(deterministic_seed, env, theme_hints, width, height)
    
    # 3. Composition
    layout_name = config.get('layout', theme_hints.get('layout_hint', 'minimal'))
    print(f"📐 Applying Layout: {layout_name}...")
    layout_engine = get_layout(layout_name, config)
    final_image = layout_engine.compose(base_image, quote, palette, resolution)
    
    # 4. Storage
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date_str}_{theme_name}_{deterministic_seed}.jpg"
    if preview:
        output_path = f"/tmp/genwal_preview_{filename}"
    else:
        output_path = os.path.join(HISTORY_DIR, filename)
        
    final_image.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"💾 Saved to: {output_path}")
    
    # 5. Application
    if not preview:
        set_wallpaper(output_path)
    else:
        print("👀 Preview mode. OS wallpaper not changed.")
