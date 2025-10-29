#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

SESSION_FILE = Path.home() / ".config" / "hypr" / "session.json"

APP_MAP = {
    "firefox": "firefox",
    "code": "code",
    "kitty": "kitty",
    "thunar": "thunar",
    "org.gnome.Nautilus": "nautilus",
    "Alacritty": "alacritty",
    "chrome-chatgpt.com__-Default": "chromium -app=https://chat.openai.com",
    "chrome-keep.google.com__-Default": "chromium -app=https://keep.google.com",
    "chrome-drive.google.com__-Default": "chromium -app=https://drive.google.com",
    "chrome-web.whatsapp.com__-Default": "chromium -app=https://web.whatsapp.com",
    "li.oever.aether": "aether",
    "org.gnome.Evince": "evince",
    "Brave-browser": "brave-browser",
    "dev.zed.Zed": "zeditor",
}


def notify(msg: str, urgency: str = "normal"):
    """Send desktop notification using notify-send"""
    subprocess.run(["notify-send", "-u", urgency, "Hypr Session", msg])


def get_clients():
    """Return the JSON from hyprctl clients -j"""
    result = subprocess.run(
        ["hyprctl", "clients", "-j"], capture_output=True, text=True
    )
    if result.returncode != 0:
        notify("Failed to get clients from Hyprland.", "critical")
        sys.exit(1)
    return json.loads(result.stdout)


def save_session():
    """Save all running clients to JSON file"""
    clients = get_clients()
    session_data = []

    for c in clients:
        if not c.get("class"):
            continue
        session_data.append(
            {
                "class": c["class"],
                "workspace": c["workspace"]["name"] if c.get("workspace") else None,
            }
        )

    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f, indent=2)

    notify(f"Session saved ({len(session_data)} apps).")


def restore_session():
    """Restore saved apps on their respective workspaces"""
    if not SESSION_FILE.exists():
        notify("No saved session found.", "critical")
        sys.exit(1)

    with open(SESSION_FILE) as f:
        session_data = json.load(f)

    restored = 0
    skipped = 0

    for entry in session_data:
        app_class = entry["class"]
        workspace = entry["workspace"] or "1"
        cmd = APP_MAP.get(app_class)

        if not cmd:
            skipped += 1
            continue

        launch = f"[workspace {workspace}] uwsm app -- {cmd}"
        subprocess.run(["hyprctl", "dispatch", "exec", launch])
        restored += 1

    msg = f"Restored {restored} apps"
    if skipped:
        msg += f" (skipped {skipped} unknown)"
    notify(msg, "low")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        notify("Usage: hypr_session.py [save|restore]", "normal")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action == "save":
        save_session()
    elif action == "restore":
        restore_session()
    else:
        notify("Invalid argument. Use 'save' or 'restore'.", "critical")
