# Two-player LAN verification and handoff

Implemented 14 November 2026 in response to the user's request for different laptops on the same Wi-Fi, visible teammates, and independent tasks.

## What is implemented

- N opens a host/join lobby with name, IPv4 address and room-code entry. Host listens on TCP 8765; friend joins Science & Operations. Host is Spacecraft Engineer. Two participants maximum.
- Named colored astronaut geometry, heading/position interpolation, activity labels, distinct spawn positions facing each other. Avatars are visual and do not block movement. Existing navigation bindings were preserved.
- Role-scoped editing: engineer owns sensor/power/launcher; operations owns radio/orbit/plan/source. Both see the shared model and resource consequences. Undo is scoped to a player's own last edit; reset touches only owned categories.
- Host-authoritative sequential mission gates and readiness revalidation. Engineer owns design/readiness tasks; operations owns briefing/orbit/launch. Only a validated host result can advance the shared operational outcome.
- Host worker executes cached/live GMAT and simulation; complete frames/results are sent once on outcome events, not every movement update. Each client plays the same data independently. Changes lock until both finish, with disconnect cleanup and reconnect handling.
- Shared Lab door and occupancy guard for either player. Reading/pause panels remain local; learning-card completion is shared.
- Host-only crew save/load/new mission, with plan/source persistence. Solo save is separate. Disconnect status, avatar removal, explicit leave/rejoin, wrong-code rejection, occupied-role rejection, and catalog/model fingerprint checks.
- Bounded newline JSON; finite/bounded pose validation; no remote execution or pickle. Background socket readers/writers do not mutate Ursina. State is applied on the render thread. Content fingerprints normalize JSON and line endings for Windows/Linux checkouts.

## Evidence

28 unittest cases passed, including seven real two-client localhost TCP cases. The suite exercises simultaneous independent changes, an undo that preserves a teammate's setting, wrong-role and malformed selection/pose rejection, name/task/pose propagation, disconnect removal, wrong room code, both-role objective gates, shared operational success, both finish acknowledgements, readiness invalidation, doorway occupancy and host-only save/load.

`scripts/verify_crew.py` passed using a real graphical host and a second protocol client over localhost: lobby rendering, named avatar, shared geometry, simultaneous subsystem changes, role-specific progression, synchronized launch/report, finish acknowledgements, disconnect removal. QA images and structured evidence are under ignored runtime files. The oversized avatar label found during inspection was corrected. The design, hub, and cached solo campaign regression harnesses pass; pip check and compilation pass. The hub harness now supports both movement layouts used in this workspace without overwriting user navigation edits.

Restricted Codex sandbox execution initially blocked localhost with WinError 10013. The same tests passed with socket access. No system firewall, router, security settings, or system packages were modified.

## Remaining real-world acceptance

Two separate laptops over actual Wi-Fi have NOT been tested here. Arch Linux graphics/network/native GMAT remain unverified. Run both laptops from the same updated files; use N -> Host on one and N -> Join on the other. Enter the actual Wi-Fi adapter address, room code, and distinct names. Permit the host's intended private-network TCP connection if the OS firewall prompts. See README for device isolation and multiple-adapter troubleshooting.

Have one player read in the Lab while the other configures hardware, then open the same console on both and make independent edits. Verify names, movement/turning, activity labels, the shared door, coupled resource updates and shared readiness. Complete the distributed mission tasks, launch, skip on only one laptop and confirm edits stay locked until the other finishes. Save/load on the host and disconnect/rejoin the guest. Record OS/interpreter versions and results in this file before claiming two-laptop acceptance.

## Limits

Trusted LAN only, two fixed roles, no encryption, chat, host migration, avatar collision, or internet matchmaking. A lost connection requires explicit leave/join; a restarted host creates a new room code. A late reconnect during launch replays that outcome from the beginning. Cameras/playback are locally rendered; this is synchronized data/outcome playback, not frame-perfect lockstep cinematics. Pose replication is client-reported and bounded, not competitive anti-cheat. Persistent saves live on the host. Live GMAT runs only on the host. No new Python dependencies.
