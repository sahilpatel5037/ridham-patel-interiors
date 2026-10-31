
import sys, json, asyncio, os
from playwright.async_api import async_playwright
# jobs: [{"svg": path, "png": path, "w": px, "bg": css or null}]
async def main(jobs):
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--no-sandbox"])
        pg = await b.new_page(device_scale_factor=1)
        for j in jobs:
            s = open(j["svg"]).read()
            vb = [float(x) for x in s.split('viewBox="')[1].split('"')[0].split()]
            w = j["w"]; h = round(w * vb[3] / vb[2])
            bg = j.get("bg") or "transparent"
            await pg.set_viewport_size({"width": w, "height": h})
            s2 = s.replace("<svg ", '<svg width="%d" height="%d" ' % (w, h), 1)
            await pg.set_content('<html><body style="margin:0;background:%s">%s</body></html>' % (bg, s2))
            await pg.screenshot(path=j["png"], omit_background=(bg == "transparent"), clip={"x":0,"y":0,"width":w,"height":h})
        await b.close()
asyncio.run(main(json.load(open(sys.argv[1]))))
