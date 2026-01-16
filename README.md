# Gen-Wal 🧠

**Your desktop becomes your quiet daily coach.**

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge&logo=github)

![Gen-Wal Banner](docs/images/banner.gif)

> A personal-first AI daemon that generates a personalized motivational
> wallpaper on your desktop every morning.\
> Private. Beautiful. Automatic.

------------------------------------------------------------------------

## Why?

Most motivation apps require you to open them. Gen-Wal just exists in your environment.

It runs quietly in the background, updating your desktop once a day with a new wallpaper and quote tailored to your specific goals. It's a simple, set-and-forget ritual to keep your digital space fresh.

Values: I built this because my desktop felt like noise. Now, it keeps my plans in focus—reminding me not just of the goal, but that I have to do the work to see results.

------------------------------------------------------------------------

## What It Does

• Generates a new wallpaper every morning\
• Uses your personal profile (goals, habits, mindset)\
• Runs with a local AI brain (llama.cpp / Ollama) or Cloud (Pollinations / Hugging Face)\
• Auto-contrast typography for perfect readability\
• systemd-powered scheduling\
• Modular architecture for quotes, images, and prompts

------------------------------------------------------------------------

## Example Wallpapers


| **Founder Profile** | **Monk Profile** |
| :---: | :---: |
| <img src="docs/images/founder-example-1.jpg" width="100%" alt="Founder Startup Wallpaper"> | <img src="docs/images/monk-example-1.jpg" width="100%" alt="Zen Monk Wallpaper"> |

| **Gym Profile** | **Founder Profile (Variant)** |
| :---: | :---: |
| <img src="docs/images/gym-example-1.jpg" width="100%" alt="Gym Motivation Wallpaper"> | <img src="docs/images/founder-example-2.jpg" width="100%" alt="Founder Wallpaper Variant"> |


------------------------------------------------------------------------

60-Second Install
``` bash
curl -fsSL https://laptopserver.dev/genwal | bash
```

Installs:
• **Gen-Wal** (Python-based AI daemon)
• **Systemd** daily service
• **Zero-Config** default (uses Pollinations.ai)
• **Interactive** Setup Wizard (Profile & Vibe)

You'll get your first personalized wallpaper in under 2 minutes. No heavy downloads required.

> **Power User?** You can still switch to local LLMs (Ollama/Llama.cpp) in `config.yaml` after install.

------------------------------------------------------------------------

## Customize Your Mindset

``` yaml
profile_path: "profiles/my_profile.md"

quote_provider: "llm:ollama"
image_provider: "pollinations:image"
image_prompt_provider: "pollinations:text"

llm:
  ollama:
    base_url: "http://localhost:11434/v1"
    model: "qwen3"

resolution:
  width: 1920
  height: 1080
```

### Included Mindset Packs

Gen-Wal profiles are **"Smart Packs"** that contain their own system prompts. A standard profile not only defines *who* you want to be but *how* the AI should speak to you.

| Pack | Focus | Prompt Style |
| :--- | :--- | :--- |
| **Stoic** | Resilience, Virtue | Marcus Aurelius (Direct, Ancient) |
| **Founder** | Speed, Leverage | YC Partner (Curt, High-Tech) |
| **Monk** | Deep Work, Zen | Zen Master (Cryptic, Misty) |
| **Gym** | Discipline, Strength | Drill Sergeant (Aggressive, Gritty) |

Select one by changing `profile_path` in `config.yaml` or running:
```bash
python3 main.py --profile profiles/examples/gym_profile.md
```



------------------------------------------------------------------------

## Advanced Usage

### CLI Overrides
You can override your config settings directly from the command line:

```bash
# Run with a specific profile and text position
python3 main.py --profile profiles/examples/monk_profile.md --text-pos center
```

------------------------------------------------------------------------

## Personal-First

• **Your values** and intent stay on your machine\
• **Visual beauty** is generated on demand\
• **Privacy** where it matters most\
• **A tiny personal AI ritual** that refreshes your desktop every day

------------------------------------------------------------------------

## Roadmap

• Multiple mindset packs\
• Theme marketplace\
• Journal memory mode\
• Multi-monitor support\
• Live animated wallpapers

------------------------------------------------------------------------

## License

MIT --- build your own mental OS.
