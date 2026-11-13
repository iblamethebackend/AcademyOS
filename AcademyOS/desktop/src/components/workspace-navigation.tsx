'use client';
import Link from 'next/link';
import {useLayoutEffect,useRef,useState} from 'react';
import {workspacePages,workspaceHref} from '@/lib/workspace';
import {DashIcon as Icon} from './dashboard-icons';

export function WorkspaceNavigation({currentId,completed}:{currentId:string;completed:string[]}){
 const nav=useRef<HTMLElement>(null);
 const [position,setPosition]=useState<{x:number;y:number;width:number;height:number}|null>(null);
 const [animate,setAnimate]=useState(false);
 useLayoutEffect(()=>{
  const element=nav.current;if(!element)return;
  let active=true;
  function measure(){
   const link=element!.querySelector<HTMLElement>('[aria-current="page"]');if(!link)return;
   const bounds=link.getBoundingClientRect(),parent=element!.getBoundingClientRect();
   const next={x:bounds.left-parent.left+element!.scrollLeft,y:bounds.top-parent.top+element!.scrollTop,width:bounds.width,height:bounds.height};
   setPosition(previous=>previous&&Object.keys(next).every(key=>Math.abs(previous[key as keyof typeof next]-next[key as keyof typeof next])<.5)?previous:next);
  }
  measure();
  const frame=requestAnimationFrame(()=>setAnimate(true));
  const observer=new ResizeObserver(measure);observer.observe(element);element.querySelectorAll('a').forEach(link=>observer.observe(link));
  void document.fonts.ready.then(()=>{if(active)measure()});
  const selected=element.querySelector<HTMLElement>('[aria-current="page"]');
  if(selected){const left=selected.offsetLeft,right=left+selected.offsetWidth;if(left<element.scrollLeft||right>element.scrollLeft+element.clientWidth)element.scrollTo({left:Math.max(0,left-(element.clientWidth-selected.offsetWidth)/2),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'})}
  return()=>{active=false;observer.disconnect();cancelAnimationFrame(frame)};
 },[currentId,completed]);
 return <div className="ws-section-bar"><nav ref={nav} aria-label="School workspace sections" className="ws-sliding-nav"><span aria-hidden="true" className={'ws-tab-indicator'+(animate?' is-ready':'')} style={{width:position?.width||0,height:position?.height||0,transform:`translate3d(${position?.x||0}px,${position?.y||0}px,0)`,opacity:position?1:0}}/>{workspacePages.map(page=><Link key={page.id} href={workspaceHref(page.id)} aria-label={page.label} className={currentId===page.id?'active':''} aria-current={currentId===page.id?'page':undefined}><Icon name={page.icon} size={17}/><span>{page.label}</span>{completed.includes(page.id)&&<Icon name="check" size={12}/>}</Link>)}</nav></div>;
}
