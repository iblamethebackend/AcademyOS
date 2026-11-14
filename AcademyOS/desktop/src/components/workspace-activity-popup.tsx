'use client';
import {useEffect,useLayoutEffect,useRef,useState,type RefObject} from 'react';
import {createPortal} from 'react-dom';
import {DashIcon as Icon} from './dashboard-icons';
import './workspace-activity-popup.css';

export function WorkspaceActivityPopup({activity,anchor,onClose}:{activity:{id:string;text:string}[];anchor:RefObject<HTMLButtonElement|null>;onClose:()=>void}){
 const popup=useRef<HTMLDivElement>(null),closeButton=useRef<HTMLButtonElement>(null);
 const [position,setPosition]=useState<{left:number;top:number;width:number;maxHeight:number}|null>(null);
 useLayoutEffect(()=>{
  function place(){const rect=anchor.current?.getBoundingClientRect();if(!rect)return;const width=Math.min(380,innerWidth-24),top=Math.min(rect.bottom+12,Math.max(12,innerHeight-100));setPosition({width,left:Math.max(12,Math.min(rect.right-width,innerWidth-width-12)),top,maxHeight:Math.min(440,innerHeight-top-12)})}
  place();window.addEventListener('resize',place);window.addEventListener('scroll',place,{capture:true,passive:true});
  return()=>{window.removeEventListener('resize',place);window.removeEventListener('scroll',place,true)};
 },[anchor]);
 useEffect(()=>{if(position)closeButton.current?.focus({preventScroll:true})},[!!position]);
 useEffect(()=>{
  function outside(event:PointerEvent){const target=event.target as Node;if(!popup.current?.contains(target)&&!anchor.current?.contains(target))onClose()}
  function escape(event:KeyboardEvent){if(event.key==='Escape'){event.preventDefault();onClose();anchor.current?.focus({preventScroll:true})}}
  document.addEventListener('pointerdown',outside,true);document.addEventListener('keydown',escape);
  return()=>{document.removeEventListener('pointerdown',outside,true);document.removeEventListener('keydown',escape)};
 },[anchor,onClose]);
 if(!position)return null;
 return createPortal(<div ref={popup} id="workspace-activity-popup" role="dialog" aria-modal="false" aria-labelledby="workspace-activity-title" className="ws-activity-popup" style={position}><div className="ws-activity-popup-head"><div><h2 id="workspace-activity-title">Notifications</h2><p>Your latest school workspace updates</p></div><button ref={closeButton} type="button" aria-label="Close notifications" onClick={()=>{onClose();anchor.current?.focus({preventScroll:true})}}><Icon name="close" size={17}/></button></div><div className="ws-activity-popup-scroll" data-lenis-prevent>{activity.length?<ul>{activity.map((item,index)=><li key={item.id}><span className="ws-notification-dot" aria-hidden="true"/><div><p>{item.text}</p><small>{index===0?'Latest workspace update':'School activity'}</small></div></li>)}</ul>:<p className="ws-notifications-empty">No school activity yet.</p>}</div></div>,document.body);
}
