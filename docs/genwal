#!/bin/bash

# Gen-Wal Installer
# Strict error handling: Exit on any error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[GEN-WAL]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 1. Pre-flight & Bootstrap
log "Checking prerequisites..."

# Install system dependencies if on Debian/Ubuntu
if command -v apt-get &> /dev/null; then
    log "Debian/Ubuntu detected. Ensuring dependencies..."
    # We use sudo if available, otherwise hope for the best (or running as root)
    SUDO=""
    if command -v sudo &> /dev/null; then SUDO="sudo"; fi
    
    # Only update/install if missing
    if ! command -v git &> /dev/null || ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
         $SUDO apt-get update -qq
         $SUDO apt-get install -y python3 python3-venv python3-pip git curl -qq
    fi
fi

if ! command -v python3 &> /dev/null; then
    error "Python3 is not installed. Please install it."
fi

if ! command -v git &> /dev/null; then
    error "Git is not installed. Please install it."
fi

# Detect if running via curl/pipe (helper to find where we are)
PROJECT_DIR=$(pwd)
INSTALL_DIR="$HOME/.gen-wal"

if [ ! -f "$PROJECT_DIR/requirements.txt" ]; then
    log "Running in bootstrap mode (curl | bash detected or not in source dir)."
    
    if [ -d "$INSTALL_DIR" ]; then
        log "Updating existing installation in $INSTALL_DIR..."
        cd "$INSTALL_DIR"
        git pull
    else
        log "Cloning Gen-Wal to $INSTALL_DIR..."
        git clone https://github.com/nicemit/gen-wal.git "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
    
    # Re-run the installer from the correct directory
    log "Handing off to local installer..."
    exec ./install.sh
    exit 0
fi

# We are now strictly inside the repository
REQUIREMENTS_FILE="requirements.txt"
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    error "requirements.txt not found in $(pwd). Something went wrong."
fi

# --- Interactive Setup ---
echo ""
log "🎨 Let's set up your profile."
if [ -z "$USER_NAME" ]; then
    read -p "What's your name? (Default: User): " USER_NAME
fi
USER_NAME=${USER_NAME:-User}

if [ -z "$FOCUS" ]; then
    echo "What is your main focus/vibe right now?"
    echo "Examples: 'Ruthless Founder', 'Calm Stoic', 'Creative Artist', 'Disciplined Athlete'"
    read -p "Your Focus (Default: Stoic): " FOCUS
fi
FOCUS=${FOCUS:-Stoic}

if [ -z "$TIME" ]; then
    read -p "Wallpaper refresh time (HH:MM, default 06:30): " TIME
fi
TIME=${TIME:-06:30}
echo ""

# 2. Setup Virtual Environment
log "Setting up Python Virtual Environment..."

# Check if we can create a venv (python3-venv might be missing on some Debians)
if ! python3 -m venv venv; then
    error "Failed to create virtual environment. You might need to install 'python3-venv'.\nRun: sudo apt install python3-venv"
fi

source venv/bin/activate

# 3. Install Dependencies
log "Installing dependencies..."
if ! pip install -r requirements.txt; then
    error "Failed to install dependencies from requirements.txt"
fi

PYTHON_EXEC="$PROJECT_DIR/venv/bin/python"
log "Using Python: $PYTHON_EXEC"

# 4. Setup Directories & Config
SERVICE_DIR="$HOME/.config/systemd/user"
CACHE_DIR="$HOME/.cache/gen-wal"
CONFIG_DIR="$HOME/.config/gen-wal" # Not used by code yet, code uses local config.yaml, but let's stick to repo structure for now.

mkdir -p "$SERVICE_DIR"
mkdir -p "$CACHE_DIR"

# Generate Profile
PROFILE_PATH="$PROJECT_DIR/profiles/user_profile.md"
if [ ! -f "$PROFILE_PATH" ]; then
    log "Generating User Profile..."
    cat > "$PROFILE_PATH" <<EOF
# $USER_NAME's Gen-Wal Profile

## Core Identity
- **Name:** $USER_NAME
- **Current Focus:** $FOCUS

## Themes
- Discipline
- Consistency
- Growth
- Focus

## Preferred Styles
- Minimalist
- High Contrast
- Cinematic
EOF
fi

# Generate Config
CONFIG_PATH="$PROJECT_DIR/config.yaml"
if [ ! -f "$CONFIG_PATH" ]; then
    log "Generating Configuration..."
    cat > "$CONFIG_PATH" <<EOF
# Gen-Wal Configuration

# Profile Settings
profile_provider: "local_file"
profile_path: "profiles/user_profile.md"

# Providers (Defaulting to Pollinations for zero-setup)
quote_provider: "pollinations:text" 
image_provider: "pollinations:image"
image_prompt_provider: "pollinations:text"

# Unified Pollinations Configuration
pollinations:
  image:
    model: "flux" 
    nologo: true
  text:
    model: "openai"

# Rendering
resolution:
  width: 1920
  height: 1080

text_position: "bottom_center"
text_padding: 80
font_size: 50

# Prompts
prompts:
  quote: |
    You are a motivational coach for $USER_NAME who is focused on $FOCUS. 
    Generate a single, short, punchy, direct motivational quote (max 20 words).
    Do not explain. Do not use quotes around the text.
    
    PROFILE:
    {profile_content}

  image_description: |
    Generate a concise visual description for an image to accompany this motivational quote. 
    Focus on abstract, nature, or technological themes fitting a $FOCUS vibe. No text in the image. 
    Max 15 words.
    
    QUOTE: {quote}
    PROFILE: {profile_content}

# Wallpaper Settings
wallpaper_settings:
  apply_wallpaper: true
  save_path: "$CACHE_DIR/current_wallpaper.jpg"
EOF
fi

# 5. Create Systemd Service
log "Creating Systemd Service..."

cat > "$PROJECT_DIR/gen-wal.service" <<EOF
[Unit]
Description=Gen-Wal: Motivational Wallpaper Generator
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=$PROJECT_DIR
ExecStart=$PYTHON_EXEC main.py
Environment="DISPLAY=:0"
# Attempt to find the user's DBus session (required for gsettings)
Environment="DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus"
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF

# Default to 06:30 AM if TIME not set (redundant check but safe)
RUN_TIME="${TIME:-06:30}"
log "Setting up daily timer (Time: $RUN_TIME)..."

cat > "$PROJECT_DIR/gen-wal.timer" <<EOF
[Unit]
Description=Run Gen-Wal Daily at $RUN_TIME

[Timer]
OnCalendar=*-*-* $RUN_TIME:00
Persistent=true
Unit=gen-wal.service

[Install]
WantedBy=timers.target
EOF

# 6. Install Service
log "Installing Systemd units to $SERVICE_DIR..."
mv "$PROJECT_DIR/gen-wal.service" "$SERVICE_DIR/"
mv "$PROJECT_DIR/gen-wal.timer" "$SERVICE_DIR/"

# 7. Enable and Reload
log "Enabling systemd timer..."
systemctl --user daemon-reload
systemctl --user enable --now gen-wal.timer

log "Installation Complete! 🚀"
log "To test it immediately, run: systemctl --user start gen-wal.service"
log "Check logs with: journalctl --user -u gen-wal.service"
