import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const browser=await chromium.launch({channel:'msedge',headless:true});const page=await browser.newPage();let navigations=0;
page.on('framenavigated',f=>{if(f===page.mainFrame()){navigations++;console.log('NAV',f.url())}});
page.on('pageerror',e=>console.log('ERROR',e.message));
page.on('console',m=>{if(m.type()==='error'||/reload|refresh|hmr/i.test(m.text()))console.log('CONSOLE',m.text().slice(0,1200))});
page.on('response',r=>{if(r.request().isNavigationRequest()||r.status()>=400)console.log('RESPONSE',r.status(),r.url().split('?')[0])});
try{await page.goto('http://localhost:3000/login',{waitUntil:'domcontentloaded',timeout:25000});await page.waitForTimeout(12000);console.log('RESULT',JSON.stringify({navigations,title:await page.title(),text:(await page.locator('body').innerText()).slice(0,900)}));await page.screenshot({path:'test-results/login-loop.png'})}finally{await browser.close()}
