(()=>{
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');let lenis;
 function sync(){
  const paused=reduced.matches||document.body.classList.contains('motion-paused');
  if(paused){lenis?.destroy();lenis=undefined;return}
  if(!lenis&&window.Lenis)lenis=new Lenis({autoRaf:true,lerp:.12,smoothWheel:true,syncTouch:false,allowNestedScroll:true,prevent:node=>!!node.closest('dialog,textarea,[data-lenis-prevent]')});
 }
 sync();reduced.addEventListener('change',sync);
 const observer=new MutationObserver(records=>{
  for(const record of records){
   if(record.target===document.body){sync();continue}
   if(reduced.matches||document.body.classList.contains('motion-paused'))continue;
   const target=record.target;
   if(target instanceof HTMLElement&&target.matches('[role="tabpanel"]')&&!target.hidden)target.animate([{opacity:0,translate:'0 7px'},{opacity:1,translate:'0 0'}],{duration:280,easing:'cubic-bezier(.22,1,.36,1)'});
  }
 });
 observer.observe(document.body,{attributes:true,subtree:true,attributeFilter:['class','hidden']});
 window.addEventListener('pagehide',()=>{observer.disconnect();lenis?.destroy();reduced.removeEventListener('change',sync)},{once:true});
})();
