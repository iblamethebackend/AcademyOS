'use client';
import {useEffect} from 'react';
import {usePathname} from 'next/navigation';
import Lenis from 'lenis';

const enterSelector='.login-card,[role="tabpanel"],[data-motion-panel]';
function enter(element:Element){
 if(!(element instanceof HTMLElement)||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 element.getAnimations().filter(a=>a.id==='app-enter').forEach(a=>a.cancel());
 const animation=element.animate([{opacity:0,translate:'0 8px'},{opacity:1,translate:'0 0'}],{duration:280,easing:'cubic-bezier(.22,1,.36,1)'});animation.id='app-enter';
}
export function AppMotion(){
 const path=usePathname();
 useEffect(()=>{window.dispatchEvent(new Event('academyos:route-change'));document.querySelectorAll(enterSelector).forEach(enter)},[path]);
 useEffect(()=>{
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let root:Lenis|undefined;
  const nested=new Map<HTMLElement,Lenis>();
  function sync(){
   if(reduced.matches){root?.destroy();root=undefined;for(const instance of nested.values())instance.destroy();nested.clear();return}
   root??=new Lenis({autoRaf:true,lerp:.12,smoothWheel:true,syncTouch:false,anchors:true,allowNestedScroll:true,prevent:node=>!!node.closest('dialog,[data-smooth-scroll],textarea,[data-lenis-prevent]')});
   for(const [element,instance] of nested){if(!element.isConnected){instance.destroy();nested.delete(element)}}
   document.querySelectorAll<HTMLElement>('[data-smooth-scroll]').forEach(element=>{
    const content=element.firstElementChild;
    if(nested.has(element)||!(content instanceof HTMLElement))return;
    nested.set(element,new Lenis({wrapper:element,content,autoRaf:true,lerp:.12,smoothWheel:true,syncTouch:false,allowNestedScroll:true,prevent:node=>!!node.closest('dialog,textarea,[data-lenis-prevent]')}));
   });
  }
  sync();
  function navigate(){root?.scrollTo(window.scrollY,{immediate:true});for(const instance of nested.values())instance.scrollTo(0,{immediate:true})}
  window.addEventListener('academyos:route-change',navigate);
  const observer=new MutationObserver(records=>{
   let changed=false;
   for(const record of records){
    if(record.type==='childList'){
     changed=true;
     for(const node of record.addedNodes){if(!(node instanceof HTMLElement))continue;if(node.matches(enterSelector))enter(node);node.querySelectorAll(enterSelector).forEach(enter)}
    }else if(record.attributeName==='hidden'&&record.target instanceof HTMLElement&&record.target.matches('[role="tabpanel"]')&&!record.target.hidden){enter(record.target)
    }else if(record.target instanceof HTMLElement&&record.target.matches('.register-content,.signup-content')){
     if(record.oldValue!==record.target.className)enter(record.target);
    }
   }
   if(changed)sync();
  });
  observer.observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['class','hidden'],attributeOldValue:true});
  reduced.addEventListener('change',sync);
  return()=>{observer.disconnect();window.removeEventListener('academyos:route-change',navigate);reduced.removeEventListener('change',sync);root?.destroy();for(const instance of nested.values())instance.destroy()};
 },[]);
 return null;
}
