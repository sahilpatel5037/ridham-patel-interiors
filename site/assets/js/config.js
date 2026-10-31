/* ============================================================
   SITE SETTINGS — the only file you need to edit.
   ============================================================ */
window.SITE_CONFIG = {
  /* Look of the site: "dark" (Dark Luxury, chosen 31 Oct), "minimal" or "earthy".
     Add ?theme=minimal to the address to preview another without changing this. */
  THEME: "dark",

  /* Brand / name shown in the header, footer, title and cover. */
  BRAND: "Ridham Patel Interior Designer",
  PERSON: "Ridham Patel",
  CITY: "Gandhinagar",

  /* WhatsApp number with country code, digits only, e.g. "91XXXXXXXXXX".
     While empty, the buttons still open WhatsApp with the message ready,
     but the visitor has to pick the contact. */
  WHATSAPP_NUMBER: "919978621029",
  WHATSAPP_TEXT: "Hi Ridham, I saw your portfolio and would like a free consultation for my space.",

  /* Phone number for the "Call for Turnkey Project" button, with country code,
     e.g. "+91XXXXXXXXXX". While empty, the button shows "Call — number coming soon"
     (greyed out, not clickable). */
  CALL_NUMBER: "+919978621029",

  /* Instagram profile (link only, nothing is embedded). */
  INSTAGRAM_URL: "https://www.instagram.com/_ridham_patel_2507/",

  /* Where the project videos live. Default: the media/ folder next to index.html
     (works as-is on Vercel). MEDIA_URLS can point single files somewhere else,
     e.g. { "p01.mp4": "https://cdn.example.com/p01.mp4" }. */
  MEDIA_BASE: "media/",
  MEDIA_URLS: {},

  /* LAUNCH SWITCH — countdown screen + cinematic reveal (31 Oct, like Monarch & Mark).
     LAUNCH_AT is the ONE line to change:
       null                          = "Launching soon · After Diwali" screen, no numbers (current — date not decided)
       "2026-11-15T10:00:00+05:30"   = live days/hours/min/sec countdown to that moment (India time, keep the +05:30);
                                       at zero the reveal plays (film + curtains) and the full site opens by itself.
     Test any time without changing this: add ?launch=2026-10-31T18:30:00+05:30 to the main address.
     Private preview: the main address shows only the countdown screen (public); the full site is behind the
     login at /?preview=1 (or /preview). After editing, run build_private.py again to republish. */
  LAUNCH_AT: null,

  /* Small line under the title on the countdown screen. "" hides it. */
  LAUNCH_NOTE: "Something beautiful is on its way. See you after Diwali.",

  /* "auto" = follow LAUNCH_AT (normal). "live" = open the full site to everyone now. "paused" = never show numbers. */
  COUNTDOWN_MODE: "auto"
};
