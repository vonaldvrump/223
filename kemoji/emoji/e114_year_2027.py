"""114 · 2027 — crystal digits with snow caps that bounce in a wave, with
little fireworks above."""
import math

from .. import geom as G
from ..glyphs import glyphs
from ..lottie import IN, OUT, SINE, Anim, Comp, ellipse, fill, group
from ..style import (SKY, WHITE, dgrad, drift, glow, outlined, shape, sheen, snowfall, stack, twinkle, vgrad)

NAME = "year_2027"
TITLE = "2027"
EMOJI = "🎆"
HERO = 0

BASE = 352


def layout():
    probe = glyphs("2027", 0, BASE, 100, tracking=-4)
    width = probe[-1][2][2] - probe[0][2][0]
    cap = 100 * 446 / width
    return glyphs("2027", 0, BASE, cap, tracking=-4, center_x=256), cap


def snow_cap(x0, x1, y):
    w = x1 - x0
    pts = [(x0 - 4, y + 10), (x0 + w * 0.08, y - 12), (x0 + w * 0.5, y - 18), (x1 - w * 0.08, y - 12), (x1 + 4, y + 8),
           (x1 - w * 0.12, y + 16), (x1 - w * 0.26, y + 10), (x1 - w * 0.36, y + 30), (x1 - w * 0.48, y + 10),
           (x0 + w * 0.3, y + 14), (x0 + w * 0.18, y + 24), (x0 + w * 0.08, y + 12)]
    return G.smooth(pts, t=1.0)


def firework(cx, cy, t0, color, n=10, r0=12, r1=76, T=180):
    items = []
    for k in range(n):
        a = math.radians(k * 360 / n)
        p0 = (cx + math.cos(a) * r0, cy + math.sin(a) * r0)
        p1 = (cx + math.cos(a) * r1, cy + math.sin(a) * r1)
        items += drift([shape(G.circle(0, 0, 8 if k % 2 else 6), fill(color))], p0, p1, t0, 40, T, fade=0.15,
                       s0=120, s1=50)
    items.append(group([ellipse([cx, cy], [18, 18]), fill(WHITE)], "flash", o=Anim((t0, 0, OUT), (t0 + 6, 90, SINE),
                                                                                    (t0 + 18, 0))))
    return items


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 290, 220, SKY, 0.3, opacity=Anim((0, 70), (90, 100), (180, 70)))])
    c.add("fireworks", firework(118, 112, 30, "#c9b8ff") + firework(392, 112, 70, "#8fe3ff") +
          firework(256, 92, 118, "#ffd35a", n=12, r1=56))

    digits, cap = layout()
    groups = []
    for k, (ch, bs, (x0, y0, x1, y1)) in enumerate(digits):
        items = [outlined(bs, dgrad("#d6ecff", "#2a5fd0", (x0, y0), (x1, y1 + 20), mid="#6fadf6"), ow=12, nm="digit")]
        items.append(sheen(bs, 70 + k * 8, 104 + k * 8, angle=30, width=26, alpha=0.75))
        items.append(outlined(snow_cap(x0 + 4, x1 - 4, y0 + 6), vgrad(WHITE, "#d6e8fb", y0 - 14, y0 + 30), ow=7, nm="snow"))
        items.append(shape(G.circle(x0 + (x1 - x0) * 0.32, y0 - 4, 4), fill("#cfe3fa"), nm="dot"))
        t0 = 8 + k * 9
        hop = Anim((0, [0, 0]), (t0, [0, 0], OUT), (t0 + 12, [0, -26], IN), (t0 + 24, [0, 0], OUT),
                   (t0 + 30, [0, -5], SINE), (t0 + 36, [0, 0]), (180, [0, 0]))
        sq = Anim((0, [100, 100]), (t0 + 22, [100, 100], OUT), (t0 + 26, [106, 94], SINE), (t0 + 34, [100, 100]),
                  (180, [100, 100]))
        cx = (x0 + x1) / 2
        groups.append(stack(items, "d%d" % k, pivot=(cx, BASE), s=sq,
                            p=Anim(*[(t, [cx + v[0], BASE + v[1]], e) for t, v, e in hop.keys])))
    c.add("digits", groups)
    c.add("sparkles", [twinkle(50, 250, 16, 20, 30, halo=False), twinkle(470, 380, 16, 90, 30, halo=False),
                       twinkle(160, 440, 14, 140, 28, halo=False)])
    c.add("snow", snowfall([(60, 170, 0), (452, 200, 60), (300, 380, 120), (180, 400, 30)], T, dur=110, fall=90, r=11))
    return c
