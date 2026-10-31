
import asyncio, json, sys
from playwright.async_api import async_playwright
BASE="https://ridham-interiors-e1eb3b.sites.tab.bot"
CFG=json.load(open("/home/user/tab/state/ridham-private/config.json"))
OUT=sys.argv[1]; WIDTHS=[int(x) for x in sys.argv[2].split(",")]; ENGINES=sys.argv[3].split(",")
FILTERS=["all","residential","bedroom","design","site"]
GRID_JS="""(()=>{const g=document.querySelector('#grid');const gr=g.getBoundingClientRect();const cs=[...g.querySelectorAll('.card')].filter(c=>getComputedStyle(c).display!=='none').map(c=>c.getBoundingClientRect());
 const cols=getComputedStyle(g).gridTemplateColumns.split(' ').length; const rows={};cs.forEach(r=>{const k=Math.round(r.top);rows[k]=(rows[k]||0)+r.width});
 const gap=parseFloat(getComputedStyle(g).columnGap)||0; const out=Object.keys(rows).sort((a,b)=>a-b).map(k=>{const n=cs.filter(r=>Math.round(r.top)==k).length;return Math.round((rows[k]+gap*(n-1))/gr.width*100)});
 const more=document.querySelector('#moreCard'); return {cols,rows:out,more:!more.hidden,moreSpan:more.style.gridColumn,overflowEls:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>document.documentElement.clientWidth+1&&getComputedStyle(e).position!=='fixed'&&r.width>0}).slice(0,3).map(e=>e.className||e.tagName)}})()"""
async def run():
  res=[]
  async with async_playwright() as p:
    for eng in ENGINES:
      br=await getattr(p,eng).launch()
      for w in WIDTHS:
        mobile = w<768
        ctx=await br.new_context(viewport={"width":w,"height":860 if w<1024 else 900}, device_scale_factor=2 if w<1024 else 1, is_mobile=(mobile and eng=="chromium"), has_touch=mobile)
        r=await ctx.request.post(BASE+"/login", form={"u":CFG["username"],"p":CFG["password"],"next":"/?preview=1"}, max_redirects=0)
        pg=await ctx.new_page(); errs=[]
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE+"/?preview=1", wait_until="networkidle", timeout=60000)
        await pg.add_style_tag(content=".js .reveal{transition:none!important} .more{animation:none!important}")
        await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in'))")
        await pg.wait_for_timeout(500)
        row={"eng":eng,"w":w,"login":r.status,"filters":{}}
        for f in FILTERS:
          await pg.click(f'.chip[data-f="{f}"]'); await pg.wait_for_timeout(350)
          gi=await pg.evaluate(GRID_JS)
          sw=await pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
          gi["scroll"]=sw; row["filters"][f]=gi
          el=await pg.query_selector("#work"); await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(250)
          await pg.evaluate("document.querySelectorAll('.card__media video').forEach(v=>{v.pause();v.style.opacity=0})")
          await el.screenshot(path=f"{OUT}/{eng}-{w}-projects-{f}.jpg", type="jpeg", quality=78)
        # show-all button works
        await pg.click('.chip[data-f="bedroom"]'); await pg.wait_for_timeout(200)
        if await pg.is_visible('#moreCard [data-showall]'):
          await pg.click('#moreCard [data-showall]'); await pg.wait_for_timeout(200)
          row["showall_ok"]=await pg.evaluate("document.querySelector('.chip.is-on').dataset.f==='all' && document.querySelector('#moreCard').hidden")
        else: row["showall_ok"]="n/a (no gap at this width)"
        # lightbox on p02 (logo used to show) 
        await pg.click('.chip[data-f="all"]'); await pg.wait_for_timeout(200)
        b=await pg.query_selector('[data-video="p02.mp4"]'); await b.scroll_into_view_if_needed(); await b.click()
        await pg.wait_for_timeout(2500)
        lb=await pg.evaluate("(()=>{const v=document.querySelector('#lbVideo');return {src:v.currentSrc||v.src,vw:v.videoWidth,vh:v.videoHeight,rs:v.readyState,open:!document.querySelector('#lb').hidden}})()")
        row["lightbox"]=lb
        await pg.screenshot(path=f"{OUT}/{eng}-{w}-lightbox-p02.jpg", type="jpeg", quality=80)
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(300)
        row["links"]=await pg.evaluate("""(()=>{const bad=[];document.querySelectorAll('a[href]').forEach(a=>{const h=a.getAttribute('href');if(h.startsWith('#')&&h.length>1&&!document.querySelector(h))bad.push(h);if(h===''||h==='#')bad.push('empty:'+a.textContent.trim().slice(0,30))});
          const call=document.querySelector('[data-call]');return {bad, call: call?call.textContent.trim()+' | '+(call.getAttribute('href')||''):null, wa:[...document.querySelectorAll('a[href*="wa.me"]')].length}})()""")
        if w in (375,1440):
          for sec in ["#turnkey","#contact"]:
            el=await pg.query_selector(sec); await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
            await el.screenshot(path=f"{OUT}/{eng}-{w}-{sec[1:]}.jpg", type="jpeg", quality=78)
        row["errors"]=errs[:3]
        res.append(row); print(json.dumps(row),flush=True)
        await ctx.close()
      await br.close()
asyncio.run(run())
