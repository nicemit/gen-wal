# Gen-Wal Configuration Guide

## 🛠️ Quick Edits (Recommended)

Use the built-in CLI to edit your configuration safely:

```bash
genwal config
```

This ensures you are editing the correct file for your installation.

# Configuration Reference

## 🧠 Smart Profiles
Gen-Wal profiles support "Smart Prompts" using YAML Frontmatter. This creates self-contained "Mindset Packs" that define specific personas without needing global config.

**Example `my_profile.md`:**
```markdown
---
quote_prompt_template: "Act as a Drill Sergeant. SCREAM the quote. Max 15 words."
image_prompt_template: "Generate a prompt for a gritty, dark industrial gym. Iron, sweat, shadows. Max 15 words."
---
# Iron Gym
I value strength...
```

When you run `python3 main.py --profile my_profile.md`, these prompts will override your `config.yaml` defaults.

## Global Settings (`config.yaml`).

### Configuration Logic
Gen-Wal uses a powerful **path-based** configuration system. You can point any provider to a specific section of your config using `provider:subtype`.

**Example:**
- `quote_provider: "llm:ollama"` -> Uses config from `llm` -> `ollama`.
- `quote_provider: "csv:work"` -> Uses config from `csv` -> `work`.

## Core Settings

| Key | Description | Default |
| :--- | :--- | :--- |
| `profile_path` | Path to your personal motivation profile (Markdown). | `profiles/amit_motivation_profile.md` |
| `quote_provider` | Options: `huggingface:text`, `llm:profile`, `pollinations:text`, `csv:profile`. | `zenquotes` |
| `image_provider` | Options: `huggingface:image`, `pollinations:image`, `local_dir:profile`. | `pollinations:image` |
| `image_prompt_provider` | Options: `huggingface:text`, `pollinations:text`, `llm:profile`. | `pollinations:text` |

## Quote Providers

### LLM (Local/Cloud)
Define multiple profiles under the `llm` block and select one.

```yaml
quote_provider: "llm:ollama"

llm:
  # Profile 1: Local Ollama
  ollama:
    base_url: "http://localhost:11434/v1" 
    api_key: "ollama" 
    model: "llama3.2" 

  # Profile 2: Llama.cpp or OpenAI
  openai_cloud:
    base_url: "https://api.openai.com/v1"
    api_key: "sk-..."
    model: "gpt-4"
```

### Hugging Face
Use the free Hugging Face Inference API for high-availability access to open models.

```yaml
quote_provider: "huggingface:text"
huggingface:
  api_key: "hf_YOUR_TOKEN"
  # Optional overrides
  # text_model: "Qwen/Qwen2.5-7B-Instruct"
  # image_model: "stabilityai/stable-diffusion-2-1"
```

### CSV / YAML
Load your own collection of quotes.

```yaml
quote_provider: "csv" 
csv:
  file: "my_quotes.csv"

# Or nested:
# quote_provider: "csv:work"
# csv:
#   work:
#     file: "work_quotes.csv"
```

## Image Providers

### Pollinations.ai (AI Generation)
Generates free AI images based on prompts.

```yaml
image_provider: "pollinations"
pollinations:
  model: "flux" # Options: flux, turbo, etc.
  nologo: true # Set to false if you want the logo (why?)
```

### Local Directory
Picks a random image from a folder.

```yaml
image_provider: "local_dir"
local_dir:
  path: "/path/to/wallpapers"
```

## Rendering & Styling

Customize how the wallpaper looks.

```yaml
resolution:
  width: 1920
  height: 1080

text_position: "center" # bottom_left, bottom_center, bottom_right, left_center, right_center, top_left, center, etc.
text_padding: 100 # Distance from screen edge in pixels
```

## External Customization (Prompts)

You can tweak the "personality" of the AI without touching code by editing the `prompts` section in `config.yaml`.

```yaml
prompts:
  quote: |
    You are a motivational coach. Based on the following profile, generate a single, short...
    PROFILE:
    {profile_content}

  image_description: |
    Generate a concise visual description...
    QUOTE: {quote}
    PROFILE: {profile_content}
```

- **`{profile_content}`**: Injected automatically from your selected markdown profile.
- **`{quote}`**: Injected automatically into the image description prompt.

## Wallpaper Settings

Control where the wallpaper is saved and if it is applied.

| Key | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| `save_path` | string | Absolute path (or path with `~`) to save the final image. | `~/.cache/gen-wal/current_wallpaper.jpg` |
| `apply_wallpaper` | boolean | If `true`, sets the desktop background. If `false`, only saves the file. | `true` |

```yaml
# -----------------------------------------------------------------------------
# 1. Wallpaper Settings
# -----------------------------------------------------------------------------
wallpaper_settings:
  apply_wallpaper: true  # Set to false to generate image but not set desktop background
  save_path: "~/.cache/gen-wal/current_wallpaper.jpg" # Where to save the generated image
```

## CLI Overrides

You can temporarily override configuration settings via command-line arguments:

| Argument | Description | Example |
| :--- | :--- | :--- |
| `--profile` | Use a different profile file for this run. | `python3 main.py --profile profiles/examples/monk_profile.md` |
| `--text-pos` | Override text positioning. | `python3 main.py --text-pos center` |
| `--config` | Use a specific config file. | `python3 main.py --config my_custom_config.yaml` |
