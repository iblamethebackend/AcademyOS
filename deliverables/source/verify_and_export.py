from pathlib import Path
import json, csv, re, zipfile
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parents[1]
pdf=root/'CampusOS-School-SaaS-Blueprint.pdf'
doc=fitz.open(pdf)
pages=json.loads((root/'page-map.json').read_text())
records=list(csv.DictReader((root/'CampusOS-Requirements.csv').open(encoding='utf-8-sig')))
text='\n'.join(p.get_text() for p in doc)
issues=[]
for i,page in enumerate(doc,1):
    if not page.get_text().strip():issues.append(f'Blank page {i}')
    for block in page.get_text('dict')['blocks']:
        if 'lines' not in block:continue
        for ln in block['lines']:
            for span in ln['spans']:
                r=fitz.Rect(span['bbox'])
                if r.x0 < -1 or r.y0 < -1 or r.x1 > page.rect.width+1 or r.y1 > page.rect.height+1:
                    issues.append(f'Out-of-page text {i}: {span["text"][:60]}')
for row in records:
    if row['Requirement ID'] not in text:issues.append('Missing requirement '+row['Requirement ID'])
assert len(doc)==71
assert len(records)==144 and len({r['Requirement ID'] for r in records})==144
assert len(doc.get_toc())==71
assert sum(1 for p in pages if re.match(r'S\d\d /',p['title']))==23
assert len(doc[1].get_links())==4
assert len(doc[-1].get_links())==5
assert json.loads((root/'source/layout-check.json').read_text())==[]
screens=root/'screens';screens.mkdir(exist_ok=True)
for meta in pages:
    if re.match(r'S\d\d /',meta['title']):
        p=doc[meta['page']-1]
        pix=p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
        slug=re.sub('[^a-z0-9]+','-',meta['title'].lower()).strip('-')
        pix.save(screens/(slug+'.png'))
# A compact contact sheet of every screen for quick review.
thumb_w=504;thumb_h=357
sheet=Image.new('RGB',(1560,8*393+68),'#E9ECF3')
draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',23)
draw.text((20,17),'CampusOS | 23 screen concepts',fill='#18243D',font=font)
for j,f in enumerate(sorted(screens.glob('*.png'))):
    im=Image.open(f);im.thumbnail((thumb_w,thumb_h),Image.Resampling.LANCZOS)
    xx=16+(j%3)*520;yy=65+(j//3)*393
    sheet.paste(im,(xx,yy));draw.text((xx+2,yy+360),f.stem[:3].upper(),fill='#6553D9',font=font)
sheet.save(root/'CampusOS-Screen-Gallery.jpg',quality=92)
report=dict(pdf_pages=len(doc),functional_modules=24,unique_requirements=len(records),screen_concepts=23,pdf_bookmarks=len(doc.get_toc()),contents_links=4,source_links=5,layout_warnings=0,bounds_and_completeness_issues=issues,pdf_bytes=pdf.stat().st_size,validation='Document validation only; no application has been implemented or tested.')
(root/'verification-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if issues:raise SystemExit(1)

