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

# 4. Remove Config
CONFIG_DIR="$HOME/.config/genwal"
if [ -d "$CONFIG_DIR" ]; then
    log "Removing configuration at $CONFIG_DIR..."
    rm -rf "$CONFIG_DIR"
fi

# 5. Remove Themes
THEMES_DIR="$HOME/.local/share/genwal"
if [ -d "$THEMES_DIR" ]; then
    log "Removing themes at $THEMES_DIR..."
    rm -rf "$THEMES_DIR"
fi

# 6. Remove History/Cache
CACHE_DIR="$HOME/.cache/genwal"
if [ -d "$CACHE_DIR" ]; then
    log "Cleaning up history and cache at $CACHE_DIR..."
    rm -rf "$CACHE_DIR"
fi

# 7. Remove CLI Tool
CLI_PATH="$HOME/.local/bin/genwal"
if [ -f "$CLI_PATH" ]; then
    log "Removing CLI tool..."
    rm "$CLI_PATH"
fi

log "Uninstallation Complete. Local files and schedule have been removed."
