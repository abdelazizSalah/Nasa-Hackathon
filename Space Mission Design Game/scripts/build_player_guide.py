"""Build the concise, two-page player guide using optional document tooling."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT.parent/'output/pdf/mission-forge-player-guide.pdf'
NAVY=HexColor('#0C1727');CYAN=HexColor('#147C85');INK=HexColor('#182F43');MUTED=HexColor('#536A7A');PALE=HexColor('#EDF5F6')
W,H=595.276,841.89

def build():
    # Fonts are document build inputs, never runtime game dependencies.
    font_dir=Path('C:/Windows/Fonts')
    if (font_dir/'arial.ttf').exists():
        pdfmetrics.registerFont(TTFont('Guide',str(font_dir/'arial.ttf')))
        pdfmetrics.registerFont(TTFont('GuideBold',str(font_dir/'arialbd.ttf')))
    else:
        from reportlab import rl_config
        font_dir=Path(rl_config.TTFSearchPath[0])
        candidates=[Path('/usr/share/fonts/truetype/dejavu'),font_dir]
        directory=next(p for p in candidates if (p/'DejaVuSans.ttf').exists())
        pdfmetrics.registerFont(TTFont('Guide',str(directory/'DejaVuSans.ttf')))
        pdfmetrics.registerFont(TTFont('GuideBold',str(directory/'DejaVuSans-Bold.ttf')))
    pdfmetrics.registerFontFamily('Guide',normal='Guide',bold='GuideBold')
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(OUTPUT),pagesize=(W,H));c.setTitle('Mission Forge - First Launch and Component Trade-offs')
    c.setAuthor('Mission Forge')
    def text(value,x,y,width=507,size=10.5,leading=14,color=INK,bold=False):
        style=ParagraphStyle('body',fontName='GuideBold' if bold else 'Guide',fontSize=size,leading=leading,textColor=color)
        p=Paragraph(value,style);_,height=p.wrap(width,H);p.drawOn(c,x,y-height);return y-height
    def header(kicker,title,subtitle,page):
        c.setFillColor(NAVY);c.rect(0,H-150,W,150,fill=1,stroke=0)
        text('MISSION FORGE / '+kicker,44,H-31,size=9,leading=12,color=HexColor('#68DDDE'),bold=True)
        text(title,44,H-61,size=25,leading=29,color=HexColor('#FFFFFF'),bold=True)
        text(subtitle,44,H-106,size=10.4,leading=14,color=HexColor('#D5E6EC'))
        c.setStrokeColor(HexColor('#C6D8E0'));c.line(44,43,W-44,43)
        text('PLAYER FIELD GUIDE / 15 NOV 2026',44,32,size=8,leading=10,color=MUTED)
        text(f'{page} / 2',W-81,32,width=40,size=8,leading=10,color=MUTED)

    header('01 / EXACT RECIPE','Make your first mission succeed.','Use these choices in order. Tested with the shipped Cached GMAT trajectory and Targeted plan.',1)
    y=H-176
    y=text('FLOOD WATCH',44,y,size=12,bold=True,color=CYAN)-8
    y=text('1. Close the welcome instructions. For co-op, press <b>N</b> and connect everyone first; the host selects <b>Flood Watch</b> at the Earth display.',44,y)-12
    choices=[('1 / Payload','BASIC','EUR 15,000'),('2 / Power','COMPACT','EUR 18,000'),('3 / Communications','STANDARD','EUR 10,000'),
             ('4 / Orbit','REGIONAL','EUR 8,000 ground service'),('5 / Launcher','LIGHT','EUR 18,000'),('6 / Fuel table','SOLID','Included / EUR 0 extra')]
    for row in range(3):
        for col in range(2):
            title,choice,price=choices[row*2+col];x=44+col*259
            c.setFillColor(PALE);c.roundRect(x,y-72,248,72,6,fill=1,stroke=0)
            text(title,x+12,y-10,width=222,size=9,color=MUTED,bold=True)
            text(choice,x+12,y-27,width=222,size=14,color=INK,bold=True)
            text(price,x+12,y-49,width=222,size=9,color=CYAN)
        y-=82
    y-=1
    y=text('2. Walk through the Library\'s right-hand doorway. At each assigned table press <b>E</b>, then click <b>SELECT &amp; PICK</b> once; choose Orbit and Launcher in Mission Planning, then visit the separate Fuel table.',44,y)-11
    y=text('3. At Integration, use <b>E</b> to place Sensor, Power and Radio. At the Mission Plan desk submit <b>Orbit, Launcher and Fuel</b>; left/right chooses a plan and E places it.',44,y)-11
    y=text('4. The host runs <b>Validation</b> after all <b>6/6</b> contributions are placed. The Flight engineer then approaches Launch Readiness, selects <b>CACHED</b> and <b>TARGETED</b>, and clicks <b>LAUNCH &amp; OPERATE</b>.',44,y)-15
    c.setFillColor(NAVY);c.roundRect(44,y-79,507,79,6,fill=1,stroke=0)
    text('EXPECTED RESULT',56,y-10,size=10,color=HexColor('#68DDDE'),bold=True)
    text('<b>EUR 89,000 / EUR 145,000</b> budget; 57 / 70 kg; +8 W peak-power margin.<br/><b>120 MB delivered</b> against the 60 MB goal; zero storage loss and zero unmet energy.',56,y-29,width=480,size=10.5,leading=15,color=HexColor('#FFFFFF'))
    y-=95
    text('<b>Avoid:</b> Continuous imaging, Wide orbit, or an Advanced sensor on this first run. Preview-cycle data (300 MB here) differs from the trajectory-driven mission result; changing a choice requires recollection, resubmission and fresh approval.',44,y,size=9.4,leading=12,color=MUTED)
    c.showPage()

    header('02 / EXPLAIN THE TRADE-OFF','Six tables. One connected design.','Each explanation is at most two sentences. Prices and numerical hardware limits are teaching assumptions.',2)
    sections=[
      ('PAYLOAD / WHAT YOU MEASURE',
       '<b>Basic:</b> EUR 15k, 10 kg, 20 W, grade 1 and 30 MB/min; <b>Advanced:</b> EUR 30k, 18 kg, 40 W, grade 2 and 60 MB/min. The imager collects science: better detail doubles data production and increases power, mass and cost.'),
      ('POWER / KEEP THE SATELLITE ALIVE',
       '<b>Compact:</b> EUR 18k, 12 kg, 55 W generation and 9 Wh battery; <b>Extended:</b> EUR 30k, 22 kg, 120 W and 24 Wh. Solar arrays run the spacecraft and the battery covers eclipse, so more reserve costs mass and may require a heavier launcher.'),
      ('COMMUNICATIONS / GET SCIENCE TO EARTH',
       '<b>Standard:</b> EUR 10k, 5 kg, 15 W and 80 MB/min downlink; <b>Fast:</b> EUR 20k, 9 kg, 25 W and 200 MB/min. The radio clears stored observations during ground contact: faster delivery reduces backlog but adds electrical demand, mass and cost.'),
      ('ORBIT / WHEN YOU OBSERVE AND TRANSMIT',
       '<b>Regional:</b> EUR 8k ground service, 10 observing / 6 contact / 30 eclipse minutes per preview cycle; <b>Wide:</b> EUR 18k, 12 / 4 / 45 minutes. Orbit geometry determines observation, sunlight and ground access; these preset timings teach why more observing can worsen storage, battery and delivery.'),
      ('LAUNCHER / GET THE SPACECRAFT TO ITS ORBIT',
       '<b>Light:</b> EUR 18k, 70 kg capacity, Regional only; <b>Heavy:</b> EUR 30k, 100 kg, either orbit. A launcher carries the complete spacecraft, so extra capacity and orbit compatibility consume budget instead of improving the sensor.'),
      ('FUEL TABLE / LAUNCH PROPELLANT, NOT SATELLITE FUEL',
       '<b>Solid:</b> included, premixed fuel/oxidizer and usually burns to completion; <b>Liquid:</b> EUR 5k extra, separate propellant feed systems with flow control. Liquid systems add hardware/operating complexity, and throttle or restart capability depends on engine design [1, 2].')]
    y=H-174
    for title,body in sections:
        y=text(title,44,y,size=10.3,leading=13,color=CYAN,bold=True)-5
        y=text(body,44,y,size=9.8,leading=13)-15
    y=text('WHAT THE GAME MODELS',44,y,size=9.5,color=CYAN,bold=True)-5
    y=text('Fixed bus: 30 kg, EUR 20k, 12 W and 800 MB storage, already included in totals. Propellant choice changes the launch-plan price and shared submission, not bus mass or GMAT thrust; both launch classes are simplified options rather than specific real rocket designs.',44,y,size=9.1,leading=12,color=MUTED)-12
    y=text('NASA REFERENCES / CLICK TO READ',44,y,size=9.5,color=CYAN,bold=True)-5
    y=text('[1] <link href="https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/propulsion-system/" color="#147C85">NASA Glenn - Propulsion System</link> &nbsp; [2] <link href="https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/model-solid-rocket-engine/" color="#147C85">NASA Glenn - Model Solid Rocket Engine</link>',44,y,size=9,leading=12,color=MUTED)
    assert y>49,('Content exceeds page',y)
    c.save();print(OUTPUT)

if __name__=='__main__':build()
