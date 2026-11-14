"""Read-only dependency checks, with optional graphics/GMAT execution tests."""
import argparse
import importlib
from importlib.metadata import PackageNotFoundError, version
import json
import platform
import subprocess
import sys
from common import ROOT, RUNTIME, gmat_executable


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--graphics', action='store_true', help='Open a 5-second graphics smoke test')
    parser.add_argument('--gmat', action='store_true', help='Execute and validate the standalone orbit proof')
    parser.add_argument('--gmat-bin', help='GMAT root, bin directory, or executable')
    args = parser.parse_args()
    print('OS:', platform.platform())
    print('Python:', sys.version.split()[0], sys.executable)
    failures = int(sys.version_info < (3, 12))
    for package, module in {'ursina': 'ursina', 'panda3d': 'panda3d.core',
                            'pillow': 'PIL.Image', 'panda3d-gltf': 'gltf'}.items():
        try:
            installed = version(package)
            importlib.import_module(module)
            print(package + ':', installed, '(import OK)')
        except PackageNotFoundError:
            print(package + ': MISSING - run scripts/bootstrap.py')
            failures += 1
        except Exception as exc:
            print(package + ': IMPORT FAILED:', exc)
            failures += 1
    try:
        print('GMAT console:', gmat_executable(args.gmat_bin))
        print('GMAT execution:', 'requested below (--gmat)' if args.gmat
              else 'not run in this invocation (use --gmat); prior evidence follows if available')
    except (ValueError, KeyError, OSError) as exc:
        print('GMAT configuration:', exc)
        failures += 1
    previous_gmat = RUNTIME / 'gmat-latest.json'
    if previous_gmat.exists():
        previous = json.loads(previous_gmat.read_text())
        print('Previous GMAT evidence:', previous.get('status'), previous.get('distribution_version'),
              previous.get('sample_count'), 'samples at', previous.get('utc'))
    evidence = RUNTIME / 'graphics-smoke.json'
    if evidence.exists():
        print('Previous graphics evidence:', evidence)
        print(json.dumps(json.loads(evidence.read_text()), indent=2))
    else:
        print('Graphics: NOT TESTED (use --graphics in a desktop session)')
    if args.graphics:
        result = subprocess.run([sys.executable, str(ROOT / 'main.py'), '--engine-check', '--smoke-seconds', '5'], cwd=ROOT)
        failures += int(result.returncode != 0)
    if args.gmat:
        command = [sys.executable, str(ROOT / 'scripts/gmat_smoke.py')]
        if args.gmat_bin:
            command += ['--gmat-bin', args.gmat_bin]
        failures += int(subprocess.run(command, cwd=ROOT).returncode != 0)
    return int(failures > 0)


if __name__ == '__main__':
    raise SystemExit(main())
