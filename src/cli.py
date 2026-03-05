import argparse
import sys
import os
import subprocess

# Guarantee Python can resolve "src.*" when this file is executed directly by systemd/bash wrappers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from src.config import load_config
from src.themes import list_themes, use_theme, edit_theme
from src.pipeline import run_pipeline
from src.seed import get_seed_info
from src.providers import auto_register, list_registered_providers
from src.history import list_history, apply_history

def main():
    parser = argparse.ArgumentParser(description="Gen-Wal: Deterministic Generative Wallpaper Daemon")
    subparsers = parser.add_subparsers(dest="command")

    # genwal run
    run_parser = subparsers.add_parser("run", help="Run full pipeline execution")
    
    # genwal preview
    preview_parser = subparsers.add_parser("preview", help="Generate to tmp, do not apply to OS")

    # genwal theme
    theme_parser = subparsers.add_parser("theme", help="Manage themes")
    theme_sub = theme_parser.add_subparsers(dest="subcommand")
    theme_sub.add_parser("list", help="List available themes")
    use_parser = theme_sub.add_parser("use", help="Switch active theme in config")
    use_parser.add_argument("name", help="Theme name to use")
    edit_parser = theme_sub.add_parser("edit", help="Open theme file in editor")
    edit_parser.add_argument("name", help="Theme name to edit")

    # genwal config
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_sub = config_parser.add_subparsers(dest="subcommand")
    config_sub.add_parser("edit", help="Edit settings easily")
    config_sub.add_parser("show", help="Print current active configuration")

    # genwal schedule
    schedule_parser = subparsers.add_parser("schedule", help="Manage daemon scheduling")
    schedule_sub = schedule_parser.add_subparsers(dest="subcommand")
    set_parser = schedule_sub.add_parser("set", help="Interacts with systemd timer")
    set_parser.add_argument("time", help="Time in HH:MM format")
    schedule_sub.add_parser("show", help="View timer status")
    schedule_sub.add_parser("disable", help="Stop the timer")

    # genwal providers
    providers_parser = subparsers.add_parser("providers", help="Manage providers")
    providers_sub = providers_parser.add_subparsers(dest="subcommand")
    providers_sub.add_parser("list", help="Show available providers")

    # genwal history
    history_parser = subparsers.add_parser("history", help="Manage generated history")
    history_sub = history_parser.add_subparsers(dest="subcommand")
    history_sub.add_parser("list", help="List generated wallpapers") # default behavior of history
    apply_parser = history_sub.add_parser("apply", help="Re-apply past history entry")
    apply_parser.add_argument("index", type=int, help="Index of history entry to apply")

    # genwal seed
    subparsers.add_parser("seed", help="Prints current active deterministic seed details")

    # genwal palette
    palette_parser = subparsers.add_parser("palette", help="Manage color palettes")
    palette_sub = palette_parser.add_subparsers(dest="subcommand")
    palette_sub.add_parser("preview", help="Preview 5 deterministic color palette variations")

    # genwal doctor
    subparsers.add_parser("doctor", help="Validation and environment checks")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    if args.command == "run":
        run_pipeline(preview=False)
    elif args.command == "preview":
        run_pipeline(preview=True)
    elif args.command == "theme":
        if args.subcommand == "list":
            list_themes()
        elif args.subcommand == "use":
            use_theme(args.name)
        elif args.subcommand == "edit":
            edit_theme(args.name)
    elif args.command == "config":
        if getattr(args, 'subcommand', None) == "show":
            config = load_config()
            print(json.dumps(config, indent=2))
        elif getattr(args, 'subcommand', None) in ("edit", None):
            from src.config import CONFIG_PATH
            print(f"📝 Opening config file: {CONFIG_PATH}")
            editor = os.environ.get('EDITOR', 'nano')
            subprocess.run([editor, CONFIG_PATH])
    elif args.command == "seed":
        config = load_config()
        theme_name = config.get("theme", "minimal")
        seed_cfg = config.get("seed", "auto")
        info = get_seed_info(theme_name, seed_cfg)
        print(f"Current seed: {info['seed']}")
        print(f"Derived from: {info['derived']}")
    elif args.command == "schedule":
        if args.subcommand == "show":
            print("🗓️  Schedule Status:")
            subprocess.run(["systemctl", "--user", "status", "gen-wal.timer"])
        elif args.subcommand == "disable":
            print("🛑 Disabling schedule...")
            subprocess.run(["systemctl", "--user", "disable", "--now", "gen-wal.timer"])
        elif args.subcommand == "set":
            time_str = args.time
            print(f"⏰ Reconfiguring schedule for {time_str}...")
            # Ideally this writes to the systemd unit, but for MVP we match what install.sh does
            timer_dir = os.path.expanduser("~/.config/systemd/user")
            timer_file = os.path.join(timer_dir, "gen-wal.timer")
            
            content = f"""[Unit]
Description=Run Gen-Wal daily at {time_str}

[Timer]
OnCalendar=*-*-* {time_str}:00
Persistent=true

[Install]
WantedBy=timers.target
"""
            os.makedirs(timer_dir, exist_ok=True)
            with open(timer_file, 'w') as f:
                f.write(content)
            
            subprocess.run(["systemctl", "--user", "daemon-reload"])
            subprocess.run(["systemctl", "--user", "enable", "--now", "gen-wal.timer"])
            print("✅ Schedule updated.")
            
    elif args.command == "providers":
        if args.subcommand == "list":
            auto_register()
            providers = list_registered_providers()
            print("Registered Providers:")
            for category, items in providers.items():
                print(f"  {category.capitalize()}:")
                for item in items:
                    print(f"    - {item}")
    elif args.command == "history":
        if getattr(args, 'subcommand', None) in ("list", None):
            list_history()
        elif args.subcommand == "apply":
            apply_history(args.index)
            
    elif args.command == "palette":
        if args.subcommand == "preview":
            from src.env import collect_env_signals
            from src.themes import load_theme
            from src.seed import generate_daily_seed, derive_seed
            from src.providers import get_provider
            from src.color.strategies import apply_strategy, compute_color_strategy
            from PIL import Image, ImageDraw
            
            config = load_config()
            theme_name = config.get('theme', 'minimal')
            theme_hints, _ = load_theme(theme_name)
            env = collect_env_signals()
            auto_register()
            palette_name = config.get('palette_provider', 'system_theme')
            palette_prov = get_provider('palette', palette_name, config)
            color_mode = config.get('color_mode', 'balanced')

            seed_cfg = config.get('seed', 'auto')
            base_seed = generate_daily_seed(theme_name, seed_cfg)

            print(f"🎨 Palette Preview (Theme: {theme_name}, Mode: {color_mode})")
            
            out_dir = "/tmp/genwal_palette_preview"
            os.makedirs(out_dir, exist_ok=True)
            
            for i in range(5):
                iter_base_seed = derive_seed(base_seed, f"iter_{i}")
                color_seed = derive_seed(iter_base_seed, "color")
                
                base_palette = palette_prov.generate(iter_base_seed, env, theme_hints)
                strategy = compute_color_strategy(color_mode, color_seed)
                palette = apply_strategy(base_palette, strategy, color_seed)
                
                bg = palette.get("background", "#000000")
                sec = palette.get("secondary", "#555555")
                acc = palette.get("accent", "#ffffff")
                
                print(f"\nVariation {i+1} [{strategy}]:")
                print(f"  Background : {bg}")
                print(f"  Secondary  : {sec}")
                print(f"  Accent     : {acc}")
                
                img = Image.new('RGB', (300, 100))
                draw = ImageDraw.Draw(img)
                def h2rgb(h):
                    if not h: return (0,0,0)
                    h = h.lstrip('#')
                    return tuple(int(h[j:j+2], 16) for j in (0, 2, 4))
                
                draw.rectangle([0, 0, 100, 100], fill=h2rgb(bg))
                draw.rectangle([100, 0, 200, 100], fill=h2rgb(sec))
                draw.rectangle([200, 0, 300, 100], fill=h2rgb(acc))
                
                out_path = os.path.join(out_dir, f"preview_{i+1}_{strategy}.png")
                img.save(out_path)
                print(f"  saved -> {out_path}")
            
    elif args.command == "doctor":
        print("🩺 Running Gen-Wal Diagnostics...")
        from src.config import CONFIG_DIR, THEMES_DIR, HISTORY_DIR, CONFIG_PATH
        
        print("\n📂 Directories:")
        print(f"  Config:  {CONFIG_DIR} {'✅' if os.path.exists(CONFIG_DIR) else '❌'}")
        print(f"  Themes:  {THEMES_DIR} {'✅' if os.path.exists(THEMES_DIR) else '❌'}")
        print(f"  History: {HISTORY_DIR} {'✅' if os.path.exists(HISTORY_DIR) else '❌'}")
        
        print("\n⚙️  Configuration:")
        print(f"  Path: {CONFIG_PATH} {'✅' if os.path.exists(CONFIG_PATH) else '⚠️ (Using Defaults)'}")
        try:
            cfg = load_config()
            print(f"  Theme: {cfg.get('theme', 'minimal')}")
            print(f"  Seed Mode: {cfg.get('seed', 'auto')}")
        except Exception as e:
            print(f"  ❌ Failed to parse config: {e}")
            
        print("\n✨ Ready. Fix any ❌ marks manually or by running 'install.sh' again.")
        
    else:
        print(f"Executing placeholder: {args.command}")

if __name__ == "__main__":
    main()
