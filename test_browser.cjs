'use strict';
const {chromium,webkit}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');const fs=require('node:fs');
const base=process.env.BASE_URL||'http://127.0.0.1:5000';
(async()=>{fs.mkdirSync('artifacts',{recursive:true});for(const [name,engine] of [['chromium',chromium],['webkit',webkit]]){
 const browser=await engine.launch({headless:true});try{const p=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];p.on('pageerror',e=>errors.push(e.message));
 let mode='success';let posted=null;
 await p.route('**/api/emotions',async route=>{posted=route.request();if(mode==='network')return route.abort();if(mode==='slow')await new Promise(r=>setTimeout(r,400));return route.fulfill({status:mode==='error'?503:200,contentType:'application/json',body:JSON.stringify(mode==='error'?{error:'The model is unavailable. Your text is still here; try again.'}:mode==='malformed'?{scores:{joy:'bad'}}:{scores:{anger:.01,disgust:.02,fear:.03,joy:.9,sadness:.04,dominant_emotion:'joy'}})});});
 await p.goto(base);await p.getByRole('button',{name:'A moment of joy'}).click();await p.locator('#analyze').click();await p.locator('#scores:not([hidden])').waitFor();assert.equal(await p.locator('meter').count(),5);assert.equal(posted.method(),'POST');assert(!posted.url().includes('glad'));assert.equal(posted.postDataJSON().text,'I am glad this happened.');
 for(const scenario of ['error','network','malformed']){mode=scenario;await p.locator('#analyze').click();await p.locator('[data-error=true]').waitFor();assert.equal(await p.locator('#scores').isVisible(),false);assert.equal(await p.locator('#textToAnalyze').inputValue(),'I am glad this happened.');assert.equal(await p.locator('#analyze').isEnabled(),true);}
 mode='slow';await p.locator('#analyze').click();await p.locator('#textToAnalyze').fill('Changed while waiting.');await p.waitForTimeout(600);assert.equal(await p.locator('#scores').isVisible(),false);assert.equal(await p.locator('#analyze').isEnabled(),true);
 await p.getByRole('button',{name:'Clear',exact:true}).click();assert.equal(await p.locator('#textToAnalyze').inputValue(),'');
 // Capture the actual idle UI; no synthetic scores are presented as live inference.
 await p.screenshot({path:`artifacts/emotion-${name}.png`,fullPage:true});
 for(const width of [320,390,768,1024,1440]){await p.setViewportSize({width,height:900});assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
 assert.deepEqual(errors,[]);console.log(name+': success, failure, network, malformed response, stale response, reset and five viewport checks passed');
 }finally{await browser.close();}
}})().catch(e=>{console.error(e);process.exitCode=1});
