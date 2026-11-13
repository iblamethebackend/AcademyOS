'use client';
import {useState} from 'react';
import {DashIcon as Icon} from './dashboard-icons';

type Feature={name:string;description:string;available?:boolean};
const groups:{name:string;icon:string;features:Feature[]}[]=[
 {name:'Your school, organised',icon:'school',features:[
  {name:'School onboarding & sign-in',description:'Owner registration, email verification, workspace sign-in and password recovery.',available:true},
  {name:'School profile & campuses',description:'School identity, contact details, workspace address and multiple campus locations.',available:true},
  {name:'Brand & preferences',description:'School colours, initials, date and number formats, document prefixes and portal preferences.',available:true},
  {name:'Guided setup & workspace overview',description:'A foundation checklist, setup progress and a view of your school records.',available:true},
  {name:'Access, approvals & school lifecycle',description:'Account invitations, scoped roles, approval workflows, custom domains and managed retention.'},
 ]},
 {name:'Every learner, every chapter',icon:'cap',features:[
  {name:'Student & team directories',description:'Basic student records, staff profiles and a directory of school departments.',available:true},
  {name:'Admissions & enquiries',description:'Enquiries, application forms, follow-ups, assessments, offers, waitlists and enrolment.'},
  {name:'Student information & lifecycle',description:'Family relationships, documents, enrolment history, grade progression and alumni records.'},
  {name:'Attendance & leave',description:'Class registers, leave requests, corrections, absence alerts and attendance trends.'},
 ]},
 {name:'Learning with a clear plan',icon:'book',features:[
  {name:'Academic foundations',description:'School year dates, grades, subjects, teaching days and holidays.',available:true},
  {name:'Curriculum & academic planning',description:'Terms, class groups, teacher allocations, board profiles and published calendars.'},
  {name:'Timetables & substitutions',description:'Class schedules, room and teacher conflict checks, cover assignments and timetable sharing.'},
  {name:'Teaching, homework & learning',description:'Lesson plans, assignments, submissions, feedback, learning resources and quizzes.'},
  {name:'Examinations & report cards',description:'Assessment rules, exam schedules, marks entry, moderation and published report cards.'},
 ]},
 {name:'The business of a school',icon:'coins',features:[
  {name:'Fees & concessions',description:'Fee plans, instalments, concessions, invoices, dues, receipts and refunds.'},
  {name:'Payments & reconciliation',description:'Online checkout, payment verification, settlements and payment dispute tracking.'},
  {name:'Accounts & financial controls',description:'Cash controls, expenses, budgets, bank reconciliation and accounting exports.'},
  {name:'Staff, leave & payroll',description:'Staff records, leave approvals, attendance, pay structures, payroll runs and payslips.'},
 ]},
 {name:'Life beyond the classroom',icon:'building',features:[
  {name:'Transport & pickup',description:'Fleet records, routes, trips, location updates, pickup changes and incident reporting.'},
  {name:'Library & circulation',description:'Book catalogues, loans, reservations, fines and stock reviews.'},
  {name:'Inventory, purchasing & assets',description:'Supplies, purchase orders, receiving, stock movements and asset audits.'},
  {name:'Health, wellbeing & safeguarding',description:'Medical profiles, clinic visits, care permissions and restricted incident records.'},
  {name:'Front office, events & helpdesk',description:'Visitor check-in, authorised pickup, events, facilities and support requests.'},
  {name:'Hostel, meals & enrichment',description:'Residential records, hostel attendance, dining services, clubs and activities.'},
 ]},
 {name:'A connected community',icon:'chat',features:[
  {name:'Communication & engagement',description:'Notices, notification preferences, conversations, meetings and feedback.'},
  {name:'Parent & student portals',description:'Personal school updates, learning, fees, requests and access linked to each family.'},
  {name:'Mobile app for your school',description:'A React Native / Expo app for parents, students, teachers and departments. UI prototype in progress.'},
  {name:'Analytics & reporting',description:'Operational dashboards, report libraries, drilldowns and scoped exports.'},
  {name:'Migration, integrations & automation',description:'Reviewed imports, data migration, APIs, connectors and automated school workflows.'},
 ]},
];
export function LandingFeatures(){
 const [filter,setFilter]=useState<'all'|'available'|'planned'>('all');
 const visible=groups.map(group=>({...group,features:group.features.filter(f=>filter==='all'||(filter==='available'?f.available:!f.available))})).filter(group=>group.features.length);
 const count=visible.reduce((sum,group)=>sum+group.features.length,0);
 return <section id="features" className="landing-section landing-features" aria-labelledby="features-title"><div className="landing-split-heading"><div><p className="landing-kicker"><span className="landing-dot"/> THE WHOLE SCHOOL, CONSIDERED</p><h2 id="features-title">From the first admission<br/>to the last bell.<br/><em>Room for everything.</em></h2></div><p>Start with the foundations available today.<br/>Explore the connected school we’re building next.</p></div><div className="landing-feature-toolbar"><div role="group" aria-label="Filter features by availability">{(['all','available','planned'] as const).map(value=><button type="button" key={value} aria-pressed={filter===value} onClick={()=>setFilter(value)}>{value==='all'?'The full picture':value==='available'?'Available now':'Planned'}</button>)}</div><span role="status" aria-live="polite">{count} features · {filter==='all'?'one connected vision':filter==='available'?'available now':'on the roadmap'}</span></div><div className="landing-feature-groups">{visible.map(group=><article className="landing-feature-group" key={group.name}><div className="landing-feature-group-heading"><Icon name={group.icon} size={22}/><h3>{group.name}</h3></div>{group.features.map(feature=><details key={feature.name}><summary><span>{feature.name}</span><small className={feature.available?'feature-status available':'feature-status'}>{feature.available?'Available':'Planned'}</small><Icon name="plus" size={13}/></summary><p>{feature.description}</p></details>)}</article>)}</div><p className="landing-feature-note">Available features cover the current school workspace. Planned modules are part of our roadmap; release dates will be shared as they’re ready. Department directories do not yet include their operational workflows.</p></section>
}
