'use client';
import {useEffect,useRef,useState} from 'react';

const COUNT=900;
const stages=['A world of possibility','Your school takes shape','Everything, connected','Made for your community'];
type Point=[number,number,number];
// Stable coordinates make the field repeatable and allow smooth shape transitions.
const points=Array.from({length:COUNT},(_,i)=>{
 const y=1-2*(i+.5)/COUNT,angle=i*Math.PI*(3-Math.sqrt(5)),radius=Math.sqrt(1-y*y);
 const globe:Point=[Math.cos(angle)*radius,y,Math.sin(angle)*radius];
 const side=i%2===0?-1:1,u=((i*73)%COUNT)/COUNT,v=((i*151)%COUNT)/COUNT;
 const book:Point=[side*(.08+u*.95),(v-.5)*1.5+Math.sin(u*Math.PI)*.2,(.5-u)*.42];
 const grid:Point=[((i%30)/29-.5)*1.8,(Math.floor(i/30)/29-.5)*1.55,Math.sin(i*.17)*.12];
 const a=i/COUNT*Math.PI*2,ring=i%3;
 const orbit:Point=ring===0?[Math.cos(a),Math.sin(a)*.4,Math.sin(a)*.8]:ring===1?[Math.cos(a)*.4,Math.sin(a),Math.cos(a)*.8]:[Math.cos(a)*.85,Math.sin(a)*.85,Math.sin(a)*.1];
 return [globe,book,grid,orbit];
});

export function LandingParticles(){
 const canvas=useRef<HTMLCanvasElement>(null),pausedRef=useRef(false);
 const [paused,setPaused]=useState(false),[reduced,setReduced]=useState(false),[stage,setStage]=useState(0);
 useEffect(()=>{
  const surface=canvas.current,ctx=surface?.getContext('2d');if(!surface||!ctx)return;
  const preference=matchMedia('(prefers-reduced-motion: reduce)');
  let width=0,height=0,frame=0,last=0,time=0,scroll=0,progress=0,currentStage=-1,visible=true;
  function measure(){width=innerWidth;height=innerHeight;const ratio=Math.min(devicePixelRatio||1,1.5);surface!.width=Math.round(width*ratio);surface!.height=Math.round(height*ratio);ctx!.setTransform(ratio,0,0,ratio,0,0);updateScroll()}
  function updateScroll(){scroll=window.scrollY;const total=document.documentElement.scrollHeight-height;progress=total>0?Math.min(1,scroll/total):0;if(!frame&&visible)frame=requestAnimationFrame(draw)}
  function draw(stamp:number){
   frame=0;const delta=Math.min(40,stamp-last||16);last=stamp;
   const still=preference.matches||pausedRef.current;
   if(!still)time+=delta*.00012;
   ctx!.clearRect(0,0,width,height);
   const position=preference.matches?0:progress*3,from=Math.floor(position),to=Math.min(3,from+1),blend=position-from,mix=blend*blend*(3-2*blend);
   if(from!==currentStage){currentStage=from;setStage(from)}
   const hero=Math.max(0,1-scroll/(height*.85));
   const mobile=width<760;
   const cx=width*(mobile?.68:.77),cy=height*(mobile?.31:.48),scale=Math.min(width*(mobile?.51:.26),height*.39);
   const rotation=preference.matches?-.2:time*.23+progress*1.6,cos=Math.cos(rotation),sin=Math.sin(rotation);
   ctx!.globalAlpha=hero*.66+.18;
   const glow=ctx!.createRadialGradient(cx,cy,0,cx,cy,scale*1.5);glow.addColorStop(0,'rgba(84,138,103,.1)');glow.addColorStop(1,'rgba(84,138,103,0)');ctx!.fillStyle=glow;ctx!.fillRect(0,0,width,height);
   for(let i=0;i<COUNT;i++){
    if(mobile&&i%2)continue;
    const p=points[i][from],q=points[i][to];
    const x=p[0]+(q[0]-p[0])*mix,y=p[1]+(q[1]-p[1])*mix,z=p[2]+(q[2]-p[2])*mix;
    const rx=x*cos-z*sin,rz=x*sin+z*cos,perspective=2.9/(2.9-rz*.42);
    const drift=still?0:Math.sin(time+i*.07)*.008;
    const px=cx+(rx+drift)*scale*perspective,py=cy+(y+drift)*scale*perspective;
    const depth=(rz+1)/2,alpha=(.23+depth*.67)*(hero*.76+.24);
    ctx!.fillStyle=i%7===0?`rgba(218,194,150,${alpha})`:`rgba(161,204,173,${alpha})`;
    ctx!.beginPath();ctx!.arc(px,py,(.65+depth*.95)*perspective,0,Math.PI*2);ctx!.fill();
    if(i%19===0&&hero>.3){ctx!.strokeStyle=`rgba(140,191,154,${alpha*.16})`;ctx!.beginPath();ctx!.moveTo(px,py);ctx!.lineTo(px+rx*14,py+y*14);ctx!.stroke()}
   }
   ctx!.globalAlpha=1;
   if(!still&&visible)frame=requestAnimationFrame(draw);
  }
  function changePreference(){setReduced(preference.matches);updateScroll()}
  function visibility(){visible=!document.hidden;if(!visible){cancelAnimationFrame(frame);frame=0}else{last=0;updateScroll()}}
  function toggle(){updateScroll()}
  measure();changePreference();window.addEventListener('resize',measure);window.addEventListener('scroll',updateScroll,{passive:true});window.addEventListener('academyos-motion',toggle);document.addEventListener('visibilitychange',visibility);preference.addEventListener('change',changePreference);
  return()=>{cancelAnimationFrame(frame);window.removeEventListener('resize',measure);window.removeEventListener('scroll',updateScroll);window.removeEventListener('academyos-motion',toggle);document.removeEventListener('visibilitychange',visibility);preference.removeEventListener('change',changePreference)};
 },[]);
 return <><canvas ref={canvas} className="landing-particle-canvas" aria-hidden="true"/><div className="landing-motion-console"><span><i/> {String(stage+1).padStart(2,'0')} / {stages[stage]}</span><button type="button" disabled={reduced} aria-label={paused?'Resume ambient animation':'Pause ambient animation'} aria-pressed={paused} onClick={()=>{const next=!paused;pausedRef.current=next;setPaused(next);window.dispatchEvent(new Event('academyos-motion'))}}>{reduced?'Reduced motion':paused?'Play motion':'Pause motion'}<span aria-hidden="true">{paused?'▷':'Ⅱ'}</span></button></div></>;
}
