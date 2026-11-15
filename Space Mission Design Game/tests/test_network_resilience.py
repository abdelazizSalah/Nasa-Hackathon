"""Join races, stalled game loops and slow sockets with actual TCP clients."""
import concurrent.futures
import queue
import threading
import time
import unittest
from game.network.lan import Server,Client,SnapshotQueue
from test_lan import receive

class NetworkResilienceTests(unittest.TestCase):
    def room(self):
        s=Server(('127.0.0.1',0),'112233');self.addCleanup(s.stop)
        host=self.client(s,'Host','engineer')
        receive(host,lambda d:d.get('kind')=='welcome')
        return s,host

    def client(self,server,name,role='operations'):
        c=Client(server.server_address,'112233',name,role);self.addCleanup(c.close);return c

    def test_snapshot_queue_keeps_latest_without_reordering_reliable_events(self):
        q=SnapshotQueue(8)
        q.put({'kind':'welcome'})
        for i in range(1000):q.put({'kind':'players','i':i})
        q.put({'kind':'notice'})
        q.put({'kind':'players','i':1000})
        self.assertEqual(q.qsize(),3)
        self.assertEqual([q.get()['kind'],q.get()['kind']],['welcome','notice'])
        self.assertEqual(q.get()['i'],1000)

    def test_simultaneous_join_for_two_three_and_four_players(self):
        for count in (2,3,4):
            with self.subTest(players=count):
                server,host=self.room()
                def join(i):
                    c=self.client(server,f'Friend {i}')
                    return c,receive(c,lambda d:d.get('kind')=='welcome')
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
                    guests=list(pool.map(join,range(count-1)))
                self.assertEqual(len({d['role'] for _,d in guests}),count-1)
                for c in [host]+[c for c,_ in guests]:
                    state=receive(c,lambda d:d.get('kind')=='state' and len(d['players'])==count)
                    self.assertEqual(len({(p['x'],p['z']) for p in state['players'].values()}),count)
                for c,_ in guests:c.close()
                host.close();server.stop()

    def test_four_player_pose_flood_survives_a_stalled_game_loop(self):
        server,host=self.room()
        guests=[self.client(server,str(i)) for i in range(3)]
        for c in guests:receive(c,lambda d:d.get('kind')=='welcome')
        # Deliberately do not consume any client's render-thread event queue.
        for i in range(360):
            host.send({'action':'pose','x':i%20/10,'z':-4,'yaw':i})
            time.sleep(.004)
        time.sleep(1.2)
        for c in [host]+guests:
            self.assertFalse(c.closed)
            self.assertLessEqual(c.events.qsize(),3)
        host.send({'action':'read','card':'purpose'})
        for c in guests:
            receive(c,lambda d:d.get('kind')=='state' and 'purpose' in d['cards'])

    def test_background_heartbeat_keeps_idle_players_connected(self):
        server,host=self.room();friend=self.client(server,'Idle friend')
        receive(friend,lambda d:d.get('kind')=='welcome')
        # Longer than the previous ten-second timeout; no pose or UI pump.
        time.sleep(11)
        self.assertFalse(host.closed);self.assertFalse(friend.closed)
        self.assertEqual(len(server.room.players),2)
        friend.send({'action':'read','card':'purpose'})
        receive(host,lambda d:d.get('kind')=='state' and 'purpose' in d['cards'])

    def test_slow_socket_does_not_block_other_players_or_the_room_lock(self):
        server,host=self.room();slow=self.client(server,'Slow');other=self.client(server,'Other')
        slow_role=receive(slow,lambda d:d.get('kind')=='welcome')['role']
        receive(other,lambda d:d.get('kind')=='welcome')
        entered=threading.Event();release=threading.Event()
        peer=server.room.peers[slow_role];original=peer.request
        class Gate:
            def sendall(self,data):entered.set();release.wait(5);return original.sendall(data)
            def __getattr__(self,name):return getattr(original,name)
        peer.request=Gate()
        try:
            host.send({'action':'pose','x':1,'z':-4,'yaw':0})
            self.assertTrue(entered.wait(2))
            host.send({'action':'read','card':'purpose'})
            receive(other,lambda d:d.get('kind')=='state' and 'purpose' in d['cards'],seconds=2)
        finally:release.set()

if __name__=='__main__':unittest.main()
