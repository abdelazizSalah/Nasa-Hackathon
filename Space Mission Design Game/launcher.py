"""Portable GUI entry point with a useful log if startup fails."""
import sys
import traceback
from game.paths import RUNTIME

if __name__=='__main__':
    RUNTIME.mkdir(parents=True,exist_ok=True)
    if getattr(sys,'frozen',False):
        sys.stdout=sys.stderr=(RUNTIME/'game.log').open('w',encoding='utf-8',buffering=1)
    try:
        from main import main
        main()
    except Exception:
        traceback.print_exc()
        if getattr(sys,'frozen',False) and sys.platform=='win32':
            import ctypes
            ctypes.windll.user32.MessageBoxW(None,'Mission Forge could not start.\nSee: '+str(RUNTIME/'game.log'),'Mission Forge',0x10)
        raise
