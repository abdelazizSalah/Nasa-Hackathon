# Play Mission Forge

## Windows: clone and play

1. Clone this repository, or download its ZIP and **extract it first**.
2. Open `play/windows` and double-click **MissionForge.exe**.
3. Click **Start Exploring**. The game starts fullscreen; **F11** toggles windowed mode.

You do **not** need Python, pip, Ursina, internet or GMAT for **Cached** mode. All books, NASA textures and cached orbit data are inside the executable. First startup briefly unpacks its runtime; allow it time to open. This build targets **64-bit Windows** with an OpenGL-capable graphics driver. The executable is unsigned; use the repository's published SHA256 to check your copy if Windows displays a reputation notice.

From PowerShell, a windowed start is:

```powershell
.\play\windows\MissionForge.exe --windowed
```

## What to do first

Select **Flood Watch** at the Earth display. Follow the next-step guide through Payload, Power, Communications and Mission Planning; press **E** at tables and choose **Select & Pick**. Place all six contributions in Integration, press **M**, have the host **Validate & Approve**, then **Launch Now**.

For a verified first success: **Basic / Compact / Standard / Regional / Light / Solid**, **Source: Cached**, **Plan: Targeted**. Expected: EUR 91,000, 57 kg, 120 MB delivered and no energy/storage loss.

Read [the complete mission handbook](../output/pdf/mission-forge-complete-handbook.pdf) for every table, option, constraint and telemetry label, or [the short winning recipe](../output/pdf/Successful_Congigurations.pdf).

## Controls

| Input | Action |
| --- | --- |
| W / S | Forward / backward |
| A / D | Strafe left / right |
| Mouse | Look in all directions |
| Left / right arrows | Optional turning; choose a plan at the submission desk |
| Shift | Run; adjust 3-60 m/s through Esc > Settings |
| Space / Alt | Jump / hold crouch |
| E | Interact, pick, place or retrieve your contribution |
| I / M / N | Inventory / Mission Control / Multiplayer |
| Esc | Close panel or open pause |
| F11 | Toggle fullscreen |

## Play together on the same Wi-Fi (2, 3 or 4 players)

Every laptop must use the **same build/version**. One player presses **N > Host New Crew Mission**; up to three friends use **N > Join Friend** with that host's Wi-Fi IPv4 and six-digit code. Use the host address for every guest; do not use VPN/VM adapter addresses. Only the host starts a shared mission and approves readiness; roles distribute automatically.

If Windows asks, allow the host game on the trusted/private network you are using. Incoming **TCP 8765** must reach the host. Guest Wi-Fi isolation can prevent laptop-to-laptop traffic; no internet/router port forwarding is needed. The lobby displays wrong-code/version errors and times out an unconfirmed join. Leave Session to retry.

## Saves, settings and logs

Windows executable writes to `%LOCALAPPDATA%\MissionForge\runtime`: `player_settings.json`, `campaign.json`, `crew-save.json`, reading progress, reports and `game.log`. They survive executable restarts/replacement. No write access to the repo or executable folder is needed. A failed startup displays the log path; copy `game.log` when reporting a problem.

Source runs keep their existing `Space Mission Design Game/runtime` folder; source and packaged saves are separate. A one-file executable extracts read-only assets into a temporary directory, then removes them at exit. Cached mode always reads the shipped trajectory. Live-generated trajectories/logs go into persistent user data.

## Optional: Live GMAT

Cached works immediately. Live requires **GMAT R2026a** installed separately on the **host only**; GMAT is not redistributed inside this executable.

Set `GMAT_BIN` to the GMAT installation directory or `bin/GmatConsole.exe` before launching, or place `local_config.json` beside MissionForge.exe:

```json
{"gmat_bin": "C:/path/to/gmat-win-R2026a"}
```

Choose **Source: Live** in M. Preparation may take time; failures are shown rather than silently switching to Cached. Friends can use Cached or join the host without installing GMAT.

## Linux / Arch

The checked-in `.exe` is a **Windows binary**, not a Linux executable. A native Linux binary must be built on Linux; this Windows workspace cannot verify it. Maintainers can run the repository's **Build Mission Forge** GitHub Actions workflow and download the Linux artifact, or build locally using [the game setup instructions](../Space%20Mission%20Design%20Game/README.md) followed by:

```sh
cd "Space Mission Design Game"
.venv/bin/python -m pip install -r requirements-build.txt
.venv/bin/python scripts/build_executable.py
chmod +x ../play/linux/MissionForge
../play/linux/MissionForge
```

The resulting binary includes Python and game dependencies, but still uses the OS display/graphics driver and OpenGL/X11 libraries. Native Arch acceptance remains pending. Windows and Linux players can share a LAN room when their game content/version matches.

## Rebuild and verify (maintainers)

On Windows, after the normal source setup:

```powershell
cd "Space Mission Design Game"
.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.venv\Scripts\python.exe scripts/build_executable.py
..\play\windows\MissionForge.exe --verify-package
```

Build on the target OS; PyInstaller does not cross-compile Windows to Linux. `--verify-package` tests bundled resources, offline science success and real localhost 2/3/4-player integration/launch, then renders briefly. See `package-check.json`, `graphics-smoke.json` and `package-smoke.png` in user runtime. Actual separate-laptop Wi-Fi remains a manual check.

Commit the rebuilt executable, SHA256 and source changes together to make the new build available after clone. The build script is repeatable; exact binary hashes can vary between builds. The repository includes asset credits under `Space Mission Design Game/content/materials/README.md`; third-party license files accompany the executable under `play/licenses`.
