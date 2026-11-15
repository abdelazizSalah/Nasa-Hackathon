"""Read-only bundled resources and persistent, user-writable game data."""
import os
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FROZEN=bool(getattr(sys,'frozen',False))
if FROZEN:
    base=Path(os.environ.get('LOCALAPPDATA',Path.home()/'AppData/Local')) if os.name=='nt' else Path(os.environ.get('XDG_DATA_HOME',Path.home()/'.local/share'))
    RUNTIME=base/'MissionForge'/'runtime'
    CONFIG_PATH=Path(sys.executable).resolve().parent/'local_config.json'
else:
    RUNTIME=ROOT/'runtime'
    CONFIG_PATH=ROOT/'local_config.json'
