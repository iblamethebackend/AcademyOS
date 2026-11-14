import {maxSubmissionBytes,validTaskDate,type TaskAttachment} from './staff-tasks';

export type SchoolAchievement={id:string;kind:'Achievement'|'Certificate';title:string;issuedBy:string;awardedOn:string;description:string;createdAt:string;updatedAt:string;certificate?:TaskAttachment};
export function validCertificateFile(file:{name:string;size:number}){
 return typeof file.name==='string'&&file.name.length<=180&&Number.isInteger(file.size)&&file.size>0&&file.size<=maxSubmissionBytes&&['pdf','png','jpg','jpeg'].includes(file.name.split('.').pop()?.toLowerCase()||'');
}
const text=(value:unknown,max:number,min=0):value is string=>typeof value==='string'&&value.trim().length>=min&&value.length<=max;
const timestamp=(value:unknown)=>typeof value==='string'&&Number.isFinite(Date.parse(value));
export function validAchievementConfiguration(value:unknown):boolean{
 if(!value||typeof value!=='object')return false;
 const records=(value as {achievements?:unknown}).achievements;
 if(records===undefined)return true;
 if(!Array.isArray(records)||records.length>200)return false;
 const ids=new Set<string>();
 return records.every((record:SchoolAchievement)=>{
  if(!record||!text(record.id,64,1)||ids.has(record.id)||!['Achievement','Certificate'].includes(record.kind)||!text(record.title,120,3)||!text(record.issuedBy,120)||!text(record.description,2000)||(record.awardedOn!==''&&!validTaskDate(record.awardedOn))||!timestamp(record.createdAt)||!timestamp(record.updatedAt))return false;
  ids.add(record.id);
  const file=record.certificate;
  if(record.kind==='Certificate'&&!file)return false;
  return !file||(text(file.id,64,1)&&validCertificateFile(file)&&text(file.type,150)&&text(file.path,300,1)&&['local','cloud'].includes(file.storage));
 });
}
