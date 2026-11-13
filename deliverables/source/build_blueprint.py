from pathlib import Path
import math, json, csv
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from requirements import MODULES, SOURCES

ROOT=Path(__file__).resolve().parents[1]
W,H=1120,792
for n,f in [('UI','segoeui.ttf'),('Bold','segoeuib.ttf'),('Light','segoeuil.ttf')]:
    pdfmetrics.registerFont(TTFont(n,'C:/Windows/Fonts/'+f))
pdfmetrics.registerFont(TTFont('Symbols','C:/Windows/Fonts/seguisym.ttf'))
pdfmetrics.registerFontFamily('UI',normal='UI',bold='Bold',italic='UI',boldItalic='Bold')
INK='#18243D'; MUTED='#657188'; PURPLE='#6553D9'; LAV='#EFEDFF'; BG='#F6F7FB'; LINE='#E5E8F0'; GREEN='#087C67'; PALE='#E9F7F2'; AMBER='#976009'; ROSE='#B44562'; WHITE='#FFFFFF'; NAV='#1D2542'
c=canvas.Canvas(str(ROOT/'CampusOS-School-SaaS-Blueprint.pdf'),pagesize=(W,H),pageCompression=1)
c.setTitle('CampusOS | Complete India-first K–12 School SaaS Blueprint')
c.setAuthor('Prepared for Gaurav Sharma')
c.setSubject('Product requirements, SaaS architecture, implementation plan and high-fidelity screen designs')
pages=[]; errors=[]
def col(v): return HexColor(v)
def rect(x,y,w,h,fill=WHITE,r=0,stroke=None):
    c.setFillColor(col(fill))
    c.setStrokeColor(col(stroke or fill))
    if r:c.roundRect(x,H-y-h,w,h,r,stroke=bool(stroke),fill=1)
    else:c.rect(x,H-y-h,w,h,stroke=bool(stroke),fill=1)
def line(x,y,x2,y2,color=LINE,width=1):
    c.setStrokeColor(col(color));c.setLineWidth(width);c.line(x,H-y,x2,H-y2)
def text(s,x,y,size=12,color=INK,font='UI',align='left'):
    s=str(s)
    runs=[]
    for ch in s:
        actual=font if ord(ch) in pdfmetrics.getFont(font).face.charToGlyph else 'Symbols'
        if runs and runs[-1][0]==actual:runs[-1]=(actual,runs[-1][1]+ch)
        else:runs.append((actual,ch))
    width=sum(pdfmetrics.stringWidth(v,f,size) for f,v in runs)
    if align=='right':x-=width
    elif align=='center':x-=width/2
    c.setFillColor(col(color))
    for f,v in runs:
        c.setFont(f,size);c.drawString(x,H-y-size,v);x+=pdfmetrics.stringWidth(v,f,size)
def para(s,x,y,w,size=13,color=INK,leading=None,maxh=None):
    st=ParagraphStyle('p',fontName='UI',fontSize=size,leading=leading or size*1.45,textColor=col(color),spaceAfter=0)
    p=Paragraph(s,st);pw,ph=p.wrap(w,1000)
    if maxh and ph>maxh+1:errors.append((len(pages),s[:70],round(ph),maxh))
    p.drawOn(c,x,H-y-ph);return ph
def circle(x,y,r,fill):
    c.setFillColor(col(fill));c.circle(x,H-y,r,fill=1,stroke=0)
def chip(s,x,y,color=PURPLE,bg=LAV):
    width=pdfmetrics.stringWidth(s,'Bold',9.5)+20
    rect(x,y,width,23,bg,11);text(s,x+10,y+5,9.5,color,'Bold');return width
def heading(s,x,y,w=480):
    return para('<b>'+escape(s)+'</b>',x,y,w,18,INK,23)
def card(title,body,x,y,w,h=150,fill=BG):
    rect(x,y,w,h,fill,14)
    if h < 140:
        text(title,x+18,y+12,14,INK,'Bold')
        top=36 if h < 95 else 38
        sz=10.5 if h < 95 else 11
        lead=14 if h < 95 else 15
        para(body,x+18,y+top,w-36,sz,MUTED,lead,maxh=h-top-5)
    else:
        heading(title,x+22,y+20,w-44)
        para(body,x+22,y+54,w-44,12.5,MUTED,18,maxh=h-66)
def bullets(items,x,y,w,size=13,gap=13):
    for item in items:
        circle(x+3,y+9,2.5,PURPLE)
        ph=para(item,x+17,y,w-17,size,INK,size*1.4)
        y+=ph+gap
    return y
def newpage(title,section='Product blueprint',subtitle='',dark=False):
    if pages:c.showPage()
    pages.append(dict(title=title,section=section,page=len(pages)+1))
    rect(0,0,W,H,NAV if dark else WHITE)
    c.bookmarkPage('p'+str(len(pages)))
    c.addOutlineEntry(title,'p'+str(len(pages)),0,False)
    if not dark:
        text('CAMPUS',48,25,12,PURPLE,'Bold');text('OS',99,25,12,INK,'Bold')
        text(section.upper(),1072,27,9,MUTED,'Bold','right')
        line(48,53,1072,53)
        text(title,48,73,31,INK,'Bold')
        if subtitle:para(subtitle,48,118,1000,12.5,MUTED,18,maxh=40)
        line(48,748,1072,748)
        text('CAMPUSOS  /  PRODUCT & EXPERIENCE BLUEPRINT  /  10 NOV 2026',48,762,8.5,MUTED)
        text(str(len(pages)).zfill(2),1072,758,12,PURPLE,'Bold','right')
    return len(pages)
def table(headers,rows,x=48,y=180,width=1024,ratios=None,rowh=47,size=11.5):
    ratios=ratios or [1]*len(headers); widths=[width*r/sum(ratios) for r in ratios]
    rect(x,y,width,36,NAV,7)
    xx=x
    for h,ww in zip(headers,widths): text(h,xx+12,y+10,10,WHITE,'Bold');xx+=ww
    y+=36
    for i,row in enumerate(rows):
        rect(x,y,width,rowh,WHITE if i%2 else BG)
        xx=x
        for val,ww in zip(row,widths):
            offset=min(11,(rowh-size*1.35)/2)
            para(str(val),xx+12,y+offset,ww-24,size,INK,size*1.35,maxh=rowh-offset-3);xx+=ww
        line(x,y+rowh,x+width,y+rowh)
        y+=rowh
    return y
def flow(labels,x,y,w):
    gap=13;boxw=(w-gap*(len(labels)-1))/len(labels)
    for i,l in enumerate(labels):
        rect(x+i*(boxw+gap),y,boxw,52,LAV,9)
        para('<b>'+l+'</b>',x+i*(boxw+gap)+12,y+12,boxw-24,11.5,PURPLE,15)
        if i<len(labels)-1:text('›',x+(i+1)*boxw+i*gap+3,y+11,21,PURPLE)
def note(body,y=682): 
    rect(48,y,1024,44,LAV,10);para(body,64,y+12,992,11,PURPLE,15,maxh=24)

def cover():
    newpage('A calmer school day.','Cover',dark=True)
    circle(1060,80,290,'#293253');circle(1050,80,220,'#353C67');circle(1050,80,145,'#514A9C')
    text('CAMPUSOS',58,44,19,'#CEC8FF','Bold')
    chip('INDIA-FIRST  /  K–12  /  MULTI-TENANT SAAS',58,100,'#D9D4FF','#333855')
    text('A calmer',55,155,73,WHITE,'Light');text('school day.',55,234,73,WHITE,'Bold')
    para('The complete product, engineering<br/>and experience blueprint.',59,341,570,24,'#D7DCEB',34)
    para('One connected system for school leaders, teachers,<br/>families and the teams who keep everything running.',59,434,590,15,'#B9C3D8',23)
    for i,(v,l) in enumerate([('24','feature domains'),('23','screen concepts'),('144','requirements')]):
        xx=60+i*202;text(v,xx,540,34,WHITE,'Bold');text(l,xx,586,12,'#BAC4D9')
    rect(738,296,309,355,WHITE,22)
    text('Your school, in focus',762,321,18,INK,'Bold');text('Tuesday, 10 November',762,350,10,MUTED)
    rect(762,384,120,76,LAV,12);text('Attendance',777,398,10,MUTED);text('95.8%',777,419,25,PURPLE,'Bold')
    rect(895,384,127,76,PALE,12);text('Collections',910,398,10,MUTED);text('₹ 18.4L',910,419,24,GREEN,'Bold')
    text('A little more progress, every day',762,483,11,INK,'Bold')
    for i,bh in enumerate([34,48,43,64,56,80,94,84]):
        rect(764+i*33,610-bh,19,bh,PURPLE if i>5 else '#DAD5FA',5)
    text('PRODUCT REQUIREMENTS + UI DESIGN + DELIVERY PLAN',59,712,10,'#CEC8FF','Bold')
    text('V1.0   •   10 NOVEMBER 2026',1062,713,10,'#BAC4D9','UI','right')

def intro():
    newpage('A complete plan, built to be used.','Read this first','An implementation blueprint and visual design direction. All screen data and school names are fictional.')
    card('What this deliverable contains','A prioritized feature catalogue with stable IDs; business rules and acceptance checks; SaaS operations; technical architecture; data and API contracts; and 23 designed screens.',48,177,498,154)
    card('How to read the priorities','<b>P0 — launch:</b> a usable, secure school product.<br/><b>P1 — expansion:</b> deeper operations and automation.<br/><b>P2 — optional:</b> enterprise and specialist modules.<br/>Priorities indicate sequence, not missing scope.',566,177,506,154)

    card('Working assumptions','India-first K–12; independent schools and school groups; responsive web first; English at launch with localization foundations; INR and Asia/Kolkata defaults; configurable school calendars.',48,351,498,169)
    card('What still needs validation','Confirm pilot school workflows, board-specific templates, fee/refund policies, legal applicability, retention periods, scale and provider contracts. Mockups are design targets; they are not a functioning application.',566,351,506,169)
    heading('Navigate the blueprint',48,551)
    # Contents ranges filled from fixed section order; final page map is exported as JSON.
    table(['PART','CONTENTS'],[
      ['01 / Product · 3–8','Scope, roles, permissions, navigation, journeys and commercial model'],
      ['02 / Requirements · 9–32','24 modules • 144 requirements with rules and acceptance checks'],
      ['03 / Engineering · 33–44','Architecture, data, APIs, security, delivery and operational readiness'],
      ['04 / Experience · 45–71','Design system, 23 screen concepts, state patterns and sources']
    ],y=588,rowh=27,size=10.5,ratios=[1.3,4])
    for i,target in enumerate([3,9,33,45]):
        c.linkRect('', 'p'+str(target), (48,H-(624+(i+1)*27),1072,H-(624+i*27)),relative=0,thickness=0)

    newpage('Built around the whole school.','01 / Product strategy','A single operational record with purposeful experiences for each role.')
    card('Customer & job to be done','Sell to school owners and groups; support principals, administrators and staff as daily users. Families receive a simple portal for learning, communication and payments.',48,180,498,157)
    card('Product boundaries','Support the full student lifecycle and a commercial SaaS operating model. Launch with a fee subledger; grow into deeper finance, payroll and operations after validated core workflows.',566,180,506,157)
    heading('Success measures • proposed pilot targets',48,366)
    table(['OUTCOME','MEASURE','INITIAL TARGET'],[
      ['Reliable start','Required setup checklist completed','100% before go-live'],
      ['Daily adoption','Class registers finalized by school cutoff','≥ 95% on school days'],
      ['Financial clarity','Provider captures with one matched receipt','100%; exceptions owned'],
      ['Family access','Invited guardians who complete activation','≥ 80% within 30 days'],
      ['Operational value','Monthly reconciliation time vs baseline','30% reduction in pilot'],
      ['Trust','Cross-tenant exposure / duplicate postings','0 accepted defects']
    ],y=406,rowh=43,ratios=[1.2,2,1.5])
    note('Targets are proposed acceptance hypotheses, not measured product results. Baseline and approve them with pilot schools.',706)

    newpage('The right workspace for each role.','01 / People & accountability','Role templates reduce setup effort; scoped permissions remain the source of truth.')
    table(['ROLE','PRIMARY JOB','DEFAULT SCOPE'],[
      ['School owner / group leader','School configuration, governance and campus comparison','Authorized tenant or school group'],
      ['Principal / academic coordinator','Daily exceptions, approvals, curriculum and outcomes','Assigned campuses'],
      ['Registrar / admissions officer','Applications, records, enrolment and certificates','Assigned campuses / admissions intake'],
      ['Teacher / substitute','Attendance, lessons, homework and assigned marks','Assigned classes, subjects and dates'],
      ['Finance officer / accountant','Fees, collection, reconciliation and close','Assigned finance scope; no counselling notes'],
      ['HR / payroll approver','Employment, leave, salary and payroll approval','Restricted staff fields'],
      ['Librarian / transport / office','Operate assigned campus services','Relevant service records only'],
      ['Nurse / safeguarding lead','Care, sensitive cases and emergency escalation','Explicit care/case permissions'],
      ['Guardian / student','Own family tasks / own learning and results','Verified relationship / own record'],
      ['SaaS operator / support','Subscriptions, service health and approved assistance','Metadata; temporary approved data access']
    ],y=178,rowh=47,ratios=[1.3,2.1,1.65],size=11.5)
    note('Custom roles cannot grant permissions their creator does not hold. Temporary assignments expire automatically.',700)

    newpage('Permissions are a product feature.','01 / Authorization model','Template matrix: every allowance is further constrained by tenant, campus, relationship and field rules.')
    table(['ACTION','OWNER','PRINCIPAL','TEACHER','FINANCE','GUARDIAN','SUPPORT'],[
      ['Manage tenant settings','Manage','Delegated','—','—','—','Grant only'],
      ['View student basics','Scoped','Scoped','Assigned','Minimum','Own child','Grant only'],
      ['Finalize attendance','Delegated','Approve','Assigned','—','View own','—'],
      ['Publish final results','Delegated','Approve','Submit','—','View own','—'],
      ['Post fee receipt','Delegated','View','—','Manage','View own','—'],
      ['Approve refund','If separate','If delegated','—','If separate','Request','—'],
      ['Read clinical/case notes','Explicit only','Explicit only','Care alert','—','Reviewed','—'],
      ['Read salary/bank fields','Explicit HR','Explicit HR','Own','Explicit HR','—','—'],
      ['Bulk export child data','Step-up','Scoped','Restricted','Finance only','Own child','Grant only']
    ],y=180,rowh=46,ratios=[2.1,1,1,1,1,1,1],size=10.5)
    card('Enforcement contract','Server action permission + row scope + field scope + current relationship. Re-check on asynchronous execution and file download; log sensitive operations.',48,662,1024,69)
    # Compact card uses custom text placement instead.
    
    newpage('Navigation with clear boundaries.','01 / Information architecture','Desktop favors operational density. Mobile favors one child, one class or one task at a time.')
    groups=[
      ('School workspace','Overview • Admissions • Students • Academics • Timetable • Attendance • Learning • Examinations • Fees • Payments'),
      ('People & operations','Staff • Payroll • Messages • Meetings • Transport • Library • Inventory • Health • Visitors • Helpdesk • Reports'),
      ('Administration','School & campuses • Academic years • Roles • Imports • Integrations • Audit log • Branding • Subscription • Privacy'),
      ('Family & student','Today • Children • Timetable • Homework • Results • Attendance • Fees • Messages • Requests • Profile'),
      ('SaaS control plane','Tenants • Plans & usage • Billing • Onboarding • Service health • Support grants • Jobs • Incidents • Feature flags')
    ]
    y=181
    for i,(t,b) in enumerate(groups):
        rect(48,y,48,73,LAV,10);text(str(i+1).zfill(2),72,y+23,20,PURPLE,'Bold','center')
        heading(t,118,y+2,900);para(b,118,y+32,935,13,MUTED,19);y+=104
    note('Every screen preserves current tenant, campus and academic year. Search obeys the same permissions as the underlying records.',710)

    newpage('Five journeys that must work end to end.','01 / Service journeys','The exception path receives the same implementation attention as the happy path.')
    flows=[

      ('01 / A school goes live',['Verify owner','Configure year','Import & review','Invite users','Readiness check'],'Recovery: invalid import rows stay in quarantine; activation waits for required setup.'),
      ('02 / A pupil joins',['Enquiry','Application','Offer / seat','Verified deposit','Enrol & invite'],'Recovery: expired offers and full classes route to review or waitlist.'),
      ('03 / A school day starts',['Open roster','Mark & review','Submit register','Notify absence','Correct / audit'],'Recovery: offline edits sync with conflict resolution; unmarked never becomes absent.'),
      ('04 / A family pays',['Select invoice','Hosted payment','Verify capture','Post receipt','Reconcile bank'],'Recovery: delayed webhooks show pending; retries cannot duplicate receipts.'),
      ('05 / A year closes',['Finalize results','Approve reports','Reconcile fees','Preview promotion','Commit new year'],'Recovery: exceptions remain in review; prior reports and enrolments stay intact.')
    ]
    y=178
    for t,labels,n in flows:
        text(t,48,y,14,INK,'Bold');flow(labels,48,y+28,1024);text(n,48,y+88,11,MUTED);y+=111

    newpage('A SaaS business, not just a school portal.','01 / Commercial requirements','Packaging below is a proposed commercial model. Validate willingness to pay before setting prices.')
    table(['CAPABILITY','CORE','GROWTH','ENTERPRISE'],[
      ['Student records, attendance, learning, exams','Included','Included','Included'],
      ['Fees, parent portal, basic reporting','Included','Included','Included'],
      ['Transport, library, inventory, payroll','Optional add-ons','Included / agreed limits','Contracted'],
      ['Multi-campus governance / analytics','Single-campus baseline','Multi-campus','Group-wide policies'],
      ['SSO, dedicated onboarding, advanced SLA','—','Optional','Contracted'],
      ['Hosting isolation / residency choices','Shared logical isolation','Shared logical isolation','Assessed dedicated option']
    ],y=180,rowh=46,ratios=[2.2,1.1,1.1,1.2],size=11)
    card('Billing meter','Define billable active students as a signed-off daily or monthly snapshot of active enrolments, deduplicated across campuses as agreed. Exclude demo, rejected and archived records. Show included allowance, overage and adjustment history.',48,517,498,157)
    card('Lifecycle & cost controls','Trial → active → past due → grace → read-only → closed. Support annual/monthly terms, renewals, credits and cancellation. Meter messages, storage and premium integrations separately. Display the effective date of every plan change.',566,517,506,157)
    note('Keep the school’s merchant payments separate from SaaS subscription collections. Never use an unverified frontend flag for entitlements.',697)

def modules():
    for m in MODULES:
        newpage(m['title'],'02 / Functional requirements',m['outcome'])
        chip(m['code']+' / '+m['phase'],48,158)
        y=204
        rows=[r for r in m['requirements'] if len(r)==2]
        for i,(title,body) in enumerate(rows,1):
            text(m['code']+'-'+str(i).zfill(2),48,y+2,10,PURPLE,'Bold')
            heading(title,130,y,535)
            ph=para(escape(body),130,y+28,535,12.3,MUTED,17.7)
            y+=max(76,ph+42)
        if y>735:errors.append((len(pages),'module rows',y,735))
        card('Primary owner',714,0,1,1) if False else None
        rect(714,204,358,88,LAV,14)
        text('PRIMARY OWNER',736,223,9.5,PURPLE,'Bold')
        para(escape(m['owner']),736,246,314,15,INK,21)
        card('Business rules',escape(m['rules']),714,312,358,160)
        card('Acceptance check',escape(m['acceptance']),714,492,358,166,PALE)
        text('SCREEN REFERENCES',736,683,9.5,PURPLE,'Bold')
        para(escape(m['screens']),736,704,314,12,MUTED,16)



def technical():
    newpage('Architecture that can grow with the product.','03 / Engineering','Recommended starting point: a modular application with explicit domain boundaries and managed infrastructure.')
    for i,(title,body) in enumerate([
      ('Responsive clients','Admin web • teacher web/PWA • family portal • operator console'),
      ('Edge & identity','CDN / TLS / rate limits • verified sessions • tenant/campus context'),
      ('Application modules','SIS & admissions • academics • finance • operations • SaaS control plane'),
      ('Durable async work','Transactional outbox • job workers • provider inbox • retries / dead-letter queue'),
      ('Data & integrations','PostgreSQL • private object storage • cache • payment / messaging / GPS adapters')]):
        rect(48,180+i*91,660,72,LAV if i==2 else BG,12)
        text(title,68,193+i*91,15,PURPLE if i==2 else INK,'Bold')
        para(body,68,220+i*91,620,12,MUTED,17)
        if i<4:text('↓',375,251+i*91,19,PURPLE)
    card('Suggested implementation','TypeScript across frontend and backend; React-based responsive UI; PostgreSQL transactional store; private object storage; durable queue; OpenAPI contracts. Select maintained framework versions during build.',734,180,338,184)
    card('Why this structure','One deployable application initially keeps cross-domain transactions manageable. Isolate modules in code and data access. Extract services only when scale, team ownership or failure isolation justifies it.',734,384,338,168)
    card('External dependencies','Use adapters for payment, communications, storage and GPS. Vendor failures must not corrupt school records. Infrastructure/provider choice remains an implementation decision.',734,566,338,135)
    note('This is a proposed architecture, not an installed stack. No particular cloud, database vendor or payment provider is required.',704)

    newpage('Tenant isolation is enforced at every layer.','03 / Architecture & tenancy','Recommended default: shared PostgreSQL with tenant-aware keys, policy enforcement and a non-privileged runtime role.')
    table(['LAYER','REQUIRED CONTROL','VERIFICATION'],[
      ['Request context','Derive tenant from authenticated membership; validate campus scope.','Reject crafted tenant/campus IDs.'],
      ['Database','tenant_id on scoped rows; composite foreign keys; RLS as defense in depth.','Attempt cross-tenant read/write/joins.'],
      ['Connection pooling','Set transaction-local scope; reset context; no owner/BYPASSRLS runtime.','Reuse pooled connections across tenants.'],
      ['Object storage','Private objects, tenant paths, short-lived links after authorization.','Try guessed paths and expired links.'],
      ['Cache / search','Include tenant and permission-sensitive scope in keys/index queries.','Check cache/search results after role changes.'],
      ['Jobs / exports','Carry explicit tenant + actor; revalidate scope when executing/downloading.','Revoke permissions while job is queued.'],
      ['Control plane','Separate operator roles and data access; time-limited school grants.','Expired support grant fails everywhere.'],
      ['Analytics / backups','Scoped aggregation; restricted restore tooling; audited data movement.','Reconcile tenant export and recovery scope.']
    ],y=180,rowh=53,ratios=[1.05,2.5,1.7],size=11.5)
    card('Database caveat [5]','Row-level policies supplement application authorization. Database owners, privileged jobs and maintenance paths can bypass ordinary policy behavior; inventory and test these paths explicitly.',48,662,1024,74)

    newpage('A durable model of a changing school.','03 / Data architecture','Accounts, people and enrolments are separate. Academic and financial history is preserved.')
    table(['DOMAIN','CORE ENTITIES','RELATIONSHIP / SOURCE OF TRUTH'],[
      ['Tenancy','Tenant, Campus, AcademicYear, Membership, RoleGrant','Tenant owns campuses; grants carry scope/effective dates.'],
      ['People','Account, Student, Guardian, StudentGuardian, Employee','Guardian ↔ student is verified many-to-many; account is optional.'],
      ['School structure','Grade, Section, Subject, TeachingAssignment, Enrolment','Student → many historical enrolments; section belongs to year/campus.'],
      ['Admissions','Enquiry, Application, Offer, SeatReservation','Accepted application → one enrolment conversion.'],
      ['Teaching','TimetableVersion, Session, Lesson, Assignment, Submission','Session uses effective roster; submissions have versions.'],
      ['Assessment','Exam, Component, MarkEntry, SchemeVersion, ReportIssue','Issued report snapshots scheme and approved values.'],
      ['Attendance','Register, AttendanceEntry, LeaveRequest, Correction','Unique student + session; corrections retain audit history.'],
      ['Money','Invoice, Line, CreditNote, Payment, Allocation, Refund, Journal','Payment ↔ invoice via allocation; reversals are explicit.'],
      ['Operations','Route, Trip, Loan, Asset, StockMovement, Ticket, CareCase','Each has scoped owner, status, history and service permissions.'],
      ['Platform','Subscription, UsageSnapshot, WebhookInbox, Outbox, AuditEvent','School subscription books are distinct from student-fee books.']
    ],y=180,rowh=49,ratios=[1,2.3,2.7],size=11)
    note('Use opaque stable IDs. Attach tenant_id to scoped rows and include it in cross-table foreign keys to prevent cross-tenant references.',714)

    newpage('Data integrity, lifecycle & retention.','03 / Data contracts','Minimum constraints belong in the database as well as application validation.')
    table(['CONTRACT','IMPLEMENTATION REQUIREMENT'],[
      ['Identity','Unique tenant + admission number; explicit correction flow. IDs remain stable through profile changes.'],
      ['Enrolment','Prevent overlapping active placements where school policy forbids them; retain effective dates/history.'],
      ['Attendance','Unique tenant + student + session; version number prevents lost updates; no default absence for missing rows.'],
      ['Money','Integer minor units + ISO currency; allocation totals cannot exceed available balances; refunds cannot exceed eligibility.'],
      ['Payment processing','Unique tenant + provider + merchant + event ID; unique verified payment posting; atomic receipt + ledger + outbox.'],
      ['Capacity','Atomic seat/bed reservation and single open library loan per copy; prevent simultaneous resource overbooking.'],
      ['Publication','Immutable issued report snapshot, template version, signer and checksum; reissue references the previous version.'],
      ['Audit','Append-only actor, tenant, action, target, server timestamp, reason and safe before/after summary; redact secrets.']
    ],y=180,rowh=51,ratios=[1.15,4],size=12)

    card('Retention decision register','For each record class define purpose, owner, legal/contract basis, retention trigger, duration, hold rules and deletion method. Cover applicant files, school records, finance, health, GPS, messages, audit logs and backups.',48,650,498,86)
    card('Deletion semantics','Use archive for operational lifecycle; use actual deletion/anonymization for approved erasure. Do not treat soft delete as completed erasure. Export and legal holds require explicit review and audit.',566,650,506,86)

    newpage('API contracts & reliable background jobs.','03 / Integration design','Illustrative versioned routes. Final schemas belong in OpenAPI with request, response, auth scope and error examples.')
    table(['ROUTE / ACTION','SCOPE','SAFETY CONTRACT'],[
      ['POST /v1/applications/{id}/accept','admissions.accept','Seat reservation + enrolment transaction; idempotency key.'],
      ['PUT /v1/registers/{id}/entries','attendance.write','Roster validation; expected version; conflict returns 409.'],
      ['POST /v1/reports/{id}/publish','results.publish','Required marks resolved; independent approval; immutable issue.'],
      ['POST /v1/invoices/{id}/payment-attempts','fees.pay / own child','Server amount/currency; provider order; safe retry semantics.'],
      ['POST /v1/webhooks/payments/{connection}','Provider signature','Raw-body verify; durable inbox; dedupe; async processing.'],
      ['POST /v1/payments/{id}/refund-requests','refund.request','Eligibility check; separate approval; provider reconciliation.'],
      ['POST /v1/exports','export.create','Authorized filter snapshot; async job; expiring download.'],
      ['POST /v1/support-grants','tenant.owner','Ticket, scope, reason, expiry and audit; revocable at any time.']
    ],y=180,rowh=48,ratios=[2.3,1.35,2.65],size=11)
    card('Shared contract','Cursor pagination; bounded filters; stable error codes with field details and correlation ID; consistent time/money formats. Use 401/403, 409, 422 and 429 deliberately. Never expose another tenant’s record existence.',48,626,498,109)
    card('Job contract','Durable queue, attempt count, bounded exponential retry, dead-letter queue and authorized replay. Idempotency keys bind actor/tenant/action/body hash. Use an outbox for post-transaction notifications.',566,626,506,109)

    newpage('Payments: explicit states, recoverable failures.','03 / Critical workflow','A bank movement and an application message are different events. Reconciliation closes the loop.')
    heading('Capture path',48,180);flow(['Attempt created','Checkout pending','Provider captured','Verified posting','Receipt issued'],48,218,1024)
    heading('Settlement path',48,302);flow(['Captured ledger','Provider settlement','Bank statement','Match / exception','Close batch'],48,340,1024)
    card('Failure handling','<b>Browser closes:</b> recover using provider events/status.<br/><b>Duplicate webhook:</b> acknowledge stored event; no second posting.<br/><b>Out-of-order event:</b> apply valid transitions only.<br/><b>Worker crashes:</b> retry the durable inbox transaction.<br/><b>Amount mismatch:</b> quarantine for review.',48,438,498,220)
    card('Refund & dispute control','Requested → independently approved → provider initiated → pending → completed / failed. Keep the original payment and record a separate reversal only when justified. Track partial refunds and chargebacks independently. Reconcile gross amount, charges, net settlement and bank references.',566,438,506,220)
    note('PAY acceptance: verified receipt + allocation + ledger + outbox commit atomically; family-facing status never relies only on a redirect. [4]',690)

    newpage('Security, privacy & child data.','03 / Trust requirements','Implement these controls from P0. Validate applicable legal obligations and commencement dates before launch.')
    card('Application security [2]','Use ASVS 5.0 as a verification catalogue. Require MFA for privileged users, short-lived sessions, secure cookies, CSRF protection, input validation, dependency scanning, secret management and rate limits. Test file uploads for type/size, malware and unauthorized retrieval.',48,180,498,211)
    card('India privacy readiness [3]','Maintain a processing inventory and purpose-specific notices. Implement guardian verification and consent records where applicable, withdrawal handling, correction/erasure requests, grievance routing and breach response. Validate school/vendor responsibilities, exemptions and staged commencement against official material.',566,180,506,211)
    card('Child-safe defaults','No targeted advertising or sale of child data. Minimize identity collection; do not require Aadhaar by default. Use restricted health/custody access, private media, verified guardian links and minimal lock-screen notifications. Prohibit training third-party models on school data without an approved basis and contract.',48,411,498,216)
    card('Governance & evidence','Agree school/vendor data roles, subprocessors, hosting region, access requests, retention and offboarding in contracts. Record policy versions and approval. Encrypt transport/storage; isolate production; redact logs; audit sensitive reads, support access and exports. Rehearse incident triage and notification decisions.',566,411,506,216)
    note('Legal review is a launch dependency. This document specifies product controls; it does not assert that every law is fully in force or that the product is compliant.',685)

    newpage('Measurable quality requirements.','03 / Non-functional requirements','Proposed engineering acceptance targets; benchmark against a representative pilot dataset before making SLA commitments.')
    table(['ID','REQUIREMENT','TARGET / TEST CONDITION'],[
      ['NFR-01','Availability','99.9% monthly core-service target; define exclusions and measurement in the SLA.'],
      ['NFR-02','Interactive performance','p95 API reads < 500 ms, writes < 800 ms excluding provider latency under agreed load.'],
      ['NFR-03','Web experience','p75 LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 on representative midrange mobile/4G.'],
      ['NFR-04','Initial load envelope','Benchmark 100 tenants × 2,000 pupils; 2,000 concurrent sessions; 300 requests/s peak.'],
      ['NFR-05','Batch processing','10,000-row import/export completes within 10 min in benchmark; visible progress/cancellation.'],
      ['NFR-06','Recovery','Proposed RPO ≤ 15 min and RTO ≤ 4 h for core data; prove through restore exercises.'],
      ['NFR-07','Accessibility [1]','WCAG 2.2 AA target; keyboard, screen reader, focus, errors and zoom checks on key journeys.'],
      ['NFR-08','Consistency','No duplicated receipt, capacity overbooking or lost approved correction under concurrency tests.'],
      ['NFR-09','Compatibility','Current and prior major Chrome/Edge/Safari/Firefox; responsive widths 360–1920 px.'],

      ['NFR-10','Localization','Externalized strings; English + Hindi pilot where validated; Unicode names, INR and local dates.']
    ],y=180,rowh=48,ratios=[.6,1.3,3.9],size=11.5)
    note('The load envelope is a planning assumption, not a measured capacity claim. Include peak attendance, payment and result-release bursts.',711)

    newpage('Deploy, observe, restore.','03 / Production operations','Operational readiness is part of the product scope and has named ownership.')
    card('Environments & delivery','Separate local, staging and production accounts/data. Use synthetic test records, reviewed migrations, infrastructure-as-code, protected secrets and CI gates. Deploy with feature flags and gradual tenant rollout. Use backward-compatible expand/migrate/contract schema changes.',48,180,498,203)
    card('Observability','Capture metrics, redacted structured logs and traces with tenant-aware correlation. Monitor latency, error rate, queue age, provider failures, overdue reconciliation, storage and backup age. Define alert ownership, severity and runbooks; avoid student details in alerts.',566,180,506,203)
    card('Backup & recovery','Encrypt scheduled backups and point-in-time recovery. Restrict backup operators and region copies. Rehearse full restoration and tenant-level export recovery. Verify database, files and encryption-key dependencies together. Confirm counts, balances and checksums after restore.',48,403,498,203)
    card('Incident & continuity','Maintain on-call escalation, status communication and evidence preservation. Provide manual attendance/cash-collection fallback with later reconciliation. Disable failing integrations safely. Practice provider outage, accidental deletion, credential compromise and regional failure.',566,403,506,203)
    note('Release rollback is not database rollback. Document forward-fix and data-recovery strategies for each migration; test them before a risky rollout.',684)

    newpage('A release gate with meaningful evidence.','03 / Test strategy','The following are scenario requirements for implementation, not claims that the application has already passed.')
    table(['TEST ID','SCENARIO','REQUIRED RESULT'],[
      ['QA-01','Cross-tenant API, search, file and cache access','Denied without leakage; security event recorded.'],
      ['QA-02','Guardian revoked while session/export is active','API and file access stop; communication audience updated.'],
      ['QA-03','Concurrent seat, bed, room and copy allocation','Capacity constraint holds; loser gets actionable conflict.'],
      ['QA-04','Offline attendance vs approved correction','Conflict resolved; no silent overwrite or duplicate alert.'],
      ['QA-05','Duplicate/out-of-order/tampered payment events','One valid posting; invalid signature rejected; audit preserved.'],
      ['QA-06','Partial refund, chargeback and settlement mismatch','Balances reconcile; exception owner and status visible.'],
      ['QA-07','Missing marks, scheme change and report reissue','Publication blocks correctly; earlier report stays intact.'],
      ['QA-08','Rollover with repeats, transfers and outstanding dues','Correct enrolments, fee carry-forward and historical reports.'],
      ['QA-09','Import retry, malformed file and duplicate IDs','Safe validation, recoverable progress and reconciled totals.'],
      ['QA-10','Keyboard, screen reader, zoom and low bandwidth','Key tasks complete with understandable errors and focus.'],
      ['QA-11','Backup restore + job replay + provider outage','Recovery targets met; no duplicate financial side effects.']
    ],y=180,rowh=44,ratios=[.65,2.1,2.6],size=11)
    note('Go-live gate: zero unresolved critical/high access or financial defects; signed pilot UAT; restore evidence; reconciled migration; trained owners.',716)

    newpage('From discovery to a sustainable release.','03 / Delivery plan','Illustrative sequencing for a dedicated cross-functional team; estimates require discovery and capacity confirmation.')
    table(['PHASE','INDICATIVE WINDOW','DELIVERABLE / EXIT GATE'],[
      ['Discovery & design','Weeks 1–3','Pilot interviews, school policy mapping, source data audit, validated prototype and signed P0 backlog.'],
      ['Platform foundation','Weeks 4–7','Tenancy, IAM, roles, audit, environments, imports, school/year setup and security tests.'],
      ['School core','Weeks 8–13','Admissions, SIS, manual timetable, attendance, staff directory, teaching and family portal.'],
      ['Finance & results','Weeks 14–19','Fees, verified payments, reconciliation, examinations/report cards and communications.'],
      ['Pilot & launch','Weeks 20–23','Migration rehearsals, UAT, accessibility/load checks, restore exercise, training and monitored go-live.'],
      ['P1 operations','Next 12–16 weeks','Transport, library, purchasing, deeper HR/payroll, accounting, analytics and scheduling solver.'],
      ['P2 options','Demand-led increments','Hostel, meals, enterprise SSO, public pages, assistive AI and further localization.']
    ],y=180,rowh=56,ratios=[1.15,1.2,3.4],size=11.5)
    card('Suggested team & costing','Product/domain lead; product designer; technical lead; 3–4 engineers across frontend/backend; QA automation; shared DevOps/security and school/accounting reviewers. Estimate cost as role-months × agreed rates plus hosting, messaging, gateways and support.',48,636,1024,100)

    newpage('Dependencies, decisions & rollout readiness.','03 / Implementation handoff','Resolve material product assumptions before committing to scope, cost or a customer SLA.')
    table(['DECISION / RISK','OWNER','REQUIRED EVIDENCE'],[
      ['Pilot school sizes, boards and operating model','Product + school owners','Validated workflows, volumes and signed priority exceptions.'],
      ['School/vendor data roles, consent and retention','Legal/privacy + school','Reviewed contract, notices, retention register and legal timeline.'],
      ['Fee, concession, tax, refund and payroll policies','Finance + reviewers','Signed calculation examples and accounting mappings.'],
      ['Provider access and ongoing unit costs','Engineering + procurement','Sandbox tests, commercial terms, quotas and outage procedures.'],
      ['Data migration quality / opening balances','Registrar + finance','Reconciled dry run, issue register and school approval.'],
      ['Budget, staffing and schedule','Delivery lead','Capacity plan and estimates against the requirements register.'],
      ['Regional rollout and support languages','Customer success','Training materials, language QA and staffed escalation channels.']
    ],y=180,rowh=52,ratios=[2.2,1.3,2.4],size=11.5)
    card('Critical dependency order','TEN + IAM → SIS + ACA → TIM / ATT / LMS / EXM.<br/>SIS + FEE → PAY → FIN.<br/>IAM + staff records → payroll.<br/>All modules → ANA + platform operations.<br/>Security, audit and accessibility run through every phase.',48,607,498,129)

    card('Definition of done','Reviewed design + business rules; server authorization; meaningful tests; failure/empty/loading states; accessibility; analytics; documentation; support runbook; school acceptance. Feature completion includes recovery and migration behavior.',566,607,506,129)

    newpage('A visual system with room to breathe.','04 / Experience foundations','Design direction: calm operational clarity, warm surfaces, precise typography and restrained violet accents.')
    palette=[('Ink',INK),('Primary',PURPLE),('Lavender',LAV),('Canvas',BG),('Success',GREEN),('Warning',AMBER)]
    for i,(name,color) in enumerate(palette):
        xx=48+i*173;rect(xx,184,156,70,color,12);text(name,xx,265,12,INK,'Bold');text(color,xx,285,10,MUTED)
    card('Type & spacing','Segoe UI in this PDF; use an appropriately licensed UI font in production. Screen hierarchy: 28/20/16/14/12 px equivalent; body line-height around 1.45. Use a 4 px grid, 16–24 px card padding, 10–16 px radii and subtle borders.',48,332,498,158)
    card('Reusable components','Workspace switcher, page header, metric card, data table, search/filter bar, status label, tabs, calendar, form field, drawer, modal, stepper, empty state, toast, upload queue, approval timeline and audit history.',566,332,506,158)
    card('Responsive rules','Desktop: persistent navigation, 12-column content grid and dense but readable tables. Tablet: collapsed rail and prioritized columns. Mobile: one-column tasks, bottom navigation and explicit child/class context. Offer list alternatives to wide tables.',48,510,498,165)
    card('Interaction & accessibility [1]','Visible focus, keyboard actions, associated field labels and inline errors. Status uses text plus color; charts include tables. Respect reduced motion. Aim for 44 px touch controls, sufficient contrast and screen-reader announcements for async results.',566,510,506,165)
    note('Screens are high-fidelity static concepts with fictional data. They demonstrate layout and behavior intent; production accessibility must be verified.',707)



def button(label,x,y,w=110,primary=True):
    rect(x,y,w,32,PURPLE if primary else WHITE,7,stroke=None if primary else LINE)
    text(label,x+w/2,y+8,10.5,WHITE if primary else INK,'Bold','center')
def avatar(initials,x,y,color=PURPLE,r=15):
    circle(x,y,r,LAV if color==PURPLE else PALE);text(initials,x,y-8,10,color,'Bold','center')
def metric(label,value,detail,x,y,w=190):
    rect(x,y,w,91,WHITE,11,LINE)
    text(label,x+16,y+12,10.5,MUTED)
    text(value,x+16,y+31,26,INK,'Bold')
    text(detail,x+16,y+69,9.5,GREEN)
def ui_table(headers,rows,x,y,width=812,ratios=None,rowh=37):
    ratios=ratios or [1]*len(headers);ws=[width*r/sum(ratios) for r in ratios]
    rect(x,y,width,31,'#F0F2F8',7)
    xx=x
    for h,ww in zip(headers,ws):
        text(h,xx+12,y+9,9,MUTED,'Bold');xx+=ww
    y+=31
    for i,row in enumerate(rows):
        rect(x,y,width,rowh,WHITE)
        xx=x
        for val,ww in zip(row,ws):
            if str(val).startswith('@'):
                s=str(val)[1:];chip(s,xx+9,y+7,GREEN,PALE)
            elif str(val).startswith('!'):
                s=str(val)[1:];chip(s,xx+9,y+7,AMBER,'#FFF5DF')
            else:para(escape(str(val)),xx+12,y+10,ww-20,10.4,INK,13,maxh=rowh-12)
            xx+=ww
        line(x,y+rowh,x+width,y+rowh)
        y+=rowh
    return y
def ucard(title,x,y,w,h):
    rect(x,y,w,h,WHITE,12,LINE)
    text(title,x+18,y+15,13,INK,'Bold')
def field(label,value,x,y,w=240):
    text(label,x,y,10,MUTED,'Bold')
    rect(x,y+20,w,37,WHITE,7,LINE)
    text(value,x+12,y+30,11,INK)
def spark(x,y,w,h,values,color=PURPLE,fill=False,ymin=None,ymax=None):
    mx=max(values) if ymax is None else ymax;mn=min(0,min(values)) if ymin is None else ymin;pts=[(x+i*w/(len(values)-1),y+h-(v-mn)/(mx-mn)*h) for i,v in enumerate(values)]
    for a,b in zip(pts,pts[1:]):line(a[0],a[1],b[0],b[1],color,2.5)
    for px,py in pts:circle(px,py,3,color)
def screen(sid,title,subtitle,nav='Overview',action=None,operator=False):
    newpage(sid+' / '+title,'04 / Screen design',subtitle)
    rect(48,166,1024,530,BG,15,LINE)
    rect(48,166,164,530,NAV,14)
    # mask inner rounded edge for a continuous workspace
    rect(198,166,14,530,NAV)
    text('campus',67,185,18,WHITE,'Bold');text('os',132,185,18,'#BEB4FF','Bold')
    rect(64,223,132,46,'#303855',8)
    text('PLATFORM' if operator else 'GREENFIELD SCHOOL',75,233,8.3,'#CDD4E5','Bold')
    text('Operator workspace' if operator else 'Main campus  ▾',75,249,9.8,WHITE)
    items=['Overview','Admissions','Students','Attendance','Timetable','Learning','Examinations','Fees & payments','Staff & payroll','Communications','Operations','Reports']
    if operator:items=['Overview','Tenants','Subscriptions','Usage & billing','Onboarding','Service health','Support','Audit log']
    for i,l in enumerate(items):
        yy=286+i*26
        if l==nav:rect(60,yy-3,140,25,'#514A87',6)
        circle(72,yy+9,2.6,'#BCB4F5' if l==nav else '#75809D')
        text(l,84,yy+1,10.4,WHITE if l==nav else '#C0C8DC','Bold' if l==nav else 'UI')
    line(65,635,195,635,'#424B67')
    avatar('AS',79,664);text('Ananya Shah',101,650,10,WHITE,'Bold');text('Administrator',101,667,9,'#AEB9D0')
    rect(212,166,860,48,WHITE)
    text('Search students, classes, invoices…',234,183,10.5,MUTED)
    text('2026–27  ▾',870,183,10,INK)
    circle(982,190,12,BG);text('3',982,182,9,PURPLE,'Bold','center');avatar('AS',1036,190,r=13)
    line(212,214,1072,214)
    text(title,236,230,23,INK,'Bold')
    if action:button(action,926,232,122)
    text('Greenfield School  /  Main campus' if not operator else 'CampusOS  /  Service operations',236,261,9.5,MUTED)
def annotations(left,right):
    para('<b>Primary flow:</b> '+left,48,706,497,10.2,MUTED,14,maxh=32)
    para('<b>Recovery & access:</b> '+right,575,706,497,10.2,MUTED,14,maxh=32)

def screens():
    # S01
    newpage('S01 / Welcome to your school workspace','04 / Screen design','Identity and onboarding • TEN-01 to TEN-05, IAM-01 • desktop concept')
    rect(48,166,1024,530,BG,16,LINE)
    rect(48,166,465,530,NAV,16)
    text('campusos',81,201,24,WHITE,'Bold')
    text('More time for',81,282,34,WHITE,'Light');text('what matters.',81,326,34,WHITE,'Bold')
    para('A connected school.<br/>A clearer day.<br/>A place for every learner.',83,399,350,18,'#C6CEE1',29)
    for i,(a,b) in enumerate([('01','Bring your school together'),('02','Make the everyday easier'),('03','See the progress that matters')]):
        yy=529+i*43;circle(97,yy+10,13,'#3B4267');text(a,97,yy+3,9,'#D3CCFF','Bold','center');text(b,123,yy+3,12,'#DCE1ED')
    text('Welcome back',585,218,29,INK,'Bold')
    text('Sign in to Greenfield School',585,262,13,MUTED)
    field('School workspace','greenfield.campusos.app',585,304,410)
    field('Email address','ananya@greenfield.example',585,379,410)
    field('Password','••••••••••••',585,454,410)
    text('Forgot password?',995,519,10.5,PURPLE,'Bold','right')
    button('Continue securely',585,554,410)
    text('New school?  Start your workspace',790,614,12,PURPLE,'Bold','center')
    text('Privacy  •  Help  •  Language: English',790,656,10,MUTED,'UI','center')
    annotations('Verified sign-in → MFA when required → role workspace.','Expired invitation and recovery states retain clear next steps.')

    # S02
    screen('S02','Good morning, Ananya','School overview • TEN, ATT, FEE, ANA • one place to start the school day',action='View reports')
    for i,(l,v,d) in enumerate([('Total students','1,248','+24 this term'),('Attendance today','95.8%','1,196 of 1,248 present'),('Fees collected','₹ 18.4L','78% of ₹ 23.6L billed'),('Open applications','86','12 ready for review')]):
        metric(l,v,d,236+i*207,290,191)
    ucard('Last school week',236,398,502,178)
    text('Present rate',255,431,10,MUTED);text('School days only',718,414,9,MUTED,'UI','right')
    for j in range(3):line(258,462+j*34,716,462+j*34)
    spark(288,453,414,78,[92,96,94,97,95.8],ymin=90,ymax=100)
    text('100%',254,448,8,MUTED);text('95%',254,487,8,MUTED);text('90%',254,526,8,MUTED)
    for i,d in enumerate(['Mon','Tue','Wed','Thu','Fri']):text(d,270+i*105,553,9,MUTED)
    ucard('Needs your attention',756,398,292,278)
    for i,(t,d,cl) in enumerate([('12 applications to review','Admissions • updated 10 min ago',PURPLE),('3 attendance registers open','Grade 6–8 • closes at 10:00',AMBER),('5 payment exceptions','Finance • reconciliation queue',ROSE),('Annual day permissions','38 responses still pending',GREEN)]):
        yy=442+i*54;circle(778,yy+8,4,cl);text(t,792,yy,10.5,INK,'Bold');text(d,792,yy+19,8.8,MUTED)
    ucard('Coming up today',236,592,502,84)
    text('10:30   Academic review',255,632,11,INK);chip('Meeting',444,625);text('14:00   Parent visits',545,632,10,MUTED)
    annotations('Open an exception, complete its action, return to the filtered overview.','Every metric shows the applicable campus, date and authorized drilldown.')

    # S03
    screen('S03','Admissions pipeline','Admissions • ADM-01 to ADM-06 • intake 2027–28',nav='Admissions',action='+ Application')
    text('All grades  ▾      Assigned to anyone  ▾      Intake 2027–28  ▾',236,291,11,MUTED)

    lanes=[('New enquiries','18',LAV),('In review','12','#EAF2FF'),('Offer sent','8','#FFF4DF'),('Accepted','24',PALE)]
    names=[['Aarav Mehta','Diya Rao','Kabir Sethi'],['Anika Patel','Ishaan Roy','Meera Shah'],['Riya Nair','Vivaan Jain','Sara Khan'],['Aditi Sen','Arjun Das','Tara Kapoor']]
    for i,(label,count,color) in enumerate(lanes):
        xx=236+i*207;rect(xx,326,191,350,'#EEF0F6',10);text(label,xx+13,339,12,INK,'Bold');chip(count,xx+143,333)
        for j,n in enumerate(names[i]):
            yy=379+j*94;rect(xx+10,yy,171,82,WHITE,9)
            text(n,xx+22,yy+12,12,INK,'Bold');text('Grade '+str(3+j)+' • Web enquiry',xx+22,yy+33,9.5,MUTED)
            chip(['Follow up','Documents due','Ready'][j],xx+20,yy+51,GREEN if j==2 else PURPLE,PALE if j==2 else LAV)
    annotations('Review application → validate documents → offer → reserve seat → enrol.','Capacity and offer expiry are checked before acceptance; changes are audited.')

    # S04
    screen('S04','Student directory','Student records • SIS-01 to SIS-04 • searchable, scoped and easy to scan',nav='Students',action='+ Add student')
    for i,(l,v,d) in enumerate([('Active students','1,248','Across 42 sections'),('New this term','24','Enrolment confirmed'),('Documents due','18','Requires office follow-up')]):
        metric(l,v,d,236+i*276,290,260)
    rect(236,400,812,42,WHITE,9,LINE);text('Search name or admission number…',252,413,11,MUTED)
    text('Grade: All  ▾     Section: All  ▾     Export ↓',1028,413,10,PURPLE,'UI','right')
    ui_table(['STUDENT','ADMISSION NO.','GRADE / SECTION','GUARDIAN','STATUS'],[
      ['Aarav Mehta','GF-2026-0142','6 / A','Neha Mehta','@Active'],
      ['Anika Patel','GF-2026-0143','6 / A','Rohan Patel','@Active'],
      ['Diya Rao','GF-2025-0089','6 / B','Kavya Rao','!Docs due'],
      ['Ishaan Roy','GF-2024-0118','7 / A','Ritu Roy','@Active'],
      ['Meera Shah','GF-2025-0241','7 / B','Nisha Shah','@Active']
    ],236,459,ratios=[1.4,1.25,1.2,1.3,1],rowh=35)
    text('Showing 1–5 of 1,248 students',252,674,9.5,MUTED)
    annotations('Search/filter → student record → approved update or certificate.','Exports are asynchronous and scoped; duplicate records go through review.')

    # S05
    screen('S05','Student profile','Student lifecycle • SIS, HLT, FAM • a connected record with restricted sensitive panels',nav='Students',action='Edit profile')
    rect(236,290,812,91,WHITE,12,LINE);avatar('AM',279,335,r=25)
    text('Aarav Mehta',320,307,20,INK,'Bold');text('GF-2026-0142  •  Grade 6 A  •  Roll 08',320,339,11,MUTED)
    chip('Active',846,314,GREEN,PALE);text('Academic year 2026–27',1029,347,9.5,MUTED,'UI','right')
    text('Overview     Attendance     Academics     Fees     Documents     History',252,401,11,PURPLE,'Bold')
    line(236,429,1048,429)
    ucard('Student information',236,446,393,225)
    for i,(l,v) in enumerate([('Date of birth','14 Aug 2014'),('Class teacher','Priya Menon'),('House','Cedar'),('Transport','Route 04 • Lake Road'),('Emergency contact','Neha Mehta • verified')]):
        yy=489+i*34;text(l,254,yy,10,MUTED);text(v,608,yy,10.5,INK,'UI','right')
    ucard('Family & authorized access',647,446,401,112)
    avatar('NM',677,507);text('Neha Mehta',701,489,12,INK,'Bold');text('Guardian • fees & learning access',701,513,10,MUTED);chip('Verified',948,496,GREEN,PALE)
    ucard('Recent activity',647,574,401,97)
    text('09 Nov   Homework feedback released',666,615,10,INK)
    text('07 Nov   Term 2 fee receipt issued',666,640,10,MUTED)
    annotations('Review academic and family history before making a controlled change.','Health/custody details appear only for explicit permissions; all reads are audited.')

    # S06
    screen('S06','Take attendance','Class attendance • ATT-01 to ATT-06 • fast entry with a deliberate review step',nav='Attendance',action='Review & submit')
    rect(236,290,812,47,WHITE,9,LINE);text('Grade 6 A  ▾      10 Nov 2026  ▾      Morning register  ▾',252,305,11,INK)
    chip('Draft',963,301,AMBER,'#FFF5DF')
    for i,(l,v,d) in enumerate([('Present','30','Review before submission'),('Absent','1','Guardian alert after review'),('Unmarked','1','Complete remaining entry')]):
        metric(l,v,d,236+i*276,353,260)
    ui_table(['ROLL','STUDENT','ATTENDANCE','NOTE'],[
      ['01','Anika Patel','Present  /  Absent  /  Late','—'],
      ['02','Aarav Mehta','Present  /  Absent  /  Late','—'],
      ['03','Diya Rao','Absent','Leave request received'],
      ['04','Ishaan Roy','Present  /  Absent  /  Late','—'],
      ['05','Meera Shah','Unmarked','Choose a status']
    ],236,461,ratios=[.5,1.4,2,1.4],rowh=34)
    text('Saved just now  •  1 entry needs your attention',252,675,10,AMBER)
    annotations('Mark each pupil → review unmarked entries → finalize → notify permitted guardians.','Offline mode shows queued changes; conflicting edits cannot silently overwrite.')

    # S07
    screen('S07','Weekly timetable','Academic scheduling • ACA, TIM • a clear weekly grid with conflict detection',nav='Timetable',action='Publish version')
    text('Grade 6 A  ▾         Week of 09 Nov 2026  ▾',236,291,11,INK);chip('Draft v3',916,286)
    xx=236;yy=331;cw=145;labelw=78
    for i,d in enumerate(['TIME','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY']):
        text(d,xx+(labelw if i else 0)+(i-1)*cw+13 if i else xx+8,yy,9,MUTED,'Bold')
    subj=['Mathematics','English','Science','Hindi','Social studies','Computer lab']
    colors=[LAV,'#E7F2FE',PALE,'#FFF3DE','#FCECF0','#EAF0F7']
    for r in range(5):
        y=yy+31+r*58;text(['08:30','09:20','10:25','11:15','12:05'][r],xx+9,y+13,10,MUTED)
        for k in range(5):
            j=(r+k*2)%6;x=xx+labelw+k*cw
            rect(x,y,cw-9,49,colors[j],7);text(subj[j],x+10,y+8,10.4,INK,'Bold');text(['P. Menon','R. Singh','A. Iyer'][j%3]+' • R'+str(201+k),x+10,y+29,8.5,MUTED)
    rect(236,659,812,25,PALE,6);text('No hard conflicts found  •  30 periods assigned  •  Version starts 16 Nov',251,665,10,GREEN)
    annotations('Edit draft → resolve teacher/room conflicts → review workload → publish.','Hard conflicts block publication; an effective date preserves historical timetables.')

    # S08
    screen('S08','Learning workspace','Teaching & assignments • LMS • keep preparation, work and feedback together',nav='Learning',action='+ Assignment')
    rect(236,290,812,79,LAV,12);text('Grade 6 A  /  Mathematics',256,306,20,INK,'Bold')
    text('Priya Menon  •  Term 2  •  32 learners',256,338,11,MUTED);button('View class',915,313,110,False)
    text('Assignments       Lesson plans       Resources       Progress',252,389,11,PURPLE,'Bold')
    for i,(t,sub,count,status) in enumerate([('Fractions in everyday life','Due tomorrow • Practice sheet','24 / 32 submitted','Published'),('Patterns & sequences','Due 14 Nov • Group activity','12 / 32 submitted','Published'),('Exploring symmetry','Draft • Worksheet','Ready for your review','Draft')]):
        yy=427+i*80;rect(236,yy,525,68,WHITE,10,LINE)

        text(t,253,yy+12,13,INK,'Bold');text(sub,253,yy+37,10,MUTED)
        chip(status,650,yy+20);text(count,533,yy+40,9,MUTED,'UI','right')
    ucard('Your next lesson',779,427,269,229)
    text('Equivalent fractions',797,469,16,INK,'Bold')
    para('Help learners connect visual models to equivalent fractions.',797,505,230,11,MUTED,17)
    text('Objective coverage',797,559,10,MUTED);rect(797,581,230,7,LAV,3);rect(797,581,170,7,PURPLE,3)
    button('Open lesson plan',797,610,230,False)
    annotations('Prepare lesson → publish assignment → review submissions → release feedback.','Draft scores stay private; individual extensions preserve original class deadlines.')

    # S09
    screen('S09','Results & report cards','Assessment • EXM-01 to EXM-06 • review before publication',nav='Examinations',action='Review results')
    for i,(l,v,d) in enumerate([('Grade 6 / Term 2','128','Students in this cohort'),('Marks complete','96%','5 entries still required'),('Report status','Draft','Approval pending')]):
        metric(l,v,d,236+i*276,290,260)
    ui_table(['STUDENT','ENGLISH / 100','MATHS / 100','SCIENCE / 100','REVIEW'],[
      ['Aarav Mehta','86','92','88','@Ready'],
      ['Anika Patel','91','89','94','@Ready'],
      ['Diya Rao','84','—','87','!Missing'],
      ['Ishaan Roy','78','85','82','@Ready']
    ],236,400,width=812,ratios=[1.6,1.2,1.2,1.2,1],rowh=40)
    rect(236,608,812,66,'#FFF5DF',10)
    text('Publication needs one more review',255,620,13,AMBER,'Bold')
    text('Resolve missing marks, verify the grading scheme and obtain coordinator approval.',255,646,10.5,AMBER)
    annotations('Enter marks → validate → submit → moderate → approve → publish report snapshots.','Missing required marks block release; corrections produce versioned reissues.')



    # S10
    screen('S10','Fees & collections','Finance • FEE, FIN • explainable balances and controlled adjustments',nav='Fees & payments',action='+ Create invoice')
    for i,(l,v,d) in enumerate([('Billed this term','₹ 23.6L','Posted invoices only'),('Collected','₹ 18.4L','78% of billed amount'),('Outstanding','₹ 5.2L','Includes future due dates')]):
        metric(l,v,d,236+i*276,290,260)
    text('All invoices     Overdue     Concessions     Cashier close',252,404,11,PURPLE,'Bold')
    ui_table(['INVOICE / STUDENT','DUE DATE','AMOUNT','BALANCE','STATUS'],[
      ['INV-26142 • Aarav Mehta','15 Nov 2026','₹ 24,000','₹ 12,000','!Part paid'],
      ['INV-26143 • Anika Patel','15 Nov 2026','₹ 24,000','₹ 24,000','Due'],
      ['INV-26089 • Diya Rao','31 Oct 2026','₹ 18,000','₹ 18,000','!Overdue'],
      ['INV-26118 • Ishaan Roy','15 Nov 2026','₹ 24,000','₹ 0','@Paid'],
      ['INV-26241 • Meera Shah','15 Nov 2026','₹ 24,000','₹ 0','@Paid']
    ],236,437,ratios=[2,1.2,1,1,1.1],rowh=38)
    button('Send reviewed reminders',236,655,193,False)
    annotations('Filter receivables → open ledger → collect, allocate or request adjustment.','Posted entries use reversals; refunds/waivers require independent approval.')

    # S11
    screen('S11','Payment reconciliation','Payment operations • PAY, FIN • compare capture, receipt and settlement',nav='Fees & payments',action='Import statement')
    for i,(l,v,d) in enumerate([('Matched today','142','Verified and allocated'),('Needs review','5','Assigned to finance'),('Settlement batch','₹ 2.84L','Net expected bank credit')]):
        metric(l,v,d,236+i*276,290,260)
    ucard('Unmatched payments',236,401,423,272)
    ui_table(['REFERENCE','AMOUNT','REASON'],[
      ['pay_demo_102','₹ 12,000','Receipt pending'],
      ['pay_demo_108','₹ 8,500','Invoice mismatch'],
      ['pay_demo_114','₹ 24,000','Settlement pending'],
      ['pay_demo_119','₹ 6,000','Review required']
    ],249,447,width=397,ratios=[1.25,1,1.7],rowh=42)
    ucard('Review • pay_demo_102',677,401,371,272)
    for i,(l,v) in enumerate([('Student','Aarav Mehta'),('Invoice','INV-26142'),('Provider status','Captured'),('Verified amount','₹ 12,000'),('Receipt status','Not posted')]):
        yy=449+i*33;text(l,695,yy,10,MUTED);text(v,1027,yy,11,INK,'UI','right')
    button('Retry verified posting',695,630,334)
    annotations('Inspect verified evidence → resolve exception → post safely → reconcile bank.','Repeated events or replay cannot create a second receipt or allocation.')

    # S12
    screen('S12','Staff & payroll','HR and payroll • HRM • a reviewable monthly run with restricted access',nav='Staff & payroll',action='Review payroll')
    for i,(l,v,d) in enumerate([('Active employees','86','72 teaching • 14 operations'),('Net pay / November','₹ 32.8L','Draft estimate'),('Exceptions','3','Review before approval')]):
        metric(l,v,d,236+i*276,290,260)
    text('Directory       Attendance       Leave       Payroll',252,403,11,PURPLE,'Bold')
    ui_table(['EMPLOYEE','ROLE','PAID DAYS','NET PAY','REVIEW'],[
      ['Priya Menon','Teacher','30','₹ 48,200','@Ready'],
      ['Rohit Singh','Teacher','30','₹ 46,500','@Ready'],
      ['Asha Iyer','Teacher','29','₹ 45,100','!Leave check'],
      ['Nitin Das','Office admin','30','₹ 32,800','@Ready'],
      ['Farah Khan','Librarian','30','₹ 34,600','!Adjustment']
    ],236,438,ratios=[1.45,1.1,1,1.1,1.1],rowh=38)
    text('Draft run  •  Calculations require review  •  Approval by a different authorized user',252,676,10,MUTED)
    annotations('Reconcile inputs → draft payroll → resolve exceptions → independent approval.','Salary and bank fields require HR scope; approved corrections remain versioned.')

    # S13
    screen('S13','Communication centre','Notices, meetings and messages • COM • audience clarity before sending',nav='Communications',action='Save draft')
    ucard('Compose a school notice',236,290,502,383)
    field('Subject','Parent–teacher meetings • November',254,337,465)
    field('Audience','Grade 6–8 guardians  •  384 recipients',254,411,465)
    text('MESSAGE',254,485,9,MUTED,'Bold');rect(254,507,465,105,BG,7,LINE)
    para('Dear families,<br/><br/>Meeting slots are now open for 21 November. Please select a convenient time to meet your child’s class teacher.',267,518,436,11,INK,17)
    button('Preview & schedule',254,631,465)
    ucard('Delivery settings',756,290,292,218)
    for i,(label,val) in enumerate([('In-app inbox','Enabled'),('Email','Enabled'),('SMS','Not selected'),('Schedule','Tomorrow, 09:00')]):
        yy=337+i*35;text(label,775,yy,10,MUTED);text(val,1028,yy,10.5,INK,'UI','right')
    ucard('Before you send',756,526,292,147)
    para('384 verified recipients<br/>12 contacts need verification<br/>No student contact details exposed<br/>Quiet hours respected',775,569,250,11,MUTED,21)
    annotations('Select audience → preview recipients/content → approve → schedule → monitor.','Consent, verified contacts, restricted guardians and quotas filter the audience.')

    # S14
    screen('S14','Transport operations','Routes and live trips • TRN • route diagram is illustrative, not a real map',nav='Operations',action='Manage routes')
    rect(236,290,501,382,'#EEF3F4',12,LINE)
    # Deliberately schematic route: not geographical data.
    for j in range(7):line(252,318+j*47,719,318+j*47,'#DCE4E7',5)
    for j in range(6):line(270+j*82,307,270+j*82,653,'#E0E7E9',4)
    pts=[(288,603),(378,603),(378,511),(512,511),(512,393),(666,393)]
    for a,b in zip(pts,pts[1:]):line(*a,*b,PURPLE,6)
    for i,(x,y) in enumerate(pts):
        circle(x,y,10,WHITE);circle(x,y,5,PURPLE);text(str(i+1),x+15,y-8,9,INK,'Bold')
    rect(263,322,202,41,WHITE,8);text('Route 04  •  Afternoon trip',276,335,11,INK,'Bold')
    chip('Bus 04',492,480);text('Illustrative route • not to scale',252,650,9,MUTED)
    ucard('Route 04 • Lake Road',756,290,292,230)
    text('On schedule',775,335,20,GREEN,'Bold');text('Last update: 12 seconds ago',775,368,10,MUTED)
    for i,(l,v) in enumerate([('On board','28 / 32'),('Driver','R. Kumar'),('Attendant','S. Devi'),('Next stop','Cedar Avenue')]):
        yy=404+i*25;text(l,775,yy,10,MUTED);text(v,1028,yy,10,INK,'UI','right')
    ucard('Trip activity',756,538,292,134)
    text('15:12   Departed school',775,580,10,INK);text('15:18   Stop 1 completed',775,608,10,INK);text('15:23   Stop 2 completed',775,636,10,MUTED)
    annotations('Review assigned route → board/alight roster → record exceptions and handover.','Stale location displays its age and no ETA; families see only authorized trips.')

    mobile_screens()

    # S18
    screen('S18','Roles & access','Administration • IAM, INT • explicit permissions with understandable scopes',nav='Overview',action='Save role')
    text('Role: Class teacher  ▾       Template: Teaching staff',236,295,12,INK,'Bold')
    rect(236,330,247,342,WHITE,11,LINE)
    text('Role templates',254,348,13,INK,'Bold')

    for i,l in enumerate(['School owner','Principal','Class teacher','Finance officer','School nurse','Librarian','Guardian']):
        yy=391+i*35
        if i==2:rect(246,yy-5,227,31,LAV,6)
        text(l,260,yy+2,11,PURPLE if i==2 else MUTED,'Bold' if i==2 else 'UI')
    ui_table(['CAPABILITY','ACTION','SCOPE'],[
      ['Student basics','View','Assigned classes'],
      ['Attendance','Create / correct','Assigned sessions'],
      ['Homework','Manage','Assigned subjects'],
      ['Marks','Draft / submit','Assigned subjects'],
      ['Final results','View published','Assigned classes'],
      ['Financial records','No access','—'],
      ['Health records','Care alert only','Assigned pupils']
    ],501,330,width=547,ratios=[1.5,1.2,1.5],rowh=40)
    annotations('Start from template → adjust bounded actions/scopes → preview access → save.','No role grants beyond the editor’s authority; sensitive changes require audit.')

    # S19
    screen('S19','SaaS operations','Platform control plane • PLT • operational metadata without child records',nav='Overview',action='+ Create tenant',operator=True)
    for i,(l,v,d) in enumerate([('Active schools','124','8 onboarding this month'),('Active students','1.82L','Illustrative billable usage'),('Service availability','99.97%','Illustrative last 30 days')]):
        metric(l,v,d,236+i*276,290,260)
    ui_table(['SCHOOL','PLAN','STUDENTS','LIFECYCLE','HEALTH'],[
      ['Greenfield School','Growth','1,248','@Active','Healthy'],
      ['Cedar Valley Academy','Core','842','@Active','Healthy'],
      ['Northstar Public School','Growth','2,180','Onboarding','Setup 72%'],
      ['Maple International','Enterprise','4,920','@Active','Healthy'],
      ['Hillview School','Core','615','!Grace period','Billing review']
    ],236,402,ratios=[1.9,1.2,1,1.2,1.1],rowh=40)
    rect(236,651,812,31,LAV,7);text('Support access requires an approved school grant. All service metrics shown here are fictional.',249,661,10,PURPLE)
    annotations('Review tenant lifecycle/health → resolve onboarding, usage or billing tasks.','School data requires a separate time-limited grant; suspension follows policy.')

    # S20
    screen('S20','Library desk','Resource circulation • LIB • books, borrowers and availability in one view',nav='Operations',action='Issue a book')
    for i,(l,v,d) in enumerate([('Copies available','4,216','Across 1,780 titles'),('On loan','384','Across 296 borrowers'),('Overdue','18','Reminders ready for review')]):
        metric(l,v,d,236+i*276,290,260)
    rect(236,400,812,41,WHITE,8,LINE);text('Scan barcode or search title, author, accession number…',253,414,11,MUTED)
    books=[('The Blue Umbrella','Ruskin Bond','Fiction','#B7B0E4'),('A World of Numbers','Learning collection','Mathematics','#92C5B9'),('Our Living Planet','Science collection','Science','#E1B983'),('Stories of Discovery','Reading collection','Non-fiction','#9DB6D9')]
    for i,(title,author,cat,color) in enumerate(books):
        xx=236+i*207;rect(xx,460,191,213,WHITE,11,LINE)
        rect(xx+17,476,44,65,color,4);line(xx+24,477,xx+24,539,WHITE,1)
        text(cat.upper(),xx+76,480,8,PURPLE,'Bold');chip('Available',xx+73,506,GREEN,PALE)
        para('<b>'+title+'</b>',xx+17,554,160,13,INK,17);text(author,xx+17,596,9,MUTED)
        button('View copies',xx+17,626,157,False)
    annotations('Scan borrower + copy → validate limits → issue → renew or return.','Only one open loan per copy; lost/damaged fines use reviewed policies.')

    # S21
    screen('S21','Purchasing & inventory','Procurement • INV • clear status from request to receipt',nav='Operations',action='+ Requisition')
    for i,(l,v,d) in enumerate([('Awaiting approval','8','3 above department limit'),('Open orders','14','₹ 4.2L committed'),('Low-stock items','6','Review reorder quantities')]):
        metric(l,v,d,236+i*276,290,260)
    ui_table(['REQUEST','DEPARTMENT','VALUE','STAGE','OWNER'],[
      ['REQ-041 • Lab supplies','Science','₹ 48,000','!Approval','A. Iyer'],
      ['REQ-042 • Library books','Library','₹ 32,500','@Ordered','F. Khan'],
      ['REQ-043 • Sports kits','Sports','₹ 18,200','Receiving','R. Singh'],
      ['REQ-044 • Projector','Academics','₹ 42,000','!Approval','P. Menon'],
      ['REQ-045 • Stationery','Office','₹ 8,400','@Received','N. Das']
    ],236,402,ratios=[2,1.1,1,1.2,1],rowh=40)
    text('Requester → Budget check → Approval → Purchase order → Goods receipt → Reconciliation',252,665,10.5,PURPLE,'Bold')
    annotations('Review request and budget → approve → order → receive quantities → reconcile.','Partial receipts keep orders open; requester cannot approve controlled spend.')

    # S22
    screen('S22','Help & service desk','Support and operations • OPS, PLT • shared accountability with scoped conversations',nav='Operations',action='+ New ticket')
    rect(236,290,276,382,WHITE,11,LINE);text('Your queues',254,307,14,INK,'Bold')
    for i,(t,d) in enumerate([('Open tickets','12'),('Awaiting school','4'),('Assigned to me','5'),('Resolved this week','28')]):
        yy=352+i*43;text(t,254,yy,11,INK);chip(d,452,yy-5)
    rect(253,554,242,96,LAV,9);text('Need product support?',267,568,11,PURPLE,'Bold')
    para('Create a time-limited support grant only when needed.',267,592,213,10.5,MUTED,16)
    ucard('TKT-1042 • Payment receipt not visible',530,290,518,382)
    chip('In progress',548,334);text('Owner: Finance team  •  Priority: Normal',548,372,10,MUTED)
    rect(548,405,482,78,BG,9);text('Neha Mehta  •  Parent',563,418,10,INK,'Bold')
    para('My payment shows as pending. Please help me confirm the receipt for invoice INV-26142.',563,440,450,10.5,MUTED,16)
    rect(548,500,482,78,LAV,9);text('Finance team  •  Visible to parent',563,513,10,PURPLE,'Bold')
    para('We are checking the provider confirmation. Please wait before making another payment.',563,536,450,10.5,INK,16)
    button('Reply to parent',548,620,159)
    text('Internal note  /  Add attachment',730,630,10,MUTED)
    annotations('Classify → assign → investigate → reply → resolve with an auditable outcome.','Internal notes stay private; platform support requires a separate school grant.')

    # S23
    screen('S23','School insights','Analytics • ANA • explainable trends and permission-aware drilldowns',nav='Reports',action='Export report')
    text('Academic year 2026–27  ▾       Main campus  ▾       Term 2  ▾',236,292,11,INK)
    ucard('Attendance by grade',236,330,395,258)
    vals=[96,94,97,95,92,96]
    for i,v in enumerate(vals):
        xx=262+i*58;bh=v*.95;rect(xx,539-bh,32,bh,'#C9C2F4' if i!=4 else PURPLE,5)
        text(str(v)+'%',xx+16,518-bh,10,INK,'Bold','center');text(str(i+3),xx+16,554,10,MUTED,'UI','center')
    text('Grade',252,571,9,MUTED)
    ucard('Monthly fee collections',649,330,399,258)
    for j in range(4):line(669,405+j*38,1028,405+j*38)
    spark(676,412,340,112,[12.3,14.8,13.9,17.1,16.3,18.4])
    for i,m in enumerate(['Jun','Jul','Aug','Sep','Oct','Nov']):text(m,673+i*67,560,9,MUTED)

    rect(236,607,812,68,WHITE,10,LINE)
    text('Metric definitions are part of the report',254,619,13,INK,'Bold')
    text('Attendance excludes holidays and unmarked entries. Collections reflect verified receipts, not bank settlement.',254,645,10.5,MUTED)
    annotations('Choose scope → inspect definitions → drill into records → schedule/export.','Filters apply to charts and downloads; small sensitive cohorts are restricted.')

def phone(x,y,title,child='Aarav • Grade 6 A',tab='Today'):
    rect(x-3,y-3,272,489,NAV,27)
    rect(x,y,266,483,BG,24)
    text('9:41',x+21,y+13,10,INK,'Bold');text('•••  ▰',x+244,y+13,10,INK,'UI','right')
    text(title,x+18,y+48,22,INK,'Bold')
    text(child+'  ▾',x+18,y+81,10,MUTED)
    rect(x,y+432,266,51,WHITE,18)
    nav_items=['Today','Classes','Tasks','Inbox'] if 'Teacher' in child else ['Today','Learn','Fees','Inbox']
    for i,l in enumerate(nav_items):
        text(l,x+34+i*65,y+451,10,PURPLE if l==tab else MUTED,'Bold' if l==tab else 'UI','center')

def mobile_screens():
    newpage('S15 / The family day, beautifully simple.','04 / Screen design','Parent portal • FAM, FEE, PAY • three connected mobile views')
    for i,t in enumerate(['Today','School fees','Payment status']):
        phone(109+i*329,181,t,tab='Fees' if i else 'Today')
    x=109
    rect(x+16,289,234,91,LAV,12);text('A good day to learn.',x+30,303,15,INK,'Bold')
    text('Tuesday, 10 November',x+30,331,10,MUTED);chip('Present today',x+28,352,GREEN,PALE)
    text('Your next actions',x+17,400,13,INK,'Bold')
    for j,(t,d) in enumerate([('Fractions worksheet','Due tomorrow • Mathematics'),('Term 2 instalment','₹ 12,000 due 15 Nov'),('Parent–teacher meeting','Choose a time slot')]):
        yy=432+j*54;rect(x+16,yy,234,47,WHITE,8,LINE);text(t,x+28,yy+8,11,INK,'Bold');text(d,x+28,yy+28,9,MUTED)
    x=438
    rect(x+16,289,234,117,WHITE,12,LINE);text('Amount due',x+30,304,11,MUTED);text('₹ 12,000',x+30,330,30,INK,'Bold');text('INV-26142 • Due 15 Nov',x+30,377,10,MUTED)
    for j,(a,b) in enumerate([('Tuition instalment','₹ 10,000'),('Transport','₹ 2,000'),('Total due','₹ 12,000')]):
        yy=430+j*37;text(a,x+18,yy,11,MUTED);text(b,x+248,yy,11,INK,'Bold','right')
    button('Continue to secure payment',x+16,553,234)
    text('UPI • Cards • Netbanking',x+133,595,9,MUTED,'UI','center')
    x=767
    circle(x+133,331,33,PALE);text('✓',x+133,306,36,GREEN,'Bold','center')
    text('Payment received',x+133,387,20,INK,'Bold','center')
    text('₹ 12,000',x+133,426,27,PURPLE,'Bold','center')
    para('Your school has confirmed the payment. Receipt RCPT-26184 is ready.',x+26,477,214,12,MUTED,18)
    button('Download receipt',x+16,553,234)
    annotations('Home → invoice detail → hosted payment → verified receipt.','If confirmation is delayed, show pending and discourage duplicate payment.')

    newpage('S16 / Attendance from the classroom.','04 / Screen design','Teacher mobile • ATT • touch-first entry with visible offline and review states')
    for i,t in enumerate(['My teaching day','Grade 6 A','Review attendance']):
        phone(109+i*329,181,t,child='Priya Menon • Teacher',tab='Today')
    x=109
    rect(x+16,289,234,88,LAV,12);text('Good morning, Priya',x+29,304,15,INK,'Bold');text('3 lessons • 1 register to finish',x+29,338,10,MUTED)
    for j,(t,d) in enumerate([('08:30 • Mathematics','Grade 6 A • Room 201'),('10:25 • Mathematics','Grade 7 B • Room 204'),('12:05 • Class period','Grade 6 A • Room 201')]):
        yy=395+j*57;rect(x+16,yy,234,54,WHITE,8,LINE);text(t,x+29,yy+10,12,INK,'Bold');text(d,x+29,yy+32,10,MUTED)
    button('Take attendance',x+16,574,234)
    x=438
    chip('Offline • 4 changes queued',x+16,289,AMBER,'#FFF5DF')
    text('P Present  •  A Absent  •  L Late',x+17,317,8.5,MUTED)
    for j,n in enumerate(['Anika Patel','Aarav Mehta','Diya Rao','Ishaan Roy','Meera Shah']):
        yy=334+j*47;rect(x+16,yy,234,44,WHITE,8,LINE);text(n,x+28,yy+13,11,INK,'Bold')
        for k,l in enumerate(['P','A','L']):
            selected=k==[0,0,1,0,2][j]
            active_color=[PURPLE,ROSE,AMBER][k]
            rect(x+149+k*28,yy+10,23,24,active_color if selected else BG,5);text(l,x+160+k*28,yy+15,9,WHITE if selected else MUTED,'Bold','center')
    button('Review entries',x+16,574,234)
    x=767
    rect(x+16,289,234,105,WHITE,12,LINE)
    for j,(v,l) in enumerate([('30','Present'),('1','Absent'),('1','Late')]):
        text(v,x+54+j*80,307,28,INK,'Bold','center');text(l,x+54+j*80,354,10,MUTED,'UI','center')
    text('One absence to confirm',x+18,422,14,INK,'Bold')
    para('Diya Rao • Leave request received.<br/><br/>The guardian alert is sent only after the register is finalized.',x+18,458,230,12,MUTED,19)
    button('Finalize when online',x+16,574,234)
    annotations('Open class → mark students → review totals → finalize when synchronized.','Offline changes are drafts; conflicting newer corrections need explicit resolution.')

    newpage('S17 / Learning with a clear next step.','04 / Screen design','Student mobile • LMS, FAM • from assignment to a confirmed submission')
    for i,t in enumerate(['My learning','Fractions at home','Submission ready']):
        phone(109+i*329,181,t,child='Aarav Mehta • Grade 6 A',tab='Learn')
    x=109
    rect(x+16,289,234,86,LAV,12);text('You’re making progress.',x+28,306,14,INK,'Bold');text('2 tasks to finish this week',x+28,338,10,MUTED)
    for j,(t,d) in enumerate([('Fractions at home','Mathematics • Due tomorrow'),('The story around us','English • Due 14 Nov'),('Our solar system','Science • Feedback ready')]):
        yy=400+j*64;rect(x+16,yy,234,55,WHITE,8,LINE);text(t,x+28,yy+10,12,INK,'Bold');text(d,x+28,yy+33,9,MUTED)
    x=438
    chip('Due 11 Nov, 17:00',x+16,289)
    para('<b>Find fractions in your day.</b><br/><br/>Choose three examples from home. Draw each example and label the fraction.<br/><br/>Upload a clear photo or PDF of your work.',x+18,338,230,13,INK,20)
    rect(x+16,507,234,55,WHITE,9,LINE);text('Practice sheet.pdf',x+30,519,11,PURPLE,'Bold');text('PDF • 280 KB',x+30,541,9,MUTED)
    button('Add my work',x+16,574,234)
    x=767
    circle(x+133,331,33,PALE);text('✓',x+133,306,36,GREEN,'Bold','center')
    text('Your work is submitted',x+133,390,17,INK,'Bold','center')
    para('Submitted 10 Nov, 16:42<br/>fractions-aarav.pdf • 1.2 MB<br/><br/>Your teacher will share feedback here.',x+24,439,218,12,MUTED,20)
    button('View my submission',x+16,574,234,False)
    annotations('Find assigned work → read instructions → upload → confirm submission.','Uploads show progress/retry; allowed resubmission creates a new version.')



def closing():
    newpage('Design the difficult moments, too.','04 / States & interaction patterns','These states are part of every applicable screen’s definition of done.')
    states=[
      ('Empty / first use','No students yet','Import your student list or add your first student.','Import students',BG),
      ('Validation / inline','A little more information','Add the required due date before creating this invoice.','Review highlighted fields','#FFF5DF'),
      ('Offline / queued','Saved on this device','4 attendance changes are waiting to sync. Keep this device secure.','Retry connection',LAV),
      ('Conflict / stale data','This register has changed','Another teacher saved a newer version. Review both changes.','Compare changes','#FFF5DF'),
      ('Payment / pending','We’re confirming your payment','You can safely leave this page. Please wait before paying again.','Check payment status',LAV),
      ('Access / permission','This record is restricted','Your current role does not include this action. Contact your school admin.','Return to workspace',BG)
    ]
    for i,(label,title,body,action,color) in enumerate(states):
        x=48+(i%3)*347;y=181+(i//3)*265
        text(label.upper(),x,y,9.5,PURPLE,'Bold')
        rect(x,y+28,330,211,color,12,LINE)
        heading(title,x+19,y+47,292)
        para(body,x+19,y+90,292,12,MUTED,18,maxh=66)
        button(action,x+19,y+185,292,False)
    note('Also implement loading skeletons, no search results, expired sessions, failed uploads, safe destructive confirmation and success feedback.',718)

    newpage('Screen index & requirement traceability.','04 / Design handoff','The 23 screen concepts cover representative high-value journeys. Related modules reuse the same component system.')
    screen_pages=[p for p in pages if p['title'].startswith('S') and p['title'][1:3].isdigit()]
    refs=['TEN / IAM','TEN / ATT / FEE / ANA','ADM','SIS','SIS / HLT / FAM','ATT','ACA / TIM','LMS','EXM','FEE / FIN','PAY / FIN','HRM','COM','TRN','FAM / FEE / PAY','ATT','LMS / FAM','IAM / INT','PLT','LIB','INV','OPS / PLT','ANA']
    rows=[]
    for p,r in zip(screen_pages,refs):
        sid,title=p['title'].split(' / ',1);rows.append([sid,title,r,str(p['page'])])
    table(['ID','SCREEN / EXPERIENCE','REQUIREMENTS','PAGE'],rows,y=176,rowh=21,size=9.5,ratios=[.5,3.5,1.6,.4])
    note('Each module also includes an acceptance scenario. The companion CSV lists every functional requirement with module, phase and screen references.',700)

    newpage('Source notes & implementation handoff.','Sources / version 1.0','Primary references checked for this blueprint on 10 November 2026. Product requirements are original recommendations.')
    y=178
    for num,topic,title,url,desc in SOURCES:
        chip('['+num+']',48,y)
        heading(topic+' • '+title,106,y,966)
        ph=para(desc,106,y+30,946,12,MUTED,17)
        linktext='Open official source ↗'
        text(linktext,106,y+ph+39,10.5,PURPLE,'Bold')
        c.linkURL(url,(106,H-(y+ph+55),285,H-(y+ph+38)),relative=0)
        y+=102
    rect(48,700,1024,34,LAV,8)
    text('Handoff: PDF + requirements CSV + screen previews + editable Python source + build/verification notes.',64,710,10.5,PURPLE,'Bold')

cover()
intro()
modules()
technical()
screens()
closing()
c.save()
(ROOT/'page-map.json').write_text(json.dumps(pages,indent=2),encoding='utf-8')
(ROOT/'source'/'layout-check.json').write_text(json.dumps(errors,indent=2),encoding='utf-8')
with (ROOT/'CampusOS-Requirements.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.writer(f)
    writer.writerow(['Requirement ID','Module','Phase','Owner','Requirement','Implementation detail','Screen references','Module business rules','Module acceptance check'])
    for m in MODULES:
        for i,row in enumerate([r for r in m['requirements'] if len(r)==2],1):
            writer.writerow([m['code']+'-'+str(i).zfill(2),m['title'],m['phase'],m['owner'],*row,m['screens'],m['rules'],m['acceptance']])
print(json.dumps(dict(pages=len(pages),modules=len(MODULES),requirements=sum(len([r for r in m['requirements'] if len(r)==2]) for m in MODULES),layout_warnings=errors),indent=2))


