"""Mission-owned euro budgets and shared display formatting (fictional teaching costs)."""
import json
from pathlib import Path

def missions():
    path=Path(__file__).resolve().parents[2]/'content/missions.json'
    return json.loads(path.read_text(encoding='utf-8'))['missions']

def mission_definition(mission_id):
    mission=next((m for m in missions() if m['id']==mission_id and m['available']),None)
    if mission is None:raise ValueError('That mission is unavailable.')
    budget=mission.get('budget_eur')
    if mission.get('currency')!='EUR' or type(budget) not in (int,float) or not 0<budget<1e12:
        raise ValueError('Mission needs a positive EUR budget.')
    return mission

def eur(value):return f'€{value:,.0f}'
