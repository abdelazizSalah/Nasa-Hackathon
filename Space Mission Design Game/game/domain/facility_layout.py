"""Renderer-independent station coordinates shared with host interaction checks."""
from game.domain.assembly import PLAYER_IDS

ROOMS=(('Payload Design',16,('sensor',)),('Power Systems',30,('power',)),
       ('Communications',44,('radio',)),('Mission Planning',58,('orbit','launcher')))

def station_position(category,player,players):
    center=next(x for _,x,cs in ROOMS if category in cs)
    ordered=[p for p in PLAYER_IDS if p in players];n=len(ordered)
    slots={1:[(0,11.5)],2:[(-3,11.5),(3,11.5)],3:[(-3,11.5),(3,11.5),(0,6.2)],
           4:[(-3,11.5),(3,11.5),(-3,6.2),(3,6.2)]}
    dx,z=slots[n][ordered.index(player)]
    return center+dx,z

def integration_target(category):
    targets={'sensor':(70,8),'power':(72,8),'radio':(74,8),'orbit':(76,11.5),'launcher':(76,11.5)}
    if category not in targets:raise ValueError('Unknown placement location.')
    return targets[category]
