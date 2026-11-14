'use client';
import {useState,type FormEvent} from 'react';
import {id,roles} from '@/lib/model';
import {departmentInfo} from '@/lib/workspace';
import {normalizeDepartmentName,suggestedDepartmentPrefix} from '@/lib/invitation-department';
import {prepareStaffMember} from '@/lib/staff-members';
import {useSetup} from './setup-context';
import {Field,Modal} from './ui';
import {Icon} from './icons';

export function WorkspaceAddStaff({department='',onCreated,onClose}:{department?:string;onCreated:(id:string)=>void;onClose:()=>void}){
 const {state,update,saving,storageError}=useSetup();
 const [draft,setDraft]=useState(()=>({id:id(),name:'',email:'',role:'Teacher',departmentId:department==='__unassigned__'?'':department})),[error,setError]=useState('');
 const departments=state.departments||[],blocked=!!saving||storageError,suggestions=Object.keys(departmentInfo).filter(name=>!departments.some(item=>normalizeDepartmentName(item.name)===normalizeDepartmentName(name)));
 function submit(event:FormEvent){event.preventDefault();if(blocked)return;try{const prepared=prepareStaffMember(state,draft);update(current=>prepareStaffMember(current,draft).state,'Staff member added: '+prepared.member.name+'.',false);onCreated(prepared.member.id);onClose()}catch(error){setError((error as Error).message)}}
 return <Modal title="Add a staff member" onClose={onClose}><form className="modal-body" onSubmit={submit}><Field label="Staff full name"><input required autoFocus minLength={2} maxLength={70} value={draft.name} disabled={blocked} autoComplete="name" placeholder="e.g. Priya Sharma" onChange={event=>{setDraft({...draft,name:event.target.value});setError('')}}/></Field><Field label="Staff email"><input required type="email" maxLength={254} value={draft.email} disabled={blocked} autoComplete="email" placeholder="name@school.com" onChange={event=>{setDraft({...draft,email:event.target.value});setError('')}}/></Field><Field label="Staff role"><select value={draft.role} disabled={blocked} onChange={event=>setDraft({...draft,role:event.target.value})}>{roles.map(role=><option key={role}>{role}</option>)}</select></Field><Field label="Staff department"><select value={draft.departmentId} disabled={blocked} onChange={event=>{setDraft({...draft,departmentId:event.target.value});setError('')}}><option value="">No department assigned</option>{departments.length>0&&<optgroup label="School departments">{departments.map(item=><option key={item.id} value={item.id}>{item.name}</option>)}</optgroup>}{suggestions.length>0&&<optgroup label="Suggested departments">{suggestions.map(name=><option key={name} value={suggestedDepartmentPrefix+name} disabled={departments.length>=100}>{name}</option>)}</optgroup>}</select></Field>{error&&<p role="alert" className="error">{error}</p>}<p className="staff-context">Adds a staff record to your school. No task, login or email is created.</p><div className="form-actions"><button type="button" className="button" onClick={onClose}>Cancel</button><button type="submit" className="button primary" disabled={blocked}>Add staff member<Icon name="addperson" size={16}/></button></div></form></Modal>;
}
