#!/usr/bin/env python3
"""Build launch/ = the PUBLIC countdown-only page that Vercel serves (vercel.json at the repo root: outputDirectory "launch").
Nothing of the full site goes into launch/: only the countdown page, its fonts, icons and the background loop.
Settings come from site/assets/js/config.js (LAUNCH_AT, LAUNCH_NOTE, CALL_NUMBER, WHATSAPP_*). LAUNCH_AT null = "Launching soon" (no numbers).
With a date set, the page counts down and at zero plays the reveal, then reloads; to open the full site on Vercel at launch
change vercel.json outputDirectory from "launch" to "site" (README: "Launch day").
Usage: python3 build_launch.py"""
import json, os, re, shutil
from urllib.parse import quote
HERE = os.path.dirname(os.path.abspath(__file__)); SITE = HERE + "/site"; OUT = HERE + "/launch"
cfg_js = open(SITE + "/assets/js/config.js", encoding="utf-8").read()
def cfgv(k):
    m = re.search(r'\b' + k + r':\s*"([^"]*)"', cfg_js); return m.group(1) if m else ""
LAUNCH = cfgv("LAUNCH_AT")
MODE = "countdown" if LAUNCH else "paused"
mn = re.search(r'\bLAUNCH_NOTE:\s*"((?:[^"\\]|\\.)*)"', cfg_js)
NOTE = json.loads('"' + mn.group(1) + '"') if mn else ""
digits = re.sub(r"\D", "", cfgv("CALL_NUMBER"))
tel = "tel:+" + digits if digits else "#"
wa = "https://wa.me/" + re.sub(r"\D", "", cfgv("WHATSAPP_NUMBER")) + "?text=" + quote(cfgv("WHATSAPP_TEXT"))
html = open(HERE + "/cover_template.html", encoding="utf-8").read()
html = (html.replace("%TEL%", tel).replace("%WA%", wa).replace("%MODE%", json.dumps(MODE)).replace("%LAUNCH%", json.dumps(LAUNCH or None))
        .replace("%NOTE%", json.dumps(NOTE, ensure_ascii=False)).replace('<link rel="preconnect" href="%BGHOST%">\n', "")
        .replace("%BGHOST%", "").replace("%BGV%", "/bg.mp4?v=b1").replace("%BGP%", "/bg.jpg?v=b1"))
# public build: no ?launch= test mode, and at zero it reloads "/" (which is the full site only once Vercel serves site/)
html, n1 = re.subn(r'var test=q\.get\("launch"\)', 'var test=null', html)
html, n2 = re.subn(r'if\(test\)return Promise\.resolve\("/\?preview=1"\);', '', html)
assert n1 == 1 and n2 == 1, "cover_template changed: update build_launch.py"
html = re.sub(r"/\*[^*]*preview[^*]*\*/\n?", "", html)  # drop comments that mention the private preview
assert not re.search(r"%(TEL|WA|MODE|LAUNCH|NOTE|BGHOST|BGV|BGP)%", html) and "preview" not in html, "placeholder or preview reference left"
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT + "/assets/fonts")
open(OUT + "/index.html", "w", encoding="utf-8").write(html)
for f in ("CormorantGaramond-normal-500.woff2", "CormorantGaramond-italic-500.woff2", "Manrope-normal-400-700.woff2"):
    shutil.copy(SITE + "/assets/fonts/" + f, OUT + "/assets/fonts/" + f)
for f in ("favicon.svg", "apple-touch-icon.png"): shutil.copy(SITE + "/" + f, OUT + "/" + f)
for f in ("bg.mp4", "bg.jpg"): shutil.copy(HERE + "/launch-media/" + f, OUT + "/" + f)
open(OUT + "/robots.txt", "w").write("User-agent: *\nDisallow: /\n")
open(OUT + "/404.html", "w", encoding="utf-8").write('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=/"><title>Ridham Patel Interior Designer</title><a href="/">Ridham Patel Interior Designer</a>')
print("launch/ built: mode=%s launch_at=%s files=%d" % (MODE, LAUNCH or "-", sum(len(f) for _, _, f in os.walk(OUT))))
