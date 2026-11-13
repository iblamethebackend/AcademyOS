import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const browser=await chromium.launch({channel:'msedge',headless:true});const page=await browser.newPage();const base=process.env.BASE_URL||'http://localhost:3000';let documents=0;const errors=[];
page.on('request',r=>{if(r.isNavigationRequest()&&r.frame()===page.mainFrame())documents++});
page.on('pageerror',e=>errors.push(e.message));
try{
 await page.goto(base+'/login',{waitUntil:'domcontentloaded',timeout:60000});
 await page.getByLabel('Email address',{exact:true}).fill('stability-check@example.com');
 await page.waitForTimeout(12000);
 if(documents!==1)throw Error('Login reloaded '+documents+' times');
 if(await page.getByLabel('Email address',{exact:true}).inputValue()!=='stability-check@example.com')throw Error('Form state was lost');
 await page.getByRole('button',{name:'Forgot password?',exact:true}).click();
 await page.getByRole('button',{name:'Send reset instructions',exact:true}).waitFor();
 if(errors.length)throw Error(errors.join('\n'));
 console.log('Login stable: one document load, form input retained, recovery navigation works, no runtime errors.');
}finally{await browser.close()}
