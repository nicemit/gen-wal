# Gen-Wal Configuration Guide

This document explains how to configure **Gen-Wal** using `config.yaml`.

## Core Settings

| Key | Description | Default |
| :--- | :--- | :--- |
| `profile_path` | Path to your personal motivation profile (Markdown). | `profiles/amit_motivation_profile.md` |
| `quote_provider` | Which service to use for quotes. Options: `llm`, `zenquotes`, `csv`, `yaml`. | `zenquotes` |
| `image_provider` | Which service to use for background images. Options: `pollinations`, `local_dir`. | `pollinations` |

## Quote Providers

### LLM (Local/Cloud)
Use a Local LLM (like Ollama) or an OpenAI-compatible API to generate personalized quotes.

```yaml
quote_provider: "llm"
llm:
  base_url: "http://localhost:11434/v1" # Local Ollama URL
  api_key: "ollama" # Dummy key for local, actual key for cloud
  model: "llama3.2" # Model name
  # Optional: Customize the persona
  prompt_template: "You are a stoic philosopher. Give me a quote based on: {profile_content}"
```

### Llama.cpp (or other specific APIs)
You can point to your local `llama-server` (usually port 8080). You can also pass precise parameters in `request_params`.

```yaml
quote_provider: "llm"
llm:
  base_url: "http://localhost:8080/v1"
  api_key: "any"
  model: "default"
  request_params:
    temperature: 0.9
    top_k: 40
    top_p: 0.5
    n_predict: 50 # llama.cpp specific
```

Load your own collection of quotes.

```yaml
quote_provider: "csv" # or "yaml"
quotes_file: "my_quotes.csv" # Path to file
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
local_image_dir: "/path/to/wallpapers"
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
