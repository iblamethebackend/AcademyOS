import type {State} from './model';
import {prepareStaffMember,type StaffMemberDraft} from './staff-members';
import {normalizeDepartmentName,suggestedDepartmentPrefix} from './invitation-department';

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
export function taskDepartment(state:State,task:StaffTask){
 const member=state.members.find(person=>person.id===task.memberId);
 return state.departments?.find(department=>department.id===member?.departmentId);
}
export function matchesTaskDepartment(state:State,task:StaffTask,selection:string){
 if(!selection)return true;
 const department=taskDepartment(state,task);
 if(selection==='__unassigned__')return !department;
 if(!department)return false;
 return selection.startsWith(suggestedDepartmentPrefix)?normalizeDepartmentName(department.name)===normalizeDepartmentName(selection.slice(suggestedDepartmentPrefix.length)):department.id===selection;
}
export type NewTaskStaff=StaffMemberDraft;
export type TaskAssignment={id:string;memberId:string;title:string;description:string;dueDate:string;createdAt:string};
export function assignStaffTask(state:State,input:TaskAssignment,newStaff?:NewTaskStaff):State{
 if(schoolTasks(state).length>=500)throw new Error('This workspace has reached its 500 task limit.');
 if(input.title.trim().length<3||input.title.length>120||input.description.length>1000||!validTaskDate(input.dueDate))throw new Error('Enter a task title, instructions and a valid due date.');
 if(schoolTasks(state).some(task=>task.id===input.id))throw new Error('This task already exists.');
 let members=state.members,departments=state.departments;
 let person=members.find(member=>member.id===input.memberId&&member.status==='Active');
 if(newStaff){const prepared=prepareStaffMember(state,newStaff);members=prepared.state.members;departments=prepared.state.departments;person=prepared.member;}
 if(!person)throw new Error('Select an active staff member or add a new one.');
 const task:StaffTask={id:input.id,memberId:person.id,memberName:person.name,title:input.title.trim(),description:input.description.trim(),dueDate:input.dueDate,createdAt:input.createdAt,status:'Assigned',submissions:[]};
 const next={...state,members,...(departments?{departments}:{}),staffTasks:[task,...schoolTasks(state)]};
 if(!validStaffTaskConfiguration(next))throw new Error('Check the task details before saving.');
 return next;
}
