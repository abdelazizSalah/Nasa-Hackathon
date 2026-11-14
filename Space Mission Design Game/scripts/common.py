"""Local configuration shared by setup diagnostics and the standalone GMAT proof."""
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / 'runtime'


def gmat_executable(override=None):
    raw = override or os.environ.get('GMAT_BIN')
    if not raw and (ROOT / 'local_config.json').exists():
        raw = json.loads((ROOT / 'local_config.json').read_text(encoding='utf-8'))['gmat_bin']
    names = ('GmatConsole.exe',) if os.name == 'nt' else ('GmatConsole', 'GMATConsole')
    if raw:
        path = Path(raw).expanduser().resolve()
        if path.is_dir():
            for directory in (path, path / 'bin'):
                for name in names:
                    if (directory / name).is_file():
                        return directory / name
        elif path.is_file():
            return path
        raise FileNotFoundError('No GMAT console at configured path: ' + str(path))
    for name in names:
        found = shutil.which(name)
        if found:
            return Path(found).resolve()
    raise FileNotFoundError('Set GMAT_BIN to your platform\'s GMAT folder or console executable.')
