#!/usr/bin/env bash
set -euo pipefail

# --------------------------------------------------
# Colors & helpers
# --------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[GEN-WAL]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
die()  { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# If running via pipe (stdin not TTY) and script exists locally,
# Restart with TTY to allow interactive prompts.
if [ ! -t 0 ] && [ -f "install.sh" ]; then
    log "Pipe detected in source dir. Restarting with TTY..."
    exec bash install.sh < /dev/tty
fi

# --------------------------------------------------
# Pre-flight
# --------------------------------------------------
log "Checking prerequisites..."

if command -v apt-get >/dev/null 2>&1; then
    log "Debian/Ubuntu detected. Ensuring dependencies..."
    SUDO=""
    command -v sudo >/dev/null 2>&1 && SUDO="sudo"

    if ! command -v python3 >/dev/null 2>&1 || \
       ! command -v git >/dev/null 2>&1 || \
       ! command -v pip3 >/dev/null 2>&1; then
        $SUDO apt-get update -qq
        $SUDO apt-get install -y python3 python3-venv python3-pip git curl -qq
    fi
fi

command -v python3 >/dev/null 2>&1 || die "python3 not installed"
command -v git >/dev/null 2>&1 || die "git not installed"

# --------------------------------------------------
# Bootstrap detection
# --------------------------------------------------
PROJECT_DIR="$(pwd)"
INSTALL_DIR="$HOME/.gen-wal"

if [ ! -f "$PROJECT_DIR/requirements.txt" ]; then
    log "Bootstrap mode detected"

    if [ -d "$INSTALL_DIR" ]; then
        log "Updating existing install..."
        cd "$INSTALL_DIR"
        git pull
    else
        log "Cloning Gen-Wal..."
        git clone https://github.com/nicemit/gen-wal.git "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi

    exec bash install.sh < /dev/tty
fi

# --------------------------------------------------
# Hard guard (NO short-circuit expressions)
# --------------------------------------------------
REQUIREMENTS_FILE="requirements.txt"
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    die "requirements.txt not found"
fi

# --------------------------------------------------
# Interactive setup
# --------------------------------------------------
echo ""
log "🎨 Profile setup"

read -r -p "Your name (default: User): " USER_NAME
USER_NAME="${USER_NAME:-User}"

echo "Choose your Mindset Source:"
echo "  1) Stoic     (Meditations, Seneca)"
echo "  2) Deep Work (Atomic Habits, War of Art)"
echo "  3) Builder   (Hackers & Painters, Unix)"
echo "  4) Zen       (Mindfulness, Tao)"
read -r -p "Select [1-4] (default: 1): " FOCUS_CHOICE
FOCUS_CHOICE="${FOCUS_CHOICE:-1}"

read -r -p "When should this run? (HH:MM, default 06:30): " RUN_AT
RUN_AT="${RUN_AT:-06:30}"

# Normalize H:MM → HH:MM
if [[ "$RUN_AT" =~ ^[0-9]:[0-9]{2}$ ]]; then
    RUN_AT="0$RUN_AT"
fi

# Strict validation
if ! [[ "$RUN_AT" =~ ^[0-2][0-9]:[0-5][0-9]$ ]]; then
    die "Invalid time format: $RUN_AT"
fi

# --------------------------------------------------
# Python venv
# --------------------------------------------------
log "Setting up Python virtual environment..."
python3 -m venv venv || die "python3-venv missing"

source venv/bin/activate
pip install -r requirements.txt

PYTHON_EXEC="$PROJECT_DIR/venv/bin/python"
log "Using Python: $PYTHON_EXEC"

# --------------------------------------------------
# Directories (XDG Standard)
# --------------------------------------------------
SYSTEMD_DIR="$HOME/.config/systemd/user"
mkdir -p "$SYSTEMD_DIR"

# Ensure XDG directories via Python config helper
log "Configuring XDG directories..."
"$PYTHON_EXEC" -c "from src.config import ensure_xdg_dirs; ensure_xdg_dirs()"

# --------------------------------------------------
# Default Core Config (Zero-API Key)
# --------------------------------------------------
log "Setting default local-first configuration..."
CONFIG_DIR="$HOME/.config/genwal"
CONFIG_DEST="$CONFIG_DIR/config.json"
if [ ! -f "$CONFIG_DEST" ]; then
    cp "$PROJECT_DIR/config.example.json" "$CONFIG_DEST"
    log "Copied default configuration to $CONFIG_DEST"
fi

# --------------------------------------------------
# Systemd Service
# --------------------------------------------------
log "Creating systemd service..."

cat > "$SYSTEMD_DIR/gen-wal.service" <<EOF
[Unit]
Description=Gen-Wal Wallpaper Generator
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
WorkingDirectory=$PROJECT_DIR
ExecStart=$PYTHON_EXEC src/cli.py run
Environment=DISPLAY=:0
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus

[Install]
WantedBy=default.target
EOF

# --------------------------------------------------
# Systemd Timer
# --------------------------------------------------
log "Creating systemd timer (Time: $RUN_AT)"

cat > "$SYSTEMD_DIR/gen-wal.timer" <<EOF
[Unit]
Description=Run Gen-Wal daily at $RUN_AT

[Timer]
OnCalendar=*-*-* $RUN_AT:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

# --------------------------------------------------
# Enable
# --------------------------------------------------
log "Reloading systemd..."
systemctl --user daemon-reload

log "Enabling timer..."
systemctl --user enable --now gen-wal.timer

# --------------------------------------------------
# CLI Helper
# --------------------------------------------------
CLI_DEST="$HOME/.local/bin"
mkdir -p "$CLI_DEST"

# Copy CLI script and update INSTALL_DIR to match actual install location
log "Installing CLI tool..."

# We use sed to replace the default INSTALL_DIR with the one determined by this script ($PROJECT_DIR)
# This handles cases where user installs to a different location or runs from source
sed "s|INSTALL_DIR=\"\$HOME/.gen-wal\"|INSTALL_DIR=\"$PROJECT_DIR\"|g" "$PROJECT_DIR/genwal" > "$CLI_DEST/genwal"

chmod +x "$CLI_DEST/genwal"
log "Installed 'genwal' CLI to $CLI_DEST"

# Install Bash Autocompletion
BASH_COMP_DIR="$HOME/.local/share/bash-completion/completions"
mkdir -p "$BASH_COMP_DIR"
cp "$PROJECT_DIR/scripts/genwal-completion.bash" "$BASH_COMP_DIR/genwal"
log "Installed bash auto-completion"

# Check PATH
if [[ ":$PATH:" != *":$CLI_DEST:"* ]]; then
    warn "Your PATH does not include $CLI_DEST. You may need to add it to run 'genwal' directly."
fi

log "Installation Complete! 🚀"
echo ""
log "   - Config: ~/.config/genwal/config.json"
log "   - Themes: ~/.local/share/genwal/themes/"
log "   - Next run: Tomorrow at $RUN_AT"
echo ""
log "🔥 NEW: Use the CLI to manage everything!"
echo "   genwal config   # Edit settings easily"
echo "   genwal run      # Generate wallpaper now"
echo "   genwal logs     # See what happened"
echo ""
log "To test it immediately, run: genwal run"
