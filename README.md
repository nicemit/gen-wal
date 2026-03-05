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

I spend a large portion of my day in front of my machine. Keeping goals in my head wasn’t enough, but I also didn’t want yet another app demanding attention.

Gen-Wal changes **one visual element of the environment** once per day.

Quietly.

It uses a *profile* (a simple text file describing a mindset or focus) and generates a daily background that acts as a passive reference frame — something you see repeatedly without being interrupted.

This is not meant to push behavior. It’s meant to **exist**.

---

## What It Is

Gen-Wal is a small local daemon written in Python that:

- Reads a text-based theme (e.g. Stoic, Builder, Terminal)
- Generates short text using a local or remote AI provider
- Optionally generates a matching base image / gradient
- Updates the desktop wallpaper automatically

You can use it, modify it, or ignore it.

---

## Privacy & Local Execution

**Gen-Wal runs as a local daemon.** It has no accounts, no analytics, and no tracking code.

- **Default**: Uses free remote APIs (Pollinations.ai) for zero-setup generation.
- **Local**: Can be configured to run **100% locally** using Ollama/LocalAI for text and local directories for images.

You control where the data goes.

---

## Installation

One-line install for Linux (GNOME / KDE / Unity):

```bash
curl -sL https://gen-wal.laptopserver.dev/install | bash
```

This sets up:

- The `genwal` CLI (for config, themes, scheduling)
- A systemd timer (daily update)
- XDG-compliant data directories (`~/.config/genwal/`, `~/.local/share/genwal/themes/`)

---

## Configuration

Everything is configurable. You can control how visible or subtle the output is.

```yaml
theme: "stoic"
layout: "bottom_right"
seed: "auto"

quote_provider: "pollinations:text"
image_provider: "pollinations:image"
palette_provider: "system_theme"

# Themes are sourced from ~/.local/share/genwal/themes/
```

---

## Themes (Mindsets)

Themes are not just aesthetic tweaks — they define **mental reference frames**.

Included examples:

- **Stoic** — *Restraint, impermanence, control*  
  *(Meditations, Letters from a Stoic)*

- **Deep Work** — *Focus, systems, resistance*  
  *(Deep Work, Atomic Habits, War of Art)*

- **Builder** — *Craft, simplicity, iteration*  
  *(Hackers & Painters, Unix philosophy)*

- **Zen** — *Presence, patience, non-forcing*  
  *(Zen Mind, Tao Te Ching)*

---

## Create Your Own Theme

Themes are plain Markdown files stored in `~/.local/share/genwal/themes/`.

```markdown
---
layout_hint: minimal
palette_hint: dark abstract
quote_style: short, calm, stoic
---
# Quiet Focus
Presence over pressure.
```

Point your config to it and that’s it.

---

## CLI Usage

```bash
genwal run                         # Generate now in the background
genwal preview                     # Generate to tmp, do not apply to OS
genwal config show                 # View active configuration
genwal config edit                 # Edit configuration
genwal theme list                  # List available themes
genwal theme use <name>            # Switch to active theme
genwal theme edit <name>           # Create/Edit theme file
genwal seed                        # Check the deterministic seed
genwal history                     # View generated wallpaper history
genwal schedule set 08:00          # Schedule a daily run
genwal doctor                      # Check system health & directories
genwal uninstall                   # Completely remove Gen-Wal
```

---

## Uninstall

To remove everything:

```bash
cd ~/.gen-wal && ./uninstall.sh
```

---

## Future Ideas

- Time-bounded focus windows
- Extended context from books/articles
- Daily intent injection
- Community profile sharing

---

## Developing

This is a personal project.

```bash
git clone https://github.com/nicemit/gen-wal
cd gen-wal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

---

## License

MIT

If you find this experiment interesting, a GitHub star helps others discover it.

