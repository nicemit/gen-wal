# Gen-Wal Configuration Guide

This document explains how to configure **Gen-Wal** using `config.yaml`.

## Configuration Logic
Gen-Wal uses a powerful **path-based** configuration system. You can point any provider to a specific section of your config using `provider:subtype`.

**Example:**
- `quote_provider: "llm:ollama"` -> Uses config from `llm` -> `ollama`.
- `quote_provider: "csv:work"` -> Uses config from `csv` -> `work`.

## Core Settings

| Key | Description | Default |
| :--- | :--- | :--- |
| `profile_path` | Path to your personal motivation profile (Markdown). | `profiles/amit_motivation_profile.md` |
| `quote_provider` | Options: `llm:profile`, `pollinations:text`, `csv:profile`, `yaml:profile`. | `zenquotes` |
| `image_provider` | Options: `pollinations:image`, `local_dir:profile`. | `pollinations:image` |
| `image_prompt_provider` | Options: `pollinations:text`, `llm:profile`. Optional dynamic prompt generation. | `pollinations:text` |

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
