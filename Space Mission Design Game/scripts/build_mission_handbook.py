"""Six-page mission, choice, constraint and telemetry handbook; optional PDF tooling."""
from pathlib import Path
import json
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'output/pdf/mission-forge-complete-handbook.pdf'
NAVY=colors.HexColor('#102235');TEAL=colors.HexColor('#147C85');INK=colors.HexColor('#21374A');PALE=colors.HexColor('#EDF4F6')

def build():
    font=Path('C:/Windows/Fonts')
    if (font/'arial.ttf').exists():normal=font/'arial.ttf';bold=font/'arialbd.ttf'
    else:normal=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');bold=normal.with_name('DejaVuSans-Bold.ttf')
    pdfmetrics.registerFont(TTFont('Handbook',str(normal)));pdfmetrics.registerFont(TTFont('HandbookBold',str(bold)))
    pdfmetrics.registerFontFamily('Handbook',normal='Handbook',bold='HandbookBold')
    styles={
      'body':ParagraphStyle('body',fontName='Handbook',fontSize=10,leading=14,textColor=INK,spaceAfter=8),
      'small':ParagraphStyle('small',fontName='Handbook',fontSize=8.6,leading=11.5,textColor=INK,spaceAfter=5),
      'cell':ParagraphStyle('cell',fontName='Handbook',fontSize=8.6,leading=11.5,textColor=INK),
      'white':ParagraphStyle('white',fontName='HandbookBold',fontSize=9,leading=12,textColor=colors.white),
      'h':ParagraphStyle('h',fontName='HandbookBold',fontSize=12,leading=16,textColor=TEAL,spaceBefore=10,spaceAfter=7),
      'title':ParagraphStyle('title',fontName='HandbookBold',fontSize=25,leading=30,textColor=NAVY,spaceAfter=10)}
    flow=[]
    def p(text,style='body'):return Paragraph(text,styles[style])
    def add(text,style='body'):flow.append(p(text,style))
    def title(kicker,text,subtitle):
        add(kicker,'h');add(text,'title');add(subtitle)
    def table(headers,rows,widths):
        data=[[p(c,'white') for c in headers]]+[[p(str(c),'cell') for c in row] for row in rows]
        t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[PALE,colors.white]),
          ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
          ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),1,TEAL)]))
        flow.append(t);flow.append(Spacer(1,9))
    def page():flow.append(PageBreak())
    catalog=json.loads((ROOT/'content/design_catalog.json').read_text(encoding='utf-8'))
    cats={c['id']:c for c in catalog['categories']}
    def options(category,fields,impacts):
        rows=[]
        for o,impact in zip(cats[category]['options'],impacts):
            values='; '.join(label.format(**o) for label in fields)
            rows.append((o['label'],values,impact))
        table(['Choice','Game values','Trade-off / impact'],rows,[68,190,249])

    title('01 / THE MISSION + YOUR SCREEN','Understand Flood Watch.','Build a satellite mission that gets useful flood-observation data back to Earth, rather than merely putting a satellite in space.')
    add('WHAT SUCCESS MEANS','h')
    add('Deliver <b>at least 60 MB</b> to the ground with <b>no storage loss and no unmet energy</b>. First pass all eight design checks, place all six contributions and obtain host readiness approval; the mission budget is <b>EUR 145,000</b>.')
    add('The game connects launch (rocket and propellant), space (sensor, power, radio), ground (contact and downlink), and user needs (useful observations). These are simplified educational mission segments, inspired by NASA mission-design guidance [1].')
    add('READ THE TELEMETRY IN YOUR SCREENSHOT','h')
    table(['Screen label','Meaning'],[
      ('Cached GMAT R2026a','Saved output from a real GMAT trajectory run; GMAT is not running now. Live mode instead invokes the host\'s installed GMAT R2026a.'),
      ('389 simulated min','389 minutes since the trajectory start, not 389 minutes spent playing. The cached run spans 600 simulated minutes with 60-second samples; the visual replay is accelerated.'),
      ('Battery 9.0 Wh','9 watt-hours remain in the battery. This is stored energy, not watts of instantaneous power; the Compact battery is full at 9 Wh.'),
      ('Storage 0 MB','No unsent observations currently occupy onboard storage. Data may already have been transmitted; this is not the total amount collected.'),
      ('Delivered 120/60 MB','120 MB have reached the ground against a 60 MB requirement: the delivery goal is already met. This is not a storage-capacity ratio.'),
      ('SUNLIGHT / ECLIPSE','Sunlight allows solar generation; Earth shadow stops it and loads draw on the battery. The game estimates shadow from orbit positions.'),
      ('CONTACT / NO CONTACT','Contact means the satellite is above the modeled station\'s 5-degree elevation threshold and may downlink. NO CONTACT is normal between passes; data waits in storage.')],[126,381])
    add('<b>GMAT versus game:</b> GMAT supplies time-stamped position/velocity. The game derives contact, eclipse and target visibility, then computes energy, storage and delivery; those resource numbers are not GMAT telemetry. The Earth artwork and cloud animation are presentation only.','small')
    page()

    title('02 / HARDWARE TABLES','Choose what flies.','Each choice changes a connected design. The fixed spacecraft bus already contributes 30 kg, EUR 20,000, 12 W idle demand and 800 MB storage.')
    add('PAYLOAD / SENSOR - WHAT YOU MEASURE','h')
    add('The imager collects observations; Science &amp; Payload owns this table. Higher quality means a better teaching science grade, with higher electrical and data demand.','small')
    options('sensor',['EUR {cost_eur:,}; {mass_kg} kg','{power_w} W; {data_mb_min} MB/min; grade {quality}'],[
      'Basic meets the mission\'s grade-1 requirement at lower mass, cost and data production.',
      'Advanced adds EUR 15,000, 8 kg and 20 W; data rate doubles. It may require larger power, downlink or launch capacity.'])
    add('POWER PACKAGE - SOLAR ARRAYS + BATTERY','h')
    add('Arrays supply power in sunlight; the battery covers shadow and deficits. Power &amp; Spacecraft Systems owns this table.','small')
    options('power',['EUR {cost_eur:,}; {mass_kg} kg','{generation_w} W generation; {battery_wh} Wh capacity'],[
      'Compact saves mass and budget but leaves only +8 W peak margin in the default design.',
      'Extended adds EUR 12,000 and 10 kg, with +65 W generation and +15 Wh capacity. More reserve may push spacecraft mass beyond Light launch limits.'])
    add('COMMUNICATIONS / RADIO - RETURN THE DATA','h')
    add('The radio sends queued observations only during ground contact. Communications &amp; Data owns this table.','small')
    options('radio',['EUR {cost_eur:,}; {mass_kg} kg','{power_w} W; {downlink_mb_min} MB/min'],[
      'Standard clears less data per contact but saves mass, budget and power.',
      'Fast adds EUR 10,000, 4 kg and 10 W, increasing downlink by 120 MB/min. It does not create additional contact windows.'])
    add('<b>Example:</b> Advanced + Compact + Standard gives 67 W simultaneous load against 55 W generation, so peak power fails. Extended fixes generation, but Advanced + Extended + Standard totals 75 kg and then requires Heavy launch.','small')
    page()

    title('03 / PLANNING TABLES','Choose how it operates.','Mission & Flight Dynamics owns three separate benches: Orbit, Launcher and Fuel. Submit all three choices as planning contributions in Integration.')
    add('ORBIT - OBSERVATION, SUNLIGHT AND GROUND ACCESS','h')
    add('The preview uses preset timing opportunities; the launch run instead derives events from GMAT positions. Ground-service prices cover the fictional 12-month scenario, while the demonstration propagates only 10 hours.','small')
    options('orbit',['EUR {ground_cost_eur:,} ground service','{period_min}-min preview; {sunlight_min} sunlight','{observation_min} observation; {contact_min} contact'],[
      'Regional: 30 min eclipse in the preview; GMAT semi-major axis 7,000 km and inclination 28.5 degrees (about 622 km altitude). Compatible with Light or Heavy.',
      'Wide: 45 min eclipse; GMAT semi-major axis 7,200 km and inclination 98 degrees (about 822 km altitude). Adds EUR 10,000, shortens preview contacts and requires Heavy; the name does not guarantee better delivered science.'])
    add('LAUNCHER - MASS LIMIT + ORBIT COMPATIBILITY','h')
    options('launcher',['EUR {cost_eur:,}; capacity {capacity_kg} kg'],[
      'Light supports Regional only and carries up to 70 kg. Lowest-cost launch option.',
      'Heavy costs EUR 12,000 more, supports either preset and carries up to 100 kg. It adds capacity, not sensor quality or data rate.'])
    add('FUEL - LAUNCH PROPELLANT, NOT SATELLITE FUEL','h')
    options('fuel',['EUR {cost_eur:,}'],[
      'Solid combines fuel and oxidizer in a stored solid motor; normally burns to completion after ignition. Simpler handling is the educational trade-off [2].',
      'Liquid uses separate tanks/feed systems and controllable propellant flow, with more complexity; throttle/restart capability depends on the engine [2]. In this game the only numerical difference is EUR 3,000 more.'])
    add('<b>Model boundary:</b> Fuel selection changes budget and a required shared contribution. Neither propellant option changes satellite mass, thrust, burn time, launch reliability or the GMAT trajectory; those effects are not simulated. All prices and hardware values are teaching assumptions, not NASA product specifications.','small')
    page()

    title('04 / CONSTRAINTS','Know what must pass.','Approval verifies the complete design, then the trajectory-driven mission has its own result. A green preview is necessary, but does not guarantee a successful operations run.')
    add('EIGHT PREVIEW / READINESS CHECKS','h')
    table(['Check','Constraint','How to respond'],[
      ('Science quality','Sensor grade >= 1.','Basic already meets Flood Watch; Advanced increases demand.'),
      ('Budget','Total <= EUR 145,000, including bus, components, ground service, launcher and fuel.','Choose cheaper options; changing launch or power also changes available budget.'),
      ('Launch mass','Bus + sensor + power + radio <= launcher capacity: 70 kg Light / 100 kg Heavy.','Reduce hardware mass or select Heavy; fuel/launcher prices do not add modeled satellite mass.'),
      ('Orbit compatibility','Light: Regional only. Heavy: Regional or Wide.','Choose a matching orbit/launcher pair.'),
      ('Peak power','12 W bus + sensor W + radio W <= array generation W.','Increase power package or reduce sensor/radio demand; this is a conservative simultaneous-load rule.'),
      ('Eclipse energy','Zero unmet energy over the preview cycle. Battery must cover shadow loads.','Increase battery/arrays or reduce demand/eclipses. A positive peak margin alone is not enough.'),
      ('Data storage','Zero overflow; storage capacity is 800 MB.','Reduce production or improve radio/contact. Excess data is lost.'),
      ('Data delivery','Deliver all expected preview-cycle observations. Basic: 300 MB Regional / 360 MB Wide; Advanced: 600 / 720 MB.','Increase downlink/contact or lower production. This differs from the final 60 MB goal.')],[99,202,206])
    add('OPERATIONS RESULT + WORKFLOW GATES','h')
    table(['Requirement','Pass condition'],[
      ('Final science outcome','Delivered >= 60 MB AND storage loss = 0 AND unmet energy = 0 over the GMAT-based run. Numerical zero checks use small floating-point tolerances.'),
      ('Before launch','Select Flood Watch; explicitly pick all six options, place/submit all six, pass all checks and get host approval for that exact design.'),
      ('After editing','Recollect/resubmit affected choices and approve again; earlier approval is invalidated. Overspend blocks collection, approval and launch.')],[126,381])
    add('The twelve-month service figure is a cost/scenario assumption, not a demonstrated lifetime. The game does not process real flood images or prove coverage, reliability, propulsion performance or flight readiness.','small')
    page()

    title('05 / RESOURCE GLOSSARY','Read the trade-off panel.','The station panel shows the current shared design and a preset-cycle preview; the flight screen shows the evolving trajectory-driven run.')
    table(['Property / unit','Meaning and relationship'],[
      ('Cost / budget / remaining (EUR)','Total selected mission price / allowed spending / budget minus cost. A negative remainder fails the budget check.'),
      ('Mass / capacity / margin (kg)','Spacecraft mass / launch limit / capacity minus mass. Negative margin means the launcher cannot carry this design.'),
      ('Science grade','Teaching instrument-quality level: Basic 1, Advanced 2. Higher grade does not multiply delivered megabytes in the operations model.'),
      ('Peak load / generation (W)','Worst-case simultaneous electrical demand / solar-array output in sunlight. Power margin = generation minus peak load.'),
      ('Battery capacity (Wh)','Maximum stored energy. Watts are a rate; watt-hours are an amount: 12 W for 30 minutes consumes 6 Wh.'),
      ('Battery minimum / end (Wh)','Lowest stored energy reached / energy remaining after the preview cycle. The flight battery value is the current amount instead.'),
      ('Eclipse / contact (min)','Time in shadow / time available to transmit in the preview. Flight events come from simplified geometry along the GMAT trajectory.'),
      ('Expected / produced (MB)','Expected observations = instrument rate x preview observing minutes. Produced is actual data after any energy shortage reduces activity.'),
      ('Delivered (MB)','Cumulative data successfully transmitted; onboard collection alone does not count as delivery.'),
      ('Stored at end / peak (MB)','Unsent data remaining after the preview / highest queue occupancy reached. Compare peak with the 800 MB capacity.'),
      ('Overflow / storage loss (MB)','Observations discarded because new data exceeded available storage. Any loss fails readiness or operations success.'),
      ('Unserved load / energy (Wh)','Electrical demand that solar generation plus available battery could not supply. Any meaningful shortage fails the energy requirement.'),
      ('Solar energy (Wh)','Total energy generated during the preview; differs from instantaneous generation in watts.'),
      ('Used energy (Wh)','Energy actually supplied to loads over the preview, after any shortage.'),
      ('Curtailed energy (Wh)','Surplus generation discarded because the battery was full; it is unused opportunity, not a failure by itself.'),
      ('Preview checks passed','Number of the eight engineering checks that currently pass. It is not the count of placed contributions.')],[150,357])
    add('WHY CAN THE PREVIEW SAY 300 MB BUT FLIGHT SAY 120 MB?','h')
    add('The preview schedules a preset cycle and expects all of its observations to be delivered. <b>Targeted</b> operations collect only while the target is visible and sunlit, stopping at <b>120 MB total</b>; <b>Continuous</b> keeps collecting in eligible windows and can overload storage. The final delivery threshold remains <b>60 MB</b>.','small')
    page()

    title('06 / SUCCESSFUL RUN','Follow this exact recipe.','This configuration is verified against the shipped Cached GMAT trajectory with the Targeted plan. Other valid designs can work, but may need different trade-offs.')
    table(['Table','Pick','Price'],[
      ('Payload','Basic','EUR 15,000'),('Power','Compact','EUR 18,000'),('Communications','Standard','EUR 10,000'),
      ('Orbit','Regional','EUR 8,000'),('Launcher','Light','EUR 18,000'),('Fuel','Solid','EUR 2,000'),
      ('Fixed bus (already included)','Structure, computer, attitude control, storage','EUR 20,000')],[136,248,123])
    for heading,body in [
      ('1 / BRIEF + BUILD','Select Flood Watch at the entry Earth display. Use the Library\'s right-hand doorway; visit Payload, Power, Communications, then the three Mission Planning benches. Press E and SELECT &amp; PICK at each assigned table.'),
      ('2 / INTEGRATE','Place Sensor, Power and Radio at their marked Integration slots with E. At Mission Plan, submit Orbit, Launcher and Fuel; left/right selects the planning contribution and E places it. All six must be submitted.'),
      ('3 / APPROVE + LAUNCH','Press M: the host uses the gold VALIDATE &amp; APPROVE button. Choose CACHED + TARGETED; host or Flight presses the green LAUNCH NOW. Preparation and playback start automatically.'),
      ('4 / EXPLAIN THE RESULT','Expected: EUR 91,000 / 145,000; 57 / 70 kg; 47 W peak load / 55 W generation (+8 W). The verified run delivers 120 MB, with zero storage loss and zero unmet energy; 120/60 MB means twice the required volume.')]:
        add(heading,'h');add(body,'small')
    add('PLAYING WITH FRIENDS','h')
    add('N opens a LAN room for 2-4 players. Everyone uses the same game version, host Wi-Fi IPv4 and room code; only the host needs GMAT for Live mode. Science owns payload, Power owns power, Communications owns radio and Flight owns orbit/launcher/fuel; roles are combined automatically for smaller crews.','small')
    add('SOURCES + MODEL NOTES','h')
    add('Game values and rules: content/design_catalog.json, content/missions.json, game/domain/design.py, game/domain/operations.py and game/orbit/provider.py. The previous two-page quick recipe remains available; this guide adds the full glossary and constraints.','small')
    add('[1] <link href="https://www.nasa.gov/wp-content/uploads/2025/04/250323-design-and-develop-science-mission.pdf" color="#147C85">NASA - Design and Develop Science Missions (2025)</link><br/>[2] <link href="https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/propulsion-system/" color="#147C85">NASA Glenn - Propulsion System</link>','small')

    def footer(c,doc):
        c.setStrokeColor(colors.HexColor('#C3D4DC'));c.line(44,41,551,41)
        c.setFont('Handbook',8);c.setFillColor(TEAL);c.drawString(44,27,'MISSION FORGE / PLAYER HANDBOOK / 15 NOV 2026')
        c.drawRightString(551,27,f'{doc.page} / 6')
    OUT.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(OUT),pagesize=(595.276,841.89),leftMargin=44,rightMargin=44,topMargin=35,bottomMargin=55,
                          title='Mission Forge - Complete Player Handbook',author='Mission Forge')
    doc.build(flow,onFirstPage=footer,onLaterPages=footer)
    from pypdf import PdfReader
    assert len(PdfReader(OUT).pages)==6,'Reflow requires page review / footer update'
    print(OUT)

if __name__=='__main__':build()
