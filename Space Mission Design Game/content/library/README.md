# Mission Forge: Aerospace Field Library

Implemented 2026-11-14. This guide is intentionally library-specific; the existing main README and campaign tracker were left untouched.

## Enter and read

Launch normally from the project directory (`.venv\Scripts\python.exe main.py` on Windows, `.venv/bin/python main.py` on Linux). No installation or new dependencies are required by this enhancement. Use the game's existing movement controls, open the Learning Lab door with E, and use E at the original library console. Alternatively, click a physical book when close to the shelves.

On the bookshelf, hover for the full title, difficulty and opening hint. Click a cover, or select with arrows/Tab and press Enter. Each hardcover has thickness, a named spine, a separate hinged cover and an original subject illustration. Opening eases the book out of the shelf into the reading position. Closing reverses the motion. Next/previous pages use an animated plane; rapid additional page requests are ignored until the turn finishes.

The two-page reader has bounded text pages, original diagrams and paginated engineering comparisons. Left/right changes spread; up/down changes chapter. Mouse buttons provide page and chapter navigation, contents, sources, review and close book. T opens contents; R opens the reference desk. CLOSE BOOK returns to the shelf; Escape / CLOSE exits the library, animating the return if a book is open. Closing through existing external game interfaces disposes the reader immediately and safely.

SEARCH matches words across the chapter corpus, including comparison tables. GLOSSARY contains 42 terms. REVIEW has three questions and revealable answers per book; it awards no score. Chapter/spread positions restore per book in `runtime/library-reading.json`, separate from campaign and crew saves. Missing/corrupt position data falls back to the first chapter.

## Collection

1. **Introduction to Space and Spaceflight** — Beginner; 3 chapters.
   - The space environment
   - Gravity, inertia and falling around Earth
   - Choosing a kind of spacecraft
2. **How to Design a Space Mission** — Beginner / Intermediate; 3 chapters.
   - From a science question to requirements
   - Budgets, margins and fair trade studies
   - Maturity, reviews and evidence
3. **Spacecraft Anatomy and Subsystems** — Beginner; 3 chapters.
   - The bus and its payload
   - Following energy, heat and information
   - The ground segment completes the spacecraft
4. **Spacecraft Materials and Structures** — Intermediate; 3 chapters.
   - Properties that matter in a structure
   - Metals and composites in context
   - Thermal films, adhesives and vacuum compatibility
5. **Rockets, Fuels, and Space Propulsion** — Intermediate; 3 chapters.
   - Thrust, delta-v and rocket performance
   - Chemical propulsion and propellant storage
   - Electric propulsion, cold gas and solar sails
6. **Orbital Mechanics and Navigation** — Intermediate; 3 chapters.
   - Describing an orbit
   - Orbit families and observation choices
   - Navigation, maneuvers and disturbances
7. **Spacecraft Power and Thermal Systems** — Intermediate; 3 chapters.
   - Generating and distributing power
   - Battery energy through an eclipse
   - Managing heat without surrounding air
8. **Scientific Payloads and Space Sensors** — Intermediate; 3 chapters.
   - Turning a scientific question into a measurement
   - Four different meanings of resolution
   - Payload choices become spacecraft requirements
9. **Space Communication Systems** — Intermediate; 3 chapters.
   - Telemetry, tracking and commands
   - Link budgets and frequency choices
   - Contacts, storage and the delivery deadline
10. **Spacecraft Computers, Software, and Control** — Intermediate; 3 chapters.
   - Flight computing and dependable software
   - Knowing and changing spacecraft orientation
   - Redundancy, autonomy and safe operation
11. **Spacecraft Testing and Reliability** — Advanced; 3 chapters.
   - Assembly, integration and environmental tests
   - Verification, validation and reliability reasoning
   - Deployment, lifetime and responsible end of mission
12. **Real NASA Missions and Engineering Lessons** — All levels; 5 chapters.
   - MarCO: a relay is an entire mission
   - RainCube: packaging the aperture and the payload
   - CYGNSS: designing for repeated observations
   - Lunar Flashlight: useful evidence from an unmet objective
   - Landsat 9: measurements that stay comparable

38 chapters contain approximately 10,000 words of explanatory prose, plus comparison tables. Every chapter has a learning objective, explanation, engineering example, trade-offs and takeaways. Comparisons cover all eight requested material families and chemical/electric/cold-gas/sail propulsion choices. Numerical material properties are intentionally avoided: alloy, process and environment matter. The vegetation satellite is a worked educational example, not a validated flight design. Mission lessons inferred from the real NASA examples are labeled as engineering inferences.

## References and artwork

`references.json` contains 30 NASA/JPL source records, each with title, organization, date/edition or explicit date uncertainty, resource type, description and HTTPS URL. Sources were checked on 2026-11-14. Chapter metadata binds each lesson to its sources. Resources include the NASA Systems Engineering Handbook, SmallSat State-of-the-Art subsystem chapters, Basics of Space Flight, the SmallSat Institute lecture collection, and official MarCO, RainCube, CYGNSS, Lunar Flashlight and Landsat pages.

SOURCES shows references for the current chapter. Only clicking OPEN NASA RESOURCE opens a default-browser request; merely reading or navigating never opens websites. The worker keeps that request out of the render loop. Only registered HTTPS nasa.gov/subdomain URLs are accepted. Browser configuration and internet access are needed to view external resources. Offline reading requires neither. NASA pages can change after the check date; the books do not scrape them at runtime.

All 12 covers and 12 schematics are original procedural project artwork, generated by `python -m game.library.art` using the existing Pillow dependency. They are conceptual, not to scale, and labeled as such. No NASA logos, mission photographs, third-party art, datasets or document text are redistributed. Diagrams reuse visual concepts where helpful; they are not engineering drawings or spacecraft-accurate mission models. See NASA's media guidance at https://www.nasa.gov/nasa-brand-center/images-and-media/ for any future photographic additions. Missing diagram files show explanatory fallback text; missing cover art leaves a titled hardcover.

## Scope and compatibility

The old library lived in `game/presentation/hub.py`: its wall display, learning modal input branch, `open_library`, `select_card`, `open_source`, and cleanup in `close_panel`. Those are the only edited existing code regions. The console geometry, interaction target, doors, collisions, movement/camera functions, initialization, shared panel constructor, unrelated UI, design/simulation/GMAT, campaign saves and network code are unchanged.

Compatibility detail: the existing game already counted library selections as the ten original concept receipts, including an initial selection on entry. Those receipt IDs/events and existing network messages are preserved for the first ten book indices. The two extra books send no new receipt types. No additional chapter completion, quiz scores or reading-position requirements enter campaign progression. This preserves the existing briefing behavior rather than redefining mission gates. The legacy ten-card JSON remains present for those protocol IDs; it is no longer the reading interface.

## Validation

- 33 automated tests passed: 28 existing tests plus five new library-specific tests. Includes real localhost LAN tests (socket access required outside the restricted sandbox).
- New tests check 12 books, >=3 chapters each, >=200 prose words per chapter, all asset paths and source keys, URL allowlisting, explicit browser invocation with a stub, page bounds, search/comparison coverage and separate robust reading-position persistence.
- Scripted graphical library harness traversed all 12 books, 38 chapters and every spread; exercised open/close, chapter changes, rapid turns, contents, sources, answers, search, glossary, exit during a flip and forced external close during opening. Design preview remains identical. Screenshots and JSON evidence are in ignored `runtime/library-review/`.
- Existing hub harness: 11 checks passed (door, navigation, pause/resume, reading freeze, ten receipts and exit).
- Existing design harness: 14 checks passed.
- Existing campaign harness passed (cached orbit playback, result, completion and invalidation).
- Existing real-socket crew graphical harness passed (avatar, concurrent edits, shared mission/launch/report, finish acknowledgements and disconnect cleanup).
- AST comparison against HEAD confirmed all other existing Hub functions are unchanged; the diff was reviewed for library-only scope.

Reproduce with the project's Python: `python -m unittest discover -s tests -q`, `python -m game.library.verify`, and unchanged `scripts/verify_hub.py`, `scripts/verify_design.py`, `scripts/verify_campaign.py`, `scripts/verify_crew.py`.

Limitations: graphical checks are scripted on Windows, with visual inspection of captured pages; they are not user acceptance testing. Arch Linux and two separate physical laptops were not tested in this session. Browser calls were verified with a stub, not by launching a real external browser. No live GMAT run was repeated because its integration was untouched. This is an educational reference, not flight-design certification. Very narrow windows scale the complete library panel; normal landscape laptop sizes are preferable for comfortable reading.

## Complete change manifest

Paths below are relative to `Space Mission Design Game`. Only the shared Hub file is modified; all other entries are new library-specific files. Runtime evidence is ignored and is not part of this source change. The pre-existing modified design PDF at repository root was not edited by this work.

- `content/library/README.md`
- `content/library/answers.json`
- `content/library/assets/blueprint.png`
- `content/library/assets/chamber.png`
- `content/library/assets/cover-anatomy.png`
- `content/library/assets/cover-communications.png`
- `content/library/assets/cover-control.png`
- `content/library/assets/cover-fundamentals.png`
- `content/library/assets/cover-materials.png`
- `content/library/assets/cover-mission.png`
- `content/library/assets/cover-missions.png`
- `content/library/assets/cover-orbits.png`
- `content/library/assets/cover-power.png`
- `content/library/assets/cover-propulsion.png`
- `content/library/assets/cover-sensors.png`
- `content/library/assets/cover-testing.png`
- `content/library/assets/dish.png`
- `content/library/assets/electronics.png`
- `content/library/assets/fleet.png`
- `content/library/assets/layers.png`
- `content/library/assets/orbit.png`
- `content/library/assets/orbits.png`
- `content/library/assets/rocket.png`
- `content/library/assets/satellite.png`
- `content/library/assets/sensor.png`
- `content/library/assets/solar.png`
- `content/library/catalog.json`
- `content/library/glossary.json`
- `content/library/lessons.md`
- `content/library/references.json`
- `game/library/__init__.py`
- `game/library/art.py`
- `game/library/book.py`
- `game/library/content.py`
- `game/library/verify.py`
- `game/library/view.py`
- `game/presentation/hub.py`
- `tests/test_library.py`
