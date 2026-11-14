# Mission Forge - Phase 3

Current navigation: Up/Down move forward/backward; Left/Right strafe sideways relative to your heading. A turns left and D turns right. The mouse stays free for interface controls and does not turn the camera. Reading/pause/design panels freeze movement and turning. Panel arrow controls still select cards/options. This supersedes earlier mouse-look and turn-with-arrows descriptions.

The default scene is a walkable hub, Learning Lab, and working spacecraft design bay. Campaign progression and the in-game GMAT bridge remain later phases. The Phase 1 renderer and separate real GMAT proof are retained.

## Try Phase 3: linked engineering choices

Restart the game to load the current code, then approach the **spacecraft design bay on the right** of mission control and press **E**. No new dependencies are needed. Click options or use Up/Down to focus a row and Left/Right/Enter to change its selection. **U / Undo** reverses the last change; **Backspace / Reset** restores the default. Escape closes the panel. Choices remain when you reopen it during this session; disk saves are Phase 4.

The panel shows budget, mass, peak-power margin, minimum battery energy, peak storage, and data delivered. Bracketed numbers compare with the immediately preceding selection, undo, or reset. A highlighted limiting factor explains what fails; additional failures stay listed. The spacecraft's sensor, solar-panel size, and radio change both in the panel and above the bay. A compact resource summary remains visible outside the panel.

### Suggested trade-off demo

Start from Reset and select these options in order:

| Choice | Visible consequence |
| --- | --- |
| Default: Basic / Compact / Standard / Regional / Light | All eight preview checks pass: 57 kg, 89 credits, 300/300 MB delivered. |
| Advanced sensor | Quality rises from 1 to 2; mass rises 8 kg, cost rises 15 credits, peak load rises 20 W, and expected data doubles. Power and delivery checks fail. |
| Extended power | Larger solar panels appear and power margin becomes +53 W. Spacecraft mass becomes 75 kg, exceeding the light launch's 70 kg capacity. Data still fails. |
| Heavy launch | Mass capacity becomes 100 kg, but cost rises to 128 credits. The remaining data bottleneck is still visible. |
| Fast radio | Data delivery reaches 600/600 MB. Mass is 79 kg, total cost 138/145 credits, and all eight preview checks pass. |
| Wide orbit preset | Observing/contact/eclipse assumptions change. This expensive advanced configuration now costs 148/145 credits, so budget fails. Undo returns to the regional design. |

There are **seven feasible configurations out of 32 combinations**, including both basic and advanced sensors. A passing preview is a trade study, not launch clearance or mission completion.

### Model assumptions and boundaries

All parameters in `content/design_catalog.json` are invented educational values, not NASA hardware specifications. The fixed bus includes structure, computer, pointing, and storage. Total cost includes that bus, selected hardware, launch, and the preset's ground-service cost for a fixed 12-month teaching scenario. No multi-year reliability prediction is made.

The one-minute preview begins with a full battery. Observations occur at the beginning of sunlight; contacts occur at the end of the orbit cycle. Regional: 90 minutes, 60 sunlit, 10 observing, 6 in contact. Wide: 100 minutes, 55 sunlit, 12 observing, 4 in contact. These are curated opportunities, not GMAT-computed visibility or coverage.

Energy is integrated in Wh using watts multiplied by elapsed hours; storage/data are in MB and rates in MB/min. Solar energy can be curtailed when the battery is full. Shortage reduces productive activity proportionally and fails the energy check. Overflow is explicitly counted as lost data. Every required observation's data must be delivered by the end of this cycle to pass the simplified delivery check.

The **peak-power check is a conservative design rule**: solar generation must cover bus + sensor + radio simultaneously. A real spacecraft could use battery power or scheduling for a transient peak; this preview deliberately enforces the simpler conservative requirement separately from its energy simulation. This avoids presenting a negative margin as a universal physical impossibility.

Eight checks: science grade, total budget, launch mass, launcher/orbit compatibility, conservative peak power, cycle energy, storage overflow, and full-cycle data delivery. A separate budget/compatibility result prevents a powerful but unaffordable or incompatible design from passing.

### Phase 3 verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/verify_design.py
.\.venv\Scripts\python.exe scripts/verify_hub.py
```

`verify_design.py --review` leaves the advanced passing design open. Add `--failing` to inspect a sensor-only upgrade with visible deficits. The harness calls the same selection/input paths as the panel, checks undo/reset and model changes, and records `runtime/design-verification.json`. It is scripted integration evidence, not human acceptance. On Linux substitute `.venv/bin/python`. The underlying model has no Ursina or GMAT imports.

## Explore the hub and Learning Lab

After setup, run `.venv\Scripts\python.exe main.py` on Windows or `.venv/bin/python main.py` on Linux, from this project directory. No new dependencies were added in Phases 2 or 3.

| Control | Action |
| --- | --- |
| Up / Down | Walk forward / backward |
| Left / Right | Strafe sideways |
| A / D during exploration | Turn left / right |
| E | Use the nearby door or console you are facing |
| Escape | Close a reading panel; otherwise open the pause menu |
| Enter | Resume from pause; confirm the selected card |
| Arrows / Tab inside library | Select a card without moving the player |
| Up/Down inside design panel | Focus a component row |
| Left/Right/Enter inside design panel | Change the focused option |
| U / Backspace inside design panel | Undo / Reset |
| Mouse | Select cards and panel buttons |
| R inside library | Open the selected NASA source in your browser (optional) |

Follow the cyan floor lights toward the **Learning Lab**. Walk near its door, press **E**, enter, and approach the card console. Press **E** to open the card list. Reading pauses movement and camera turning. Close with Escape to resume. The door will not close while you stand in its opening. Exit through Escape > Exit Game or the window close button.

Try walking toward/away from the Earth display, turning into a wall, opening the door from either side, selecting all ten cards with mouse/keyboard, and closing the panel while holding a movement key. Check the pause menu's Resume and Exit buttons. Card counts mean opened, not a quiz score or mission completion. Progress is session-only until Phase 4 saves.

The ten cards cover mission purpose, science requirements, spacecraft/instruments, mass/launch, power/energy, orbit/coverage, communications/data, budget/lifetime, mission segments, and verification/trade-offs. Content is local JSON and readable offline. Source buttons explicitly open external references; no internet is needed to explore or read.

### Additional Phase 2 verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/verify_hub.py
```

The graphical integration harness runs a scripted traversal through actual hub controls, door state, library, movement blocking, and pause/resume. It writes `runtime/hub-verification.json` and closes automatically. `--review` leaves its card panel open for visual review. Scripted checks are not user acceptance. On Linux substitute `.venv/bin/python`; a graphics session is required.

The original renderer is available with `main.py --engine-check`. `doctor.py --graphics` continues to use that five-second engine proof. A timed hub check is `main.py --smoke-seconds 5`.

Read the root `PROJECT_TRACKER.md` before continuing development. Stop after each phase for user testing and approval. There is one Python codebase for Windows and Linux.

## Requirements

- A desktop session and working graphics driver.
- Python **3.12 or newer** with pip/venv support. Phase 1 was tested on Python 3.13.0 on Windows. Python 3.12 compatibility is supported by package metadata but has not been run here.
- GMAT R2026a extracted with its `bin`, `plugins`, and `data` folders for the platform where it will run. No Python GMAT bindings are needed.
- Internet for initial pip installation; no online service needed for the scene or standalone GMAT proof afterward.

The bootstrap installs pinned Python dependencies into `.venv`. It never installs system packages, graphics drivers, or GMAT. No administrator access or virtual-environment activation is needed.

## Windows setup

Open PowerShell in `Space Mission Design Game`. Use your Python 3.12+ interpreter:

```powershell
python scripts/bootstrap.py --python 'C:\path\to\Python313\python.exe'
```

For this machine, the compatible interpreter found is:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" scripts/bootstrap.py
```

The default `python` on this machine is 3.10, and `py` currently selects Python 2.7. Use the explicit interpreter above for the initial setup. After that, use `.venv\Scripts\python.exe`.

Configure GMAT once per terminal session:

```powershell
$env:GMAT_BIN = 'C:\path\to\gmat-win-R2026a'
```

Alternatively copy `local_config.example.json` to `local_config.json`, replace `gmat_bin` with the installation folder or executable, and use JSON-escaped backslashes (`\\`) or forward slashes. Local config is ignored by git; each colleague has their own path. `GMAT_BIN` takes precedence.

Run the Phase 1 checks:

```powershell
.\.venv\Scripts\python.exe scripts/doctor.py
.\.venv\Scripts\python.exe scripts/doctor.py --graphics --gmat
.\.venv\Scripts\python.exe main.py
```

## Arch Linux setup

Use the same files and dependency set:

```bash
cd 'Space Mission Design Game'
python3 --version
python3 scripts/bootstrap.py
export GMAT_BIN='/absolute/path/to/linux-gmat'
.venv/bin/python scripts/doctor.py
.venv/bin/python scripts/doctor.py --graphics --gmat
.venv/bin/python main.py
```

If `python3` is older than 3.12, pass a compatible interpreter with `--python`. If `venv`, pip, graphics, or GMAT native libraries are unavailable, install/configure the missing system dependency using the distribution's instructions. The bootstrap deliberately does not run sudo or distro package managers.

GMAT's official Linux binaries target other distributions; **Arch compatibility is not yet tested**. Keep the full distribution together. Inspect its supplied README/native-library requirements, and make the console executable if the archive did not preserve permissions. The Windows `.exe` cannot be the Linux backend. Core graphics can be tested even before Linux GMAT is available; doctor will report the missing GMAT check separately and return a nonzero status.

## What to test manually

1. `doctor.py` identifies the intended Python, all dependency versions, and GMAT executable. Default diagnostics do not launch graphics/GMAT.
2. `doctor.py --graphics` opens a five-second window with a blue Earth, cyan orbit, and moving satellite; it closes automatically. This is a renderer proof, **not** GMAT playback.
3. `main.py --engine-check` stays open. Confirm text is readable, animation is visible, and **Escape** closes it. The default `main.py` now opens the Phase 2 hub; Escape there opens pause instead of immediately exiting.
4. `scripts/gmat_smoke.py` (or doctor `--gmat`) prints PASS for 11 samples over approximately 600 seconds. Read the generated trajectory and metadata. Repeat once to confirm independent output folders.
5. On Arch, send the OS/Python versions, diagnostics output, and any errors. Do not report Linux as passed without running it.

Generated evidence lives under ignored `runtime/`: `graphics-smoke.json`, `gmat-latest.json`, and per-run GMAT folders containing the generated script, local startup copy, console log, raw trajectory, and metadata. Setup alone does not prove rendering; frame evidence alone does not prove user acceptance.

## GMAT proof and limits

The proof propagates an Earth point-mass orbit for ten 60-second intervals. It validates sample count, finite data, elapsed times, A1 epoch consistency, plausible radius/speed, and movement. Frame: EarthMJ2000Eq. Position: km. Velocity: km/s. Epoch input: UTCGregorian; report epoch: GMAT A1ModJulian convention.

It uses a project-local copy of the installed startup file and directs reports/logs/updates into the project. The installed startup is unchanged. Python, MATLAB, and Fmincon plugins are disabled only in that generated copy because this proof uses none of them. The game interpreter does not need to match GMAT's Python-plugin ABI.

Successful GMAT execution here is a standalone compatibility proof. It does not prove game integration, observation geometry, a radio link budget, or full mission feasibility. Those arrive in later phases.

Inside a restricted agent sandbox, GMAT may incorrectly report that its existing data directories are missing. The Windows proof succeeded outside that sandbox with outputs still under the project. This does not imply that users should move/delete data or change security settings. Normal local terminal execution is the intended workflow.

## Verification commands

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

On Linux substitute `.venv/bin/python`. Tests validate malformed report rejection and configuration/startup isolation without requiring GMAT or a graphics window.

## Sources

- [Ursina installation](https://www.ursinaengine.org/installation.html)
- [Pinned engine release](https://pypi.org/project/ursina/8.3.0/)
- GMAT R2026a bundled README, `docs/help/html/CommandLine.html`, `StartupFile.html`, and `samples/Ex_CSSISpaceWeatherFile.script` were consulted for the console/report workflow.
