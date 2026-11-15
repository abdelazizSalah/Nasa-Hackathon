"""Opt-in executable acceptance check: offline assets, cached science and real LAN."""
import json
import queue
import time
from game.paths import ROOT,RUNTIME
from game.domain.design import DesignSession
from game.domain.assembly import CATEGORIES,owned
from game.domain.facility_layout import station_position,integration_target
from game.domain.operations import simulate
from game.orbit.provider import trajectory
from game.network.lan import Server,Client,fingerprint
from game.library.content import load_library

def verify():
    checks=[]
    def receive(client,predicate):
        deadline=time.monotonic()+8
        while time.monotonic()<deadline:
            try:data=client.events.get(timeout=.1)
            except queue.Empty:continue
            if data.get('kind')=='error':raise RuntimeError(data['message'])
            if predicate(data):return data
        raise RuntimeError('Packaged LAN verification timed out')
    def state(client,predicate):return receive(client,lambda d:d.get('kind')=='state' and predicate(d))
    books,_=load_library();assert len(books)==12
    assert (ROOT/'content/materials/earth-blue-marble.png').is_file()
    checks.append('Bundled library and NASA imagery')
    session=DesignSession();rows,_,_=trajectory('regional',False)
    result=simulate(session.catalog,session.design,rows,True)
    assert result['passed'] and result['delivered_mb']==120
    checks.append('Cached GMAT / Targeted delivers 120 MB without GMAT installed')
    for count in (2,3,4):
        server=Server(('127.0.0.1',0),'456789');clients={}
        try:
            for i in range(count):
                client=Client(server.server_address,'456789',f'Packaged {i+1}','engineer' if i==0 else 'operations')
                role=receive(client,lambda d:d.get('kind')=='welcome')['role'];clients[role]=client
            host=clients['engineer'];host.send({'action':'mission','mission':'flood-watch'})
            state(host,lambda d:d['assembly']['mission']=='flood-watch')
            for cat in CATEGORIES:
                role=next(p for p in clients if cat in owned(p,clients));client=clients[role]
                x,z=station_position(cat)
                client.send({'action':'pose','x':x,'z':z-1,'yaw':0})
                client.send({'action':'collect','category':cat,'option':getattr(session.design,cat)})
                state(client,lambda d:cat in d['assembly']['confirmed'])
                x,z=integration_target(cat);client.send({'action':'pose','x':x,'z':z-1,'yaw':0})
                client.send({'action':'submit','category':cat})
                state(client,lambda d:cat in d['assembly']['submitted'])
            host.send({'action':'validate'});state(host,lambda d:d['assembly']['ready'])
            host.send({'action':'launch'});result=state(host,lambda d:d['result'] is not None)
            assert result['result']['passed']
            for client in clients.values():
                seen=state(client,lambda d:d['result'] is not None) if client is not host else result
                assert seen['result']['delivered_mb']==120
                client.send({'action':'finished','flight_id':result['flight_id']})
            state(host,lambda d:not d['busy'])
            checks.append(f'{count}-player real TCP join, six contributions, approval, successful launch and all finish acknowledgements')
        finally:
            for client in clients.values():client.close()
            server.stop()
    report={'status':'passed','checks':checks,'fingerprint':fingerprint()}
    (RUNTIME/'package-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report
