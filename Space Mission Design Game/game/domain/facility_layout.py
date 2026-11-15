"""Renderer-independent station coordinates shared with host interaction checks."""
from game.domain.assembly import PLAYER_IDS

ROOMS=(('Payload Design',16,('sensor',)),('Power Systems',30,('power',)),
       ('Communications',44,('radio',)),('Mission Planning',58,('orbit','launcher')))

def station_position(category,player=None,players=None):
    # One category per workbench; responsibility follows the current role owner.
    return {'sensor':(16,11.5),'power':(30,11.5),'radio':(44,11.5),
            'orbit':(55,11.5),'launcher':(61,11.5),'fuel':(58,6.2)}[category]

def integration_target(category):
    targets={'sensor':(70,8),'power':(72,8),'radio':(74,8),'orbit':(76,11.5),'launcher':(76,11.5),'fuel':(76,11.5)}
    if category not in targets:raise ValueError('Unknown placement location.')
    return targets[category]
