# Mission Forge - playable campaign

## Multiplayer reliability update (2026-11-15)

**2, 3 and 4 players are supported: one host and up to three friends.** Update **every laptop to the same checkout and restart all games** before testing this transport revision. Host one room with N; every friend joins that same host Wi-Fi IPv4 and six-digit code, not another guest's address. No new packages or firewall changes are installed automatically.

Join errors now replace the misleading Connecting message in the open lobby; an unconfirmed join times out after 12 seconds with retry guidance. The open roster updates immediately as friends join. Guests spawn separately rather than overlapping. Complete position/state snapshots are coalesced so a stalled game loop cannot accumulate hundreds of obsolete updates. Each peer has its own socket writer, preventing a slow connection from blocking all players under the room lock. Background heartbeat traffic keeps connections alive while the game loop is paused or slow.

Verified **62 tests**, including simultaneous 2/3/4-player joins, idle connections beyond the old timeout, four-player movement flooding without UI consumption, slow-socket isolation, fifth-player rejection, disconnect/rejoin, and successful missions at every crew size. The four-client graphical harness verifies visible roster updates, shared preview/parts/approval and a visible wrong-code error. Evidence: ignored runtime/facility-review/. Actual separate Wi-Fi laptops and Arch remain manual acceptance.

Run `.venv/Scripts/python.exe -m unittest discover -s tests -q` (Windows) or `.venv/bin/python -m unittest discover -s tests -q` (Linux); rendered check: `python scripts/verify_four_player_scene.py`. If a join still fails, copy the new displayed error. Check the host's Wi-Fi IPv4 and incoming TCP 8765/private-network permission; guest/client isolation on the Wi-Fi may prevent direct laptop connections.

## Latest update: adaptive stations, one-click collection and launch propellant

Every workstation dialog now shows the same rotating spacecraft preview and the entire shared design's resource values, with **Show Checks** for all eight engineering checks. Teammate selections refresh an already-open preview without restarting its rotation; the full in-world spacecraft remains on the Integration table. Option buttons now **SELECT & PICK** in a single atomic action, including defaults; permissions, prerequisites and budget are checked before any selection changes.

Panels and their hitboxes resize together across maximize/restore, landscape and narrow windows. Controls appear at initial spawn and on LAN spawn/join/reconnect; **Start Exploring** closes the welcome panel. The existing library retains its own reader layout and navigation.

A separate **Launch Propellant** table is in Mission Planning, owned by the Flight role. Select **Solid** (included) or **Liquid** (EUR 5,000 extra) and submit its planning tablet alongside Orbit and Launcher: the crew now needs **6/6 contributions**. NASA's [Propulsion System](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/propulsion-system/) explains the real distinction; game prices are fictional, and this launch-plan choice does not change satellite mass, power or GMAT thrust. Old design saves default missing fuel to Solid and require fresh assembly/readiness.

The [two-page player guide](../output/pdf/mission-forge-player-guide.pdf) gives the tested first-run recipe and six explanations capped at two sentences each. Choose **Basic / Compact / Standard / Regional / Light / Solid**, then **Cached + Targeted**: the shipped assessment delivers 120 MB with no loss/unmet energy at EUR 89,000. Existing earlier five-choice or two-button instructions below are superseded by this update.

Verification: **57 automated tests** pass; `scripts/verify_workstation_upgrade.py` checks visual-center button collisions after resize/action refresh, rotating previews, welcome controls, one-click collection and the actual successful mission. The four-client graphical test verifies that a remote choice updates an observer's already-open preview. Physical multi-laptop Wi-Fi and Arch graphics remain manual. PDF generation uses optional document tooling, not new game dependencies.

## Mouse look

Move the mouse to look up/down/left/right while exploring. The cursor is captured for continuous turning; pitch stops before the view flips upside down. W/S walk, A/D strafe and left/right arrows remain optional keyboard turning. Escape opens pause and releases the cursor. Books, consoles and menus also release it automatically; closing them resumes mouse look. Focus loss releases capture, and returning skips recenter motion. This supersedes older statements that the mouse never turns the camera.

Verified with two unit tests and `python scripts/verify_mouse_look.py` (both axes, camera sync, reading/menu capture, focus loss and safe restoration).

## Latest update: retrieval, red diagnostics, stacked parts and euro budgets

At a marked integration location, **E toggles placement/retrieval** of your own component. Retrieval returns it to your carried stack, preserves other contributions and invalidates approval. At the mission-plan desk, **left/right** selects orbit/launcher and **E** submits or retrieves that tablet. All confirmed, unsubmitted choices are now displayed in a vertical stack locally and on remote astronauts. **I > Stack Base** changes the lowest item.

Read the large **red validation screen on the left of Integration** for current failures, actual values, return stations and suggestions. Approach it and use E for the detailed validation panel. The display updates after edits/retrieval, shows budget/remaining funds and rotates through multiple failures automatically.

**Flood Watch has a EUR 145,000 budget**, defined by `budget_eur` and `currency: EUR` in `content/missions.json`. Canonical prices in `content/design_catalog.json` use `cost_eur`, `ground_cost_eur` and `baseline_cost_eur`. Each option shows its euro price, resulting full-design total and remaining/overspent euros. Overspend may be previewed but blocks collection, approval and launch. Old teaching amounts were scaled by 1,000, preserving their relative trade-offs; these are fictional educational prices. Historical credit examples below are superseded by the euro amounts. Retrieval does not cancel a design selection or refund its reserved price; choosing a cheaper replacement lowers the total. Restart all laptops with the same checkout after editing mission budgets/prices.

**50 automated tests** pass, plus **14 rendered revision checks** and real four-client local networking checks. Run `python scripts/verify_integration_revision.py`; evidence is in ignored `runtime/integration-revision/`. Existing facility, design and cached campaign checks pass. Separate Wi-Fi laptops and Arch graphics remain manual acceptance. No additional install is needed.

## Current game: connected workshops and 1–4 player crews

Start with the **Flood Watch** mission screen beside the Earth/orbit display in the original Spawn Room. Mission 02 is visibly disabled. The host selects the shared mission; solo players do the same. The original Library is still optional reading, with all twelve animated books preserved.

Walk through the Library's new right-side doorway into **Payload Design → Power Systems → Communications → Mission Planning → Satellite Integration → Launch Readiness**. The original spawn geometry/decorations are retained; its previous design console now opens a workshop directory. The same rotating spacecraft object is displayed in Integration.

At your assigned table, press **E**, select an existing option and click **Confirm & Collect**. Complete workshops in order. Defaults also need explicit confirmation. Physical parts appear in your hand; **I** lists confirmed, unsubmitted choices and switches the visible item. Orbit and launcher use plan tablets. Other players see your carried selection. No new component specifications or engineering equations were introduced.

At Integration, use E at each marked payload/power/radio location, then submit orbit and launcher at the separate mission-plan desk. The host runs validation at the central console. All five contributions are required. Failed checks show actual values/limits, contributing roles/current owners, stations and suggested revisions. Return to workshops, edit, reconfirm and resubmit affected choices. Unaffected submissions stay valid; approval is always invalidated by a design change. After approval, the flight engineer uses the Launch Readiness console for the existing cached/live GMAT mission and results.

| Players | Automatic role distribution in join-slot order |
| --- | --- |
| 1 | All four roles |
| 2 | Host: Science + Power; guest: Communications + Flight |
| 3 | Host: Science + Power; guest 1: Communications; guest 2: Flight |
| 4 | Science, Power, Communications, Flight: one role each |

Science owns **sensor**; Power owns **power package**; Communications owns **radio**; Flight owns **orbit + launcher**, observation plan/source and launch. The host retains final validation, mission selection and shared saves. Join/leave redistributes responsibilities without discarding valid selections. A room never accepts a fifth player.

### Actual controls

**W/S** forward/back · **A/D** strafe · **Left/Right arrows** turn · **Space** jump · **Alt** hold crouch · **E** interact · **I** parts inventory · **M** mission tablet · **N** crew · **Esc** close/pause. Mouse remains free for selection. Panels capture input; books retain their own navigation. The glowing question mark inside the Library opens current controls. The new wing includes one raised cable crossing (jump) and one low service passage (crouch); standing is blocked under its beam.

### Same-Wi-Fi setup

Use the **same updated checkout** on all laptops. Press **N**: the host starts a new crew mission; up to three friends join with the host's Wi-Fi IPv4 address and six-digit room code. TCP port **8765** and the existing LAN workflow are unchanged. No dependency installation is added by this enhancement. Only the host needs a configured GMAT install for Live mode; Cached needs neither GMAT nor internet.

The host owns the canonical mission/design, permissions, confirmations, inventory, submissions and approval. Complete snapshots initialize joining/reconnecting clients. Player position, vertical displacement and crouch state update remote avatars. Leaving preserves the current design locally; integration must be resubmitted for fresh solo approval. There is no automatic host migration. Reconnect through N → Leave Session → Join. Guest slots are reassigned, not authenticated accounts.

If Windows prompts for Python network access, allow it on the trusted/private network being used. The game does not change firewall settings. The host firewall must permit incoming TCP 8765. Pick the **Wi-Fi adapter** IPv4 (`ipconfig` on Windows, `ip -4 addr` on Linux), not VPN/VM adapters. Some institutional networks use public-looking IPv4 addresses. Client isolation on guest Wi-Fi can block laptop-to-laptop connections; no router port forwarding is required. This remains a trusted-LAN prototype, not an encrypted internet service.

Saves retain their existing schema and engineering data with an additive `assembly` object. Old saves load; missing/stale integration records require explicit recollection/submission and fresh approval. Mission results remain available. Crew saves remain host-only at `runtime/crew-save.json`; solo saves use `runtime/campaign.json`.

### Verification and handoff

See [COOPERATIVE_FACILITY.md](COOPERATIVE_FACILITY.md) for the full implementation report, file manifest, five-minute demo and manual acceptance checklist. **46 automated tests passed**, including real localhost sessions for all four player counts. Scripted graphical checks cover the single-player correction-to-launch flow, two-player launch/results, four-player carried parts/role redistribution, preserved hub/design/campaign behavior and the existing library. Separate Wi-Fi laptops and Arch graphics remain manual checks.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -q
.\.venv\Scripts\python.exe scripts/verify_facility.py
.\.venv\Scripts\python.exe scripts/verify_four_player_scene.py
```

## Earlier campaign and phase reference

The following sections record earlier phases. The connected-workshop flow and current controls above supersede their old isolated design-bay and two-player instructions. Simulation assumptions and numerical examples below still apply.

## Complete mission and five-minute presentation

Press **M** during exploration to open Mission Control. The five objectives unlock consecutively. Open a Lab card first, then use Complete Current Task to accept the brief. Build a feasible spacecraft, validate its orbit/ground configuration, and pass integrated readiness. Launch & Operate becomes available only for that exact approved configuration. Any component change invalidates readiness and returns you to design review.

Mission Control offers **Save**, **Load**, and **New Mission**. Saves are versioned JSON under `runtime/campaign.json`; loading revalidates readiness. These are local files, not cloud accounts. The latest result is in `runtime/mission-report.json`; the debrief compares the preceding attempt during the same campaign.

The source toggle explicitly selects **Cached** or **Live** GMAT. Both supported cached trajectories were generated with the installed R2026a console and ship under `content/orbit_cache/`, keyed by input settings. Cached mode needs no GMAT install or network. Live mode runs GMAT in a worker thread via a separate console process, preserves script/report/log provenance in runtime, and shows errors without secretly switching providers. Regional: SMA 7000 km, inclination 28.5 degrees. Wide: SMA 7200 km, inclination 98 degrees. Each report has 601 samples covering 36000 seconds. These geometric orbits differ from Phase 3's deliberately curated resource-preview timings.

Operations derives contacts, target visibility and eclipses from the actual trajectory timestamps/positions. Coordinates are EarthMJ2000Eq, km, s; display maps inertial Z upward. A rotating equatorial station/target starts at epoch-relative longitude zero, rather than a geolocated real facility. Contact minimum elevation is 5 degrees; observation region is within 35 degrees of the target's radial direction. A fixed Sun along +X and cylindrical Earth shadow approximate illumination. Earth radius is 6378.137 km; spin rate is 7.292115e-5 rad/s. These short-run educational geometry assumptions are not precision access analysis.

The operational goal is at least **60 MB delivered**, no storage loss, and no unmet electrical load over the assessment window. **Targeted** imaging stops at 120 MB. **Continuous** imaging demonstrates how otherwise viable hardware can overflow storage. Retry with a different plan or revise the spacecraft. Battery, storage, contacts, delivered data and satellite movement use the same simulation timeline. Launch animation is illustrative; readiness failure blocks launch rather than causing an unrelated crash. Skip/Enter/Escape during playback goes to the calculated result.

Suggested presentation: 0:00-0:30 explain flood response; 0:30-1:10 walk into the Lab and read one card; 1:10-2:30 demonstrate Advanced -> Extended -> Heavy -> Fast and undo; 2:30-3:00 complete the mission reviews using a passing design; 3:00-4:15 show launch/orbit with cached GMAT, eclipse/contact telemetry, and the debrief; 4:15-5:00 explain coupled trade-offs and compare a Continuous failure with Targeted repair. Use Skip to fit the time limit. There is no hidden mission-unlock bypass.

Windows checks: 21 unit tests, 14 design integration checks, 11 hub checks, cached end-to-end campaign rendering, and live GMAT worker-to-result flow passed. Arch Linux and a second-machine clean install remain **unverified**. Run the same bootstrap and checks there; cached mode isolates the game from GMAT native-library differences. Do not treat the shared Python codebase as proof that Arch graphics/GMAT will work.

```powershell
.\.venv\Scripts\python.exe scripts/verify_campaign.py
.\.venv\Scripts\python.exe scripts/verify_campaign.py --live
```

The graphical harness saves QA frames in ignored runtime files and exercises campaign completion and revalidation. `--live` requires a configured native GMAT install. All visual geometry is procedural; no remote asset download or Blender is required. Multiplayer remains intentionally deferred.

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
