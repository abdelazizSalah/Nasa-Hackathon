"""Real-socket graphical crew harness; LAN-only loopback, no firewall changes."""
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData,Filename
loadPrcFileData('', 'audio-library-name null')
from ursina import Ursina,application
from game.presentation.hub import Hub
from game.network.lan import Server,Client

app=Ursina(size=(1280,800),borderless=False,development_mode=False,editor_ui_enabled=False)
h=Hub(); h.network.open()
def shot(name):
    for _ in range(3):app.taskMgr.step();app.graphicsEngine.render_frame()
    assert app.win.save_screenshot(Filename.from_os_specific(str(ROOT/'runtime'/name)))
shot('crew-lobby.png');h.close_panel()
server=Server(('127.0.0.1',0),'123456')
friend=None
try:
    net=h.network;net.server=server;net.port=server.server_address[1];net.code=server.room.code
    net.client=Client(server.server_address,'123456','Host','engineer')
    friend=Client(server.server_address,'123456','Friend','operations')
    def pump():
        import queue
        for i in range(40):
            if i%10==0 and not friend.closed:friend.send({'action':'pose','x':0,'z':-.8,'yaw':180,'task':'Mission control'})
            h.tick(.025);app.taskMgr.step();time.sleep(.01)
            while True:
                try:friend.events.get_nowait()
                except queue.Empty:break
    def wait_for(condition):
        deadline=time.monotonic()+6
        while not condition() and time.monotonic()<deadline:pump()
        assert condition(),'Timed out during shared crew flow'
    pump()
    assert net.role=='engineer' and 'operations' in net.avatars
    shot('crew-avatar.png')
    h.open_design();h.design_panel.choose('sensor','advanced',0)
    friend.send({'action':'choose','category':'radio','option':'fast'})
    pump()
    assert h.design_session.design.sensor=='advanced' and h.design_session.design.radio=='fast'
    shot('crew-design.png')
    net.send('choose',category='power',option='extended')
    net.send('choose',category='launcher',option='heavy')
    wait_for(lambda:h.design_session.preview.passed)
    friend.send({'action':'read','card':'purpose'})
    wait_for(lambda:'purpose' in h.read_cards)
    for role,stage in [('operations',1),('engineer',2),('operations',3),('engineer',4)]:
        if role=='operations':friend.send({'action':'advance'})
        else:h.mission.advance()
        wait_for(lambda:h.mission.campaign.stage==stage)
    friend.send({'action':'launch'})
    wait_for(lambda:h.mission.flight is not None)
    assert h.mission.flight['result']['passed']
    h.mission.finish_flight()
    friend.send({'action':'finished','flight_id':net.seen_flight})
    wait_for(lambda:not net.busy)
    assert h.mission.campaign.stage==5
    shot('crew-result.png')
    h.close_panel();net.open();shot('crew-connected.png')
    friend.close();pump();assert not net.avatars
    import json
    (ROOT/'runtime/crew-verification.json').write_text(json.dumps({
        'status':'passed','transport':'real TCP / 127.0.0.1 / two clients',
        'checks':['lobby render','named remote avatar','role-scoped concurrent edits','shared design model',
                  'role-specific campaign gates','shared launch and report','both finish acknowledgements','disconnect removes avatar'],
        'limitations':'One graphical host and a second protocol client on one Windows laptop; physical Wi-Fi and Arch not tested.'
    },indent=2))
    print('PASS: lobby, avatar, concurrent edits, shared mission/launch/report, finish acknowledgements and disconnect cleanup')
finally:
    if friend:friend.close()
    if h.network.client:h.network.client.close()
    server.stop()
application.quit()
