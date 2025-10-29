#!/bin/bash

#!/bin/bash
set -e

SCRIPT_NAME="hypr-session"
INSTALL_DIR="$HOME/.local/bin"
SCRIPT_PATH="$INSTALL_DIR/$SCRIPT_NAME"
CONFIG_FILE="$HOME/.config/hypr/autostart.conf"
SRC_SCRIPT="./hypr_session.py"

echo "Installing Hyprland Session Saver..."

# 1. Ensure local bin exists
mkdir -p "$INSTALL_DIR"

# 2. Copy script
if [[ ! -f "$SRC_SCRIPT" ]]; then
    echo "Error: Cannot find $SRC_SCRIPT. Run this installer from your project folder."
    exit 1
fi
cp "$SRC_SCRIPT" "$SCRIPT_PATH"

# 3. Make executable
chmod +x "$SCRIPT_PATH"

# 4. Ensure PATH includes ~/.local/bin
# if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc" 2>/dev/null; then
#     echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
#     echo "Added ~/.local/bin to PATH (reload your shell after install)."
# fi
#
# 5. Add Hyprland hooks if not already present
if [[ -f "$CONFIG_FILE" ]]; then
    if ! grep -q "hypr-session" "$CONFIG_FILE"; then
        echo "" >> "$CONFIG_FILE"
        echo "# --- Session Saver Integration ---" >> "$CONFIG_FILE"
        # echo "exec-on = lock, hypr-session save" >> "$CONFIG_FILE"
        # echo "exec-on = prelogout, hypr-session save" >> "$CONFIG_FILE"
        # echo "exec-on = shutdown, hypr-session save" >> "$CONFIG_FILE"
        echo "exec-once = hypr-session restore" >> "$CONFIG_FILE"
        echo "Added hooks to $CONFIG_FILE"
    else
        echo "Hyprland config already contains session saver hooks."
    fi
else
    echo "Warning: Hyprland config not found at $CONFIG_FILE — skipping hook setup."
fi

echo "Installation complete."
echo "Run 'hypr-session save' or 'hypr-session restore' to test."

