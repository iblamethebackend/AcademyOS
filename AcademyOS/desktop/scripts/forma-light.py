from pathlib import Path
from bs4 import BeautifulSoup
import re
p=Path('public/landing-pages/forma-ai.html');s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
def color(m):
 h=m.group(1)
 if len(h) not in [3,6]:return m.group(0)
 if len(h)==3:h=''.join(c*2 for c in h)
 r,g,b=[int(h[i:i+2],16) for i in [0,2,4]]
 if max(r,g,b)-min(r,g,b)<48:
  v=(r+g+b)/3;v=int(245-v*.82);return '#%02x%02x%02x'%(max(0,v-5),v,max(0,v-4))
 if r>g and r>b and r>140:return '#6b8f7a'
 return m.group(0)
for style in s.find_all('style'):
 code=re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F])',color,style.string or '')
 code=re.sub(r'rgba\(\s*(?:244,236,222|255,255,255|255, 255, 255|242,240,233|238,236,231)', 'rgba(46,93,78',code)
 style.string=code
p.write_text(str(s),encoding='utf-8')
