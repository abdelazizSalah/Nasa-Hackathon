from pathlib import Path
from PyInstaller.utils.hooks import collect_all,collect_dynamic_libs,copy_metadata

root=Path(SPECPATH)
datas,binaries,hidden=collect_all('ursina')
binaries+=collect_dynamic_libs('panda3d')
datas+=copy_metadata('panda3d')
datas+=[(str(root/'content'),'content')]
# Fingerprints inspect these exact source files; source and executable peers match.
for source in (root/'game').rglob('*.py'):
    if '__pycache__' not in source.parts:datas.append((str(source),str(source.parent.relative_to(root))))
a=Analysis([str(root/'launcher.py')],pathex=[str(root),str(root/'scripts')],
           binaries=binaries,datas=datas,hiddenimports=hidden+['common','gmat_smoke','PIL.Image','gltf'],
           excludes=['tkinter','pytest','numpy','matplotlib'],noarchive=False)
pyz=PYZ(a.pure)
exe=EXE(pyz,a.scripts,a.binaries,a.datas,[],name='MissionForge',debug=False,
        bootloader_ignore_signals=False,strip=False,upx=False,console=False)
