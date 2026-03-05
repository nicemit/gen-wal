# Gen-Wal Configuration Guide

## Quick Setup

Use the CLI to inspect and modify your configuration without ever opening a file:

```bash
genwal config get              # Print entire active config as JSON
genwal config get seed         # Get a single key
genwal config set seed random  # Set a key (tab-completion shows valid values)
genwal config set noise.opacity 0.5    # Dot-notation for nested keys
genwal config edit             # Open in $EDITOR
```

Config file lives at: `~/.config/genwal/config.json`

---

## How It Works

Gen-Wal is a simple daemon that fires once per day via systemd. The pipeline:

1. **Load Config** — Reads `~/.config/genwal/config.json` as the single source of truth.
2. **Derive Seed** — Generates a deterministic or random seed for the run.
3. **Generate Palette** — Creates a color scheme using the active palette provider.
4. **Apply Color Strategy** — Transforms the palette using seeded color theory rules.
5. **Fetch Quote** — Gets a short text from the configured quote provider.
6. **Generate Image** — Creates a procedural background (mesh, voronoi, noise, etc.).
7. **Post-Processing** — Applies vignette and grain effects.
8. **Layout** — Composes the quote and image using the selected layout engine.
9. **Set Wallpaper** — Updates the desktop background.

---

## Core Settings

| Key | Description | Options | Default |
| :--- | :--- | :--- | :--- |
| `theme` | Active theme name | any theme in `themes/` | `minimal` |
| `seed` | Generation seed mode | `auto`, `random`, or integer | `auto` |
| `color_mode` | Color variation intensity | `minimal`, `balanced`, `vibrant`, `wild` | `balanced` |
| `image_provider` | Background generator | `mesh`, `gradient`, `noise`, `flow`, `voronoi`, `aurora`, `pollinations` | `mesh` |
| `palette_provider` | Color scheme source | `system_theme`, `theme_palette`, `random` | `system_theme` |
| `quote_provider` | Quote source | `csv`, `pollinations` | `csv` |
| `layout` | Text composition strategy | `minimal`, `centered` | `minimal` |
| `layout_hint` | Layout hint from theme | `minimal`, `centered` | `minimal` |
| `palette_hint` | Palette hint from theme | `dark`, `light`, `warm`, `cool` | `dark` |
| `quote_style` | Quote style hint from theme | `stoic`, `concise`, `builder`, `zen`, `deepwork` | `stoic` |

---

## Resolution

```json
"resolution": {
  "width": 1920,
  "height": 1080
}
```

Set via CLI: `genwal config set resolution.width 2560`

---

## Image Providers

### Local (No Network Required)

| Provider | Description |
|---|---|
| `mesh` | Apple-style mesh gradients (default) |
| `gradient` | Smooth linear/radial gradients |
| `noise` | Configurable geometric noise patterns |
| `flow` | Abstract vector field generative art |
| `voronoi` | Geometric Voronoi cell diagrams |
| `aurora` | Aurora borealis-style soft gradients |

### Remote

| Provider | Description |
|---|---|
| `pollinations` | Free AI-generated images (no API key needed) |

Switch providers: `genwal config set image_provider voronoi`

### Noise Provider Settings

```json
"noise": {
  "scale": 10,
  "opacity": 0.25,
  "style": "smooth"
}
```

`style` options: `smooth`, `blocky`

---

## Quote Providers

### CSV (Local, Default)

```json
"quote_provider": "csv",
"csv": {
  "file": "~/.local/share/genwal/quotes.csv"
}
```

CSV format: one quote per line.

### Pollinations AI (Remote)

```json
"quote_provider": "pollinations"
```

Uses free AI endpoints. No API key required.

---

## Color Strategies

Gen-Wal applies seeded color theory transforms to the base palette each run.

| `color_mode` | Strategies Used |
|---|---|
| `minimal` | monochrome |
| `balanced` | analogous, complementary, accent |
| `vibrant` | complementary, triadic, analogous |
| `wild` | all strategies randomly |

Set via: `genwal config set color_mode vibrant`

---

## Themes

Themes are Markdown files in `~/.local/share/genwal/themes/` (or `themes/` in the repo). Running `genwal theme use <name>` reads the frontmatter and writes those values directly into `config.json`.

**Example `~/.local/share/genwal/themes/deep_work.md`:**

```markdown
---
layout_hint: centered
palette_hint: dark
quote_style: deepwork
---
# Deep Work
Focus is the new IQ.
```

```bash
genwal theme use deep_work   # Applies frontmatter keys into config.json
genwal theme list            # List all available themes
genwal theme edit deep_work  # Edit or create a theme
```

---

## Scheduling

```bash
genwal schedule list           # Show current schedule and systemd status
genwal schedule set 08:00      # Set daily run time (validates HH:MM format)
genwal schedule remove         # Remove the timer entirely
genwal schedule show           # Full systemd debug output
```

---

## CLI Reference

| Command | Description |
| :--- | :--- |
| `genwal run` | Generate and apply wallpaper now |
| `genwal preview` | Generate to `/tmp`, don't apply to OS |
| `genwal theme list` | List available themes |
| `genwal theme use <name>` | Switch active theme (writes to config) |
| `genwal theme edit <name>` | Create/edit a theme file |
| `genwal config get` | Print full config as JSON |
| `genwal config get <key>` | Print a specific value |
| `genwal config set <key> <val>` | Set any config key (dot.notation supported) |
| `genwal config edit` | Open config in `$EDITOR` |
| `genwal schedule list` | Show current schedule and status |
| `genwal schedule set <HH:MM>` | Set daily run time |
| `genwal schedule remove` | Remove the schedule |
| `genwal palette preview` | Preview 5 color palette variations |
| `genwal history` | View generated wallpaper history |
| `genwal history apply <N>` | Restore a previous wallpaper |
| `genwal providers list` | List all registered providers |
| `genwal seed` | Inspect the active deterministic seed |
| `genwal doctor` | Diagnose paths and config health |
| `genwal logs` | Tail systemd service logs |
| `genwal uninstall` | Completely remove Gen-Wal |
