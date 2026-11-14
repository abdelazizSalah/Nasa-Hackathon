# Mission Forge - project tracker and handoff

Updated: 2026-11-14. Current checkpoint: design proposal complete; awaiting user review before Phase 1. No game implementation or dependency installation has started.

## Read first

- Scope: only the Space Mission Design Game project. Earth_Detective is separate; do not modify it as part of this plan.
- Current design source: [PHASED_DESIGN.md](Space%20Mission%20Design%20Game/PHASED_DESIGN.md).
- Current PDF: [phased design](output/pdf/mission-forge-phased-design.pdf).
- Earlier proposal: [initial design](output/pdf/mission-forge-game-design.pdf). The new proposal reduces eight game objectives to five missions and requires a 3D desktop experience.
- User notes: Space Mission Design Game/Notes.md and Initial_Used_Command.md. Preserve user edits and unrelated files.

## Intended product

A simple, visually impressive, single-player 3D mission-design game built in Python/Ursina for a five-minute hackathon presentation. The player uses arrows to move and turn with the camera; E opens doors/consoles; a Learning Lab displays short concept cards. One flood-monitoring satellite scenario progresses through five missions: briefing, spacecraft configuration, orbit/communications, launch review, operations/science delivery.

Trade-offs are the central mechanic: every major selection changes related mass, power, budget, data, communications, or coverage values. Multiple designs can succeed. Launch visuals cannot substitute for scientific success. A real GMAT adapter is required; a labeled simplified provider and matching cached GMAT data are fallback/demo paths, not proof of integration. Multiplayer is deferred.

## Review and approval workflow

After EACH implementation phase, stop and ask the user whether to continue. First update this file, provide exact run/manual-test instructions and expected results, summarize automated checks separately from user tests, identify limitations, and suggest the next phase. Do not treat elapsed time or silence as approval. Do fixes in the current phase before requesting the next gate.

Record statuses distinctly: proposed, approved, in progress, implemented, manual test pending, accepted. A phase is not accepted until the user has reviewed/tested it. Do not automatically continue because another agent/session reads this file.

## Phase status

| Phase | Deliverable | Current status | Acceptance evidence |
| --- | --- | --- | --- |
| Planning | Revised design source, PDF, tracker | Ready for review | Sources checked; PDF rendered/inspected before delivery |
| 1 | Setup scripts, engine window, standalone GMAT proof | Proposed; not authorized yet | None |
| 2 | 3D hub, arrows/camera, Lab door and cards | Proposed | None |
| 3 | Configuration and visible trade-off engine | Proposed | None |
| 4 | Five consecutive missions, readiness, saves | Proposed | None |
| 5 | GMAT bridge and orbital/resource operations | Proposed | None |
| 6 | Launch gallery, spectators, feedback and report | Proposed | None |
| 7 | Windows/Linux checks, offline demo and rehearsal | Proposed | None |

## Completed work

- Reviewed the existing six-page proposal, supplied challenge notes/resources, and NASA mission-design guide.
- Checked official Ursina installation/package metadata: propose Python 3.12 and stable Ursina 8.3.0, with actual version pinning/verification in Phase 1.
- Identified GSC-19468-1 as GMAT and confirmed official distribution notes describe Windows and Linux console applications.
- Designed a separate file/process GMAT bridge and early compatibility proof. No live GMAT run has been performed.
- Created the phased design and this handoff tracker. Final artifact verification belongs to the planning checkpoint, not game acceptance.

## Environment and unknowns

- Planning performed on Windows. Active `python` reports 3.10.14. Another compatible interpreter may exist; locate or install Python 3.12 for the game in Phase 1.
- User supplied GMAT R2026a folder: `C:\Users\20115\Dropbox\My PC (LAPTOP-ILAL93NC)\Downloads\gmat-win-R2026a`. Read-only inspection confirmed bin/GmatConsole.exe, README.txt, docs, data, and samples. This is local machine context, not a portable default or a value to hardcode in game code. Execution/version remains to be verified.
- Colleague uses Arch Linux. User prefers avoiding unnecessary OS-specific work; use one Python implementation and bootstrap, with only necessary native/graphics checks. A Windows GMAT binary will not serve as the Linux backend.
- NASA catalog page refers to R2025a; current project documentation also has R2026a. Target the supplied R2026a installation, not an automatic upgrade. Match scripts and console invocation to the installed distribution.
- Ursina/graphics compatibility, Linux setup, GMAT execution, trajectory import, and numerical game balance are unverified.
- The PDF was authored with existing document tooling. Those dependencies do not imply that game dependencies are installed.
- Planning artifact check: PDF has 8 pages and 6 clickable references; rendered pages were visually checked, with no table overflow or clipped text found. Read-only checks did not launch GMAT or install game packages.

## Phase 1 next actions, once approved

1. Inspect supplied GMAT R2026a folder and bundled docs/samples; verify execution. Check Arch Linux native compatibility with colleague when available.
2. Locate a Python 3.12 interpreter; establish game source layout without touching Earth_Detective.
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
