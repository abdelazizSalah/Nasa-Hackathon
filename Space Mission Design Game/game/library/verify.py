"""Scripted rendering checks: python -m game.library.verify. No browser launches."""
import json
from pathlib import Path
from panda3d.core import loadPrcFileData, Filename
loadPrcFileData('', 'audio-library-name null\nnotify-level-device error')
from ursina import Ursina, application, window, color
from game.presentation.hub import Hub
from game.library.content import ROOT, ReadingPosition

def main():
    app=Ursina(title='Mission Forge | Library verification',size=(1440,900),borderless=False,
               development_mode=False,editor_ui_enabled=False)
    window.color=color.rgb32(6,12,25);window.fps_counter.enabled=False;window.exit_button.enabled=False
    output=ROOT/'runtime/library-review';output.mkdir(parents=True,exist_ok=True)
    hub=Hub();before=hub.design_session.preview;checks=[]
    def frame(name=None):
        for _ in range(3):app.taskMgr.step();app.graphicsEngine.render_frame()
        if name:assert app.win.save_screenshot(Filename.from_os_specific(str(output/f'{name}.png')))
    def settle(lib):
        for _ in range(12):lib.advance(.05)
        frame()
    hub.open_library();lib=hub.library
    # Do not overwrite the user's actual saved reading positions during verification.
    lib.positions=ReadingPosition(output/'test-reading.json')
    frame('01-shelves')
    for bi,b in enumerate(lib.books):
        lib.open_book(bi,0);settle(lib);assert lib.state=='reading'
        frame('02-reader' if bi==0 else None)
        for ci,c in enumerate(b['chapters']):
            lib.change_chapter(ci)
            for spread in range(lib.spreads):
                lib.spread=spread;lib.render_pages()
            lib.spread=0;lib.render_pages();lib.turn(1);lib.turn(1);settle(lib)
            assert lib.state=='reading'
        lib.toc();frame('03-contents' if bi==3 else None)
        lib.references();frame('04-references' if bi==3 else None)
        lib.review(True);frame('05-review' if bi==3 else None)
        lib.back();lib.turn(-1);lib.close_book();settle(lib);assert lib.state=='shelf'
        checks.append(b['id']+': opens, chapters/spreads, rapid turn, contents, sources, review, closes')
    lib.search_view();lib.query.text='vegetation';lib.find();frame('06-search');lib.back()
    lib.glossary_view();frame('07-glossary');lib.back()
    lib.open_book(3,1);lib.advance(.25);frame('08-opening');settle(lib)
    lib.spread=1;lib.render_pages();frame('09-materials-table')
    lib.turn(1);lib.advance(.25);frame('10-page-turn');settle(lib)
    window.size=(1000,900);frame('11-narrow-window')
    window.size=(1440,900);frame()
    lib.turn(1);lib.exit();settle(lib);assert hub.modal is None
    assert hub.design_session.preview==before
    hub.open_library();hub.library.open_book(0);hub.close_panel();frame()
    assert hub.modal is None
    report={'status':'passed','books':checks,'checks':['all chapters and spreads constructed','search/glossary rendered',
        'exit during page flip','forced panel cleanup during opening','design preview unchanged'],
        'limits':'Scripted graphical checks; browser invocation mocked in unit tests; no manual acceptance claim.'}
    (output/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('PASS: 12 books, all chapters/spreads, navigation and animation cleanup; screenshots:',output,flush=True)
    application.quit()

if __name__=='__main__':main()
