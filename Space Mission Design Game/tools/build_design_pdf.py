"""Rebuild the design document; authoring utility, not a game dependency.

Requires reportlab. Run from any directory with Python.
"""
from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Space Mission Design Game' / 'PHASED_DESIGN.md'
OUTPUT = ROOT / 'output' / 'pdf' / 'mission-forge-phased-design.pdf'
NAVY = colors.HexColor('#101E35')
TEAL = colors.HexColor('#007F91')
GRAY = colors.HexColor('#49576B')
LIGHT = colors.HexColor('#EDF4F7')
styles = {
    'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=25, leading=28, textColor=NAVY, spaceAfter=10),
    'subtitle': ParagraphStyle('subtitle', fontName='Helvetica', fontSize=12, leading=16, textColor=GRAY, spaceAfter=13),
    'heading': ParagraphStyle('heading', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=NAVY, spaceBefore=10, spaceAfter=5, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=13, textColor=NAVY, spaceAfter=7),
    'list': ParagraphStyle('list', fontName='Helvetica', fontSize=9.5, leading=13, textColor=NAVY, spaceAfter=5, leftIndent=10, firstLineIndent=-8),
    'cell': ParagraphStyle('cell', fontName='Helvetica', fontSize=8.4, leading=11.3, textColor=NAVY),
    'th': ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=8.4, leading=11.3, textColor=colors.white),
    'reference': ParagraphStyle('reference', fontName='Helvetica', fontSize=8, leading=10.5, textColor=GRAY, spaceAfter=6),
}

def markup(s):
    s = escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', s)
    # Short labels preserve clickable URLs without long source strings in print.
    s = re.sub(r'(https://\S+)', lambda m: '<link href="' + m.group(1) + '" color="#007F91">' + ('[open source]' if len(m.group(1)) > 42 else m.group(1)) + '</link>', s)
    return s

story = []
lines = SOURCE.read_text(encoding='utf-8').splitlines()
i = 0
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1
        continue
    if line == '---':
        story.append(PageBreak())
    elif line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            cells = [x.strip() for x in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[- :]+', x) for x in cells):
                rows.append(cells)
            i += 1
        n = len(rows[0])
        widths = [107,197,195] if n == 3 else [82,417]
        data = [[Paragraph(markup(c), styles['th' if r == 0 else 'cell']) for c in row] for r,row in enumerate(rows)]
        t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('ROWBACKGROUNDS',(0,1),(-1,-1),[LIGHT,colors.white]),('LINEBELOW',(0,0),(-1,0),1,TEAL)]))
        story.append(t)
        continue
    elif line.startswith('### '):
        story.append(Paragraph(markup(line[4:]), styles['heading']))
    elif line.startswith('## '):
        story.append(Paragraph(markup(line[3:]), styles['subtitle']))
    elif line.startswith('# '):
        story.append(Paragraph(markup(line[2:]), styles['title']))
    elif line.startswith('- '):
        story.append(Paragraph('- ' + markup(line[2:]), styles['list']))
    else:
        story.append(Paragraph(markup(line), styles['reference' if line.startswith('[S') else 'body']))
    i += 1

def frame(c, doc):
    w,h = doc.pagesize
    c.setFillColor(NAVY); c.rect(0,h-11,w,11,fill=1,stroke=0)
    c.setFont('Helvetica',7.6); c.setFillColor(GRAY)
    c.drawString(48,h-29,'MISSION FORGE  /  PHASED DESIGN  /  PROPOSED')
    c.setStrokeColor(colors.HexColor('#D7E2E8')); c.line(48,42,w-48,42)
    c.drawString(48,28,'14 November 2026  |  Single player first  |  Review after every phase')
    c.drawRightString(w-48,28,f'{doc.page}')

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
SimpleDocTemplate(str(OUTPUT), pagesize=(595,842), leftMargin=48,rightMargin=48,topMargin=48,bottomMargin=56,title='Mission Forge - 3D Game Phased Design',author='Mission Forge project team').build(story,onFirstPage=frame,onLaterPages=frame)
print(OUTPUT)
