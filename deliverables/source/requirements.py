"""Original implementation catalogue for CampusOS. P0=launch; P1=expansion; P2=optional."""
MODULES=[]
def add(code,title,phase,owner,screens,outcome,reqs,rules,test):
    MODULES.append(dict(code=code,title=title,phase=phase,owner=owner,screens=screens,outcome=outcome,requirements=[r.split('|',1) for r in reqs.strip().split('\n')],rules=rules,acceptance=test))

add('TEN','Tenant setup & onboarding','P0','School owner / SaaS operations','S01, S02, S19','Create an isolated school workspace with a verifiable path to its first live day.','''
Workspace creation|Verify the owner; capture legal/display names, billing contact, timezone, language and workspace slug. Support school groups, campuses and delegated administrators.
Guided setup|Save progress through academic year, grades, subjects, staff, students, fees and communications. Show dependencies, task owners and completion evidence.
Configuration|Set branding, working week, holidays, number/date formats, document sequences and portal preferences. Preview receipts and report cards.
Invitations & imports|Use expiring single-use invitations. Provide import preview, duplicate review, row errors, checkpoints and reconciliation summaries.
Activation & domains|Check rosters, verified sender, fee test, backup and sample family login. Isolate demo data. Verify custom-domain ownership before DNS/TLS mapping.
Exit lifecycle|Support exports, notice periods, retention holds, cancelled deletion requests and scheduled removal of operational data. Explain backup expiry separately.
''','Resolve tenant identity server-side. Campus scope never replaces tenant isolation. Sandbox actions cannot message real families.','Two schools with identical admission numbers see only their own records, files, search and exports. Retried setup creates one tenant.')

add('IAM','Identity, roles & permissions','P0','Owner / security administrator','S01, S18','Authorize actions through role, assignment, relationship and field sensitivity.','''
Authentication|Offer verified email/phone sign-in, secure recovery and session management. Require MFA for privileged roles; provide recovery codes. Add enterprise SSO in P2.
Membership model|Separate login accounts from staff, student and guardian profiles. Support people in several schools, staff across campuses and guardians with several children.
Authorization|Check tenant, campus, role, academic year, class assignment and guardian relationship on APIs, exports, jobs and downloads. Deny by default.
Role templates|Ship owner, principal, registrar, teacher, finance, HR, librarian, transport, counsellor, guardian, student and support roles. Provide bounded custom roles and effective-access preview.
Delegation & approval|Time-limit substitute access. Require step-up verification and independent approval for refunds, large waivers, payroll release, report reissue and bulk exports.
Lifecycle|Handle expired invites, staff departure, custody changes and shared-device logout. Revoke sessions on access changes. Recovery responses must avoid account enumeration.
''','A role alone does not establish child access. Support has no default student-data access; grants require school authorization, scope and expiry.','A teacher cannot fetch another section by changing an ID. Revoked guardians lose access immediately. A requester cannot approve their own refund.')

add('ADM','Admissions & enquiry CRM','P0','Admissions team / principal','S03','Convert enquiries into capacity-checked enrolments with complete application history.','''
Intake|Capture web, walk-in, phone and referral enquiries with source, target grade, owner and follow-up. Flag possible duplicates without automatically merging families.
Applications|Build versioned grade-specific forms with conditional fields, saved drafts, document checklists, notices and accessible public links.
Pipeline|Track enquiry, applied, review, assessment, offered, waitlisted, accepted and withdrawn stages, with tasks, history and decision reasons.
Assessment & offers|Book interviews with capacity checks; capture rubrics and restricted notes. Issue versioned offers with expiry, fee terms and outstanding documents.
Seats & conversion|Apply school-approved allocation policy. Atomically reserve seats, verify deposits and convert applicants into student, guardian and enrolment records once.
Reporting|Show source performance, conversion, time in stage, incomplete applications and grade capacity. Export reviewed application packets with scoped access.
''','Check offer expiry and capacity at acceptance. Applicant retention differs from permanent academic-record retention. Admission criteria are configurable.','Concurrent acceptances for the last seat yield one enrolment and one clear capacity error. Repeated conversion cannot create duplicate students.')

add('SIS','Student information & lifecycle','P0','Registrar / class teacher','S04, S05','Keep reliable records across family changes, years, transfers and graduation.','''
Student master|Maintain admission number, preferred/legal name, birth date, photo, address and emergency contacts. Collect additional identifiers only for a defined approved purpose.
Family relationships|Track guardian role, communication preference, financial responsibility, emergency priority, authorized pickup and contact restrictions. Verify relationship changes.
Enrolment history|Store effective-dated campus, year, grade, section, roll number, house and electives. Preserve prior placements when classes change.
Documents|Scan/version uploads; track verification, expiry and download audit. Generate ID cards, bonafide/study and transfer certificates from approved templates.
Promotion & rollover|Preview promotion, retention, transfers and graduation. Copy selected settings, reconcile fee carry-forward and commit an approved batch with recovery planning.
Corrections & alumni|Require reason/review for identity changes and duplicate merges. Preserve source references. Separate opt-in alumni engagement from retained academic records.
''','Never overwrite historical enrolments or issued reports. Custody restrictions apply to messages, files and search. Admission-number corrections are audited.','Rollover changes current classes while preserving last year’s report. A section transfer changes future rosters without rewriting past attendance.')

add('ACA','Academic setup & calendars','P0','Academic coordinator','S07, S08','Support varied curricula, grade structures and school-year conventions.','''
Academic periods|Define years, terms, assessments, working days, holidays and campus exceptions. Lock completed periods with controlled reopening.
Grades & groups|Manage sections, capacities, class teachers, houses, composite teaching groups and cross-section electives.
Subjects|Maintain codes, language options, compulsory/elective rules, practical components and grade-specific offerings.

Board profiles|Version school-validated configurations for CBSE, CISCE and state-board needs. Use configurable rules and templates without claiming board certification.
Teacher allocations|Assign subject/class responsibilities, workloads and effective dates. Retain assignment history for reporting and permissions.
Publishing & cloning|Publish calendars and closure updates. Clone a draft year, compare differences, check missing allocations and require coordinator review.
''','Do not hardcode April-to-March for every school. Calendar changes flag affected attendance, timetable and billing rules.','Two schools can use different practical weightings, term structures and language electives without affecting each other.')

add('TIM','Timetable & substitutions','P0 manual / P1 solver','Timetable coordinator','S07','Publish workable schedules across teachers, rooms, sections and resources.','''
Period templates|Configure periods, breaks, assemblies, rotating weeks and special days, with distinct primary/senior templates.
Scheduling|Offer weekly editing, collision checks, workloads, missing periods and accessible keyboard/list alternatives.
Constraints|Separate hard rules such as availability from soft preferences such as balanced subjects. Explain every conflict precisely.
Versions|Draft, compare, approve and publish with effective dates. Preserve the schedule used for historical attendance.
Substitutions|Find eligible available teachers, record acceptance, notify affected classes and grant only temporary session access.
Generation & sharing|In P1 generate candidate schedules with explanations and locked slots. Require review. Offer teacher/class/room views, print and revocable calendar feeds.
''','Hard conflicts block publication. A solver must report an infeasible schedule rather than silently break a hard rule.','One teacher cannot occupy concurrent classes. Published substitutions update both schedules and temporary access correctly.')

add('ATT','Attendance & leave','P0','Teachers / attendance officer','S06, S16','Make attendance fast to record, safe to correct and accurate to report.','''
Registers|Build daily/period rosters from effective enrolments and calendars. Distinguish present, absent, late, excused, unmarked and not scheduled.
Fast marking|Provide touch/keyboard entry, all-present with review, notes, draft saving and an unmarked count before submission.
Offline capture|Queue minimal records on approved devices with expiry and visible pending sync. Use server versions to detect conflicts.
Corrections|Apply deadlines, locks, correction reasons and approvals. Retain before/after values, actor and server receipt time.
Leave & alerts|Accept guardian leave requests with limited attachments. Delay finalized absence alerts; cancel queued alerts when mistakes are corrected.
Analysis|Show register completion, trends and policy-based absence thresholds. Explain denominator exclusions for holidays, future and pre-admission dates.
''','Unmarked is not absent. Replayed offline events cannot overwrite a newer approved correction. Device time is not the authoritative sequence.','Conflicting device edits require resolution. Withdrawn pupils remain in history but leave future rosters. Duplicate sync produces one change.')

add('LMS','Teaching, homework & learning','P0 basics / P1 advanced','Teachers / students','S08, S17','Connect lessons, assignments, submissions and deliberately released feedback.','''
Lesson planning|Plan units, objectives, resources and syllabus coverage with coordinator review and reusable school-scoped plans.
Assignments|Set instructions, attachments, rubrics, recipients, due dates and submission types. Draft, schedule, publish, revise and close.
Submission|Provide text/files, progress, scanning, drafts, late flags, resubmissions and individual extensions.
Marking|Support rubric scores, private comments, annotated work and return-for-rework. Release scores explicitly rather than while marking drafts.
Resources & quizzes|Manage access-controlled resources. In P1 add formative quizzes, question banks, objective auto-marking, attempts and accommodations.
Progress & sessions|Show missing work and coverage without public student ranking. Add approved virtual-class links/recordings in P1 with sharing and retention controls.
''','Published changes notify recipients. Retain submission versions. Teachers review automated marking; high-impact decisions are not fully automated.','An extension changes one student’s deadline. Draft scores remain private until release. Students cannot download one another’s submissions.')

add('EXM','Examinations & report cards','P0','Exam coordinator / teachers','S09','Generate approved, reproducible results and traceable report-card versions.','''
Assessment rules|Configure components, maxima, pass rules, weightings, grade bands, rounding and absent/exempt codes. Version by year/grade.
Logistics|Schedule rooms/invigilators, accommodations, seating and admit cards. Detect student, room and teacher collisions.
Marks entry|Restrict entry to assigned subjects. Validate imports, ranges and required fields; distinguish zero, absent, exempt and missing.
Moderation|Use draft, submitted, reviewed, approved and published states. Lock submissions; require reason and authorization to reopen.
Report generation|Create branded multilingual-ready PDFs with grades, competencies, attendance, remarks and signatories. Snapshot values and calculation rules.
Publication & appeals|Release by cohort on schedule. Provide secure family access, review requests and controlled reissue retaining prior versions and reasons.
''','Required missing marks block publication. Scheme changes do not alter issued reports. Fee arrears must not automatically hide results.','Screen and PDF use the same rounding. Reissue creates a new version and publication record while the original remains reproducible.')



add('FEE','Fees, concessions & receivables','P0','Finance officer / approver','S10, S15','Create correct charges, transparent balances and controlled adjustments.','''
Plans|Configure tuition, admission, transport, hostel and optional heads, instalments, due dates, effective dates and explicit late-fee rules.
Allocations|Assign by enrolment/service. Preview proration, joins, withdrawals, sibling benefits and opening balances before posting.
Concessions|Manage scholarships, waivers and discounts with eligibility, validity, caps, funding and approval. Prevent incompatible stacking.
Invoices|Number line-item invoices; support partial payments, credit notes, cancellation and student/family ledgers. Store money in minor units.
Collections|Record cash, cheque, transfer and verified online payments. Track cheque pending/cleared/bounced; reconcile cashier sessions and receipts.
Dues & refunds|Show aging, installment plans and disputes; pause contested reminders. Apply overpayments as credits. Refund only eligible unrefunded payments.
''','Reverse posted entries instead of editing them. Student fees and SaaS invoices use separate accounts/sequences. Tax treatment requires accounting review.','Partial payment reduces the correct balance. Credit notes post once. Cashiers cannot approve their own waivers or refunds.')

add('PAY','Payments & reconciliation','P0','Finance / payment operations','S11, S15','Match student balances, provider records and bank settlements without double posting.','''
Merchant setup|Use school-owned approved gateway accounts; segregate tenant and test/live credentials. Track merchant onboarding and secret rotation.
Checkout|Use provider-hosted UPI/cards/netbanking where available. Bind orders to amount, currency, invoice and payer; expire stale attempts.
Verification|Treat redirects as pending evidence. Verify raw-byte webhook signatures, merchant context and provider status before issuing confirmed receipts.
Durable processing|Persist verified events, deduplicate event IDs and enforce unique business postings. Handle retries and out-of-order events with explicit states.
Reconciliation|Match captures, receipt allocations, refunds, gateway charges and bank settlements. Assign unmatched exceptions and run daily reconciliation.
Recovery & disputes|Poll unresolved attempts, safely retry jobs and audit replay. Track chargebacks/refund deadlines and show pending states without repeated-pay prompts.
''','Captured, receipted and settled are distinct. Settlement charges cannot reduce the student’s paid amount. Confirm provider contracts; see [4].','Ten concurrent duplicate capture events create one receipt/posting. Late authorization cannot move a captured payment backwards.')

add('FIN','Accounting & financial controls','P1','Accountant / school management','S10, S11','Provide auditable operational books and a controlled accounting handoff.','''
Subledger|Use balanced double-entry postings for receivables, collections, concessions, refunds and gateway clearing. Agree mappings with accountants.
Cash controls|Track opening float, shifts, mode totals, variance explanations, supervisor sign-off and protected receipt sequences.
Expenses|Manage vendors, bills, categories, cost centres, attachments and approvals. Capture settlement references without putting credentials in notes.
Budgets|Track department/campus budgets, commitments and actual spend. Route exceptional purchases and threshold breaches.
Bank reconciliation|Import statements with duplicate detection, suggested matches, source provenance, unresolved items and reconciliation locks.
Close & export|Restrict backdating, approve adjustments and close periods. Reconcile counts/totals when exporting to accounting packages. Validate statutory filing separately.
''','Every journal balances within one currency. Reopening a period requires a named approver.','Refunds and gateway charges produce balanced entries. Ordinary users cannot post in closed periods. Export retries do not duplicate postings.')

add('HRM','Staff, leave & payroll','P0 staff / P1 payroll','HR / payroll approver','S12','Manage employment, availability and a reviewable payroll cycle.','''
Staff records|Maintain employee IDs, roles, qualifications, contracts, join/exit dates and emergency contacts. Restrict bank, identity and salary fields.
Leave & attendance|Set shifts, balances, requests and approvals. Reconcile approved leave with payroll and timetable substitutions.
Pay structures|Version allowances, deductions, reimbursements, arrears and effective dates. Separate recurring and one-time components.
Payroll runs|Draft with exceptions and comparisons, independently approve, lock, disburse and reconcile failed payments.
Payslips & local rules|Publish secure versioned payslips. Configure applicable PF, ESI, TDS and professional tax using current reviewed inputs or a payroll provider.
Lifecycle|Manage onboarding, document expiry, training, appraisal, clearance and final settlement. Reassign duties and revoke access at departure.
''','No statutory rates are prescribed here. General administrators do not automatically see salaries. Published payroll is corrected through a new version.','Retroactive salary changes create visible arrears. Teachers retrieve only their own payslips. Preparers cannot release their own run.')

add('COM','Communication & engagement','P0','School office / teachers','S13','Deliver targeted messages with clear consent, recipients and delivery status.','''
Notices|Compose categorized notices, translations, attachments and expiry. Preview recipients, schedule sends and approve sensitive broadcasts.
Channels|Launch in-app/email, then approved SMS/WhatsApp. Distinguish provider acceptance, delivery, failure and read status.
Preferences|Respect purpose, consent, verified contacts and guardian restrictions. Apply quiet hours with an authorized emergency override.
Templates|Version templates/approvals. Support provider-required Indian SMS sender/template registration and quotas.
Conversations & meetings|Offer moderated family-school conversations, office hours, escalation and safe attachments. Book parent-teacher slots with capacity/rescheduling.
Feedback & costs|Collect surveys, acknowledgement and consent. Estimate billable sends, deduplicate recipients, save audience snapshots and handle applicable opt-outs.
''','Read receipts do not prove consent. Contact changes recheck verification and permission. Emergency override is recorded.','A section notice reaches only authorized families. Correcting absence cancels its unsent alert. Failed delivery stays visible for recovery.')

add('FAM','Parent & student portals','P0','Guardians / students','S15, S17','Give families a clear daily view and safe paths to complete school tasks.','''
Home|Show today’s timetable, attendance, homework, notices and next action. Keep selected school/child visible across child switching.

Fees|Explain charges, concessions, allocations, disputes and pending payments. Provide hosted checkout and secure receipts.
Learning|Students access resources, submissions and released feedback. Guardians receive only school-approved learning information.
Requests|Handle leave, contact updates, certificates, pickup and meetings with status, expected response and history.
Accessible mobile|Provide language preference, readable type, keyboard/screen-reader support, large targets, low-bandwidth views and file-size hints.
Safety|Use minimal push content, authenticated deep links, verified guardian linking, age-appropriate permissions and expiring caches.
''','Student and guardian accounts are distinct. Switching children rechecks access. Unpaid fees do not automatically disable education access.','A guardian pays one child’s invoice and retrieves its receipt without other-family data. Revoked relationships lose inbox and file access.')

add('TRN','Transport & student pickup','P1','Transport manager / attendant','S14','Coordinate routes, riders and handover with honest tracking reliability.','''
Fleet|Track vehicles, capacity, drivers, attendants and permit/insurance/fitness expiry. Flag or block invalid assignments under school policy.
Routes|Configure stops, directions, schedules, academic-day applicability and effective-dated riders. Check capacity and pickup/drop windows.
Trips|Create daily manifests, record boarding/alighting and reconcile missing riders. Provide minimal offline manifests to attendants.
Location|Integrate approved GPS; show last update, signal loss and approximate ETA. Restrict tracking to active trips and authorized families.
Changes & incidents|Approve one-day stop/pickup changes, verify handover and notify attendants. Route breakdowns, delays and emergencies through a contact tree.
Fees & reports|Link subscriptions to fees. Report utilization, punctuality, missing boardings and expiry risks with restricted location history.
''','GPS is advisory, not guaranteed safety monitoring. Retention requires a justified duration. Never expose unrelated children’s locations.','Stale GPS visibly loses its ETA. Concurrent assignments cannot overfill a vehicle. Unauthorized families cannot access the trip.')

add('LIB','Library & circulation','P1','Librarian','S20','Track titles and individual copies from acquisition to withdrawal.','''
Catalogue|Separate bibliographic titles from accessioned copies; store author, language, ISBN, shelf, category and acquisition.
Loans|Issue, renew and return via barcode/QR; check borrower eligibility, limits, due dates and reservations.
Holds|Manage queues, pickup expiry and notifications. Prevent simultaneous loans of one copy.
Fines|Configure grace, caps, damage/loss and approved waivers. Integrate approved charges with finance without duplicates.
Stock & digital|Scan stocktakes, reconcile missing items and preserve history of withdrawn copies. Link licensed resources with access and expiry.
Reporting|Show overdue loans, circulation, stock value and borrower clearance at transfer/graduation with controlled borrowing-history access.
''','At most one open loan per copy. Fines require policy authorization. Digital material needs appropriate school permission.','Concurrent issues create one open loan. Returning a lost book triggers fine/refund review rather than an automatic refund.')

add('INV','Inventory, purchasing & assets','P1','Storekeeper / procurement','S21','Control purchasing and stock through auditable movements and approvals.','''
Items|Manage consumables, serialized assets, units, locations, reorder levels, campus ownership and relevant lots/expiry.
Purchasing|Handle requisition, budget check, quotations, approval, purchase order and cancellation using policy thresholds.
Receiving|Record partial deliveries, rejection, shortage, vendor return and invoice matching with evidence.
Movements|Issue, return and transfer with recipient/purpose. Block negative stock except under explicitly approved policy.
Assets|Assign devices, furniture and lab equipment to people/rooms. Track condition, warranty, repair, custody and disposal.
Audits|Count stock, investigate variances and approve adjustments. Report vendors, commitments and consumption; export reviewed accounting entries.
''','Separate requester and approver for controlled spend. Derive balances from movements rather than editable totals.','A partial receipt leaves an order partly open. Duplicate receipt imports cannot inflate stock. Unauthorized disposal is rejected.')

add('HLT','Health, wellbeing & safeguarding','P0 essentials / P1 casework','Nurse / safeguarding lead','S05 restricted panel','Support student care while isolating especially sensitive records.','''
Medical profiles|Collect necessary allergies, care instructions and emergency contacts. Separate detailed medical records from the general profile.
Clinic visits|Record observations, action, referral and notification. Medication workflows require documented authorization and trained staff.
Care permissions|Show assigned teachers only essential alerts. Treatment/counselling notes require explicit role and purpose.
Incidents|Capture concerns, witnesses and restricted evidence. Assign severity, owner, follow-up and escalation under school-approved procedures.
Case privacy|Use sealed permissions, redaction and restricted exports. Do not automatically share case notes through family portals.
Support & emergencies|Track accommodations/reviews with approved staff. Provide minimal emergency rosters and manual fallback; audit sensitive reads/exports.
''','Software does not diagnose or replace safeguarding judgement. Schools approve disclosure, escalation and retention procedures.','Finance cannot discover counselling notes via search, API or export. Teachers see necessary allergy instructions without detailed medical files.')

add('OPS','Front office, events & helpdesk','P1','Office / operations manager','S13, S22','Make campus visitors, requests and events accountable and easy to follow.','''
Visitors|Pre-register, verify hosts, issue expiring passes and log entry/exit. Minimize identity retention.
Pickup|Manage authorized people, one-time changes, gate verification and exceptions. Record staff releasing the child and the recipient.
Events|Set capacity, fees, schedule, consent, participants and emergency contacts. Manage waitlists, cancellation and refunds.
Facilities|Book rooms, grounds and equipment with collision checks, access rules and maintenance blackouts.
Helpdesk & office|Route IT, maintenance, academic and billing tickets with owner, priority and service target. Separate internal notes. Process certificates and dispatch.
Public pages|In P2 offer school pages, enquiry forms and announcements with consented media, moderation, accessible templates and spam protection.

''','Visitor approval is not pickup authorization. Public pages never expose private records. Ticket notifications respect participant scope.','Expired passes require renewal. Concurrent bookings cannot occupy one room. Internal notes remain hidden from families.')

add('EXT','Hostel, meals & enrichment','P2 optional','Wardens / activity leads','Reuse S04, S06, S21','Add residential and enrichment operations only where required.','''
Hostel|Model residences, rooms, beds, approved allocation policies, effective dates, waitlists and moves.
Residential attendance|Record roll call, overnight leave, guardian approval, gate movement and safe return; escalate unexplained absence.
Services|Track inspections, belongings, room issues, deposits and boarding fees. Limit wardens to relevant residents.
Meals|Plan menus, dietary instructions, headcounts and stock. Use controlled meal credits with explicit accounting/refunds; review wallet-like features separately.
Activities|Manage clubs, sports, teams, houses, achievements, instructors, consent, capacity and optional charges.
Community|Offer opt-in alumni events and authorized donations with separate receipts/accounts and engagement consent.
''','Residential leave does not change classroom attendance automatically. Staff verify dietary instructions. Optional modules inherit tenant/access controls.','One bed cannot host overlapping stays. Cancelled paid activities follow refund approval. Wardens cannot access other residences.')

add('ANA','Analytics & reporting','P0 essentials / P1 advanced','Principal / group leadership','S02, S23','Make metrics traceable, permission-aware and useful for decisions.','''
Dashboards|Show attendance, admissions, fees, learning, staffing and services with role-appropriate campus/year/date filters.
Definitions|Show formula, population, exclusions, source and refresh time. Distinguish invoiced fees, collections, capture and settlement.
Drilldown|Preserve filters and access rules. Apply privacy restrictions for sensitive small cohorts.
Report library|Provide registers, aging, concessions, cash close, results, student strength, staff leave and audit reports with versioned layouts.
Exports|Generate large files asynchronously with expiry/counts/audit. Recheck scheduled recipients and authorization at download.
Assistive insight|In P2 add reviewed summaries and explainable exception suggestions. Do not automate admissions, discipline, final grading or eligibility decisions.
''','Group visibility is explicitly granted. Avoid unnecessary direct student identifiers in analytics. Totals reconcile to filtered source records.','Campus users cannot expand scope with crafted filters. A revoked user cannot download a previously generated report.')

add('INT','Migration, integrations & automation','P0 imports / P1 ecosystem','School IT / integrations','S18, S22','Move records and connect providers without losing traceability.','''
Templates|Support CSV/XLSX mapping, encoding/date checks, duplicates, dry runs and row errors. Reconcile student counts and opening balances.
Import jobs|Checkpoint chunks, quarantine invalid rows, preserve external IDs and produce manifests. Allow controlled rollback before activation.
APIs|Use versioned scoped APIs with pagination, limits, idempotency and deprecation. Derive tenant scope from validated membership.
Events|Publish signed minimal webhooks with IDs, retries, logs and audited replay. Restrict event types and destinations.
Connectors|Prioritize payments, messaging, accounting and calendars. Separately evaluate GPS, SSO, staff biometric devices and learning platforms.
Automation|Use allowed event-condition-action rules with dry run, caps, loop protection and approval for sensitive changes. Track provider health/credentials.
''','Government or board API access is not assumed. UDISE+ and board reporting start as reviewed export mappings pending a supported authorized interface.','Unchanged external IDs update/skip under the selected mode, with reconciled totals. Provider outages produce visible retry/manual states.')

add('PLT','SaaS control plane & support','P0 core / P1 enterprise','SaaS operations / customer success','S19, S22','Operate commercial subscriptions, tenant health, support and exits.','''
Console|Show tenant health, lifecycle, plan, campuses, usage and onboarding without child data by default.
Subscriptions|Track trial, active, past-due, grace, read-only, cancelled and closed states with notices/effective dates. Separate school billing from student fees.
Entitlements|Enforce features/quotas server-side. Record override owner, reason and expiry. Preserve historical reading/export after downgrade under contract.
Usage & invoices|Snapshot billable active students under a published definition; reconcile adjustments, invoices, renewals and credits.
Support grants|Require a ticket and school-approved scoped session with expiry/banner. Log actions and prohibit invisible permanent impersonation.
Operations & exit|Monitor queues, providers, hotspots and storage. Use staged flags/kill switches. Export, honor holds and delete operational copies under policy.
''','Subscription failure does not instantly remove critical-record access. Backup expiry is separate from live deletion.','Retrying a usage snapshot yields one invoice. Expired support grants cannot query students or download earlier exports.')

SOURCES=[
('1','Accessibility','W3C: Web Content Accessibility Guidelines 2.2','https://www.w3.org/TR/WCAG22/','Target WCAG 2.2 AA; visual mockups alone do not establish conformance.'),
('2','Security','OWASP: Application Security Verification Standard','https://asvs.owasp.org/','Use ASVS 5.0 as a verification catalogue. This blueprint does not constitute certification.'),
('3','India data protection','MeitY: DPDP Rules 2025, corrigendum and enforcement timeline','https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa','Validate current applicability, commencement and child-data obligations before launch; official material includes phased enforcement.'),
('4','Payment events','Razorpay: Validate and Test Webhooks','https://razorpay.com/docs/webhooks/validate-test/','Verify signatures and handle duplicate/out-of-order events. Confirm current chosen-provider contracts.'),
('5','Database isolation','PostgreSQL: Row Security Policies','https://www.postgresql.org/docs/current/ddl-rowsecurity.html','Row policies add isolation; owners and privileged roles require special care. Test the deployed version.')]


