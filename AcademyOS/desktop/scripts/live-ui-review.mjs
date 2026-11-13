import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const base=process.env.BASE_URL||'http://127.0.0.1:3000';
const browser=await chromium.launch({channel:'msedge',headless:true});const page=await browser.newPage({viewport:{width:1366,height:768}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
try{
 await page.goto(base+'/login');await page.getByRole('heading',{name:'Welcome back.',exact:true}).waitFor();
 if(await page.getByRole('button',{name:'Fill demo account',exact:true}).count())throw Error('Demo credentials remain enabled in live mode');
 await page.getByRole('button',{name:'Forgot password?',exact:true}).click();await page.getByRole('button',{name:'Send reset instructions',exact:true}).waitFor();
 await page.goto(base+'/register-school');await page.getByLabel('Your full name',{exact:true}).waitFor();await page.getByRole('button',{name:'Create owner account',exact:true}).waitFor();
 if(await page.evaluate(()=>document.documentElement.scrollHeight>innerHeight))throw Error('Registration page scrolls');
 await page.goto(base+'/workspace');await page.waitForURL('**/login?next=*');
 const r=await page.request.get(base+'/api/workspace');if(r.status()!==401)throw Error('Anonymous workspace access not rejected: '+r.status());
 const csrf=await page.request.patch(base+'/api/workspace',{headers:{Origin:'https://untrusted.example'},data:{}});if(csrf.status()!==403)throw Error('Invalid-origin mutation not rejected');
 if(errors.length)throw Error(errors.join('\n'));console.log('Live-mode UI, unauthenticated route guards and mutation-origin checks passed. No email or account creation was attempted.');
}finally{await browser.close()}
