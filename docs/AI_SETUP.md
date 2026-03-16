# AI Providers

Gen-Wal supports **Bring Your Own AI** for image generation. It acts as a universal client that dynamically translates themes, quotes, and palettes into cohesive text-to-image prompts.

## Activating AI Generation

To use an AI backend, you must change your image provider to `"ai"` and configure an `"ai"` block in your `~/.config/genwal/config.json`.

```json
{
    "image_provider": "ai",
    "ai": {
        "backend": "openai",
        "api_key": "sk-...",
        "model": "dall-e-3"
    }
}
```

## Prompt Generation

You do not need to write prompts manually. The AI dispatcher uses a centralized prompt builder (`src/ai_prompt.py`) that observes the deterministic seed pipeline. It automatically constructs prompts by combining:
1. The deterministic quote for the day.
2. The exact color palette (including hex codes) chosen for the run.
3. The layout and style hints defined by your active Gen-Wal theme.

## Supported Backends

### Local AI (Ollama / LMStudio)

You can run entirely local AI image generation models (like FLUX or Stable Diffusion wrappers) that provide an OpenAI-compatible API endpoint.

**Config Example:**
```json
{
    "image_provider": "ai",
    "ai": {
        "backend": "openai_compatible",
        "base_url": "http://localhost:1234/v1",
        "model": "flux-image-v1"
    }
}
```

*Note: For LMStudio, ensure the local server is started. For Ollama, you may need a specialized proxy bridging images, although `base_url` can be pointed to `http://localhost:11434/v1`.*

### OpenAI (DALL-E)

Uses standard OpenAI REST APIs.

**Config Example:**
```json
{
    "image_provider": "ai",
    "ai": {
        "backend": "openai",
        "api_key": "YOUR_API_KEY",
        "model": "dall-e-3"
    }
}
```
*(You can also omit `api_key` if you have `OPENAI_API_KEY` set as an environment variable.)*

### OpenRouter

Use OpenRouter to access hundreds of models utilizing the standard compatible layer.

**Config Example:**
```json
{
    "image_provider": "ai",
    "ai": {
        "backend": "openrouter",
        "api_key": "YOUR_OPENROUTER_KEY",
        "model": "google/imagen-3.0"
    }
}
```

### Gemini & Anthropic
We ship provider configuration stubs for Gemini and Anthropic. At present, these usually require dedicated SDKs rather than the generic `.generate_image` flow. Advanced users can modify `src/providers/images/ai/gemini.py` locally if using the `google-generativeai` SDK.
