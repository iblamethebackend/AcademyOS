import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require('Z:/Rainbow/node_modules/playwright');
const b=await chromium.launch({channel:'msedge',headless:true});
try{const p=await b.newPage({viewport:{width:1440,height:950}});const errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});await p.goto('http://127.0.0.1:3100/',{waitUntil:'networkidle'});
const all=await p.locator('.landing-feature-group details').count();if(all!==29)throw Error('Missing feature coverage');
await p.getByRole('button',{name:'Available now',exact:true}).click();if(await p.locator('.feature-status:not(.available)').count())throw Error('Planned feature labelled available');if(await p.locator('.landing-feature-group details').count()!==6)throw Error('Incorrect available feature count');
await p.getByRole('button',{name:'Planned',exact:true}).click();if(await p.locator('.feature-status.available').count())throw Error('Available feature in planned filter');await p.getByText('Payments & reconciliation',{exact:true}).click();await p.getByText('Online checkout, payment verification, settlements and payment dispute tracking.',{exact:true}).waitFor();
await p.getByRole('button',{name:'The full picture',exact:true}).click();if(await p.locator('.landing-feature-group details').count()!==all)throw Error('Reset filter failed');
await p.locator('#mobile').scrollIntoViewIfNeeded();await p.waitForTimeout(850);await p.screenshot({caret:'initial',path:'test-results/platform-mobile-story.png'});
for(const width of [1440,390,320]){await p.setViewportSize({width,height:900});await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(800);if(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Overflow '+width);await p.locator('#features').scrollIntoViewIfNeeded();await p.waitForTimeout(800);await p.screenshot({caret:'initial',path:'test-results/platform-features-'+width+'.png'})}
await p.emulateMedia({reducedMotion:'reduce'});await p.locator('#questions').scrollIntoViewIfNeeded();if(await p.evaluate(()=>document.getAnimations().some(a=>a.playState==='running')))throw Error('Motion still running with reduced motion');
if(errors.length)throw Error(errors.join('\n'));console.log('Feature directory passed: '+all+' features, availability filters, details, mobile layouts, and reduced motion.');}finally{await b.close()}

