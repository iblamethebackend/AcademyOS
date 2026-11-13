from pathlib import Path
from bs4 import BeautifulSoup,NavigableString,Comment
import re,json,hashlib
raw=Path('vendor/threeui-forma/public/landing-pages/forma-ai.html').read_text(encoding='utf-8')
s=BeautifulSoup(raw,'html.parser')
for e in s.select('.brand svg'):
 e.replace_with(BeautifulSoup('<img src="/brand/book-mark.svg" alt="" width="32" height="32">','html.parser'))
def html(q,v):
 e=s.select_one(q)
 if e:e.clear();e.append(BeautifulSoup(v,'html.parser'))
def txt(q,v):html(q,v)
# Preserve all authored animation hooks and timeline structures.
for e in s.select('.brand'):
 for n in list(e.children):
  if isinstance(n,NavigableString):n.replace_with('AcademyOS')
html('#hero-heading','<span class="line"><span>One connected school.</span></span><span class="line"><span><em>Endless possibility.</em></span></span>')
html('.hero-description','Bring your people, your plans and your campus together.<br> A smarter school day starts with a thoughtful foundation.')
html('.announcement','<span>ACADEMYOS / 01</span> A new chapter for your school <span aria-hidden="true">↗</span>')
s.select_one('#prompt')['placeholder']='Your school name';s.select_one('#prompt')['aria-label']='Your school name';s.select_one('#prompt')['maxlength']='100'
html('label[for="prompt"]','Your school name')
html('.build-button','Register your school ↗')
html('#hero-style','<option value="editorial">School workspace</option>');s.select_one('#hero-style')['aria-label']='Workspace type'
for b,label in zip(s.select('[data-prompt]'),['School owners','Parents & students','Teachers & teams']):b.clear();b.append(label);b['data-audience']=label
html('.hero-note','School workspace available. Parent, student and staff experiences planned.')
html('.coordinates','A smarter campus. A calmer day.')
html('.assembly .eyebrow','01 / Your school, coming together')
for i,(a,b) in enumerate([('A whole community.','One shared purpose.'),('Every team. Every detail.','Finding their place.'),('One school workspace.','Entirely your own.')]):html('[data-assembly-title="'+str(i)+'"]',a+'<br><span class="soft">'+b+'</span>')
s.select_one('#assembly-heading')['aria-label']='Your community becomes one connected school workspace.'
html('.assembly-aside p','<b>From the first classroom<br>to the front office.</b><br>Watch your school’s foundations come together, one considered detail at a time.')
html('.brief-fragment','<small>YOUR SCHOOL’S NEXT CHAPTER ↗</small><p>Our people. Our plans.<br>One connected school.<i class="brief-caret"></i></p>')
html('.assembled-nav','<b>AcademyOS</b><span>Overview &nbsp; People &nbsp; Academics</span>')
html('.assembled-content','<small>YOUR SCHOOL WORKSPACE</small><h3>Good mornings.<br><span>Better beginnings.</span></h3><p>Your campuses, academic year and people.<br>Beautifully together.</p><span class="assembled-cta">School workspace &nbsp; ↗</span>')
html('.assembly-chrome','<span>AcademyOS / School workspace</span><span>Desktop · Preview</span><span class="chrome-ready">● Your school foundations</span>')
# Use the original responsive three-stage product story for real school setup.
html('#story-heading','Your school.<br><em>Every detail, considered.</em>')
for e,(k,h,p) in zip(s.select('.step'),[('01 / REGISTER','Make it official.','Create your school owner account and verify your email.'),('02 / PERSONALISE','Make it your school.','Add campuses, academic foundations, student records, staff and branding.'),('03 / GET STARTED','A clearer school day.','Follow your setup checklist and explore your school workspace.')]):
 e.select_one('.step-number').string=k;e.select_one('h3').string=h;e.select_one('p').string=p
html('.editor-brand','School setup <span class="assistant-status"></span>');html('.chat-prompt','One school workspace for our campuses, academic year, team and student records.');html('.chat-response','<strong>Your school. Your identity.</strong><br>A clear foundation for everything that comes next.');html('.build-checks','<span>School profile</span><span>Academic year</span><span>People & departments</span>');html('.editor-file','<span>School workspace<small>Ready to personalise</small></span>');html('.chat-input','Your next setup step <span>↑</span>');html('.editor-url','AcademyOS / School workspace');html('.publish-mini','School preview');html('.mini-nav','<b>AcademyOS</b><span>Overview &nbsp; People &nbsp; Academics</span>');html('.editor-collection-label','ONE COMMUNITY / ONE SHARED PURPOSE');html('.editor-viewport h3','Your school.<br><em>More connected.</em>');html('.editor-viewport p','A place for your people and your plans.<br>Make room for what matters.');html('.tiny-cta','Explore your workspace ↗');html('.export-card h4','Your next chapter is ready.');html('.export-card p','Start with a verified school owner account.');html('.export-card button','Register your school ↗')
html('#manifesto-text','A school is more than a place. It is the people, the learning, and the small moments that make every day matter.')
html('.manifesto .eyebrow','Less friction. More school.')
# Retain authored illustration cards, adapted to the platform.
for e,(h,p) in zip(s.select('.feature'),[('Your school. Your identity.','School branding, campuses, calendars and preferences available in your workspace.'),('One community. Every screen.','Parent, student, teacher and department mobile experiences are planned. The Expo UI prototype is in progress.'),('Your operations, connected.','Admissions, attendance, learning, fees, reporting and campus services are on the roadmap.')]):
 if e.select_one('h3'):e.select_one('h3').string=h
 if e.select_one('p'):e.select_one('p').string=p
html('#features-heading','Thoughtful foundations.<br><em>A connected future.</em>')
# Replace pricing with factual delivery stages; retain hidden hooks used by authored JS.
html('.pricing .section-head h2','Built step by step.<br><em>Clear about what’s next.</em>');html('.pricing .eyebrow','PRODUCT ROADMAP')
for e,(h,p,items) in zip(s.select('.price-card'),[('Available now','Your school foundation',['Owner registration & sign-in','School profile & campuses','Academic year, grades & subjects','Basic student & staff directories','Departments, branding & setup checklist']),('Planned modules','Daily school operations',['Admissions, attendance & timetables','Learning, examinations & reports','Fees, payments, accounts & HR','Communication & campus services']),('Mobile experience','UI prototype in progress',['Parent & student experiences','Teacher & department workflows','React Native / Expo app','iOS and Android planned'])]):
 e.select_one('h3').string=h;e.select_one('.plan-description').string=p;html_selector=e.select_one('ul');html_selector.clear()
 for item in items:t=s.new_tag('li');t.string=item;html_selector.append(t)
 e.select_one('[data-plan]').string='Explore all features ↗'
html('.pricing-note','Planned features are not yet operational. Release dates will be shared as each module is ready. No pricing has been announced.')
faq=[('What is available today?','School owner accounts, school profiles, campuses, academic foundations, basic student and staff directories, departments, branding and a guided setup checklist.'),('How do I register my school?','Choose Register your school, create your owner account, verify your email and add your school details. Then follow the workspace checklist.'),('Can parents, students and teachers join?','These dedicated account experiences and invitation activation are planned. The mobile UI prototype is in progress; operational access is still being developed.'),('When will the remaining modules launch?','AcademyOS is being built module by module. Browse the full feature directory for current and planned capabilities. Dates have not been announced.')]
for e,(q,a) in zip(s.select('.faq details'),faq):e.select_one('summary').string=q;e.select_one('p').string=a
html('.final-copy h2','One school.<br><em>Every possibility.</em>');html('.final-copy p','Bring your people and your plans together.<br>Your school’s next chapter starts here.');html('.footer-large','AcademyOS');html('.footer-bottom','<span>© 2026 AcademyOS. A smarter campus for modern schools.</span><span>Made for your school’s next chapter.</span>')
for e in s.select('[data-start]'):e.clear();e.append('Register your school ↗')
for a in s.select('a[href="#pricing"]'):a.string='Roadmap'
for a in s.select('a[href="#showcase"]'):a.string='Features';a['href']='#academy-features'
# Detailed feature content comes from our existing product inventory.
features=re.findall(r"\{name:'([^']+)',description:'([^']+)'(,available:true)?\}",Path('src/components/landing-features.tsx').read_text(encoding='utf-8'))
section=s.new_tag('section',id='academy-features');section['class']='wrap academy-features'
section.append(BeautifulSoup('<div class="section-head"><div><div class="eyebrow">THE COMPLETE PICTURE</div><h2>Every part of school.<br><em>Considered.</em></h2></div><p>Available foundations. A clearly labelled roadmap.</p></div><div class="academy-filter"><button data-status="all" aria-pressed="true">All features</button><button data-status="available" aria-pressed="false">Available now</button><button data-status="planned" aria-pressed="false">Planned</button></div><div class="academy-feature-grid"></div>','html.parser'))
for name,description,available in features:
 status='available' if available else 'planned';section.select_one('.academy-feature-grid').append(BeautifulSoup(f'<details data-status="{status}"><summary>{name}<small>{status.capitalize()}</small></summary><p>{description}</p></details>','html.parser'))
s.select_one('.showcase').insert_after(section)
# Local adapter runs before authored handlers to route product actions correctly.
adapter=s.new_tag('script');adapter.string="""
(()=>{function navigate(path){parent.postMessage({type:'academyos:navigate',path},'*')}
document.addEventListener('submit',e=>{if(e.target.id==='prompt-form'){e.preventDefault();e.stopImmediatePropagation();navigate('/register-school')}},true);
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
if(b.matches('[data-start],.export-card button')){e.preventDefault();e.stopImmediatePropagation();navigate('/register-school')}
if(b.matches('[data-prompt]')){e.preventDefault();e.stopImmediatePropagation();navigate(b.dataset.audience==='School owners'?'/register-school':'/login')}
if(b.matches('[data-plan],[data-template]')){e.preventDefault();e.stopImmediatePropagation();document.querySelector('#academy-features').scrollIntoView({behavior:'smooth'})}
if(b.matches('.academy-filter button')){document.querySelectorAll('.academy-filter button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('.academy-feature-grid details').forEach(x=>x.hidden=b.dataset.status!=='all'&&x.dataset.status!==b.dataset.status)}
},true);
})();
""";s.body.insert(0,adapter)
# Preserve scripts; recolour their particles for readable contrast on light backgrounds.
for script in s.find_all('script'):
 if script.string:
  code=script.string
  for old in ['238,190,145','179,186,202','234,186,140','164,171,187','203,181,156','211,189,164','217,182,147','237,189,142']:code=code.replace(old,'65,110,81')
  script.string=code
s.title.string='AcademyOS · A smarter campus'
for e in s.select('.mini-nav'):
 e.clear();e.append(BeautifulSoup('<b>AcademyOS</b><span>Overview &nbsp; People &nbsp; Academics</span>','html.parser'))
for e in s.select('.editor-page-foot'):
 e.clear();e.append(BeautifulSoup('<span>MADE FOR YOUR SCHOOL.</span><span>ONE CONNECTED COMMUNITY</span>','html.parser'))
# The authored page contains complete styling; light overrides are kept separate.
link=s.new_tag('link',rel='stylesheet',href='/landing-pages/academyos-light.css');s.head.append(link)
# Generic source labels outside scripts.
for node in list(s.find_all(string=True)):
 if isinstance(node,Comment):continue
 if node.parent.name in ['script','style']:continue
 t=re.sub(r'\bforma\b','AcademyOS',str(node),flags=re.I).replace('Your idea. Beautifully realized.','Your school. Beautifully connected.').replace('A blank canvas. A world of possibility.','A smarter campus. A more connected school day.')
 if t!=str(node):node.replace_with(t)
from feature_explorer import install
install(s)
Path('public/landing-pages/forma-ai.html').write_text(str(s),encoding='utf-8')
print('Adapted authored source. Feature entries:',len(features))
