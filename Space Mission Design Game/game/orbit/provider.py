"""Real GMAT subprocess bridge with input-keyed portable trajectory cache."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile

from game.paths import ROOT,RUNTIME
sys.path.insert(0,str(ROOT/'scripts'))
from common import gmat_executable
from gmat_smoke import prepare_startup

PRESETS={'regional':(7000,28.5),'wide':(7200,98)}

def trajectory(preset,live=True):
    sma,inc=PRESETS[preset]
    inputs={'preset':preset,'sma_km':sma,'inclination_deg':inc,'duration_s':36000,'step_s':60,
            'frame':'EarthMJ2000Eq','epoch':'14 Nov 2026 12:00 UTC','model':'Earth point mass','schema':1,'gmat_release':'R2026a'}
    key=hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest()
    cache=ROOT/'content/orbit_cache'/f'{preset}.json'
    if not live:
        data=json.loads(cache.read_text())
        if data['input_hash']!=key: raise ValueError('Cached trajectory does not match inputs')
        return data['rows'],'Cached GMAT R2026a',data
    exe=gmat_executable()
    if 'Version R2026a' not in (exe.parent.parent/'README.txt').read_text(encoding='utf-8',errors='replace'):
        raise ValueError('Live bridge requires the tested GMAT R2026a distribution; choose cached mode or configure that version.')
    run=Path(tempfile.mkdtemp(prefix='orbit-',dir=ensure_runtime()))
    startup=prepare_startup(exe,run)
    report=run/'trajectory.txt'
    text=(ROOT/'content/gmat/smoke.script.template').read_text()
    text=text.replace('DemoSat.SMA = 7000;',f'DemoSat.SMA = {sma};').replace('DemoSat.INC = 28.5;',f'DemoSat.INC = {inc};')
    text=text.replace('Step = 1:10','Step = 1:600').replace('@REPORT_PATH@',report.as_posix())
    script=run/'orbit.script'; script.write_text(text)
    p=subprocess.run([str(exe),'--startup_file',str(startup),'--run',str(script),'--exit'],cwd=run,
                     capture_output=True,text=True,errors='replace',timeout=90,stdin=subprocess.DEVNULL)
    (run/'console.txt').write_text(p.stdout+p.stderr,encoding='utf-8')
    if p.returncode or not report.exists(): raise RuntimeError('GMAT failed; see '+str(run/'console.txt'))
    rows=[]
    for line in report.read_text().splitlines():
        if not line.strip() or 'DemoSat.' in line: continue
        row=[float(v) for v in line.split()]
        if len(row)!=8 or not all(math.isfinite(v) for v in row): raise ValueError('Invalid GMAT row')
        rows.append(row)
    if len(rows)!=601: raise ValueError('Expected 601 time samples')
    for i,row in enumerate(rows):
        if abs(row[0]-i*60)>.1 or abs((row[1]-rows[0][1])*86400-row[0])>.1: raise ValueError('Invalid trajectory times')
        if not sma-30<math.sqrt(sum(v*v for v in row[2:5]))<sma+30: raise ValueError('Invalid orbit radius')
    data={'inputs':inputs,'input_hash':key,'rows':rows,'source':'Live GMAT console R2026a',
          'units':'elapsed s, A1ModJulian, XYZ km, velocity km/s','script_sha256':hashlib.sha256(text.encode()).hexdigest()}
    cache=ensure_runtime()/'orbit_cache'/f'{preset}.json'
    cache.parent.mkdir(exist_ok=True); cache.write_text(json.dumps(data),encoding='utf-8')
    return rows,'Live GMAT R2026a',data

def ensure_runtime():
    RUNTIME.mkdir(parents=True,exist_ok=True); return RUNTIME
