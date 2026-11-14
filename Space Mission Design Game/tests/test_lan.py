"""Real loopback TCP tests for shared state, permissions, presence and launch."""
import sys
from pathlib import Path
import queue
import time
import unittest
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from game.network.lan import Server,Client


def receive(client,predicate,seconds=5):
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline:
        try:data=client.events.get(timeout=.1)
        except queue.Empty:continue
        if predicate(data):return data
    raise AssertionError('Timed out waiting for expected network message')

class LANTests(unittest.TestCase):
    def setUp(self):
        self.server=Server(('127.0.0.1',0),'123456')
        self.addCleanup(self.server.stop)
        self.a=Client(self.server.server_address,'123456','Host','engineer')
        self.b=Client(self.server.server_address,'123456','Friend','operations')
        self.addCleanup(self.a.close);self.addCleanup(self.b.close)
        receive(self.a,lambda d:d.get('kind')=='welcome')
        receive(self.b,lambda d:d.get('kind')=='welcome')
    def send(self,client,action,**values):client.send({'action':action,**values})
    def state(self,client,predicate):return receive(client,lambda d:d.get('kind')=='state' and predicate(d))

    def test_simultaneous_subsystem_edits_survive_and_are_shared(self):
        self.send(self.a,'choose',category='sensor',option='advanced')
        self.send(self.b,'choose',category='radio',option='fast')
        state=self.state(self.b,lambda d:d['design']['sensor']=='advanced' and d['design']['radio']=='fast')
        self.assertEqual(state['design']['power'],'compact')
        self.send(self.a,'undo')
        state=self.state(self.b,lambda d:d['design']['sensor']=='basic' and d['design']['radio']=='fast')
        self.assertEqual(state['stage'],0)

    def test_permissions_and_invalid_inputs_rejected_by_host(self):
        self.send(self.b,'choose',category='power',option='extended')
        receive(self.b,lambda d:d.get('kind')=='notice' and 'teammate' in d['message'])
        self.assertEqual(self.server.room.session.design.power,'compact')
        self.send(self.a,'pose',x=10000,z=0,yaw=0)
        receive(self.a,lambda d:d.get('kind')=='notice' and 'pose' in d['message'])
        self.send(self.a,'choose',category='power',option='INVALID')
        receive(self.a,lambda d:d.get('kind')=='notice')
        self.assertEqual(self.server.room.session.design.power,'compact')

    def test_avatar_pose_task_and_disconnect_presence(self):
        self.send(self.b,'pose',x=2,z=3,yaw=90,task='Learning')
        data=receive(self.a,lambda d:d.get('kind')=='players' and d['players'].get('operations',{}).get('x')==2)
        self.assertEqual(data['players']['operations']['task'],'Learning')
        self.b.close()
        receive(self.a,lambda d:d.get('kind')=='players' and 'operations' not in d['players'])

    def test_shared_gates_launch_and_both_finish_acknowledgements(self):
        self.send(self.b,'read',card='purpose')
        self.state(self.a,lambda d:'purpose' in d['cards'])
        for client,stage in ((self.b,1),(self.a,2),(self.b,3)):
            self.send(client,'advance');self.state(client,lambda d:d['stage']==stage)
        # Physical integration is now required in addition to the original campaign gates.
        from game.domain.assembly import CATEGORIES,owned
        from game.domain.facility_layout import station_position,integration_target
        players=('engineer','operations')
        self.send(self.a,'mission',mission='flood-watch')
        for category in CATEGORIES:
            player=next(p for p in players if category in owned(p,players))
            client=self.a if player=='engineer' else self.b
            x,z=station_position(category,player,players)
            self.send(client,'pose',x=x,z=z-1,yaw=0)
            self.send(client,'confirm',category=category)
            self.state(client,lambda d:category in d['assembly']['confirmed'])
            x,z=integration_target(category)
            self.send(client,'pose',x=x,z=z-1,yaw=0)
            self.send(client,'submit',category=category)
            self.state(client,lambda d:category in d['assembly']['submitted'])
        self.send(self.a,'pose',x=72,z=6.5,yaw=0)
        self.send(self.a,'validate');self.state(self.a,lambda d:d['stage']==4)
        self.send(self.b,'pose',x=76,z=6.5,yaw=0)
        self.send(self.b,'launch')
        data=self.state(self.a,lambda d:d['result'] is not None)
        self.assertTrue(data['result']['passed']);self.assertTrue(data['busy'])
        self.send(self.a,'finished',flight_id=data['flight_id'])
        self.send(self.b,'finished',flight_id=data['flight_id'])
        self.state(self.a,lambda d:not d['busy'])
        self.send(self.a,'choose',category='sensor',option='advanced')
        state=self.state(self.b,lambda d:d['stage']==1)
        self.assertIsNone(state['approved'])

    def test_wrong_room_code_cannot_join(self):
        third=Client(self.server.server_address,'000000','Wrong','operations');self.addCleanup(third.close)
        receive(third,lambda d:d.get('kind')=='error' and 'code' in d['message'])

    def test_shared_door_protects_either_player(self):
        self.send(self.a,'door');self.state(self.b,lambda d:d['door_open'])
        self.send(self.b,'pose',x=0,z=5,yaw=180,task='Exploring')
        receive(self.a,lambda d:d.get('kind')=='players' and d['players'].get('operations',{}).get('z')==5)
        self.send(self.a,'door')
        receive(self.a,lambda d:d.get('kind')=='notice' and 'doorway' in d['message'])
        self.assertTrue(self.server.room.door_open)

    def test_shared_save_restores_plan_and_design_and_is_host_only(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'crew.json';self.server.room.save_path=path
            self.send(self.b,'plan');self.state(self.a,lambda d:not d['targeted'])
            self.send(self.a,'choose',category='power',option='extended')
            self.state(self.a,lambda d:d['design']['power']=='extended')
            self.send(self.b,'save')
            receive(self.b,lambda d:d.get('kind')=='notice' and 'host manages' in d['message'])
            self.send(self.a,'save')
            receive(self.a,lambda d:d.get('kind')=='notice' and 'saved' in d['message'])
            self.assertTrue(path.exists())
            self.send(self.a,'new');reset=self.state(self.a,lambda d:d['design']['power']=='compact')
            self.send(self.a,'load')
            receive(self.a,lambda d:d.get('kind')=='notice' and 'restored' in d['message'])
            restored=self.state(self.b,lambda d:d['revision']>reset['revision'] and d['design']['power']=='extended')
            self.assertFalse(restored['targeted'])

if __name__=='__main__':unittest.main()
