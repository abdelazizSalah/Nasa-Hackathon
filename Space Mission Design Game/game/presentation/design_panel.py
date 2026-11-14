"""Spacecraft choices, resource deltas, checks and a live model preview."""
import textwrap
from ursina import Entity, Text, Button, color, destroy
from game.presentation.spacecraft import Spacecraft
from game.domain.economy import eur

CYAN=color.rgb32(64,216,222)
WHITE=color.rgb32(226,237,246)
MUTED=color.rgb32(151,176,198)
AMBER=color.rgb32(255,190,89)


class DesignPanel:
    def __init__(self, parent, session, on_change, network=None):
        self.root=Entity(parent=parent)
        self.session=session
        self.on_change=on_change
        self.network=network
        self.row=0
        self.body=None
        self.model=Spacecraft(self.root,position=(-.06,.13,-.12),scale=.125)
        self.refresh()

    def text(self, text, x, y, scale=.7, tint=WHITE):
        return Text(text,parent=self.body,position=(x,y,-.045),scale=scale,color=tint)

    def refresh(self):
        if self.body is not None:
            # Disable immediately; deferred destruction must not leave old buttons clickable.
            self.body.enabled=False
            destroy(self.body)
        self.body=Entity(parent=self.root)
        session=self.session
        values=session.preview.values
        for i,category in enumerate(session.catalog['categories']):
            y=.245-i*.091
            locked=self.network is not None and not self.network.owned(category['id'])
            self.text(('> ' if self.row==i else '  ')+category['label'].upper()+(' / TEAMMATE' if locked else ''),-.675,y,.60,AMBER if self.row==i else MUTED)
            for j,option in enumerate(category['options']):
                chosen=getattr(session.design,category['id'])==option['id']
                Button(option['label'],parent=self.body,position=(-.586+j*.186,y-.038,-.04),scale=(.174,.042),
                       text_size=.68,color=color.rgb32(28,103,118) if chosen else color.rgb32(28,46,64),
                       disabled=self.network is not None and (not self.network.owned(category['id']) or self.network.busy),
                       on_click=lambda c=category['id'],o=option['id'],r=i:self.choose(c,o,r))
        self.model.apply(session.design)
        self.text('SPACECRAFT',-.175,.252,.63,CYAN)
        self.text('Model changes with\nyour sensor, panels\nand radio.',-.175,-.015,.62,MUTED)
        self.text('Science grade '+str(values['quality']),-.175,-.10,.75,CYAN)
        base=session.catalog['scenario']
        self.text(f"Fixed bus: {base['baseline_mass_kg']:g} kg / {eur(base['baseline_cost_eur'])}\n{base['baseline_power_w']:g} W idle / {base['storage_mb']:g} MB storage",-.175,-.145,.50,MUTED)
        self.text('RESOURCE BALANCE',.20,.252,.65,CYAN)
        failed={check.code for check in session.preview.failures}
        metrics=[
            ('Budget', 'cost_eur',f"{eur(values['cost_eur'])}/{eur(session.catalog['scenario']['budget_eur'])}",'budget'),
            ('Mass', 'mass_kg',f"{values['mass_kg']:g}/{values['launch_capacity_kg']:g} kg",'mass'),
            ('Power margin', 'power_margin_w',f"{values['power_margin_w']:+g} W",'power'),
            ('Min battery', 'min_battery_wh',f"{values['min_battery_wh']:.1f} Wh",'energy'),
            ('Peak storage', 'max_storage_mb',f"{values['max_storage_mb']:.0f}/{values['storage_capacity_mb']:g} MB",'storage'),
            ('Data delivered', 'delivered_mb',f"{values['delivered_mb']:.0f}/{values['expected_data_mb']:.0f} MB",'delivery'),
        ]
        for i,(label,key,value,check) in enumerate(metrics):
            y=.205-i*.048
            delta=session.delta(key)
            delta_text=f' ({delta:+.1f})' if abs(delta)>.01 else ''
            self.text(label,.20,y,.58,MUTED)
            self.text(value+delta_text,.20,y-.020,.73,AMBER if check in failed else WHITE)
        orbit_check=next(check for check in session.preview.checks if check.code=='orbit')
        self.text('Orbit / launch: '+('compatible' if orbit_check.passed else 'INCOMPATIBLE'),.20,-.103,.61,CYAN if orbit_check.passed else AMBER)
        self.text('Brackets: change from previous choice',.20,-.153,.50,MUTED)
        self.text('Change: '+ '\n'.join(textwrap.wrap(session.message,95)), -.67,-.207,.64,MUTED)
        first=session.preview.failures[0] if session.preview.failures else None
        self.text('LIMITING FACTOR: '+first.label.upper() if first else 'PREVIEW PASSES ALL 8 CHECKS',-.67,-.278,.77,AMBER if first else CYAN)
        explanation=first.explanation if first else 'Multiple designs can work. This preset preview is not launch clearance.'
        self.text(explanation,-.67,-.311,.64,WHITE)
        other=', '.join(check.label for check in session.preview.failures[1:])
        self.text('Also check: '+other if other else 'Teaching assumptions / preset orbit cycle / service plan: 12 months',-.67,-.34,.59,MUTED)
        Button('UNDO / U',parent=self.body,position=(-.54,-.378,-.04),scale=(.25,.044),text_size=.65,
               color=color.rgb32(31,59,77),disabled=not bool(session.history),on_click=self.undo)
        Button('RESET / BACKSPACE',parent=self.body,position=(-.22,-.378,-.04),scale=(.33,.044),text_size=.64,
               color=color.rgb32(31,59,77),on_click=self.reset)
        self.text('UP/DOWN Row   LEFT/RIGHT Change   ESC Close',.005,-.367,.55,MUTED)

    def choose(self,category,option,row):
        self.row=row
        if self.network is not None:
            if not self.network.owned(category) or self.network.busy:
                self.session.message='That row belongs to your teammate, or the crew launch is in progress.'
                self.refresh();return
            self.network.send('choose',category=category,option=option); return
        if self.session.choose(category,option):
            self.on_change()
        self.refresh()

    def undo(self):
        if self.network is not None:self.network.send('undo'); return
        if self.session.undo(): self.on_change()
        self.refresh()

    def reset(self):
        if self.network is not None:self.network.send('reset_design'); return
        if self.session.reset(): self.on_change()
        self.refresh()

    def handle_input(self,key):
        categories=self.session.catalog['categories']
        if key in ('up arrow','down arrow','tab'):
            self.row=(self.row+(-1 if key=='up arrow' else 1))%len(categories)
            self.refresh()
        elif key in ('left arrow','right arrow','enter'):
            category=categories[self.row]
            options=category['options']
            index=next(i for i,item in enumerate(options) if item['id']==getattr(self.session.design,category['id']))
            self.choose(category['id'],options[(index+(-1 if key=='left arrow' else 1))%len(options)]['id'],self.row)
        elif key=='u': self.undo()
        elif key=='backspace': self.reset()
