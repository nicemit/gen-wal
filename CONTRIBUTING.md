# Contributing to Gen-Wal

Thanks for considering contributing! This is a personal project, but I love seeing how others use it.

## 🛠️ Development Setup

If you want to run Gen-Wal locally for development (without the systemd installer), follow these steps:

### 1. Clone & Setup
```bash
git clone https://github.com/nicemit/gen-wal.git
cd gen-wal

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Copy the example config to the root directory:
```bash
cp config.yaml.example config.yaml
# Or just create a simple one:
# touch config.yaml (The app has defaults, but adding your API keys helps)
```

### 3. Running Manually
You can trigger a run directly via Python:
```bash
python3 main.py
```
This will generate a wallpaper in `~/.cache/gen-wal/` and attempt to set it.

### 4. Running Tests
We use `unittest`. Please ensure all tests pass before submitting a PR.
```bash
python3 -m unittest discover tests
```

---

## 📂 Project Structure

- `src/`: Core logic
    - `providers/`: Adapters for different APIs (Pollinations, OpenAI, etc.)
    - `utils.py`: Desktop environment interaction code
    - `factory.py`: Dependency injection logic
- `profiles/`: Markdown files defining personas
- `install.sh`: The installer script (also serves as the CLI generator)

## 🤝 How can I help?

1.  **Add a Profile**: Created a cool "Cyberpunk" or "Nature" profile? Submit a PR adding it to `profiles/examples/`.
2.  **Fix Bugs**: If something breaks on your specific Linux distro (KDE, XFCE, Mate), fixes in `src/utils.py` are welcome.
3.  **Improve Providers**: Want to add a new Image Generator or LLM provider? Go for it.

## The Flow

1.  Fork the repo.
2.  Create your branch (`git checkout -b feature/amazing-profile`)
3.  Commit your changes.
4.  Open a Pull Request.

## Philosophy

*   **Keep it simple**: We don't need a heavy database or GUI.
*   **Local-first**: Prefer tools that can run on the user's machine.
*   **Flexible**: Allow users to change prompts and logic easily.

Happy hacking! 🧠
