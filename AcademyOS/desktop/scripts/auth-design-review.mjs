import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const base=process.env.BASE_URL||'http://127.0.0.1:3100';
const browser=await chromium.launch({channel:'msedge',headless:true});
const errors=[];
try{
 const page=await browser.newPage();page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 for(const size of [{width:1440,height:900},{width:1366,height:768},{width:390,height:844},{width:320,height:568}]){
  await page.setViewportSize(size);
  for(const path of ['/login','/signup','/signup/join','/register-school','/reset-password']){
   console.log(size.width,path);await page.goto(base+path,{waitUntil:'domcontentloaded'});await page.locator('.login-card').waitFor();await page.waitForTimeout(200);
   const fit=await page.evaluate(()=>{const c=document.querySelector('.login-card').getBoundingClientRect();return {page:document.documentElement.scrollHeight<=innerHeight,width:document.documentElement.scrollWidth<=innerWidth,card:c.bottom<=innerHeight,overflow:document.querySelector('.login-card').scrollHeight>document.querySelector('.login-card').clientHeight}});
   if(!fit.page||!fit.width||!fit.card||fit.overflow)throw Error(path+' '+JSON.stringify(size)+' '+JSON.stringify(fit));
   if(await page.getByText(/UI preview|DEMO CODE|Use demo invitation|Passwords are not saved or sent/).count())throw Error('Preview text in live screen: '+path);
   if(size.width===1366)await page.screenshot({caret:'initial',path:'test-results/auth-restored-'+path.slice(1).replaceAll('/','-')+'.png'});
  }
 }
 await page.setViewportSize({width:1366,height:768});await page.goto(base+'/login');await page.waitForTimeout(800);
 await page.getByLabel('Password',{exact:true}).fill('example-password');await page.getByRole('button',{name:'Show password',exact:true}).click();
 await page.waitForFunction(()=>document.querySelector('input[aria-label="Password"]').type==='text');
 await page.goto(base+'/register-school');await page.waitForTimeout(800);await page.getByRole('button',{name:'Create owner account',exact:true}).click();await page.getByText('Enter your full name.',{exact:true}).waitFor();
 // Exercise the real registration handler with a mocked Auth response, without sending an email.
 await page.route('**/auth/v1/signup**',route=>route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({id:'test-owner',email:'owner@example.com',identities:[{id:'test-identity'}]})}));
 await page.getByLabel('Your full name',{exact:true}).fill('Test Owner');await page.getByLabel('Work email address',{exact:true}).fill('owner@example.com');await page.getByLabel('Create password',{exact:true}).fill('ExamplePass123');await page.getByLabel('Confirm password',{exact:true}).fill('ExamplePass123');await page.getByRole('button',{name:'Create owner account',exact:true}).click();
 await page.getByRole('button',{name:'Resend confirmation email',exact:true}).waitFor();
 if(await page.getByText('DEMO CODE',{exact:false}).count())throw Error('Fake verification code exposed');
 for(const size of [{width:1366,height:768},{width:320,height:568}]){await page.setViewportSize(size);if(await page.evaluate(()=>document.documentElement.scrollHeight>innerHeight||document.querySelector('.login-card').scrollHeight>document.querySelector('.login-card').clientHeight))throw Error('Verification screen overflows '+size.width)}
 if(errors.length)throw Error(errors.join('\n'));
 console.log('Auth design passed: five routes at four viewport sizes, no page or card scrolling, password visibility, validation and mocked real-email verification flow. No real account or email was created.');
}finally{await browser.close()}
