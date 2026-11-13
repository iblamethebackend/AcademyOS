import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const browser=await chromium.launch({channel:'msedge',headless:true});const base=process.env.BASE_URL||'http://127.0.0.1:3100';
try{
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 const pose=()=>page.locator('.glass-ribbon').evaluate(e=>({turn:parseFloat(e.style.getPropertyValue('--ribbon-turn'))||0,group:getComputedStyle(e.querySelector('.glass-ribbon-plates')).transform,plate:getComputedStyle(e.querySelector('.glass-ribbon-plate:nth-child(25)')).transform}));
 for(const size of [{width:1440,height:950},{width:390,height:844},{width:320,height:568}]){
  await page.setViewportSize(size);await page.goto(base+'/',{waitUntil:'networkidle'});const start=await pose();
  if(size.width===1440)await page.screenshot({caret:'initial',path:'test-results/scroll-ribbon-start.png'});
  await page.evaluate(()=>scrollTo(0,300));await page.waitForFunction(()=>parseFloat(document.querySelector('.glass-ribbon').style.getPropertyValue('--ribbon-turn'))>50);await page.waitForTimeout(700);
  const forward=await pose();if(start.group===forward.group||start.plate===forward.plate)throw Error('Sculpture did not rotate and move at '+size.width);
  const visible=await page.locator('.glass-ribbon-plate').evaluateAll(plates=>plates.some(p=>{const r=p.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth}));if(!visible)throw Error('Animated ribbon is offscreen');
  if(size.width!==320)await page.screenshot({caret:'initial',path:'test-results/scroll-ribbon-'+size.width+'.png'});
  await page.evaluate(()=>scrollTo(0,120));await page.waitForTimeout(750);const reverse=await pose();if(reverse.turn>=forward.turn)throw Error('Scroll reversal failed');
  await page.evaluate(()=>scrollTo(0,0));await page.waitForFunction(()=>parseFloat(document.querySelector('.glass-ribbon').style.getPropertyValue('--ribbon-turn'))===0);
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Scroll animation caused horizontal overflow');
 }
 await page.emulateMedia({reducedMotion:'reduce'});const still=await pose();await page.evaluate(()=>scrollTo(0,400));await page.waitForTimeout(400);const reduced=await pose();if(reduced.turn!==0||reduced.plate!==still.plate||reduced.group!==still.group)throw Error('Reduced motion was not respected');
 await page.emulateMedia({reducedMotion:'no-preference'});await page.waitForFunction(()=>parseFloat(document.querySelector('.glass-ribbon').style.getPropertyValue('--ribbon-turn'))>70);
 await page.goto(base+'/login');if(errors.length)throw Error(errors.join('\n'));
 console.log('Scroll animation passed: visible movement and plate rotation on desktop/mobile, reverse scrolling, no overflow, reduced-motion toggle, and clean navigation.');
}finally{await browser.close()}
