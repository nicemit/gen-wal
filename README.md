# Gen-Wal 🧠

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge&logo=github)

**A personal experiment in ambient computing.**

| | | |
|:---:|:---:|:---:|
| <img src="docs/images/carousel/1.jpg" width="100%"> | <img src="docs/images/carousel/2.jpg" width="100%"> | <img src="docs/images/carousel/3.jpg" width="100%"> |
| <img src="docs/images/carousel/4.jpg" width="100%"> | <img src="docs/images/carousel/5.jpg" width="100%"> | <img src="docs/images/carousel/6.jpg" width="100%"> |

> I was curious whether the desktop itself could be part of a productivity system.
> Specifically, whether passive environmental cues (like a wallpaper) work better than apps, notifications, or dashboards.

------------------------------------------------------------------------

## The Experiment

I spend a lot of time working on my machine. I realized that keeping goals in my head wasn't enough, but I didn't want another app to check.

**Gen-Wal** is a background daemon that changes one thing a day. Nothing more. It generates a wallpaper based on a "profile" (a text file defining a mindset or goal).

It's not a product. It's just a script I wrote to see if changing my environment quietly could change my focus.

------------------------------------------------------------------------

## What It Is

A Python script that:

1.  **Reads a text profile** (e.g., "Stoic", "Founder", "Creative").
2.  **Generates a quote** using a local or cloud LLM.
3.  **Generates an image** matching that quote.
4.  **Updates your wallpaper** automatically.

Use it if you want to. Modify it if you need to.

------------------------------------------------------------------------

## Installation

One-line install for Linux (GNOME/Unity/KDE):

```bash
curl -sL https://gen-wal.laptopserver.dev/install | bash
```

This sets up:
- The `genwal` CLI tool (for easy config & overrides)
- A systemd timer (daily update at 9:00 AM)
- Default config in `~/.gen-wal/`

------------------------------------------------------------------------

## Configuration

The system is fully configurable. You can tweak the text content, font size, position, and timing in `config.yaml`.

```yaml
# config.yaml example

text_position: "bottom_right" # understated placement
font_size: 45                 # smaller text
image_provider: "pollinations:image" # or "local_dir"

# Watermark your profile name (e.g. "Stoic", "F1 Racing")
watermark:
  enabled: true
  position: "bottom_right"
  opacity: 150

# Randomly rotate between mentors/mindsets
profile_path: 
  - "profiles/examples/stoic.md"
  - "profiles/examples/deep_work.md"
  - "profiles/examples/builder.md"
  - "profiles/examples/zen.md"
```

### Profiles

profiles/examples/stoic.md
```

### Reference Frames

Gen-Wal comes with a curated set of **Mindset Sources** to quietly influence your day. These are not just quotes—they are mental reference frames.

- **Stoic** (Meditations, Letters from a Stoic) -> *Restraint, impermanence, control.*
- **Deep Work** (Atomic Habits, War of Art) -> *Systems, focus, resistance.*
- **Builder** (Hackers & Painters, Unix Philosophy) -> *Craft, simplicity, iteration.*
- **Zen** (Zen Mind, Tao Te Ching) -> *Presence, patience, non-forcing.*

### Create Your Own
You are not limited to these. Create a new `my_focus.md` file in `profiles/` with your own prompts:

```markdown
---
quote_prompt_template: "Act as a Drill Sergeant. SCREAM the quote. Max 15 words."
image_prompt_template: "Generate a prompt for a gritty, dark industrial gym. Iron, sweat, shadows."
---
# Iron Mode
Strength, Pain, Victory.
```

Then point your config to it.

------------------------------------------------------------------------

## CLI Usage

```bash
genwal run             # Trigger a new wallpaper now
genwal run --font-size 40 --text-pos center  # Override settings instantly
genwal config          # Edit your settings
genwal profile list    # See available profiles
genwal profile use     # Switch your active profile
```

------------------------------------------------------------------------

## Uninstallation

To remove it completely:

```bash
cd ~/.gen-wal && ./uninstall.sh
```

------------------------------------------------------------------------

------------------------------------------------------------------------
 
 ## Future Ideas
 
 - **Focus Window**: Toggle the service for a specific daily period (e.g., 4-6 PM) to transform the desktop into a deep work environment.
 - **Extended Context**: Dynamically generate quotes from a wider range of books, articles, and specific personalities.
 - **Daily Task Intent**: Allow the user to input a specific focus for the day, generating wallpapers that quietly reinforce that single task.
 - **Profile Marketplace**: A community hub to share, vote on, and download new reference frames directly from the CLI.

 
 ------------------------------------------------------------------------
 
 ## Developing

This is a personal project. If you want to hack on it:

1. Clone the repo
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python3 main.py`

License: MIT.

> If you find this experiment interesting, a star on GitHub helps others find it.
