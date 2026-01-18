# Hyprland Session Saver ✨

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A lightweight and configurable session saver for Hyprland. Never lose your workspace again!

This tool saves the state of your open applications—including their workspaces, and for some apps, their current working directory or open files—and restores them automatically on your next startup.

## Features

-   **Save & Restore:** Save your entire session with a single command and have it restored automatically.
-   **Application-Specific Logic:**
    -   **Terminal Support (Alacritty):** Remembers the current working directory. It can even detect if you are running `nvim` and restore it.
    -   **Video Player (MPV):** Remembers the video file you were watching and restores it paused.
-   **Configurable:** Easily customize which applications are saved and how they are launched via a simple Python configuration file.
-   **System Tray Icon:** An optional tray icon for easy point-and-click access to save, restore, and clear session data.
-   **Easy Installation:** A simple installer script to get you up and running in minutes.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/anky209e/hyprland-session-saver
    cd hyprland-session-saver
    ```

2.  **Run the installer:**
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
    The installer will copy the necessary files to `~/.local/bin` and create a default configuration file at `~/.config/hypr-session/config.py`. It will also guide you through setting up your `hyprland.conf` for auto-restoration.

## Usage

### Command Line

-   `hypr-session save`: Saves the current session.
-   `hypr-session restore`: Restores the last saved session.
-   `hypr-session clear`: Removes the saved session file.

### System Tray

You can run `hypr-session-tray` (you may want to add this to your Hyprland startup config) to get a convenient tray icon with "Save", "Restore", and "Clear" actions.

## Customization

You can customize the application mappings by editing the configuration file:

`~/.config/hypr-session/config.py`

The `APP_MAP` dictionary maps the application's `class` (from `hyprctl clients`) to the command used to launch it. You can add your own applications or change the launch commands for existing ones.

For example, to add support for the Kitty terminal:

```python
APP_MAP = {
    # ... other apps
    "kitty": "kitty",
}
```

## Roadmap

Here are some of the planned features:

-   [ ] **TUI/Walker Integration:** Add a menu for saving/loading sessions using tools like Rofi or Wofi.
-   [ ] **Session Profiles:** Allow saving and loading different sessions for different tasks (e.g., "Work", "Gaming").
-   [ ] **More Application Support:** Add more specific handlers for popular applications.
-   [ ] **Daemon Mode:** An optional mode to save the session automatically in the background.

## Contributing

Contributions are welcome! If you have a feature request, bug report, or want to contribute to the code, please open an issue or a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
