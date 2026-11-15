"""Shared progress and explicit next destination, independent of rendering."""
from game.domain.assembly import CATEGORIES,owned,ROLES
from game.domain.facility_layout import station_position,integration_target

NAMES={'sensor':'Payload Camera','power':'Power Package','radio':'Communications','orbit':'Orbit Plan','launcher':'Launcher','fuel':'Launch Fuel'}
ROOM_NAMES={'sensor':'Payload / cyan room','power':'Power / amber room','radio':'Communications / violet room',
            'orbit':'Mission Planning / blue room','launcher':'Mission Planning / blue room','fuel':'Mission Planning / blue room'}

def next_step(state,session,players,complete=False):
    def step(action,label,target,owner=None):
        name=players.get(owner,{}).get('name',owner or 'Host')
        return {'action':action,'label':label,'target':target,'owner':owner,'responsible':name}
    if complete:return step('MISSION COMPLETE','Delivered useful observations',(76,6.5))
    if not state['mission']:return step('SELECT MISSION','Earth display / Spawn Room',(-5.55,-1.8),'engineer')
    for c in CATEGORIES:
        owner=next((p for p in players if c in owned(p,players)),None)
        if c not in state['confirmed']:
            return step('PICK '+NAMES[c],ROOM_NAMES[c],station_position(c,owner,players),owner)
    for c in CATEGORIES:
        if c not in state['submitted']:
            owner=next((p for p in players if c in owned(p,players)),None)
            return step('PLACE '+NAMES[c],'Integration / marked '+NAMES[c]+' slot',integration_target(c),owner)
    if state['issues']:
        issue=state['issues'][0]
        category={'quality':'sensor','budget':'sensor','mass':'launcher','orbit':'launcher','power':'power',
                  'energy':'power','storage':'radio','delivery':'radio'}[issue['code']]
        owner=next((p for p in players if category in owned(p,players)),None)
        return step('FIX '+issue['label'],ROOM_NAMES[category]+' / red screen explains the trade-off',station_position(category,owner,players),owner)
    if not state['ready']:return step('HOST: APPROVE READINESS','Integration / gold approval console or M',(68,9.8),'engineer')
    pilot=next((p for p in players if 'orbit' in owned(p,players)),None)
    return step('LAUNCH NOW','M / Mission Control or Launch desk',(76,6.5),pilot)

def progress_text(state,complete=False):
    done=int(bool(state['mission']))+len(state['confirmed'])+len(state['submitted'])+int(state['ready'])+int(complete)
    return f"PROGRESS {done}/15 | Picked {len(state['confirmed'])}/6 | Placed {len(state['submitted'])}/6 | Approval: "+('DONE' if state['ready'] else 'WAIT')
