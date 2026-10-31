
import asyncio, json, datetime
from playwright.async_api import async_playwright
BASE="https://ridham-interiors-e1eb3b.sites.tab.bot"
CFG=json.load(open("/home/user/tab/state/ridham-private/config.json"))
OUT="/home/user/tab/files/ridham-site/qa/logo-v2"
OVF="""(()=>{const W=document.documentElement.clientWidth;return [...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return r.width>0&&r.right>W+1&&cs.position!=='fixed'&&cs.visibility!=='hidden'}).slice(0,5).map(e=>(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||e.tagName)+':'+Math.round(e.getBoundingClientRect().right))})()"""
async def run():
  rep=[]
  async with async_playwright() as p:
    for eng,w,h in [("webkit",375,812),("chromium",1440,900)]:
      br=await getattr(p,eng).launch()
      ctx=await br.new_context(viewport={"width":w,"height":h},device_scale_factor=2 if w<1024 else 1,has_touch=w<768)
      tag=f"{eng}-{w}"; row={"eng":eng,"w":w,"errs":[],"console":[]}
      # login page (signed out)
      lp=await ctx.new_page(); await lp.goto(BASE+"/login",wait_until="networkidle"); await lp.wait_for_timeout(500)
      row["login_has_mark"]=await lp.evaluate("!!document.querySelector('svg.lm.rp2')"); await lp.screenshot(path=f"{OUT}/{tag}-login.png"); await lp.close()
      r=await ctx.request.post(BASE+"/login",form={"u":CFG["username"],"p":CFG["password"],"next":"/?preview=1"},max_redirects=0)
      row["login_status"]=r.status
      pg=await ctx.new_page(); pg.on("pageerror",lambda e,row=row: row["errs"].append(str(e)))
      pg.on("console",lambda m,row=row: row["console"].append(m.text) if m.type=="error" else None)
      # countdown screen (paused "launching soon") + a numbers countdown
      await pg.goto(BASE+"/",wait_until="networkidle",timeout=60000); await pg.wait_for_timeout(2800)
      row["cd_mark"]=await pg.evaluate("(()=>{const e=document.querySelector('svg.mark.rp2');if(!e)return null;const r=e.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height)]})()")
      row["cd_ovf"]=await pg.evaluate(OVF); await pg.screenshot(path=f"{OUT}/{tag}-countdown.png")
      t0=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(days=15,hours=3)).isoformat(timespec="seconds").replace("+00:00","Z")
      await pg.goto(BASE+"/?launch="+t0,wait_until="domcontentloaded",timeout=60000); await pg.wait_for_timeout(3500)
      await pg.screenshot(path=f"{OUT}/{tag}-countdown-numbers.png")
      # full site header + in-site cover check + footer
      await pg.goto(BASE+"/?preview=1",wait_until="networkidle",timeout=60000); await pg.wait_for_timeout(1500)
      row["site_ovf"]=await pg.evaluate(OVF)
      row["head"]=await pg.evaluate("(()=>{const m=document.querySelector('.brand__mark').getBoundingClientRect(),n=document.querySelector('.brand__name').getBoundingClientRect(),c=document.querySelector('.nav__call'),cr=c?c.getBoundingClientRect():null;return {mark:[Math.round(m.width)],nameRight:Math.round(n.right),callLeft:cr&&cr.width?Math.round(cr.left):null,favicon:document.querySelector('link[rel=icon]').getAttribute('href')}})()")
      await pg.screenshot(path=f"{OUT}/{tag}-header.png")
      await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in'))")
      await pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); await pg.wait_for_timeout(1300)
      await pg.screenshot(path=f"{OUT}/{tag}-footer.png")
      row["fav"]=[(await ctx.request.get(BASE+u)).status for u in ["/favicon.svg?v=3","/apple-touch-icon.png?v=3"]]
      row["incover_mark"]=await pg.evaluate("!!document.querySelector('svg.cover__mark.rp2')")
      rep.append(row); await br.close()
  print(json.dumps(rep,indent=1))
asyncio.run(run())
