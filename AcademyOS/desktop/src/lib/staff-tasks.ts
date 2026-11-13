import type {State} from './model';

export type TaskAttachment={id:string;name:string;size:number;type:string;path:string;storage:'local'|'cloud'};
export type StaffSubmission={id:string;submittedAt:string;note:string;recordedBy:'School owner';attachment?:TaskAttachment};
export type StaffTask={id:string;memberId:string;memberName:string;title:string;description:string;dueDate:string;createdAt:string;status:'Assigned'|'Submitted'|'Completed';completedAt?:string;submissions:StaffSubmission[]};
export const maxSubmissionBytes=10*1024*1024;
export const submissionExtensions=['pdf','csv','txt','docx','xlsx','png','jpg','jpeg'];
export function validSubmissionFile(file:{name:string;size:number}){
 return file.size>0&&file.size<=maxSubmissionBytes&&file.name.length<=180&&submissionExtensions.includes(file.name.split('.').pop()?.toLowerCase()||'');
}
export function schoolDate(timezone:string,now=new Date()){
 return new Intl.DateTimeFormat('en-CA',{timeZone:timezone||'UTC',year:'numeric',month:'2-digit',day:'2-digit'}).format(now);
}
export function taskOverdue(task:StaffTask,today:string){return task.status!=='Completed'&&task.dueDate<today}
export function staffActivity(tasks:StaffTask[],memberId:string,now=Date.now()){
 const assigned=tasks.filter(task=>task.memberId===memberId);
 const submissions=assigned.flatMap(task=>task.submissions).sort((a,b)=>b.submittedAt.localeCompare(a.submittedAt));
 return {assigned:assigned.length,completed:assigned.filter(task=>task.status==='Completed').length,submissions:submissions.length,uploads:submissions.filter(s=>s.attachment).length,lastSubmitted:submissions[0]?.submittedAt,active:submissions.some(s=>Date.parse(s.submittedAt)>=now-7*86400000&&Date.parse(s.submittedAt)<=now)};
}
const text=(v:unknown,max:number,min=0):v is string=>typeof v==='string'&&v.trim().length>=min&&v.length<=max;
const timestamp=(v:unknown):v is string=>typeof v==='string'&&Number.isFinite(Date.parse(v));
export function validTaskDate(value:unknown):value is string{return typeof value==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(value)&&!Number.isNaN(Date.parse(value))&&new Date(value).toISOString().slice(0,10)===value}
export function validStaffTaskConfiguration(value:unknown):boolean{
 if(!value||typeof value!=='object')return false;
 const tasks=(value as {staffTasks?:unknown}).staffTasks;
 if(tasks===undefined)return true;
 if(!Array.isArray(tasks)||tasks.length>500)return false;
 const ids=new Set<string>();
 return tasks.every((task:StaffTask)=>{
  if(!task||!text(task.id,64,1)||ids.has(task.id)||!text(task.memberId,64,1)||!text(task.memberName,100,1)||!text(task.title,120,3)||!text(task.description,1000)||!validTaskDate(task.dueDate)||!timestamp(task.createdAt)||!['Assigned','Submitted','Completed'].includes(task.status)||!Array.isArray(task.submissions)||task.submissions.length>50)return false;
  ids.add(task.id);
  if(task.status!=='Assigned'&&!task.submissions.length)return false;
  if(task.status==='Completed'&&!timestamp(task.completedAt))return false;
  return task.submissions.every(s=>{
   if(!s||!text(s.id,64,1)||!timestamp(s.submittedAt)||!text(s.note,2000)||s.recordedBy!=='School owner'||(!s.note.trim()&&!s.attachment))return false;
   const a=s.attachment;
   return !a||(text(a.id,64,1)&&text(a.name,180,1)&&Number.isInteger(a.size)&&validSubmissionFile(a)&&text(a.type,150)&&text(a.path,300,1)&&['local','cloud'].includes(a.storage));
  });
 });
}
export function schoolTasks(state:State){return state.staffTasks||[]}
