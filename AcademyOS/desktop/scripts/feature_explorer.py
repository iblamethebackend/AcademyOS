from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import re

def install(s):
 source=Path('src/components/landing-features.tsx').read_text(encoding='utf-8')
 groups=re.findall(r"\{name:'([^']+)',icon:'([^']+)',features:\[(.*?)\]\}",source,re.S)
 labels=['School essentials','Student journey','Teaching & learning','Finance & people','Campus life','Community']
 descriptions=['A strong start. A school that feels like yours.','Every learner has a story. Keep the whole picture.','More space for teaching. A clearer path for learning.','Keep the work behind your school moving forward.','Care for everything that makes a campus a community.','Bring every family, teacher and team closer together.']
 paths=['M4 21V9l8-6 8 6v12M2 21h20M9 21v-7h6v7M9 9h6','M3 9l9-5 9 5-9 5-9-5Zm4 3v6c3 3 7 3 10 0v-6M21 9v8','M12 6c-3-3-7-3-10-3v15c4 0 7 0 10 3 3-3 6-3 10-3V3c-3 0-7 0-10 3Zm0 0v15','M4 7h16v14H4zM7 7V3h10v4M4 12h16M10 12v3h4v-3','M3 21h18M5 21V7h7v14M12 12h7v9M7 10h2M7 14h2M15 15h2M7 18h2','M15 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM5 21v-3a7 7 0 0 1 14 0v3M19 4a3 3 0 0 1 0 6M21 14l1 5']
 tabs=[];panels=[]
 for i,(name,icon,raw) in enumerate(groups):
  features=re.findall(r"\{name:'([^']+)',description:'([^']+)'(,available:true)?\}",raw)
  svg=f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{paths[i]}"/></svg>'
  tabs.append(f'<button class="fx-tab" id="fx-tab-{i}" role="tab" aria-selected="{str(i==0).lower()}" aria-controls="fx-panel-{i}" tabindex="{0 if i==0 else -1}"><span class="fx-icon">{svg}</span><strong>{labels[i]}</strong><span class="fx-tab-meta">0{i+1} <span>{len(features)} modules ↗</span></span></button>')
  rows=[]
  for title,description,available in features:
   rows.append(f'<details class="fx-module"><summary><span>{escape(title)}</span><small class="fx-status {"is-live" if available else ""}">{"Available now" if available else "Planned"}</small><span class="fx-plus" aria-hidden="true">+</span></summary><p>{escape(description)}</p></details>')
  live=sum(bool(f[2]) for f in features)
  panels.append(f'<div class="fx-panel" id="fx-panel-{i}" role="tabpanel" aria-labelledby="fx-tab-{i}" tabindex="0" {"hidden" if i else ""}><div class="fx-intro"><span class="fx-chapter">CHAPTER / 0{i+1}</span><h3>{escape(name)}</h3><p>{descriptions[i]}</p><div class="fx-orbit" aria-hidden="true"><i></i><i></i><span>{svg}</span><b>AcademyOS</b></div><span class="fx-panel-count">{live} available · {len(features)-live} planned</span></div><div class="fx-modules"><div class="fx-list-label"><span>EXPLORE THE MODULES</span><span>CLICK TO DISCOVER</span></div>{"".join(rows)}</div></div>')
 markup=f'''<section class="wrap academy-features fx" id="academy-features" aria-labelledby="fx-heading"><div class="fx-heading"><div><div class="eyebrow">ONE SCHOOL. A WORLD OF POSSIBILITIES.</div><h2 id="fx-heading">Big picture.<br><em>Every little detail.</em></h2></div><div class="fx-heading-aside"><p>From the first hello to the final bell.<br>Explore a more connected school day.</p><div class="fx-stats"><span><strong>06</strong> connected areas</span><span><strong>29</strong> thoughtful modules</span></div></div></div><div class="fx-tabs" role="tablist" aria-label="School feature areas">{''.join(tabs)}</div><div class="fx-panels">{''.join(panels)}</div><div class="fx-footnote"><span><i></i> Built today. Growing with you.</span><p>Available modules cover the current school workspace. Planned features are in development; release dates will be shared as they’re ready.</p></div></section>'''
 s.select_one('#academy-features').replace_with(BeautifulSoup(markup,'html.parser'))
 s.head.append(s.new_tag('link',rel='stylesheet',href='/landing-pages/feature-explorer.css'))
 script=s.new_tag('script',src='/landing-pages/feature-explorer.js',defer=True);s.body.append(script)
