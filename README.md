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

- Reads a text-based profile (e.g. Stoic, Builder, Zen)
- Generates short text using a local or remote LLM
- Optionally generates a matching image
- Updates the desktop wallpaper automatically

You can use it, modify it, or ignore it.

---

## Installation

One-line install for Linux (GNOME / KDE / Unity):

```bash
curl -sL https://gen-wal.laptopserver.dev/install | bash
```

This sets up:

- The `genwal` CLI (for easy config & overrides)
- A systemd timer (daily update)
- Default config in `~/.gen-wal/`

---

## Configuration

Everything is configurable. You can control how visible or subtle the output is.

```yaml
text_position: "bottom_right"   # understated placement
font_size: 45                   # smaller text
image_provider: "pollinations:image"  # or "local_dir"

watermark:
  enabled: true
  position: "bottom_right"
  opacity: 150

profile_path:
  - "profiles/examples/stoic.md"
  - "profiles/examples/deep_work.md"
  - "profiles/examples/builder.md"
  - "profiles/examples/zen.md"
```

---

## Profiles (Reference Frames)

Profiles are not just quote collections — they define **mental reference frames**.

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

## Create Your Own Profile

Profiles are plain Markdown files.

```markdown
---
quote_prompt_template: "Max 12 words. Calm, direct, non-preachy."
image_prompt_template: "Muted, minimal, low-contrast background."
---
# Quiet Focus
Presence over pressure.
```

Point your config to it and that’s it.

---

## CLI Usage

```bash
genwal run                         # Generate now
genwal run --font-size 40           # Override settings
genwal config                      # Edit config
genwal profile list                # List profiles
genwal profile use                 # Switch profile
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

