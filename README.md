# Gen-Wal 🧠

**Your desktop becomes your quiet daily coach.**

![Gen-Wal Banner](docs/images/banner.png)

> A local-first AI daemon that generates a personalized motivational
> wallpaper on your desktop every morning.\
> Offline. Private. Automatic.

------------------------------------------------------------------------

## Why Gen-Wal?

Motivation apps need attention.\
Gen-Wal lives in your peripheral vision.

You don't open it.\
It opens you --- every morning.

Your wallpaper quietly reinforces focus, discipline, and clarity\
using your own local AI.

No subscriptions.\
No tracking.\
No cloud dependency.

------------------------------------------------------------------------

## What It Does

• Generates a new wallpaper every morning\
• Uses your personal profile (goals, habits, mindset)\
• Runs fully offline using llama.cpp / Ollama\
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
curl -fsSL https://get.genwal.sh/genwal | bash
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

## Runs 100% Locally

• No internet required\
• No data collection\
• Your AI runs on your machine\
• Fully deterministic and reproducible

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
