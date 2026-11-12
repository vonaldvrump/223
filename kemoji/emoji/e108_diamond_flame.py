"""108 · Алмазное пламя — a living three-layer blue flame with a diamond heart."""
import math

from .. import geom as G
from ..gems import brilliant
from ..lottie import LIN, Anim, Comp, fill, group, path, stroke
from ..style import INK, OW, WHITE, drift, glow, shape, stack, twinkle, vgrad

NAME = "diamond_flame"
TITLE = "Алмазное пламя"
EMOJI = "🔥"
HERO = 72

OUTER = [(256, 454), (170, 432), (114, 360), (118, 270), (152, 204), (180, 252), (210, 160), (256, 54),
         (300, 150), (332, 250), (360, 200), (394, 270), (398, 360), (342, 432)]
MIDDLE = [(256, 448), (196, 430), (162, 374), (170, 302), (198, 252), (214, 288), (236, 200), (256, 136),
          (276, 196), (298, 286), (318, 246), (346, 300), (350, 374), (316, 430)]
CORE = [(256, 446), (212, 432), (194, 386), (204, 330), (234, 272), (256, 220), (278, 272), (308, 330),
        (318, 386), (300, 432)]


def flicker(points, sharp, amp, phase, T=180, step=12, base_y=430):
    keys = []
    for t in range(0, T + 1, step):
        pts = []
        for i, (x, y) in enumerate(points):
            k = amp * (1.0 if i in sharp else 0.55) * max(0.0, min(1.0, (base_y - y) / 160 + 0.25))
            a = 2 * math.pi * t / 90 + phase + i * 1.7
            b = 2 * math.pi * t / 60 + phase * 1.3 + i * 0.9
            dx = k * (0.65 * math.sin(a) + 0.35 * math.sin(b))
            dy = k * 0.6 * (0.5 * math.cos(a * 1.0) + 0.5 * math.sin(b))
            pts.append((x + dx, y + dy))
        keys.append((t, G.smooth(pts, sharp=sharp), LIN))
    return Anim(*keys)


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 300, 214, "#7fc0ff", 0.36, opacity=Anim((0, 70), (45, 100), (90, 70), (135, 100), (180, 70)))])

    outer = group([path(flicker(OUTER, (4, 7, 10), 21, 0.0, T)),
                   vgrad("#6fb3ff", "#2150c6", 60, 450), stroke(INK, OW * 2)], "outer")
    middle = group([path(flicker(MIDDLE, (4, 7, 10), 17, 1.3, T)), vgrad("#c6e4ff", "#5a9cf5", 140, 446)], "middle")
    core = group([path(flicker(CORE, (5,), 12, 2.6, T)), vgrad(WHITE, "#d2eaff", 222, 444)], "core")
    gem, outline = brilliant(256, 376, 50, "blue", wave=34, step=6, ow=8)
    heart = stack([glow(256, 384, 96, WHITE, 0.8, opacity=Anim((0, 70), (45, 100), (90, 70), (135, 100), (180, 70))),
                   gem, twinkle(222, 352, 22, 60, 30), twinkle(294, 396, 18, 130, 28)], "heart",
                  pivot=(256, 380), p=Anim((0, [256, 382]), (90, [256, 374]), (180, [256, 382])))
    flame = stack([outer, middle, core, heart], "flame", pivot=(256, 454),
                  s=Anim((0, [100, 100]), (45, [103, 97]), (90, [98, 103]), (135, [103, 97]), (180, [100, 100])))
    c.add("flame", [flame])

    embers = []
    for k, (x, t0) in enumerate([(226, 0), (290, 30), (246, 60), (304, 90), (214, 120), (272, 150)]):
        embers += drift([shape(G.sparkle(12 if k % 2 else 9), fill(WHITE))], (x, 250), (x + (-1) ** k * 26, 70),
                        t0, 64, T, fade=0.2, s0=110, s1=40, r1=120)
    c.add("embers", embers)
    c.add("sparkles", [twinkle(96, 130, 16, 20, 30, halo=False), twinkle(420, 116, 18, 80, 30, halo=False),
                       twinkle(440, 380, 14, 140, 28, halo=False)])
    return c
