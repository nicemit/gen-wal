# Gen-Wal: Motivational Wallpaper Generator

A modular, automated wallpaper generator that keeps you motivated with fresh quotes and stunning backgrounds every day.

## Features
- **Daily Updates**: Scheduled automatically via systemd.
- **Personalized**: Supports custom profiles and themes.
- **Modular**: Swap out Quote and Image providers easily.
- **Providers**:
    - **Quotes**: Local LLM (Ollama), CSV/YAML file, ZenQuotes (API).
    - **Images**: Pollinations.ai (AI Generated), Local Folder.
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


# Choose Providers
quote_provider: "llm" # Options: llm, csv, yaml, zenquotes
image_provider: "pollinations" # Options: pollinations, local_dir

# LLM Settings (for 'llm' provider)
llm:
  base_url: "http://localhost:11434/v1" # Local Ollama
  model: "llama3"

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
