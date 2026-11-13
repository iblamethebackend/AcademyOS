'use client';
import {useEffect,useState,type ReactNode} from 'react';
import {useRouter,usePathname} from 'next/navigation';
import {liveSupabase} from '@/lib/supabase/config';
import {browserSupabase} from '@/lib/supabase/browser';
import {WorkspaceLoading} from './workspace-loading';
import {getDemoSession,clearDemoSession,SESSION_KEY} from '@/lib/demo-auth';
export function DemoSessionGate({children}:{children:ReactNode}){
 const router=useRouter(),path=usePathname();const [allowed,setAllowed]=useState(false);
 useEffect(()=>{if(liveSupabase)return;function check(){if(getDemoSession()){setAllowed(true)}else{setAllowed(false);router.replace('/login?next='+encodeURIComponent(path))}}function sync(e:StorageEvent){if(e.key===SESSION_KEY&&!e.newValue)clearDemoSession();check()}check();window.addEventListener('focus',check);window.addEventListener('storage',sync);const timer=setInterval(check,60000);return()=>{window.removeEventListener('focus',check);window.removeEventListener('storage',sync);clearInterval(timer)}},[path,router]);
 return (liveSupabase||allowed)?children:<WorkspaceLoading/>;
}
export function DemoSignOut({className='button'}:{className?:string}){const router=useRouter();return <button className={className} onClick={async()=>{if(liveSupabase){const {error}=await browserSupabase().auth.signOut();if(error)return}clearDemoSession();router.replace('/login');router.refresh()}}>{liveSupabase?'Sign out':'Sign out of demo'} <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true"><path d="M9 3H3v18h6m1-9h12m-5-5 5 5-5 5"/></svg></button>}
