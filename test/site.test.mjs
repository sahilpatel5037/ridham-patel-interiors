import test from "node:test"; import assert from "node:assert"; import fs from "node:fs"; import path from "node:path";
const SITE = new URL("../site/", import.meta.url).pathname; const html = fs.readFileSync(SITE + "index.html", "utf8");
test("title, viewport, noindex", () => { assert.match(html, /<title>[^<]*Ridham Patel[^<]*Gandhinagar/); assert.match(html, /name="viewport"/); assert.match(html, /name="robots" content="noindex/); });
test("all sections present", () => { for (const id of ["top","work","about","services","process","area","contact"]) assert.ok(html.includes(`id="${id}"`), id);
  for (const a of ["Sargasan","Kudasan","Raysan","Randesan","Koba","sectors"]) assert.ok(html.includes(a), a);
  for (const s of ["Consultation","Design &amp; 3D views","Execution on site","Handover"]) assert.ok(html.includes(`<h3>${s}</h3>`), s);
  assert.ok(!/tanki/i.test(html)); assert.ok(html.includes('id="turnkey"') && html.includes("data-call")); assert.ok(html.includes("Projects by P&nbsp;Square Interior Studio")); });
test("local assets exist", () => { const refs = [...html.matchAll(/(?:src|href)="([^"#:]+)"/g)].map(m => m[1].split("?")[0]).filter(r => !r.startsWith("http"));
  for (const r of refs) assert.ok(fs.existsSync(path.join(SITE, r)), "missing " + r);
  for (const m of html.matchAll(/data-video="([^"]+)"/g)) assert.ok(fs.existsSync(SITE + "media/" + m[1]), "video " + m[1]); });
test("media within budget", () => { for (const f of fs.readdirSync(SITE + "media")) if (f.endsWith(".mp4")) assert.ok(fs.statSync(SITE + "media/" + f).size < 850 * 1024, f);
  for (const f of fs.readdirSync(SITE + "media/posters")) assert.ok(fs.statSync(SITE + "media/posters/" + f).size < 120 * 1024, f); });
test("no embeds, no phone number, no AI wording, no secrets", () => { const all = html + fs.readFileSync(SITE + "assets/js/main.js", "utf8") + fs.readFileSync(SITE + "assets/js/config.js", "utf8");
  assert.ok(!/<iframe|instagram\.com\/(p|reel)\/|youtube\.com/i.test(all)); assert.ok(!/\b\d{10}\b/.test(all.replace(/data-[a-z]+="[^"]*"/g, "")));
  assert.ok(!/\bAI\b|artificial intelligence/i.test(html)); assert.ok(!/password|pw_hash|session_secret/i.test(all)); });
test("config has the editable switches", () => { const c = fs.readFileSync(SITE + "assets/js/config.js", "utf8");
  for (const k of ["BRAND","WHATSAPP_NUMBER","INSTAGRAM_URL","MEDIA_BASE","MEDIA_URLS","COUNTDOWN_MODE","LAUNCH_AT","CALL_NUMBER"]) assert.ok(c.includes(k + ":"), k);
  assert.match(c, /COUNTDOWN_MODE:\s*"auto"/); assert.match(c, /LAUNCH_AT:\s*null,/); assert.ok(c.includes("LAUNCH_NOTE:")); }); /* countdown pass 31 Oct: date not decided yet -> null */
test("topbar: monogram, call pill, full-screen menu, nav to sections", () => { assert.ok(/class="brand__mark( rp2)?"/.test(html) && html.includes("brand__sub"));
  assert.ok(html.includes('class="nav__call"') && html.includes('class="nav__turnkey"') && html.includes('id="menu"') && html.includes("data-tel"));
  for (const id of ["work","turnkey","about","services","contact"]) assert.ok(html.includes(`data-sec="${id}"`), id); assert.ok(html.includes('id="lbSnd"')); });
test("launch switch is one of auto / paused / live, LAUNCH_AT is null or an IST-style date", () => { const c = fs.readFileSync(SITE + "assets/js/config.js", "utf8"); assert.match(c, /COUNTDOWN_MODE:\s*"(auto|paused|countdown|live)"/); assert.match(c, /LAUNCH_AT:\s*(null|"\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d)?([+-]\d\d:\d\d|Z)")/); });
test("polish 31 Oct: no weak experience claim, 3 hero facts, equal hero buttons, grid crops watermark", () => { const css = fs.readFileSync(SITE + "assets/css/styles.css", "utf8");
  assert.ok(!/1\+\s*year|more than a year/i.test(html)); assert.strictEqual((html.match(/<ul class="hero__facts[\s\S]*?<\/ul>/)[0].match(/<li>/g) || []).length, 3);
  assert.match(css, /\.hero__cta\{display:grid;grid-template-columns:1fr 1fr/); assert.ok(!html.includes("aspect-ratio:9 / 16")); assert.match(css, /object-position:50% 15%/); });
test("fix pass 31 Oct: even grid, distinct descriptors, About wording, no-wrap on site, CTA", () => {
  const grid = html.match(/<div class="grid" id="grid">([\s\S]*?)<a class="nextcard/)[1];
  const cards = grid.match(/<article class="card(?! card--more)[^"]*"/g); const wide = (grid.match(/card--wide/g) || []).length;
  assert.strictEqual(cards.length, 11); assert.strictEqual(wide, 1);
  const cells = cards.length - wide + 2 * wide; assert.strictEqual(cells % 6, 0, "grid must fill 2 and 3 columns evenly");
  const srcs = [...grid.matchAll(/<p class="card__src">([^<]+)<\/p>/g)].map(m => m[1]); assert.strictEqual(new Set(srcs).size, srcs.length, "descriptors must differ");
  assert.ok(!srcs.some(s => /Project work with/.test(s)));
  assert.ok(html.includes("alongside Parth Patel, who brings nine years")); assert.strictEqual((html.match(/Parth/g) || []).length, 1);
  assert.ok(!/Gandhinagar<\/span> only|work in Gandhinagar only|Only in/i.test(html));
  assert.ok(html.includes('<em class="nowrap">on&nbsp;site</em>'));
  assert.ok(html.includes("Your space could be next")); assert.ok(html.includes('<p class="eyebrow reveal">How I work</p>'));
  assert.ok(!html.includes(">Free consultation</a>")); });

const js = fs.readFileSync(SITE + "assets/js/main.js", "utf8"), css2 = fs.readFileSync(SITE + "assets/css/styles.css", "utf8");
test("fix pass 2 (31 Oct): filter views end even, logo-free 4:5 clips, cache-buster a4", () => {
  assert.ok(html.includes('id="moreCard" hidden'), "filler tile present and hidden by default (All view)");
  assert.ok(/data-showall/.test(html));
  assert.match(js, /function fillGap\(\)/); assert.match(js, /\(cols-cells%cols\)%cols/);
  assert.match(css2, /\.card--more\[hidden\]\{display:none!important\}/);
  const b = fs.readFileSync(new URL("../build_private.py", import.meta.url), "utf8");
  for (const p of ["p01","p02","p03","p04","p05","p09","p10","p11"]) { assert.ok(b.includes(`"${p}": "a4"`), p + " cache-buster"); assert.ok(html.includes(`posters/${p}.jpg" alt=`)); }
  assert.ok(!/@[a-z0-9_.]{3,}/i.test(html.replace(/[\w.+-]+@[\w.-]+/g,"")), "no social handles on the page");
  assert.ok(!/posters\/p0[1-59]\.jpg"[^>]*height="768"/.test(html), "re-cut posters are 4:5");
});

test("countdown pass (31 Oct): launch screen template, reveal hand-off, site curtains", () => {
  const cov = fs.readFileSync(new URL("../cover_template.html", import.meta.url), "utf8");
  for (const k of ["data-rp-cover", "%MODE%", "%LAUNCH%", "%NOTE%", "%BGV%", "%BGP%", 'id="timer"', 'id="soon"', "c-top", "c-bot", "rp_reveal", 'q.get("launch")', "/?preview=1"]) assert.ok(cov.includes(k), k);
  assert.ok(!/Monarch|M&amp;M|Fiverr/.test(cov), "no Monarch & Mark text on Ridham's screen");
  const html = fs.readFileSync(SITE + "index.html", "utf8"), css = fs.readFileSync(SITE + "assets/css/styles.css", "utf8"), js = fs.readFileSync(SITE + "assets/js/main.js", "utf8");
  assert.ok(html.includes('id="rv"') && html.includes("rp_reveal") && html.includes("rp-reveal"));
  assert.ok(css.includes(".rp-reveal .rv") && css.includes("@keyframes rvTop"));
  assert.ok(js.includes('q("#rv")'));
  const b = fs.readFileSync(new URL("../build_private.py", import.meta.url), "utf8");
  assert.ok(b.includes('"countdown" if LAUNCH else "paused"') && b.includes("%BGV%"));
});

test("logo v2 (31 Oct): R+P ring monogram in header, footer, cover; favicon + countdown + login carry it", () => {
  for (const c of ["brand__mark","foot__mark","cover__mark"]) assert.ok(html.includes(`class="${c} rp2"`), c);
  assert.ok(!html.includes('A60.0 60.0 0 0 1 148.0'), "old arch path gone from the site");
  const cd = fs.readFileSync(new URL("../cover_template.html", import.meta.url), "utf8"), lg = fs.readFileSync(new URL("../login_template.html", import.meta.url), "utf8");
  assert.ok(cd.includes('class="mark rp2"') && lg.includes('class="lm rp2"'));
  assert.ok(!cd.includes('A60.0 60.0 0 0 1 148.0') && !lg.includes('A60.0 60.0 0 0 1 148.0'));
  const fav = fs.readFileSync(SITE + "favicon.svg", "utf8"); assert.ok(fav.includes("linearGradient") && !fav.includes("A60.0"));
  assert.ok(html.includes("favicon.svg?v=3") && html.includes("apple-touch-icon.png?v=3"));
});
