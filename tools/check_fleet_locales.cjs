/* Browser smoke for the bilingual public fleet guides, using only repository files. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
let chromium;
try{({chromium}=require('playwright-core'))}catch{({chromium}=require('playwright'))}
const site=path.resolve(__dirname,'../site'),origin='https://www.mywavelink.com',pages={
'en':'offshore-fleet-operations.html','pt-BR':'operacoes-de-frota-offshore.html'};
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.BROWSER_EXECUTABLE});
 try{
  for(const width of [320,390,1360]){
   const ctx=await browser.newContext({viewport:{width,height:920}});
   await ctx.route('**/*',r=>{
    const u=new URL(r.request().url());
    if(u.origin!==origin)return r.abort();
    let f=u.pathname.slice(1)||'index.html';
    if(pages.en===f.replace(/\/$/,'')+'.html'||pages['pt-BR']===f.replace(/\/$/,'')+'.html')f=f.replace(/\/$/,'')+'.html';
    if(!fs.existsSync(path.join(site,f)))return r.abort();
    return r.fulfill({path:path.join(site,f)});
   });
   const p=await ctx.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
   await p.goto(origin+'/#panel-operations');
   for(const [lang,file] of Object.entries(pages)){
    const peer=lang==='en'?'pt-BR':'en';
    const link=p.locator('#panel-operations a[href="'+file+'"]');
    assert(await link.isVisible());
    await link.click();
    assert.equal(await p.locator('html').getAttribute('lang'),lang);
    assert.equal(await p.locator('link[rel=canonical]').getAttribute('href'),origin+'/'+file);
    assert.equal(await p.locator('link[rel=alternate][hreflang="'+peer+'"]').getAttribute('href'),origin+'/'+pages[peer]);
    assert.equal(await p.locator('h1').count(),1);
    assert(await p.locator('a[href^="https://demo.mywavelink.com"]').isVisible());
    assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
    if(process.env.QA_OUTPUT&&((width===1360&&lang==='en')||(width===390&&lang==='pt-BR')))
     await p.screenshot({path:path.join(process.env.QA_OUTPUT,'fleet-guide-'+lang+'.png'),fullPage:true});
    await p.getByRole('navigation').locator('a').click();
    assert.equal(await p.locator('html').getAttribute('lang'),peer);
    await p.goto(origin+'/'+file.replace(/\.html$/,'/'));
    assert.equal(await p.locator('a[href="privacy.html"]').evaluate(e=>e.href),origin+'/privacy.html');
    assert.equal(await p.locator('a.skip-link').evaluate(e=>new URL(e.href).pathname),'/'+file);
    await p.goto(origin+'/#panel-operations');
   }
   await p.locator('#tab-safety').click();
   assert(await p.locator('#panel-safety a[href$="?area=readiness"]').isVisible());
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   assert.deepEqual(errors,[]);
   await ctx.close();
   console.log('PASS',width,'EN/PT switching, canonical URLs, guide aliases and readiness link');
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
