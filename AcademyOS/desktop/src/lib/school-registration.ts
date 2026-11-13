import {initialState,type State,slugValid,id} from './model';
export const REGISTERED_SCHOOLS_KEY='academyos.registered-schools.v1';
export const SETUP_KEY='academyos.desktop.setup.v1';
export type RegisteredSchool=Registration & {createdAt:number};
export type Registration={ownerName:string;email:string;name:string;slug:string;board:string;city:string;phone:string};
export function registeredSchools():RegisteredSchool[]{try{const value=JSON.parse(localStorage.getItem(REGISTERED_SCHOOLS_KEY)||'[]');return Array.isArray(value)?value.filter(s=>s&&slugValid(s.slug||'')&&typeof s.email==='string'&&typeof s.ownerName==='string'&&typeof s.createdAt==='number'&&['name','board','city','phone'].every(k=>typeof s[k]==='string')):[]}catch{return []}}
export function findRegisteredSchool(slug:string,email:string){return registeredSchools().find(s=>s.slug===slug.toLowerCase()&&s.email===email.toLowerCase())}
export function schoolSlugTaken(slug:string){return ['greenfield','admin','login','signup','register','api','www','setup','dashboard'].includes(slug)||registeredSchools().some(s=>s.slug===slug)}
export function registeredSetupKey(slug:string){return SETUP_KEY+':'+slug}
export function makeRegisteredState(data:Registration){
 const state:State=structuredClone(initialState);
 state.school={...state.school,name:data.name,legalName:data.name,slug:data.slug,email:data.email.toLowerCase(),phone:data.phone,address:'',board:data.board};
 state.departments=[];state.campuses=[{id:id(),name:'Main campus',city:data.city,code:'MAIN'}];state.members=[{id:id(),name:data.ownerName,email:data.email.toLowerCase(),role:'School leader',status:'Active'}];state.students=[];state.completed=[];state.checks=[];state.activated=false;state.domain='';state.domainVerified=false;state.pause=false;state.deletionScheduled=false;state.retentionHold=false;state.academic={...state.academic,holidays:[]};state.brand={...state.brand,color:'#2e5d4e',initials:data.name.split(/\s+/).map(w=>w[0]).join('').slice(0,3).toUpperCase()};state.activity=[{id:id(),text:data.ownerName+' created the '+data.name+' preview workspace.'}];
 return state;
}
export function createSchoolPreview(data:Registration){
 if(!slugValid(data.slug)||schoolSlugTaken(data.slug))throw new Error('This workspace address is already used in this browser. Choose another address.');
 const school:RegisteredSchool={...data,email:data.email.toLowerCase(),createdAt:Date.now()};const state=makeRegisteredState(data);
 const key=registeredSetupKey(data.slug);if(localStorage.getItem(key))throw new Error('This workspace already has saved data. Choose another address.');
 try{localStorage.setItem(key,JSON.stringify(state));localStorage.setItem(REGISTERED_SCHOOLS_KEY,JSON.stringify([...registeredSchools(),school]))}catch{try{localStorage.removeItem(key)}catch{}throw new Error('Your browser could not save this workspace. Enable browser storage and try again. Existing school data was not changed.')}
 return school;
}
