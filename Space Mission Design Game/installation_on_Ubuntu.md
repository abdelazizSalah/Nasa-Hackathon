# Ubuntu 22.04: setup and desktop controls

## Install with Python 3.12

The game requires Python 3.12 or newer. Ubuntu 22.04's default Python 3.10 and legacy `python`/`pip` commands are not sufficient. Use an isolated interpreter; do not replace the system Python.

```bash
cd "$HOME/Desktop/Nasa-Hackathon/Space Mission Design Game"
curl -LsSf https://astral.sh/uv/install.sh | sh
"$HOME/.local/bin/uv" python install 3.12
"$HOME/.local/bin/uv" venv --seed --python 3.12 .venv
"$HOME/.local/bin/uv" pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python main.py
```

If curl is missing, install it with `sudo apt update` and `sudo apt install curl`. See the [official uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/). Cached mode needs neither a local GMAT installation nor internet after setup.

## Window disappears after Alt-Tab

The updated Linux launcher starts in a **titled 1280x720 resizable window**, so GNOME/VMware can keep it in the normal application switcher. Return to the **Mission Forge** window with Alt-Tab or its taskbar entry, then **click inside the game** to resume mouse look. Focus loss releases cursor capture and freezes walking; menus keep the cursor free.

F11 toggles a desktop-sized borderless window and restores the original titled window. Linux does not request an exclusive display mode or change the VM's display resolution. You can also start in desktop-sized mode:

```bash
.venv/bin/python main.py --fullscreen
```

For the most conservative VM launch:

```bash
.venv/bin/python main.py --windowed --mouse-mode warp
```

## Mouse does not turn the camera

Auto mode first requests native relative input. Some X11/VM desktops report `XF86-DGA missing` and cannot supply it; the game then falls back to recentering using the **actual game-window dimensions**, rather than the detected monitor size. Use `--mouse-mode warp` to select this fallback directly and skip the unsupported relative-mode request.

If the VM's mouse integration also prevents cursor warping, use the fallback that needs no capture or warping:

```bash
.venv/bin/python main.py --windowed --mouse-mode drag
```

In drag mode, **hold the right mouse button and move the mouse to look**. Release it to reposition the pointer; left-click still operates menus. The game displays a reminder while exploring. Arrow turning remains available in every mode. Do not grant raw `/dev/input` permissions or run the game as root.

## Game looks zoomed or stretched

The updated camera takes its aspect ratio from the rendered client area. It preserves the same vertical field of view as a 75-degree horizontal view at 16:9, expanding the horizontal view for wide displays such as 2560x974. Resize the window or toggle F11; you should see more of the scene horizontally rather than a narrower vertical view. UI and click targets continue to resize together.

## Manual acceptance on Ubuntu

1. Start windowed and close the welcome panel. Verify looking up/down/left/right and W/S, A/D and Shift movement.
2. Alt-Tab to another app. The cursor must be free and movement must stop.
3. Alt-Tab back and click inside Mission Forge. Mouse look must resume without a sudden turn.
4. Open/close a book, workstation and pause panel; verify their buttons and cursor behavior.
5. Resize wide/narrow and toggle F11 twice. Check that the room remains proportionate and the titled window returns.
6. Repeat with `--mouse-mode warp`; if the VM blocks warping, verify `--mouse-mode drag` and right-button look.

Diagnostics are in `runtime/graphics-smoke.json` after an automatic smoke run:

```bash
.venv/bin/python main.py --windowed --mouse-mode warp --smoke-seconds 8
```

The report records OS, window dimensions, display mode, camera field of view and mouse mode. The smoke run exits automatically; the welcome panel intentionally leaves the pointer free. Automated fallback/projection tests and Windows rendering are verified; physical Ubuntu/GNOME/VM mouse and Alt-Tab acceptance still require this checklist.
