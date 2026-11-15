"""Offline library catalog, bounded pagination, search, and safe reference actions."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import textwrap
from urllib.parse import urlsplit
import webbrowser

from game.paths import ROOT,RUNTIME
DATA=ROOT/'content/library'
LINE_WIDTH=53
PAGE_LINES=20

def load_library():
    books=json.loads((DATA/'catalog.json').read_text(encoding='utf-8'))['books']
    refs=json.loads((DATA/'references.json').read_text(encoding='utf-8'))['sources']
    by_id={book['id']:book for book in books}
    chapter=None; section=None
    for book in books:book['chapters']=[]
    for line in (DATA/'lessons.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('# '):book=by_id[line[2:].strip()]; chapter=None
        elif line.startswith('## '):
            title,diagram,sources=[v.strip() for v in line[3:].split('|')]
            chapter={'title':title,'diagram':diagram,'refs':sources.split(','),'sections':[],'table':[]}
            book['chapters'].append(chapter); section=None
        elif line.startswith('### '):
            section={'heading':line[4:],'paragraphs':[]}; chapter['sections'].append(section)
        elif line.strip() and section is not None:
            if section['heading']=='Comparison':chapter['table'].append([v.strip() for v in line.split('|')])
            else:section['paragraphs'].append(line.strip())
    for book in books:
        book['refs']=list(dict.fromkeys(r for c in book['chapters'] for r in c['refs']))
        for chapter in book['chapters']:
            if not all(r in refs for r in chapter['refs']):raise ValueError('Unknown chapter source')
    return books,refs

def paginate(chapter):
    lines=[]
    for section in chapter['sections']:
        if section['heading']=='Comparison':continue
        if lines and lines[-1]!='':lines.append('')
        lines.extend(textwrap.wrap(section['heading'].upper(),LINE_WIDTH))
        for paragraph in section['paragraphs']:
            lines.extend(textwrap.wrap(paragraph,LINE_WIDTH,break_long_words=False,break_on_hyphens=False))
    pages=['\n'.join(lines[i:i+PAGE_LINES]) for i in range(0,len(lines),PAGE_LINES)]
    return pages or ['']

def table_pages(chapter):
    """One material/technology per support page keeps every comparison field readable."""
    rows=chapter['table']
    if not rows:return []
    headers=rows[0]; pages=[]
    for row in rows[1:]:
        lines=[]
        for header,value in zip(headers,row):
            lines.extend(textwrap.wrap(header.upper(),LINE_WIDTH))
            lines.extend(textwrap.wrap(value,LINE_WIDTH));lines.append('')
        for i in range(0,len(lines),PAGE_LINES):pages.append('\n'.join(lines[i:i+PAGE_LINES]))
    return pages

def search(books,query):
    words=re.findall(r'\w+',query.casefold())
    if not words:return []
    hits=[]
    for bi,book in enumerate(books):
        for ci,chapter in enumerate(book['chapters']):
            body=' '.join(p for s in chapter['sections'] for p in s['paragraphs'])
            text=(book['title']+' '+chapter['title']+' '+body+' '+str(chapter['table'])).casefold()
            if all(word in text for word in words):hits.append((bi,ci))
    return hits

def safe_url(url):
    try:
        parts=urlsplit(url)
        return (parts.scheme=='https' and parts.hostname is not None
                and (parts.hostname=='nasa.gov' or parts.hostname.endswith('.nasa.gov'))
                and not parts.username and not parts.password and parts.port in (None,443)
                and not any(ord(c)<32 for c in url))
    except (TypeError,ValueError):return False

class ReferenceOpener:
    def __init__(self,refs,opener=None):
        self.refs=refs;self.opener=opener or webbrowser.open
        self.pool=ThreadPoolExecutor(max_workers=1);self.future=None
    def open(self,key):
        if key not in self.refs or not safe_url(self.refs[key]['url']):raise ValueError('Reference URL is not approved')
        if self.future is not None and not self.future.done():return False
        self.future=self.pool.submit(self.opener,self.refs[key]['url'],new=2);return True
    def close(self):self.pool.shutdown(wait=False,cancel_futures=True)

class ReadingPosition:
    def __init__(self,path=None):
        self.path=Path(path) if path else RUNTIME/'library-reading.json'
        try:
            data=json.loads(self.path.read_text(encoding='utf-8'))
            self.positions=data.get('positions',{}) if data.get('schema_version')==1 else {}
            if not isinstance(self.positions,dict):self.positions={}
        except (OSError,ValueError,TypeError,AttributeError):self.positions={}
    def get(self,key):
        position=self.positions.get(key,[0,0])
        if not isinstance(position,list) or len(position)!=2 or not all(type(v)is int and v>=0 for v in position):return 0,0
        return tuple(position)
    def save(self,key,chapter,spread):
        self.positions[key]=[chapter,spread]
        try:
            self.path.parent.mkdir(exist_ok=True,parents=True)
            temp=self.path.with_suffix('.tmp');temp.write_text(json.dumps({'schema_version':1,'positions':self.positions},indent=2),encoding='utf-8');temp.replace(self.path)
            return True
        except OSError:return False
