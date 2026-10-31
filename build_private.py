#!/usr/bin/env python3
"""Build + publish the PRIVATE preview of Ridham's site (login-gated).
Source of truth: /home/user/tab/files/ridham-site/site/ (pure static, Vercel-ready).
- Every page/asset (except the .mp4 videos) is packed INSIDE the Worker and served only after login.
- Videos are served from the unlisted media hosts in config (media_slugs), so config.js gets MEDIA_URLS for the preview build.
- Login secrets live in /home/user/tab/state/ridham-private/config.json (never in the site folder; only a salted hash ships).
Usage: TAB_TASK_ID=<id> python3 build_private.py [--no-publish]"""
import base64, json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SITE, OUT = HERE + "/site", HERE + "/publish/main"
CFG = json.load(open("/home/user/tab/state/ridham-private/config.json"))
GROUPS = {"m1": ["p01", "p02"], "m2": ["p03", "p04"], "m3": ["p05", "p06"], "m4": ["p07", "p08"], "m5": ["p09", "p10"], "m6": ["p11"]}
CT = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".svg": "image/svg+xml",
      ".jpg": "image/jpeg", ".png": "image/png", ".woff2": "font/woff2", ".txt": "text/plain; charset=utf-8", ".json": "application/json"}
MEDIA_VER = "a2"  # bump when the clips change (31 Oct: clips now carry sound) so phones don't replay a cached old copy
# 31 Oct fix pass: p04 replaced (old reel had room-label text), p05 re-cut (no client nameplate), p07 cropped (no "In process" text), p09-p11 new -> v=a3 (m3/m4/m5/m6 republished)
# 31 Oct fix pass 2: P Square logo cropped out of p01-p05, p09-p11 (new 4:5 cuts, 540x676) -> v=a4 (m1/m2/m3/m5/m6 republished)
MEDIA_VER_FILE = {"p01": "a4", "p02": "a4", "p03": "a4", "p04": "a4", "p05": "a4", "p07": "a3", "p09": "a4", "p10": "a4", "p11": "a4"}
media_urls = {f"{p}.mp4": f"https://{CFG['media_slugs'][g]}.sites.tab.bot/{p}.mp4?v={MEDIA_VER_FILE.get(p, MEDIA_VER)}" for g, ps in GROUPS.items() for p in ps}
files = {}
for root, _, fs in os.walk(SITE):
    for f in fs:
        full = os.path.join(root, f); rel = os.path.relpath(full, SITE).replace(os.sep, "/")
        ext = os.path.splitext(f)[1].lower()
        if ext == ".mp4" or rel in ("vercel.json",): continue
        ct = CT.get(ext, "application/octet-stream")
        if ext in (".html", ".css", ".js", ".svg", ".txt", ".json"):
            body = open(full, encoding="utf-8").read()
            if rel == "assets/js/config.js":
                body, n = re.subn(r'MEDIA_URLS:\s*\{\}', "MEDIA_URLS: " + json.dumps(media_urls), body); assert n == 1, "config.js MEDIA_URLS line not found"
            files[rel] = [ct, body, False]
        else:
            files[rel] = [ct, base64.b64encode(open(full, "rb").read()).decode(), True]
cfg_js = open(SITE + "/assets/js/config.js", encoding="utf-8").read()
def cfgv(k):
    m = re.search(r'\b' + k + r':\s*"([^"]*)"', cfg_js); return m.group(1) if m else ""
# Launch switch (countdown pass, 31 Oct): LAUNCH_AT is the one line. null -> "Launching soon · After Diwali" (no numbers);
# a date -> live countdown, at zero the cinematic reveal plays and the server opens the full site. COUNTDOWN_MODE "live" opens it now.
LAUNCH = cfgv("LAUNCH_AT")
from datetime import datetime
if LAUNCH:
    datetime.fromisoformat(LAUNCH)  # raises if the date is not like 2026-11-15T10:00:00+05:30
    assert re.search(r"[+-]\d\d:\d\d$|Z$", LAUNCH), "LAUNCH_AT needs a time zone, e.g. +05:30"
MODE = (cfgv("COUNTDOWN_MODE") or "auto").lower()
MODE = {"off": "live"}.get(MODE, MODE)
if MODE in ("auto", "countdown"): MODE = "countdown" if LAUNCH else "paused"
assert MODE in ("paused", "countdown", "live"), "COUNTDOWN_MODE must be auto / paused / live"
mn = re.search(r'\bLAUNCH_NOTE:\s*"((?:[^"\\]|\\.)*)"', cfg_js)
NOTE = json.loads('"' + mn.group(1) + '"') if mn else ""
BGHOST = "https://" + CFG["media_slugs"]["m7"] + ".sites.tab.bot"
BG_VER = "b1"  # bump when the launch-screen loop changes
tel = "tel:" + "+" + re.sub(r"\D", "", cfgv("CALL_NUMBER")) if re.sub(r"\D", "", cfgv("CALL_NUMBER")) else "#"
from urllib.parse import quote
wa = "https://wa.me/" + re.sub(r"\D", "", cfgv("WHATSAPP_NUMBER")) + "?text=" + quote(cfgv("WHATSAPP_TEXT"))
cover = open(HERE + "/cover_template.html", encoding="utf-8").read().replace("%TEL%", tel).replace("%WA%", wa).replace("%MODE%", json.dumps(MODE)).replace("%LAUNCH%", json.dumps(LAUNCH)).replace("%NOTE%", json.dumps(NOTE, ensure_ascii=False)).replace("%BGHOST%", BGHOST).replace("%BGV%", BGHOST + "/bg.mp4?v=" + BG_VER).replace("%BGP%", BGHOST + "/bg.jpg?v=" + BG_VER)
assert "%" + "TEL%" not in cover and "%NOTE%" not in cover and "%BGV%" not in cover
print("launch switch: mode=%s launch_at=%s note=%r" % (MODE, LAUNCH or "-", NOTE[:60]))
login = open(HERE + "/login_template.html", encoding="utf-8").read().replace("%BRAND%", "Ridham Patel Interior Designer")
vals = {"USER": json.dumps(CFG["username"]), "PH": json.dumps(CFG["pw_hash"]), "SECRET": json.dumps(CFG["session_secret"]),
        "SALT": json.dumps(CFG["salt"]), "LOGIN": json.dumps(login), "MODE": json.dumps(MODE), "LAUNCH": json.dumps(LAUNCH), "COVER": json.dumps(cover), "FILES": json.dumps(files, ensure_ascii=False)}
gate = re.sub(r"%(USER|PH|SECRET|SALT|LOGIN|MODE|LAUNCH|COVER|FILES)%", lambda m: vals[m.group(1)], open(HERE + "/gate_template.js", encoding="utf-8").read())
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
open(OUT + "/_worker.js", "w", encoding="utf-8").write(gate)
open(OUT + "/robots.txt", "w").write("User-agent: *\nDisallow: /\n")
json.dump({"kind": "worker", "entry": "_worker.js"}, open(OUT + "/tab-site.json", "w"))
total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print("built: %d files packed, worker %d KB, folder %d bytes" % (len(files), os.path.getsize(OUT + "/_worker.js") // 1024, total))
assert total < 880000, "publish folder over ~880 KB: multi-slice publishes have failed before; shrink posters"
if "--no-publish" in sys.argv: sys.exit(0)
r = subprocess.run(["timeout", "-k", "5", "600", "node", "/home/user/tab/publish-cli.mjs", "site.publish",
                    json.dumps({"slug": CFG["slug"], "source_dir": OUT, "title": "Ridham Patel Interior Designer (private preview)"})], capture_output=True, text=True)
s = r.stdout
try: res = json.loads(s[s.find("{"):]); rr = res.get("result", res)
except Exception: res, rr = {"ok": False}, {"error": (s + r.stderr)[-800:]}
print(json.dumps({"ok": res.get("ok"), **{k: rr.get(k) for k in ("status", "url", "error", "unchanged")}}, ensure_ascii=False))
if not res.get("ok"): print(s[:2000]); sys.exit(1)
