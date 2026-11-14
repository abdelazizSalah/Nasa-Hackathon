# Phase 3 verification - 14 November 2026

Status: implemented; Windows automated/desktop checks recorded; user acceptance and Arch Linux testing pending. Phase 4 is not authorized.

## Delivered

- A JSON catalog containing scenario assumptions, the fixed bus, and two options each for sensor, power package, radio, orbit preset, and launcher.
- Renderer-independent design/session models with integrated resource calculations, eight preview checks, previous-selection deltas, undo, and reversible reset.
- A design bay opened with E. Its panel supports mouse and keyboard, highlights limiting factors, and updates a procedural spacecraft both in the panel and world.
- Persistent in-session design and a HUD resource summary; no disk save yet. No new dependencies or GMAT changes.

## Model evidence

Enumerated all 32 combinations: **seven pass**. Both a basic-sensor design and an advanced-sensor design are feasible. This is preview feasibility under the stated teaching assumptions, not a NASA-validated mission design.

| Step | Mass | Cost | Peak margin | Delivered / required | Failed checks |
| --- | --- | --- | --- | --- | --- |
| Default | 57 kg | 89 cr | +8 W | 300/300 MB | None |
| Advanced sensor | 65 kg | 104 cr | -12 W | 480/600 MB | Peak power, delivery |
| Extended power | 75 kg | 116 cr | +53 W | 480/600 MB | Launch mass, delivery |
| Heavy launch | 75 kg | 128 cr | +53 W | 480/600 MB | Delivery |
| Fast radio | 79 kg | 138 cr | +43 W | 600/600 MB | None |

The final configuration has at least 15.5 Wh remaining during the cycle and stays within the 145-credit budget. Switching it to Wide increases cost to 148 credits, causing a budget failure. Values and orbit opportunities are invented for teaching. The peak rule is intentionally conservative; real transient demand can instead involve battery support or scheduling.

## Checks

- **17 unit tests**: eight new model tests plus nine existing checks. New checks cover the sensor's multiple consequences, sequential fixes, multiple feasible solutions, energy/data conservation across all 32 combinations, eclipse/compatibility failures, budget failure, undo/reset, and storage overflow even with a fast radio.
- **14 graphical design integration checks**: E opens the console; default passes; keyboard selection exposes deficits; world/panel models agree; panels grow; mass and data fixes remain independent; a valid advanced design works; reading freezes position/heading; animation does not alter totals; undo/reset restore exact outcomes; closing/reopening preserves the session.
- **11 hub integration checks** are retained and rerun as regression coverage.
- Dependency consistency and compilation checks are included. No unnecessary repeat of the unchanged standalone GMAT backend.

## Desktop review

Selected Extended power, Heavy launch, and Fast radio with the mouse and inspected the visible power -> mass -> data -> passing chain in the actual window. Reviewed the 3D model changes, deltas, limiting-factor explanations, keyboard Backspace reset, and clicked Undo to restore the advanced design. U is covered by the scripted input harness; an independent held-key comfort test remains the user's manual check.

## Manual test

```powershell
cd 'E:\GitHub\Nasa Hackathon\Space Mission Design Game'
.\.venv\Scripts\python.exe main.py
```

Close any older build before launching to avoid confusing windows. Walk to the right-hand design console and press E. From Reset, try Advanced -> Extended -> Heavy -> Fast and compare the table above. Switch to Wide to reveal the budget limit, then Undo. Confirm a basic design also passes, keyboard navigation works, Escape restores walking, and changes remain when reopening the console. Reset and Undo should restore the complete configuration and model, not only its totals.

On Arch use `.venv/bin/python main.py` after the shared setup. Arch results remain untested, not passed.

## Repeatable commands

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/verify_design.py
.\.venv\Scripts\python.exe scripts/verify_hub.py
```

See README.md for precise units, cycle assumptions, source layout, and further review options. Raw generated evidence is ignored under runtime/. No saves, five-mission progression, readiness clearance, GMAT-backed geometry, launch cinematic, or multiplayer is claimed here.

## Next proposed phase

Phase 4: connect the five missions to explicit completion checks, add integrated readiness and local saves, and invalidate affected checks after earlier design changes. Request the user's approval before starting it.
