import {notFound} from 'next/navigation';
import {workspacePages} from '@/lib/workspace';
import {WorkspacePage} from '@/components/workspace-page';
export default async function Page({params}:{params:Promise<{section?:string[]}>}){const {section}=await params;const key=section?.[0]||'overview';if((section?.length||0)>1||!workspacePages.some(s=>s.id===key))notFound();return <WorkspacePage section={key}/>}
