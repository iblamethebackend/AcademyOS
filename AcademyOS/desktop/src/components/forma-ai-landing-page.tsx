'use client';
import {useEffect,useRef} from 'react';
import {useRouter} from 'next/navigation';
/** Local adaptation of ThreeUI's authored document wrapper. Source hashes are in vendor/threeui-forma. */
export function FormaAiLandingPage(){
 const frame=useRef<HTMLIFrameElement>(null),router=useRouter();
 useEffect(()=>{function navigate(event:MessageEvent){if(event.source!==frame.current?.contentWindow||event.data?.type!=='academyos:navigate')return;const path=event.data.path;if(path==='/login'||path==='/register-school')router.push(path)}window.addEventListener('message',navigate);return()=>window.removeEventListener('message',navigate)},[router]);
 return <iframe ref={frame} src="/landing-pages/forma-ai.html" title="AcademyOS — a smarter campus" sandbox="allow-scripts allow-forms" style={{display:'block',width:'100%',height:'100dvh',border:0,background:'#f7f9f6'}}/>;
}
