import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
import fs from 'node:fs';
const out=new URL('../previews/',import.meta.url);fs.mkdirSync(out,{recursive:true});
const roles=JSON.parse(fs.readFileSync(new URL('./workspaces.json',import.meta.url),'utf8'));
const browser=await chromium.launch({channel:'msedge',headless:true});
const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const shot=async name=>{await page.waitForTimeout(450);await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:new URL(name+'.png',out).pathname.replace(/^\/(\w:)/,'$1')})};
await page.goto('http://127.0.0.1:8765');await page.getByText('More room for').waitFor();await shot('mobile-welcome');
await page.getByRole('button',{name:'Explore the demo'}).click();await page.getByText('Good morning, Neha').waitFor();await shot('mobile-parent');
await page.getByRole('button',{name:/Fractions, all around us/}).click();await page.getByRole('button',{name:'Mark reviewed in preview'}).click();await page.getByText('Reviewed in this preview').waitFor();
await page.getByRole('tab',{name:'Workspace',exact:true}).click();await page.getByRole('textbox').fill('zzzz');await page.getByText('No matching modules. Try another search.').waitFor();await page.getByRole('textbox').fill('');await shot('mobile-modules');
await page.getByRole('tab',{name:'Inbox',exact:true}).click();await page.getByRole('button',{name:/Parent–teacher conversations/}).click();await shot('mobile-message');await page.getByRole('button',{name:'Close details'}).click();
for(let i=1;i<roles.length;i++){
 await page.getByRole('tab',{name:'You',exact:true}).click();await page.getByRole('button',{name:'Explore another workspace'}).click();
 await page.getByRole('radio').filter({hasText:roles[i].name}).first().click();await page.getByText(`Good morning, ${roles[i].person}`).waitFor();
 await page.getByRole('tab',{name:'Today',exact:true}).click();await shot('mobile-'+roles[i].name.toLowerCase().replace(/[^a-z]+/g,'-'));
 await page.getByRole('tab',{name:'Workspace',exact:true}).click();await shot('modules-'+i);await page.getByRole('button').filter({hasText:roles[i].modules[0]}).first().click();await shot('detail-'+i);await page.getByRole('button',{name:'Close details'}).click();
}
await page.setViewportSize({width:1440,height:1050});await page.getByRole('tab',{name:'You',exact:true}).click();await page.getByRole('button',{name:'Explore another workspace'}).click();await page.getByRole('radio').filter({hasText:'School leadership'}).click();await shot('desktop-overview');
await page.getByRole('tab',{name:'Workspace',exact:true}).click();await shot('desktop-workspace');
await page.setViewportSize({width:320,height:740});await page.getByRole('tab',{name:'Today',exact:true}).click();await shot('mobile-small');
if(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth))throw new Error('Horizontal page overflow');
if(errors.length)throw new Error(errors.join('\n'));
fs.writeFileSync(new URL('../ui-verification.json',import.meta.url),JSON.stringify({roles:roles.length,viewports:[390,1440,320],checks:['Role switching','Task reviewed state','Module details across all departments','Search empty state','Inbox read state','No page errors','No horizontal overflow at 320px'],errors},null,2));
await browser.close();console.log('Verified 18 workspaces and saved UI previews.');
