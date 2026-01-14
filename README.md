# Gen-Wal 🧠

**Your desktop becomes your quiet daily coach.**

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge&logo=github)

![Gen-Wal Banner](docs/images/banner.png)

> A personal-first AI daemon that generates a personalized motivational
> wallpaper on your desktop every morning.\
> Private. Beautiful. Automatic.

------------------------------------------------------------------------

## Why?

Most motivation apps require you to open them. Gen-Wal just exists in your environment.

It runs quietly in the background, updating your desktop once a day with a new wallpaper and quote tailored to your specific goals. It's a simple, set-and-forget ritual to keep your digital space fresh.

Values: I built this for myself because my desktop felt like noise. Now it quietly reminds me what actually matters.

------------------------------------------------------------------------

## What It Does

• Generates a new wallpaper every morning\
• Uses your personal profile (goals, habits, mindset)\
• Runs with a local AI brain (llama.cpp / Ollama)\
• Auto-contrast typography for perfect readability\
• systemd-powered scheduling\
• Modular architecture for quotes, images, and prompts

------------------------------------------------------------------------

## Example Wallpapers

*(Add 4--6 real generated wallpapers here --- this section massively
increases stars.)*

------------------------------------------------------------------------

## 60-Second Install

``` bash
curl -fsSL https://laptopserver.dev/genwal | bash
```

Installs:

• llama.cpp\
• A local 4B AI model\
• systemd daily service\
• Interactive setup wizard

You'll get your first personalized wallpaper in under 2 minutes.

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

Gen-Wal comes with pre-built profiles to jumpstart your day. Select one by changing `profile_path` in `config.yaml`:

| Pack | Focus | Config Path |
| :--- | :--- | :--- |
| **Stoic** | Resilience, Virtue | `profiles/examples/stoic_profile.md` |
| **Founder** | Speed, Leverage | `profiles/examples/founder_profile.md` |
| **Monk** | Deep Work, Zen | `profiles/examples/monk_profile.md` |
| **Iron/Gym** | Discipline, Strength | `profiles/examples/gym_profile.md` |

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
