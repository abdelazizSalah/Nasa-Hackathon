"""One graphical host + three real TCP clients; no remote laptop claim."""
import sys
import time
import json
import queue
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData,Filename
loadPrcFileData('','audio-library-name null\nnotify-level-device error')
from ursina import Ursina,application,window,color
from game.presentation.hub import Hub
from game.network.lan import Server,Client
from game.domain.assembly import CATEGORIES,owned
from game.domain.facility_layout import station_position,integration_target
from game.domain.navigation import Pose

app=Ursina(size=(1440,900),borderless=False,development_mode=False,editor_ui_enabled=False)
window.color=color.rgb32(6,12,25);h=Hub();net=h.network
out=ROOT/'runtime/facility-review';out.mkdir(parents=True,exist_ok=True)
server=Server(('127.0.0.1',0),'246810');clients={};poses={};checks=[]
def pump():
    h.tick(.025);app.taskMgr.step();time.sleep(.01)
    for p,c in clients.items():
        c.send({'action':'pose',**poses[p]})
        while True:
            try:c.events.get_nowait()
            except queue.Empty:break
def wait(test):
    deadline=time.monotonic()+8
    while not test() and time.monotonic()<deadline:pump()
    assert test(),'Timed out waiting for shared state'
def send(player,action,**fields):
    if player=='engineer':net.send(action,**fields)
    else:clients[player].send({'action':action,**fields})
def move(player,x,z,**extra):
    fields={'x':x,'z':z,'yaw':0,**extra}
    if player=='engineer':h.pose=Pose(x,z,0)
    else:poses[player]=fields
    send(player,'pose',**fields)
def shot(name):
    for _ in range(4):pump();app.graphicsEngine.render_frame()
    assert app.win.save_screenshot(Filename.from_os_specific(str(out/f'{name}.png')))
try:
    net.server=server;net.code=server.room.code;net.port=server.server_address[1]
    net.client=Client(server.server_address,net.code,'Host','engineer')
    wait(lambda:net.role=='engineer')
    net.open()
    for i,p in enumerate(('operations','crew3','crew4')):
        clients[p]=Client(server.server_address,net.code,f'Crew {i+2}','operations')
        poses[p]={'x':i,'z':-.8,'yaw':180}
        wait(lambda:p in net.players)
        assert h.modal=='crew'
        def texts(root):
            return '\n'.join(str(getattr(c,'text',''))+'\n'+texts(c) for c in root.children)
        assert f'Crew {i+2}' in texts(h.panel),'Open lobby must refresh its roster after every join'
        shot(f'join-{i+2}-players')
    assert len(net.players)==4 and all(len(r)==1 for r in h.facility.state['assignments'].values())
    net.open();shot('13-four-player-lobby');h.close_panel();checks.append('two/three/four-player joins visibly update the open lobby; four unique roles')
    net.send('mission',mission='flood-watch');wait(lambda:h.facility.state['mission']=='flood-watch')
    for category in CATEGORIES:
        owner=next(p for p in net.players if category in owned(p,net.players))
        x,z=station_position(category,owner,net.players);move(owner,x,z-1)
        send(owner,'collect',category=category,option=getattr(h.design_session.design,category));wait(lambda:category in h.facility.state['confirmed'])
    h.facility.open_station('sensor','engineer')
    x,z=station_position('power','operations',net.players);move('operations',x,z-1)
    send('operations','collect',category='power',option='extended')
    wait(lambda:h.design_session.design.power=='extended')
    assert h.facility.preview.arrays[0][1].scale_x>1
    shot('17-live-observer-preview');h.close_panel()
    checks.append('teammate selection updates an already-open rotating workstation preview')
    wait(lambda:len(net.avatars)==3)
    for i,p in enumerate(clients):move(p,70+i*2,7,y=.6 if i==0 else 0,crouch=i==1)
    move('engineer',72,3.9);h._sync_camera()
    for _ in range(12):pump()
    shot('14-remote-carried-parts')
    assert all(getattr(a,'held_part',None) for a in net.avatars.values())
    assert all(len(a.held_parts)==len(h.facility.state['inventory'][p]) for p,a in net.avatars.items())
    checks.append('three remote avatars carry actual selections; jump/crouch pose shown')
    for category in CATEGORIES:
        owner=next(p for p in net.players if category in owned(p,net.players))
        x,z=integration_target(category);move(owner,x,z-1);send(owner,'submit',category=category)
        wait(lambda:category in h.facility.state['submitted'])
    move('engineer',72,6.5);net.send('validate');wait(lambda:h.facility.state['ready'])
    h.facility.open_validation();shot('15-four-player-approved');h.close_panel()
    checks.append('all role contributions submitted and host approval synchronized')
    # Revision preserves unrelated submissions and removes exactly the changed payload.
    net.send('choose',category='sensor',option='advanced')
    wait(lambda:not h.facility.state['ready'] and 'sensor' not in h.facility.state['submitted'])
    assert len(h.facility.state['submitted'])==len(CATEGORIES)-1
    checks.append('selection changes invalidate approval and only affected submission')
    # Disconnect while integration is incomplete; surviving crew retain all choices.
    clients['crew3'].close();clients.pop('crew3');poses.pop('crew3')
    wait(lambda:len(net.players)==3)
    assert h.facility.state['assignments']['operations']==['communications']
    assert h.design_session.design.sensor=='advanced'
    shot('16-three-player-redistribution');checks.append('disconnect redistributes roles without losing selections')
    # A rejected graphical join must replace Connecting with the actual reason.
    clients['crew3']=Client(server.server_address,net.code,'Replacement','operations')
    poses['crew3']={'x':0,'z':-.8,'yaw':0};wait(lambda:len(net.players)==4)
    if h.panel:h.close_panel()
    net.client.close();net.client=None;net.role=None;net.players={}
    net.join('127.0.0.1','000000','Wrong code')
    wait(lambda:net.client.closed and 'Incorrect room code' in net.message)
    assert 'Incorrect room code' in texts(h.panel),'Join error must be visible in the lobby'
    shot('18-visible-join-error');checks.append('rejected join visibly explains Incorrect room code instead of staying Connecting')
    (out/'four-player-report.json').write_text(json.dumps({'status':'passed','checks':checks,'transport':'four real localhost TCP clients; one graphical window',
        'limitations':'Separate laptops, Wi-Fi firewall and Arch Linux remain manual acceptance.'},indent=2))
    print('PASS:',', '.join(checks),flush=True)
finally:
    for c in clients.values():c.close()
    if net.client:net.client.close()
    server.stop()
application.quit()
