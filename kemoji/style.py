"""Shared KRONOS style: palette and reusable animated parts."""
import math

from . import geom as G
from .lottie import (Anim, IN, LIN, OUT, SINE, ellipse, fill, gradient, group, path,
                     stroke)

# Palette sampled from the KRONOS STAFF set.
INK = "#0b1533"
WHITE = "#ffffff"
SNOW = "#f4faff"
ICE = "#dcefff"
SKY = "#a9d6ff"
LIGHT = "#78b6f7"
MID = "#4a8ff0"
BLUE = "#2f6be0"
DEEP = "#1f4dbb"
NAVY = "#183a8f"
LAV = "#b9a8ff"
VIOLET = "#7b5cf0"
PINK = "#ff8fc6"
GOLD_HI = "#fff4c2"
GOLD = "#ffd35a"
GOLD_LO = "#e79a2a"
SILVER_HI = "#ffffff"
SILVER = "#d5e3f7"
SILVER_LO = "#93a9cf"

OW = 13  # visible outer outline width (px on the 512 canvas)


def paths(bs):
    if isinstance(bs, dict):
        bs = [bs]
    return [path(b) for b in bs]


def stack(items, nm="stack", **tf):
    """Group whose items are given in painter's order (back first)."""
    return group(list(reversed(list(items))), nm, **tf)


def shape(bs, *paints, nm="shape", **tf):
    return group(paths(bs) + list(paints), nm, **tf)


def outlined(bs, paint, ow=OW, ink=INK, nm="part", **tf):
    """Fill with an outer-only outline (2x stroke drawn under the fill)."""
    return group(paths(bs) + [paint, stroke(ink, ow * 2)], nm, **tf)


def lines(bs, color=INK, w=6, opacity=100, cap=2, nm="lines", **tf):
    return group(paths(bs) + [stroke(color, w, opacity, cap=cap)], nm, **tf)


def lin(stops, p0, p1, opacity=100):
    return gradient(stops, list(p0), list(p1), opacity=opacity)


def vgrad(top, bottom, y0, y1, x=256, opacity=100):
    return gradient([(0, top), (1, bottom)], [x, y0], [x, y1], opacity=opacity)


def dgrad(c0, c1, p0, p1, mid=None, opacity=100):
    stops = [(0, c0), (1, c1)] if mid is None else [(0, c0), (0.5, mid), (1, c1)]
    return gradient(stops, list(p0), list(p1), opacity=opacity)


def glow(cx, cy, r, color=SKY, alpha=0.55, opacity=100, nm="glow", ry=None):
    ry = r if ry is None else ry
    g = gradient([(0, color, alpha), (0.45, color, alpha * 0.45), (1, color, 0)],
                 [cx, cy], [cx + r, cy], radial=True, opacity=opacity)
    return group([ellipse([cx, cy], [2 * r, 2 * ry]), g], nm)


def highlight(bs, opacity=90, color=WHITE, nm="hl"):
    return shape(bs, fill(color, opacity), nm=nm)


def sheen(bs, t0, t1, angle=30, width=46, alpha=0.75, color=WHITE, rule=1, nm="sheen"):
    """A bright band sweeping across the given shapes (clipped by the shapes
    themselves via an animated gradient - no masks needed)."""
    if isinstance(bs, dict):
        bs = [bs]
    pts = [p for b in bs for p in G.flatten(b, 8)]
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    proj = [p[0] * ux + p[1] * uy for p in pts]
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    c_proj = cx * ux + cy * uy
    half = width * 2.0
    lo = min(proj) - c_proj - half * 0.6
    hi = max(proj) - c_proj + half * 0.6

    def se(off):
        mx, my = cx + ux * off, cy + uy * off
        return [mx - ux * half, my - uy * half], [mx + ux * half, my + uy * half]

    s0, e0 = se(lo)
    s1, e1 = se(hi)
    s = Anim((t0, s0, SINE), (t1, s1))
    e = Anim((t0, e0, SINE), (t1, e1))
    f = 0.25
    g = gradient([(0, color, 0), (0.5 - f / 2, color, 0), (0.5, color, alpha),
                  (0.5 + f / 2, color, 0), (1, color, 0)], s, e, rule=rule)
    return group(paths(bs) + [g], nm)


def twinkle(cx, cy, r, t0, dur=36, color=WHITE, spin=90, peak=100, halo=True, q=0.62,
            total=180, nm="twinkle"):
    """Four-point sparkle that pops in and out once per loop."""
    t0 = max(0, min(t0, total - dur))
    sc = Anim((t0, [0, 0], OUT), (t0 + dur * 0.42, [peak, peak], IN), (t0 + dur, [0, 0]))
    rot = Anim((t0, -spin / 2, LIN), (t0 + dur, spin / 2))
    items = [group(paths(G.sparkle(r, q)) + [fill(color)], "star")]
    if halo:
        items.append(glow(0, 0, r * 0.9, WHITE, 0.55, nm="halo"))
    return group(items, nm, p=(cx, cy), s=sc, r=rot)


def blink(t0, dur=24, lo=0, hi=100, total=180):
    t0 = max(0, min(t0, total - dur))
    return Anim((t0, lo, OUT), (t0 + dur * 0.35, hi, IN), (t0 + dur, lo))


def pulse_scale(t0, dur, amp, base=100, total=180):
    t0 = max(0, min(t0, total - dur))
    return Anim((t0, [base, base], OUT), (t0 + dur * 0.35, [base + amp, base + amp], SINE),
                (t0 + dur, [base, base]))


def bob(x, y, amp, total=180, phase=0):
    """Smooth vertical float, extremes on keys so the loop is seamless."""
    h = total / 2
    keys = [(0, [x, y + amp]), (h, [x, y - amp]), (total, [x, y + amp])]
    if phase:
        keys = [(0, [x, y - amp]), (h, [x, y + amp]), (total, [x, y - amp])]
    return Anim(*keys)


def sway(amp, total=180, periods=1, phase=0):
    keys = []
    step = total / (2 * periods)
    for k in range(2 * periods + 1):
        sign = 1 if (k + phase) % 2 == 0 else -1
        keys.append((k * step, -amp * sign))
    return Anim(*keys)


def shimmer(bs, t0, dur=22, peak=60, color=WHITE, nm="shimmer"):
    """White overlay flash on one facet."""
    return shape(bs, fill(color, blink(t0, dur, 0, peak)), nm=nm)


def flake(r=14, w=3.5, color=WHITE, opacity=100):
    """Tiny six-armed snowflake centred on the origin (for falling snow)."""
    arms = []
    for k in range(6):
        a = math.radians(-90 + k * 60)
        ux, uy = math.cos(a), math.sin(a)
        arms.append(G.line((0, 0), (ux * r, uy * r)))
        bx, by = ux * r * 0.55, uy * r * 0.55
        for s in (-1, 1):
            b = a + s * math.radians(45)
            arms.append(G.line((bx, by), (bx + math.cos(b) * r * 0.35, by + math.sin(b) * r * 0.35)))
    return group(paths(arms) + [stroke(color, w, opacity)], "flake")


def snowfall(spots, total=180, dur=110, fall=120, r=12):
    """[(x, y_start, t0)] -> drifting snowflakes (wrapping around the loop)."""
    out = []
    for k, (x, y, t0) in enumerate(spots):
        sway_x = 14 if k % 2 else -14
        out += drift([flake(r if k % 3 else r * 0.75)], (x, y), (x + sway_x, y + fall), t0, dur, total,
                     fade=0.25, r0=0, r1=90 if k % 2 else -90)
    return out


def arc_keys(p0, p1, height, t0, t1, n=10):
    """Parabolic flight p0 -> p1 peaking `height` px above the chord (LIN keys)."""
    keys = []
    for k in range(n + 1):
        u = k / n
        x = p0[0] + (p1[0] - p0[0]) * u
        y = p0[1] + (p1[1] - p0[1]) * u - 4 * height * u * (1 - u)
        keys.append((t0 + (t1 - t0) * u, [x, y], LIN))
    return keys


def _pl(keys, t):
    """Piecewise-linear sample of [(t, value)] (values: number or list)."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (ta, va), (tb, vb) in zip(keys, keys[1:]):
        if ta <= t <= tb:
            f = 0 if tb == ta else (t - ta) / (tb - ta)
            if isinstance(va, (list, tuple)):
                return [a + (b - a) * f for a, b in zip(va, vb)]
            return va + (vb - va) * f
    return keys[-1][1]


def _window(keys, lo, hi):
    """Linear keys restricted to [lo, hi] (values at the cut are interpolated)."""
    out = [(lo, _pl(keys, lo))]
    out += [k for k in keys if lo < k[0] < hi]
    out.append((hi, _pl(keys, hi)))
    return out


def drift(items, p0, p1, t0, dur, total=180, fade=0.22, s0=100, s1=100, r0=0, r1=0, peak=100,
          nm="particle"):
    """Particle that travels p0 -> p1 during [t0, t0+dur] (wrapping around the
    loop end), fading in/out.  Returns one or two groups."""
    t0 = t0 % total
    pk = [(t0, list(p0)), (t0 + dur, list(p1))]
    ok = [(t0, 0), (t0 + dur * fade, peak), (t0 + dur * (1 - fade), peak), (t0 + dur, 0)]
    sk = [(t0, [s0, s0]), (t0 + dur, [s1, s1])]
    rk = [(t0, r0), (t0 + dur, r1)]
    spans = [(t0, min(t0 + dur, total), 0)]
    if t0 + dur > total:
        spans.append((total, t0 + dur, -total))
    out = []
    for lo, hi, shift in spans:
        def mk(keys):
            w = _window(keys, lo, hi)
            return Anim(*[(t + shift, v, LIN) for t, v in w])
        out.append(group(list(items), nm, p=mk(pk), o=mk(ok), s=mk(sk), r=mk(rk)))
    return out
