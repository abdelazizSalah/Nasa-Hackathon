"""Graphical design-console integration checks; --review leaves a panel for visual inspection."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review',action='store_true')
    parser.add_argument('--failing',action='store_true',help='Leave the sensor-only upgrade for visual inspection')
    args=parser.parse_args()
    from panda3d.core import loadPrcFileData
    loadPrcFileData('', 'audio-library-name null\nnotify-level-device error')
    from ursina import Ursina,application,window,color,held_keys,time
    from game.presentation.hub import Hub
    from game.domain.navigation import Pose
    app=Ursina(title='Mission Forge | Design Review',size=(1280,800),borderless=False,
               development_mode=False,editor_ui_enabled=False)
    window.color=color.rgb32(6,12,25)
    window.fps_counter.enabled=False
    window.exit_button.enabled=False
    hub=Hub()
    checks=[]
    def check(condition,name):
        if not condition: raise AssertionError(name)
        checks.append(name)
    hub.pose=Pose(4.2,-1.6,0)
    hub.handle_input('e')
    check(hub.modal=='directory','E opens the new physical-workshop directory')
    hub.close_panel();hub.open_design()
    session=hub.design_session
    check(session.preview.passed,'Default configuration passes preview')
    hub.handle_input('right arrow')
    check({c.code for c in session.preview.failures}=={'power','delivery'},'Keyboard sensor upgrade exposes power and data constraints')
    check(hub.spacecraft.sensor.scale_x>.5 and hub.design_panel.model.sensor.scale_x>.5,'World and panel sensors update together')
    hub.handle_input('down arrow')
    hub.handle_input('right arrow')
    check('mass' in {c.code for c in session.preview.failures},'Bigger power package shifts limiting factor to mass')
    check(hub.spacecraft.arrays[0][1].scale_x>1,'Solar panel geometry grows with power choice')
    hub.design_panel.choose('launcher','heavy',4)
    check({c.code for c in session.preview.failures}=={'delivery'},'Heavier launcher fixes mass without hiding data limit')
    hub.design_panel.choose('radio','fast',2)
    check(session.preview.passed,'Fast radio completes a feasible advanced design')
    expected=session.preview
    pose=hub.pose
    held_keys['up arrow']=held_keys['right arrow']=1
    for _ in range(10): hub.tick(.05)
    held_keys['up arrow']=held_keys['right arrow']=0
    check(hub.pose==pose and session.preview==expected,'Design panel freezes navigation and animation does not change totals')
    hub.handle_input('u')
    check(not session.preview.passed and session.design.radio=='standard','Undo restores radio choice and its data failure')
    hub.handle_input('right arrow')
    check(session.preview==expected,'Reselecting fast radio restores all totals')
    hub.handle_input('backspace')
    check(session.design.sensor=='basic' and session.preview.passed,'Reset restores feasible default design')
    hub.handle_input('u')
    check(session.preview==expected,'Undo can reverse reset')
    hub.handle_input('escape')
    hub.open_design()
    check(hub.modal=='design' and session.preview==expected,'Closing and reopening keeps session design')
    if args.failing:
        hub.design_panel.reset()
        hub.design_panel.choose('sensor','advanced',0)
    report={'status':'passed','checks':checks,'method':'scripted graphical integration, not user acceptance',
            'design':asdict(session.design),'preview_values':session.preview.values,
            'displayed_checks_pass':session.preview.passed}
    output=ROOT/'runtime/design-verification.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(f'PASS: {len(checks)} design integration checks. Evidence: {output}',flush=True)
    elapsed=[0.]
    def update():
        hub.tick(time.dt)
        elapsed[0]+=time.dt
        if not args.review and elapsed[0]>1: application.quit()
    sys.modules['__main__'].update=update
    sys.modules['__main__'].input=hub.handle_input
    app.run()


if __name__=='__main__': main()
