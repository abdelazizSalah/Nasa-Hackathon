"""Versioned local campaign state; changes invalidate engineering approvals."""
from dataclasses import asdict
import json
from pathlib import Path
from game.domain.design import Design, evaluate

MISSIONS=('Accept the flood-monitoring brief','Design the spacecraft','Connect orbit and ground','Pass integrated readiness','Deliver useful observations')

class Campaign:
    def __init__(self):
        self.stage=0
        self.approved=None
        self.last_result=None
        self.previous_result=None

    def changed(self):
        self.stage=min(self.stage,1)
        self.approved=None

    def advance(self,session,read_cards):
        checks={c.code:c.passed for c in session.preview.checks}
        if self.stage==0:
            if not read_cards: return 'Open a learning card first, then accept the brief.'
        elif self.stage==1:
            if not all(checks[k] for k in ('quality','power','energy')): return 'Resolve science, power and battery checks first.'
        elif self.stage==2:
            if not all(checks[k] for k in ('orbit','storage','delivery')): return 'Resolve orbit, storage and delivery checks first.'
        elif self.stage==3:
            if not session.preview.passed: return 'Resolve every preview check before readiness approval.'
            self.approved=asdict(session.design)
        else: return 'Use Launch & Operate after readiness approval.'
        self.stage+=1
        return 'Objective complete. Next objective unlocked.'

    def save(self,path,session,read_cards):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        data={'schema_version':1,'design':asdict(session.design),'stage':self.stage,
              'approved':self.approved,'read_cards':sorted(read_cards),'last_result':self.last_result,
              'previous_result':self.previous_result}
        temp=path.with_suffix('.tmp'); temp.write_text(json.dumps(data,indent=2),encoding='utf-8'); temp.replace(path)

    def load(self,path,session):
        data=json.loads(Path(path).read_text(encoding='utf-8'))
        if data.get('schema_version')!=1: raise ValueError('Unsupported save version')
        design=Design(**data['design']); preview=evaluate(session.catalog,design)
        stage=data['stage']
        if type(stage) is not int or not 0<=stage<=5: raise ValueError('Invalid mission stage')
        approved=data.get('approved')
        if stage>=4 and (approved!=asdict(design) or not preview.passed): stage=1; approved=None
        session._apply(design,'Saved design restored.'); session.history=[]
        self.stage=stage; self.approved=approved
        self.last_result=data.get('last_result'); self.previous_result=data.get('previous_result')
        return set(data['read_cards'])
