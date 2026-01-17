#!/bin/bash

# Gen-Wal Uninstaller
# Removes Gen-Wal and all its components

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[GEN-WAL]${NC} $1"
}

warn() {
    echo -e "${RED}[WARNING]${NC} $1"
}

# 1. Stop and Disable Systemd Units
log "Stopping systemd background tasks..."
systemctl --user stop gen-wal.timer 2>/dev/null || true
systemctl --user disable gen-wal.timer 2>/dev/null || true
systemctl --user stop gen-wal.service 2>/dev/null || true

# 2. Remove Systemd Files
SERVICE_DIR="$HOME/.config/systemd/user"
if [ -f "$SERVICE_DIR/gen-wal.timer" ]; then
    log "Removing systemd timer..."
    rm "$SERVICE_DIR/gen-wal.timer"
fi

if [ -f "$SERVICE_DIR/gen-wal.service" ]; then
    log "Removing systemd service..."
    rm "$SERVICE_DIR/gen-wal.service"
fi

# Reload systemd to recognize removal
systemctl --user daemon-reload

# 3. Remove Installation Directory
INSTALL_DIR="$HOME/.gen-wal"
if [ -d "$INSTALL_DIR" ]; then
    log "Removing application files at $INSTALL_DIR..."
    rm -rf "$INSTALL_DIR"
fi

# 4. Remove Cache (Optional)
CACHE_DIR="$HOME/.cache/gen-wal"
if [ -d "$CACHE_DIR" ]; then
    log "Cleaning up cache..."
    rm -rf "$CACHE_DIR"
fi

# 5. Config (Ask user or just notify)
CONFIG_DIR="$HOME/.config/gen-wal" # Note: install.sh didn't seem to create this explicitly in a std location, config is usually inside the repo.
# If config was inside the repo ($INSTALL_DIR), it's already gone.

log "Uninstallation Complete. Local files and schedule have been removed."
