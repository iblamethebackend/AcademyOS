from pathlib import Path
import json, re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image,ImageDraw,ImageFont
import pymupdf as fitz

root=Path(__file__).resolve().parents[1]
roles=json.loads((root/'mobile/workspaces.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('UI','C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('Bold','C:/Windows/Fonts/segoeuib.ttf'))
pdfmetrics.registerFontFamily('UI',normal='UI',bold='Bold')
W,H=1200,900;ink='#203B36';muted='#62726D';green='#256855'
c=canvas.Canvas(str(root/'AcademyOS-Design-Review.pdf'),pagesize=(W,H));c.setTitle('AcademyOS | Desktop & Mobile Design Review');page=0
def text(s,x,y,size=12,color=ink,font='UI'):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size,s)
def box(x,y,w,h,color,r=20):
 c.setFillColor(HexColor(color));c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=0)
def para(s,x,y,w,size=14,color=muted):
 p=Paragraph(s,ParagraphStyle('body',fontName='UI',fontSize=size,leading=size*1.5,textColor=HexColor(color)));_,h=p.wrap(w,900);p.drawOn(c,x,H-y-h)
def new(title,sub):
 global page
 if page:c.showPage()
 page+=1;box(0,0,W,H,'#F7F6F0',0);text('AcademyOS.',42,26,21,ink,'Bold');text('DESIGN REVIEW / 11 NOVEMBER 2026',850,34,10,muted,'Bold');text(title,42,82,34,ink,'Bold');text(sub,42,133,13,muted);text('AcademyOS · Fictional data · UI prototype',42,867,10,muted);text(str(page).zfill(2),1130,864,13,green,'Bold');c.bookmarkPage(str(page));c.addOutlineEntry(title,str(page),0)
def pic(name,x,y,w,h):
 f=root/'previews'/f'{name}.png';im=Image.open(f);iw,ih=im.size;scale=min(w/iw,h/ih);ww,hh=iw*scale,ih*scale
 box(x-3,y-3,ww+6,hh+6,'#DDE5D7',19);c.drawImage(str(f),x,H-y-hh,width=ww,height=hh)
new('More room for what matters.','A calmer desktop workspace. A more personal school day in your pocket.')
pic('desktop-overview',42,196,790,600);pic('mobile-parent',880,196,260,600)
new('01 / The desktop, reconsidered.','An open workspace, purposeful colour, generous type and a hierarchy that makes the next action obvious.')
pic('desktop-overview',130,182,940,680)
new('02 / A place for everything.','Role-aware navigation brings the relevant school modules together without exposing platform controls.')
pic('desktop-workspace',130,182,940,680)
new('03 / A welcoming first moment.','One visual language, from a quiet welcome screen to focused conversations.')
for name,x in [('mobile-welcome',62),('mobile-parent',439),('mobile-message',816)]:pic(name,x,188,300,650)
for i,r in enumerate(roles):
 new(f'{str(i+4).zfill(2)} / {r["name"]}',r['context']+' · '+r['headline'])
 slug=re.sub('[^a-z]+','-',r['name'].lower())
 pic('mobile-parent' if i==0 else 'mobile-'+slug,52,190,275,595)
 pic('mobile-modules' if i==0 else 'modules-'+str(i),357,190,275,595)
 box(674,190,474,595,'#FFFFFF')
 text('THE WORKSPACE',700,218,10,green,'Bold')
 para(' · '.join(r['modules']),700,249,416,16,ink)
 text('A CLEAR NEXT STEP',700,373,10,green,'Bold')
 para('<b>'+r['tasks'][0][0]+'</b><br/>'+r['tasks'][0][2],700,402,416,15)
 text('DESIGN BEHAVIOUR',700,568,10,green,'Bold')
 para('Today surfaces priorities. Workspace groups relevant modules. Inbox holds school conversations. You retains profile and school context.<br/><br/>Task details and preview review states work locally. Module sheets are navigation concepts, ready for the detailed service workflows.',700,595,416,13)
 text('TODAY',52,807,10,green,'Bold');text('WORKSPACE',357,807,10,green,'Bold')
new('22 / Glass with a purpose.','A restrained material system that gives content room to breathe.')
tokens=[('Ink','#203B36'),('Fern','#256855'),('Sage','#E3EEDB'),('Ivory','#F7F6F0'),('Sand','#F1E8D9'),('Lilac','#E9E5F0')]
for i,(name,color) in enumerate(tokens):
 x=42+i*190;box(x,191,168,91,color);text(name,x,300,16,ink,'Bold');text(color,x,328,12,muted)
for x,y,title,body in [(42,402,'Quiet surfaces','White content cards, soft colour in summary cards, and glass reserved for the floating navigation. Borders supply separation without heavy shadows.'),(630,402,'Native material, honest fallbacks','The Expo source uses BlurView on iOS. Reduced Transparency, Android and web receive a readable near-opaque surface. This is Apple-inspired glass, not a claim of native Liquid Glass.'),(42,612,'Type, touch and layout','System typography; 12–16 px content, 18–31 px headings. 44 px minimum icon controls, 52 px primary buttons. Desktop sidebar from 1000 px; compact bottom navigation below it.'),(630,612,'Scope of this handoff','Desktop blueprint: 23 static screen concepts. Expo: 18 role workspaces, shared navigation and local interactions. Authentication, real records, payment, messaging, uploads and approval workflows require backend implementation.')]:
 box(x,y,528,180,'#FFFFFF');text(title,x+22,y+20,18,ink,'Bold');para(body,x+22,y+57,482,14)
c.save()
doc=fitz.open(root/'AcademyOS-Design-Review.pdf');issues=[]
for i,p in enumerate(doc):
 for block in p.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   for span in line['spans']:
    r=fitz.Rect(span['bbox'])
    if r.x0<0 or r.y0<0 or r.x1>W or r.y1>H:issues.append({'page':i+1,'text':span['text']})
assert not issues,issues
(root/'design-verification.json').write_text(json.dumps({'pages':len(doc),'roles':len(roles),'bounds_issues':issues},indent=2))
names=['mobile-welcome','mobile-parent','mobile-student','mobile-teaching','mobile-finance','mobile-transport']
sheet=Image.new('RGB',(1800,1180),'#F7F6F0');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',46);d.text((40,30),'AcademyOS. A little more possibility.',font=font,fill=ink)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22)
for i,name in enumerate(names):
 im=Image.open(root/'previews'/f'{name}.png');im.thumbnail((270,950),Image.Resampling.LANCZOS);x=30+i*295;sheet.paste(im,(x,135));d.text((x,1040),name.removeprefix('mobile-').title(),font=small,fill=ink)
sheet.save(root/'AcademyOS-Mobile-Gallery.jpg',quality=94)
print(f'Design review: {len(doc)} pages, {len(roles)} workspaces, no out-of-page text.')
