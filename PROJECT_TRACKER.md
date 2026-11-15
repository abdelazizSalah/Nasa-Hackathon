# Mission Forge - project tracker and handoff

Updated: 2026-11-14. Remaining single-player gameplay is implemented and Windows-verified. Phases 4-6 have working campaign, live/cached GMAT, launch and results. Phase 7 Windows verification/documentation is done; Arch and second-machine clean-install validation remain pending external access.

CURRENT EXTENSION (2026-11-14): Implemented connected Payload, Power, Communications, Mission Planning and Satellite Integration rooms, shared mission selection, 1â€“4 player dynamic roles, physical component carrying/submission, original validation feedback, host approval, jump/crouch and traversal. User explicitly approved ONE narrow doorway in the Library's right wall; book modules/content are unchanged. Existing spacecraft geometry/rotation and engineering/orbit/operations calculations are unchanged. See `Space Mission Design Game/COOPERATIVE_FACILITY.md` and current README for usage and test evidence. No new dependencies. Old design console now opens the physical-workshop directory. The five existing campaign objectives still feed the same mission simulation. Separate-laptop Wi-Fi/Arch acceptance is pending.

LATEST AUTHORIZATION: User said "finish all the remaining phases, only contact me when you need permissions". This supersedes every older instruction in this tracker to pause for phase approvals. Continue fixes autonomously; ask only for genuinely necessary permissions. Do not mark Arch validation passed without evidence.

LATEST VERIFICATION: 46 automated tests passed, including real TCP sessions, full launch and all-player finish acknowledgements at 1/2/3/4 participants. Graphical checks passed: 18 new facility checks, four-player scene with carried parts and disconnect redistribution, updated two-player launch/results, 11 hub checks, 14 design checks, unchanged cached campaign and unchanged 12-book/38-chapter library harness. Final protected-file Git audit confirms no edits to library modules/data, engineering catalog/equations, orbit provider, operations simulation or spacecraft geometry. Remaining manual work: separate Wi-Fi laptops, Arch native graphics/Alt bindings, optional fresh Live GMAT validation. See COOPERATIVE_FACILITY.md for exact commands and the complete 20-file manifest.

LATEST REVISION (2026-11-14): E retrieves/resubmits owned integration parts and plan tablets, restoring inventory and clearing approval. All carried items stack vertically, including remote views. A large red integration screen shows actual failed checks, return stations and budget overruns. Flood Watch owns EUR 145,000 in content/missions.json; catalog/report monetary fields now use EUR, scaled from old teaching costs by 1,000. Option prices/projected totals/remaining funds are visible, and overspend blocks collection, approval and launch. 50 automated tests and 14 new rendered revision checks pass, alongside facility/design/campaign and four-client graphical regressions. See README and COOPERATIVE_FACILITY.md. Physical Wi-Fi and Arch remain manual. No Library, physical component specifications, spacecraft geometry or orbit/operations changes. Budget numbers are fictional educational costs.

LATEST CONTROLS UPDATE: Mouse displacement now controls yaw and pitch during exploration; vertical look is clamped to +/-85 degrees. Existing W/S walking, A/D strafing and optional arrow turning remain. Books/menus release capture and freeze look; closing resumes capture with stale/recenter motion suppressed. Alt-Tab also releases safely. Two unit tests and the scripted graphical mouse-look harness pass; run scripts/verify_mouse_look.py. No mission/engineering/network changes in this update.

LATEST WORKSTATION UPDATE (2026-11-15): Shared ResponsivePanel scales all modal contents and hitboxes after resize/rebuild. Each E-opened workstation reuses the rotating Spacecraft model, with full shared resource metrics and a checks view; remote updates preserve the preview's rotation phase. SELECT & PICK is one atomic server-validated selection/collection. Main launch and LAN spawn/join show welcome controls. Added a Flight-owned Launch Propellant table in Mission Planning (Solid included / Liquid +EUR 5k), NASA-sourced and explicitly launch-plan-only, without invented thrust or bus-mass changes. Six contributions now required; old saves default fuel to Solid and need fresh approval. Verified 57 tests, resize/hitbox + one-click + successful Cached/Targeted graphical flow, four-client live observer preview, and existing facility/mouse-look checks. Two-page PDF: output/pdf/mission-forge-player-guide.pdf; generator scripts/build_player_guide.py. No extra game dependencies. Physical Wi-Fi and Arch remain manual acceptance.

## Read first

- Scope: only the Space Mission Design Game project. Earth_Detective is separate; do not modify it as part of this plan.
- Current design source: [PHASED_DESIGN.md](Space%20Mission%20Design%20Game/PHASED_DESIGN.md).
- Current PDF: [phased design](output/pdf/mission-forge-phased-design.pdf).
- Earlier proposal: [initial design](output/pdf/mission-forge-game-design.pdf). The new proposal reduces eight game objectives to five missions and requires a 3D desktop experience.
- User notes: Space Mission Design Game/Notes.md and Initial_Used_Command.md. Preserve user edits and unrelated files.

## Intended product

A simple, visually impressive, single-player 3D mission-design game built in Python/Ursina for a five-minute hackathon presentation. The player uses arrows to move and turn with the camera; E opens doors/consoles; a Learning Lab displays short concept cards. One flood-monitoring satellite scenario progresses through five missions: briefing, spacecraft configuration, orbit/communications, launch review, operations/science delivery.

Trade-offs are the central mechanic: every major selection changes related mass, power, budget, data, communications, or coverage values. Multiple designs can succeed. Launch visuals cannot substitute for scientific success. A real GMAT adapter is required; a labeled simplified provider and matching cached GMAT data are fallback/demo paths, not proof of integration. Two-player LAN mode is now implemented; broader multiplayer remains future scope.

## Review and approval workflow

After EACH implementation phase, stop and ask the user whether to continue. First update this file, provide exact run/manual-test instructions and expected results, summarize automated checks separately from user tests, identify limitations, and suggest the next phase. Do not treat elapsed time or silence as approval. Do fixes in the current phase before requesting the next gate.

Record statuses distinctly: proposed, approved, in progress, implemented, manual test pending, accepted. A phase is not accepted until the user has reviewed/tested it. Do not automatically continue because another agent/session reads this file.

## Phase status

| Phase | Deliverable | Current status | Acceptance evidence |
| --- | --- | --- | --- |
| Planning | Revised design source, PDF, tracker | Accepted for implementation | User: "Nice, lets start phase 1" on 2026-11-14 |
| 1 | Setup scripts, engine window, standalone GMAT proof | Accepted for continuation | User: "Very good, lets go to phase 2 :)"; Windows evidence retained; Arch pending |
| 2 | 3D hub, arrows/camera, Lab door and cards | Accepted for continuation | User: "Very cool, now lets go to phase 3"; Windows evidence retained; Arch pending |
| 3 | Configuration and visible trade-off engine | Implemented; user review pending | 17 unit tests, 14 design and 11 hub graphical integration checks; desktop trade-off chain inspected |
| 4 | Five consecutive missions, readiness, saves | Implemented; Windows verified | Gate/save/revalidation tests and end-to-end harness |
| 5 | GMAT bridge and orbital/resource operations | Implemented; Windows verified | Both real GMAT presets, input-keyed cached data, live worker/game flow |
| 6 | Launch gallery, spectators, feedback and report | Implemented; Windows verified | Rendered launch/orbit/report, targeted success and continuous failure |
| 7 | Windows/Linux checks, offline demo and rehearsal | Windows checks/docs done; Arch pending | 21 tests, graphics harnesses, offline caches; no remote Arch access |

## Completed work

- Reviewed the existing six-page proposal, supplied challenge notes/resources, and NASA mission-design guide.
- Checked official Ursina installation/package metadata: propose Python 3.12 and stable Ursina 8.3.0, with actual version pinning/verification in Phase 1.
- Identified GSC-19468-1 as GMAT and confirmed official distribution notes describe Windows and Linux console applications.
- Designed a separate file/process GMAT bridge and completed the early standalone compatibility proof. The in-game bridge remains Phase 5.
- Created the phased design and this handoff tracker. Final artifact verification belongs to the planning checkpoint, not game acceptance.

## Environment and unknowns

- Planning performed on Windows. Default `python` reports 3.10.14 and `py` selects 2.7. Found a separate user installation at `%LOCALAPPDATA%\Programs\Python\Python313\python.exe` (3.13.0); used it to create the project `.venv`. Python 3.12+ is the supported setup target. Do not replace the user's default interpreter.
- User supplied GMAT R2026a folder: `C:\Users\20115\Dropbox\My PC (LAPTOP-ILAL93NC)\Downloads\gmat-win-R2026a`. Verified actual console execution and distribution README version. Local path is configured in ignored `Space Mission Design Game/local_config.json`, not hardcoded into code or portable defaults.
- Colleague uses Arch Linux. User prefers avoiding unnecessary OS-specific work; use one Python implementation and bootstrap, with only necessary native/graphics checks. A Windows GMAT binary will not serve as the Linux backend.
- NASA catalog page refers to R2025a; current project documentation also has R2026a. Target the supplied R2026a installation, not an automatic upgrade. Match scripts and console invocation to the installed distribution.
- Windows Ursina/graphics and standalone GMAT execution are verified. Phase 3's teaching model is balanced and conserves energy/data across all 32 configurations. Arch setup, live Linux GMAT, real orbital geometry, and in-game trajectory import remain unverified.
- The PDF was authored with existing document tooling. Those dependencies do not imply that game dependencies are installed.
- Planning artifact check: PDF has 8 pages and 6 clickable references; rendered pages were visually checked, with no table overflow or clipped text found. Read-only checks did not launch GMAT or install game packages.

## Phase 1 evidence (2026-11-14)

- User approval: "Nice, lets start phase 1". Implemented only Phase 1.
- Added isolated bootstrap, pinned dependencies, read-only doctor with optional execution checks, 3D renderer scene, GMAT script/template/validator, tests, local config example, and project README.
- Installed game dependencies into `Space Mission Design Game/.venv`; no system Python or GMAT installation modified. Pip download needed network access beyond the restricted sandbox and then succeeded.
- Windows environment: Python 3.13.0, Ursina 8.3.0, Panda3D 1.10.16, Intel UHD Graphics. Initial timed run rendered 399 frames in about 5 seconds. Visual review corrected Ursina color units and adjusted camera framing/lighting. Final scene was visually inspected; Escape exited successfully.
- GMAT: three successful live R2026a console runs, each producing 11 finite state samples over about 600 seconds. Checked elapsed time, A1 epoch consistency, expected Earth-orbit radius/speed, and actual position change. Frame EarthMJ2000Eq, positions km, velocities km/s. Final combined doctor check exited 0; final timed scene rendered 319 frames in 5.000 seconds. Not a full mission-feasibility or game-integration proof.
- GMAT needs installed data access outside the restricted agent sandbox: inside it, initialization reported existing directories missing. The same script succeeded with normal installed-data access while all outputs stayed in project runtime folders.
- Generated startup copies redirect output/log/update paths into the project and disable unused external Python/MATLAB/Fmincon interfaces. Original startup remains unchanged.
- Checks: 4 unit tests pass; `pip check` passes; bootstrap rerun succeeds without changing installed versions; scripts compile.
- Evidence files: ignored runtime/graphics-smoke.json, runtime/gmat-latest.json, per-run GMAT trajectory/script/startup/console/metadata. See `Space Mission Design Game/PHASE1_VERIFICATION.md` for a portable summary.
- Manual results: agent visual inspection and Escape verified on Windows. User acceptance pending. Arch tests not run; colleague must supply results. No claim of Linux acceptance.

## Phase 2 evidence (2026-11-14)

- User approval: "Very good, lets go to phase 2 :)". This authorizes Phase 2, not Phase 3.
- Default `main.py` now opens the compact 3D hub. Original Phase 1 rendering remains available with `--engine-check`; doctor graphics smoke continues using that original scene.
- Implemented arrow-key walking and turning, attached fixed-height camera, delta-time motion, floor-plan collision/sliding, focus-loss key clearing, cyan route markers, hologram, design-bay placeholder, sliding Lab door, and doorway-close protection.
- Added ten offline JSON learning cards with summaries, examples, trade-offs, and optional primary NASA source links. Keyboard and mouse selection work. Card counts track opened cards, not learning mastery. No mission-completion claim yet.
- Reading and pause freeze both position and heading. Escape closes panels or opens pause; Enter resumes. Exit Game works. Mouse stays released, with no head-bob or required mouse-look.
- Architecture: `game/domain/navigation.py` is renderer-independent; `game/presentation/hub.py` builds the world/panels; `engine_check.py` retains the separate proof. No dependencies added.
- Verification: 9 unit tests pass (4 existing GMAT-proof checks, 5 navigation behaviors); 11 explicit graphical integration checks pass. The harness exercises actual hub movement inputs, door state, Lab entry, all cards, reading freeze, resumed walking, pause/resume, and doorway safety. Output: ignored `runtime/hub-verification.json`.
- Desktop inspection verified initial hub, card layout, Down-arrow selection, mouse selection of a different card, Escape close, room materials, pause controls, and clicked Exit Game (process exit 0). The initial dark material/overlay-depth issues were corrected before final review. Optional source-browser launch was not exercised.
- Original engine scene still renders and exits after the requested timed run. Compile and pip dependency checks pass. No new GMAT run needed because the backend did not change.
- User manual acceptance and Arch graphics/navigation remain pending. No Phase 3 simulation/trade-off engine, campaign, saves, in-game GMAT bridge, or launch gallery has been implemented.
- See `Space Mission Design Game/PHASE2_VERIFICATION.md` and the updated project README for exact manual checks.

## Phase 3 evidence (2026-11-14)

- User approval: "Very cool, now lets go to phase 3". Phase 4 is not authorized.
- Added `content/design_catalog.json` with five binary choices (sensor, power, communications, orbit, launcher), fixed bus, scenario limits, and explicit invented teaching assumptions.
- Added renderer-independent `game/domain/design.py`: deterministic one-minute cycle preview, mass/cost sums, eight checks, previous-selection comparisons, session undo and reversible reset. Evaluated all 32 combinations: seven feasible, including basic and advanced sensor designs.
- Added a live design panel and procedural spacecraft shared between panel/world. Sensor, solar arrays and radio geometry reflect choices; a resource summary stays in the HUD. The design bay is now functional, and changes persist when closing/reopening it within the session.
- Demonstrated chain: default 57 kg / 89 credits passes; Advanced -> power/data failures; Extended -> mass/data failures; Heavy -> data failure; Fast -> all checks pass at 79 kg / 138 credits / 600 MB delivered. Wide orbit on that advanced design exposes a 148/145 credit budget failure.
- Preview checks: science grade, budget, launch mass, launcher/orbit compatibility, conservative peak-power rule, cycle energy, storage overflow, and cycle data delivery. Regional/Wide observation/contact/eclipse opportunities are curated, not GMAT-derived. Service duration is fixed at 12 months for cost assumptions, not years of reliability prediction.
- Tests: 17 unit tests pass; energy and data balances checked over all 32 combinations; 14 graphical design integration checks and the existing 11 hub checks pass. Compile and pip checks pass. No dependencies added; no change to the GMAT backend requiring a repeat proof.
- Desktop review: mouse clicks followed the power -> mass -> data -> success sequence; inspected 3D changes, deltas, deficits and viable state. Keyboard Backspace reset and mouse Undo were checked; scripted U/row input is covered by the harness. User comfort/independent manual acceptance remains pending.
- Current generated evidence: ignored runtime/design-verification.json and runtime/hub-verification.json. The former records a valid advanced design after the non-review test run. Full commands, expected values, and limitations are in `Space Mission Design Game/PHASE3_VERIFICATION.md` and README.
- No disk saves, five-mission progression, launch clearance, GMAT-backed coverage/contact geometry, launch cinematic, or multiplayer is claimed. These remain future phases.

## What the user should test now

From `Space Mission Design Game` in PowerShell:

```powershell
.\.venv\Scripts\python.exe main.py
```

Restart any older build, approach the design bay on the right, and press E. From Reset, select Advanced sensor -> Extended power -> Heavy launch -> Fast radio. Expect the limiting factor to shift from power to mass to data, then a passing preview. Try Wide orbit to reveal the budget limit, then Undo. Test keyboard row/option selection, reset, undo, model changes, and closing/reopening the panel. Existing Lab/pause/navigation should still work. No new install is needed on this Windows setup; Arch instructions remain in README.

## Next actions

Latest navigation preference: A/D now turn left/right; arrows retain forward/backward and strafing. Mouse-look and pointer capture are removed. The HUD, pause instructions, and room sign reflect these controls. Reading/pause/design panels and loss of window focus still freeze navigation. This supersedes the mouse-look adjustment below; Phase 4 remains unauthorized.

Navigation adjustment requested after Phase 3: Left/Right now strafe, and captured mouse movement controls yaw/pitch. Panels and pause release the pointer; closing them restores capture. Focus loss freezes movement/releases capture. Diagonal speed is normalized, and lateral motion uses existing wall collision. This supersedes earlier arrow-turning descriptions. Phase 4 remains unauthorized. Automated navigation and hub checks passed; mouse sensitivity/comfort still needs user review.

1. Await user review and resolve any Phase 3 issues.
2. Record colleague's Arch graphics and GMAT evidence when available; until then leave those checks pending.
3. Ask for explicit approval before Phase 4 (five consecutive missions, readiness review, local saves and revalidation after changes).

## Original Phase 1 checklist (completed on Windows)

1. Inspect supplied GMAT R2026a folder and bundled docs/samples; verify execution. Arch native compatibility remains pending colleague test.
2. Locate a Python 3.12+ interpreter; establish game source layout without touching Earth_Detective.
3. Add pinned requirements and a stdlib-based cross-platform bootstrap plus doctor commands; no silent admin/system installation.
4. Open a minimal Ursina scene and record graphics/runtime results.
5. Run one GMAT sample and inspect time-stamped position output with frame, time scale, and units recorded.
6. Give both teammates manual commands, record actual platform evidence, and request review before Phase 2.

## Planned boundaries and contracts

Proposed code under Space Mission Design Game/ (final layout confirmed in Phase 1): game/presentation, game/domain, game/orbit, content, tests, scripts. Keep domain code independent of Ursina. Agree on MissionConfig, ComponentSpec, CheckResult, ObjectiveState, TrajectorySample, SimulationState, and MissionResult before parallel work. Version JSON saves/content. Keep GMAT_BIN/local paths untracked. Cache keys include normalized input settings, frame, and version; never reuse mismatched trajectories.

## Team ownership

- Two people: A = 3D, controls, panels, teaching copy, cinematic/report presentation. B = models, progression/saves, GMAT, operations/results. Both own integration and platform checks.
- Three people: A = 3D/camera/interactions/cinematics. B = engineering/GMAT/operations. C = campaign/content/saves/panels/report assembly and integration coordination.

## Evidence log template for each phase

- Date / phase / approval reference:
- Files and behavior changed:
- Setup/run commands:
- Automated checks and results:
- Windows manual results (who, OS, versions):
- Linux manual results (who, distro, versions):
- GMAT mode and provenance verified:
- Known issues / remaining manual work:
- User review outcome:
- Next phase proposed / explicit approval received:

## Backlog after the core demo

Multiplayer roles and shared authoritative mission state; additional mission scenarios; detailed risk/lifetime models; richer assets; optional crash simulation with a valid physical cause. None are required for initial acceptance. First protect the five-minute trade-off demonstration and the real GMAT connection.
