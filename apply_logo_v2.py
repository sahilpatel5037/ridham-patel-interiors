
# Logo v2 (31 Oct, Sahil "P square ka logo ha wese kuch chaiye"): V1 R+P interlocked monoline monogram in a ring, gold gradient.
# Replaces the arch (C) mark in header, footer, in-site cover, countdown, login; favicon + apple-touch icon.
import re, sys, shutil, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo', 'v2'))
import gen_logo as G
HERE = os.path.dirname(os.path.abspath(__file__))
VAR = 'v1'
L, Rg = G.mark_paths(VAR)
DARK = G.PAL['dark']
def inline(cls, gid, extra=''):
    stops = ''.join(f'<stop offset="{o}" style="stop-color:var(--lg{i},{c})"/>' for i, (o, c) in enumerate(DARK))
    return (f'<svg class="{cls} rp2" viewBox="-6 -6 212 212" {extra}><defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="10" y1="10" x2="190" y2="190">{stops}</linearGradient></defs>'
            f'<path style="fill:url(#{gid});stroke:none" d="{Rg}"/><path style="fill:url(#{gid});stroke:none" d="{L}"/></svg>')
def swap(html, cls, new):
    pat = re.compile(r'<svg class="' + re.escape(cls) + r'"[^>]*>.*?</svg>', re.S)
    out, n = pat.subn(lambda m: new, html, count=1)
    assert n == 1, cls
    return out
p = os.path.join(HERE, 'site/index.html'); h = open(p, encoding='utf-8').read()
h = swap(h, 'cover__mark', inline('cover__mark', 'rpg-cover', 'aria-hidden="true"'))
h = swap(h, 'brand__mark', inline('brand__mark', 'rpg-head', 'aria-hidden="true"'))
h = swap(h, 'foot__mark', inline('foot__mark', 'rpg-foot', 'aria-hidden="true"'))
h = h.replace('favicon.svg?v=2', 'favicon.svg?v=3').replace('apple-touch-icon.png"', 'apple-touch-icon.png?v=3"').replace('?v=nf2', '?v=lg2')
open(p, 'w', encoding='utf-8').write(h)
p = os.path.join(HERE, 'cover_template.html'); h = open(p, encoding='utf-8').read()
h = swap(h, 'mark', inline('mark', 'rpg-cd', 'role="img" aria-label="Ridham Patel Interior Designer logo"'))
h = h.replace('/favicon.svg?v=2', '/favicon.svg?v=3').replace('/apple-touch-icon.png"', '/apple-touch-icon.png?v=3"')
h = h.replace('.mark{width:70px;height:72px;', '.mark{width:92px;height:92px;')
h = h.replace('.mark path{fill:none;stroke:var(--gold)}.mark .a1,.mark .a3{stroke-width:1.4px}.mark .a2{stroke-width:.8px;opacity:.5}.mark .r{fill:var(--gold);stroke:none}', '')
h = h.replace('  .mark{width:58px;height:60px}', '  .mark{width:76px;height:76px}')
h = h.replace('.mark{width:50px;height:52px}', '.mark{width:62px;height:62px}')
open(p, 'w', encoding='utf-8').write(h)
p = os.path.join(HERE, 'login_template.html'); h = open(p, encoding='utf-8').read()
h = swap(h, 'lm', inline('lm', 'rpg-login', 'aria-hidden="true"'))
h = h.replace('.lm{display:block;width:46px;height:48px;margin:0 0 18px}.lm path{fill:none;stroke:#D9BC86;stroke-width:1.2px}.lm .a2{stroke-width:.7px;opacity:.5}.lm .r{fill:#D9BC86;stroke:none}',
              '.lm{display:block;width:64px;height:64px;margin:0 0 18px}')
if 'rel="icon"' not in h:
    h = h.replace('<title>', '<link rel="icon" href="/favicon.svg?v=3" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png?v=3"><title>', 1)
open(p, 'w', encoding='utf-8').write(h)
shutil.copy(os.path.join(HERE, 'logo/v2', f'{VAR}-favicon.svg'), os.path.join(HERE, 'site/favicon.svg'))
shutil.copy(os.path.join(HERE, 'logo/v2', f'{VAR}-favicon-180.png'), os.path.join(HERE, 'site/apple-touch-icon.png'))
print('applied', VAR)
