"""Generate original, offline schematic artwork; no downloaded images or logos."""
from pathlib import Path
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont
from game.library.content import DATA, load_library

ASSETS=DATA/'assets'

def font(size):
    return ImageFont.load_default(size=size)

def schematic(symbol):
    im=Image.new('RGB',(720,420),'#102b3a');d=ImageDraw.Draw(im)
    cyan='#66e5e3';gold='#ffd58d';white='#dfedf0'
    def line(points,fill=cyan,width=4):d.line(points,fill=fill,width=width)
    def box(rect,label,fill='#22495a'):
        d.rounded_rectangle(rect,10,fill=fill,outline=cyan,width=3)
        x,y,X,Y=rect;d.text(((x+X)/2,(y+Y)/2),label,font=font(19),fill=white,anchor='mm')
    if symbol=='fleet':
        # Labeled conceptual silhouettes, not scale models of flight hardware.
        for i,label in enumerate(['MarCO','RainCube','CYGNSS','Lunar Flashlight','Landsat']):
            x=130+(i%3)*230;y=110+(i//3)*190
            d.rectangle((x-25,y-35,x+25,y+35),fill='#496f80',outline=cyan,width=3)
            if i in (0,2,4):
                for sign in (-1,1):
                    d.rectangle((x+sign*45-18,y-25,x+sign*45+18,y+25),fill='#264f7d',outline=gold,width=2)
            if i==1:
                d.ellipse((x+10,y-65,x+75,y),outline=gold,width=4);line([(x+25,y),(x+45,y-30)],gold)
            if i==3:
                for dx in (-15,-5,5,15):line([(x+dx,y+35),(x+dx*2,y+65)],gold,2)
            if i==4:
                d.ellipse((x-15,y-45,x+15,y-15),fill='#102b3a',outline=white,width=2)
            d.text((x,y+80),label,font=font(18),fill=white,anchor='mm')
    elif symbol=='satellite':
        box((250,55,470,120),'SCIENCE PAYLOAD')
        box((255,170,465,315),'STRUCTURE / BUS')
        box((25,145,205,205),'POWER / EPS')
        box((25,250,205,310),'ADCS / GNC')
        box((515,140,695,200),'COMMS')
        box((515,250,695,310),'AVIONICS')
        line([(360,120),(360,170)],gold)
        for x,y,X,Y in [(205,175,255,200),(205,280,255,280),(465,200,515,170),(465,280,515,280)]:line([(x,y),(X,Y)],gold)
        d.text((360,365),'Thermal control spans payload, bus and interfaces',font=font(20),fill=white,anchor='mm')
    elif symbol in ('orbit','orbits'):
        d.ellipse((275,125,445,295),fill='#266e96',outline=cyan,width=3)
        d.ellipse((75,60,645,360),outline=cyan,width=3)
        if symbol!='orbit':d.ellipse((220,28,500,390),outline=gold,width=3)
        box((535,155,605,205),'SAT')
        line([(570,205),(570,300)],gold);d.text((530,320),'velocity',fill=gold,font=font(18))
        line([(560,205),(440,210)],white);d.text((460,225),'gravity',fill=white,font=font(18))
        d.text((310,205),'EARTH',font=font(22),fill=white)
    elif symbol in ('satellite','solar','sensor'):
        box((285,125,435,290),'BUS');box((70,155,265,255),'SOLAR ARRAY');box((455,155,650,255),'SOLAR ARRAY')
        line([(265,205),(285,205)]);line([(435,205),(455,205)])
        d.polygon([(325,125),(360,55),(395,125)],outline=gold,width=4)
        d.text((285,25),'PAYLOAD / ANTENNA',font=font(19),fill=gold)
        if symbol=='sensor':
            line([(320,290),(250,365),(470,365),(400,290)],gold)
            d.text((267,380),'SENSING FOOTPRINT',font=font(19),fill=gold)
        elif symbol=='solar':
            d.ellipse((30,25,100,95),fill=gold)
            line([(115,75),(185,130)],gold)
            d.text((220,350),'Sunlight -> electricity -> storage -> loads',font=font(18),fill=white,anchor='mm')
        else:d.text((360,350),'Structure connects every subsystem',font=font(21),fill=white,anchor='mm')
    elif symbol=='rocket':
        d.polygon([(330,300),(330,120),(360,50),(390,120),(390,300)],fill='#426c7b',outline=cyan,width=4)
        d.polygon([(330,260),(295,325),(330,310)],fill=cyan);d.polygon([(390,260),(425,325),(390,310)],fill=cyan)
        d.polygon([(340,310),(360,390),(380,310)],fill=gold)
        line([(470,210),(470,80)],gold);d.text((490,140),'THRUST',font=font(24),fill=gold)
        d.text((70,210),'Momentum in exhaust\nchanges vehicle motion',font=font(20),fill=white)
    elif symbol=='layers':
        labels=['Protective finish','Structural skin','Core / supports','Fasteners + adhesive']
        for i,label in enumerate(labels):
            y=65+i*80;d.polygon([(70,y+20),(340,y),(420,y+30),(150,y+50)],fill=['#427283','#657b8e','#926b5c','#3c6574'][i],outline=cyan,width=3)
            line([(420,y+30),(470,y+30)],gold);d.text((485,y+30),label,font=font(18),fill=white,anchor='lm')
    elif symbol=='dish':
        d.arc((90,95,360,320),20,160,fill=cyan,width=12)
        line([(135,280),(225,150),(315,280)]);line([(225,150),(255,100)],gold)
        for r in (90,135,180):d.arc((235-r,85-r,235+r,85+r),220,310,fill=gold,width=3)
        box((475,230,650,310),'GROUND')
        line([(325,130),(520,220)],gold)
        d.text((440,80),'Pointing + power\n+ contact time',font=font(22),fill=white)
    elif symbol=='chamber':
        d.rounded_rectangle((100,55,590,350),40,outline=cyan,width=7)
        box((270,145,410,265),'TEST ITEM')
        for x in (180,540):
            for y in range(95,310,40):d.ellipse((x-5,y-5,x+5,y+5),fill=gold)
        d.text((350,385),'Environment -> measured response -> evidence',font=font(20),fill=white,anchor='mm')
    else:
        labels=['SCIENCE GOAL','REQUIREMENTS','DESIGN','TEST EVIDENCE'] if symbol=='blueprint' else ['SENSORS','FLIGHT COMPUTER','ACTUATORS','FEEDBACK']
        positions=[(40,70,310,150),(410,70,680,150),(410,260,680,340),(40,260,310,340)]
        for p,label in zip(positions,labels):box(p,label)
        for p in [[(310,110),(410,110)],[(545,150),(545,260)],[(410,300),(310,300)],[(175,260),(175,150)]]:line(p,gold)
    return im

CAPTIONS={
 'orbit':'Gravity bends the path; sideways velocity sustains orbit.',
 'orbits':'Orbit geometry changes coverage, eclipse and contact opportunities.',
 'fleet':'Mission architecture connects spacecraft, geometry and ground users.',
 'satellite':'The bus supplies services; the payload performs the measurement.',
 'solar':'A power budget includes generation, storage and time-dependent loads.',
 'sensor':'Pointing and observation geometry shape the measured footprint.',
 'rocket':'Thrust is a force; specific impulse measures propellant efficiency.',
 'layers':'Interfaces and joints matter as much as bulk material properties.',
 'dish':'Useful data requires an end-to-end communication link.',
 'chamber':'Tests produce evidence against defined environmental requirements.',
 'blueprint':'Requirements, design and verification form a traceable loop.',
 'electronics':'Measurement, computation and actuation form a feedback loop.'}

def generate():
    ASSETS.mkdir(parents=True,exist_ok=True)
    books,_=load_library()
    for symbol in CAPTIONS:schematic(symbol).save(ASSETS/f'{symbol}.png')
    for i,book in enumerate(books):
        im=Image.new('RGB',(512,720),book['color']);d=ImageDraw.Draw(im)
        d.rectangle((20,20,492,700),outline='#9fced0',width=2)
        d.rectangle((30,35,42,685),fill='#182c3c')
        d.text((65,55),f'MISSION FORGE  /  {i+1:02}',font=font(20),fill='#d9eeee')
        d.text((65,120),'\n'.join(textwrap.wrap(book['title'],23)),font=font(30),fill='white',spacing=8)
        art=schematic(book['symbol']).resize((425,248));im.paste(art,(60,330))
        d.text((65,610),book['level'],font=font(20),fill='#ffe1a0')
        d.text((65,650),'AEROSPACE FIELD LIBRARY',font=font(17),fill='white')
        im.save(ASSETS/f'cover-{book["id"]}.png')

if __name__=='__main__':generate()
