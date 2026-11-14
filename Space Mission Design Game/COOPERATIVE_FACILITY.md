# Cooperative engineering facility: implementation and handoff

Implemented 2026-11-14. This extends the existing Ursina game, with no new dependencies.

## Latest revision: retrieval, red screen, stacks and mission EUR budgets

This revision supersedes the original single-visible-item and credit-cost descriptions below. E retrieves an already placed owned component; a second E resubmits it. The host checks ownership, proximity and launch-busy state. Retrieval clears assembly and campaign approval, preserving unaffected contributions. The plan desk uses left/right and E for orbit/launcher tablets.

All confirmed, unsubmitted inventory renders as a height-spaced vertical stack on local and remote carrying anchors. Stack Base in the inventory changes the lowest item. Geometry remains extracted from the existing spacecraft; planning tablets remain distinct from hardware.

The large room screen shows current failed requirements and measured values in red, return stations and suggestions. Two issues display at a time, cycling every seven seconds. Total euro cost, mission budget, remaining/overspent funds and contribution counts remain visible. E at the screen opens details and permits host validation there or at the central console.

Flood Watch owns a **EUR 145,000** budget in `content/missions.json`. The component catalog contains EUR prices, including bus and ground service. The old monetary numbers were scaled by 1,000; physical values and nonmonetary equations are unchanged. Catalog loading reads the mission budget, host snapshots carry canonical totals/issues and clients apply the same selected mission budget. Workstation options show individual prices and projected totals/remaining funds. Overspend may be previewed but cannot be collected, approved or launched. Retrieval keeps the selection/cost reserved until a replacement is selected. New report keys end in `_eur` instead of `_credits`; old design saves retain their component IDs and are re-evaluated on load. Existing result summaries remain readable. All clients must update together because the content fingerprint changes.

**50 automated tests** passed, including euro totals, budget boundary changes, collection rejection, retrieval/invalidation, permissions, proximity and synchronization. **14 rendered revision checks** passed: five-item stack, E retrieval/resubmission, plan E controls, red engineering feedback and the exact EUR 3,000 overspend example. The existing facility (18), design (14), cached campaign and four-client graphical checks passed. Separate Wi-Fi and Arch remain manual. No library, spacecraft geometry, navigation, campaign-domain or orbit/operations files were changed by this revision. Authorized changes are monetary fields/calculation inputs, validation/carrying presentation and synchronization.

Run `python scripts/verify_integration_revision.py` and `python -m unittest discover -s tests -q`. Evidence is in ignored `runtime/integration-revision/`.

## Rooms and entry

Select **Flood Watch** at the mission screen beside the original Earth/orbit display. Mission 02 is disabled both in UI and domain logic. The dedicated `content/missions.json` catalog references the existing configuration rather than duplicating hardware data. Selecting the real mission records acknowledgment of its existing purpose/brief, so the educational library remains optional.

The original spawn shell, floor, dimensions, decorations and Earth/orbit display remain. The previous design console now opens a workshop directory; its geometry remains. The existing satellite object moves to Integration as requested. The Library books, reader, assets, lessons, navigation and animations remain byte-for-byte unchanged. User authorization explicitly permits one new doorway in its right wall, at x=7 / z=9. Its wall elsewhere is identical; a floating question-mark controls object is the only other direct Library addition.

The new wing connects physically along +X: **Payload Design** (x=16), **Power Systems** (30), **Communications** (44), **Mission Planning** (58), **Satellite Integration / Validation** (72), then its **Launch Readiness** desk. Corridors, illuminated doorway frames, floor guidance and room signs connect them. All rooms permit return travel. Confirmations enforce the workshop order; visiting a later room never bypasses missing engineering contributions or approval. One raised cable crossing at x=37 requires Space; the low service beam at x=51 requires Alt. The original floor and door in the spawn/library stay intact.

## Roles, tables and state

Stable session slot IDs (`engineer`, `operations`, `crew3`, `crew4`) identify players, not engineering permissions. Engineering roles are separate and assigned in contiguous, balanced groups in stable slot order:

| Active players | Distribution |
| --- | --- |
| 1 | Host/solo owns Science, Power, Communications, Flight |
| 2 | Host: Science + Power; guest: Communications + Flight |
| 3 | Host: Science + Power; guest 1: Communications; guest 2: Flight |
| 4 | Science; Power; Communications; Flight: one each |

Science owns sensor; Power owns power package; Communications owns radio; Flight owns orbit and launcher plus operations plan/source/launch. The host alone selects mission, finalizes validation and manages shared saves. All five component categories and their ten existing options remain exactly as defined in `design_catalog.json`. Each workshop has exactly one table per connected participant (1Ã¢â‚¬â€œ4). Relevant tables show responsibilities, selected choice and confirmation status; other tables are informational. The crew panel shows names, role assignments and confirmation counts. Membership changes rebuild tables and permissions without discarding valid choices.

## Select, collect and carry

Press E by your table. Inspect the original option names, descriptions and specifications. Select and explicitly **Confirm & Collect** each category, including unchanged defaults. Earlier workshops must be confirmed first. Permissions are checked on the host; confirming and submitting also require proximity to the corresponding station. A player may inspect another table but cannot alter its selections. Inventory (**I**) lists confirmed, unsubmitted choices and changes the visible held item. Only one item is held, avoiding overlaps when a player owns several roles.

Physical sensor, array and radio views reuse the original `Spacecraft` geometry and apply the actual design selection; no second satellite geometry implementation was written. Orbit/launcher appear as plan tablets, never as components bolted into the bus. Items have no collision volumes. Local carried items follow the camera at a side carrying position; remote items follow the astronaut, including vertical displacement and crouch scaling.

## Integrate, validate, revise and launch

At the integration table, E places payload, power and radio at their labeled points. Use the separate Mission Plan desk to submit orbit and launcher individually. Each submission records its current option and submitting player; duplicate placement and unauthorized submission are rejected. Shared views animate newly drawn placement representations settling onto the table. Group status shows submitted roles and missing contributions.

All five contributions are necessary before host validation. `Assembly.validate` calls the existing `DesignSession.preview` results without replacing equations. Feedback uses each original check's measured values/limits and explanation, plus all relevant contributing categories, current owners, engineering roles, return stations and practical suggestions. Failed checks are shown first. Success approves the exact configuration and completes the existing campaign review gates using `Campaign.advance`.

Editing a choice invalidates approval and that category's confirmation/submission. Unaffected submissions remain. Reconfirm and resubmit changed items, then validate again. Launch requires both new integration approval and the original campaign approval for the same design, plus proximity to Launch Readiness. The flight engineer controls the existing launch button, source and plan. Trajectory generation, operations math, scientific delivery criteria, telemetry, cinematic and result calculation are unchanged.

The world satellite is the **same pre-existing `hub.spacecraft` instance**, moved to the central table, with identical scale, styling, component updates and the unchanged `Hub.tick` rotation increment (`dt*8`). `spacecraft.py` was not modified. It remains visible during assembly and validation rather than being replaced by a static model.

## Movement and help

W/S walks, A/D strafes, left/right arrows turn. Those bindings are unchanged. Space applies a single grounded jump impulse; gravity returns the player to floor/raised crossing. Alt is held crouch, with left/right/general Alt events supported, lower eye height and reduced travel speed. A height-aware volume layer supplies blockers to the existing horizontal `advance` function; it also checks low ceilings, raised landing surfaces and standing clearance. No airborne re-jump or indefinite flight is added. Panels freeze movement, and the library's own input branch remains untouched. The question-mark help shows the actual keys and can be closed normally. Mouse look remains unimplemented, as before; the mouse stays free for interface selection.

## Networking and saves

The existing newline-JSON TCP server/client, LAN address/code flow, bounded queues, lock and socket-thread/main-thread separation are reused. Four slots replace two fixed responsibilities. Protocol v2 and the expanded content fingerprint require the same checkout on every laptop. Host snapshots carry mission, assignments, confirmations, inventory, current held item, submitted choices and provenance, validation and exact-design approval. Authoritative actions under the existing room lock prevent conflicting edits and duplicate placement. Position broadcasts add vertical displacement/crouch. A fifth player is rejected. Guests reconnect through the existing Leave/Join flow and receive a complete snapshot in an available slot; identity recovery and host migration are not added.

A single connected host can complete and launch a crew mission. Guests leaving redistribute all four roles, preserving selected configuration and valid submissions. If the host/server goes away, use N to leave and reconnect or continue solo with the retained design. Local integration records are conservatively reset on leaving a session. Existing finish acknowledgements support any current participant count, and disconnected players stop blocking playback completion.

Campaign save schema remains version 1, with additive `assembly` data at the presentation/network boundary. Design, results and source/plan data keep their original format. Restoring a save preserves consistent confirmed choices but conservatively requires resubmission and fresh approval; older saves have no assembly records and therefore require recollection. No legacy saved approval can skip the new physical integration requirement.

## Suggested five-minute demo

1. 0:00Ã¢â‚¬â€œ0:30: host/join and show balanced roles; select Flood Watch.
2. 0:30Ã¢â‚¬â€œ1:00: briefly show the preserved Library and controls help; enter the wing.
3. 1:00Ã¢â‚¬â€œ2:15: demonstrate Advanced sensor with Compact power; confirm defaults for other categories, carry and submit parts/plans.
4. 2:15Ã¢â‚¬â€œ3:15: show failed power/data checks; return to Power, Communications and Planning for Extended power, Fast radio and Heavy launcher; reconfirm/resubmit.
5. 3:15Ã¢â‚¬â€œ4:00: host validates; point out exact original mass/budget/power totals and the rotating spacecraft.
6. 4:00Ã¢â‚¬â€œ5:00: flight engineer uses Cached + Targeted at Launch Readiness; skip cinematic as needed and show the real calculated outcome.

## Verification

- **46 automated tests pass**: the prior 33 plus nine assembly/locomotion and four real-TCP cooperative tests. Coverage includes every player count, all roles, permission/capacity errors, workshop order, proximity, missing/duplicate contributions, consistent snapshots, correction invalidation, safe persistence, disconnect/rejoin, jump/gravity, raised landing, crouch/standing clearance and one-player authoritative launch/finish.
- Existing LAN launch test now performs required physical confirmation/submission/validation; it retains the previous result/acknowledgement assertions. Other original unit tests are unchanged.
- `scripts/verify_facility.py`: **18 scripted graphical checks** including doorway, jump/crouch routes, carried part, all role responsibilities in solo, failed design, correction/resubmission, original rotating spacecraft, original trajectory-driven launch/result and library movement capture.
- `scripts/verify_four_player_scene.py`: graphical host plus **three real TCP clients**; unique roles, remote held parts and crouch/jump poses, collective submission, shared approval, edit invalidation and disconnect redistribution.
- Updated `scripts/verify_crew.py`: two-player concurrent selection, physical integration, shared launch/results, both completion acknowledgements and disconnect cleanup passed.
- Existing hub harness: **11 checks pass**. Design harness: **14 checks pass**, with its entrance assertion updated to the new workshop directory while retaining all original engineering/geometry/undo/reset checks through the compatible preview API.
- Existing cached campaign graphical harness passes unchanged.
- Existing library graphical harness passes unchanged: all 12 books, 38 chapters/spreads, navigation and animation cleanup. All library files are unchanged in Git.
- The game launches via `main.py --smoke-seconds 2`. Graphical evidence is in ignored `runtime/facility-review/`; prior evidence paths remain unchanged.

Reproduce from this directory with the virtualenv Python:

```text
python -m unittest discover -s tests -q
python scripts/verify_facility.py
python scripts/verify_four_player_scene.py
python scripts/verify_crew.py
python scripts/verify_hub.py
python scripts/verify_design.py
python scripts/verify_campaign.py
python -m game.library.verify
```

Network tests require localhost socket access; restricted agent sandboxes can deny it. This session used approved local socket access and did not change firewall settings.

### Remaining manual acceptance

Tests are scripted Windows checks, not a claim that four physical laptops were tested. On the actual Wi-Fi, verify one host plus 1Ã¢â‚¬â€œ3 guest laptops, correct Wi-Fi IPv4 and firewall access, simultaneous walking/carrying, confirming at assigned tables after each join/leave, both traversal passages, placement visibility, failure/correction, launch and returning from results. Verify Arch native graphics and Alt key events on that laptop. No dependency changes are required, but native graphics support still depends on the OS. Live GMAT was not rerun for this enhancement; the unchanged provider and cached mission flow were regression-tested. No host migration, account-based reconnect identity, WAN hosting or encrypted transport is added. Page/mission panels remain local; snapshots synchronize engineering decisions.

## Original facility preservation audit (before the EUR revision)

No unrelated game systems or other repository projects were intentionally changed. Protected files have no diff: `content/design_catalog.json`, all `game/library` and `content/library` files, `game/domain/design.py`, `campaign.py`, `operations.py`, `navigation.py`, `game/orbit`, and `game/presentation/spacecraft.py`. Original physics/specifications and mission results are preserved. Necessary shared-file edits are limited to the new world extension, approved doorway, movement layer, interaction/launch gating, dynamic roles and state synchronization. The old isolated selection entry is now a physical-workshop directory. Test harness assertions were adjusted only where those intentionally requested flows changed.

## Complete source change manifest

Paths below are repository-relative. Runtime screenshots/reports and bytecode are ignored. No build artifacts or external assets are added.

- `PROJECT_TRACKER.md`
- `Space Mission Design Game/COOPERATIVE_FACILITY.md`
- `Space Mission Design Game/README.md`
- `Space Mission Design Game/content/missions.json`
- `Space Mission Design Game/game/domain/assembly.py`
- `Space Mission Design Game/game/domain/facility_layout.py`
- `Space Mission Design Game/game/domain/locomotion.py`
- `Space Mission Design Game/game/network/lan.py`
- `Space Mission Design Game/game/presentation/carried.py`
- `Space Mission Design Game/game/presentation/crew.py`
- `Space Mission Design Game/game/presentation/facility.py`
- `Space Mission Design Game/game/presentation/hub.py`
- `Space Mission Design Game/game/presentation/mission.py`
- `Space Mission Design Game/scripts/verify_crew.py`
- `Space Mission Design Game/scripts/verify_design.py`
- `Space Mission Design Game/scripts/verify_facility.py`
- `Space Mission Design Game/scripts/verify_four_player_scene.py`
- `Space Mission Design Game/tests/test_assembly.py`
- `Space Mission Design Game/tests/test_four_player.py`
- `Space Mission Design Game/tests/test_lan.py`

## Revision files

The latest revision changes the mission/component catalogs, assembly and design monetary handling, LAN actions/snapshots, carried views, crew/facility/design/mission/HUD presentation, test coverage and documentation. New modules: `game/domain/economy.py`, `tests/test_integration_revision.py`, `scripts/verify_integration_revision.py`. The existing design test now refers to `cost_eur`; the four-player graphical harness additionally verifies the number of visible stack items against each remote inventory. No dependencies or external assets were added.
