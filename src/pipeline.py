import os
from datetime import datetime
from src.config import load_config, HISTORY_DIR
from src.env import collect_env_signals
from src.seed import generate_daily_seed, derive_seed
from src.providers import auto_register, get_provider
from src.layouts import get_layout
from src.wallpaper import set_wallpaper

def run_pipeline(preview=False):
    """Executes the deterministic wallpaper generation pipeline."""
    print("🚀 Starting Gen-Wal Pipeline...")
    
    # 1. Setup
    config = load_config()
    
    theme_name = config.get('theme', 'minimal')
    theme_hints = config # The config IS the theme now
    
    env = collect_env_signals()
    seed_cfg = config.get('seed', 'auto')
    base_seed = generate_daily_seed(theme_name, seed_cfg)
    
    color_seed = derive_seed(base_seed, "color")
    pattern_seed = derive_seed(base_seed, "pattern")
    layout_seed = derive_seed(base_seed, "layout")
    
    width = config.get('resolution', {}).get('width', 1920)
    height = config.get('resolution', {}).get('height', 1080)
    resolution = (width, height)

    # 2. Generation
    auto_register()
    
    palette_name = config.get('palette_provider', 'system_theme')
    quote_name = config.get('quote_provider', 'csv')
    image_name = config.get('image_provider', 'gradient')
    color_mode = config.get('color_mode', 'balanced')
    layout_name = config.get('layout', config.get('layout_hint', 'minimal'))

    print(f"  ➜ Theme    : {theme_name}")
    print(f"  ➜ Seed     : {base_seed} ({seed_cfg})")
    print(f"  ➜ Image    : {image_name}")
    print(f"  ➜ Palette  : {palette_name}")
    print(f"  ➜ Quotes   : {quote_name}")
    print(f"  ➜ Layout   : {layout_name}")
    print(f"  ➜ Color    : {color_mode}")
    print(f"  ➜ Canvas   : {width}×{height}")
    
    palette_prov = get_provider('palette', palette_name, config)
    quote_prov = get_provider('quote', quote_name, config)
    image_prov = get_provider('image', image_name, config)
    
    print("🎨 Generating Palette...")
    base_palette = palette_prov.generate(base_seed, env, theme_hints)
    
    from src.color.strategies import apply_strategy, compute_color_strategy
    strategy = compute_color_strategy(color_mode, color_seed)
    print(f"  ➜ Color Strategy: {strategy}")
    palette = apply_strategy(base_palette, strategy, color_seed)
    
    # CRITICAL: Overwrite the env palette so Image Providers pull the modified seeded colors!
    env['palette'] = palette
    
    print("📝 Fetching Quote...")
    quote = quote_prov.generate(base_seed, env, theme_hints)
    print(f"    > \"{quote}\"")
    
    print("🖼️  Generating Image...")
    # Providers consume pattern_seed for geometric/random visual variation
    base_image = image_prov.generate(pattern_seed, env, theme_hints, width, height)
    
    print("✨ Applying Post-Processing Enhancements...")
    from src.renderer import apply_grain, apply_vignette
    base_image = apply_vignette(base_image, strength=0.2)
    base_image = apply_grain(base_image, seed=pattern_seed, strength=8)
    
    # 3. Composition
    print(f"📐 Applying Layout: {layout_name}...")
    layout_engine = get_layout(layout_name, config)
    final_image = layout_engine.compose(base_image, quote, palette, resolution)
    
    # 4. Storage
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date_str}_{theme_name}_{base_seed}.jpg"
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
