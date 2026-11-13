import {DemoSessionGate} from '@/components/demo-session-gate';
import {SetupProvider} from '@/components/setup-context';
import {WorkspaceShell} from '@/components/workspace-shell';
import './workspace.css';
export const metadata={title:'School workspace · AcademyOS',description:'Your school community, setup and everyday essentials in one place.'};
export default function Layout({children}:{children:React.ReactNode}){return <DemoSessionGate><SetupProvider><WorkspaceShell>{children}</WorkspaceShell></SetupProvider></DemoSessionGate>}
