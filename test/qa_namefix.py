
import asyncio, json, sys, re, datetime
from playwright.async_api import async_playwright
BASE="https://ridham-interiors-e1eb3b.sites.tab.bot"
CFG=json.load(open("/home/user/tab/state/ridham-private/config.json"))
OUT="/home/user/tab/files/ridham-site/qa/name-fix"
OVF="""(()=>{const W=document.documentElement.clientWidth;return [...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return r.width>0&&r.right>W+1&&cs.position!=='fixed'&&cs.visibility!=='hidden'}).slice(0,5).map(e=>(e.className||e.tagName)+':'+Math.round(e.getBoundingClientRect().right))})()"""
async def run():
  rep=[]
  async with async_playwright() as p:
    for eng,w,h in [("webkit",375,812),("chromium",1440,900)]:
      br=await getattr(p,eng).launch()
      ctx=await br.new_context(viewport={"width":w,"height":h},device_scale_factor=2 if w<1024 else 1,has_touch=w<768)
      r=await ctx.request.post(BASE+"/login",form={"u":CFG["username"],"p":CFG["password"],"next":"/?preview=1"},max_redirects=0)
      row={"eng":eng,"w":w,"login":r.status,"errs":[]}
      pg=await ctx.new_page(); pg.on("pageerror",lambda e,row=row: row["errs"].append(str(e)))
      # html greps
      for path in ["/","/?preview=1","/assets/js/config.js","/assets/js/main.js","/assets/css/styles.css"]:
        t=await (await ctx.request.get(BASE+path)).text()
        row["grep "+path]={"interiors":len(re.findall(r"interiors",t,re.I)),"brand":t.count("Ridham Patel Interior Designer"),"ctx":re.findall(r".{0,30}interiors.{0,20}",t,re.I)[:3]}
      tag=f"{eng}-{w}"
      lp=await ctx.new_page(); await lp.goto(BASE+"/login",wait_until="networkidle"); await lp.screenshot(path=f"{OUT}/{tag}-login.png")
      row["login_html_brand"]=(await lp.content()).count("Ridham Patel Interior Designer"); await lp.close()
      # paused cover
      await pg.goto(BASE+"/",wait_until="networkidle",timeout=60000); await pg.wait_for_timeout(2500)
      row["cover_ovf"]=await pg.evaluate(OVF)
      await pg.screenshot(path=f"{OUT}/{tag}-cover-paused.png")
      # countdown + reveal
      t0=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=14)).isoformat(timespec="seconds").replace("+00:00","Z")
      await pg.goto(BASE+"/?launch="+t0,wait_until="domcontentloaded",timeout=60000); await pg.wait_for_timeout(4000)
      row["cd_ovf"]=await pg.evaluate(OVF)
      await pg.screenshot(path=f"{OUT}/{tag}-countdown.png")
      start=datetime.datetime.fromisoformat(t0.replace("Z","+00:00"))
      while datetime.datetime.now(datetime.timezone.utc)<start: await pg.wait_for_timeout(200)
      for i,dt in enumerate([1500,1500,1200,1200,1500]):
        await pg.wait_for_timeout(dt); await pg.screenshot(path=f"{OUT}/{tag}-reveal-{i}.png")
      await pg.wait_for_timeout(5000)
      row["after_url"]=pg.url; await pg.screenshot(path=f"{OUT}/{tag}-after-reveal.png")
      # full site header + footer
      await pg.goto(BASE+"/?preview=1",wait_until="networkidle",timeout=60000); await pg.wait_for_timeout(1200)
      row["title"]=await pg.title(); row["site_ovf"]=await pg.evaluate(OVF)
      await pg.screenshot(path=f"{OUT}/{tag}-header.png")
      row["header_sub"]=await pg.evaluate("(()=>{const e=document.querySelector('.brand__sub');const r=e.getBoundingClientRect();return [e.textContent,Math.round(r.right),document.documentElement.clientWidth]})()")
      await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in'))")
      await pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); await pg.wait_for_timeout(1200)
      await pg.screenshot(path=f"{OUT}/{tag}-footer.png")
      row["footer"]=await pg.evaluate("document.querySelector('footer')?document.querySelector('footer').innerText.slice(0,300):''")
      rep.append(row); await br.close()
  print(json.dumps(rep,indent=1,ensure_ascii=False))
asyncio.run(run())
