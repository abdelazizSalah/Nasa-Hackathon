# fundamentals
## The space environment | orbit | basics,onboard
### Learning objective
Distinguish the vacuum environment from familiar conditions at Earth's surface.
### Concept explanation
Space has no single sharply defined physical edge: atmospheric density decreases with height. Near Earth, the remaining gas is sparse but can still interact with a spacecraft. Vacuum removes the surrounding air that carries heat away from a warm object in a room. A satellite instead exchanges heat with its surroundings mainly by radiation, while heat moves within solid components by conduction. Sunlight, planetary radiation, internal electronics and the direction of exposed surfaces all matter. A surface facing the Sun and one facing deep space need not reach the same temperature.
Radiation includes energetic particles as well as electromagnetic radiation. These can affect electronics, materials and solar cells. The risks depend on orbit, shielding, exposure time and component sensitivity. There is no universal shielding thickness that makes all electronics safe.
### Why it matters
An electronics board demonstrated on a desk has not demonstrated that it can reject heat, tolerate vacuum or survive its radiation environment. A useful first design question is where every watt of waste heat will go.
### Engineering example
Imagine a camera operating inside a sealed spacecraft enclosure. A fan can circulate its internal gas, but it cannot transfer heat from the outside enclosure into vacuum by blowing on space. Engineers still need a conductive path to a suitable radiator and must check its view of the Sun and Earth.
### Trade-offs
Insulation reduces unwanted heat exchange, but covering a radiator can trap heat. Shielding adds mass and must be designed for the relevant radiation, not selected by thickness alone.
### Key takeaways
Vacuum does not automatically keep a spacecraft cold. Start with energy flows, environmental exposure and component limits.

## Gravity, inertia and falling around Earth | orbits | gravity,trajectories
### Learning objective
Explain orbit without imagining that gravity disappears above the atmosphere.
### Concept explanation
Newton's first law describes motion at constant velocity when net external force is zero. His second law relates force to acceleration: F = m a. Gravity supplies an acceleration toward Earth, continuously changing a satellite's direction. With sufficient sideways velocity and an appropriate trajectory, its falling path curves around Earth instead of immediately intersecting the surface. Orbit is sustained free fall, not a balance between gravity and an engine pushing upward.
Mass measures inertia and is expressed in kilograms. Weight is a gravitational force, expressed in newtons: W = m g for a local gravitational acceleration g. A spacecraft keeps essentially the same mass when moved to the Moon, although its weight changes. Astronauts appear weightless in orbit because they and their surroundings fall together; significant gravitational acceleration is still present.
### Why it matters
Launch must provide an appropriate velocity as well as altitude. Merely lifting a payload above most of the atmosphere does not establish a stable Earth orbit.
### Engineering example
In an ideal circular orbit, speed is sqrt(mu/r), where mu is the central body's gravitational parameter and r is distance from its center, not altitude above its surface. Raising the orbit changes both the required speed and the period. This ideal equation omits drag, Earth's uneven gravity and other disturbances.
### Trade-offs
A lower orbit can support finer imaging for a given instrument geometry, but residual atmospheric drag can shorten lifetime and increase orbit-maintenance needs. A higher orbit changes coverage and launch requirements.
### Key takeaways
Orbit depends on position and velocity together. Distinguish mass, gravitational force and the experience of free fall.

## Choosing a kind of spacecraft | satellite | classes,cubesat
### Learning objective
Connect spacecraft types to what a mission must actually do.
### Concept explanation
A satellite operates in orbit around a body. A probe may investigate an environment during a flyby or along another trajectory. A lander reaches a surface; a rover adds surface mobility. A space station supports an extended orbital presence, often including people. These labels describe functions, not a universal ranking of complexity. A modest flyby probe and a long-lived observatory can have very different requirements even though both are spacecraft.
A launch rocket provides thrust to accelerate its payload through ascent and toward the desired flight condition. The spacecraft is the system that performs the mission afterward. Some vehicles combine functions or have multiple stages, but treating launch and space operations separately helps reveal interfaces: payload dimensions, attachment points, loads, power, communications and deployment conditions.
### Why it matters
Selecting a rover before defining the scientific measurement can commit the project to landing and mobility challenges that a simpler orbiter might avoid. Conversely, an orbiter cannot directly collect a buried surface sample without additional systems.
### Engineering example
Suppose students want to measure seasonal vegetation changes across a region. Repeated orbital imaging is a plausible architecture. If the question instead concerns the chemistry of a particular rock, a lander, rover or sample-return system might become relevant. Write the measurement and access requirement before choosing the vehicle.
### Trade-offs
An ambitious architecture can increase capability while adding interfaces, deployment events, operational workload and failure opportunities. Standardized small-satellite packaging can help integration but does not remove environmental or scientific constraints.
### Key takeaways
Choose a spacecraft type to satisfy the question. Identify what launch delivers and what the spacecraft must accomplish independently.

# mission
## From a science question to requirements | blueprint | handbook,lectures
### Learning objective
Translate an interesting goal into measurable engineering work.
### Concept explanation
A goal describes a desired benefit; a requirement states a condition the system must satisfy. Requirements should identify measurable quantities, operating conditions and a verification approach. A vague request for excellent images cannot decide between instruments. A requirement for a specified ground sampling, spectral bands, coverage region and delivery deadline can guide a design. Ground sampling alone is not a complete statement of image quality: blur, signal-to-noise, calibration and pointing must also be considered.
The Concept of Operations, or ConOps, describes how users and hardware will work together over time. It includes launch, commissioning, observations, contacts, fault responses and disposal. A traceability chain connects stakeholder needs to measurements, payload functions, subsystem requirements and tests. This prevents an attractive component from becoming a requirement merely because it is available.
### Why it matters
A design can meet many component specifications and still fail the user's actual need. An emergency product delivered after the response window illustrates why the user segment belongs in the requirements discussion.
### Engineering example
For a small vegetation-monitoring satellite, begin by identifying the vegetation indicator and the scientists who will interpret it. Identify suitable red and near-infrared measurements, required calibration, target areas and revisit needs. Then derive data, pointing, storage and downlink requirements. These are educational design steps, not validated requirements for a flight project.
### Trade-offs
Tighter spatial detail or more frequent observations can raise payload, pointing, power and data demands. Make constraints visible and negotiate them before committing to hardware.
### Key takeaways
Define success, conditions and tests early. Trace every major subsystem decision back to a measurement or operational need.

## Budgets, margins and fair trade studies | solar | handbook,soa
### Learning objective
Compare complete mission alternatives rather than isolated components.
### Concept explanation
An architecture assigns functions to spacecraft, instruments, launch services, ground facilities and people. Each option needs consistent mass, volume, power, energy, data, cost and schedule budgets. Power describes a rate in watts; energy describes an amount, often in watt-hours. A peak load check and an orbit energy balance answer different questions. Similarly, installed storage capacity and daily downlink throughput are not interchangeable.
Margin accounts for uncertainty and growth relative to a defined requirement or available capacity. State its convention and denominator: a percentage of predicted usage is not the same as a percentage of capacity. Avoid consuming every remaining resource in an early concept, when estimates and interfaces are still changing. A trade study compares alternatives against shared requirements, assumptions and evaluation criteria, including risks that are difficult to reduce to one score.
### Why it matters
The lightest payload might require an expensive pointing system. An inexpensive radio may require ground access the team cannot obtain. A subsystem advantage is useful only when the integrated mission benefits.
### Engineering example
Compare two vegetation concepts using the same observing schedule. One camera produces fewer bands; another improves discrimination but increases data and processing. Include bus support, calibration, contacts and operations in both estimates. Vary uncertain assumptions to see whether a preferred option remains preferred.
### Trade-offs
More capability can reduce financial and engineering reserves. Weighting criteria differently can legitimately change the preferred design; the weights should reflect stakeholder priorities, not hide a predetermined answer.
### Key takeaways
Use consistent boundaries and units. Report assumptions, sensitivities and margins alongside the selected concept.

## Maturity, reviews and evidence | chamber | handbook,lectures,cubesat
### Learning objective
Understand how a concept becomes a credible, testable mission design.
### Concept explanation
Technology Readiness Levels, or TRLs, describe maturity from basic principles toward demonstrated operational capability. A component's maturity depends on its relevant environment and use; heritage in a different application does not prove suitability here. A Preliminary Design Review, PDR, examines whether the preliminary design can satisfy requirements with acceptable risk and a credible path forward. A Critical Design Review, CDR, examines whether the detailed design is sufficiently complete to proceed into the next development activities. Reviews are evidence-based decisions, not guarantees that nothing will fail.
Verification asks whether a product meets its specified requirements. Validation asks whether the resulting system serves the intended use and stakeholder need. Methods include analysis, inspection, demonstration and test. A risk assessment identifies possible problems, their consequences and likelihood, then assigns mitigation and ownership. Testing must be planned while the design can still be changed economically.
### Why it matters
An impressive prototype may depend on an untested deployment, a fragile supply chain or an operations assumption nobody has verified. Recording those risks helps a team choose what to demonstrate next.
### Engineering example
For the vegetation concept, trace a usable-image requirement to detector tests, calibration evidence, pointing analysis and an end-to-end ground-processing demonstration. Separately validate that the delivered product supports the scientist's vegetation question. A successful data download alone is insufficient evidence of scientific validity.
### Trade-offs
Novel technologies can enable a mission but require more development and verification effort. Extra testing costs time and resources; skipping essential evidence transfers risk into flight.
### Key takeaways
Reviews assess evidence and readiness. Keep verification, validation, technology maturity and risk management connected but distinct.

# anatomy
## The bus and its payload | satellite | classes,onboard,soa
### Learning objective
Identify what makes a scientific payload usable in orbit.
### Concept explanation
The payload performs the mission's central measurement or service. The spacecraft bus supplies supporting functions such as structure, electrical power, thermal management, communications and attitude control. The boundary is a useful engineering convention rather than a law of nature: an instrument may include its own processor or thermal hardware, and interfaces must say who provides each function.
The Electrical Power System, EPS, generates, stores, conditions and distributes electrical energy. Attitude Determination and Control, ADCS, estimates orientation and commands changes in pointing. Guidance, Navigation and Control, GNC, is a broader term covering desired motion, estimated state and control actions. Avionics includes flight computers and associated electronics. None of these systems works in isolation: the camera's exposure timing may rely on attitude knowledge, a stable clock and an available data path.
### Why it matters
Selecting a payload without its support requirements can hide most of the mission's complexity. Mass and power estimates must include harnesses, brackets, conversion losses and operational support, not merely a sensor's advertised specification.
### Engineering example
Imagine adding a spectrometer to a small satellite. It may require a clear field of view, a stable detector temperature, precise pointing, electrical power and packetized data transfer. An interface document assigns these requirements to the payload or bus and specifies acceptable ranges and timing.
### Trade-offs
A standardized bus can reduce integration effort if it fits the payload. A heavily customized bus may improve performance but increase development cost and verification work.
### Key takeaways
The payload makes the measurement; the bus makes that measurement possible, repeatable and deliverable.

## Following energy, heat and information | electronics | onboard,power,thermal
### Learning objective
Trace dependencies across a satellite using physical flows.
### Concept explanation
Start with energy: solar arrays or another source supply the power system, which feeds computers, radios, heaters, sensors and actuators. Batteries bridge intervals when generation is unavailable or insufficient. Most electrical energy eventually becomes waste heat, so thermal design must provide suitable paths to radiating surfaces. A warm instrument and a temperature-sensitive battery may need different thermal arrangements.
Follow information next. Sensors produce measurements and status, onboard electronics process and store them, and communications hardware transfers selected packets to the ground. Commands travel in the opposite direction through a controlled interface. Timing, data formats, error handling and power state are therefore shared concerns. Follow forces too: launch loads pass through structural attachments; actuator torques act through mounting interfaces; moving mechanisms can disturb an instrument's line of sight.
### Why it matters
Subsystem budgets are coupled. A heater schedule changes battery use; a downlink schedule changes radio heating; a pointing maneuver can interrupt observations. Interface failures can defeat otherwise healthy equipment.
### Engineering example
Draw a block diagram for one imaging event: command received, spacecraft points, detector stabilizes, exposure occurs, processor formats data, storage accepts it, radio later transmits it. Add the energy and heat path at every step. Missing arrows are useful questions for a design review.
### Trade-offs
Separate electronics can isolate faults but add interfaces and mass. Sharing a processor or power converter can reduce hardware while creating a common dependency that must be assessed.
### Key takeaways
Block diagrams should describe flows and responsibilities, not merely list component names. Check interfaces under normal and fault conditions.

## The ground segment completes the spacecraft | dish | ground,cubesat
### Learning objective
Explain why a mission includes more than flight hardware.
### Concept explanation
The ground segment receives telemetry, transmits commands, tracks spacecraft, plans activities and processes mission data. Telemetry reports health and measurements; tracking supports knowledge of motion; commanding requests permitted actions. Mission operators need procedures and tools for commissioning, routine work and anomalies. Scientists need calibrated products and enough metadata to interpret them. Users may require products on a different timescale than the next convenient contact.
A ground station's existence does not imply unlimited access. Visibility, scheduling, hardware compatibility, licensing arrangements, staffing and data infrastructure all influence the actual service. An end-to-end interface must preserve the meaning of a measurement from detector to delivered product, including time tags, units, calibration and quality flags. This is why a communication subsystem and a ground network should be designed together.
### Why it matters
An image left in onboard memory provides no timely service to a person on Earth. A downloaded file with missing calibration or ambiguous timing may also fail the scientific objective.
### Engineering example
For vegetation monitoring, describe who requests observations, when the satellite collects them, how long it stores them and who produces the final vegetation product. Test a simulated detector packet through the intended ground software before flight hardware is finalized. Verify both the data path and the human responsibilities.
### Trade-offs
Additional station access can reduce latency but adds cost and coordination. More onboard processing may reduce transmission demand, but it increases software complexity and requires validation of the processing itself.
### Key takeaways
Include launch, space, ground and users in the architecture. Plan operations and product delivery while designing the satellite.

# materials
## Properties that matter in a structure | layers | structures,handbook
### Learning objective
Choose material properties that match a structural function.
### Concept explanation
Density is mass per volume. Strength describes resistance to a specified failure mode; stiffness describes resistance to deformation. Specific strength relates strength to density, but it does not by itself predict whether a thin panel will buckle, a joint will slip or a telescope will lose alignment. Fatigue concerns damage under repeated loading. Thermal expansion changes dimensions with temperature, while thermal conductivity describes how readily heat moves through a material.
A spacecraft structure must survive its launch environment and maintain required geometry in operation. Load paths, joint design, local stress concentrations and manufacturing defects can matter as much as a material's nominal properties. Compare data for the relevant alloy, temper, fiber layup, processing route and temperature. A family name such as aluminum or composite is not a material specification.
### Why it matters
The lowest-density option can require thicker sections, stronger inserts or more elaborate joints. The resulting assembly may be heavier or less reliable than an apparently less attractive bulk material.
### Engineering example
Consider a camera mounting plate. Begin with alignment tolerance, launch loads, allowed deflection and temperature range. Compare complete plate-and-joint designs, not equal-volume coupons. Check the expansion mismatch with the camera housing and the thermal path to its radiator.
### Trade-offs
High stiffness can improve pointing stability while complicating fabrication or heat transfer. Corrosion, inspectability, procurement, machining and repair all belong in the decision.
### Key takeaways
Material selection is a system and manufacturing decision. Numerical properties require a traceable specification and operating conditions; this library avoids unsupported generic property values.

## Metals and composites in context | layers | structures
### Learning objective
Compare common structural families without assuming a universal winner.
### Concept explanation
Aluminum alloys are common candidates for panels, brackets and bus structures because many forms are readily machined and integrated. Titanium alloys can be attractive where strength, temperature capability or interface requirements justify harder processing and greater expense. Stainless steels can suit selected mechanisms, tanks or demanding interfaces, but their density must be included in the assembly budget. Carbon-fiber reinforced polymer composites can provide useful directional stiffness and tailored expansion, but behavior depends strongly on fiber orientation, matrix and manufacturing quality.
Composites are not simply light metals. They can be anisotropic: properties differ with direction. Fasteners and inserts must transmit loads without unacceptable local damage, and inspection must address defects appropriate to the material. Likewise, metallic structures need fatigue, corrosion and joint assessments suited to their specific environment. A fair comparison holds the required function constant, not merely the external dimensions.
### Why it matters
Choosing from a property leaderboard ignores how the part will be built, joined, verified and used. Availability of qualified processes may determine which otherwise plausible concept is credible.
### Engineering example
Compare two antenna supports that meet the same pointing tolerance. Include the bracket, joints, inserts, coatings, grounding provisions and inspection effort. Evaluate the relevant temperature cycle before declaring that a low-expansion composite will preserve alignment better in the finished assembly.
### Trade-offs
Tailored composite performance can require specialized tooling and inspection. A machined metal assembly may be simpler to qualify but need more mass for stiffness.
### Key takeaways
Compare finished structures, specify the exact material condition, and make manufacturing assumptions visible.
### Comparison
Material and use | Advantages | Limits, manufacture and trade-off
Aluminum alloys: bus panels and brackets | Many machinable forms; established joining approaches | Strength depends on alloy/temper; compare stiffness and joint mass, corrosion protection and expansion.
Titanium alloys: highly loaded interfaces and selected mechanisms | Useful strength and environmental performance in appropriate conditions | Machining and joining can be demanding; cost and mass must justify the local benefit.
Stainless steel: selected tanks, mechanisms and interfaces | Useful toughness, fabrication options and corrosion resistance for suitable grades | Relatively dense; thickness, weld quality and complete load path determine the actual mass penalty.
Carbon-fiber composites: panels, booms and optical structures | Tailorable directional stiffness and expansion | Layup, matrix, inserts, tooling and inspection affect performance; joints can erase a mass advantage.

## Thermal films, adhesives and vacuum compatibility | layers | thermal,outgassing,structures
### Learning objective
Treat nonstructural materials as engineered parts of the spacecraft.
### Concept explanation
Copper and other conductive materials can help move heat away from electronics, but a good thermal conductor may be too heavy for an entire structure. Polyimide films can serve in flexible circuits, insulation and protective applications, depending on their formulation and construction. Multilayer insulation, MLI, uses multiple low-emittance layers to reduce radiative heat exchange; it is not a load-bearing wall and does not eliminate the need for radiators or heat paths.
Adhesives and coatings can provide bonding, surface protection or tailored optical properties. In vacuum, some constituents can leave a material through outgassing and deposit on nearby sensitive surfaces. Material compatibility must consider the specific formulation, cure process, temperature and exposure. A familiar trade name is not a substitute for qualification evidence, and a database record must be interpreted under its stated test conditions.
### Why it matters
A tiny contamination deposit on an optical surface can affect a measurement even when the contaminating material has negligible mass. Small items such as tapes and coatings deserve controlled selection and handling.
### Engineering example
Plan a camera assembly with bonded joints near an optical aperture. Identify the adhesive and cure schedule, locate possible contamination paths, review applicable vacuum test evidence, and decide how to protect and verify optical cleanliness. Do not infer cleanliness from strength alone.
### Trade-offs
Conductive straps add mass but can provide a targeted heat path. Insulation saves heater energy yet may worsen overheating. Coatings change thermal balance and require durability checks.
### Key takeaways
Check the exact material, its process and its location. Vacuum, thermal and contamination compatibility are coupled design requirements.
### Comparison
Material and use | Advantages | Limits, manufacture and trade-off
Copper: thermal straps and electrical paths | Strong heat/electrical conduction in suitable forms | Density and interface contact resistance matter; use locally rather than assuming a whole copper structure is efficient.
Polyimide films: flexible circuits and insulation | Thin, flexible forms support compact packaging | Not a structural substitute; grade, coatings, adhesives, handling and environmental exposure require verification.
MLI blankets: radiative insulation | Limits unwanted radiation exchange when designed and installed correctly | Seams, compression, penetrations and installation change performance; leave intended radiator areas functional.
Adhesives/coatings: bonds and surface treatment | Can simplify joints or control surface behavior | Cure, outgassing, aging and inspection are formulation-specific; qualification effort can outweigh apparent convenience.

# propulsion
## Thrust, delta-v and rocket performance | rocket | rockets,impulse
### Learning objective
Separate force, velocity change and propellant efficiency.
### Concept explanation
A rocket expels momentum and experiences a reaction force; it does not need air to push against. Chemical propulsion converts stored energy into hot exhaust. Fuel and oxidizer have different roles: a chemical rocket may carry both, whereas a monopropellant uses a single propellant formulation with an appropriate reaction process. Thrust is force in newtons. Delta-v is a change in velocity, commonly expressed in m/s, and is an important way to budget maneuvers.
Specific impulse, Isp, expresses thrust divided by propellant weight flow using standard reference gravity. Its unit is seconds. It is a propulsion performance measure, not a burn duration or a direct statement of system energy efficiency. In an idealized rocket model, delta-v = Isp * g0 * ln(m_initial/m_final). This relation omits losses and assumes an applicable effective exhaust performance. Tanks, structure and residual propellant affect the mass ratio available to a real mission.
### Why it matters
A high-Isp device may deliver very little thrust. Launch from Earth requires sufficient thrust relative to vehicle weight and an ascent trajectory, not merely an attractive ideal mass ratio.
### Engineering example
For an educational comparison, ask two candidate systems to deliver the same orbital velocity change. Estimate propellant using a clearly stated ideal model, then add tankage, valves, electrical supply and operating time before comparing complete spacecraft mass. Do not interpret this exercise as launch-vehicle sizing.
### Trade-offs
Higher exhaust performance may reduce propellant while increasing storage or power-system complexity. High thrust can shorten a maneuver but place different demands on structure and control.
### Key takeaways
Use the right units and system boundary. Isp, thrust, thrust-to-weight ratio and mission delta-v answer different questions.

## Chemical propulsion and propellant storage | rocket | rockets,propulsion
### Learning objective
Compare chemical systems using storage and operations as well as thrust.
### Concept explanation
Liquid-propellant systems can provide controllable flow, but require suitable tanks, feed systems, valves and thermal management. Cryogenic propellants require low-temperature storage and can impose insulation, conditioning and boil-off concerns. Solid motors package propellant in a different way, with burn behavior strongly tied to formulation and grain design; their control and shutdown possibilities differ from those of many liquid engines. These are broad families rather than interchangeable catalog items.
Launch propulsion must operate through ascent, while in-space systems may prioritize long storage, repeated small maneuvers or precise attitude control. Hydrazine monopropellant has flight heritage but serious handling toxicity concerns. Alternatives called green monopropellants can reduce some handling hazards, but that label does not mean harmless, universally compatible or automatically higher performing. Materials, catalyst, temperature and operating conditions still need verification.
### Why it matters
A propellant's performance at an engine test stand is not the performance of a stored, integrated propulsion system after a long cruise. Thermal conditions and feed reliability can decide whether thrust is available when required.
### Engineering example
A small-satellite team should specify the duration between fueling and use, permitted ground handling, maneuver sequence and total impulse before comparing thrusters. Include qualification of seals, cleanliness, storage temperatures and interfaces. Operational restrictions can eliminate an otherwise plausible chemistry.
### Trade-offs
Storable systems may simplify a long wait before firing, while other combinations offer different exhaust performance or launch benefits. More valves and restart capability add functionality and verification work.
### Key takeaways
Choose a complete propulsion architecture for its environment and operations. No propellant family is best for every mission.
### Comparison
System | Performance character | Storage, integration and mission fit
Liquid hydrogen / liquid oxygen | High chemical exhaust performance; substantial thrust in suitable engines | Cryogenic handling and low hydrogen density affect tank volume and insulation; relevant to selected launch stages.
RP-1 / liquid oxygen | Chemical launch thrust with relatively dense fuel | Oxygen remains cryogenic; engine cycle, deposits and reuse requirements affect the design.
Methane / liquid oxygen | Chemical thrust; performance depends on engine conditions | Both require cold storage; tankage, conditioning and mission duration must be assessed.
Solid rocket propellants | High thrust with a packaged motor architecture | Grain/manufacturing integrity and limited control options matter; not a universal substitute for restartable liquid systems.
Hydrazine monopropellant | Useful controllable in-space thrust with established heritage | Toxic handling and material/catalyst requirements add operational burden; trained facilities are required.
Green monopropellants | Alternative in-space chemistries with formulation-specific performance | Potential handling benefits are not absence of hazards; thermal, catalyst and compatibility evidence remains essential.

## Electric propulsion, cold gas and solar sails | rocket | propulsion,impulse
### Learning objective
Match maneuver duration and available power to a propulsion technology.
### Concept explanation
Electric propulsion uses electrical energy to accelerate propellant. Ion thrusters and Hall-effect thrusters use different physical arrangements to produce and accelerate charged particles. They can achieve high exhaust velocity while producing low thrust compared with many chemical systems. The spacecraft must supply electrical power, handle waste heat and plan the long-duration trajectory. Xenon and krypton are examples of propellants used in electric propulsion; their suitability depends on the thruster, supply and mission, not on their names alone.
Cold-gas thrusters release stored gas through nozzles without a combustion process. Their architecture can be attractive for simple control tasks, but storage pressure, gas mass and limited exhaust performance constrain capability. A solar sail exchanges momentum with sunlight rather than expelling onboard propellant. It requires a large, controllable optical surface and suitable illumination; its acceleration and navigation demands differ from those of a rocket.
### Why it matters
A low-thrust system may be excellent for gradual orbit changes and unsuitable for an urgent maneuver. High specific impulse does not overcome an inadequate launch thrust-to-weight ratio.
### Engineering example
Compare a slow orbit-raising mission with a lander's brief, high-acceleration descent. The former might accept long thrust arcs and a large electrical supply. The latter must meet an immediate force requirement. Include time constraints before using propellant mass as the deciding metric.
### Trade-offs
Solar arrays that support electric propulsion add mass, area and deployment risk. Eliminating expelled propellant with a sail shifts complexity into structures, attitude control and trajectory design.
### Key takeaways
High exhaust performance is valuable only when the mission can support the required thrust duration, power and control.
### Comparison
Technology | Principal benefit | Limiting system considerations
Ion / Hall with xenon or krypton | High exhaust velocity can reduce required propellant | Low thrust, power processors, electrical generation, thermal paths and plume interactions; suited to compatible long-duration maneuvers.
Cold gas | Relatively simple momentum-control concept | Pressure vessels and modest exhaust performance limit total maneuver capability; propellant choice and storage remain engineered decisions.
Solar sail | No expelled onboard propellant for sail force | Large deployable area, illumination, low acceleration and orientation control; unsuitable as a conventional Earth-launch engine.

# orbits
## Describing an orbit | orbits | gravity,trajectories,planetary
### Learning objective
Read the basic geometric and timing properties of an orbit.
### Concept explanation
In the ideal two-body problem, a bound orbit is an ellipse with the central body at one focus. Eccentricity describes its shape; a circle is the zero-eccentricity case. A satellite in an elliptical orbit moves faster near its closest approach and slower near its farthest point, sweeping equal areas in equal times. The orbital period depends on the semimajor axis for a specified central body, rather than being an independent setting. These relationships are summarized by Kepler's laws.
Altitude is height above a stated reference surface. Orbital equations often use radius from the body's center instead. Inclination is the angle between the orbital plane and a reference plane, such as Earth's equator. A near-polar inclination supports access to high latitudes, but coverage also depends on Earth rotation, sensor field of view and when observations are possible. A ground track is the path of the spacecraft's subsatellite point over the rotating surface.
### Why it matters
Two satellites at the same altitude can have very different target access if their planes differ. A period, altitude and central body chosen independently may describe an inconsistent ideal orbit.
### Engineering example
For a teaching sketch, draw a circular Earth orbit and mark its plane relative to the equator. Add Earth's rotation during one revolution, then sketch the shifted ground track. Ask whether the desired latitude lies within reach before optimizing image quality.
### Trade-offs
Greater geographic access can change contact timing, lighting and launch options. An orbit selected for one target's schedule may be poor for another.
### Key takeaways
Always state the reference frame and distinguish altitude, radius, inclination, eccentricity and period. Ideal laws are a foundation, not a complete flight prediction.

## Orbit families and observation choices | orbits | basics,planetary,navigation
### Learning objective
Compare orbit families against a mission's coverage and timing requirements.
### Concept explanation
Low Earth Orbit, LEO, and Medium Earth Orbit, MEO, describe broad altitude regions with different uses and operating environments. A geosynchronous orbit has a period matching Earth's rotation; a geostationary orbit additionally requires the circular, equatorial, prograde geometry that keeps its apparent position fixed above the equator. Not every synchronous orbit is stationary in the sky. A polar orbit is oriented near the poles. A Sun-synchronous orbit uses an appropriate precession rate to maintain a roughly consistent relationship between its orbital plane and the Sun.
The field of view projected onto the surface, target illumination, viewing angles and pointing capability determine useful coverage. Revisit is not simply orbital period: a spacecraft may circle Earth many times without seeing a particular target in acceptable conditions. Clouds or observation constraints can further reduce usable opportunities. A constellation can change sampling opportunities, but introduces multiple spacecraft and additional operations.
### Why it matters
An orbit label is not a scientific performance guarantee. A sensor's resolution and a region's observation frequency must be evaluated in the actual geometry and operating plan.
### Engineering example
For vegetation monitoring, compare consistent local illumination with frequent regional access. Identify whether an observation at a different Sun angle remains scientifically comparable. Evaluate the sensor's footprint and the required revisit before choosing a named orbit family.
### Trade-offs
Higher altitude generally changes footprint and ground sampling for a fixed angular detector geometry, while increasing path length to a station. The effect on delivered science depends on the entire system.
### Key takeaways
Choose an orbit for the required observations, not for a familiar name. Explain what access and illumination assumptions support the choice.
### Comparison
Family | Useful characteristic | Question to check
LEO | Closer surface observation geometry | Are drag, eclipse, target access and contact opportunities acceptable?
MEO | Different coverage and period regimes | Do radiation, link distance and launch demands fit this mission?
Geostationary | Persistent view of a region from an equatorial location | Does viewing geometry provide the needed measurements and spatial detail?
Polar / Sun-synchronous | High-latitude access or controlled lighting relationship | What revisit and seasonal constraints remain after choosing the plane?

## Navigation, maneuvers and disturbances | dish | navigation,trajectories
### Learning objective
Connect predicted motion to observations, contacts and orbit maintenance.
### Concept explanation
Navigation estimates spacecraft position and velocity from measurements and models. Orbit propagation predicts how a state evolves, while orbit determination uses observations to estimate that state. They are related but different activities. A maneuver changes velocity and therefore the future trajectory; where and when it occurs can be as important as its magnitude. Maneuver execution and navigation uncertainties require attention, especially near demanding events.
Real orbits depart from the simple two-body ideal. Earth's nonspherical gravity, residual atmospheric drag, other bodies and solar radiation pressure can perturb motion. Drag depends on atmospheric conditions and spacecraft properties and can affect LEO lifetime. Eclipses depend on the relative geometry of spacecraft, Earth and Sun, so a fixed eclipse duration is only a teaching approximation. A station sees the spacecraft only when line of sight, elevation and other link conditions permit communication.
### Why it matters
Geometry drives schedules. A new orbit can change imaging opportunities, radio contact, battery discharge and eventual disposal requirements at the same time.
### Engineering example
Create a timeline containing target access, sunlight, eclipse and station visibility. Place imaging, maneuvers and downlinks on that same timeline. If two tasks compete for pointing, revise the schedule rather than assuming both can happen independently. Then examine how timing uncertainty affects the plan.
### Trade-offs
Orbit maintenance consumes propulsion resources and operations effort. Avoiding a difficult contact schedule through a different orbit can create a new power or launch constraint.
### Key takeaways
A trajectory is an input to integrated operations. Mission Forge's simplified timelines and this library's diagrams illustrate concepts; they are not navigation products for flight.

# power
## Generating and distributing power | solar | power,onboard
### Learning objective
Build a power budget with operating modes and clearly defined boundaries.
### Concept explanation
Solar cells convert incident light into electrical power. An array's output depends on illumination, orientation, temperature, cell characteristics, degradation and electrical configuration. Nameplate output is not guaranteed power at every point in an orbit. The Electrical Power System conditions generation, manages charging and distributes energy at suitable electrical interfaces. Harness losses, converters and protection devices belong inside the system budget.
Separate operating modes such as imaging, downlink, standby and safe mode. Average demand is useful for energy planning, while peak demand determines whether sources, storage, converters and wiring can support a particular combination of loads. Batteries can support transient demand, but their allowable current, state of charge and temperature impose limits. A design rule that requires solar generation to exceed every simultaneous load is conservative, not a universal physical law.
### Why it matters
Two payloads with the same average electrical demand can have very different peak loads and operating schedules. A single total in watts cannot describe the full power-system problem.
### Engineering example
Make a mode table for an imager, processor, heater and radio. Identify which operate together and where sunlight is available. Include conversion losses explicitly in a realistic design; if an educational example neglects them, say so. Allocate a documented margin rather than silently assuming ideal performance.
### Trade-offs
Larger arrays can improve generation but add mass, stowed volume, deployment mechanisms and attitude constraints. Scheduling loads separately can reduce peak demand while consuming observation or contact time.
### Key takeaways
State what the budget includes. Compare generation and demand by mode, then check both instantaneous capability and time-integrated energy.

## Battery energy through an eclipse | solar | power
### Learning objective
Use correct units to estimate eclipse energy while recognizing battery limits.
### Concept explanation
Power in watts is a rate of energy transfer. Energy in watt-hours is power multiplied by elapsed hours when power is constant. A battery's rated capacity is not necessarily all usable under mission conditions. Allowed depth of discharge, temperature, efficiency, aging, current limits and required reserve must be considered. Battery technologies differ in cell characteristics and integration needs; selecting a chemistry also commits the design to charging, balancing, protection and verification requirements.
During eclipse, a solar-powered spacecraft normally uses stored energy for essential loads and any permitted activities. The budget should include heaters, computers and attitude-control equipment as well as the payload. Charging during sunlight must replace the energy withdrawn and accommodate losses without exceeding component limits. Repeating an energy deficit every orbit will eventually exhaust a battery even if the first orbit appears satisfactory.
### Why it matters
A large solar array does not directly supply an eclipsed spacecraft. Conversely, a larger battery cannot indefinitely compensate for insufficient average generation.
### Engineering example
For a deliberately idealized exercise, a constant 20 W load operating for 30 minutes needs 20 W * 0.5 h = 10 Wh. This is consumed energy, not a flight battery specification. A real design must add documented reserve and account for usable capacity, efficiency, thermal conditions, aging and charging opportunities.
### Trade-offs
More capacity generally adds mass and volume. Reducing eclipse activity can save storage energy but postpone science or communications. Neither choice should be evaluated without the mission schedule.
### Key takeaways
Integrate watts over time. Check charge recovery across repeated cycles and distinguish rated capacity from acceptable operational use.
### Comparison
Decision | Potential benefit | Coupled cost
Larger array | More generation in compatible lighting | Mass, deployment and pointing constraints
Larger battery | More stored energy for dark intervals | Mass, volume, charging and thermal management
Reschedule a load | Lower simultaneous demand or eclipse discharge | Lost observation/contact opportunities and more planning

## Managing heat without surrounding air | chamber | thermal,structures
### Learning objective
Identify the heat-transfer paths that keep spacecraft equipment within limits.
### Concept explanation
Thermal design balances absorbed environmental energy, internally generated heat, storage within materials and heat rejection. In vacuum, external convection is negligible for ordinary spacecraft thermal analysis. Conduction moves heat through solids and interfaces; radiation exchanges energy with viewed surroundings. The radiated power of an idealized surface depends strongly on absolute temperature, emissivity and area. Real geometry also requires appropriate view factors and environmental illumination.
Passive approaches include surface finishes, insulation, conductive straps, radiators and heat pipes. A heat pipe moves heat through a designed working-fluid cycle rather than acting as a simple solid rod. Multilayer insulation limits radiative exchange where installed appropriately. Active heaters add controlled electrical energy to avoid equipment becoming too cold. Thermal control therefore interacts directly with electrical power and layout.
### Why it matters
Every electronic load creates a thermal responsibility. A camera's calibration and a battery's usable performance can depend on temperature, while structural temperature changes can shift alignment.
### Engineering example
Sketch a path from a processor through its mounting interface to a radiator. Mark interface contact resistance, conductive material and the radiator's external view. Then examine cold and hot operational cases: a solution that prevents freezing in standby may overheat during a long transmission.
### Trade-offs
A larger radiator improves some heat-rejection cases but adds area and constrains placement. Insulation can save heater energy while trapping unwanted internal heat. Active control adds flexibility but consumes power and requires reliable sensors and software.
### Key takeaways
Thermal design is an energy balance with geometry and interfaces. Treat power, placement and temperature requirements together.

# sensors
## Turning a scientific question into a measurement | sensor | instruments,electromagnetics
### Learning objective
Choose an instrument family from the required physical measurement.
### Concept explanation
Remote sensing obtains information without direct contact with the measured target. Passive instruments observe naturally available radiation, such as reflected sunlight or thermal emission. Active instruments transmit energy and observe the response. Optical cameras form images, spectrometers separate signals by wavelength, and thermal imagers measure radiation in thermal bands. Radar transmits radio-frequency energy and analyzes returns. Radiometers measure radiation; atmospheric instruments and particle detectors address other physical quantities and environments.
These categories overlap rather than forming a simple quality ladder. A spectrometer may be an imaging instrument, and a radiometer may operate in several spectral regions. An instrument is selected for the physical question, available signal, observing geometry and required uncertainty. Calibration connects instrument response to meaningful quantities, while processing assumptions determine what scientific inference can be supported.
### Why it matters
A sharper photograph cannot substitute for a missing spectral band or a direct particle measurement. Payload selection begins with what must be learned, not with which device sounds most advanced.
### Engineering example
To examine vegetation, compare reflected-light measurements in suitable bands with a thermal measurement of surface conditions. Explain which scientific quantity each observes and what further modeling is required. Neither automatically measures every property of a plant or removes effects of atmosphere, illumination and viewing geometry.
### Trade-offs
An active transmitter can enable measurements unavailable to a passive receiver but introduces power, thermal and antenna demands. Additional bands can improve discrimination while increasing data and calibration complexity.
### Key takeaways
Match the measurement physics to the objective. Keep measured signals, processed products and scientific interpretation distinct.

## Four different meanings of resolution | sensor | instruments,electromagnetics
### Learning objective
Distinguish spatial, spectral, temporal and radiometric measurement capabilities.
### Concept explanation
Spatial resolution describes the ability to distinguish features in space; a pixel's ground sampling is related but does not by itself include optical blur, motion smear or signal quality. Spectral resolution concerns separation of wavelengths. Temporal resolution concerns how often useful observations are available. Radiometric resolution concerns the ability to distinguish signal levels; digitization bit depth is one factor, not a complete statement of measurement accuracy.
An instrument must also point and remain sufficiently stable during an observation. Changing field of view, altitude or integration time affects more than a single performance number. A narrow view can provide finer angular sampling but less coverage per exposure. Longer integration may improve signal collection in a particular case while increasing sensitivity to movement or saturation. Calibration and uncertainty remain necessary even when the detector has many pixels and bits.
### Why it matters
The word resolution can conceal several unrelated requirements. A trade study should compare the dimension that serves the science question rather than assuming all forms improve together.
### Engineering example
For vegetation maps, define the smallest relevant field, the spectral distinction needed, the acceptable interval between usable images and the uncertainty of the derived indicator. Now compare two sensors. One might image smaller patches but miss changes between visits; another could revisit more often with coarser detail.
### Trade-offs
Higher spatial sampling can increase data volume for the same mapped area. More spectral channels or more samples per signal can further increase storage and transmission demand. Pointing and processing requirements can grow too.
### Key takeaways
Specify each type of resolution separately, with uncertainty and observing conditions. More samples do not automatically create more useful knowledge.

## Payload choices become spacecraft requirements | satellite | instruments,onboard,power,communications
### Learning objective
Follow a sensor upgrade through the complete support system.
### Concept explanation
An instrument's resource footprint includes electrical operation, thermal stabilization, structure, pointing, processing, storage and downlink. A data sheet's sensor mass may omit brackets, electronics or associated hardware. The observing schedule determines duty cycle, while the format, compression method and retained metadata determine actual data volume. Compression can reduce transmission demand, but its effect on scientific information must be evaluated rather than assumed harmless.
Supporting subsystems create feedback. More data can need a faster radio that consumes additional power. Larger power hardware can change mass and deployment requirements. Better pointing may require different sensors or actuators. These changes can affect launch compatibility, cost and operational complexity. A correct design accounts for these consequences before declaring that an upgraded payload fits the bus.
### Why it matters
Mission capability is limited by the chain from measurement to delivered product. An observation that cannot be stored, accurately interpreted or transmitted in time may not satisfy the objective.
### Engineering example
In a simplified design exercise, double the image dimensions in both axes while keeping band count and bits per sample unchanged. The uncompressed sample count becomes four times larger. This is a mathematical example, not a specification for a NASA instrument. Revisit processing time, storage, ground contacts and energy before choosing the new camera.
### Trade-offs
Reducing observed area, cadence or stored detail can preserve system margins but alter science return. Better downlink may help only if access and power are available.
### Key takeaways
Specify payload interfaces and operating modes. Select the design that delivers the required science, not simply the most ambitious sensor.
### Comparison
Instrument choice | Science opportunity | Supporting constraints
Optical camera | Spatial patterns and reflected-light imaging | Illumination, pointing, blur, detector temperature and data volume
Spectrometer | Wavelength-dependent material or atmospheric signatures | Calibration, spectral signal, thermal stability and channel count
Thermal imager | Thermal-radiation observations | Temperature calibration, emissivity assumptions and detector/optics stability
Radar | Active radio observations and target structure in suitable conditions | Transmit power, antenna geometry, processing, mass and operational timing
Particle detector | Local charged-particle environment | Field of view, contamination, calibration and relevant radiation environment

# communications
## Telemetry, tracking and commands | dish | communications,ground
### Learning objective
Identify the different information flows in a mission communication system.
### Concept explanation
Telemetry carries spacecraft health and measurement information toward operators or users. Commands request authorized actions, while tracking observations support knowledge of spacecraft motion. Uplink is communication toward the spacecraft; downlink is communication away from it toward a receiving system. These functions may share hardware but have different availability and reliability needs. A low-rate health message can be more urgent than a large scientific file.
An antenna directs or receives electromagnetic energy. Broad-coverage antennas can ease pointing requirements; higher-gain configurations concentrate performance into a more restricted angular region. A suitable ground station needs compatible hardware, timing and operational access. An onboard transmitter alone is not a complete communication service. Operators also need a defined command process, data formats and recovery arrangements.
### Why it matters
A vehicle that cannot receive commands or provide health information may be difficult to recover even when its payload is healthy. A science link's performance must be assessed alongside the mission's operational needs.
### Engineering example
Design separate data products for a small imager: a compact health packet, an attitude/time record and the observation file. Decide which has priority during a short contact and how the ground software identifies missing or incomplete data. Preserve enough metadata for the scientist to interpret the image later.
### Trade-offs
A narrow-beam antenna can support a stronger link but complicate attitude control and acquisition. A simpler low-rate path may provide valuable resilience even if a separate high-rate service handles science.
### Key takeaways
Communication includes a spacecraft, a propagation path, a ground segment and procedures. Define what must arrive, in which direction, and when.

## Link budgets and frequency choices | dish | communications,electromagnetics
### Learning objective
Explain a link budget as a complete accounting of signal and noise.
### Concept explanation
A link budget estimates whether sufficient received signal quality is available for a chosen service. It accounts for transmitter power, antenna gains, propagation losses, hardware losses, receiver performance and relevant noise. The required quality depends on the modulation, coding, data rate and acceptable errors. Increasing the advertised data rate without changing anything else can reduce the margin available per bit.
S-band, X-band and Ka-band are named radio-frequency regions used in space communication. A higher frequency is not inherently better for every mission. Antenna dimensions, pointing tolerance, hardware efficiency, spectrum authorization, atmospheric effects and ground infrastructure all influence the design. Optical communication offers different bandwidth and beam characteristics but introduces demanding acquisition/pointing and weather considerations for many ground links. Frequency names alone are not a link analysis.
### Why it matters
A radio that performs well in a laboratory may not close a distant operational link. Hardware performance must be evaluated at the mission's geometry, rates and environmental conditions.
### Engineering example
Compare a broad low-rate health link with a narrow high-rate science link for the same satellite. Write the assumed station, distance, pointing and availability before comparing them. If better gain demands a pointing mode that prevents simultaneous imaging, include that lost observing time in the trade.
### Trade-offs
More electrical power can improve some links but raises thermal and generation demands. Higher gain may add deployment and pointing complexity. Better coding can improve robustness while changing data throughput or processing needs.
### Key takeaways
Evaluate complete links with explicit assumptions. Data rate, gain, transmit power and margin must be considered together.

## Contacts, storage and the delivery deadline | dish | ground,communications
### Learning objective
Determine whether collected data can reach the user on time.
### Concept explanation
A contact window is an interval when geometry, station availability and equipment conditions permit communication. Its usable duration can be shorter than geometric visibility because acquisition, setup and scheduling consume time. Multiply net delivered data rate by usable time to estimate throughput; do not confuse bits with bytes or raw symbol rate with usable science delivery. Protocol overhead, retransmission and coding can change the result.
Storage absorbs differences between collection and transmission schedules. It does not create unlimited communications capacity. If each day's observations exceed what can be sent, the backlog grows until capacity is exhausted or data must be discarded. Even a system that eventually clears its backlog can miss a user's delivery deadline. Operations therefore needs both a capacity budget and a latency assessment.
### Why it matters
Scientific success depends on delivered, interpretable observations. A perfectly functioning detector cannot compensate for an absent ground contact or a full memory device.
### Engineering example
An idealized 2 MB/s net data service operating for 60 usable seconds transfers 120 MB. Label this as an arithmetic teaching example: it assumes the rate is genuinely usable and neglects outages. Compare that amount with the observations already stored and those expected before the next contact. Then check whether priority products meet their deadlines.
### Trade-offs
More stations can reduce latency but increase service costs and coordination. More onboard processing may reduce file size while adding power use, software and validation work.
### Key takeaways
Budget collection, storage and actual delivery on one timeline. Include both throughput and time-to-user in the definition of mission success.
### Comparison
Approach | Advantage | Compromise
Low-rate broad link | Easier acquisition and useful health coverage | Long transmission time and limited science throughput
High-rate narrow link | More science during an available contact | Pointing, power, station compatibility and thermal demands
Additional ground access | More delivery opportunities | Scheduling, service cost, infrastructure and operational workload
Onboard reduction | Fewer bytes to transmit | Algorithms, processing power and protection of scientific information

# control
## Flight computing and dependable software | electronics | avionics,onboard
### Learning objective
Describe why onboard computing is different from running a desktop application.
### Concept explanation
A flight computer coordinates activities, handles data and participates in maintaining spacecraft safety. Embedded software interacts with sensors, actuators, communications and power states through specified interfaces. Memory stores executable code, temporary data and observations; each kind has requirements for capacity, integrity and recovery. Timing and resource limits matter because physical events continue while software runs.
Radiation can cause different electronics effects, including transient upsets and cumulative degradation. Appropriate component selection, error detection/correction, testing and recovery strategies depend on the environment and equipment. A watchdog can help detect an unresponsive system and initiate a defined recovery, but an uncontrolled restart is not automatically safe. Fault detection, isolation and recovery should identify what happened and preserve essential functions through a suitable response.
### Why it matters
The fastest processor is not always the most useful flight computer. Electrical demand, radiation tolerance, interfaces, software support and verifiable behavior can dominate the selection.
### Engineering example
Trace an interrupted observation file after an unexpected reset. Which data remain trustworthy? How is the partial record identified? Can the spacecraft restart without energizing a heater or transmitter at an unsafe time? An operational recovery scenario is a concrete way to test software and data handling together.
### Trade-offs
More computing can enable compression or autonomy but adds electrical, thermal and verification responsibilities. Additional memory creates opportunities for science while requiring integrity checks and a clear overwrite policy.
### Key takeaways
Design software for normal work and recoverable faults. Specify timing, state transitions and data integrity as engineering requirements.

## Knowing and changing spacecraft orientation | satellite | gnc,navigation
### Learning objective
Distinguish attitude sensing, estimation and actuation.
### Concept explanation
Attitude is orientation, not the same thing as orbital position. Star trackers observe stellar patterns to estimate orientation; Sun sensors measure the Sun's direction within their capabilities. Other measurements can include angular-rate sensors and magnetic-field sensors. Attitude estimation combines available information with models and accounts for sensor limitations. A sensor's measurement is not an actuator command by itself.
Reaction wheels change spacecraft angular momentum distribution by changing wheel speed. External disturbances can build wheel momentum toward operating limits, requiring an appropriate momentum-management strategy. Magnetorquers generate torques through interaction with a magnetic field; their effectiveness depends on that environment and geometry. Thrusters can provide attitude-control torque with different resource and disturbance consequences. Control software uses estimates and objectives to command suitable actuators.
### Why it matters
Pointing enables sunlight collection, antenna alignment, thermal orientation and stable observations. Competing pointing needs must be scheduled or accommodated in the architecture.
### Engineering example
An imager wants its line of sight toward a ground target while a directional antenna wants Earth or a station within a specified beam. Sketch the required orientations and identify whether the mechanisms or operating sequence can satisfy both. Include a recovery orientation that supports power and communications if precision pointing is lost.
### Trade-offs
More precise sensing may improve science but add mass, power and processing. Wheels avoid continuous propellant expenditure for many tasks but introduce mechanical, momentum and disturbance considerations.
### Key takeaways
Sensors tell the spacecraft about orientation; actuators change it. Evaluate the full estimation-and-control loop, not a single device.

## Redundancy, autonomy and safe operation | electronics | avionics,gnc,handbook
### Learning objective
Evaluate resilience as a system behavior rather than a count of spare parts.
### Concept explanation
Redundancy provides alternate ways to perform a function, but only if failures can be detected and the alternate path remains available. Two computers connected to one vulnerable power source can share a common-cause failure. Cross-strapping, switching logic, interfaces and recovery procedures can create new complexity. Fault tolerance requires reasoning about the whole failure path, not merely duplicating boxes.
Autonomy allows onboard decisions when ground contact is unavailable or too slow. The permitted decision space, triggers and priorities must be explicit. A safe mode typically protects essential functions and preserves a recoverable condition, but its details are mission-specific. Software must coordinate power, thermal, pointing, communications and stored data when entering or leaving that condition. Recovery should avoid oscillating between states or repeatedly triggering the original fault.
### Why it matters
An incorrectly designed response can cause more damage than the initiating upset. More complex protection is not always easier to verify or operate.
### Engineering example
Imagine a loss of attitude knowledge during downlink. Write a response that stops unsuitable activities, establishes a power-supporting orientation within available sensing capability, preserves diagnostic records and attempts a defined health link. Identify what operators need to know before returning to science. This is an educational exercise, not a flight procedure.
### Trade-offs
Extra hardware, diagnostics and alternate modes cost mass, energy, software effort and testing time. A simpler design may be acceptable for a risk-tolerant demonstration but unsuitable for another mission's consequence level.
### Key takeaways
Specify which failures must be tolerated, how they are detected and how service is restored. Match resilience effort to mission needs.
### Comparison
Choice | Benefit | Additional burden
Redundant electronics | Alternate path after specified failures | Power, interfaces, switching logic and common-cause analysis
Autonomous response | Acts between contacts or under latency | Trigger validation, state-machine complexity and recovery testing
Radiation protection | Can reduce relevant environmental exposure | Mass, geometry and environment-specific verification; not immunity

# testing
## Assembly, integration and environmental tests | chamber | testing,cubesat
### Learning objective
Explain why a functioning laboratory assembly still needs mission-specific verification.
### Concept explanation
Assembly, Integration and Test, AIT, brings components into a working spacecraft while controlling interfaces and collecting verification evidence. Integration should expose electrical, mechanical, thermal and data mismatches in a planned sequence. A test performed after inaccessible hardware is installed can become much harder to diagnose or repeat. Configuration records matter: evidence applies to a defined build, procedure and environment, not every later modification.
Launch introduces vibration, acoustics and other loads that differ from quiet operation on a desk. Vibration and acoustic tests address relevant environmental requirements, while thermal-vacuum tests exercise conditions involving temperature and vacuum. Electromagnetic compatibility examines whether equipment interferes with itself or other systems. Deployment tests investigate release mechanisms, clearances, functional operation and repeatability under the appropriate conditions or justified simulations.
### Why it matters
Connectors can loosen, structures can resonate, contamination can affect optics, and thermal paths can differ from expectation. Many failures involve interfaces rather than an obviously broken primary component.
### Engineering example
Plan the verification of a solar-array deployment before closing the spacecraft. Identify required clearances, electrical continuity, release indications and the limitations of a ground test under gravity. Document how the evidence supports the actual flight requirement rather than claiming that a successful bench movement reproduces orbit.
### Trade-offs
Testing costs schedule and hardware life, and overly severe tests can create damage. Test levels and configurations need justified requirements and approved procedures; random stress is not qualification.
### Key takeaways
Test the defined product against the defined environment. Preserve configuration, results and discrepancies through integration.

## Verification, validation and reliability reasoning | chamber | handbook,lectures
### Learning objective
Use evidence and risk analysis to judge whether a mission is ready.
### Concept explanation
Verification establishes that specified requirements have been met through appropriate analysis, inspection, demonstration or test. Validation establishes that the system will serve its intended use. Neither is satisfied by one attractive screenshot or one successful component test. A verification matrix links requirements to methods, configurations, evidence and unresolved issues. Design reviews examine the consistency and maturity of that evidence alongside resources, schedule and risk.
Reliability reasoning considers how functions can fail, the consequences and the architecture's ability to tolerate or recover from those failures. Redundancy can help, but shared power, software defects or environmental events can defeat apparently independent channels. Risk assessments identify mitigations and residual risk rather than promising certainty. Mission readiness includes hardware, software, ground systems, people and procedures.
### Why it matters
An instrument can pass every electrical test and still produce a product that does not answer the scientist's question. Likewise, a validated concept can be implemented with unverified hardware.
### Engineering example
For a vegetation product, verify detector calibration, pointing performance, timing and data transport. Separately validate that the delivered product supports the intended analysis under stated environmental conditions. Record exclusions such as cloud contamination. Trace a discovered discrepancy to its affected requirements before deciding whether to repair, retest or accept a limitation.
### Trade-offs
Schedule pressure can favor accepting unresolved risks, but those choices should be explicit and reviewed by the appropriate project authority. Adding backup features can also create new verification obligations.
### Key takeaways
Readiness is a supported decision, not a guarantee. Keep the distinction between requirements compliance and mission usefulness visible.

## Deployment, lifetime and responsible end of mission | orbits | testing,cubesat,handbook
### Learning objective
Include the end of a mission in its original engineering plan.
### Concept explanation
A mission lifetime requirement influences component selection, environmental exposure, power degradation assumptions and operational resources. It is not established merely by simulating a short orbit or choosing a battery capacity. Consumables, mechanism reliability, radiation effects, storage needs and ground support can all influence useful service life. End-of-mission planning must also address the spacecraft's future behavior after scientific operations stop.
Orbital debris mitigation can involve disposal planning, avoiding unnecessary released objects, reducing stored-energy hazards and limiting collision risks. Applicable requirements depend on mission, jurisdiction and authorization; this educational library does not prescribe a universal regulatory timetable. A deployment event must be coordinated with mechanical interfaces, safety constraints, attitude and communications. Equipment that worked before launch may fail to deploy or encounter a condition the earlier demonstration did not cover.
### Why it matters
Disposal and deployment are architectural requirements, not last-minute additions. Waiting until resources are exhausted can remove options that would have been available with a planned reserve.
### Engineering example
Write a ConOps that ends after science: final data return, spacecraft status assessment, disposal actions where applicable and a defined final configuration. Identify which systems must still function and which resources must remain. Then trace those needs back into the initial design budgets and verification plan.
### Trade-offs
Reserving resources for responsible disposal can reduce science capacity. Extra mechanisms or propulsion may enable another strategy but add cost, mass and risk.
### Key takeaways
Plan launch, deployment, routine work, anomalies and retirement as one life cycle. Never equate a simplified game lifetime value with demonstrated flight reliability.

# missions
## MarCO: a relay is an entire mission | fleet | marco
### Learning objective
Learn how a focused technology demonstration connects spacecraft and ground operations.
### Concept explanation
Mars Cube One, MarCO, used two independently flying CubeSats to demonstrate interplanetary communications-relay capabilities. NASA JPL records that the pair provided a real-time link for InSight's entry, descent and landing on 26 November 2018. The spacecraft carried their own communications and navigation experiments; they were not attached relay boxes riding on InSight at Mars. This distinction matters because each small vehicle needed a complete supporting spacecraft and its own flight operations.
The engineering lesson is broader than miniaturizing a radio. An event-driven relay requires suitable geometry, navigation knowledge, pointing, electrical supply, timing and compatibility with both the source and destination of information. A successful path includes the transmitted event data and the ground team's ability to receive and interpret them. The mission page supports the historical outcome; the design reasoning here is an educational interpretation, not an unpublished specification for MarCO.
### Why it matters
A short critical event can impose demanding requirements even on a spacecraft with a narrow purpose. Complexity does not scale directly with physical size.
### Engineering example
Sketch the path from a descending lander to a relay and then Earth. Identify which requirements change if the relay arrives too late, points incorrectly or lacks electrical energy during the event. Classify each as an instrument, bus, trajectory or ground-interface issue.
### Trade-offs
A relay can provide timely information but adds an independent spacecraft and operations problem. A technology demonstration can accept a different risk posture than a service on which another mission critically depends.
### Key takeaways
Small spacecraft still need integrated systems engineering. Evaluate an information service from event source to final user.

## RainCube: packaging the aperture and the payload | fleet | raincube
### Learning objective
Connect a compact scientific instrument to its deployment and bus needs.
### Concept explanation
RainCube demonstrated precipitation radar technology in a CubeSat. NASA JPL's mission-results article describes its radar observations of precipitation and an operating life that extended beyond the initial primary mission, ending with atmospheric reentry in December 2020. The radar measured returned signals from precipitation rather than simply taking visible-light pictures. This made the instrument's radio measurement method central to the scientific demonstration.
Miniaturizing an instrument must be considered together with its antenna, deployment and supporting spacecraft. A usable radar observation requires compatible electrical energy, signal processing, thermal conditions, pointing and data handling. The general engineering inference is that reducing launch packaging volume can move difficulty into a deployed structure and its verification. This is an interpretation students can investigate through the source, not a claim that one packaging rule explains every detail of RainCube's actual design.
### Why it matters
A compact stowed assembly does not eliminate the need for an appropriate operating aperture. Deployable hardware must survive launch and reach a repeatable functional configuration.
### Engineering example
Compare a fixed antenna that fits the launch envelope with a larger deployable alternative. State what measurement performance each enables, and list the release, structural, alignment and test evidence needed by the deployable concept. Include the consequences of a failed deployment in the risk assessment.
### Trade-offs
Deployment can enable an otherwise unavailable aperture but adds mechanisms and critical events. A smaller fixed system might be easier to verify while failing the desired measurement requirement.
### Key takeaways
Payload miniaturization is a system design problem. Evaluate stowed geometry, deployed geometry and measurement quality together.

## CYGNSS: designing for repeated observations | fleet | cygnss
### Learning objective
Understand a constellation as a sampling strategy rather than a collection of identical cameras.
### Concept explanation
NASA describes the Cyclone Global Navigation Satellite System, CYGNSS, as a constellation for measuring ocean-surface winds. Its measurement approach uses navigation signals reflected from the surface rather than treating every spacecraft as a conventional optical imager. The engineering opportunity is to obtain distributed observations through an architecture that uses available transmitted signals. The mission's scientific focus is different from a high-resolution land-imaging mission.
A constellation introduces a time-and-location sampling problem. Multiple spacecraft can provide opportunities that one vehicle cannot, but users still need measurement calibration, geolocation, processing and interpretation. The mission overview describes the architecture and objective; statements about general operational complexity here are educational deductions, not an asserted count of active spacecraft today or a detailed reconstruction of the flight design.
### Why it matters
Coverage, revisit and measurement quality are different dimensions of performance. A mission can prioritize sampling rapidly changing phenomena over fine spatial pictures of a small target.
### Engineering example
Compare observing an evolving storm with inspecting a particular field boundary. The storm study may value observations distributed in time and location. The field study may need different spatial and spectral capabilities. Ask which measurement can support each decision before selecting an architecture, and identify what metadata the scientists need to compare observations.
### Trade-offs
More vehicles can improve sampling opportunities but increase production, tracking, coordination and data-processing work. Reusing available signals does not remove receiver, antenna, calibration or operations requirements.
### Key takeaways
Design the constellation and the measurement concept together. Select temporal and geographic sampling that serves the scientific question.

## Lunar Flashlight: useful evidence from an unmet objective | fleet | flashlight
### Learning objective
Discuss a mission difficulty without inventing a definitive failure cause.
### Concept explanation
Lunar Flashlight was intended to investigate lunar polar surface conditions using an active optical measurement concept. NASA JPL's May 2023 account states that propulsion difficulties prevented the spacecraft from reaching its planned lunar trajectory and that the mission was ended after attempts to recover sufficient performance. The account describes suspected debris in fuel passages as a likely explanation, not a universally proven cause to repeat without qualification. It also reports technology achievements despite the unmet lunar observation objective.
For students, the central distinction is between a mission's desired scientific result and the evidence returned by a technology demonstration. A subsystem can contribute useful flight information even when the integrated mission cannot reach its intended operating location. This does not make the lost science objective a success; it means outcomes should be reported at the level the evidence supports. Avoid adding exact performance figures or alternative diagnoses that the cited account does not establish.
### Why it matters
Propulsion availability, trajectory timing and opportunity windows are coupled. A system that produces some thrust may still be unable to execute the required maneuvers in time.
### Engineering example
Build an educational risk chain: insufficient thrust, missed correction opportunity, unavailable observing geometry, lost primary measurement. Identify what would have to be measured to distinguish competing propulsion explanations. Separate observed symptoms from hypotheses.
### Trade-offs
New technology may enable a small mission but carries development and verification risk. A fallback objective can preserve learning without replacing the original scientific need.
### Key takeaways
State what happened, what was suspected and what was learned separately. Good engineering communication preserves uncertainty.

## Landsat 9: measurements that stay comparable | fleet | landsat
### Learning objective
Relate Earth-observation hardware to calibrated products and a long scientific record.
### Concept explanation
Landsat 9 continues a land-observation program with optical and thermal measurements. NASA's mission overview describes an Operational Land Imager and a Thermal Infrared Sensor, along with calibration provisions and a role in maintaining observation continuity. These are complementary measurements, not two versions of the same photograph. A useful vegetation or land-change product depends on appropriate spectral information, thermal context where relevant, calibration and interpretation.
The mission illustrates why scientific value is not just pixel count. Comparing a place across seasons or years requires confidence that differences represent the surface rather than changes in instrument response or processing. A complete Earth-observation system therefore includes calibration, timing, archive management and accessible ground products. Those general lessons apply to a student vegetation concept, but the small fictional satellite in Mission Forge is not a substitute for Landsat hardware or its scientific data system.
### Why it matters
The eventual user needs measurements with known meaning and quality. A visually dramatic image without trustworthy calibration may not support a quantitative comparison.
### Engineering example
Suppose students observe a field twice and see different brightness. Ask about illumination, atmosphere, viewing geometry, sensor response and processing before concluding that vegetation changed. Identify which metadata and calibration checks would support a defensible interpretation. This is an analysis exercise, not a claim about a particular Landsat product.
### Trade-offs
Stable calibrated measurements require onboard references, ground processing and verification effort. More ambitious sensing can increase payload, support-system and data-management demands.
### Key takeaways
Design for comparable, interpretable products. Scientific continuity is an end-to-end system property, not a feature supplied by a camera alone.
