# Gen-Wal 🧠

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge&logo=github)

A **personal experiment in ambient computing**.

Gen-Wal explores a simple question:

> What if the desktop itself could act as a passive environmental cue — instead of another app, notification, or dashboard?

---

## What this is NOT

Gen-Wal is **not**:
- a productivity app
- a motivational tool
- a notification system
- a dashboard or tracker

There is nothing to click.
Nothing to dismiss.
Nothing to optimize.

---

## The Experiment

I spend a large portion of my day in front of my machine. Keeping goals in my head wasn't enough, but I also didn't want yet another app demanding attention.

Gen-Wal changes **one visual element of the environment** once per day.

Quietly.

It uses a *theme* (a simple text file describing a mindset or focus) and generates a daily background that acts as a passive reference frame — something you see repeatedly without being interrupted.

This is not meant to push behavior. It's meant to **exist**.

---

## What It Is

Gen-Wal is a small local daemon written in Python that:

- Reads a text-based theme (e.g. Stoic, Builder, Terminal) and applies it to `config.json`
- Generates a short quote using a local CSV or remote AI provider
- Generates a matching procedural background image (mesh, voronoi, gradient, flow, aurora…)
- Applies post-processing effects (vignette, grain)
- Updates the desktop wallpaper automatically via systemd

You can use it, modify it, or ignore it.

---

## Privacy & Local Execution

**Gen-Wal runs as a local daemon.** It has no accounts, no analytics, and no tracking code.

- **Default**: Fully local procedural image generation. No network required.
- **Optional**: Can use remote APIs (Pollinations.ai, Ollama) for AI-generated quotes and images.

You control where the data goes.

---

## Installation

One-line install for Linux (GNOME / KDE / Unity):

```bash
curl -sL https://gen-wal.laptopserver.dev/install | bash
```

This sets up:

- The `genwal` CLI (installed to `~/.local/bin/genwal`)
- A systemd timer (daily update, configurable)
- XDG-compliant data directories
- Bash autocompletion (including dynamic config key suggestions)

---

## Configuration

All configuration lives in a single JSON file at `~/.config/genwal/config.json`.

You can edit it directly, or use the CLI:

```bash
genwal config edit             # Open in $EDITOR
genwal config get              # Print entire config as JSON
genwal config get seed         # Print a specific key
genwal config set seed random  # Set a key (supports dot notation)
genwal config set noise.opacity 0.4
```

Key config options with their valid values:

```json
{
  "theme": "stoic",
  "seed": "auto",
  "color_mode": "balanced",
  "image_provider": "mesh",
  "palette_provider": "system_theme",
  "quote_provider": "csv",
  "layout": "minimal",
  "resolution": { "width": 1920, "height": 1080 }
}
```

| Key | Options |
|---|---|
| `seed` | `auto`, `random` |
| `image_provider` | `mesh`, `gradient`, `noise`, `flow`, `voronoi`, `aurora`, `pollinations` |
| `color_mode` | `minimal`, `balanced`, `vibrant`, `wild` |
| `layout` | `minimal`, `centered` |
| `palette_provider` | `system_theme`, `theme_palette`, `random` |
| `quote_provider` | `csv`, `pollinations` |

---

## Themes (Mindsets)

Themes are not just aesthetic tweaks — they define **mental reference frames**.

Running `genwal theme use <name>` applies the theme's preset values directly into your `config.json` as a one-time macro. The pipeline runs entirely off the JSON, with no runtime file parsing.

Included themes:

- **stoic** — *Restraint, impermanence, control*
- **minimal** — *Clean, understated, clear*
- **terminal** — *Code, craft, iteration*

---

## Create Your Own Theme

Themes are Markdown files stored in `~/.local/share/genwal/themes/`.

```markdown
---
layout_hint: centered
palette_hint: dark
quote_style: concise
---
# Deep Work
Focus is the new IQ.
```

Apply it with `genwal theme use deep_work`. The frontmatter keys get written directly into your config.

---

## CLI Reference

```bash
# Generation
genwal run                         # Generate and apply wallpaper now
genwal preview                     # Generate to /tmp, don't apply

# Themes
genwal theme list                  # List available themes
genwal theme use <name>            # Switch active theme
genwal theme edit <name>           # Create/edit a theme file

# Configuration
genwal config get                  # Print full config as JSON
genwal config get <key>            # Print a specific value (supports dot.notation)
genwal config set <key> <value>    # Set a config key (with tab-completion!)
genwal config edit                 # Open config in $EDITOR

# Scheduling
genwal schedule list               # Show current schedule and status
genwal schedule set 08:00          # Set daily run time (HH:MM)
genwal schedule remove             # Remove the schedule
genwal schedule show               # Full systemd timer status

# Utilities
genwal seed                        # Inspect the active deterministic seed
genwal palette preview             # Preview 5 color palette variations
genwal history                     # View generated wallpaper history
genwal history apply <N>           # Restore a previous wallpaper
genwal providers list              # List all registered providers
genwal doctor                      # Diagnose paths and config health
genwal logs                        # Tail the systemd service logs
genwal uninstall                   # Completely remove Gen-Wal
```

---

## Uninstall

```bash
genwal uninstall
```

Or directly:

```bash
cd /path/to/gen-wal && ./uninstall.sh
```

---

## Developing

```bash
git clone https://github.com/nicemit/gen-wal
cd gen-wal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py run
```

---

## License

MIT

If you find this experiment interesting, a GitHub star helps others discover it.
