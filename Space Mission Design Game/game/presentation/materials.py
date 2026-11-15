"""Offline surface maps; procedural materials plus credited NASA Earth imagery."""
from pathlib import Path
from random import Random
from functools import lru_cache
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
    generate_details()

def generate_details():
    """Bake reusable details once; the game only loads the resulting small maps."""
    ASSETS.mkdir(parents=True,exist_ok=True);rng=Random(192)
    def grain(base,size=512,amount=5):
        im=Image.new('RGB',(size,size));pixels=im.load()
        for y in range(size):
            for x in range(size):
                n=rng.randint(-amount,amount)
                pixels[x,y]=tuple(max(0,min(255,c+n)) for c in base)
        return im
    im=grain((191,199,207));d=ImageDraw.Draw(im)
    d.rectangle((5,5,506,506),outline='#737f8a',width=3)
    d.rectangle((10,10,501,501),outline='#e0e4e6',width=2)
    for x in (22,490):
        for y in (22,490):
            d.ellipse((x-5,y-5,x+5,y+5),fill='#65717b',outline='#e8edef',width=1)
            d.line((x-3,y,x+3,y),fill='#313e47',width=2)
    for y in range(414,462,8):d.rounded_rectangle((300,y,455,y+3),radius=1,fill='#344451')
    d.rectangle((40,430,150,452),fill='#425b6a');d.line((42,433,147,433),fill='#d3dfe3',width=2)
    im.save(ASSETS/'equipment-panel.png')
    im=grain((166,176,185));d=ImageDraw.Draw(im)
    for y in (0,256,511):d.line((0,y,512,y),fill='#46525e',width=5)
    for x in (0,256,511):d.line((x,0,x,512),fill='#46525e',width=5)
    for x in (16,240,272,496):
        for y in (16,240,272,496):d.ellipse((x-3,y-3,x+3,y+3),fill='#65717d')
    im.save(ASSETS/'wall-panels.png')
    im=grain((115,126,138));d=ImageDraw.Draw(im)
    for y in range(0,512,32):
        for x in range(0,512,32):
            d.line((x+5,y+12,x+18,y+25),fill='#b7c1c9',width=3)
            d.line((x+7,y+11,x+20,y+24),fill='#364552',width=2)
    im.save(ASSETS/'deck-plate.png')
    im=grain((226,229,228),amount=3);d=ImageDraw.Draw(im)
    for y in range(0,512,64):
        for x in range(0,512,64):d.rectangle((x+2,y+2,x+62,y+62),outline='#a1aeb8',width=2)
    im.save(ASSETS/'ceramic-tiles.png')
    im=grain((186,155,70),amount=12);d=ImageDraw.Draw(im)
    for _ in range(800):
        x,y=rng.randrange(512),rng.randrange(512);dx,dy=rng.randrange(-45,46),rng.randrange(-45,46)
        d.line((x,y,x+dx,y+dy),fill=rng.choice(['#f2d67d','#7c652f','#c7ad5c']),width=rng.choice([1,2]))
    im.save(ASSETS/'thermal-foil.png')
    im=grain((220,223,221),amount=4);d=ImageDraw.Draw(im)
    for x in range(0,512,5):d.line((x,0,x,512),fill='#aab1b5')
    for y in range(0,512,5):d.line((0,y,512,y),fill='#d4d8d7')
    for i in range(-512,1024,64):d.line((i,0,i+512,512),fill='#edf0ea',width=2)
    im.save(ASSETS/'suit-fabric.png')
    im=grain((38,42,48),size=128,amount=3);d=ImageDraw.Draw(im)
    for y in range(0,128,8):d.line((0,y,128,y),fill='#68717a',width=2)
    im.save(ASSETS/'rubber-grip.png')
    im=Image.new('RGB',(256,256));pixels=im.load()
    for y in range(256):
        for x in range(256):
            r=((x-128)**2+(y-128)**2)**.5/128
            ring=max(0,1-abs(r-.62)*28)
            shine=max(0,1-((x-80)**2/50**2+(y-65)**2/25**2))*110
            pixels[x,y]=(int(min(255,9+ring*30+shine*.5)),int(min(255,24+ring*65+shine)),int(min(255,41+ring*100+shine*1.3)))
    im.save(ASSETS/'optical-glass.png')

@lru_cache(maxsize=64)
def surface(name):
    from ursina import load_texture
    from panda3d.core import SamplerState
    texture=load_texture(name if Path(name).suffix else name+'.png',folder=ASSETS)
    if texture:
        texture._texture.setMinfilter(SamplerState.FT_linear_mipmap_linear)
        texture._texture.setMagfilter(SamplerState.FT_linear)
        texture._texture.setAnisotropicDegree(4)
    return texture

if __name__=='__main__':generate()
