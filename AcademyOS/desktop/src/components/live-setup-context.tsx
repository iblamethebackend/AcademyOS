'use client';
import {useEffect,useRef,useState,type ReactNode} from 'react';
import {initialState,id,type State} from '@/lib/model';
import {loadCloudWorkspace,workspaceRequest} from '@/lib/supabase/workspace';
import {WorkspaceLoading} from './workspace-loading';
import {SetupContext,type SetupStore} from './setup-context';
export function LiveSetupProvider({children}:{children:ReactNode}){
 const [state,setState]=useState(initialState),[attempt,setAttempt]=useState(0),[ready,setReady]=useState(false),[error,setError]=useState(''),[toast,notify]=useState(''),[saving,setSaving]=useState(false);const revision=useRef(0),queue=useRef(Promise.resolve()),latest=useRef(state),failed=useRef(false);
 useEffect(()=>{let active=true;const controller=new AbortController();setError('');const timeout=setTimeout(()=>controller.abort(),20000);loadCloudWorkspace(controller.signal).then(w=>{if(active){revision.current=w.revision;latest.current=w.configuration;setState(w.configuration);setReady(true)}}).catch(e=>{if(active)setError(controller.signal.aborted?'The connection is taking too long. Please check your connection and try again.':e.message)}).finally(()=>clearTimeout(timeout));return()=>{active=false;clearTimeout(timeout);controller.abort()}},[attempt]);
 useEffect(()=>{if(toast){const timer=setTimeout(()=>notify(''),4000);return()=>clearTimeout(timer)}},[toast]);
 function update(change:(s:State)=>State,message:string,invalidate=true){if(failed.current){notify('Reload the workspace before making further changes.');return}const current=latest.current,next=change(current);const value={...next,checks:invalidate?[]:next.checks,activated:invalidate?false:next.activated,activity:[{id:id(),text:message},...current.activity].slice(0,20)};latest.current=value;setState(value);setSaving(true);queue.current=queue.current.then(async()=>{if(failed.current)return;try{const result=await workspaceRequest<{revision:number}>('PATCH',{state:value,revision:revision.current});revision.current=result.revision;notify(message)}catch(e){failed.current=true;setError((e as Error).message)}finally{if(latest.current===value||failed.current)setSaving(false)}})}
 const store:SetupStore={state,ready,storageError:!!error,toast,notify,update,reset:()=>notify('Cloud workspaces cannot be reset to demo data.'),cloud:true,saving};
 if(!ready)return <WorkspaceLoading key={attempt} error={error} noWorkspace={error==='No school workspace is linked to this account.'} onRetry={()=>setAttempt(value=>value+1)}/>;
 return <SetupContext.Provider value={store}>{error&&<div className="storage-banner" role="alert">{error} <button onClick={()=>location.reload()}>Reload school workspace</button></div>}{children}</SetupContext.Provider>
}
