# Remaining-phase verification and handoff

14 November 2026. User authorized autonomous completion of remaining phases, superseding old per-phase approval gates.

Implemented: five consecutive missions; readiness bound to exact configuration; local versioned saves; input-keyed cached and real GMAT subprocess providers; background worker and visible failure/retry; trajectory-driven energy/data/contact/observation simulation; launch sequence with spectators; accelerated orbital scene and contact beam; success/failure report and previous-attempt comparison; offline presentation route.

Verified on Windows/Python 3.13/Ursina 8.3: 21 unit tests; 14 design and 11 hub graphical checks; cached end-to-end campaign; live GMAT worker -> game -> debrief path. Both 7000 km/28.5 degree and 7200 km/98 degree presets ran through installed GMAT R2026a, producing 601 samples each. Checked finite states, radius bounds, monotonically spaced elapsed time and A1 epoch consistency. Compared different preset paths and hashes. Independent reference checks exercise the initial overhead ground contact and eclipse existence; a precision access-tool comparison remains outside this educational model.

Cached trajectories contain only generated numerical data and portable metadata, no machine-specific GMAT executable paths. Live runs keep script, report and console logs in runtime. Cache selection is explicit and hash-matched. No hidden fallback or live claim for cached data. The backend's native files remain unchanged.

Operational regression: targeted default produces 120 MB and delivers it with zero overflow/unserved energy; continuous imaging loses data and fails. This makes operational scheduling a further trade-off beyond hardware selection. The run uses a synthetic epoch-relative equatorial site and approximate Sun/shadow geometry; see README for exact rules. The Phase 3 preview remains a conservative preset trade study, not the orbital simulation itself.

Rendered frames inspected: mission-tablet.png, orbit-view.png, mission-result.png under ignored runtime. Fixed stale panel backgrounds and flight overlay visibility found during review. Existing A/D turn and arrow strafe controls remain; M opens objectives/saves. No additional Python dependencies were needed.

Known verification gaps: no access to colleague's Arch session, no clean second-machine installation, and no independent human timed rehearsal. Phase 7 is therefore not fully platform-accepted. The shared bootstrap, native-library diagnostics and offline mode are ready for those checks. Run `scripts/bootstrap.py`, unit tests, `scripts/verify_hub.py`, `scripts/verify_design.py`, `scripts/verify_campaign.py`, and optionally `scripts/verify_campaign.py --live` on Arch. Do not silently install OS packages or modify security settings.

Suggested next work after independent testing: improve rocket/planet art, refine targeting/contact physics, and plan multiplayer separately. No multiplayer functionality is claimed. The five-minute route is in README; latest campaign and report files are local runtime JSON.
