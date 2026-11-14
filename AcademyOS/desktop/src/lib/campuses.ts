import type {Campus,Member,State} from './model';

export type CampusInChargeDraft={id:string;name:string;email:string};

export function validCampusPhoto(file:{name:string;size:number}){
 return typeof file.name==='string'&&file.name.length<=180&&Number.isInteger(file.size)&&file.size>0&&file.size<=5*1024*1024&&['png','jpg','jpeg'].includes(file.name.split('.').pop()?.toLowerCase()||'');
}
const text=(value:unknown,max:number,min=0):value is string=>typeof value==='string'&&value.length<=max&&value.trim().length>=min;
function validIds(value:unknown,allowed:Set<string>){return value===undefined||(Array.isArray(value)&&value.length<=2000&&new Set(value).size===value.length&&value.every(key=>typeof key==='string'&&allowed.has(key)))}
export function validCampusConfiguration(value:unknown):boolean{
 if(!value||typeof value!=='object')return false;
 const state=value as State;
 if(!Array.isArray(state.campuses)||!state.campuses.length||state.campuses.length>2000||!Array.isArray(state.members)||!Array.isArray(state.students))return false;
 const staff=new Set(state.members.map(person=>person?.id)),students=new Set(state.students.map(person=>person?.id)),ids=new Set<string>(),codes=new Set<string>();
 return state.campuses.every(campus=>{
  if(!campus||!text(campus.id,64,1)||ids.has(campus.id)||!text(campus.name,60,1)||!text(campus.city,60,1)||!text(campus.code,12,2)||!/^[A-Za-z0-9-]{2,12}$/.test(campus.code)||codes.has(campus.code.toLowerCase()))return false;
  ids.add(campus.id);codes.add(campus.code.toLowerCase());
  if(campus.address!==undefined&&!text(campus.address,500))return false;
  if(!validIds(campus.staffIds,staff)||!validIds(campus.studentIds,students))return false;
  if(campus.inChargeId!==undefined&&campus.inChargeId!==''&&(!text(campus.inChargeId,64,1)||!staff.has(campus.inChargeId)||!campus.staffIds?.includes(campus.inChargeId)))return false;
  const photo=campus.photo;
  return !photo||(text(photo.id,64,1)&&validCampusPhoto(photo)&&text(photo.type,150)&&text(photo.path,300,1)&&['local','cloud'].includes(photo.storage));
 });
}
export function saveCampus(state:State,campus:Campus):State{
 const saved={...campus,name:campus.name.trim(),city:campus.city.trim(),code:campus.code.trim().toUpperCase(),address:(campus.address||'').trim(),staffIds:Array.from(new Set([...(campus.staffIds||[]),...(campus.inChargeId?[campus.inChargeId]:[])])),studentIds:Array.from(new Set(campus.studentIds||[]))};
 if(saved.address.length<5)throw new Error('Enter the full campus address (at least 5 characters).');
 if(state.campuses.some(item=>item.id!==saved.id&&item.code.toLowerCase()===saved.code.toLowerCase()))throw new Error('This campus code is already used. Choose a unique code.');
 const next={...state,campuses:state.campuses.some(item=>item.id===saved.id)?state.campuses.map(item=>item.id===saved.id?saved:item):[...state.campuses,saved]};
 if(!validCampusConfiguration(next))throw new Error('Check the campus details, photo and selected staff or students.');
 return next;
}
export function removeCampus(state:State,campusId:string):State{
 if(state.campuses[0]?.id===campusId)throw new Error('The primary campus cannot be removed.');
 return {...state,campuses:state.campuses.filter(campus=>campus.id!==campusId)};
}
export function saveCampusWithInCharge(state:State,campus:Campus,person?:CampusInChargeDraft):State{
 if(!person)return saveCampus(state,campus);
 const name=person.name.trim(),email=person.email.trim().toLowerCase();
 if(name.length<2||name.length>70)throw new Error('Enter the new in-charge\'s full name (2-70 characters).');
 if(email.length>254||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))throw new Error('Enter a valid email for the new campus in-charge.');
 if(state.members.some(member=>member.email.toLowerCase()===email))throw new Error('This email already belongs to your school team. Select that person from the existing staff list.');
 if(!person.id||state.members.some(member=>member.id===person.id))throw new Error('This staff record already exists. Choose an existing staff member.');
 const member:Member={id:person.id,name,email,role:'Campus in-charge',status:'Active'};
 return saveCampus({...state,members:[...state.members,member]},{...campus,inChargeId:member.id});
}
