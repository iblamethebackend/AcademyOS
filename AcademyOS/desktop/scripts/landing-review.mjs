import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const base=process.env.BASE_URL||'http://127.0.0.1:3100';
const browser=await chromium.launch({channel:'msedge',headless:true});
const errors=[];
try{
 const page=await browser.newPage({viewport:{width:1440,height:950}});page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 const response=await page.goto(base+'/',{waitUntil:'networkidle'});if(response.status()!==200)throw Error('Home page failed');
 if(await page.title()!=='AcademyOS · A more connected school day')throw Error('Wrong page metadata');
 await page.screenshot({caret:'initial',path:'test-results/landing-desktop.png'});await page.screenshot({caret:'initial',path:'test-results/landing-full.png',fullPage:true});
 await page.getByRole('tab',{name:'People & departments',exact:true}).click();await page.getByRole('heading',{name:'Everyone has a place.',exact:true}).waitFor();
 await page.getByRole('tab',{name:'People & departments',exact:true}).press('ArrowRight');await page.getByRole('heading',{name:'A year with a clear beginning.',exact:true}).waitFor();
 await page.getByRole('tab',{name:'Academic foundations',exact:true}).press('Home');await page.getByRole('heading',{name:'A clearer picture. A calmer beginning.',exact:true}).waitFor();
 await page.locator('.landing-faq-list summary').first().click();if(!(await page.locator('.landing-faq-list details').first().getAttribute('open')===''))throw Error('FAQ failed to open');
 await page.locator('.landing-faq-list summary').nth(1).click();if(await page.locator('.landing-faq-list details[open]').count()!==1)throw Error('FAQ did not preserve a single expanded answer');
 const hrefs=await page.locator('a').evaluateAll(a=>a.map(x=>x.getAttribute('href')));for(const href of hrefs){if(href.startsWith('#')&&!await page.locator(href).count())throw Error('Missing anchor '+href);if(!href.startsWith('#')&&!['/','/login','/register-school'].includes(href))throw Error('Unexpected destination '+href)}
 for(const size of [{width:1024,height:768},{width:768,height:1024},{width:390,height:844},{width:320,height:568}]){
  await page.setViewportSize(size);await page.goto(base+'/');await page.waitForTimeout(200);
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Horizontal overflow '+size.width);
  for(const tab of ['Overview','People & departments','Academic foundations']){await page.getByRole('tab',{name:tab,exact:true}).click();if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Tab overflow '+size.width+' '+tab)}
  if(size.width===390){await page.getByRole('tab',{name:'Overview',exact:true}).click();await page.evaluate(()=>scrollTo(0,0));await page.screenshot({caret:'initial',path:'test-results/landing-mobile.png'});await page.getByLabel('Open navigation',{exact:true}).click();await page.getByRole('navigation',{name:'Mobile navigation',exact:true}).getByRole('link',{name:'Register your school',exact:true}).click();await page.waitForURL('**/register-school')}
 }
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto(base+'/');await page.getByRole('button',{name:'Pause ambient animation',exact:true}).waitFor();await page.waitForFunction(()=>document.querySelector('.landing-motion-console button')?.disabled);
 await page.setViewportSize({width:1440,height:950});await page.goto(base+'/login');await page.screenshot({caret:'initial',path:'test-results/auth-split-login.png'});await page.goto(base+'/register-school');await page.screenshot({caret:'initial',path:'test-results/auth-split-register.png'});
 if(errors.length)throw Error(errors.join('\n'));console.log('Landing page passed: responsive layouts, interactive preview and keyboard tabs, FAQs, all links, mobile navigation and reduced motion.');
}finally{await browser.close()}
