

Space Mission Design Game Join the Challenge DetailsResourcesTeams Event 2026 N…

NASA does not endorse any non-U.S. Government entity and is not responsible for…
https://www.spaceappschallenge.org/2026/challenges/space-mission-design-game/


I want to build a software for this project, it is a part of a hackathon.


I want to make it like a simulator for real life project, and I want to make it has a Space Theme. It should also be objective orianted, and each objective teach the player something new and allow him after finishing it to proceed to the next objective, until he manages to solve the whole challenge, propose a design for the game first to me, then lets discuss it first before we proceed with the implementation

Friday 7:20 PM
I propose MISSION FORGE: a space-themed mission simulator where the player leads a small space agency from an initial scientific goal to a functioning satellite mission.

The central idea is: every objective teaches one concept, every decision changes the spacecraft, and the final simulation tests the design the player actually built.

This follows the emphasis in your supplied challenge brief on complete missions, engineering trade-offs, limited resources, and learning through experimentation.

1. The experience
The player becomes the mission director of a new orbital research program. Their first assignment:

Design and operate a satellite that monitors flooding and delivers useful observations to emergency response teams.

I recommend starting with an Earth-observation mission. It gives the player a clear real-world purpose while naturally introducing instruments, orbit selection, power, communications, launch, and operations.

The campaign should take approximately 20–30 minutes, with a faster demonstration path for hackathon judges.

The gameplay loop is:

Receive an objective → experiment with a design → see its consequences → validate it → unlock the next objective.

2. The objectives
Stage	Player’s objective	What they learn	Condition for progressing
1. Define the mission	Decide what observations the satellite must deliver and how quickly	Scientific goals become measurable requirements	Create a consistent mission brief
2. Choose the orbit	Compare orbital options using animated coverage previews	Orbit affects coverage, revisit time, and communications	Demonstrate that the orbit can support the mission
3. Select the instruments	Equip the satellite with a suitable sensor	Better capabilities can require more mass, energy, money, and data capacity	Meet observation requirements within initial limits
4. Build the spacecraft	Add structure, solar panels, battery, computer, and attitude control	Instruments depend on supporting spacecraft systems	Produce a technically feasible configuration
5. Connect to Earth	Choose communications hardware and ground-station access	Collecting data and delivering useful data are different problems	Transmit enough observations before their deadline
6. Prepare for launch	Select a compatible launch option and complete the budget	Launch capacity depends on destination orbit; reserves matter	Pass the launch readiness review
7. Operate the mission	Schedule observations, battery use, and downlinks	A feasible design still needs good operations	Complete the mission’s operational targets
8. Review the results	Inspect performance and improve the design	Engineering improves through evidence and iteration	Earn mission completion and unlock replay
Each stage introduces a small amount of information through an action. For example, the player first sees the battery drain during an eclipse, then receives a short explanation of why solar panels cannot supply power there.

Progress should require a defensible design, with multiple valid solutions. Earlier stages remain editable; changes trigger revalidation of affected requirements.

3. Make it feel like a simulator
The spacecraft should behave according to a consistent, simplified engineering model.

For example:

The player adds a more capable sensor. Observation quality improves, but power consumption and data generation rise. A larger battery increases mass and cost. More ground-station access helps deliver the data but consumes the remaining budget.

During operations, a simulation clock advances the satellite around Earth. The game tracks:

Battery charge, sunlight, and eclipse periods.
Observation opportunities and instrument activity.
Onboard storage and generated data.
Ground-station contact windows and transmitted observations.
Spending, mission time, and delivered scientific value.
The orbital animation and the resource calculations should use the same mission state, so what the player sees explains what happens.

We should label the model as an educational approximation, with sourced assumptions and units available in an optional engineering panel.

4. The visual design
I would use a mission-control aesthetic: deep navy backgrounds, a detailed Earth, white typography, cyan interface highlights, amber cautions, and red critical alerts.

The main screen has four areas:

Area	Purpose
Left: Mission objectives	Current assignment, completion conditions, and unlocked stages
Center: Interactive scene	Earth and orbit, spacecraft assembly, or mission operations
Right: Engineering panel	Component choices, specifications, comparisons, and explanations
Bottom: Resource strip	Budget, mass, battery, power, storage, and mission time
The center changes with the task. Instrument selection shows the spacecraft and payload slots; orbit selection shows Earth and coverage; operations shows the moving satellite, contacts, and timeline.

A persistent “Why did this change?” interaction explains consequences directly:

“Your storage is filling because the sensor generates more data each orbit than your current downlink schedule transmits.”

5. Failure, feedback, and replay
Failure should create an understandable engineering problem.

If the battery runs out, the game pauses at the relevant moment, highlights the cause, and lets the player revise the configuration or schedule. Restarting the entire campaign should be unnecessary.

The final report shows:

Whether the mission met its requirements.
How much useful data reached Earth on time.
Resource margins and operational problems.
Which decisions caused the largest effects.
A comparison with the player’s previous attempt.
Meeting the mission requirements determines success. Efficiency and resilience provide additional distinctions, so a cheap spacecraft cannot “win” while failing its scientific purpose.

6. What I recommend building for the hackathon
The first version should include one polished mission, all eight objectives, a small component catalog, an animated orbital view, and a working operations simulation.

Save/load and a clear mission report would make the experience complete. Additional missions, extensive spacecraft customization, and online multiplayer can follow. Optional team play could initially work on one screen with four roles: mission director, science lead, spacecraft engineer, and operations lead.

The strongest demonstration would be watching a player build a satellite, discover a specific weakness in simulation, fix it, and successfully deliver observations.

My recommendation is a guided strategy simulator with a strong visual space environment. Does this match your vision, or were you imagining more hands-on control—such as piloting the rocket and manually assembling the spacecraft?

Friday 7:21 PM
Generate a pdf for that, also explain how it can be split on a team of either 2, or 3 people

Friday 7:32 PM
Created the six-page PDF covering the game design, eight objectives, simulation mechanics, hackathon scope, and team plans.

The recommended split is:

Team	Responsibilities
2 people	A: interface, visualization, tutorials. B: simulation, engineering checks, progression, save/load.
3 people	A: interface and visualization. B: simulation and engineering. C: objectives, educational content, save/load, and integration coordination.
Both plans include concrete deliverables and checkpoints. With three people, I recommend keeping the same scope and using the extra capacity for polish and reliability.

mission-forge-game-design.pdf
PDF

Edited create_proposal.py
+128
-0
Friday 7:35 PM

- We need to design a space mission game, and to consider different factors suc…

NASA does not endorse any non-U.S. Government entity and is not responsible for…
Now based on the design pdf and these notes:

We should also consider this tool: https://www.libhunt.com/r/ursina as the game engine


And here are also the resources provided for the challenge:



Also some additional notes:

We should present this in 5 miniutes presentation to impress the juries, so we do not want to make the tool so complicated, it should do the basic functionality and looks impresive, but also stay simple
We want it to be 3D game which is integratable to the provided tool
The game user should be able to move in enviroment, and the movements should be with the arrows and the movement make a camera movement so it comes close or away from things.
There should be a room which he opens, in which he see list of cards, each card explain important information from the things which are provided.
Make the implementation in phases, so after each phase we can test it manually, and suggest what can be done next. 
Consider this pdf for the designing of mission: 
We can focus first on single player mode, and later think how can we integrate the multiplayer mode
The game should be splitied into consecutive missions, each mission has certain task, which is possible to know if it is success or not.
FOCUS ON THE TRADE-OFF EFFECT THAT WHEN USER SELECT CERTAIN DECISION CHOICE, IT SHOULD IMPACT OTHERS
Ensure that we can integrate :  I installed it
If there is any step that I need to do manually before we proceed or I need to install, notify me.
If possible also make a script in the repo that installs all the required dependencies, and make sure it can work on Linux and windows, because my colleague is using Linux.
If you also have some suggestion, let me know.
Keep a tracking file in the repo, in which you describe the whole thing we try to do, and what have we finished, and what is left, so we can keep track of the progress, and my friend can get it from the repo and use her own local codex to read it and continue from it. 
Lets start by the design phases suggestion, so you tell me how many phases we need to have, and generate a pdf with that design, and save it in the repo, then we can proceed with each phase and after each phase ask me whether to continue or not.

…
2:39 PM
Response started
I’ll review your notes, the NASA mission-design guide, and the engine and integration requirements, then create a phased design




