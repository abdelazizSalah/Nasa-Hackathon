"""Cooperative workflow only. Engineering equations remain in domain.design."""
from dataclasses import asdict
import json
from pathlib import Path

ROLES={
    'science':('Science & Payload',('sensor',)),
    'power':('Power & Spacecraft Systems',('power',)),
    'communications':('Communications & Data',('radio',)),
    'flight':('Mission & Flight Dynamics',('orbit','launcher','fuel')),
}
CATEGORIES=tuple(c for _,categories in ROLES.values() for c in categories)
PLAYER_IDS=('engineer','operations','crew3','crew4')

from game.domain.economy import missions, mission_definition

def assignments(players):
    ordered=[p for p in PLAYER_IDS if p in players]
    if not ordered:return {}
    count=len(ordered);roles=list(ROLES);result={};offset=0
    for i,player in enumerate(ordered):
        size=4//count+(i<4%count)
        result[player]=roles[offset:offset+size];offset+=size
    return result

def owned(player,players):
    return {c for r in assignments(players).get(player,[]) for c in ROLES[r][1]}

def feedback(session,players):
    contributors={
        'quality':('sensor',),'budget':CATEGORIES,'mass':('sensor','power','radio','launcher'),
        'power':('sensor','power','radio'),'energy':('sensor','power','radio','orbit'),
        'storage':('sensor','radio','orbit'),'delivery':('sensor','power','radio','orbit'),
        'orbit':('orbit','launcher')}
    advice={
        'quality':'Review the instrument science grade.',
        'budget':'Compare total cost across hardware, ground service and launcher.',
        'mass':'Reduce subsystem mass or select a compatible launcher with more capacity.',
        'power':'Compare simultaneous sensor/radio demand against generation; consider a larger power package.',
        'energy':'Review battery capacity, generation, eclipse and scheduled loads together.',
        'storage':'Reduce data production or improve downlink/contact opportunities.',
        'delivery':'Check generation, observation volume, contact duration and downlink rate together.',
        'orbit':'Choose a launcher that supports the selected orbit.'}
    result=[]
    for check in session.preview.checks:
        cats=contributors[check.code]
        roles=[r for r,(_,cs) in ROLES.items() if set(cs)&set(cats)]
        owners=[p for p in players if owned(p,players)&set(cats)]
        result.append({'code':check.code,'label':check.label,'passed':check.passed,
                       'explanation':check.explanation,'categories':list(cats),'roles':roles,
                       'players':owners,'advice':advice[check.code]})
    return result

class Assembly:
    def __init__(self):
        self.mission=None;self.confirmed={};self.submitted={};self.approved=None;self.validation=[];self.carried={}

    def select_mission(self,mission,session=None):
        mission_definition(mission)
        budget_changed=session.set_mission(mission) if session is not None else False
        if self.mission!=mission or budget_changed:self.approved=None;self.validation=[]
        self.mission=mission

    def check_collection(self,session,category,design=None):
        from game.domain.design import evaluate
        design=design or session.design
        if self.mission is None:raise ValueError('Select Flood Watch in the spawn room first.')
        if category not in CATEGORIES:raise ValueError('Unknown component category.')
        stages=(('sensor',),('power',),('radio',),('orbit','launcher'),('fuel',))
        stage=next(i for i,cs in enumerate(stages) if category in cs)
        if any(self.confirmed.get(c)!=getattr(design,c) for cs in stages[:stage] for c in cs):
            raise ValueError('Complete earlier tables first: payload, power, communications, mission planning, then launch propellant.')
        if not next(c.passed for c in evaluate(session.catalog,design).checks if c.code=='budget'):
            raise ValueError('Over mission budget. Reduce the total euro cost before collecting parts.')

    def confirm(self,session,category,player):
        self.check_collection(session,category)
        self.confirmed[category]=getattr(session.design,category)
        self.carried[player]=category

    def collect(self,session,category,option,player,players):
        from dataclasses import replace
        if category not in owned(player,players):raise ValueError('That subsystem belongs to your teammate.')
        cat=next(c for c in session.catalog['categories'] if c['id']==category)
        if not any(o['id']==option for o in cat['options']):raise ValueError('Unknown component option.')
        candidate=replace(session.design,**{category:option})
        self.check_collection(session,category,candidate)  # Reject before changing any shared state.
        changed=session.choose(category,option)
        if changed:self.changed(session)
        self.submitted.pop(category,None);self.approved=None;self.validation=[]
        self.confirmed[category]=option;self.carried[player]=category
        return changed

    def changed(self,session):
        for category in list(self.confirmed):
            if self.confirmed[category]!=getattr(session.design,category):
                self.confirmed.pop(category,None);self.submitted.pop(category,None)
        self.approved=None;self.validation=[]

    def inventory(self,session,player,players):
        return [c for c in CATEGORIES if c in owned(player,players)
                and self.confirmed.get(c)==getattr(session.design,c) and c not in self.submitted]

    def carry(self,session,player,players,category=None):
        inventory=self.inventory(session,player,players)
        if category not in inventory:category=inventory[0] if inventory else None
        self.carried[player]=category
        return category

    def submit(self,session,category,player,players):
        if category not in owned(player,players):raise ValueError('That contribution belongs to your teammate.')
        if self.confirmed.get(category)!=getattr(session.design,category):raise ValueError('Confirm this choice at its workshop first.')
        if category in self.submitted:raise ValueError('This contribution is already submitted.')
        self.submitted[category]={'option':getattr(session.design,category),'by':player}
        self.carry(session,player,players)

    def remove(self,session,category,player,players):
        if category not in owned(player,players):raise ValueError('That contribution belongs to your teammate.')
        if category not in self.submitted:raise ValueError('There is no submitted contribution to remove.')
        self.submitted.pop(category)
        self.approved=None;self.validation=[]
        self.carried[player]=category

    def complete(self,session):
        return self.mission is not None and all(self.submitted.get(c,{}).get('option')==getattr(session.design,c) for c in CATEGORIES)

    def validate(self,session,players):
        if not self.complete(session):raise ValueError('Submit all six choices: payload, power, radio, orbit, launcher and launch propellant.')
        self.validation=feedback(session,players)
        self.approved=asdict(session.design) if session.preview.passed else None
        return self.approved is not None

    def ready(self,session):return self.complete(session) and session.preview.passed and self.approved==asdict(session.design)

    def snapshot(self,session,players):
        for player in players:self.carry(session,player,players,self.carried.get(player))
        return {'mission':self.mission,'confirmed':dict(self.confirmed),'submitted':dict(self.submitted),
                'approved':self.approved,'validation':self.validation,'assignments':assignments(players),
                'carried':{p:self.carried.get(p) for p in players},
                'inventory':{p:self.inventory(session,p,players) for p in players},
                'ready':self.ready(session),'issues':[r for r in feedback(session,players) if not r['passed']],
                'cost_eur':session.preview.values['cost_eur'],'budget_eur':session.catalog['scenario']['budget_eur']}

    def restore(self,data,session):
        # Older saves require a fresh physical integration; never trust stale approval.
        self.__init__()
        if not isinstance(data,dict):return
        if any(m['id']==data.get('mission') and m['available'] for m in missions()):self.mission=data['mission']
        if self.mission is None:return
        session.set_mission(self.mission)
        confirmed=data.get('confirmed',{})
        if isinstance(confirmed,dict):
            self.confirmed={c:v for c,v in confirmed.items() if c in CATEGORIES and v==getattr(session.design,c)}
