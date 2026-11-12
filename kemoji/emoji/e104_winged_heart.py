"""104 · ★ Крылатое сердце — faceted sapphire-amethyst heart with flapping
platinum wings (special: made to be worn as an emoji status)."""
import math

from .. import geom as G
from ..lottie import IN, OUT, Anim, Comp, fill, stroke
from ..style import (WHITE, dgrad, drift, glow, lines, outlined, shape, sheen, stack, twinkle)

NAME = "winged_heart"
TITLE = "Крылатое сердце"
EMOJI = "💖"
HERO = 45
SPECIAL = True

CX, CY = 256, 258
N = 32


def heart_pts(k=8.0, ky=1.08, cx=CX, cy=CY):
    pts = []
    for j in range(N):
        t = 2 * math.pi * j / N
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * k, cy + y * k * ky))
    return pts


def sub(b, ia, ib):
    """Vertices ia..ib (inclusive, wrapping) of a closed bezier, open ends."""
    n = len(b["v"])
    idx = [ia]
    while idx[-1] != ib:
        idx.append((idx[-1] + 1) % n)
    v = [b["v"][i] for i in idx]
    ins = [b["i"][i] for i in idx]
    outs = [b["o"][i] for i in idx]
    ins[0] = [0, 0]
    outs[-1] = [0, 0]
    return v, ins, outs


def facet_path(outer, inner, ia, ib):
    v1, i1, o1 = sub(outer, ia, ib)
    v2, i2, o2 = sub(inner, ia, ib)
    v2, i2, o2 = v2[::-1], o2[::-1], i2[::-1]
    return G.bez(v1 + v2, True, i1 + i2, o1 + o2)


WING = ("M 190 198 C 162 150 104 110 46 98 C 30 95 22 110 32 121 C 42 132 56 140 68 146 "
        "C 50 152 42 166 50 177 C 60 190 84 194 100 194 C 84 206 80 224 92 232 "
        "C 106 242 128 242 144 238 C 134 252 138 270 154 276 C 170 282 186 280 198 272 Z")
FEATHERS = ["M 70 146 C 104 160 140 174 176 196", "M 100 194 C 128 204 152 214 178 228",
            "M 144 238 C 160 246 174 252 190 256"]


def wing(side):
    body = G.svg(WING)[0]
    fl = [G.svg(d)[0] for d in FEATHERS]
    if side > 0:
        body = G.mirror(body)
        fl = [G.mirror(b) for b in fl]
    x0 = 30 if side < 0 else 482
    items = [
        outlined(body, dgrad(WHITE, "#a9c3ee", (x0, 96), (256 - side * -60, 290), mid="#e3eeff"), nm="wing"),
        lines(fl, "#7d97c9", 6, 80, nm="feathers"),
        shape(G.svg("M 182 190 C 150 146 104 118 56 106" if side < 0 else
                    "M 330 190 C 362 146 408 118 456 106")[0], stroke(WHITE, 7, 90), nm="hl"),
    ]
    return items


def beat(t0):
    return [(t0, [100, 100], OUT), (t0 + 7, [109, 109], IN), (t0 + 15, [100, 100], OUT),
            (t0 + 22, [105, 105], IN), (t0 + 34, [100, 100])]


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 256, 226, "#a99bff", 0.36,
                        opacity=Anim((0, 60), (12, 100), (60, 70), (102, 100), (150, 70), (180, 60)))])

    outer = G.smooth(heart_pts(), sharp=(0, N // 2))
    inner = G.smooth(heart_pts(3.6, 1.08, CX, CY - 22), sharp=(0, N // 2))
    colors = ["#9db6ff", "#7b8ff2", "#6a5fe0", "#5a45cf", "#7d8cf6", "#8aa6ff", "#a9c6ff", "#cfe0ff"]
    heart = [outlined(outer, fill("#6d6fe6"), nm="heart")]
    step = N // 8
    for k in range(8):
        fb = facet_path(outer, inner, k * step, ((k + 1) * step) % N)
        x0, y0, x1, y1 = G.bbox(fb["v"])
        heart.append(shape(fb, dgrad(colors[k], colors[(k + 1) % 8], (x0, y0), (x1, y1)), nm="facet"))
    heart.append(shape(inner, dgrad("#e4e8ff", "#9c96f2", (220, 200), (290, 300)), nm="table"))
    spokes = [G.line(outer["v"][k * step], inner["v"][k * step]) for k in range(8)]
    heart.append(lines(spokes + [inner], WHITE, 3.5, 55, nm="edges"))
    heart.append(shape(G.svg("M 150 214 C 150 180 172 162 196 160 C 184 172 172 190 170 214 Z")[0],
                       fill(WHITE, 85), nm="hl"))
    heart.append(shape(G.circle(206, 178, 7), fill(WHITE, 95), nm="hl"))
    heart.append(sheen(outer, 120, 156, angle=30, width=38, alpha=0.65))
    heart.append(twinkle(176, 172, 30, 30, 32))
    heart.append(twinkle(330, 330, 22, 140, 30))

    hs = Anim(*(beat(4) + beat(94)[1:] + [(180, [100, 100])]))
    flap_l = Anim((0, -8), (45, 18), (90, -8), (135, 18), (180, -8))
    flap_r = flap_l.map(lambda v: -v)
    lw = stack(wing(-1), "wingL", pivot=(196, 240), r=flap_l)
    rw = stack(wing(1), "wingR", pivot=(316, 240), r=flap_r)
    fly = Anim((0, [256, 266]), (52, [256, 252]), (90, [256, 266]), (142, [256, 252]), (180, [256, 266]))
    c.add("heart", [stack([lw, rw, stack(heart, "gem", pivot=(256, 270), s=hs)], "fly", pivot=(256, 262), p=fly,
                          s=[88, 88])])

    dust = []
    for k, (x, t0) in enumerate([(226, 0), (290, 40), (250, 80), (276, 120), (236, 150)]):
        dust += drift([stack([shape(G.sparkle(10), fill(WHITE))])], (x, 400), (x + (-1) ** k * 18, 486),
                      t0, 70, T, r1=90, s0=100, s1=40)
    c.add("dust", dust)
    c.add("sparkles", [
        twinkle(82, 300, 16, 20, 30, halo=False),
        twinkle(440, 316, 18, 70, 32, halo=False),
        twinkle(420, 70, 16, 110, 28, halo=False),
        twinkle(96, 60, 14, 150, 28, halo=False),
    ])
    return c
