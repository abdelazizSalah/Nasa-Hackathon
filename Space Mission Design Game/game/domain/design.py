"""Deterministic spacecraft trade studies, independent of graphics and GMAT."""
from dataclasses import dataclass, replace
from itertools import product
import json
from pathlib import Path
from game.domain.economy import mission_definition, eur

CATALOG_PATH = Path(__file__).resolve().parents[2] / 'content/design_catalog.json'


@dataclass(frozen=True)
class Design:
    sensor: str = 'basic'
    power: str = 'compact'
    radio: str = 'standard'
    orbit: str = 'regional'
    launcher: str = 'light'


@dataclass(frozen=True)
class Check:
    code: str
    label: str
    passed: bool
    explanation: str


@dataclass(frozen=True)
class Preview:
    values: dict
    checks: tuple

    @property
    def passed(self):
        return all(check.passed for check in self.checks)

    @property
    def failures(self):
        return tuple(check for check in self.checks if not check.passed)


def load_catalog(path=CATALOG_PATH,mission_id='flood-watch'):
    catalog=json.loads(Path(path).read_text(encoding='utf-8'))
    mission=mission_definition(mission_id)
    catalog['scenario'].update(budget_eur=mission['budget_eur'],currency='EUR',mission_id=mission_id)
    return catalog


def selected(catalog, design):
    return {category['id']: next(option for option in category['options']
                               if option['id'] == getattr(design, category['id']))
            for category in catalog['categories']}


def evaluate(catalog, design):
    """Preview one preset orbit, not a mission success or launch-clearance decision.

    Observations occur at the start of sunlight and contacts at the end of the
    cycle. An energy shortage proportionally reduces productive activity; the
    energy check fails regardless. Peak-power margin is a separate conservative
    installed-load requirement, even if that worst case is not scheduled here.
    """
    choice = selected(catalog, design)
    scenario = catalog['scenario']
    sensor, power, radio, orbit, launcher = (choice[key] for key in
                                             ('sensor', 'power', 'radio', 'orbit', 'launcher'))
    hardware = (sensor, power, radio)
    mass = scenario['baseline_mass_kg'] + sum(item['mass_kg'] for item in hardware)
    cost = (scenario['baseline_cost_eur'] + sum(item['cost_eur'] for item in hardware)
            + launcher['cost_eur'] + orbit['ground_cost_eur'])
    peak = scenario['baseline_power_w'] + sensor['power_w'] + radio['power_w']
    battery = power['battery_wh']
    min_battery = battery
    storage = max_storage = delivered = produced = overflow = unserved = 0.
    solar_wh = used_wh = curtailed_wh = 0.
    for minute in range(orbit['period_min']):
        observing = minute < orbit['observation_min']
        contact = minute >= orbit['period_min'] - orbit['contact_min']
        generation = power['generation_w'] if minute < orbit['sunlight_min'] else 0
        demand = (scenario['baseline_power_w'] + (sensor['power_w'] if observing else 0)
                  + (radio['power_w'] if contact else 0))
        supply_wh = generation / 60
        requested_wh = demand / 60
        available_wh = battery + supply_wh
        fraction = min(1., available_wh / requested_wh) if requested_wh else 1.
        shortfall = max(0., requested_wh - available_wh)
        actual_wh = requested_wh - shortfall
        raw_battery = battery + supply_wh - actual_wh
        curtailed_wh += max(0., raw_battery - power['battery_wh'])
        battery = min(power['battery_wh'], max(0., raw_battery))
        unserved += shortfall
        min_battery = min(min_battery, battery)
        solar_wh += supply_wh
        used_wh += actual_wh
        generated = sensor['data_mb_min'] * fraction if observing else 0
        produced += generated
        new_storage = storage + generated
        overflow += max(0., new_storage - scenario['storage_mb'])
        storage = min(scenario['storage_mb'], new_storage)
        sent = min(storage, radio['downlink_mb_min'] * fraction) if contact else 0
        storage -= sent
        delivered += sent
        max_storage = max(max_storage, storage)
    expected_data = sensor['data_mb_min'] * orbit['observation_min']
    values = {
        'mass_kg': mass, 'cost_eur': cost, 'quality': sensor['quality'],
        'peak_power_w': peak, 'generation_w': power['generation_w'],
        'power_margin_w': power['generation_w'] - peak,
        'mass_margin_kg': launcher['capacity_kg'] - mass,
        'budget_margin_eur': scenario['budget_eur'] - cost,
        'battery_capacity_wh': power['battery_wh'], 'min_battery_wh': min_battery,
        'final_battery_wh': battery, 'unserved_energy_wh': unserved,
        'expected_data_mb': expected_data, 'generated_mb': produced,
        'delivered_mb': delivered, 'stored_mb': storage, 'overflow_mb': overflow,
        'max_storage_mb': max_storage, 'storage_capacity_mb': scenario['storage_mb'],
        'solar_energy_wh': solar_wh, 'used_energy_wh': used_wh, 'curtailed_energy_wh': curtailed_wh,
        'contact_min': orbit['contact_min'], 'eclipse_min': orbit['period_min'] - orbit['sunlight_min'],
        'launch_capacity_kg': launcher['capacity_kg'],
    }
    checks = (
        Check('quality', 'Science quality', sensor['quality'] >= scenario['required_quality'],
              f"Science grade {sensor['quality']} / required {scenario['required_quality']}."),
        Check('budget', 'Budget', cost <= scenario['budget_eur'],
              f"Total {eur(cost)} / mission budget {eur(scenario['budget_eur'])}, including bus, launch and ground services."),
        Check('mass', 'Launch mass', mass <= launcher['capacity_kg'],
              f"Spacecraft {mass:g} kg / launcher capacity {launcher['capacity_kg']:g} kg."),
        Check('orbit', 'Orbit compatibility', design.orbit in launcher['allowed_orbits'],
              f"{launcher['name']} {'supports' if design.orbit in launcher['allowed_orbits'] else 'does not support'} the {design.orbit} preset."),
        Check('power', 'Peak power', peak <= power['generation_w'],
              f"Peak design rule: simultaneous load {peak:g} W / solar generation {power['generation_w']:g} W."),
        Check('energy', 'Eclipse energy', unserved < 1e-7,
              f"Lowest battery {min_battery:.1f} Wh; unmet load {unserved:.1f} Wh over the preview cycle."),
        Check('storage', 'Data storage', overflow < 1e-7,
              f"Peak storage {max_storage:.0f} / {scenario['storage_mb']:g} MB; overflow {overflow:.0f} MB."),
        Check('delivery', 'Data delivery', delivered >= expected_data - 1e-7,
              f"Delivered {delivered:.0f} / {expected_data:.0f} MB in {orbit['contact_min']} contact minutes."),
    )
    return Preview(values, checks)


class DesignSession:
    """One session's reversible choices and comparisons; no per-frame recalculation."""
    def __init__(self, catalog=None):
        self.catalog = catalog if catalog is not None else load_catalog()
        self.design = Design(**self.catalog['defaults'])
        self.preview = evaluate(self.catalog, self.design)
        self.previous = self.preview
        self.history = []
        self.message = 'Change a component to see its effects across the whole design.'

    def set_mission(self,mission_id):
        mission=mission_definition(mission_id)
        scenario=self.catalog['scenario']
        changed=scenario.get('mission_id')!=mission_id or scenario.get('budget_eur')!=mission['budget_eur']
        scenario.update(mission_id=mission_id,budget_eur=mission['budget_eur'],currency='EUR')
        if changed:self._apply(self.design,'Mission budget updated to '+eur(mission['budget_eur']))
        return changed

    def choose(self, category, option):
        options = next(item['options'] for item in self.catalog['categories'] if item['id'] == category)
        component = next(item for item in options if item['id'] == option)
        replacement = replace(self.design, **{category: option})
        if replacement == self.design:
            return False
        self.history.append(self.design)
        self.history = self.history[-30:]
        self._apply(replacement, component['description'])
        return True

    def _apply(self, design, message):
        self.previous = self.preview
        self.design = design
        self.preview = evaluate(self.catalog, design)
        self.message = message

    def undo(self):
        if not self.history:
            return False
        self._apply(self.history.pop(), 'Previous configuration restored. Compare the changes below.')
        return True

    def reset(self):
        default = Design(**self.catalog['defaults'])
        if self.design == default:
            return False
        self.history.append(self.design)
        self._apply(default, 'Default configuration restored. You can undo this reset.')
        return True

    def delta(self, key):
        return self.preview.values[key] - self.previous.values[key]


def feasible_designs(catalog):
    categories = catalog['categories']
    for options in product(*(category['options'] for category in categories)):
        design = Design(**{category['id']: option['id'] for category, option in zip(categories, options)})
        if evaluate(catalog, design).passed:
            yield design
