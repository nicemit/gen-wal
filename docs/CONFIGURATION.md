# Gen-Wal Configuration Guide

## 🛠️ Quick Edits (Recommended)

Use the built-in CLI to edit your configuration safely:

```bash
genwal config edit
```

This ensures you are editing the correct file for your installation (located at `~/.config/genwal/config.json`).

## How It Works

Gen-Wal is a simple daemon that runs once a day. The process is fully automated:

- **Read Theme:** Loads a markdown file describing the desired mindset (e.g., "stoic", "terminal").
- **Generate Text:** Uses an AI provider to generate a short, punchy quote based on the theme.
- **Generate Background:** Creates a matching background image (subtle, abstract) using an image provider.
- **Set Wallpaper:** Composes the text and image using a layout, then updates your desktop background.

## 🧠 Reference Frames (Themes)

Themes are the core of Gen-Wal. They are not just collections of quotes; they define a **mental reference frame**. By changing the theme, you change the "flavor" of your environment.

### Included Examples

- **minimal:** Clean, understated, and clear.
- **stoic:** Restraint, control, impermanence.
- **terminal:** Code, craft, iteration.

## 🛠️ Creating Your Own Theme {#customization}
Themes are plain Markdown files stored in `~/.local/share/genwal/themes/`. They provide hints to the generation engines.

**Example `~/.local/share/genwal/themes/deep_work.md`:**

```markdown
---
layout_hint: centered
palette_hint: dark abstract, deep focus, blue and black
quote_style: raw discipline, focus, no excuses
---
# Deep Work
Focus is the new IQ.
Deep work is the ability to focus without distraction on a cognitively demanding task.
```

To switch to this theme, simply run:
```bash
genwal theme use deep_work
```

## Global Settings (`config.json`)

### Core Settings

| Key | Description | Default |
| :--- | :--- | :--- |
| `theme` | Name of the theme to use (from `~/.local/share/genwal/themes/`). | `minimal` |
| `seed` | Deterministic seed. Use `"auto"` for daily cycle, or pass an integer. | `"auto"` |
| `layout` | Strategy for composing text/image. Options: `minimal`, `centered`. | `minimal` |
| `quote_provider` | Text generation engine. Options: `pollinations:text`, `csv`. | `pollinations:text` |
| `image_provider` | Image generation engine. Options: `pollinations:image`, `gradient`. | `pollinations:image` |
| `palette_provider` | Color scheme generation. Options: `system_theme`. | `system_theme` |

## Quote Providers

### Pollinations AI (Remote, Default)
Uses free, keyless AI endpoints to generate dynamic quotes matching your theme.

```yaml
quote_provider: "pollinations:text"
```

### CSV
Loads pre-written quotes from a local CSV file.

```yaml
quote_provider: "csv" 
csv:
  file: "~/.local/share/genwal/quotes.csv"
```

## Image Providers

### Pollinations AI (Remote, Default)
Generates free AI background images based on theme hints.

```yaml
image_provider: "pollinations:image"
```

### Gradient (Local)
A blazing-fast deterministic local gradient generator built cleanly in Python.

```yaml
image_provider: "gradient"
```

## Rendering & Styling

Customize the canvas resolution:

```yaml
resolution:
  width: 1920
  height: 1080
```

*Note: Visual placements (text positioning, padding, fonts) are now handled exclusively by the `layout` engine (e.g., `minimal` places text bottom-right, `centered` centers it).*

## CLI Utilities

You can manage Gen-Wal entirely from the command line:

| Command | Description |
| :--- | :--- |
| `genwal run` | Generate now in the background |
| `genwal preview` | Generate to `tmp/`, do not apply to OS |
| `genwal theme list` | List available themes |
| `genwal theme edit <name>` | Create/Edit a theme |
| `genwal config show` | Print current active configuration |
| `genwal config edit` | Open config in your default `$EDITOR` |
| `genwal history` | View recent generated wallpapers |
| `genwal history apply <N>` | Restore a previous generated wallpaper |
| `genwal seed` | Inspect the active deterministic seed |
| `genwal schedule set <Time>` | Change the daily systemd execution schedule |
| `genwal doctor` | Diagnose paths and configuration health |
