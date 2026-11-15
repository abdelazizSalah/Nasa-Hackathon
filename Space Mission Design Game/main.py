"""Mission Forge: walkable hub and spacecraft design. --engine-check retains the renderer proof."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import platform
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smoke-seconds',type=float,default=0,help='Auto-close after rendering; 0 stays open')
    parser.add_argument('--engine-check',action='store_true',help='Run the original Phase 1 renderer scene')
    args=parser.parse_args()
    if args.smoke_seconds<0: parser.error('--smoke-seconds must be non-negative')
    from panda3d.core import loadPrcFileData
    loadPrcFileData('', 'audio-library-name null\nnotify-level-device error')
    from ursina import Ursina, color, application, time, window, held_keys
    root=Path(__file__).resolve().parent
    runtime=root/'runtime'
    runtime.mkdir(exist_ok=True)
    evidence_path=runtime/'graphics-smoke.json'
    evidence_path.unlink(missing_ok=True)
    app=Ursina(title='Mission Forge | '+('Engine Check' if args.engine_check else 'Mission Design'),
               size=(1280,800),borderless=False,development_mode=False,editor_ui_enabled=False)
    window.color=color.rgb32(6,12,25)
    window.fps_counter.enabled=False
    window.exit_button.enabled=False
    if args.engine_check:
        from game.presentation.engine_check import EngineCheck
        experience=EngineCheck()
    else:
        from game.presentation.hub import Hub
        experience=Hub()
        experience.show_spawn_instructions()
    state={'elapsed':0.,'frames':0}
    def update():
        state['elapsed']+=time.dt
        state['frames']+=1
        focused=app.win.get_properties().get_foreground()
        if hasattr(experience,'focused') and experience.focused != focused:
            from ursina import mouse
            experience.focused=focused
            mouse.locked=False
        if not focused:
            held_keys.clear()
        experience.tick(time.dt)
        if args.smoke_seconds and state['elapsed']>=args.smoke_seconds: application.quit()
    sys.modules['__main__'].update=update
    sys.modules['__main__'].input=experience.handle_input
    def finish():
        if hasattr(experience,'network'):
            if experience.network.client:experience.network.client.close()
            if experience.network.server:experience.network.server.stop()
        if state['frames']<2: return
        gsg=app.win.get_gsg()
        evidence_path.write_text(json.dumps({
            'utc':datetime.now(timezone.utc).isoformat(),'os':platform.platform(),
            'python':platform.python_version(),'ursina':version('ursina'),
            'renderer':gsg.get_driver_renderer(),'vendor':gsg.get_driver_vendor(),
            'frames':state['frames'],'elapsed_seconds':state['elapsed'],
            'status':'rendered','user_acceptance':'pending',**experience.evidence(),
        },indent=2),encoding='utf-8')
    try: app.run()
    except SystemExit:
        finish()
        raise
    else: finish()


if __name__=='__main__': main()
