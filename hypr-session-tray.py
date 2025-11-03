#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

HYPR_SESSION_CMD = "hypr-session"

# fallback icon (you can replace with any .svg or .png)
ICON_PATH = Path.home() / ".local/share/icons/hypr-session.png"


def run_command(action):
    """Run hypr-session save/restore/clear with notify-send"""
    subprocess.run([HYPR_SESSION_CMD, action])
    subprocess.run(["notify-send", f"Hypr Session: {action.capitalize()} executed"])


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Prefer system icon, else use fallback
    icon = QIcon.fromTheme("preferences-system-windows")
    if icon.isNull():
        # optional: create a default icon if not exists
        if not ICON_PATH.exists():
            from PIL import Image, ImageDraw

            img = Image.new("RGBA", (64, 64), (255, 255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.text((64, 64), "Hy", fill="black")
            ICON_PATH.parent.mkdir(parents=True, exist_ok=True)
            img.save(ICON_PATH)
        icon = QIcon(str(ICON_PATH))

    tray = QSystemTrayIcon(icon)
    tray.setToolTip("Hypr Session Manager")
    tray.setVisible(True)

    menu = QMenu()

    save_action = QAction("💾 Save Session")
    restore_action = QAction("♻ Restore Session")
    clear_action = QAction("🧹 Clear Session")
    quit_action = QAction("❌ Quit")

    save_action.triggered.connect(lambda: run_command("save"))
    restore_action.triggered.connect(lambda: run_command("restore"))
    clear_action.triggered.connect(lambda: run_command("clear"))
    quit_action.triggered.connect(app.quit)

    menu.addAction(save_action)
    menu.addAction(restore_action)
    menu.addAction(clear_action)
    menu.addSeparator()
    menu.addAction(quit_action)

    tray.setContextMenu(menu)

    tray.show()
    app.exec()


if __name__ == "__main__":
    main()
