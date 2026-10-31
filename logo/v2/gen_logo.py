
import math, sys, json, os
from shapely.geometry import LineString, Point, Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
OUT = os.path.dirname(os.path.abspath(__file__))
C = (100.0, 100.0)

def arc(cx, cy, r, a0, a1, n=48):
    return [(cx + r*math.cos(math.radians(a0 + (a1-a0)*i/n)), cy + r*math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n+1)]

def stroke(pts, w):
    return LineString(pts).buffer(w/2, cap_style='flat', join_style='mitre', mitre_limit=4, quad_segs=24)

def bowl(x, top, bot, reach):
    # stem-attached bowl: top bar -> half circle -> bottom bar, returns centre-line points (without stem)
    r = (bot - top)/2
    cx = x + reach - r
    return [(x, top), (cx, top)] + arc(cx, top + r, r, -90, 90)[1:] + [(x, bot)]

def ring(r, w):
    return Point(C).buffer(r + w/2, quad_segs=64).difference(Point(C).buffer(r - w/2, quad_segs=64))

def build(variant, W=13.0, RW=6.5, RR=84.0, gap=4.5):
    if variant == 'v1':
        # R (left, rises through the ring top) + P (right, lower, falls through the ring bottom); R's leg crosses P's stem
        s = 0.86; dx = -2
        T = lambda pts: [(C[0] + s*(x - C[0]), C[1] + s*(y - C[1])) for x, y in pts]
        Rx, Rt, Rb = 52+dx, 40, 150
        r_main = stroke(T([(Rx, Rb)] + bowl(Rx, Rt, 92, 50)), W)
        Px, Pt, Pb = 112+dx, 70, 194
        px, pt = T([(Px, Pt)])[0]
        p_stem = stroke([(px, 196), (px, pt - W/2)], W)
        p_bowl = stroke(T(bowl(Px, Pt, 122, 50)), W)
        P = unary_union([p_stem, p_bowl])
        lx0, ly0 = T([(Rx + 24, 92)])[0]
        ang = math.atan2(1.25, 1.0)
        # extend the leg until it clears the ring
        L = 10
        while math.hypot(lx0 + L*math.cos(ang) - C[0], ly0 + L*math.sin(ang) - C[1]) < RR + RW/2 + 8: L += 1
        leg = stroke([(lx0, ly0), (lx0 + L*math.cos(ang), ly0 + L*math.sin(ang))], W)
        R = r_main.difference(P.buffer(gap, join_style='mitre'))  # R's bowl dips UNDER P
        P = P.difference(leg.buffer(gap, join_style='mitre'))      # R's leg passes OVER P's stem
        R = unary_union([R, leg])
        letters = unary_union([R, P])
    else:
        # V2: R and P share one stem; P's bowl is the outer bowl, R's bowl nests inside, R's leg sweeps out over P's bowl
        Sx = 70
        Sx = 72
        top = 40
        p_bowl = stroke(bowl(Sx, top, 118, 64), W)
        stem = stroke([(Sx, 194), (Sx, top - W/2)], W)
        r_bowl = stroke(bowl(Sx, 62, 96, 38), W)
        lx0, ly0 = Sx + 24, 96; ang = math.atan2(66, 52); L = 10
        while math.hypot(lx0 + L*math.cos(ang) - C[0], ly0 + L*math.sin(ang) - C[1]) < RR + RW/2 + 8: L += 1
        leg = stroke([(lx0, ly0), (lx0 + L*math.cos(ang), ly0 + L*math.sin(ang))], W)
        p_bowl = p_bowl.difference(leg.buffer(gap, join_style='mitre'))
        letters = unary_union([stem, p_bowl, r_bowl, leg])
    rg = ring(RR, RW).difference(letters.buffer(gap, join_style='mitre'))
    if not isinstance(rg, Polygon):
        rg = unary_union([p for p in rg.geoms if p.area > 12*RW*RW])
    return letters, rg

def poly_path(g, nd=2):
    polys = [g] if isinstance(g, Polygon) else list(g.geoms)
    out = []
    for p in polys:
        for ringc in [p.exterior] + list(p.interiors):
            cs = list(ringc.coords)[:-1]
            out.append('M' + ' L'.join(f'{x:.{nd}f} {y:.{nd}f}' for x, y in cs) + 'Z')
    return ''.join(out)

# ---------- wordmark ----------
_fonts = {}
def font(wght):
    if wght not in _fonts:
        f = TTFont('/home/user/.fonts/Montserrat.ttf')
        _fonts[wght] = instancer.instantiateVariableFont(f, {'wght': wght})
    return _fonts[wght]

def text_path(s, wght, size, track, x0=0, y0=0):
    f = font(wght); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    sc = size/upm; x = x0; pen = SVGPathPen(gs)
    for i, ch in enumerate(s):
        g = cmap[ord(ch)]
        tp = TransformPen(pen, (sc, 0, 0, -sc, x, y0))
        gs[g].draw(tp)
        x += gs[g].width*sc + (track*size if i < len(s)-1 else 0)
    return pen.getCommands(), x - x0

def cap_height(wght, size):
    f = font(wght); return f['OS/2'].sCapHeight * size / f['head'].unitsPerEm

PAL = {
 'dark':  [('0', '#8C6420'), ('.22', '#D9AE5C'), ('.40', '#F8E7AE'), ('.52', '#E3C27A'), ('.66', '#AF8236'), ('.84', '#EDD18E'), ('1', '#9A6F2A')],
 'light': [('0', '#5E3E0C'), ('.22', '#A57630'), ('.40', '#D2B064'), ('.52', '#B48A40'), ('.66', '#7C5418'), ('.84', '#B8924A'), ('1', '#6A4812')],
}
def grad(gid, pal, x1, y1, x2, y2):
    st = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in PAL[pal])
    return f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}">{st}</linearGradient>'

def mark_paths(variant, **kw):
    L, Rg = build(variant, **kw)
    return poly_path(L), poly_path(Rg)

def svg_mark(variant, pal='dark', gid='g', bg=None, fav=False):
    kw = dict(W=19, RW=11, RR=82, gap=5) if fav else {}
    L, Rg = mark_paths(variant, **kw)
    pad = 6 if not fav else 0
    vb = f'{-pad} {-pad} {200+2*pad} {200+2*pad}'
    bgs = ''
    if bg:
        bgs = f'<rect x="{-pad}" y="{-pad}" width="{200+2*pad}" height="{200+2*pad}" rx="{44 if fav else 0}" fill="{bg}"/>'
    if fav:
        # shrink the mark inside the tile
        inner = f'<g transform="translate(100 100) scale(.90) translate(-100 -100)"><path fill="url(#{gid})" d="{Rg}"/><path fill="url(#{gid})" d="{L}"/></g>'
    else:
        inner = f'<path fill="url(#{gid})" d="{Rg}"/><path fill="url(#{gid})" d="{L}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><defs>{grad(gid, pal, 10, 10, 190, 190)}</defs>{bgs}{inner}</svg>')

NAME = 'RIDHAM PATEL'; SUB = 'INTERIOR DESIGNER'

def svg_stacked(variant, pal='dark', gid='g', bg=None):
    L, Rg = mark_paths(variant)
    ns = 44; nt, nw = text_path(NAME, 700, ns, .10)
    ss = 15.5; st, sw = text_path(SUB, 500, ss, .52)
    MS = 1.45
    W = max(nw, sw, 200*MS) + 40
    mx = (W - 200*MS)/2
    ny = 200*MS + 34 + cap_height(700, ns)
    nt, _ = text_path(NAME, 700, ns, .10, (W-nw)/2, ny)
    sy = ny + 24 + cap_height(500, ss)
    st, _ = text_path(SUB, 500, ss, .52, (W-sw)/2 + .26*ss, sy)
    # thin rules either side of the sub line
    ly = sy - cap_height(500, ss)/2
    H = sy + 26
    a = (W-sw)/2 + .26*ss
    rules = f'<path fill="url(#{gid})" d="M{a - 38:.1f} {ly-0.8:.1f}h24v1.6h-24zM{a + sw + 14:.1f} {ly-0.8:.1f}h24v1.6h-24z"/>'
    bgs = f'<rect width="{W:.1f}" height="{H+14:.1f}" y="-14" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -14 {W:.1f} {H+14:.1f}"><defs>{grad(gid, pal, 0, -14, W, H)}</defs>{bgs}'
            f'<g transform="translate({mx:.1f} 0) scale({MS})"><path fill="url(#{gid})" d="{Rg}"/><path fill="url(#{gid})" d="{L}"/></g>'
            f'<path fill="url(#{gid})" d="{nt}"/><path fill="url(#{gid})" d="{st}"/>{rules}</svg>')

def svg_horizontal(variant, pal='dark', gid='g', bg=None):
    L, Rg = mark_paths(variant)
    ns = 50; ss = 17.5
    _, nw = text_path(NAME, 700, ns, .08); _, sw = text_path(SUB, 500, ss, .46)
    tx = 200 + 34 + 30
    nch = cap_height(700, ns); sch = cap_height(500, ss)
    block = nch + 20 + sch
    ny = 100 - block/2 + nch
    sy = ny + 20 + sch
    nt, _ = text_path(NAME, 700, ns, .08, tx, ny)
    st, _ = text_path(SUB, 500, ss, .46, tx + 2, sy)
    W = tx + max(nw, sw) + 12
    div = f'<path fill="url(#{gid})" fill-opacity=".55" d="M{200+30:.1f} 46h1.6v108h-1.6z"/>'
    bgs = f'<rect x="-8" y="-8" width="{W+16:.1f}" height="216" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-8 -8 {W+16:.1f} 216"><defs>{grad(gid, pal, 0, 0, W, 200)}</defs>{bgs}'
            f'<path fill="url(#{gid})" d="{Rg}"/><path fill="url(#{gid})" d="{L}"/>{div}'
            f'<path fill="url(#{gid})" d="{nt}"/><path fill="url(#{gid})" d="{st}"/></svg>')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    files = {}
    for v in ('v1', 'v2'):
        for pal, bg in (('dark', None), ('light', None)):
            tag = 'on-dark' if pal == 'dark' else 'on-light'
            files[f'{v}-mark-{tag}.svg'] = svg_mark(v, pal, f'{v}m{pal}')
            files[f'{v}-stacked-{tag}.svg'] = svg_stacked(v, pal, f'{v}s{pal}')
            files[f'{v}-horizontal-{tag}.svg'] = svg_horizontal(v, pal, f'{v}h{pal}')
        files[f'{v}-favicon.svg'] = svg_mark(v, 'dark', f'{v}f', bg='#11100E', fav=True)
    for n, s in files.items():
        open(os.path.join(OUT, n), 'w').write(s)
    print(json.dumps({n: len(s) for n, s in files.items()}))
