'use client';
import {useEffect,useRef,type CSSProperties} from 'react';

/** Scroll scrubs the sculpture in both directions, without rerendering its plates. */
export function GlassRibbon(){
 const ribbon=useRef<HTMLDivElement>(null);
 useEffect(()=>{
  const element=ribbon.current,hero=element?.closest('section');
  if(!element||!hero)return;
  const motion=window.matchMedia('(prefers-reduced-motion: reduce)');
  let frame=0,current=0,target=0,top=0,height=1;
  function paint(){
   if(!element)return;
   element.style.setProperty('--ribbon-turn',`${(current*210).toFixed(3)}deg`);
   element.style.setProperty('--ribbon-roll',`${(-current*18).toFixed(3)}deg`);
   element.style.setProperty('--ribbon-x',`${(-current*8).toFixed(3)}%`);
   element.style.setProperty('--ribbon-y',`${(current*height*.42).toFixed(2)}px`);
   element.style.setProperty('--ribbon-scale',(1+current*.15).toFixed(4));
  }
  function tick(){
   current+=(target-current)*.18;
   if(Math.abs(target-current)<.0001)current=target;
   paint();
   frame=current===target?0:requestAnimationFrame(tick);
  }
  function scroll(){
   target=motion.matches?0:Math.min(1,Math.max(0,(window.scrollY-top)/height));
   if(!frame&&target!==current)frame=requestAnimationFrame(tick);
  }
  function measure(){
   if(!hero)return;
   const bounds=hero.getBoundingClientRect();top=bounds.top+window.scrollY;height=Math.max(1,bounds.height);
   scroll();
  }
  function preference(){
   if(frame)cancelAnimationFrame(frame);frame=0;
   if(motion.matches){current=target=0;paint()}else scroll();
  }
  measure();
  window.addEventListener('scroll',scroll,{passive:true});
  window.addEventListener('resize',measure);
  motion.addEventListener('change',preference);
  return()=>{cancelAnimationFrame(frame);window.removeEventListener('scroll',scroll);window.removeEventListener('resize',measure);motion.removeEventListener('change',preference)};
 },[]);
 return <div ref={ribbon} className="glass-ribbon" aria-hidden="true"><div className="glass-ribbon-light"/><div className="glass-ribbon-plates">{Array.from({length:56},(_,i)=><span key={i} className="glass-ribbon-plate" style={{'--x':`${(13+i*1.85).toFixed(4)}%`,'--y':`${(-26+i*2.05+Math.sin(i/8)*5).toFixed(4)}%`,'--twist':`${(i*4.6-35).toFixed(4)}deg`,'--depth':`${(Math.sin(i/9)*40).toFixed(4)}px`,'--order':i} as CSSProperties}><i/></span>)}</div><div className="glass-ribbon-shadow"/></div>
}
