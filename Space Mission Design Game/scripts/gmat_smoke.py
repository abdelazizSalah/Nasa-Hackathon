"""Run a real GMAT console proof with all generated outputs in the project."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from common import ROOT, RUNTIME, gmat_executable


def prepare_startup(executable, output):
    """Preserve installed data/plugins, redirect writable outputs in a local copy."""
    source = executable.parent / 'gmat_startup_file.txt'
    text = source.read_text(encoding='utf-8-sig')
    overrides = {'ROOT_PATH': executable.parent.parent.as_posix() + '/',
                 'OUTPUT_PATH': output.as_posix() + '/',
                 'LOG_FILE': (output / 'GmatLog.txt').as_posix(),
                 'FILE_UPDATE_PATH': output.as_posix() + '/'}
    lines = []
    for line in text.splitlines():
        match = re.match(r'^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$', line)
        if match and match[1] in overrides:
            line = f'{match[1]} = {overrides[match[1]]}'
        elif match and match[1] == 'PLUGIN' and any(name in match[2] for name in
                    ('libPythonInterface', 'libMatlabInterface', 'libFminconOptimizer')):
            line = '# Standalone proof does not need external Python/MATLAB: ' + line
        elif match and match[1] == 'PLUGIN' and match[2].startswith('../'):
            line = 'PLUGIN = ' + (executable.parent / match[2]).resolve().as_posix()
        lines.append(line)
    startup = output / 'gmat_startup_file.txt'
    startup.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return startup


def validate_report(path):
    lines = path.read_text().splitlines()
    rows = []
    for line in lines:
        if not line.strip() or 'DemoSat.' in line:
            continue
        values = [float(value) for value in line.split()]
        if len(values) != 8 or not all(math.isfinite(x) for x in values):
            raise ValueError('Trajectory must contain eight finite columns per sample')
        rows.append(values)
    if len(rows) != 11:
        raise ValueError(f'Expected 11 samples, got {len(rows)}')
    for i, row in enumerate(rows):
        if abs(row[0] - i * 60) > .1:
            raise ValueError('Elapsed time sequence must be 0..600 seconds in 60-second steps')
        radius = math.sqrt(sum(x*x for x in row[2:5]))
        speed = math.sqrt(sum(x*x for x in row[5:8]))
        if not 6980 < radius < 7020 or not 7.4 < speed < 7.7:
            raise ValueError('Position/velocity outside expected Earth-orbit bounds')
        if i and abs((row[1] - rows[0][1]) * 86400 - row[0]) > .1:
            raise ValueError('A1 epoch and elapsed seconds disagree')
    if math.dist(rows[0][2:5], rows[-1][2:5]) < 1000:
        raise ValueError('Spacecraft did not move along orbit')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gmat-bin', help='GMAT root, bin directory, or console executable')
    parser.add_argument('--timeout', type=float, default=90)
    args = parser.parse_args()
    executable = gmat_executable(args.gmat_bin)
    output = RUNTIME / 'gmat' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output.mkdir(parents=True)
    startup = prepare_startup(executable, output)
    template = (ROOT / 'content/gmat/smoke.script.template').read_text()
    report = output / 'trajectory.txt'
    script = output / 'smoke.script'
    script.write_text(template.replace('@REPORT_PATH@', report.as_posix()), encoding='utf-8')
    command = [str(executable), '--startup_file', str(startup), '--run', str(script), '--exit']
    print('Running real GMAT; output:', output, flush=True)
    try:
        result = subprocess.run(command, cwd=output, stdin=subprocess.DEVNULL,
                                capture_output=True, text=True, errors='replace', timeout=args.timeout)
    except subprocess.TimeoutExpired as exc:
        (output / 'console.txt').write_text(str(exc), encoding='utf-8')
        raise RuntimeError('GMAT timed out; inspect ' + str(output)) from exc
    console = result.stdout + '\n' + result.stderr
    (output / 'console.txt').write_text(console, encoding='utf-8')
    if result.returncode or not report.exists():
        raise RuntimeError(f'GMAT did not produce a report (exit {result.returncode}). See {output / "console.txt"}')
    rows = validate_report(report)
    readme = (executable.parent.parent / 'README.txt').read_text(encoding='utf-8', errors='replace')
    release_match = re.search(r'Version (R\d{4}[a-z])', readme)
    build_line = next((line.strip() for line in console.splitlines() if line.startswith('Build Date:')), 'See console.txt')
    metadata = {'status': 'passed', 'provider': 'live GMAT console',
                'distribution_version': release_match[1] if release_match else 'unknown', 'build_banner': build_line,
                'disabled_optional_interfaces': ['Python', 'MATLAB', 'Fmincon optimizer'],
                'utc': datetime.now(timezone.utc).isoformat(), 'frame': 'EarthMJ2000Eq',
                'epoch_input': '14 Nov 2026 12:00:00.000 UTCGregorian', 'time_scale': 'A1ModJulian (GMAT convention)',
                'columns': ['elapsed_s','a1_mjd','x_km','y_km','z_km','vx_km_s','vy_km_s','vz_km_s'],
                'sample_count': len(rows), 'duration_s': rows[-1][0],
                'script_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
                'model': 'Earth point mass, no drag/SRP; standalone proof, not game integration'}
    (output / 'metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    (RUNTIME / 'gmat-latest.json').write_text(json.dumps({'run_dir': str(output), **metadata}, indent=2), encoding='utf-8')
    print(f'PASS: {len(rows)} time-stamped samples, {rows[-1][0]:.0f} seconds, EarthMJ2000Eq (km, km/s).')
    print('Provenance:', output / 'metadata.json')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print('GMAT proof failed: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
