"""Library-local shelves, animated reader and offline learning tools."""
import json
import math
import textwrap
from ursina import Entity, Text, Button, InputField, color, destroy, time, window, load_texture
from game.library.book import Book
from game.library.art import ASSETS, CAPTIONS
from game.library.content import DATA, load_library, paginate, table_pages, search, ReferenceOpener, ReadingPosition

INK=color.rgb32(38,47,53)
PAPER=color.rgb32(244,237,216)
CYAN=color.rgb32(72,220,218)
MUTED=color.rgb32(161,185,201)

def world_shelves(hub):
    books,_=load_library()
    hub.box((0,1.7,13.75),(11,2.6,.1),color.rgb32(15,41,57),shader=False)
    hub.label('THE AEROSPACE FIELD LIBRARY',(0,3.2,13.63),.20,CYAN)
    hub.label('12 BOOKS / CHOOSE A COVER OR USE THE CONSOLE',(0,2.86,13.63),.09)
    for y in (.54,1.65):hub.box((0,y,13.4),(10.8,.08,.65),color.rgb32(89,84,70),shader=False)
    for i,book in enumerate(books):
        x=-4.6+(i%6)*1.84;y=2.2-(i//6)*1.1
        model=Book(book,position=(x,y,13.27),scale=(.66,.92,1),rotation_y=-8)
        def choose(index=i):
            if hub.modal is None and math.hypot(hub.pose.x,hub.pose.z-12)<5:
                hub.open_library();hub.select_card(index);hub.library.open_book(index)
        model.choose=choose
        def hover(active,index=i,entity=model):
            entity.z=13.12 if active else 13.27
            if active and hub.modal is None and math.hypot(hub.pose.x,hub.pose.z-12)<5:
                book=books[index]
                hub.toast(book['title']+' / '+book['level']+' / Click to open book')
        model.on_hover=hover
        hub.label(book['short'],(x,y-.52,13.10),.055)

class LibraryController(Entity):
    def __init__(self,hub):
        super().__init__(parent=hub.panel)
        self.hub=hub;self.books,self.refs=load_library()
        self.opener=ReferenceOpener(self.refs);self.positions=ReadingPosition()
        self.glossary=json.loads((DATA/'glossary.json').read_text(encoding='utf-8'))
        self.answers=json.loads((DATA/'answers.json').read_text(encoding='utf-8'))
        self.index=0;self.chapter=0;self.spread=0;self.state='shelf';self.elapsed=0
        self.disposed=False;self.exit_after=False;self.midpoint=False;self.page=None
        self.layer=Entity(parent=self);self.reader=None;self.active_book=None
        self.status=Text('',parent=self,position=(-.66,-.36,-.09),scale=.66,color=CYAN)
        self.shelf()

    def text(self,value,x,y,size=.78,tint=INK,parent=None,width=None):
        if width:value='\n'.join(textwrap.wrap(value,width))
        return Text(value,parent=parent or self.layer,position=(x,y,-.075),scale=size,color=tint)

    def button(self,label,x,y,width,action,parent=None):
        return Button(label,parent=parent or self.layer,position=(x,y,-.10),scale=(width,.037),
                      color=color.rgb32(32,77,89),text_size=.62,on_click=action)

    def clear(self):
        destroy(self.layer);self.layer=Entity(parent=self)

    def shelf(self):
        self.clear();self.state='shelf';self.models=[]
        for y in (-.04,-.29):
            Entity(parent=self.layer,model='cube',position=(0,y,.015),scale=(1.35,.016,.12),color=color.rgb32(95,86,67))
        for i,book in enumerate(self.books):
            x=-.575+(i%6)*.23;y=.09-(i//6)*.25
            model=Book(book,parent=self.layer,position=(x,y,-.035),scale=(.151,.211,.18),rotation_y=-10)
            model.choose=lambda index=i:self.open_book(index)
            model.on_hover=lambda active,index=i:self.hover(index,active)
            self.models.append(model)
            self.text(f'{i+1:02}  {book["short"]}',x-.09,y-.119,.46,MUTED)
        self.button('SEARCH',-.54,.245,.23,self.search_view)
        self.button('GLOSSARY',-.27,.245,.23,lambda:self.glossary_view(0))
        self.text('Arrows / Tab: select    Enter: open    Esc: leave',-.10,.257,.59,MUTED)
        self.select(self.index)

    def hover(self,index,active):
        if self.state=='shelf':
            self.models[index].z=-.09 if active else (-.072 if index==self.index else -.035)
            self.status.text=(self.books[index]['title']+' / '+self.books[index]['level']+' / Click to open') if active else self.selection_label()

    def selection_label(self):
        b=self.books[self.index];return f'{self.index+1:02} / {b["title"]}  |  {b["level"]}'

    def select(self,index):
        self.index=index%len(self.books)
        if self.state=='shelf':
            for i,m in enumerate(self.models):m.z=-.072 if i==self.index else -.035
            self.status.text=self.selection_label()

    def open_book(self,index,chapter=None):
        if self.state not in ('shelf','search','toc','references','glossary','review','reading'):return
        self.hub.select_card(index)
        self.index=index
        saved_chapter,saved_spread=self.positions.get(self.books[index]['id'])
        self.chapter=min(saved_chapter,len(self.books[index]['chapters'])-1) if chapter is None else chapter
        self.spread=saved_spread if chapter is None else 0
        self.clear()
        if self.active_book:destroy(self.active_book)
        self.active_book=Book(self.books[index],parent=self,position=(-.575+(index%6)*.23,.09-(index//6)*.25,-.14),scale=(.151,.211,.18))
        self.start_position=tuple(self.active_book.position)
        self.state='opening';self.elapsed=0;self.status.text='Opening '+self.books[index]['title']

    def update(self):
        if self.disposed or self.hub.panel is None:return
        self.advance(min(time.dt,.1))
        if self.disposed or self.hub.panel is None:return
        # Adapt only this library panel; other interfaces and window settings are untouched.
        self.hub.panel.scale=min(1,float(window.aspect_ratio)/1.62)

    def advance(self,dt):
        if self.disposed:return
        if self.state not in ('opening','closing','flipping'):return
        self.elapsed+=dt
        t=min(1,self.elapsed/.55);s=t*t*(3-2*t)
        if self.state in ('opening','closing'):
            q=s if self.state=='opening' else 1-s
            self.active_book.position=tuple(v*(1-q)+w*q for v,w in zip(self.start_position,(0,-.015,-.14)))
            self.active_book.scale=(.151+q*.49,.211+q*.35,.18)
            self.active_book.hinge.rotation_y=155*q
            self.active_book.rotation_z=4*math.sin(math.pi*q)
            if t==1:
                if self.state=='opening':
                    self.active_book.enabled=False;self.show_reader()
                else:
                    destroy(self.active_book);self.active_book=None
                    if self.exit_after:self.hub.close_panel()
                    else:self.shelf()
        else:
            self.page.rotation_y=180*s*self.flip_direction
            if t>=.5 and not self.midpoint:
                self.midpoint=True;self.spread=self.pending_spread;self.render_pages()
            if t==1:
                destroy(self.page);self.page=None;self.state='reading'

    def show_reader(self):
        self.clear();self.state='reading'
        Entity(parent=self.layer,model='cube',position=(0,-.015,-.015),scale=(1.36,.535,.025),color=color.hex(self.books[self.index]['color']))
        for x in (-.327,.327):
            Entity(parent=self.layer,model='cube',position=(x,-.015,-.04),scale=(.643,.51,.02),color=PAPER)
        Entity(parent=self.layer,model='quad',position=(0,-.015,-.055),scale=(.009,.51),color=color.rgb32(133,119,94))
        self.page_content=Entity(parent=self.layer)
        self.button('PREV PAGE',-.57,-.304,.17,lambda:self.turn(-1))
        self.button('NEXT PAGE',-.37,-.304,.17,lambda:self.turn(1))
        self.button('CONTENTS',-.15,-.304,.22,self.toc)
        self.button('SOURCES',.095,-.304,.22,lambda:self.references(0))
        self.button('REVIEW',.33,-.304,.20,lambda:self.review(False))
        self.button('CLOSE BOOK',.56,-.304,.22,self.close_book)
        self.button('PREV CHAPTER',.36,.25,.19,lambda:self.change_chapter(self.chapter-1))
        self.button('NEXT CHAPTER',.575,.25,.19,lambda:self.change_chapter(self.chapter+1))
        self.render_pages()

    def chapter_data(self):return self.books[self.index]['chapters'][self.chapter]

    def render_pages(self):
        destroy(self.page_content);self.page_content=Entity(parent=self.layer)
        c=self.chapter_data();pages=paginate(c);tables=table_pages(c)
        self.spreads=max(len(pages),1+len(tables))
        self.spread=max(0,min(self.spread,self.spreads-1))
        self.text(f'{self.chapter+1:02} / '+c['title'],-.64,.257,.77,CYAN,parent=self.page_content,width=65)
        body=pages[self.spread] if self.spread<len(pages) else 'COMPARISON WORKSHOP\n\nRead the option on the facing page.\n\nWhich requirement does it serve?\nWhat resource or risk does it add?\nWhat evidence would you need?\n\nCompare it with the other options, then\nuse REVIEW to check your understanding.'
        self.text(body,-.625,.215,.75,parent=self.page_content)
        if self.spread==0:
            asset=ASSETS/f'{c["diagram"]}.png'
            if asset.exists():
                Entity(parent=self.page_content,model='quad',position=(.325,.085,-.075),scale=(.59,.344),texture=load_texture(asset.name,folder=ASSETS))
            else:self.text('Diagram unavailable: '+CAPTIONS[c['diagram']],.03,.17,.74,parent=self.page_content,width=48)
            self.text(CAPTIONS[c['diagram']],.035,-.11,.73,parent=self.page_content,width=48)
            self.text('Original schematic / not to scale\nNASA sources: use SOURCES below.',.035,-.195,.60,parent=self.page_content)
        elif tables:
            comparison=tables[(self.spread-1)%len(tables)]
            # A vertical comparison table: each band pairs a field heading with
            # its value, so long engineering caveats stay readable on one page.
            lines=comparison.splitlines();start=0;band=0
            for end in range(len(lines)+1):
                if end==len(lines) or not lines[end]:
                    if end>start:
                        top=.228-start*.01875;bottom=.228-(end+1)*.01875
                        Entity(parent=self.page_content,model='quad',position=(.325,(top+bottom)/2,-.064),
                               scale=(.60,top-bottom),color=color.rgb32(228,220,197) if band%2==0 else PAPER)
                        Entity(parent=self.page_content,model='quad',position=(.325,top,-.066),scale=(.60,.001),color=color.rgb32(151,143,121))
                        band+=1
                    start=end+1
            self.text(comparison,.035,.215,.75,parent=self.page_content)
        else:
            sections=[s for s in c['sections'] if s['heading']=='Key takeaways']
            value='\n\n'.join(p for s in sections for p in s['paragraphs'])
            self.text('ENGINEERING CHECK\n\n'+ '\n'.join(textwrap.wrap(value,49)),.035,.215,.75,parent=self.page_content)
        self.status.text=f'{self.books[self.index]["short"]} / Chapter {self.chapter+1} of {len(self.books[self.index]["chapters"])} / Spread {self.spread+1} of {self.spreads}  |  Left/right: pages  Up/down: chapters'
        self.positions.save(self.books[self.index]['id'],self.chapter,self.spread)

    def turn(self,direction):
        if self.state!='reading':return
        target=self.spread+direction
        if not 0<=target<self.spreads:return
        self.pending_spread=target;self.state='flipping';self.elapsed=0;self.midpoint=False;self.flip_direction=direction
        self.page=Entity(parent=self,position=(0,-.015,-.16))
        Entity(parent=self.page,model='quad',x=.323*direction,scale=(.646,.51),color=color.rgb32(230,221,195),double_sided=True)

    def change_chapter(self,index):
        if self.state=='flipping':return
        self.chapter=max(0,min(index,len(self.books[self.index]['chapters'])-1));self.spread=0;self.show_reader()

    def close_book(self,exit_after=False):
        if self.state in ('opening','closing'):return
        self.exit_after=exit_after
        if self.active_book:
            if self.page:destroy(self.page);self.page=None
            self.clear();self.active_book.enabled=True;self.state='closing';self.elapsed=0
            self.status.text='Returning book to its shelf'
        elif exit_after:self.hub.close_panel()
        else:self.shelf()

    def exit(self):
        if self.state=='opening':
            # Finish the current hinge pose before reversing; never schedule delayed callbacks.
            self.advance(.55)
        self.close_book(True)

    def utility(self,state,title):
        if self.state in ('opening','closing','flipping'):return False
        self.clear();self.state=state
        self.text(title,-.64,.255,1,CYAN)
        self.button('BACK',.56,-.305,.22,self.back)
        self.status.text='Library tools / local, optional and independent of mission progress'
        return True

    def back(self):
        if self.active_book:self.show_reader()
        else:self.shelf()

    def toc(self):
        if not self.utility('toc','CONTENTS / '+self.books[self.index]['short']):return
        for i,c in enumerate(self.books[self.index]['chapters']):
            self.button(f'{i+1:02}   {c["title"]}',0,.16-i*.075,1.25,lambda index=i:self.change_chapter(index))

    def references(self,page=0):
        if not self.utility('references','NASA REFERENCE DESK / optional internet links'):return
        keys=self.chapter_data()['refs'] if self.active_book else list(self.refs)
        count=max(1,math.ceil(len(keys)/3));page=page%count
        for i,key in enumerate(keys[page*3:page*3+3]):
            r=self.refs[key];y=.18-i*.145
            self.text(r['title'],-.63,y,.78,color.white,width=82)
            self.text(f'{r["organization"]} / {r["date"]} / {r["type"]}',-.63,y-.037,.58,MUTED,width=100)
            self.text(r['description'],-.63,y-.066,.61,MUTED,width=86)
            self.button('OPEN NASA RESOURCE',.50,y-.075,.29,lambda source=key:self.open_reference(source))
        self.button('PREV',-.59,-.305,.10,lambda:self.references(page-1))
        self.button('NEXT',-.46,-.305,.10,lambda:self.references(page+1))
        self.text(f'{page+1}/{count} / Browser opens only when you click OPEN.',-.34,-.297,.64,MUTED)

    def open_reference(self,key):
        try:
            started=self.opener.open(key)
            self.status.text='Opening NASA resource in your browser. Offline? The book remains available.' if started else 'Browser request already in progress.'
        except (ValueError,RuntimeError):self.status.text='This resource could not be opened. Continue reading offline.'

    def glossary_view(self,page=0):
        if not self.utility('glossary','AEROSPACE GLOSSARY'):return
        entries=list(self.glossary.items());count=math.ceil(len(entries)/5);page%=count
        for i,(term,definition) in enumerate(entries[page*5:page*5+5]):
            y=.18-i*.087
            self.text(term,-.63,y,.79,CYAN)
            self.text(definition,-.63,y-.026,.67,MUTED,width=103)
        self.button('PREV',-.59,-.305,.1,lambda:self.glossary_view(page-1))
        self.button('NEXT',-.46,-.305,.1,lambda:self.glossary_view(page+1))
        self.text(f'{page+1}/{count}',-.33,-.297,.7,MUTED)

    def review(self,reveal=False):
        if not self.utility('review','SELF CHECK / no score, no mission effect'):return
        b=self.books[self.index]
        for i,q in enumerate(b['questions']):
            y=.18-i*.135
            self.text(f'{i+1}. {q}',-.63,y,.77,color.white,width=85)
            if reveal:self.text(self.answers[b['id']][i],-.63,y-.045,.67,MUTED,width=99)
        self.button('SHOW ANSWERS' if not reveal else 'HIDE ANSWERS',-.43,-.305,.36,lambda:self.review(not reveal))

    def search_view(self):
        if not self.utility('search','SEARCH ALL BOOKS / words match within a chapter'):return
        self.query=InputField(parent=self.layer,position=(-.16,.16,-.12),scale=(.93,.046),limit_content_to='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -')
        self.query.active=True
        self.button('FIND',.49,.16,.22,self.find)
        self.results=Entity(parent=self.layer)
        self.text('Try: aluminum, thermal expansion, electric propulsion, vegetation',-.63,.09,.68,MUTED)

    def find(self,page=0):
        destroy(self.results);self.results=Entity(parent=self.layer)
        hits=search(self.books,self.query.text);count=max(1,math.ceil(len(hits)/5));page%=count
        for i,(bi,ci) in enumerate(hits[page*5:page*5+5]):
            label=self.books[bi]['short']+' / '+self.books[bi]['chapters'][ci]['title']
            self.button(label,0,.025-i*.06,1.27,lambda b=bi,c=ci:self.open_book(b,c),self.results)
        self.text(f'{len(hits)} matching chapters / page {page+1}/{count}',-.63,-.275,.66,MUTED,parent=self.results)
        self.button('PREV',-.59,-.305,.10,lambda:self.find(page-1),self.results)
        self.button('NEXT',-.46,-.305,.10,lambda:self.find(page+1),self.results)

    def handle_input(self,key):
        if key=='escape':self.exit();return
        if self.state=='search':
            if key=='enter':self.find()
            return
        if self.state=='shelf':
            if key in ('up arrow','left arrow'):self.hub.select_card((self.index-1)%12)
            elif key in ('down arrow','right arrow','tab'):self.hub.select_card((self.index+1)%12)
            elif key=='enter':self.open_book(self.index)
        elif self.state=='reading':
            if key=='left arrow':self.turn(-1)
            elif key=='right arrow':self.turn(1)
            elif key=='up arrow':self.change_chapter(self.chapter-1)
            elif key=='down arrow':self.change_chapter(self.chapter+1)
            elif key=='t':self.toc()
            elif key=='r':self.references(0)

    def dispose(self):
        self.disposed=True;self.enabled=False;self.opener.close()
        if self.page:destroy(self.page);self.page=None
