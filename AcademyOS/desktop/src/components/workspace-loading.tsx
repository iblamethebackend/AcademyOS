'use client';
import Link from 'next/link';
import {useEffect,useState} from 'react';
import {Brand} from './brand';
import './workspace-loading.css';

export function WorkspaceLoading({error,onRetry,noWorkspace=false}:{error?:string;onRetry?:()=>void;noWorkspace?:boolean}){
 const [slow,setSlow]=useState(false);
 useEffect(()=>{const timer=setTimeout(()=>setSlow(true),8000);return()=>clearTimeout(timer)},[]);
 return <div className="workspace-loading-screen">
  <header className="workspace-loading-header"><Brand href="/"/><span>YOUR SCHOOL WORKSPACE</span></header>
  <main className="workspace-loading-main">
   <section className={'workspace-loading-card'+(error?' has-error':'')} aria-labelledby="workspace-loading-title" aria-busy={!error}>
    <div className="workspace-loading-emblem" aria-hidden="true"><svg viewBox="0 0 68 54" fill="none"><path d="M6 5c11 0 20 3 28 11C42 8 51 5 62 5v35c-11 0-20 3-28 10C26 43 17 40 6 40V5Z" stroke="currentColor" strokeWidth="3.5" strokeLinejoin="round"/><path d="M34 18v31" stroke="currentColor" strokeWidth="3.5" strokeLinecap="round"/></svg>{!error&&<span/>}</div>
    <p className="workspace-loading-kicker">{error?'LET’S GET YOU CONNECTED':'A SMARTER CAMPUS. A CALMER DAY.'}</p>
    <h1 id="workspace-loading-title">{error?'Your workspace is waiting.':'A little moment for your school.'}</h1>
    <div role={error?'alert':'status'} aria-live="polite" className="workspace-loading-status"><p>{error||'Loading your school workspace…'}</p>{!error&&<small>{slow?'This is taking a little longer. We’re still waiting for your school data.':'Connecting to your school and bringing everything together.'}</small>}</div>
    {!error&&<><div className="workspace-loading-track" role="progressbar" aria-label="Loading school workspace"><span/></div><div className="workspace-loading-preview" aria-hidden="true"><div className="loading-preview-heading"><i/><b/></div><div className="loading-preview-tiles"><i/><i/><i/></div><div className="loading-preview-lines"><i/><i/></div></div></>}
    {(error||slow)&&<div className="workspace-loading-actions">{onRetry&&<button onClick={onRetry}>{error?'Try again':'Retry connection'}<span aria-hidden="true">↻</span></button>}{noWorkspace?<Link href="/register-school">Set up your school</Link>:<Link href="/login">Back to sign in</Link>}</div>}
   </section>
  </main>
  <footer className="workspace-loading-footer"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true"><path d="m12 3 8 3v6c0 4-4 7-8 9-4-2-8-5-8-9V6l8-3Z"/><path d="m8 12 3 3 5-6"/></svg>Your school. Your people. One connected space.</footer>
 </div>
}
