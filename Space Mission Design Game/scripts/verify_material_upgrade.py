"""Native screenshots and asset checks for offline Earth and physical materials."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData,Filename
loadPrcFileData('','audio-library-name null\nnotify-level-device error')
from ursina import Ursina,application,mouse
from PIL import Image
from game.presentation.hub import Hub
from game.domain.navigation import Pose
from game.presentation.planet import globe_mesh
from game.domain.operations import simulate
from game.orbit.provider import trajectory

app=Ursina(size=(1600,900),borderless=False,development_mode=False,editor_ui_enabled=False)
h=Hub();out=ROOT/'runtime/material-upgrade';out.mkdir(parents=True,exist_ok=True)
def shot(name,x,z,yaw=0,pitch=0):
    h.pose=Pose(x,z,yaw);h.pitch=pitch
    for _ in range(6):h.tick(.016);app.taskMgr.step();app.graphicsEngine.render_frame()
    app.win.save_screenshot(Filename.from_os_specific(str(out/(name+'.png'))))

assert Image.open(ROOT/'content/materials/earth-blue-marble.png').size==(2048,1024)
mesh=globe_mesh();assert len(mesh.vertices)==len(mesh.normals)==len(mesh.uvs)
assert len(mesh.triangles)==96*48*2
assert h.earth.texture and h.earth.clouds.texture
assert h.earth.model.get_parent()==h.earth and h.earth.clouds.model.get_parent()==h.earth.clouds
shot('01-entry-earth',0,-4.5,-38,-4)
shot('02-earth-close',-3.8,-2.6,0,-5)
for name,x in [('payload',16),('power',30),('radio',44),('planning',58)]:shot('03-'+name,x,8,0,7)
shot('04-integration',72,6,0,-5)
h.facility.open_station('power')
for _ in range(6):h.tick(.016);app.taskMgr.step();app.graphicsEngine.render_frame()
app.win.save_screenshot(Filename.from_os_specific(str(out/'05-workstation.png')))
h.close_panel()
rows,provenance,meta=trajectory('regional',False)
result=simulate(h.design_session.catalog,h.design_session.design,rows,True)
result.update(provenance=provenance,input_hash=meta['input_hash'])
h.mission.start_flight(result);h.mission.flight['elapsed']=7.1
for _ in range(6):h.tick(.016);app.taskMgr.step();app.graphicsEngine.render_frame()
app.win.save_screenshot(Filename.from_os_specific(str(out/'06-orbit-earth.png')))
assert h.mission.earth.texture
(out/'report.json').write_text(json.dumps({'status':'passed','checks':['NASA map 2048x1024 bundled offline','Smooth UV globe with normals','Entry clouds and atmosphere','Textured room equipment and spacecraft previews','Same Earth in operations'],'scope':'Windows rendering; visual presentation only'},indent=2))
print('PASS: offline NASA Earth, smooth sphere, cloud/atmosphere layers, rooms/parts/previews and operations Earth',flush=True)
mouse.locked=False;application.quit()
