"""120 · ★ Снежный шар — crystal globe with a glowing diamond over a snowy
hill, swirling snow and a "2027" plaque (special: profile-worthy)."""

from .. import geom as G
from ..gems import brilliant
from ..glyphs import text_paths
from ..lottie import SINE, Anim, Comp, fill, gradient, stroke
from ..style import (DEEP, INK, SILVER, SILVER_LO, WHITE, dgrad, drift, glow, outlined, shape, sheen, stack, twinkle,
                     vgrad)

NAME = "snow_globe"
TITLE = "Снежный шар"
EMOJI = "🔮"
HERO = 60
SPECIAL = True

GC = (256, 222)
GR = 150


def fir(x, base, h, w):
    pts = [(x, base - h), (x + w / 2, base - h * 0.42), (x + w * 0.3, base - h * 0.44), (x + w / 2, base),
           (x - w / 2, base), (x - w * 0.3, base - h * 0.44), (x - w / 2, base - h * 0.42)]
    return G.rounded(pts, [5, 4, 0, 4, 4, 0, 4])


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 250, 224, "#a9c8ff", 0.33, opacity=Anim((0, 70), (90, 100), (180, 70)))])

    globe = G.circle(GC[0], GC[1], GR)
    gflat = G.flatten(globe, 20)
    scene = [shape(globe, gradient([(0, "#5d9cf5"), (0.65, "#2a5fd0"), (1, "#173a8f")], [GC[0] - 30, GC[1] - 70],
                                   [GC[0] + 160, GC[1]], radial=True), nm="sky")]
    for x, y, r in ((190, 120, 3), (322, 140, 2.5), (214, 170, 2), (350, 196, 2), (160, 206, 2.2), (300, 104, 2)):
        scene.append(shape(G.circle(x, y, r), fill(WHITE, 70), nm="star"))
    hill_clip = [(100, 330), (150, 304), (210, 292), (256, 290), (302, 292), (362, 304), (412, 330), (412, 380), (100, 380)]
    ground = G.poly(G.clip(gflat, hill_clip))
    scene.append(shape(ground, vgrad(WHITE, "#cfe3fa", 290, 372), nm="ground"))
    for x, h, w in ((176, 74, 52), (340, 62, 44)):
        scene.append(outlined(fir(x, 312, h, w), dgrad("#8fd0e6", "#1f6d8f", (x - w / 2, 312 - h), (x + w / 2, 312)), ow=5,
                              nm="fir"))
        scene.append(shape(G.poly([(x, 312 - h), (x + w * 0.24, 312 - h * 0.6), (x - w * 0.24, 312 - h * 0.6)]),
                           fill(WHITE, 90), nm="firsnow"))
    gem, gem_o = brilliant(256, 214, 54, "blue", wave=40, step=6, ow=8)
    scene.append(stack([glow(256, 236, 92, WHITE, 0.7, opacity=Anim((0, 60), (90, 100), (180, 60))), gem,
                        sheen(gem_o, 120, 150, angle=30, width=24, alpha=0.8), twinkle(232, 196, 22, 70, 30)],
                       "gem", pivot=(256, 240), p=Anim((0, [256, 246]), (90, [256, 232]), (180, [256, 246])),
                       r=Anim((0, -4), (90, 4), (180, -4))))
    for k, (x, y0, t0) in enumerate([(184, 118, 0), (226, 104, 20), (270, 112, 40), (314, 120, 60), (200, 140, 80),
                                     (292, 132, 100), (244, 120, 120), (330, 150, 140), (176, 150, 160),
                                     (258, 100, 30), (210, 126, 110), (300, 108, 150)]):
        dx = 12 if k % 2 else -12
        scene += drift([shape(G.circle(0, 0, 6 if k % 3 == 0 else 4.5), fill(WHITE))], (x, y0), (x + dx, 300), t0, 110, T,
                       fade=0.2)

    base = G.rounded([(130, 352), (382, 352), (414, 446), (98, 446)], [10, 10, 14, 14])
    items = [outlined(base, dgrad("#4a8ff0", "#142f7c", (110, 352), (330, 456)), nm="base")]
    items.append(outlined(G.rounded([(116, 340), (396, 340), (396, 366), (116, 366)], 12), vgrad(WHITE, SILVER_LO, 340, 366),
                          ow=8, nm="collar"))
    items.append(outlined(G.rounded([(90, 432), (422, 432), (422, 456), (90, 456)], 12), vgrad(WHITE, SILVER_LO, 432, 456),
                          ow=8, nm="foot"))
    plaque = G.rounded([(196, 380), (316, 380), (316, 418), (196, 418)], 10)
    items.append(outlined(plaque, dgrad(WHITE, SILVER, (196, 380), (316, 418)), ow=6, nm="plaque"))
    items.append(shape(text_paths("2027", 0, 410, 22, tracking=2, center_x=256), fill(DEEP), nm="year"))
    items.append(sheen(base, 30, 66, angle=30, width=34, alpha=0.5))

    glass = [stack(scene, "scene"),
             shape(G.circle(GC[0], GC[1], GR - 10), stroke(WHITE, 4, 35), nm="rim"),
             shape(G.svg("M 136 200 C 140 150 172 108 220 90 C 186 122 164 160 158 206 Z")[0], fill(WHITE, 60), nm="hl"),
             shape(G.circle(340, 128, 10), fill(WHITE, 55), nm="hl2"),
             sheen(globe, 96, 132, angle=30, width=50, alpha=0.35),
             shape(globe, stroke(INK, 13 * 2), nm="outline-under")]
    # outline must sit under the glass content -> draw it first, then the rest
    glass = [glass[-1]] + glass[:-1]
    shake = Anim((0, 0), (6, -3, SINE), (14, 3, SINE), (22, -2, SINE), (30, 1.5, SINE), (38, 0), (180, 0))
    c.add("globe", [stack([stack(glass, "glass")] + items + [twinkle(152, 168, 26, 100, 30), twinkle(352, 96, 18, 150, 26)],
                          "globe", pivot=(256, 456), r=shake)])
    c.add("sparkles", [twinkle(64, 120, 16, 30, 30, halo=False), twinkle(448, 210, 18, 80, 30, halo=False),
                       twinkle(456, 420, 14, 130, 28, halo=False), twinkle(56, 400, 14, 160, 20, halo=False)])
    return c
