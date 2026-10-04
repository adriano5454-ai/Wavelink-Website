/* Optional local-source Chromium QA. Does not visit the live website or demo.
   Requires playwright-core (or playwright). Use BROWSER_EXECUTABLE when needed.
   Source requests are fulfilled from disk at a synthetic HTTPS origin, so this
   checks rendering and navigation without claiming HTTP/hosting acceptance. */
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
let chromium;
try { ({ chromium } = require('playwright-core')); }
catch (_) { ({ chromium } = require('playwright')); }
const root = path.resolve(__dirname, '..');
const site = path.join(root, 'site');
const out = process.env.QA_OUTPUT || path.join(root, 'test-output');
fs.mkdirSync(out, {recursive:true});
const keys = ['equipment','maintenance','operations','safety','people','documents','control'];
const widths = [320,390,600,740,741,768,900,1000,1001,1024,1280,1440,1920];
(async () => {
  const browser = await chromium.launch({headless:true,
    ...(process.env.BROWSER_EXECUTABLE ? {executablePath:process.env.BROWSER_EXECUTABLE} : {}),
    args:['--no-sandbox','--disable-dev-shm-usage','--no-zygote','--single-process']});
  const results=[]; const errors=[];
  const setup = async context => {
    await context.route('https://www.mywavelink.com/**', async route => {
      const u = new URL(route.request().url());
      const relative = u.pathname==='/' ? 'index.html' : decodeURIComponent(u.pathname).slice(1);
      const filename = path.resolve(site,relative);
      if(!filename.startsWith(site+path.sep)||!fs.existsSync(filename)||!fs.statSync(filename).isFile())return route.abort();
      const mime={'.html':'text/html','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg'};
      return route.fulfill({body:fs.readFileSync(filename),contentType:mime[path.extname(filename)]||'application/octet-stream'});
    });
  };
  const noOverflow = async (page,label) => {
    const bad=await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>{
      const r=e.getBoundingClientRect();const s=getComputedStyle(e);
      return r.width>0 && s.visibility!=='hidden' && (r.right>innerWidth+1||r.left<-1) && !e.classList.contains('sr-only') && !e.classList.contains('skip-link');
    }).map(e=>e.tagName+'.'+(typeof e.className==='string'?e.className:'svg')));
    assert.equal(bad.length,0,label+': overflow '+bad.slice(0,10));
  };
  try {
    const context=await browser.newContext({viewport:{width:1440,height:950},reducedMotion:'reduce'});
    await setup(context);const page=await context.newPage();page.setDefaultTimeout(5000);
    for(const width of widths){
      await page.setViewportSize({width,height:950});
      const runtime=[];page.on('pageerror',e=>runtime.push(e.message));
      await page.goto('https://www.mywavelink.com/',{waitUntil:'load'});
      assert.equal(await page.locator('h1').count(),1);
      assert.equal(await page.locator('[role="tab"]').count(),7);
      assert.equal(await page.locator('#panel-equipment').isVisible(),true);
      assert.equal(await page.locator('.menu-toggle').isVisible(),width<=1000);
      for(const key of keys){
        await page.locator('#tab-'+key).click();
        assert.equal(await page.locator('#panel-'+key).isVisible(),true);
        assert.equal(await page.locator('[role="tabpanel"]:visible').count(),1);
        assert.equal(await page.locator('#tab-'+key).getAttribute('aria-selected'),'true');
        await noOverflow(page,width+'/'+key);
      }
      await page.locator('#tab-equipment').click();
      await page.locator('#tab-equipment').press('End');
      assert.equal(await page.locator('#tab-control').evaluate(e=>e===document.activeElement),true);
      assert.equal(await page.locator('#panel-equipment').isVisible(),true);
      await page.locator('#tab-control').press('Enter');
      assert.equal(await page.locator('#panel-control').isVisible(),true);
      await page.locator('#tab-control').press('Home');
      await page.locator('#tab-equipment').press('Space');
      assert.equal(await page.locator('#panel-equipment').isVisible(),true);
      await page.locator('.capability-directory>summary').click();
      assert.equal(await page.locator('.capability-grid .capability:visible').count(),18);
      await noOverflow(page,width+'/directory');
      await page.locator('.capability-grid [data-show-panel="safety"]').first().click();
      assert.equal(await page.locator('#panel-safety').isVisible(),true);
      assert.equal(await page.locator('#tab-safety').evaluate(e=>e===document.activeElement),true);
      await page.locator('.capability-directory>summary').click();
      await page.locator('#imports [data-show-panel="documents"]').click();
      assert.equal(await page.locator('#panel-documents').isVisible(),true);
      for(const faq of await page.locator('.faq-item').all()){
        await faq.locator('summary').click();assert.equal(await faq.locator('p').isVisible(),true);await noOverflow(page,width+'/faq');await faq.locator('summary').click();
      }
      if(width<=1000){
        await page.locator('.menu-toggle').click();
        assert.equal(await page.locator('#main-navigation').isVisible(),true);
        await noOverflow(page,width+'/menu');await page.locator('.menu-toggle').press('Escape');
        assert.equal(await page.locator('#main-navigation').isVisible(),false);
        await page.locator('.menu-toggle').click();await page.locator('#main-navigation a[href="#imports"]').click();
        assert.equal(await page.locator('#main-navigation').isVisible(),false);
      }
      await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('Denied')}}}));
      await page.locator('.copy-email').click();
      assert.match(await page.locator('#copy-status').innerText(),/manually/);
      await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async s=>{window.__copied=s}}}));
      await page.locator('.copy-email').click();
      assert.equal(await page.evaluate(()=>window.__copied),'comercial@mywavelink.com');
      for(const name of ['privacy.html','404.html']){
        await page.goto('https://www.mywavelink.com/'+name,{waitUntil:'load'});await noOverflow(page,width+'/'+name);
      }
      assert.deepEqual(runtime,[]);results.push({width,categories:7,capabilities:18,passed:true});

    }
    await page.setViewportSize({width:1440,height:1000});await page.goto('https://www.mywavelink.com/',{waitUntil:'load'});
    await page.screenshot({path:path.join(out,'desktop-hero.png')});
    await page.screenshot({path:path.join(out,'desktop-full.png'),fullPage:true});
    for(const key of keys){await page.locator('#tab-'+key).click();await page.locator('#platform').screenshot({path:path.join(out,'platform-'+key+'.png')});}
    await page.setViewportSize({width:390,height:844});await page.locator('#tab-equipment').click();await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(out,'mobile-hero.png')});await page.screenshot({path:path.join(out,'mobile-full.png'),fullPage:true});
    await page.goto('https://www.mywavelink.com/#panel-documents',{waitUntil:'load'});assert.equal(await page.locator('#panel-documents').isVisible(),true);
    await page.setViewportSize({width:1280,height:950});await page.evaluate(()=>document.documentElement.style.fontSize='200%');
    for(const key of keys){await page.locator('#tab-'+key).click();await noOverflow(page,'200% text/'+key);}

    const cdp=await context.newCDPSession(page);await cdp.send('Emulation.setScriptExecutionDisabled',{value:true});await page.setViewportSize({width:390,height:844});await page.goto('https://www.mywavelink.com/',{waitUntil:'load'});
    assert.equal(await page.locator('.platform-panel:visible').count(),7);assert.equal(await page.locator('#main-navigation').isVisible(),true);await noOverflow(page,'No JavaScript');
  } catch(e){errors.push(e.stack);}
  const report={version:'3.0.1',browser:browser.version(),mode:'Local-source HTTPS route fulfilment; not live HTTP/deployment',results,errors,passed:errors.length===0};
  fs.writeFileSync(path.join(out,'browser-checks.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({passed:report.passed,widths:results.length,errors},null,2));await browser.close();if(errors.length)process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
