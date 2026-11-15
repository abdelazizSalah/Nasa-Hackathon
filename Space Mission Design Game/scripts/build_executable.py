"""Build a native executable on the current OS; no game dependency installation."""
from pathlib import Path
import subprocess
import sys
import hashlib
import importlib.metadata
import shutil

ROOT=Path(__file__).resolve().parents[1]
def write_release_metadata(destination):
    exe=destination/('MissionForge.exe' if sys.platform=='win32' else 'MissionForge')
    digest=hashlib.sha256(exe.read_bytes()).hexdigest()
    (destination/'SHA256SUMS.txt').write_text(digest+'  '+exe.name+'\n',encoding='utf-8')
    names=[line.split('==')[0] for line in (ROOT/'requirements.txt').read_text().splitlines() if line and not line.startswith('#')]
    names+=['pyinstaller']
    for name in names:
        dist=importlib.metadata.distribution(name)
        for file in dist.files or []:
            if any(word in file.name.lower() for word in ('license','copying','notice')) and '.dist-info' in str(file):
                source=Path(dist.locate_file(file))
                if source.is_file():
                    target=ROOT.parent/'play/licenses'/name/file.name
                    target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    python_license=Path(sys.base_prefix)/'LICENSE.txt'
    if python_license.exists():
        target=ROOT.parent/'play/licenses/Python-LICENSE.txt';target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(python_license,target)

if __name__=='__main__':
    destination=ROOT.parent/'play'/('windows' if sys.platform=='win32' else 'linux')
    subprocess.run([sys.executable,'-m','PyInstaller','--noconfirm','--clean',
                    '--distpath',str(destination),'--workpath',str(ROOT/'runtime/build'),
                    str(ROOT/'MissionForge.spec')],cwd=ROOT,check=True)
    write_release_metadata(destination)
    print('Executable:',destination/('MissionForge.exe' if sys.platform=='win32' else 'MissionForge'))
