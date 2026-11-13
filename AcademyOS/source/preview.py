from pathlib import Path
import fitz,json
from PIL import Image, ImageOps, ImageDraw
root=Path('deliverables')
doc=fitz.open(root/'AcademyOS-School-SaaS-Blueprint.pdf')
for page in [0,1,4,8,33,35,43,46,47,51,59,60,69,70]:
    pix=doc[page].get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False)
    pix.save(root/'previews'/f'page-{page+1:02}.png')
for start,end,name in [(0,35,'contact-spec-1'),(35,71,'contact-spec-2')]:
    sheet=Image.new('RGB',(1400,((end-start+3)//4)*270),'#dce1ea');d=ImageDraw.Draw(sheet)
    for j,p in enumerate(range(start,end)):
        pix=doc[p].get_pixmap(matrix=fitz.Matrix(.30,.30),alpha=False)
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        x=(j%4)*350+7;y=(j//4)*270+20
        sheet.paste(im,(x,y));d.text((x,y-15),f'{p+1:02}',fill='black')
    sheet.save(root/'previews'/f'{name}.png')
print('Rendered',len(doc),'pages; preview contact sheets ready.')
