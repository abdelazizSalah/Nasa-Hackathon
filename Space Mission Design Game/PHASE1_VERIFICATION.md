# Phase 1 verification - 14 November 2026

Historical Phase 1 record. The user approved proceeding to Phase 2 on 14 November 2026. Arch Linux results remain pending. The default scene is now the Phase 2 hub; use `main.py --engine-check` for the renderer proof described below. See PHASE2_VERIFICATION.md for current controls.

## Environment

- Windows 11, Intel UHD Graphics.
- Dedicated `.venv` created using the existing user Python 3.13.0; default Python unchanged.
- Ursina 8.3.0, Panda3D 1.10.16; full version pins in requirements.txt.
- GMAT distribution README identifies R2026a; console reports build date 26 March 2026.

## Evidence obtained

- Isolated bootstrap installed dependencies; repeat invocation succeeded with requirements already satisfied.
- `pip check`: no broken requirements.
- Four unittest checks passed: truncated report rejection, non-finite sample rejection, startup copy isolation, and actionable missing-GMAT diagnostics.
- A timed renderer run recorded 399 frames in 5.006 seconds. The final scene was inspected through the desktop, including readable text, shaded 3D sphere, orbit, and animated satellite. Escape was sent to the selected game window and the process exited with code 0.
- Three real GMAT runs completed successfully in separate run directories, including the final combined doctor command. The reviewed reports have 11 rows spanning about 599.9999988 elapsed seconds in 60-second increments.
- The final five-second graphics check recorded 319 frames in 5.000 seconds after the camera/lighting corrections. The combined doctor command exited with code 0.
- Initial state: position (6993, 0, 0) km; velocity (0, 6.63823568, 3.60426790) km/s. Frame EarthMJ2000Eq; epoch input 14 November 2026 12:00 UTCGregorian; report uses GMAT A1ModJulian.
- Validator checked finite values, sample count, elapsed times, A1 time agreement, expected radius/speed, and movement. This is a two-body propagation smoke test, not independent validation of all GMAT physics.
- Generated artifacts include the exact script, input hash, startup copy, raw report, console log, and metadata under ignored runtime folders. Re-run locally rather than relying on someone else's absolute paths.

## Resolved setup issues

- Initial pip network access was unavailable inside the restricted sandbox; downloading into the project environment succeeded with network access enabled.
- GMAT could not see its existing data directories under the restricted agent sandbox. The same generated script succeeded with access to the installed data. Do not relocate the install based on this sandbox-specific error.
- Unused Python/MATLAB/Fmincon interfaces initially emitted missing-plugin warnings. The proof now disables them in its generated startup copy; no additional Python ABI or MATLAB installation is needed.
- Visual inspection caught a color API mismatch (rgb uses normalized values in this engine release). The scene now uses rgb32/rgba32 and shows the intended space palette.

## Not yet verified or implemented

- Arch Linux dependency installation, graphics, and GMAT native-library compatibility.
- User's manual acceptance, Python 3.12-specific execution, or clean installation on a second Windows machine.
- Arrow navigation/rooms/cards, mission progression, trade-off calculations, or the in-game GMAT adapter. These remain later phases.

## Manual acceptance commands

See README.md for installation/configuration and the equivalent Arch commands. In the project directory on this machine:

```powershell
.\.venv\Scripts\python.exe scripts/doctor.py --graphics --gmat
.\.venv\Scripts\python.exe main.py
```

Check the five-second scene and 11-sample PASS message, then confirm the interactive scene remains open and Escape closes it. Report errors before approving Phase 2.
