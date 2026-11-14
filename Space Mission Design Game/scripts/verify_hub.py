"""Explicit graphical integration check. --review leaves the card panel open for inspection."""
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review',action='store_true')
    args=parser.parse_args()
    from panda3d.core import loadPrcFileData
    loadPrcFileData('', 'audio-library-name null\nnotify-level-device error')
    from ursina import Ursina,held_keys,application,window,color
    from game.presentation.hub import Hub
    app=Ursina(title='Mission Forge | Phase 2 Review',size=(1280,800),borderless=False,
               development_mode=False,editor_ui_enabled=False)
    window.color=color.rgb32(6,12,25)
    window.fps_counter.enabled=False
    window.exit_button.enabled=False
    hub=Hub()
    checks=[]
    def check(condition,name):
        if not condition: raise AssertionError(name)
        checks.append(name)
    def walk(direction,frames):
        held_keys['up arrow']=int(direction>0)
        held_keys['down arrow']=int(direction<0)
        for _ in range(frames): hub.tick(.05)
        held_keys['up arrow']=0
        held_keys['down arrow']=0

    walk(1,110)
    check(4.4<hub.pose.z<4.61,'Closed door blocks walking')
    hub.handle_input('e')
    for _ in range(16): hub.tick(.05)
    check(hub.door_open and hub.door_progress>.98,'E opens sliding Lab door')
    walk(1,40)
    check(hub.pose.z>9,'Player can enter Lab')
    hub.handle_input('e')
    check(hub.modal=='learning','E opens card library')
    before=hub.pose
    held_keys['up arrow']=1
    held_keys['right arrow']=1
    for _ in range(12): hub.tick(.05)
    held_keys['up arrow']=held_keys['right arrow']=0
    check(hub.pose==before,'Reading freezes position and camera heading')
    for _ in range(9): hub.handle_input('down arrow')
    check(len(hub.read_cards)==10,'Keyboard can select all ten cards')
    hub.handle_input('escape')
    check(hub.modal is None,'Escape closes card panel')
    walk(-1,2)
    check(hub.pose.z<before.z,'Movement resumes after reading')
    hub.handle_input('escape')
    check(hub.modal=='pause','Escape pauses exploration')
    hub.handle_input('enter')
    check(hub.modal is None,'Enter resumes exploration')
    # Walk back into the doorway, face south, and verify the leaf cannot close on the player.
    from game.domain.navigation import Pose
    hub.pose=Pose(0,5,180)
    hub.handle_input('e')
    check(hub.door_open and 'Step clear' in hub.notice,'Door refuses to close on player in opening')
    hub.pose=Pose(0,8.8,0)
    hub.open_library()
    hub.select_card(0)
    output=ROOT/'runtime/hub-verification.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps({'status':'passed','checks':checks,'method':'graphical integration harness; scripted actions, not user acceptance',**hub.evidence()},indent=2),encoding='utf-8')
    print(f'PASS: {len(checks)} hub integration checks. Evidence: {output}',flush=True)
    frames=[0]
    def update():
        hub.tick(1/60)
        frames[0]+=1
        if not args.review and frames[0]>30: application.quit()
    sys.modules['__main__'].update=update
    sys.modules['__main__'].input=hub.handle_input
    app.run()


if __name__=='__main__': main()
