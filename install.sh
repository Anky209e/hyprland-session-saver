#!/bin/bash
set -e

# --- Configuration ---
INSTALL_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.config/hypr-session"
HYPR_CONFIG_FILE="$HOME/.config/hypr/hyprland.conf"

SRC_MAIN_SCRIPT="./hypr_session.py"
SRC_TRAY_SCRIPT="./hypr-session-tray.py"
SRC_CONFIG="./config.py"

DEST_MAIN_SCRIPT="$INSTALL_DIR/hypr-session"
DEST_TRAY_SCRIPT="$INSTALL_DIR/hypr-session-tray"
DEST_CONFIG="$CONFIG_DIR/config.py"

# --- Helper Functions ---
function check_command() {
    command -v "$1" >/dev/null 2>&1
}

function print_info() {
    echo "[INFO] $1"
}

function print_success() {
    echo "✅ $1"
}

function print_warning() {
    echo "⚠️ [WARNING] $1"
}

function print_error() {
    echo "❌ [ERROR] $1"
    exit 1
}

# --- Installation Steps ---
echo "🚀 Installing Hyprland Session Saver..."

# 1. Check for source files
if [[ ! -f "$SRC_MAIN_SCRIPT" || ! -f "$SRC_TRAY_SCRIPT" || ! -f "$SRC_CONFIG" ]]; then
    print_error "One or more source files not found. Run this installer from the project folder."
fi

# 2. Ensure installation directories exist
mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"

# 3. Copy scripts and make them executable
print_info "Installing main script to $DEST_MAIN_SCRIPT..."
cp "$SRC_MAIN_SCRIPT" "$DEST_MAIN_SCRIPT"
chmod +x "$DEST_MAIN_SCRIPT"

print_info "Installing tray icon to $DEST_TRAY_SCRIPT..."
cp "$SRC_TRAY_SCRIPT" "$DEST_TRAY_SCRIPT"
chmod +x "$DEST_TRAY_SCRIPT"

# 4. Install default config if no user config exists
if [[ ! -f "$DEST_CONFIG" ]]; then
    print_info "Installing default configuration to $DEST_CONFIG..."
    cp "$SRC_CONFIG" "$DEST_CONFIG"
else
    print_info "User configuration already exists at $DEST_CONFIG. Skipping default config installation."
fi

# 5. Check if ~/.local/bin is in PATH
if [[ ! ":$PATH:" == *":$INSTALL_DIR:"* ]]; then
    print_warning "~/.local/bin is not in your PATH."
    echo "Please add the following line to your shell's configuration file (e.g., ~/.bashrc, ~/.zshrc):"
    echo '  export PATH="$HOME/.local/bin:$PATH"'
    echo "After adding it, restart your shell or run 'source ~/.your_shell_rc_file' for the changes to take effect."
else
    print_success "Installation directory is in your PATH."
fi

# 6. Check for Hyprland hook
HYPR_HOOK="exec-once = hypr-session restore"
if [[ -f "$HYPR_CONFIG_FILE" ]]; then
    if grep -q "hypr-session restore" "$HYPR_CONFIG_FILE"; then
        print_success "Hyprland restore hook already configured."
    else
        print_info "Adding restore hook to your Hyprland configuration."
        echo -e "\n# --- Hyprland Session Saver ---" >> "$HYPR_CONFIG_FILE"
        echo "$HYPR_HOOK" >> "$HYPR_CONFIG_FILE"
        print_success "Restore hook added to $HYPR_CONFIG_FILE."
    fi
else
    print_warning "Hyprland config not found at $HYPR_CONFIG_FILE."
    echo "To enable automatic session restore, please add the following line to your Hyprland config:"
    echo "  $HYPR_HOOK"
fi

# 7. Final instructions
echo ""
print_success "Installation complete!"
echo "You can now use the following commands:"
echo "  - hypr-session save      : Saves your current session."
echo "  - hypr-session restore   : Restores your last saved session."
echo "  - hypr-session clear     : Clears the saved session."
echo "  - hypr-session-tray    : Starts the tray icon for easy access."
echo ""
echo "To customize application mappings, edit the configuration file at:"
echo "  $DEST_CONFIG"
echo ""
echo "Enjoy your seamless Hyprland sessions! ✨"
