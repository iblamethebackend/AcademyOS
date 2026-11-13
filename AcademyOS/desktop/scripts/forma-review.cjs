const {chromium}=require('Z:/Rainbow/node_modules/playwright');
const assert=require('node:assert/strict');
(async()=>{const b=await chromium.launch({channel:'msedge',headless:true});const p=await b.newPage({viewport:{width:1440,height:950}});const errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});await p.goto('http://127.0.0.1:3100');const f=await (await p.waitForSelector('iframe')).contentFrame();await f.waitForSelector('#hero-heading');await p.waitForTimeout(1500);await p.screenshot({path:'test-results/exact-hero.png'});
for(const [ratio,phase] of [[.1,'0'],[.5,'1'],[.92,'2']]){await f.evaluate(r=>{const e=document.querySelector('.assembly');scrollTo({top:e.offsetTop+(e.offsetHeight-innerHeight)*r,behavior:'instant'})},ratio);await p.waitForTimeout(1000);assert.equal(await f.locator('.assembly').getAttribute('data-phase'),phase)}await p.screenshot({path:'test-results/exact-assembly.png'});
assert.equal(await f.locator('.fx-module').count(),29);
await f.locator('.fx-tab').nth(1).click();assert.equal(await f.locator('#fx-panel-1').isVisible(),true);
await f.locator('#fx-panel-1 summary').first().click();assert.equal(await f.locator('#fx-panel-1 details').first().getAttribute('open'),'');
await f.locator('.faq summary').first().click();assert.equal(await f.locator('.faq details').first().getAttribute('open'),'');
await f.locator('.motion-toggle').click();assert.equal(await f.locator('.motion-toggle').getAttribute('aria-pressed'),'true');
await f.locator('[data-step="1"]').click();assert.equal(await f.locator('.editor-wrap').getAttribute('data-stage'),'1');await p.screenshot({path:'test-results/exact-product.png'});
await f.locator('[data-step="2"]').click();assert.equal(await f.locator('.editor-wrap').getAttribute('data-stage'),'2');
for(const width of [390,320]){await p.setViewportSize({width,height:844});await f.evaluate(()=>scrollTo({top:0,behavior:'instant'}));await p.waitForTimeout(600);assert.ok(await f.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${width}`);await p.screenshot({path:`test-results/exact-mobile-${width}.png`})}
await f.locator('[data-audience="Parents & students"]').click();await p.waitForURL('**/login');
await p.goto('http://127.0.0.1:3100');const f2=await (await p.waitForSelector('iframe')).contentFrame();await f2.locator('[data-start]').first().click();await p.waitForURL('**/register-school');
assert.deepEqual(errors,[]);console.log('PASS: 3 scroll phases, feature explorer (6 categories/29 modules), details, FAQ, pause, product stages, mobile widths 390/320, login and registration links. No browser errors.');await b.close()})().catch(e=>{console.error(e);process.exit(1)});
