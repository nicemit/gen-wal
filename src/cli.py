import argparse
import sys
import os
from src.config import load_config
from src.themes import list_themes, use_theme, edit_theme
from src.pipeline import run_pipeline

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
            import yaml
            print(yaml.dump(config, default_flow_style=False))
        elif getattr(args, 'subcommand', None) in ("edit", None):
            from src.config import CONFIG_PATH
            print(f"📝 Opening config file: {CONFIG_PATH}")
            editor = os.environ.get('EDITOR', 'nano')
            subprocess.run([editor, CONFIG_PATH])
    elif args.command == "seed":
        from src.seed import get_seed_info
        config = load_config()
        theme_name = config.get("theme", "minimal")
        seed_cfg = config.get("seed", "auto")
        info = get_seed_info(theme_name, seed_cfg)
        print(f"Current seed: {info['seed']}")
        print(f"Derived from: {info['derived']}")
    elif args.command == "schedule":
        import subprocess
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
            import os
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
            from src.providers import auto_register, list_registered_providers
            auto_register()
            providers = list_registered_providers()
            print("Registered Providers:")
            for category, items in providers.items():
                print(f"  {category.capitalize()}:")
                for item in items:
                    print(f"    - {item}")
    elif args.command == "history":
        from src.history import list_history, apply_history
        if getattr(args, 'subcommand', None) in ("list", None):
            list_history()
        elif args.subcommand == "apply":
            apply_history(args.index)
            
    elif args.command == "doctor":
        print("🩺 Running Gen-Wal Diagnostics...")
        import os
        from src.config import CONFIG_DIR, THEMES_DIR, HISTORY_DIR, CONFIG_PATH, load_config
        
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
