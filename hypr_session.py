#!/usr/bin/env python3

import json
import subprocess
import sys
import os
from pathlib import Path

SESSION_FILE = Path.home() / ".config" / "hypr" / "session.json"

APP_MAP = {
    "firefox": "firefox",
    "code": "code",
    "thunar": "thunar",
    "org.gnome.Nautilus": "nautilus",
    "chrome-chatgpt.com__-Default": "chromium -app=https://chat.openai.com",
    "chrome-keep.google.com__-Default": "chromium -app=https://keep.google.com",
    "chrome-drive.google.com__-Default": "chromium -app=https://drive.google.com",
    "chrome-web.whatsapp.com__-Default": "chromium -app=https://web.whatsapp.com",
    "chrome-github.com__-Default": "chromium -app=https://github.com",
    "Spotify": "spotify",
    "Brave-browser": "brave-browser",
    "obsidian": "obsidian",
    "org.gnome.Calculator": "gnome-calculator",
    "chromium": "chromium",
    "com.obsproject.Studio": "obs",
}


def notify(msg: str, urgency: str = "normal"):
    subprocess.run(["notify-send", "-u", urgency, "Hypr Session", msg])


def get_clients():
    result = subprocess.run(
        ["hyprctl", "clients", "-j"], capture_output=True, text=True
    )
    if result.returncode != 0:
        notify("Failed to get clients from Hyprland.", "critical")
        sys.exit(1)
    return json.loads(result.stdout)


def get_child_pid(pid: int):
    """Find the shell or nvim process that is a child of Alacritty."""
    try:
        ps = (
            subprocess.run(
                ["ps", "--ppid", str(pid), "-o", "pid,comm="],
                capture_output=True,
                text=True,
            )
            .stdout.strip()
            .splitlines()
        )
        if not ps:
            return None
        # Prefer nvim > zsh/bash/fish
        for line in ps:
            if "nvim" in line:
                return int(line.split()[0])
        for line in ps:
            if any(sh in line for sh in ["zsh", "bash", "fish"]):
                return int(line.split()[0])
        return int(ps[0].split()[0])
    except Exception:
        return None


def get_cwd(pid: int):
    """Get CWD of process (using /proc)."""
    try:
        return os.readlink(f"/proc/{pid}/cwd")
    except Exception:
        return None


def is_nvim_running(pid: int):
    """Check recursively if nvim is running in the process tree."""
    try:
        children = (
            subprocess.run(["pgrep", "-P", str(pid)], capture_output=True, text=True)
            .stdout.strip()
            .split()
        )
        for child in children:
            comm = subprocess.run(
                ["ps", "-p", child, "-o", "comm="], capture_output=True, text=True
            ).stdout.strip()
            if comm == "nvim":
                return True
            if is_nvim_running(int(child)):
                return True
        return False
    except Exception:
        return False


def save_session():
    clients = get_clients()
    session_data = []

    for c in clients:
        app_class = c.get("class")
        if not app_class:
            continue

        workspace = c["workspace"]["name"] if c.get("workspace") else "1"
        pid = c.get("pid")

        entry = {"class": app_class, "workspace": workspace}

        if app_class.lower() == "alacritty" and pid:
            child_pid = get_child_pid(pid)
            cwd = get_cwd(child_pid or pid)
            in_nvim = is_nvim_running(pid)
            entry["cwd"] = cwd
            entry["in_nvim"] = in_nvim
        else:
            entry["cwd"] = None
            entry["in_nvim"] = False

        session_data.append(entry)

    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f, indent=2)

    notify(f"Session saved ({len(session_data)} apps).")


def restore_session():
    if not SESSION_FILE.exists():
        notify("No saved session found.", "critical")
        sys.exit(1)

    with open(SESSION_FILE) as f:
        session_data = json.load(f)

    restored, skipped = 0, 0

    for entry in session_data:
        app_class = entry["class"]
        workspace = entry.get("workspace", "1")
        cwd = entry.get("cwd")
        in_nvim = entry.get("in_nvim", False)

        if app_class.lower() == "alacritty":
            if cwd and Path(cwd).exists():
                if in_nvim:
                    cmd = f"alacritty -e nvim '{cwd}'"
                else:
                    cmd = f"alacritty --working-directory '{cwd}'"
            else:
                cmd = "alacritty"
        else:
            cmd = APP_MAP.get(app_class)

        if not cmd:
            skipped += 1
            continue

        launch = f"[workspace {workspace}] uwsm app -- {cmd}"
        subprocess.run(["hyprctl", "dispatch", "exec", launch])
        restored += 1

    msg = f"Restored {restored} apps"
    if skipped:
        msg += f" (skipped {skipped})"
    notify(msg, "low")


def clear_session():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
        notify("Session cleared. It won’t be restored next time.")
    else:
        notify("No session to clear.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        notify("Usage: hypr-session [save|restore|clear]")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action == "save":
        save_session()
    elif action == "restore":
        restore_session()
    elif action == "clear":
        clear_session()
    else:
        notify("Invalid argument. Use save|restore|clear.", "critical")
