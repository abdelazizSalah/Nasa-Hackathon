"""Real TCP authority checks for 1-4 players and spatial integration."""
import unittest
import time
from game.network.lan import Server,Client
from game.domain.assembly import PLAYER_IDS,CATEGORIES,owned
from game.domain.facility_layout import station_position,integration_target
from test_lan import receive

class FourPlayerTests(unittest.TestCase):
    def crew(self,n):
        server=Server(('127.0.0.1',0),'654321');self.addCleanup(server.stop)
        clients={}
        for i in range(n):
            c=Client(server.server_address,'654321',f'Player {i+1}','engineer' if i==0 else 'operations');self.addCleanup(c.close)
            welcome=receive(c,lambda d:d.get('kind')=='welcome');clients[welcome['role']]=c
        return server,clients
    def act(self,c,action,**fields):c.send({'action':action,**fields})
    def state(self,c,predicate):return receive(c,lambda d:d.get('kind')=='state' and predicate(d))

    def prepare(self,server,clients):
        self.act(clients['engineer'],'mission',mission='flood-watch')
        self.state(clients['engineer'],lambda d:d['assembly']['mission']=='flood-watch')
        for category in CATEGORIES:
            player=next(p for p in clients if category in owned(p,clients));c=clients[player]
            x,z=station_position(category,player,clients)
            self.act(c,'pose',x=x,z=z-1,yaw=0)
            self.act(c,'confirm',category=category)
            self.state(c,lambda d:category in d['assembly']['confirmed'])
            x,z=integration_target(category);self.act(c,'pose',x=x,z=z-1,yaw=0)
            self.act(c,'submit',category=category)
            self.state(c,lambda d:category in d['assembly']['submitted'])
        host=clients['engineer'];self.act(host,'pose',x=72,z=6.5,yaw=0);self.act(host,'validate')
        return self.state(host,lambda d:d['assembly']['ready'])

    def test_complete_for_every_count_and_consistent_snapshot(self):
        for n in range(1,5):
            with self.subTest(n=n):
                server,clients=self.crew(n);state=self.prepare(server,clients)
                self.assertEqual(state['stage'],4);self.assertEqual(len(state['assembly']['submitted']),5)
                for p,c in clients.items():
                    remote=self.state(c,lambda d:d['assembly']['ready']) if p!='engineer' else state
                    self.assertEqual(remote['assembly']['approved'],state['design'])
                pilot=next(p for p,rs in state['assembly']['assignments'].items() if 'flight' in rs)
                self.act(clients[pilot],'pose',x=76,z=6.5,yaw=0)
                self.act(clients[pilot],'launch')
                result=self.state(clients['engineer'],lambda d:d['result'] is not None)
                self.assertTrue(result['result']['passed'])
                for i,(p,c) in enumerate(clients.items()):
                    self.act(c,'finished',flight_id=result['flight_id'])
                    deadline=time.monotonic()+2
                    while p in server.room.awaiting and time.monotonic()<deadline:time.sleep(.01)
                    self.assertNotIn(p,server.room.awaiting)
                    if i<len(clients)-1:self.assertTrue(server.room.busy)
                self.state(clients['engineer'],lambda d:not d['busy'])

    def test_four_players_permissions_capacity_disconnect_and_rejoin(self):
        server,clients=self.crew(4);host=clients['engineer']
        extra=Client(server.server_address,'654321','Fifth','operations');self.addCleanup(extra.close)
        receive(extra,lambda d:d.get('kind')=='error' and 'full' in d['message'])
        self.act(clients['operations'],'choose',category='radio',option='fast')
        receive(clients['operations'],lambda d:d.get('kind')=='notice' and 'teammate' in d['message'])
        self.act(clients['crew3'],'choose',category='radio',option='fast')
        self.state(host,lambda d:d['design']['radio']=='fast')
        clients['crew3'].close()
        state=self.state(host,lambda d:len(d['players'])==3)
        self.assertEqual(state['design']['radio'],'fast');self.assertEqual(state['assembly']['assignments']['operations'],['communications'])
        rejoin=Client(server.server_address,'654321','Returned','operations');self.addCleanup(rejoin.close)
        self.assertEqual(receive(rejoin,lambda d:d.get('kind')=='welcome')['role'],'crew3')
        self.state(rejoin,lambda d:d['design']['radio']=='fast' and len(d['players'])==4)

    def test_proximity_missing_parts_and_remote_movement(self):
        server,clients=self.crew(2);host=clients['engineer'];friend=clients['operations']
        self.act(friend,'mission',mission='flood-watch');receive(friend,lambda d:d.get('kind')=='notice' and 'host' in d['message'])
        self.act(host,'mission',mission='coming-soon');receive(host,lambda d:d.get('kind')=='notice' and 'unavailable' in d['message'])
        self.act(host,'confirm',category='sensor');receive(host,lambda d:d.get('kind')=='notice' and 'Approach' in d['message'])
        self.act(friend,'pose',x=76,z=6.5,yaw=90,y=.7,crouch=True)
        data=receive(host,lambda d:d.get('kind')=='players' and d['players']['operations'].get('y')==.7)
        self.assertTrue(data['players']['operations']['crouch'])
        self.act(friend,'launch');receive(friend,lambda d:d.get('kind')=='notice' and 'integration' in d['message'])

    def test_one_player_authoritative_launch_and_acknowledgement(self):
        server,clients=self.crew(1);host=clients['engineer'];self.prepare(server,clients)
        self.act(host,'pose',x=76,z=6.5,yaw=0);self.act(host,'launch')
        result=self.state(host,lambda d:d['result'] is not None)
        self.assertTrue(result['result']['passed'])
        self.act(host,'finished',flight_id=result['flight_id']);self.state(host,lambda d:not d['busy'])
