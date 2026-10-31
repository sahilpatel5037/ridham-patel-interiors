
import asyncio, json
from playwright.async_api import async_playwright
BASE="https://ridham-interiors-e1eb3b.sites.tab.bot"; CFG=json.load(open("/home/user/tab/state/ridham-private/config.json")); OUT="/home/user/tab/files/ridham-site/qa/name-fix"
async def run():
  res=[]
  async with async_playwright() as p:
    for eng,w,h in [("webkit",375,812),("chromium",1440,900)]:
      br=await getattr(p,eng).launch(); ctx=await br.new_context(viewport={"width":w,"height":h},device_scale_factor=2 if w<1024 else 1)
      pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
      await pg.goto(BASE+"/?preview=1",wait_until="networkidle")  # not logged in -> login page
      html=await pg.content(); await pg.screenshot(path=f"{OUT}/{eng}-{w}-login.png")
      await pg.fill("#u",CFG["username"]); await pg.fill("#p",CFG["password"])
      await pg.click("button"); await pg.wait_for_load_state("networkidle")
      ok=await pg.evaluate("!!document.querySelector('.brand__mark .r')")
      fav=await (await ctx.request.get(BASE+"/favicon.svg?v=2")).text()
      await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in'))")
      await pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); await pg.wait_for_timeout(1200)
      await pg.screenshot(path=f"{OUT}/{eng}-{w}-footer.png")
      res.append({"eng":eng,"login_brand":html.count("Ridham Patel Interior Designer"),"login_interiors":html.lower().count("interiors"),"signed_in_site":ok,"url":pg.url,"fav_arch":"A" in fav and "<path" in fav,"errs":errs})
      await br.close()
  print(json.dumps(res))
asyncio.run(run())