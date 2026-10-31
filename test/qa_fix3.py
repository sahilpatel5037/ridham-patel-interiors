
import asyncio, json, sys
from playwright.async_api import async_playwright
BASE="https://ridham-interiors-e1eb3b.sites.tab.bot"
CFG=json.load(open("/home/user/tab/state/ridham-private/config.json"))
OUT=sys.argv[1]; WIDTHS=[int(x) for x in sys.argv[2].split(",")]; ENGINES=sys.argv[3].split(",")
async def run():
  res=[]
  async with async_playwright() as p:
    for eng in ENGINES:
      br=await getattr(p,eng).launch()
      for w in WIDTHS:
        mobile = w<768
        ctx=await br.new_context(viewport={"width":w,"height":860 if w<1024 else 900}, device_scale_factor=2 if w<1024 else 1, is_mobile=(mobile and eng=="chromium"), has_touch=mobile)
        r=await ctx.request.post(BASE+"/login", form={"u":CFG["username"],"p":CFG["password"],"next":"/?preview=1"}, max_redirects=0)
        pg=await ctx.new_page()
        await pg.goto(BASE+"/?preview=1", wait_until="networkidle", timeout=60000)
        await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in'))")
        await pg.add_style_tag(content=".js .reveal{transition:none!important}")
        await pg.wait_for_timeout(600)
        sw=await pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        # check heading lines of 'on site'
        em=await pg.evaluate("(()=>{const e=document.querySelector('#about h2 em');const r=e.getClientRects();return r.length})()")
        gridinfo=await pg.evaluate("""(()=>{const g=document.querySelector('#grid');const cs=[...g.querySelectorAll('.card')].map(c=>c.getBoundingClientRect());
           const cols=getComputedStyle(g).gridTemplateColumns.split(' ').length; const rows={};cs.forEach(r=>{const k=Math.round(r.top);rows[k]=(rows[k]||0)+r.width});
           const gw=g.getBoundingClientRect().width; return {cols, rows:Object.values(rows).map(v=>Math.round(v/gw*100))}})()""")
        for sec,sel in [("about","#about"),("projects","#work"),("howiwork","#process")]:
          el=await pg.query_selector(sel)
          await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
          await pg.evaluate("document.querySelectorAll('.card__media video').forEach(v=>{v.pause();v.style.opacity=0})")
          path=f"{OUT}/{eng}-{w}-{sec}.png"
          await el.screenshot(path=path)
        res.append({"eng":eng,"w":w,"login":r.status,"scroll":sw,"onsite_lines":em,"grid":gridinfo})
        print(json.dumps(res[-1]),flush=True)
        await ctx.close()
      await br.close()
asyncio.run(run())
