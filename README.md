# Ridham Patel Interior Designer — portfolio site (PRIVATE preview)

Built 31 Oct 2026 for Sahil (in charge of the project). Ridham's cousin site: interior designer, Gandhinagar.

## Folders
- `site/` — the real website, pure static (index.html, assets/, media/). Vercel-ready: deploy this folder as-is.
  - `site/assets/js/config.js` — THE one settings file (brand name, WhatsApp number, turnkey call number, Instagram link, media location, countdown).
  - `site/media/*.mp4` — 8 project clips (540x960 / 720x480, muted loops, ~400 KB each); `site/media/posters/*.jpg` — poster frames.
  - `site/vercel.json` — noindex header for every page (delete the `X-Robots-Tag` block when going public).
- `build_private.py` — builds + publishes the PRIVATE preview (login gate). Run: `TAB_TASK_ID=<id> python3 build_private.py`.
- `gate_template.js`, `login_template.html` — the login gate (everything packed inside the Worker; nothing served before login).
- `media_worker.js` — the small server on the 4 unlisted video hosts (adds byte-range support so iPhone Safari plays the videos).
- `publish/` — generated publish folders (main + m1..m4). `media-src/` — original downloads (yt-dlp) + metadata.
- `test/site.test.mjs` — `node --test test/site.test.mjs`.
- Login secrets: `/home/user/tab/state/ridham-private/config.json` (NOT in this folder; only a salted hash ships).

## 31 Oct update: topbar, public cover, clips with sound
- TOPBAR: gold "RP" monogram + "Ridham Patel / INTERIORS · GANDHINAGAR"; transparent over the hero, dark glass bar (blur, ~85% charcoal) with a gold hairline after scrolling; 64px phone / 76px desktop. Phone + iPad (<1024px): gold "Call" pill + 2-line burger -> full-screen menu (Projects, Turnkey, About, Services, Contact + Call / WhatsApp; Esc / link tap closes; page scroll locked). Desktop (>=1024px): links centered with gold underline + active-section highlight, "Call for Turnkey" outline button. Call buttons use `data-tel` (CALL_NUMBER). Old files kept in `backup-pre-topbar/`.
- LAUNCH SWITCH (one spot: `COUNTDOWN_MODE` + `LAUNCH_AT` in site/assets/js/config.js): "paused" (now — "Launching soon", no timer), "countdown" (live timer to LAUNCH_AT, then opens by itself), "live" (site open). LAUNCH_AT "2026-11-15T10:00:00+05:30" is a PLACEHOLDER. After editing, re-run build_private.py.
- PRIVATE BUILD routing (gate_template.js): the main URL `/` is PUBLIC and shows only `cover_template.html` (RP mark, Call + WhatsApp, gold animated background; no portfolio content, no media). Everything else (/?preview=1, /preview, every asset) needs the login. In "countdown" mode the worker itself starts serving the full site to everyone at LAUNCH_AT — no rebuild needed. In "live" mode it is open to everyone.
- CLIPS WITH SOUND: the 8 reels were re-downloaded with audio (media-src/audio/), cut at the same points (offsets p01 1.0s, p02 0.5, p03 0.5, p04 0.3, p05 3.0, p06 0.2 + crop y=600, p07 0, p08 0), H.264 + AAC 48k mono, ~400-420 KB each (media-src/av-build/), re-hosted on m1..m4. Old silent copies in media-src/video-only-backup/. Grid previews stay muted; the lightbox starts muted with a "Tap for sound" button. Clip URLs carry `?v=a2` (MEDIA_VER in build_private.py) so phones don't replay a cached silent copy — bump it when clips change.

## 31 Oct polish (surprise for Ridham — never contact him)
- Hero facts: "1+ year" removed. Now 3 non-numeric facts: "Design → Build — concept, 3D views & site execution" / "Homes · Offices — residential, commercial & turnkey" / "Gandhinagar — local, on site at every stage". About: "For more than a year…" → "He works hands-on at P Square Interior Studio, alongside Parth, who brings nine years…"; About heading "Learning the craft on site" → "Every detail, checked on site".
- Hero buttons: equal-width 2-column grid (54px tall, gold primary + gold-outline secondary), side by side ≥480px, stacked full-width equal below 480px. 761–1020px: hero columns 1.25fr/.75fr so both fit.
- Watermark: media/hero.jpg re-cut from the p02 source (1440x2560, frame 0.375s, crop y 210–2010, 720x900) above P Square's gold P logo. Project grid cards are now 4:5 (were 9:16) with object-position 50% 15%, which hides the logos (they sit at ~78–93% of the frame height in p01–p05/p07). The lightbox still plays the full clip (logo visible there). p07 keeps its "In process…" caption text and p04 its room labels in the grid. Posters unchanged (cropped by the same CSS). Backups: backup-pre-polish/.
- QA shots: screenshots/qa-polish/ (chromium/webkit × 375/390/768/1024/1440: -top, -hero2, -work, -turnkey; *-375-cover = public cover).

## Private preview hosting
- Site (login required, user `sahil`): https://ridham-interiors-e1eb3b.sites.tab.bot/?preview=1 (site directly) and https://ridham-interiors-e1eb3b.sites.tab.bot/ (shows the "Launching soon" cover).
- Videos: 4 unlisted hosts (2 clips each, because publishes over ~900 KB per folder have failed before):
  https://ridham-m1-00ca0a.sites.tab.bot/, https://ridham-m2-00ca0a.sites.tab.bot/, https://ridham-m3-00ca0a.sites.tab.bot/, https://ridham-m4-00ca0a.sites.tab.bot/
  These are not linked anywhere public and send noindex; they are not behind the login (the clips are P Square's already-public reels).
- noindex everywhere: meta robots, X-Robots-Tag headers, robots.txt Disallow.

## THEME
`THEME` in config.js: "dark" (Dark Luxury, Sahil chose it 3:44 PM 31 Oct), "minimal", "earthy". All colours are in the THEMES block of styles.css. `?theme=minimal` previews another. Live background = drifting warm glows (CSS) + slow gold dust (canvas, pauses when the tab is hidden) + fine grain; all off for prefers-reduced-motion. Hero = sharp still (`media/hero.jpg`, 720x900 from the p02 reel) with a slow zoom; the old arch frames are removed.

## PLACEHOLDERS (to replace)
1. Brand name "Ridham Patel Interior Designer" — `BRAND` in config.js (also in index.html <title>/meta for no-JS, and in build_private.py login page).
2. WhatsApp number — FILLED 31 Oct: `WHATSAPP_NUMBER: "919978621029"` (Ridham, confirmed by Sahil 3:40 PM).
3. Turnkey — `CALL_NUMBER: "+919978621029"` (confirmed by Sahil 3:40 PM). "Turnkey projects" section (`id="turnkey"`, after Projects) has no photos/videos by design (Sahil: "for turnkey project call karna ha"). If CALL_NUMBER is emptied, the button shows "Call — number coming soon" (greyed, not clickable); filled = "Call for Turnkey Project" (tel: link). Its WhatsApp button uses WHATSAPP_NUMBER with a turnkey message. The old "Tanki project" card is gone (it meant turnkey).
4. About photo — `site/media/ridham.jpg` = Ridham's Instagram profile picture (only 150x150 is available while his account is private; shown as a 132px circle). Swap in a bigger photo (square, 600px+) when Sahil/Ridham sends one. Raw copy: `ridham-profile.jpg`.
5. Launch switch: `COUNTDOWN_MODE: "paused"` (no timer), `LAUNCH_AT: "2026-11-15T10:00:00+05:30"` (placeholder). "countdown" = live timer then auto-open; "live" = open. On Vercel `?preview=1` skips the cover, `?cover=1` forces it.
6. All project videos are P Square Interior Studio work (labelled "Project work with P Square Interior Studio"). Ridham's own Instagram (@_ridham_patel_2507) is PRIVATE (3 posts, not visible without following) — nothing taken from it; only a profile link button at the bottom.
7. Project locations are not stated in the reel captions, so no location is shown per project.

## Media list (all from https://www.instagram.com/p_square_interior_studio/ — public reels, downloaded with yt-dlp, trimmed to ~7 s, muted)
| file | site title | source | caption (first line) |
|---|---|---|---|
| p01.mp4 | 3 BHK Home, Completed | P Square Interior Studio IG reel https://www.instagram.com/reel/DeXEMEXIjxk/ (Oct 2026) | ✨ 3 BHK Interior Project Completed! 🏡🤍 |
| p02.mp4 | Elegance in Every Corner | P Square Interior Studio IG reel https://www.instagram.com/reel/DfCXPVeoAsm/ (Oct 2026) | Elegance in every corner. Perfection in every detail. ✨ |
| p03.mp4 | Living & Dining, Arched Feature Wall | P Square Interior Studio IG reel https://www.instagram.com/reel/DcyR2GgS3Mz/ (Sep 2026) | Luxury That Speaks Without Words ✨ | Premium Interior Design |
| p06.mp4 | From 3D Concept to Final Render | P Square Interior Studio IG reel https://www.instagram.com/reel/DcfrMM_SR4X/ (Aug 2026) | From a Simple Idea to a Stunning Reality. ✨ |
| p04.mp4 | Living, Dining & Bedrooms | P Square Interior Studio IG reel https://www.instagram.com/reel/DblHMEey9M0/ (Aug 2026) | Luxury That Feels Like Home  |
| p05.mp4 | Bedroom, Light & Detail | P Square Interior Studio IG reel https://www.instagram.com/reel/DSMdcLtiOe_/ (Dec 2025) | Good lighting + Great design💡✨❤️ |
| p07.mp4 | On Site, Work in Progress | P Square Interior Studio IG reel https://www.instagram.com/reel/DeZkoUyIbnO/ (Oct 2026) | In Process… 🛠️✨ | Behind The Scenes |
| p08.mp4 | Bedroom, Ambient Lighting | P Square Interior Studio IG reel https://www.instagram.com/reel/DKOcFXLqtkf/ (May 2025) | #interior #interiordesign #bedroom #decor #lightingdecor #customer #ha |

p02 caption credits the video to @memories_photo_studio_ (shown in its lightbox). Source reels keep P Square's own watermark/text in a few frames.

## Going public on Vercel (after Sahil approves)
1. Fill config.js (WhatsApp number, brand, countdown).
2. Remove `<meta name="robots" ...noindex...>` from index.html, change robots.txt to `Allow: /`, delete the X-Robots-Tag block in vercel.json.
3. Leave `MEDIA_BASE: "media/"` and `MEDIA_URLS: {}` — Vercel serves site/media/ itself (the private build injects the tab.bot video URLs only into its own copy).
4. Deploy the `site/` folder.

## 31 Oct fix pass (Sahil's phone screenshots — "kya mistake ha aur add bhi karna ha")
- About: "alongside Parth" -> "alongside Parth Patel, who brings nine years of interior design experience" (Sahil 4:38 PM: keep Parth, full name, keep nine years; his own info). "Ridham takes on work in Gandhinagar only, so he can be on site…" -> "Being local to Gandhinagar, he's on site whenever the job needs him." Heading "on site" is `<em class="nowrap">on&nbsp;site</em>` (never splits). "P&nbsp;Square" non-breaking in body copy.
- Projects note (was a repeat of the Parth line) -> "Projects by P Square Interior Studio, where Ridham works hands-on. Tap any project to watch it." (the one P Square credit line). Each card now has its own true descriptor instead of the repeated "Project work with P Square Interior Studio". Dates = each reel's Instagram post date (checked against media-src/meta-candidates.json upload_date).
- Turnkey: "Taken up in Gandhinagar only." -> "…until the keys are handed over, anywhere in Gandhinagar."; "so we talk it through first" -> "so it's best talked through first" (site voice is first person "I"). Service area heading "Only in Gandhinagar" -> "Right here in Gandhinagar".
- Process -> "How I work", 4 steps: Consultation / Design & 3D views / Execution on site / Handover + "Book a free consultation →". Hero button now "Book a free consultation" (hero__cta max-width 520px).
- GRID now 11 clips (10 portrait + p06 wide) = 12 cells: fills 2 columns (phones/tablets) and 3 columns (desktop) with no empty cell. Below it a full-width "Your space could be next → Book a free consultation" banner (.nextcard).
- Clips changed (media-src/av-build-v3/, 540 wide, H.264 + AAC 48k mono, ?v=a3 via MEDIA_VER_FILE in build_private.py):
  - p04 REPLACED: old reel DblHMEey9M0 had Instagram room-label text burned in all through. New p04 = DdJzJm6yfxR (P Square reel, 11 Sep 2026) 11.0–17.6 s: dining, kitchen, bedroom.
  - p05 re-cut: old cut (3.0 s) opened on a client's door nameplate (names + flat number). New = DSMdcLtiOe_ 19.9–25.1 s (bedroom only, no nameplate).
  - p07 cropped: "In process…" text sat at y 1120–1201 of 1920 for the whole reel -> crop 864x1080 from the top (x 108, y 0) -> 540x676 (4:5). Poster = clip 4.5 s.
  - NEW p09 = DdJzJm6yfxR 2.7–9.4 s (living room, ring-light ceiling, jaali mandir). NEW p10 = DdJzJm6yfxR 22.5–29.4 s (green bedroom, arches, mural, study unit). NEW p11 = DdoXkL3qYAu (23 Sep 2026) 0–6.8 s (site work -> finished home; stops before a family photo frame at 7 s). Audio for these two reels downloaded with yt-dlp into media-src/audio/.
  - Media hosts: m2 (p03,p04), m3 (p05,p06), m4 (p07,p08), NEW m5 ridham-m5-00ca0a (p09,p10), NEW m6 ridham-m6-00ca0a (p11). To republish a host: copy clips into publish/mN/_v/, `node /home/user/tab/publish-cli.mjs site.publish '{"slug":"ridham-mN-00ca0a","source_dir":"…/publish/mN","title":"."}'`.
- Still visible in the LIGHTBOX only (grid crop hides them): P Square's small gold logo near the bottom of some clips (p02, p03, p09, p11). No client names, phone numbers or handles in any clip.
- Instagram "See more work" button NOT added: the only Ridham handle (@_ridham_patel_2507) is a private account; the footer Instagram button remains as before.
- Backup of the site before this pass: backup-pre-fix3/. QA: screenshots/qa-fix3/ (chromium/webkit × 360/375/390/414/768/1024/1440: -about, -projects, -howiwork), script test/qa_fix3.py.

## Fix pass 2 — 31 Oct 2026 (Sahil 5:06 PM "Phela fix karo sab kuch")
- P SQUARE LOGO REMOVED from every clip that had it (p01, p02, p03, p04, p05, p09, p10, p11; p06/p07/p08 never had it). The gold P logo sat at ~77-93% of the frame height (centre; p05 bottom-left). New cuts are re-encoded from the audio sources (media-src/audio/, same trim points as before) with a 4:5 crop from near the top: `crop=iw:iw*5/4:0:ih*0.025` -> 540x676, H.264 2-pass + AAC 48k mono, faststart, 405-427 KB each. The lightbox (full-screen) now plays these same logo-free 4:5 clips. Checked every clip at 2 fps (full frame + bottom-strip zoom): no logo, handle, overlay text, names or flat numbers. (Real decor stays: e.g. a "Good Vibes Only" wall sign in p04's kitchen, a Radha-Krishna wall panel in p11.)
- Posters for those 8 re-cut from the new clips (432x540, same moment as the old posters). Old clips/posters/text files: backup-pre-fix4/.
- Cache-buster ?v=a4 for p01-p05, p09-p11 (build_private.py MEDIA_VER_FILE); m1, m2, m3, m5, m6 republished.
- FILTER VIEWS END EVEN: a "See all 11 projects / View all" tile (#moreCard, last in #grid) appears only in filtered views and spans exactly the cells the last row leaves empty (JS fillGap(): visible cells vs grid columns, recomputed on filter + resize). All view has no gap (12 cells), so the tile stays hidden there. "View all" switches back to All.
- Removed the p02 lightbox credit "Video: @memories_photo_studio_" (a social handle; it also doubled the "Video: P Square Interior Studio" line).
- Tests: test/site.test.mjs (11 pass, new test 11 covers the above). QA: test/qa_fix4.py (live, logged in, Chromium + WebKit at 360/375/390/414/768/1024/1440, every filter + lightbox) -> screenshots/qa-fix4/.

## Countdown + cinematic reveal — 31 Oct 2026 (Sahil 6:03–6:05 PM: "countdown and video after that, like Monarch & Mark")
- Main address `/` = launch screen (cover_template.html, public): dark luxury, RP monogram, gold dust, slow glow, film grain, corner frame,
  and a dimmed, slightly blurred interior film loop behind it (bg.mp4, 8 s, no sound, 525 KB: p09 0–3.2 s + p03 0–3.2 s + p02 3.2–6.4 s,
  crossfades, all logo-free clips) served from the new unlisted host https://ridham-m7-00ca0a.sites.tab.bot/ (bg.mp4 + bg.jpg poster; publish/m7).
- THE ONE LINE: `LAUNCH_AT` in site/assets/js/config.js.
  - `LAUNCH_AT: null,` (now) -> "Launching soon" + gold "AFTER DIWALI" pill, no numbers.
  - `LAUNCH_AT: "2026-11-15T10:00:00+05:30",` -> Days/Hours/Minutes/Seconds tiles + "Sunday, 15 November 2026 at 10:00 AM IST".
  - Then `TAB_TASK_ID=<id> python3 build_private.py` (rebuilds + republishes). `LAUNCH_NOTE` = italic line under the title ("" hides it).
  - `COUNTDOWN_MODE`: "auto" (default, follow LAUNCH_AT), "live" (open now), "paused" (never numbers).
- At zero: tiles + monogram flare (1 s) -> text zooms away, the film comes up to full brightness with "NOW OPEN · Ridham Patel Interior Designer" (3.3 s)
  -> dark curtains close with a gold seam (1.1 s) -> page goes to the full site, whose curtains open (site/index.html `#rv`, class `rp-reveal`,
  flag sessionStorage rp_reveal) and the site scales in. ~7 s in total. The server opens `/` itself at LAUNCH_AT (gate countdown mode);
  the screen re-checks `/` for up to 15 s in case the phone clock is ahead.
- Test: `/?launch=2026-10-31T18:30:00+05:30` (any ISO time) runs the countdown + reveal without touching config; a test reveal opens
  `/?preview=1` (login needed). `?preview=1` = Sahil's private full site, unchanged.
- QA: qa/countdown/ (webkit-375-*, chromium-1440-*: 1 paused, 2 preview, 3 countdown, 4 zero, 5 film, 6 title, 7 curtains, 8 site opening, 9 site)
  + ridham-countdown-preview.mp4 (375x812 phone recording, 18.8 s). Also tested locally: a real LAUNCH_AT 40 s ahead opened `/` publicly with no login.
- NOT changed: the Vercel (public) build still has the old simple in-page cover in site/index.html; port cover_template.html before going public.
- Backup before this pass: backup-pre-countdown/.

## 31 Oct: name fix + logo (Sahil 6:35/6:37 PM)
- Brand is now "Ridham Patel Interior Designer" everywhere (BRAND in config.js, titles, countdown screen, reveal overlay "NOW OPEN · Ridham Patel / Interior Designer", header sub, footer, ©, login page). Tab title: "Ridham Patel Interior Designer · Gandhinagar" (main.js no longer appends "· Interior Designer in"). Only generic "elegant interiors" (p-card copy) remains.
- LOGO: 3 options in logo/ (A stacked square monogram, B horizontal, C arch doorway + italic R) with SVG (text converted to vector paths from the site's own Cormorant/Manrope), PNG 1024 transparent, dark/light variants; options-sheet.jpg. Applied C "Arch": header mark, footer lockup, countdown mark, in-site cover, login page, favicon.svg (?v=2) + apple-touch-icon.png (public in the gate). Asset cache-buster ?v=nf2 on styles/config/main. No og:image (private site, no public absolute URL).
- Backups: backup-pre-namefix/. QA: qa/name-fix/ (test/qa_namefix.py, test/qa_namefix_login.py).

## 31 Oct: logo v2 — P Square-style ring monogram (Sahil 6:47 PM "P square ka logo ha wese kuch chaiye")
- logo/v2/: gen_logo.py (geometry + wordmark -> SVG, text as vector paths from Montserrat Bold/Medium), render.py (SVG -> PNG via Chromium).
  V1 = R + P interlocked (R's bowl dips under P, R's leg crosses over P's stem, P's stem + R's leg pass through the ring) — APPLIED.
  V2 = R and P share one stem (P's outer bowl around R's inner bowl) — kept as alternative.
  Per variant: mark / stacked (RIDHAM PATEL + INTERIOR DESIGNER) / horizontal header lockup, each *-on-dark.svg|png and *-on-light.svg|png (PNG 1024 transparent), favicon.svg + favicon-32/180/512.png.
  Options sheet with P Square reference: logo/v2-options-sheet.jpg.
- Applied with apply_logo_v2.py (inline SVG with its own gold gradient, colours from --lg0..6 CSS vars, dark palette by default): header, footer lockup, in-site cover, countdown (cover_template), login page, favicon.svg?v=3 + apple-touch-icon.png?v=3. Header/footer name now wide gold caps (Manrope 700, tracked). Assets ?v=lg2.
- Old arch C / A / B files untouched in logo/. Backup: backup-pre-logo-v2/. QA: test/qa_logo_v2.py -> qa/logo-v2/. Tests 13/13.
- Revert to the arch: copy backup-pre-logo-v2/* back and rebuild.


## GitHub + Vercel (31 Oct 2026)
- GitHub repo (PRIVATE): https://github.com/sahilpatel5037/ridham-patel-interiors — full source (site/, launch/, build scripts, templates, tests). No passwords: the private-preview login lives only in /home/user/tab/state/ on Tab's box.
- Vercel project `ridham-patel-interiors` (imported from that repo, auto-deploys on every push to `main`).
- **Vercel serves ONLY the countdown page.** The root `vercel.json` sets `"outputDirectory": "launch"`, so production and every preview deployment contain only `launch/` (countdown HTML, its CSS/JS, logo, icons, fonts, background loop). `site/` (the full website) is in the repo but is never deployed until launch day. Unknown paths answer 404 -> back to the countdown.
- `launch/` is generated: `python3 build_launch.py` (reads LAUNCH_AT / LAUNCH_NOTE from site/assets/js/config.js). Re-run it after any change to the countdown, then commit `launch/`.
- Private full preview (login): https://ridham-interiors-e1eb3b.sites.tab.bot/?preview=1 (user `sahil`)

### Launch day (full site public on Vercel)
1. Set `LAUNCH_AT` in site/assets/js/config.js (e.g. "2026-11-15T10:00:00+05:30"), run `python3 build_launch.py` and push: the Vercel page now counts down with numbers.
2. A few minutes before the launch time, change the root `vercel.json` `"outputDirectory": "launch"` -> `"site"` and push (Vercel redeploys in ~30 s). The full site's own countdown keeps showing until zero, then the reveal opens it.
   (Before that switch nothing of the full site is on Vercel; after it, the site's HTML is public, so keep that window short.)
3. Optional: remove the `X-Robots-Tag: noindex` header in `vercel.json` (and `<meta name="robots" content="noindex">` in site/index.html, `robots.txt`) so Google can index it.
