"""Original procedural surface textures; no downloaded or licensed artwork."""
from pathlib import Path
from random import Random
from PIL import Image,ImageDraw

ASSETS=Path(__file__).resolve().parents[2]/'content/materials'

def generate():
    ASSETS.mkdir(parents=True,exist_ok=True);rng=Random(38)
    im=Image.new('RGB',(256,256));p=im.load()
    for y in range(256):
        line=rng.randrange(-12,13)
        for x in range(256):
            a=145+line+rng.randrange(-4,5);p[x,y]=(a,a+4,a+8)
    im.save(ASSETS/'brushed-metal.png')
    im=Image.new('RGB',(256,256),'#123c76');d=ImageDraw.Draw(im)
    for x in range(0,256,32):d.line((x,0,x,256),fill='#86b6d5',width=2)
    for y in range(0,256,64):d.line((0,y,256,y),fill='#b8d8ed',width=2)
    for y in range(8,256,8):d.line((0,y,256,y),fill='#23548c',width=1)
    im.save(ASSETS/'solar-cells.png')
    im=Image.new('RGB',(256,256),'#dcae43');d=ImageDraw.Draw(im)
    for x in range(-256,512,64):d.polygon([(x,0),(x+30,0),(x+286,256),(x+256,256)],fill='#202b36')
    im.save(ASSETS/'hazard-stripes.png')
    im=Image.new('RGB',(256,256),'#aa8744');d=ImageDraw.Draw(im)
    for _ in range(150):
        x,y=rng.randrange(256),rng.randrange(256)
        d.line((x,y,x+rng.randrange(-40,41),y+rng.randrange(10,60)),fill=rng.choice(['#ddbf79','#765e35','#baa36b']),width=2)
    im.save(ASSETS/'thermal-foil.png')

def surface(name):
    from ursina import load_texture
    return load_texture(name+'.png',folder=ASSETS)

if __name__=='__main__':generate()
