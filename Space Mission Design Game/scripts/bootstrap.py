"""Create an isolated game environment; never installs system packages."""
import argparse
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python', help='Path/name of a Python 3.12+ interpreter')
    args = parser.parse_args()
    if args.python:
        return subprocess.call([args.python, str(Path(__file__).resolve())])
    if sys.version_info < (3, 12):
        print('Python 3.12+ is required. Your current version is ' + sys.version.split()[0])
        print('Run again with: python scripts/bootstrap.py --python <path-to-python-3.12-or-newer>')
        return 1
    destination = ROOT / '.venv'
    interpreter = destination / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    if not interpreter.exists():
        print('Creating project environment with ' + sys.executable, flush=True)
        venv.EnvBuilder(with_pip=True).create(destination)
    check = subprocess.run([str(interpreter), '-c', 'import sys; sys.exit(sys.version_info < (3,12))'])
    if check.returncode:
        print('Existing .venv uses an unsupported Python. Rename it and rerun setup.')
        return 1
    subprocess.run([str(interpreter), '-m', 'pip', 'install', '--disable-pip-version-check',
                    '--no-cache-dir', '-r', str(ROOT / 'requirements.txt')], check=True)
    print('\nSetup complete. No activation is required. From the project directory, run:')
    print(f'  "{interpreter}" scripts/doctor.py')
    print(f'  "{interpreter}" main.py')
    print('Configure GMAT using GMAT_BIN or local_config.json; see README.md.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError) as exc:
        print('Setup failed: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
