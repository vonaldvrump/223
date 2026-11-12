"""117 · Бокалы — two crystal flutes of champagne clink with a golden splash."""
from .. import geom as G
from ..lottie import IN, LIN, OUT, SINE, Anim, Comp, fill, group, stroke
from ..style import (INK, SILVER, WHITE, arc_keys, dgrad, drift, glow, lines, outlined, shape, stack, twinkle,
                     vgrad)

NAME = "champagne"
TITLE = "Бокалы"
EMOJI = "🥂"
HERO = 44

BOWL = "M -50 -170 L 50 -170 C 52 -100 44 -40 0 -22 C -44 -40 -52 -100 -50 -170 Z"
LEVEL = -128
SCALE = 82


def glass(side, T):
    bowl = G.svg(BOWL)[0]
    flat = G.flatten(bowl, 16)
    liquid = G.poly(G.clip(flat, [(-80, LEVEL), (80, LEVEL), (80, 0), (-80, 0)]))
    items = [
        outlined(G.rounded([(-6, -26), (6, -26), (6, 104), (-6, 104)], 4), vgrad(WHITE, SILVER, -26, 104), ow=7, nm="stem"),
        outlined(G.circle(0, 110, 52, 13), vgrad(WHITE, "#b9cdee", 97, 123), ow=8, nm="foot"),
        outlined(bowl, fill("#e8f4ff", 100), nm="glass"),
        shape(liquid, dgrad("#fff2b8", "#f0a93a", (-40, LEVEL), (30, -22), mid="#ffd35a"), nm="wine"),
        shape(G.svg("M -44 %d C -20 %d 20 %d 44 %d" % (LEVEL, LEVEL + 7, LEVEL + 7, LEVEL))[0], stroke(WHITE, 5, 85),
              nm="surface"),
    ]
    for k, (x, t0) in enumerate([(-14, 0), (10, 36), (-4, 72), (16, 108), (-18, 144)]):
        items += drift([shape(G.circle(0, 0, 5 if k % 2 else 3.5), fill(WHITE, 90))], (x, -40), (x + (-1) ** k * 6, LEVEL + 8),
                       t0, 52, T, fade=0.15, s0=70, s1=120)
    items += [
        shape(G.svg("M -36 -160 C -38 -112 -32 -74 -18 -50")[0], stroke(WHITE, 9, 85), nm="hl"),
        shape(G.svg("M 38 -158 C 40 -130 38 -112 34 -98")[0], stroke(WHITE, 5, 60), nm="hl2"),
        lines(G.svg("M -50 -170 L 50 -170")[0], WHITE, 4, 70, nm="lip"),
    ]
    if side > 0:
        items.append(outlined(G.svg("M -6 56 C -26 46 -40 58 -30 70 C -22 78 -10 70 -6 62 Z")[0],
                              dgrad("#a9d6ff", "#2f6be0", (-40, 46), (0, 80)), ow=5, nm="ribbon"))
    return items


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 300, 220, "#ffe9a8", 0.26, opacity=Anim((0, 60), (32, 100), (90, 70), (180, 60)))])
    rot_l = Anim((0, 7, SINE), (26, 18.5, IN), (30, 18, OUT), (36, 15, SINE), (46, 18, SINE), (128, 18, SINE),
                 (168, 7, SINE), (180, 7))
    pos_l = Anim((0, [130, 444], SINE), (26, [146, 444], IN), (30, [147, 444], OUT), (36, [142, 444], SINE),
                 (46, [146, 444], SINE), (128, [146, 444], SINE), (168, [130, 444], SINE), (180, [130, 444]))
    left = stack(glass(-1, T), "left", a=(0, 110), p=pos_l, r=rot_l, s=[SCALE, SCALE])
    right = stack(glass(1, T), "right", a=(0, 110), p=pos_l.map(lambda v: [512 - v[0], v[1]]),
                  r=rot_l.map(lambda v: -v), s=[SCALE, SCALE])
    c.add("glasses", [stack([left, right], "pair")])

    splash = []
    colors = ["#ffd35a", "#fff2b8", "#ffd35a", WHITE, "#ffd35a", "#fff2b8"]
    for k, (dx, h) in enumerate([(-110, 90), (-70, 130), (-30, 150), (34, 146), (76, 126), (114, 92)]):
        keys = arc_keys((256, 234), (256 + dx, 300), h, 30, 76, 10)
        op = Anim((30, 0, LIN), (33, 100, LIN), (62, 100, LIN), (76, 0))
        splash.append(group([shape(G.circle(0, 0, 9 if k % 2 else 7), fill(colors[k])),
                             shape(G.circle(0, 0, 9 if k % 2 else 7), stroke(INK, 3))], "drop", p=Anim(*keys), o=op))
    c.add("splash", splash)
    c.add("clink", [glow(256, 230, 70, WHITE, 0.9, opacity=Anim((0, 0), (28, 0, OUT), (32, 100, SINE), (56, 0), (180, 0))),
                    twinkle(256, 226, 46, 28, 30), twinkle(214, 172, 18, 40, 26), twinkle(300, 168, 20, 46, 26),
                    twinkle(96, 120, 16, 110, 28, halo=False), twinkle(420, 108, 18, 140, 28, halo=False)])
    return c
