# Contributing to Gen-Wal

Thanks for considering contributing! This is a personal project, but I love seeing how others use it.

## 🛠️ Development Setup

If you want to run Gen-Wal locally for development (without the systemd installer):

### 1. Clone & Setup
```bash
git clone https://github.com/nicemit/gen-wal.git
cd gen-wal

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration
Copy the example config to your XDG config directory:
```bash
mkdir -p ~/.config/genwal
cp config.example.json ~/.config/genwal/config.json
```

### 3. Running Manually
```bash
python3 main.py run      # Generate and apply wallpaper
python3 main.py preview  # Generate to /tmp only
python3 main.py config get  # Check current config
```

Wallpapers are saved to `~/.cache/genwal/history/`.

### 4. Running Tests
```bash
python3 -m unittest discover tests
```

---

## 📂 Project Structure

```
gen-wal/
├── src/
│   ├── cli.py           # CLI definition (argparse)
│   ├── pipeline.py      # Generation orchestrator
│   ├── config.py        # JSON config loader (XDG paths)
│   ├── themes.py        # Theme manager (Markdown → config macro)
│   ├── seed.py          # Deterministic seed system
│   ├── renderer.py      # Post-processing (vignette, grain)
│   ├── color/
│   │   └── strategies.py  # Seeded color theory transforms
│   ├── providers/
│   │   ├── images/      # mesh, gradient, noise, flow, voronoi, aurora, pollinations
│   │   ├── palettes/    # system_theme, theme_palette, random
│   │   └── quotes/      # csv, pollinations
│   └── layouts/         # minimal, centered
├── themes/              # Shipped theme presets (Markdown)
├── assets/fonts/        # Bundled fonts
├── scripts/
│   └── genwal-completion.bash  # Bash autocompletion
├── config.example.json  # Full annotated config reference
├── install.sh
└── uninstall.sh
```

---

## 🤝 How can I help?

1. **Add a Theme**: Created a cool "Cyberpunk" or "Nature" theme? Submit a PR adding it to `themes/`.
2. **Fix Bugs**: If something breaks on your distro (KDE, XFCE, Mate), fixes in `src/wallpaper.py` are welcome.
3. **Add Providers**: Want a new image generator or quote provider? See `src/providers/images/gradient.py` as a template.

## The Flow

1. Fork the repo.
2. Create your branch (`git checkout -b feature/amazing-theme`)
3. Commit your changes.
4. Open a Pull Request.

## Philosophy

- **Keep it simple**: No GUI, no database, no cloud accounts.
- **Local-first**: Everything works offline by default.
- **Single config**: All state lives in `~/.config/genwal/config.json`.
- **Deterministic**: Same seed, same wallpaper, every time.

Happy hacking! 🧠
