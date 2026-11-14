import {roles,type Member,type State} from './model';
import {invitationDepartment} from './invitation-department';

export type StaffMemberDraft={id:string;name:string;email:string;role:string;departmentId:string};
export function prepareStaffMember(state:State,draft:StaffMemberDraft):{state:State;member:Member}{
 const name=draft.name.trim(),email=draft.email.trim().toLowerCase();
 if(name.length<2||name.length>70)throw new Error('Enter the new staff member\'s full name (2-70 characters).');
 if(email.length>254||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))throw new Error('Enter a valid staff email address.');
 if(!roles.includes(draft.role))throw new Error('Choose a staff role from the list.');
 if(state.members.some(member=>member.email.toLowerCase()===email))throw new Error('This email is already in your school team. Choose the existing active staff member or review their record in People & invitations.');
 if(!draft.id||draft.id.length>64||state.members.some(member=>member.id===draft.id))throw new Error('This staff record already exists.');
 const assignment=invitationDepartment(state.departments||[],draft.departmentId);
 const member:Member={id:draft.id,name,email,role:draft.role,status:'Active',departmentId:assignment.departmentId};
 return {state:{...state,members:[...state.members,member],departments:assignment.departments},member};
}
