"""105 · Кристальная звезда — faceted star that jumps, spins and lands with a burst."""
import math

from .. import geom as G
from ..lottie import IN, OUT, SINE, Anim, Comp, fill
from ..style import (SKY, WHITE, drift, glow, lines, outlined, shape, sheen, stack, twinkle)

NAME = "crystal_star"
TITLE = "Кристальная звезда"
EMOJI = "⭐"
HERO = 140

C = (256, 272)
LIGHT = (-0.55, -0.84)


def mix(c0, c1, f):
    a = [int(c0[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(x + (y - x) * f) for x, y in zip(a, b))


def star_items():
    pts = G.star_points(C[0], C[1], 200, 98, 5, -90)
    outline = G.rounded(pts, [30 if k % 2 == 0 else 10 for k in range(10)])
    flat = G.flatten(outline, 14)
    items = [outlined(outline, fill("#7fb0f0"), nm="star")]
    ridges = []
    for k in range(5):
        tip = pts[2 * k]
        ax = ((tip[0] - C[0]), (tip[1] - C[1]))
        al = math.hypot(*ax)
        ax = (ax[0] / al, ax[1] / al)
        for side in (-1, 1):
            inner = pts[(2 * k + side) % 10]
            v = (inner[0] - C[0], inner[1] - C[1])
            d = v[0] * ax[0] + v[1] * ax[1]
            n = (v[0] - d * ax[0], v[1] - d * ax[1])
            nl = math.hypot(*n)
            b = (n[0] * LIGHT[0] + n[1] * LIGHT[1]) / nl
            f = (b + 1) / 2
            light = mix("#5b92e6", "#f4faff", f)
            tri = [C, tip, inner] if side > 0 else [C, inner, tip]
            fb = G.poly(G.clip(flat, tri))
            x0, y0, x1, y1 = G.bbox(fb["v"])
            items.append(shape(fb, fill(light), nm="facet"))
        ridges.append(G.line(C, (C[0] + ax[0] * 172, C[1] + ax[1] * 172)))
    items.append(lines(ridges, WHITE, 4, 60, nm="ridges"))
    items.append(shape(G.svg("M 236 120 C 240 104 248 96 256 92 L 252 150 Z")[0], fill(WHITE, 80), nm="hl"))
    items.append(sheen(outline, 120, 156, angle=30, width=40, alpha=0.7))
    return items, outline


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 268, 214, SKY, 0.33,
                        opacity=Anim((0, 70), (70, 70), (78, 100), (120, 75), (180, 70)))])
    items, outline = star_items()
    spin = Anim((0, [100, 100]), (22, [100, 100], SINE), (46, [-100, 100], SINE), (70, [100, 100]),
                (180, [100, 100]))
    inner = stack(items + [twinkle(256, 84, 26, 128, 30), twinkle(446, 210, 22, 146, 28)],
                  "spin", pivot=C, s=spin)
    jump = Anim((0, [256, 272]), (16, [256, 278], OUT), (22, [256, 278], OUT), (46, [256, 226], IN),
                (70, [256, 272]), (180, [256, 272]))
    squash = Anim((0, [100, 100]), (16, [106, 94], OUT), (24, [96, 106], SINE), (66, [100, 100], OUT),
                  (72, [110, 90], OUT), (82, [97, 104], SINE), (94, [100, 100]), (180, [100, 100]))
    c.add("star", [stack([inner], "jump", pivot=(256, 440), p=Anim(*[(t, [v[0], v[1] + 168], e)
                                                                       for t, v, e in jump.keys]), s=squash)])
    burst = []
    for k in range(8):
        a = math.radians(-90 + k * 45 + 22.5)
        p0 = (256 + math.cos(a) * 150, 272 + math.sin(a) * 150)
        p1 = (256 + math.cos(a) * 226, 272 + math.sin(a) * 210)
        burst += drift([shape(G.sparkle(14 if k % 2 else 10), fill(WHITE))], p0, p1, 70, 40, T,
                       fade=0.15, s0=60, s1=120, r1=90)
    c.add("burst", burst)
    return c
