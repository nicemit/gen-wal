# Gen-Wal: Motivational Wallpaper Generator

![Gen-Wal Banner](docs/images/banner.png)

A modular, automated wallpaper generator that keeps you motivated with fresh quotes and stunning backgrounds every day.

## Features
- **Daily Updates**: Scheduled automatically via systemd.
- **Personalized**: Supports custom profiles and themes.
- **Modular**: Swap out Quote, Image, and Image Prompt providers easily.
- **Providers**:
    - **Quotes**: LLM (Ollama/Llama.cpp), CSV/YAML file, Pollinations (Text), ZenQuotes (API).
    - **Images**: Pollinations.ai (AI Generated), Local Folder.
    - **Image Prompts**: Dynamic AI generation of image prompts using your profile.
- **Smart Rendering**: Auto-contrasting text overlay.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gen-wal.git
   cd gen-wal
   ```

2. Run the installer:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

## Configuration
Edit `config.yaml` to customize your experience.

**[Read the Full Configuration Guide](docs/CONFIGURATION.md)**

```yaml
profile_path: "profiles/my_profile.md"

# Choose Providers (Subtype selection available)
quote_provider: "llm:ollama"
image_provider: "pollinations:image"
image_prompt_provider: "pollinations:text" # Generates dynamic image descriptions

# LLM Settings (Defined by profile name)
llm:
  ollama:
    base_url: "http://localhost:11434/v1" 
    model: "llama3"

# Pollinations Settings
pollinations:
  image:
    model: "flux"
  text:
    model: "openai"

# Image Resolution
resolution:
  width: 1920
  height: 1080
```

## Custom Quotes
You can provide your own quotes in `my_quotes.csv` or `my_quotes.yaml`.

**CSV Format:**
```csv
"The only way to do great work is to love what you do."
"Stay hungry, stay foolish."
```

## License
MIT
