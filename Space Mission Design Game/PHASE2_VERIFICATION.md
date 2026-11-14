# Phase 2 verification - 14 November 2026

Historical Phase 2 record. The user approved proceeding to Phase 3 on 14 November 2026. Arch testing remains pending. The design bay is now functional; see PHASE3_VERIFICATION.md and README.md for the current build.

## What changed

- A walkable mission-control hub and player-opened Learning Lab, with a cyan route, Earth display, and future design-bay placeholder.
- Arrow movement/turning with a fixed-height camera. Walking brings the camera physically closer to or farther from objects. Wall and furniture collision uses the same floor-plan dimensions as the visible geometry, with sliding and bounded movement steps.
- Sliding door, nearby/facing E interactions, and a guard against closing the door on the player.
- Ten readable offline learning cards. Keyboard or mouse can select each card. Each contains an explanation, an example, a trade-off, and an optional NASA reference link.
- Reading/pause block navigation and release the pointer. Escape closes panels or opens pause. Enter resumes; Exit Game closes the application. Clearing held keys on focus loss avoids walking while using another app.
- The original renderer remains runnable through `main.py --engine-check` and `doctor.py --graphics`.

## Automated evidence

- Nine unittest checks passed, including closed/open door passage, movement freeze, heading-dependent movement, thin-wall collision, sliding along a wall, and the four existing GMAT-proof checks.
- Eleven explicit graphical integration checks passed in `scripts/verify_hub.py`. This creates a real Ursina scene and scripts the hub's actual movement/interaction methods; it is not an independent human playtest.
- Integration coverage: closed door collision; E opens door; player enters Lab; E opens library; movement and heading freeze; all ten cards can be selected; Escape closes library; movement resumes; Escape pauses; Enter resumes; door refuses to close on an occupant.
- `pip check` and compilation passed. No Phase 2 dependency changes.
- Original renderer timed check passed after refactoring.

## Desktop visual/input checks

Inspected the entrance, Learning Lab card panel, room materials, and final pause menu at the default 1280x800 window on Windows/Intel UHD Graphics. Sent Down to select another card, clicked a different card with the mouse, closed the panel with Escape, and clicked Exit Game. The game process exited successfully. Fixed world-material visibility and pause-text layering found during review.

Optional external source opening was not exercised. Manual held-key movement comfort, clean setup on another machine, and Arch rendering/input still need user/colleague testing. Do not count scripted integration as user acceptance.

## Manual review

From the project directory:

```powershell
.\.venv\Scripts\python.exe main.py
```

1. Hold Up and Down to move toward/away from objects; use Left/Right to turn. Try walking into walls and the Earth pedestal.
2. Follow the cyan markers to the closed Lab door. Confirm it blocks passage; press E near it and walk through after it slides open.
3. Approach the card console, face it, and press E. Read all ten cards using arrows/Tab and mouse selection.
4. Hold movement/turning keys while a panel is open. The world should not move. Escape closes the panel and restores navigation.
5. Approach the doorway from inside, turn toward it, and try closing it while standing in the opening. The safety message should keep it open. Step clear and try again.
6. Escape opens pause. Confirm the instructions are readable; Enter/Resume resumes; Exit Game closes the window.

On Arch, use `.venv/bin/python main.py`. If needed, run setup from README first. No separate Linux game code is required.

For repeatable scripted checks:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/verify_hub.py
```

## Limits and next phase

Cards opened and door state are session-only. There is no quiz, mission unlocking, spacecraft selection, simulated engineering consequence, or in-game GMAT trajectory yet. Those are intentionally later checkpoints. After user acceptance, propose Phase 3: make selections in the design bay change mass, power, budget, and data together. Stop for explicit approval first.
