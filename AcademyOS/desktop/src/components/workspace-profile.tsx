import Link from 'next/link';
import {DemoSignOut} from './demo-session-gate';
import {DashIcon as Icon} from './dashboard-icons';
import './workspace-profile.css';

export function WorkspaceProfile({name,email,school,onClose}:{name:string;email?:string;school:string;onClose:()=>void}){
 const initials=name.split(/\s+/).filter(Boolean).map(word=>word[0]).slice(0,2).join('');
 return <div className="workspace-profile-body">
  <div className="workspace-profile-identity"><span className="workspace-profile-avatar" aria-hidden="true">{initials}</span><div><h3>{name}</h3><span className="workspace-profile-role"><Icon name="shield" size={12}/>School owner</span></div></div>
  <dl className="workspace-profile-details"><div><span className="workspace-profile-detail-icon" aria-hidden="true"><Icon name="mail" size={17}/></span><div><dt>Email address</dt><dd>{email||'Email not available'}</dd></div></div><div><span className="workspace-profile-detail-icon" aria-hidden="true"><Icon name="school" size={18}/></span><div><dt>School workspace</dt><dd>{school}</dd></div></div></dl>
  <div className="workspace-profile-actions"><Link href="/workspace/school" className="workspace-profile-manage" onClick={onClose}><span><Icon name="school" size={16}/>Manage school profile</span><Icon name="arrow" size={16}/></Link><DemoSignOut className="workspace-profile-signout"/></div>
 </div>;
}
