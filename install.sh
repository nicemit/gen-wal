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

# 1. Pre-flight Checks
log "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    error "Python3 is not installed. Please install it: sudo apt install python3"
fi

if ! command -v systemctl &> /dev/null; then
    error "systemd is not available. This script is designed for systemd-based Linux distributions."
fi

PROJECT_DIR=$(pwd)
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    error "requirements.txt not found in $PROJECT_DIR"
fi

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

# 4. Setup Directories
SERVICE_DIR="$HOME/.config/systemd/user"
CACHE_DIR="$HOME/.cache/gen-wal"

mkdir -p "$SERVICE_DIR"
mkdir -p "$CACHE_DIR"

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

cat > "$PROJECT_DIR/gen-wal.timer" <<EOF
[Unit]
Description=Run Gen-Wal Daily

[Timer]
OnCalendar=daily
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
