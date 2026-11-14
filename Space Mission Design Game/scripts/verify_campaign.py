"""Graphical end-to-end acceptance harness; writes QA frames to ignored runtime."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData, Filename
loadPrcFileData('', 'audio-library-name null')
from ursina import Ursina,application,window,color
from game.presentation.hub import Hub
from game.orbit.provider import trajectory
from game.domain.operations import simulate

app=Ursina(size=(1280,800),borderless=False,development_mode=False,editor_ui_enabled=False)
window.color=color.rgb32(6,12,25)
h=Hub(); h.open_library(); h.close_panel()
for _ in range(4): h.mission.campaign.advance(h.design_session,h.read_cards)
assert h.mission.campaign.stage==4
rows,source,meta=trajectory('regional',False)
r=simulate(h.design_session.catalog,h.design_session.design,rows)
r['provenance']=source; r['input_hash']=meta['input_hash']; r['plan']='targeted'
def shot(name):
    for _ in range(3): app.taskMgr.step(); app.graphicsEngine.render_frame()
    assert app.win.save_screenshot(Filename.from_os_specific(str(ROOT/'runtime'/name)))
h.mission.open(); shot('mission-tablet.png')
if '--live' in sys.argv:
    h.mission.mode='live'; h.mission.launch()
    h.mission.future.result(timeout=95)
    h.mission.tick(0)
    r=h.mission.flight['result']
    h.mission.finish_flight()
h.mission.start_flight(r); h.mission.tick(9); shot('orbit-view.png')
h.mission.finish_flight(); shot('mission-result.png')
assert h.mission.campaign.stage==5
h.close_panel(); h.design_session.choose('sensor','advanced'); h.design_changed()
assert h.mission.campaign.stage==1
print('PASS: campaign, cached trajectory, orbit scene, result, invalidation')
application.quit()
