'use client';
import {useState,type FormEvent} from 'react';
import {id} from '@/lib/model';
import {useSetup} from './setup-context';
import {Modal} from './ui';
import {DashIcon as Icon} from './dashboard-icons';
import './workspace-invite.css';
export function WorkspaceInvite({role='Teacher',departmentId='',onClose}:{role?:string;departmentId?:string;onClose:()=>void}){const {state,update}=useSetup();const [draft,setDraft]=useState({name:'',email:'',role,departmentId}),[error,setError]=useState('');function submit(e:FormEvent){e.preventDefault();if(!draft.name.trim()){setError('Enter your teammate’s name.');return}if(state.members.some(m=>m.email.toLowerCase()===draft.email.trim().toLowerCase())){setError('This email is already in the school roster. Review its existing invitation in People & invitations.');return}update(s=>({...s,members:[...s.members,{...draft,departmentId:draft.departmentId||undefined,id:id(),name:draft.name.trim(),email:draft.email.trim().toLowerCase(),status:'Invited'}]}),'Invitation prepared for '+draft.name.trim()+'. No email sent.');onClose()}
 return <Modal title="Invite a teammate" eyebrow="GROW YOUR SCHOOL TEAM" className="workspace-invite-modal" onClose={onClose}>
  <form className="invite-form" onSubmit={submit}>
   <div className="invite-introduction"><span className="invite-introduction-icon"><Icon name="addperson" size={22}/></span><div><p>A new face at <strong>{state.school.name}</strong>.</p><small>Add their details and choose a department.</small></div></div>
   <label className="invite-field"><span>Full name</span><div className="invite-control"><Icon name="people" size={17}/><input aria-label="Teammate name" autoFocus autoComplete="name" required maxLength={70} placeholder="e.g. Priya Sharma" value={draft.name} onChange={e=>{setDraft({...draft,name:e.target.value});setError('')}}/></div></label>
   <label className="invite-field"><span>Work email</span><div className="invite-control"><Icon name="mail" size={17}/><input aria-label="Teammate email" required type="email" autoComplete="email" maxLength={254} placeholder="name@school.com" value={draft.email} onChange={e=>{setDraft({...draft,email:e.target.value});setError('')}}/></div></label>
   <label className="invite-field"><span>Department</span><div className="invite-control"><Icon name="grid" size={17}/><select aria-label="Assigned department" value={draft.departmentId} onChange={e=>setDraft({...draft,departmentId:e.target.value})}><option value="">No department assigned</option>{(state.departments||[]).map(department=><option key={department.id} value={department.id}>{department.name}</option>)}</select><span className="invite-select-arrow" aria-hidden="true"><Icon name="down" size={13}/></span></div></label>
   {error&&<p className="invite-error" role="alert"><Icon name="warning" size={17}/>{error}</p>}
   <div className="invite-preview-note"><Icon name="mail" size={18}/><div><strong>Invitation preview</strong><p>This adds a preview to your school roster. No email or access link will be sent.</p></div></div>
   <div className="invite-actions"><button type="button" className="invite-cancel" onClick={onClose}>Cancel</button><button className="invite-submit" type="submit">Prepare invitation<Icon name="arrow" size={16}/></button></div>
  </form>
 </Modal>
}
