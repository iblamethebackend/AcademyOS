'use client';
import {useEffect,useRef} from 'react';

export function LandingMotion(){
 const progress=useRef<HTMLDivElement>(null);
 useEffect(()=>{
  const root=document.querySelector('.landing');if(!root)return;
  const preference=matchMedia('(prefers-reduced-motion: reduce)');
  let observer:IntersectionObserver|undefined,frame=0;
  const animations=new Set<Animation>();
  const selectors='.landing-hero-copy,.landing-hero-aside,.landing-section-heading,.landing-split-heading,.landing-benefit,.landing-demo,.landing-campus-photo,.landing-campus-copy,.landing-feature-group,.landing-mobile-story,.landing-steps>li,.landing-faq-list details,.landing-closing>div:last-child,.landing-footer-top';
  function setup(){
   observer?.disconnect();animations.forEach(a=>a.cancel());animations.clear();
   if(preference.matches)return;
   observer=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
     if(!entry.isIntersecting)return;
     const target=entry.target;observer?.unobserve(target);
     const animation=target.animate([{opacity:.15,transform:'translateY(26px)'},{opacity:1,transform:'translateY(0)'}],{duration:700,easing:'cubic-bezier(.2,.7,.2,1)',fill:'none'});
     animations.add(animation);animation.onfinish=()=>animations.delete(animation);
    });
   },{threshold:.08});
   root?.querySelectorAll(selectors).forEach(el=>observer?.observe(el));
  }
  function paint(){frame=0;
   if(!preference.matches){
    const showcase=root?.querySelector<HTMLElement>('.landing-demo'),phone=root?.querySelector<HTMLElement>('.landing-phone-scene');
    if(showcase){const rect=showcase.getBoundingClientRect();const amount=Math.max(-1,Math.min(1,(rect.top-innerHeight*.25)/innerHeight));showcase.style.setProperty('--showcase-tilt',`${amount*9}deg`)}
    if(phone){const rect=phone.getBoundingClientRect();const amount=Math.max(-1,Math.min(1,(rect.top-innerHeight*.2)/innerHeight));phone.style.setProperty('--phone-turn',`${amount*22}deg`);phone.style.setProperty('--phone-rise',`${amount*30}px`)}
   }
const distance=document.documentElement.scrollHeight-innerHeight;progress.current?.style.setProperty('transform',`scaleX(${distance>0?Math.min(1,Math.max(0,scrollY/distance)):0})`)}
  function scroll(){if(!frame)frame=requestAnimationFrame(paint)}
  setup();paint();preference.addEventListener('change',setup);window.addEventListener('scroll',scroll,{passive:true});window.addEventListener('resize',scroll);
  return()=>{observer?.disconnect();animations.forEach(a=>a.cancel());cancelAnimationFrame(frame);preference.removeEventListener('change',setup);window.removeEventListener('scroll',scroll);window.removeEventListener('resize',scroll)};
 },[]);
 return <div className="landing-reading-progress" aria-hidden="true"><div ref={progress}/></div>;
}
