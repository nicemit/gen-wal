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
# Directories
# --------------------------------------------------
SYSTEMD_DIR="$HOME/.config/systemd/user"
CACHE_DIR="$HOME/.cache/gen-wal"

mkdir -p "$SYSTEMD_DIR" "$CACHE_DIR"

# --------------------------------------------------
# Profile Setup
# --------------------------------------------------
PROFILE_PATH="$PROJECT_DIR/profiles/user_profile.md"
if [ ! -f "$PROFILE_PATH" ]; then
    case "$FOCUS_CHOICE" in
        2)
            log "Applying Deep Work Profile..."
            cp "$PROJECT_DIR/profiles/examples/deep_work.md" "$PROFILE_PATH"
            ;;
        3)
            log "Applying Builder Profile..."
            cp "$PROJECT_DIR/profiles/examples/builder.md" "$PROFILE_PATH"
            ;;
        4)
            log "Applying Zen Profile..."
            cp "$PROJECT_DIR/profiles/examples/zen.md" "$PROFILE_PATH"
            ;;
        *)
            log "Applying Stoic Profile..."
            cp "$PROJECT_DIR/profiles/examples/stoic.md" "$PROFILE_PATH"
            ;;
    esac
fi

# --------------------------------------------------
# Config
# --------------------------------------------------
CONFIG_PATH="$PROJECT_DIR/config.yaml"
if [ ! -f "$CONFIG_PATH" ]; then
cat > "$CONFIG_PATH" <<EOF
profile_provider: local_file
# Default: Use the selected user_profile.md
profile_path: "profiles/user_profile.md"

# Option: Random Rotation (Reference Frames)
# profile_path:
#   - "profiles/examples/stoic.md"
#   - "profiles/examples/deep_work.md"
#   - "profiles/examples/builder.md"
#   - "profiles/examples/zen.md"

quote_provider: pollinations:text
image_provider: pollinations:image
image_prompt_provider: pollinations:text

resolution:
  width: 1920
  height: 1080

watermark:
  enabled: true
  position: "bottom_right"
  font_size: 25
  opacity: 180

wallpaper_settings:
  apply_wallpaper: true
  save_path: "$CACHE_DIR/current_wallpaper.jpg"
EOF
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
ExecStart=$PYTHON_EXEC main.py
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

# Check PATH
if [[ ":$PATH:" != *":$CLI_DEST:"* ]]; then
    warn "Your PATH does not include $CLI_DEST. You may need to add it to run 'genwal' directly."
fi

log "Installation Complete! 🚀"
echo ""
log "   - Config: $PROJECT_DIR/config.yaml"
log "   - Profile: $PROFILE_PATH"
log "   - Next run: Tomorrow at $RUN_AT"
echo ""
log "🔥 NEW: Use the CLI to manage everything!"
echo "   genwal config   # Edit settings easily"
echo "   genwal run      # Generate wallpaper now"
echo "   genwal logs     # See what happened"
echo ""
log "To test it immediately, run: genwal run"
