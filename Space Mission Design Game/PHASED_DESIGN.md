# MISSION FORGE
## A 3D mission-design game in seven implementation phases

Design revision: 14 November 2026. Proposed plan, awaiting review. This replaces the earlier eight-objective campaign with five shorter in-game missions while preserving the engineering lessons. Seven implementation phases are development checkpoints, not seven levels.

### The experience
You are a mission engineer at an Earth-observation launch facility. Walk through a compact 3D mission-control hub, open the Learning Lab, configure a satellite, watch it launch, then operate it around Earth. Your purpose is to deliver useful flood observations to emergency responders.

The defining feature is a visible chain reaction: choosing a stronger sensor improves scientific capability but also increases mass, power demand, data production, and cost. The player repairs the resulting problems and sees the mission improve. A beautiful launch alone does not count as mission success.

### Small world, strong visual identity
- Mission-control hub: glowing Earth hologram, objective screen, and configuration console.
- Learning Lab: one player-opened door and a readable wall of concept cards.
- Launch-viewing gallery: window, rocket pad, and a few simple spectator figures. Show a launch after the readiness review, then transition to the orbital scene.
- Orbital scene: 3D Earth, satellite, orbit path, sunlight/eclipse indicator, and ground contact beam.

Use a navy, cyan, and amber palette, restrained lighting, simple geometry, and a few polished assets. Keep spaces close together. No open-world travel, character combat, or manual rocket piloting in the initial build.

### Controls
Arrow Up/Down walks forward/backward; Left/Right turns the player and camera. Movement physically brings the camera closer to or farther from objects. E interacts with doors and consoles; Enter confirms; Escape closes a panel or pauses. Mouse clicks select cards and options. Optional mouse-look can be added after keyboard navigation is comfortable.

Opening a readable panel pauses walking and releases the pointer. Closing it restores navigation. Use delta-time movement, collision boundaries, modest camera speed, and no compulsory head-bob. During launch, offer a short cinematic and a skip control.

### Scope target
One single-player scenario, five consecutive missions, about 10-15 minutes for a first playthrough, and a prepared five-minute jury presentation. These are design targets to verify in playtesting. Multiplayer remains a later extension.

---

# Five consecutive in-game missions
## Clear tasks, measurable outcomes, reversible decisions

| Mission | What the player does | Success check |
| --- | --- | --- |
| M1: Accept the assignment | Enter the Lab, inspect the Mission Goal card, and confirm the flood-monitoring requirements at the briefing console. | Brief accepted; target region, observation requirement, delivery deadline, budget, and duration recorded. |
| M2: Build the satellite | Select a sensor and power package. Watch the 3D model and resource deltas change. | Required observation quality met; configured mass and power checks pass. |
| M3: Connect the mission | Select one of two orbit presets and a communications package. Compare coverage, contact, storage, and cost predictions. | Orbit supports the target; preview shows sufficient timely downlink and storage. |
| M4: Earn launch clearance | Choose a launcher and run an integrated design review. Return to earlier consoles if necessary. | All required engineering checks pass, including orbit compatibility, total budget, and launch capacity. |
| M5: Deliver the science | Run accelerated orbital operations, compare an optional failed attempt, revise the plan, and deliver useful observations. | Scenario-defined quantity and quality delivered before deadlines; no required survival constraint violated during the assessment window. |

Mission checks belong to the model, not to animations or timers. Completing a cinematic cannot unlock the next mission. Changes invalidate affected downstream checks; the player keeps access to previously learned material. Save the selected configuration and objective state.

### Make the trade-offs the main attraction
Every option shows before/after values for budget, mass, available power, battery endurance, storage, and data delivery. Highlight the first limiting factor and explain it in one sentence. Provide at least two feasible designs rather than one hidden correct answer.

Example, using illustrative game values: the sensor upgrade adds 20 W demand, 8 kg mass, 15 budget credits, and doubles data production. A 10 W power reserve becomes a 10 W deficit; a larger power package fixes it but reduces budget and mass margin. The downlink may still need attention. These are invented teaching values, not NASA hardware specifications; balance and verify them in Phase 3.

### Simple simulation rules
Mass and cost are sums including launch and ground services. Battery energy changes by (generation - demand) multiplied by elapsed hours; eclipse removes solar generation. Stored data increases during observations and decreases during eligible downlinks. Observation quality and delivery latency determine useful science. Show power in W, energy in Wh, mass in kg, data in MB, and costs in labeled game credits.

Numerical scenario thresholds are data, not hardcoded UI rules. Set and verify them in Phase 3; evaluate coverage and contact from time-stamped trajectory geometry in Phase 5. Model lifetime as a chosen service-duration requirement and cost driver, not a claim to predict years of hardware reliability.

---

# Technology and NASA integration
## Ursina renders the game; a separate model explains the mission

### Engine choice
Use Python 3.12 and a tested, pinned stable Ursina release; 8.3.0 is the current PyPI candidate checked for this proposal. Ursina provides Python-based 3D scenes on Panda3D. Validate the actual Windows and Linux graphics environments in Phase 1. LibHunt is a discovery link; use the official project and package documentation for implementation.

### Architecture boundaries
- Presentation: Ursina rooms, player/camera, interactions, cards, spacecraft, launch, and orbital rendering.
- Domain model: scenario, components, resource calculations, checks, objective state, and mission results; independent of Ursina imports.
- Orbit provider: interchangeable simplified teaching model and GMAT-backed data source.
- Persistence/content: versioned JSON for scenarios, learning cards, configuration, saves, and reports. Keep local machine paths outside shared content.

### GMAT is required integration work
NASA catalog GSC-19468-1 identifies GMAT. Use it to generate a trajectory for the selected supported orbit; import time-stamped state data into the game. The game derives target visibility, contact windows, and eclipse geometry using documented assumptions. GMAT does not calculate our game budget, learning progression, or rocket animation.

Proposed bridge: scenario/orbit settings -> generated GMAT script -> separate console process -> report data -> validated normalized trajectory -> Ursina playback and resource simulation. Use a worker process, a timeout, and visible progress so the game remains responsive. Prefer this file/process boundary initially over embedding version-sensitive Python bindings. Confirm executable names, flags, and report fields against the installed distribution before implementation.

Target the user's installed GMAT R2026a. Phase 1 proves a small standalone GMAT run; Phase 5 connects changed game inputs to changed GMAT outputs. Record frame, epoch/time scale, units, version, and input hash; convert coordinates consistently before drawing or computing contacts. Compare sampled positions and one contact interval with an independent check.

Cache validated GMAT trajectories for the two supported orbit presets. Label playback as cached GMAT data; label the simplified mode separately. A cache is valid only for matching inputs. Installation failures remain visible, and GMAT integration cannot be marked complete using only a mock or cache. Do not launch a new GMAT process every rendered frame.

### NASA mission-design approach
Map the guide's need, concept, requirements, design, verification, and implementation sequence to the five missions. Represent launch, space, ground, and user segments through the pad, satellite, station, and delivered flood observations. Each requirement gets a check before implementation. This is an educational adaptation, not NASA certification. [S1]

---

# Phases 1 and 2
## Establish compatibility, then build the walkable learning space

### Phase 1 - Reproducible setup and integration proof
Deliver a Python project skeleton, pinned dependencies, a minimal Ursina window, and a standalone GMAT sample run. Confirm a usable trajectory report from the installed GMAT without yet connecting it to the full game. Resolve Python/engine/platform compatibility before making assets.

Create a cross-platform scripts/bootstrap.py using the Python standard library: check the interpreter, create a project-local virtual environment, install pinned Python requirements, and print exact run commands. Add scripts/doctor.py to report interpreter, imports, graphics smoke-test status, and GMAT path/version. Optional PowerShell and shell wrappers call the same bootstrap logic.

The bootstrap installs project Python dependencies. It detects missing Python, desktop graphics drivers, and GMAT and prints manual instructions; it does not silently install system packages or elevate privileges. GMAT setup uses a configurable GMAT_BIN/local config, not a committed absolute path. Avoid Blender-dependent assets in the initial build.

Manual test: both teammates run setup on their machines, open and close the 3D window, and run the GMAT sample to a non-empty, readable report. Record actual Python, Ursina, GMAT, OS, and graphics results. A missing platform result is pending, not passed.

Exit gate: working local 3D smoke test and GMAT proof; Linux compatibility either evidenced or explicitly pending user test. Resolve any GMAT blocker before committing to the bridge design. Update the tracker, summarize limitations, and ask whether to start Phase 2.

### Phase 2 - 3D hub, movement, door, and Learning Lab
Build the compact hub and Lab with collision boundaries, arrow-key movement and camera, E interactions, and a door that visibly opens. Add the first readable card panel and then populate a small card library.

Cards: mission purpose; science requirements; spacecraft and instruments; mass and launch capacity; power versus energy; orbit and coverage; communications and data; budget and lifetime; four mission segments; verification and trade-offs. Each has a short explanation, one example, a decision consequence, and a source link. Offer optional external learning resources; no video or internet is required to finish the game.

Manual test: walk toward and away from the console, turn, collide with a wall, open the Lab, inspect and close cards, then resume movement. Try closing a panel with Escape and verify that navigation does not continue behind it. Check text at the demo resolution and test the keyboard path.

Exit gate: a comfortable, readable explorable 3D scene. No mission simulator is claimed yet. Update the tracker and ask whether to start Phase 3.

---

# Phases 3 and 4
## Prove the trade-offs, then turn them into a campaign

### Phase 3 - Spacecraft configuration and consequence engine
Implement the core domain model and a visible configuration console. Start with two sensor choices, two power packages, two communications packages, two orbit presets, and two launcher options. Keep structure, computer, and attitude control as a visible fixed baseline. This represents the full spacecraft without excessive menus.

Define scenario thresholds and component parameters in one catalog. Include launch cost, ground-service cost, energy units, storage capacity, and operating duration. Add at least two feasible designs and one deliberately failing design. Keep all invented numbers labeled as game assumptions.

Show immediate numerical deltas, affected subsystems, and a human-readable reason when a choice creates a deficit. Let players compare the previous and current design and undo a selection. Update visible solar panels or sensor geometry on the spacecraft.

Manual test: upgrade the sensor and observe more science capability alongside increased cost, mass, power, and data. Add power capacity, observe the new budget/mass impact, then fix a communications bottleneck. Confirm restoring the original selection restores the original totals.

Verification: meaningful model checks for sums, units, energy/data balances, and two feasible solutions. No per-frame simulation process or animation may change engineering totals.

Exit gate: a player can explain a real chain of consequences from the interface. Update the tracker and ask whether to start Phase 4.

### Phase 4 - Five missions, readiness review, and saves
Connect M1-M5 into a progression state machine. Make tasks and completion rules visible at the relevant consoles. Integrate orbit/launcher selections, the briefing, a readiness review, local saves, reset, and result structure. Use the clearly labeled simplified orbit provider while the final bridge is pending.

The integrated review checks quality, target coverage, budget, spacecraft/launcher mass compatibility, power feasibility, storage/downlink, and chosen duration. M5 can use a basic operations view before the orbital spectacle arrives. Earlier design changes must invalidate relevant review results and re-evaluate affected missions without deleting the player's save.

Manual test: attempt to skip ahead; fail readiness with a known bad design; fix it; unlock the next mission; change an earlier component; confirm affected checks become pending; save, quit, reload, and reset. Complete one full run with the temporary provider.

Exit gate: an end-to-end single-player learning loop works, with honest provider labeling. Update the tracker and ask whether to start Phase 5.

---

# Phases 5 and 6
## Connect real orbit data, then make the result memorable

### Phase 5 - GMAT bridge and orbital operations
Connect the Phase 1 proof through the orbit-provider interface. Generate a script from supported orbit selections, run GMAT separately, validate report data, and feed it into Earth/satellite playback. Compute simplified observation opportunities, ground contacts, and eclipses using a consistent frame and time base. Drive power, battery, storage, and delivered observations from the same simulation timeline.

Display trajectory provenance: live GMAT, cached GMAT with matching inputs, or simplified teaching mode. A failure offers retry or an explicitly labeled fallback; no hidden substitution. Keep GMAT-generated reference data and script inputs available for inspection.

Manual test: run orbit A and then orbit B; verify their GMAT inputs and reports differ and the game shows the corresponding path. Inspect an eclipse and contact window; battery/solar and downlink indicators must agree with the scene. Compare sampled positions, units, and one computed contact against a reference calculation. Remove the configured executable temporarily and verify a clear diagnostic rather than a frozen game.

Exit gate: evidence of one real end-to-end GMAT run and valid orbital/resource behavior; cached offline playback also works. Cross-platform bridge status is recorded separately. Update the tracker and ask whether to start Phase 6.

### Phase 6 - Launch gallery, failure feedback, and mission report
Polish the gallery with spectators, rocket, lighting, exhaust, countdown, and a brief launch sequence. Switch to the orbital scene and show data flowing to the station. Add a compact report comparing useful observations, deadlines, cost, margins, and the causes of failure.

Tie spectacle to meaningful outcomes. An overweight spacecraft produces a blocked launch clearance. A bad power or downlink plan produces an orbital operational failure. Do not depict a rocket crash as the consequence of an unrelated satellite communications choice. A physical launch-failure model and crash sequence are optional later work, not required for the first build.

Provide a prepared failure-and-repair route. An optional explicitly labeled design-preview mode can demonstrate orbital failure before clearance; normal campaign progression continues to enforce readiness. Cinematic camera motion can be skipped; operational failure remains visible in telemetry and explanations.

Manual test: watch and skip the cinematic, replay it without duplicate spacecraft, run a known success and failure, read the cause, change the relevant choice, and compare results. Confirm spectacle and result calculations agree.

Exit gate: a visually strong, understandable demonstration with actionable feedback. Update the tracker and ask whether to start Phase 7.

---

# Phase 7 and manual prerequisites
## Prove the two-machine setup and rehearse the five-minute story

### Phase 7 - Portability, demo mode, and release readiness
Run the same Python bootstrap from a clean checkout on Windows and the colleague's Arch Linux machine. Keep one codebase, not separate OS editions. Confirm asset filename case, a desktop graphics session, writable saves, local GMAT configuration, and cached playback without internet. Test the real bridge on both systems where installed. Arch compatibility with GMAT's packaged native libraries needs verification; record it separately from Python compatibility.

Create a labeled presenter route with quick navigation, a prepared design, and reset. It must use the real domain calculations. Any checkpoint skipping is visible as demo mode; ordinary play keeps consecutive missions. Bundle approved assets and learning text locally and track their sources/licenses.

Manual test: start from a fresh session, perform the full five-minute presentation twice, recover from a failed GMAT launch, reload a save, and reset the demo. Check readable text and stable frame rate at the actual presentation resolution. Keep a recorded run as a backup if time allows.

Exit gate: documented Windows/Linux results, known limitations, a reproducible demonstration, and a complete tracker. Ask whether to revise, stop, or plan a new feature phase. Multiplayer is not automatically authorized.

### What may need manual installation
- Python 3.12 with pip and virtual-environment support on both machines. The currently active local interpreter checked during planning is Python 3.10.14; this does not establish whether another compatible interpreter is installed. Use a dedicated project environment, not a forced system upgrade.
- The colleague uses Arch Linux. Check that the chosen interpreter can create the project environment and open a graphics window. Avoid Ubuntu-specific package commands. A working desktop session and graphics driver are needed for 3D tests.
- You supplied a Windows GMAT R2026a folder under Downloads. Validate that local installation in Phase 1. Your colleague needs a compatible Linux GMAT build for live runs; Python cannot execute the Windows binary on Linux. Cached playback can keep the game usable while native compatibility is investigated, but does not prove a live Linux bridge.
- Internet is needed once for Python dependency installation. The core presentation should work offline after setup. Blender, Unity, a browser server, and a database are not initial requirements.

### Phase-review rule
After every phase: update PROJECT_TRACKER.md, state what was delivered, give exact manual test commands and expected outcomes, distinguish automated results from user-observed results, list limitations, propose the next phase, and ask whether to continue. Do not start the next phase until the user explicitly agrees. A request for fixes remains within the current phase.

---

# Team plan, presentation, and sources
## Keep ownership simple and the demo focused

### Split for two people
Person A owns Ursina scenes, navigation, cards, controls, and cinematics. Person B owns mission data, trade-off calculations, progression, saves, GMAT bridge, and reports. A also owns explanatory copy and report presentation to balance workload. Both agree on the data contract, connect their work frequently, and review the end-to-end demo. Setup and portability are shared.

### Split for three people
Person A owns the 3D environment, camera, interactions, and visual effects. Person B owns engineering/resource models, GMAT, and operations. Person C owns mission progression, content, saves, UI panels/report assembly, and integration coordination. B supplies engineering check results; C maps them to objective gates; A renders the world. Each person verifies their own changes.

### Suggested five-minute jury presentation
| Time | What to show |
| --- | --- |
| 0:00-0:30 | Explain the flood-response need and the mission's measurable goal. |
| 0:30-1:05 | Walk into the Lab, open one card, and connect the lesson to a design choice. |
| 1:05-2:25 | Upgrade the sensor, show power/data/cost consequences, and repair the design. |
| 2:25-3:05 | Pass the review and watch the launch from the gallery. |
| 3:05-4:20 | Show GMAT-backed orbital playback, eclipse/contact effects, and useful data delivery. |
| 4:20-5:00 | Show the report, explain what was learned, and distinguish real GMAT work from the teaching model. |

### References checked for this proposal
[S1] NASA, Design and Develop Science Missions, 26 March 2025, especially slides 8, 10, 13, and 19: https://www.nasa.gov/wp-content/uploads/2025/04/250323-design-and-develop-science-mission.pdf

[S2] Ursina official installation guide: https://www.ursinaengine.org/installation.html

[S3] Ursina package metadata (Python >=3.12; stable candidate 8.3.0): https://pypi.org/project/ursina/

[S4] NASA GMAT catalog entry: https://software.nasa.gov/software/GSC-19468-1

[S5] GMAT R2025a distribution notes (console on Windows/Linux): https://sourceforge.net/projects/gmat/files/GMAT/GMAT-R2025a/

[S6] NASA GMAT source/distribution documentation: https://github.com/nasa/GMAT

Also considered: the original design PDF and the user's challenge/resource notes. LibHunt could not be fetched, so engine facts were checked against primary sources. The catalog labels R2025a; the user supplied an R2026a installation folder, matching the newer project release. Use R2026a documentation and verify the installation in Phase 1. Integration compatibility remains unproven.
