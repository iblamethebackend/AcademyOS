import {notFound} from 'next/navigation';
import {redirect} from 'next/navigation';
import {sections} from '@/lib/model';
export default async function Page({params}:{params:Promise<{section?:string[]}>}){
 const {section}=await params;const key=section?.[0]||'overview';
 if((section?.length||0)>1||!sections.some(s=>s.id===key))notFound();
 redirect('/workspace'+(key==='overview'?'':'/'+(key==='lifecycle'?'settings':key)));
}
