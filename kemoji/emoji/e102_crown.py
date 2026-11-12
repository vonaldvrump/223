"""102 · Алмазная корона — platinum crown with sapphires and pearls."""
from .. import geom as G
from ..gems import kite_gem, round_gem
from ..lottie import Anim, Comp, fill
from ..style import (DEEP, INK, MID, SILVER, SILVER_LO, SKY, WHITE, bob, dgrad, glow, outlined,
                     shape, sheen, stack, sway, twinkle, vgrad)

NAME = "crown"
TITLE = "Алмазная корона"
EMOJI = "👑"
HERO = 58

TIPS = [(90, 178), (186, 146), (256, 104), (326, 146), (422, 178)]
VALLEYS = [(166, 238), (222, 224), (290, 224), (346, 238)]


def crown_body():
    pts = [(126, 312), TIPS[0], VALLEYS[0], TIPS[1], VALLEYS[1], TIPS[2], VALLEYS[2], TIPS[3],
           VALLEYS[3], TIPS[4], (386, 312)]
    radii = [6, 12, 9, 12, 9, 12, 9, 12, 9, 12, 6]
    return G.rounded(pts, radii)


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 250, 220, SKY, 0.33, opacity=Anim((0, 70), (90, 100), (180, 70)))])

    body = crown_body()
    items = [outlined(body, vgrad(WHITE, SILVER, 110, 312), nm="body")]
    # darker right half of every spike -> faceted metal
    flat = G.flatten(body, 12)
    halves = []
    for k, tip in enumerate(TIPS):
        right = VALLEYS[k] if k < 4 else (386, 312)
        tri = [tip, right, (right[0], 320), (tip[0], 320)] if k < 4 else [tip, (440, 320), (tip[0], 320)]
        halves.append(G.poly(G.clip(flat, tri)))
    items.append(shape(halves, fill(SILVER_LO, 38), nm="shade"))
    items.append(shape(G.poly([(118, 190), (128, 206), (160, 236), (150, 240)]), fill(WHITE, 70), nm="hl"))

    gem, _ = kite_gem(256, 204, 50, 70, "#bfe0ff", "#4a8ff0", "#1f4dbb", ow=7)
    items.append(gem)
    for x in (186, 326):
        g, _ = round_gem(x, 230, 13, "#d9ccff", "#7b5cf0", ow=6)
        items.append(g)

    # pearls on the tips
    for k, (x, y) in enumerate(TIPS):
        r = 19 if k == 2 else 16
        g, _ = round_gem(x, y - 8, r, WHITE, "#b8cdee", ow=7, star=False)
        items.append(g)

    band = G.rounded([(108, 292), (404, 292), (404, 364), (108, 364)], 24)
    items.append(outlined(band, dgrad(MID, DEEP, (108, 292), (300, 380)), nm="band"))
    items.append(shape(G.rounded([(126, 302), (386, 302), (386, 312), (126, 312)], 5), fill(WHITE, 45), nm="bandhl"))
    g, _ = kite_gem(256, 328, 64, 46, WHITE, "#d3e9ff", "#8cc4fb", ow=7)
    items.append(g)
    for x, cl, cd in ((168, "#c9f2ff", "#2aa3d8"), (344, "#c9f2ff", "#2aa3d8")):
        g, _ = round_gem(x, 328, 15, cl, cd, ow=6)
        items.append(g)
    for x in (126, 212, 300, 386):
        items.append(outlined(G.circle(x, 328, 6), fill(WHITE), ow=4, ink=INK))

    items += [
        sheen(band, 20, 56, angle=25, width=34, alpha=0.6),
        sheen(body, 96, 138, angle=25, width=44, alpha=0.65),
        twinkle(240, 186, 30, 40, 32),
        twinkle(256, 78, 26, 66, 30),
        twinkle(330, 318, 24, 98, 30),
        twinkle(176, 318, 20, 112, 28),
        twinkle(90, 160, 20, 136, 28),
        twinkle(422, 160, 20, 148, 28),
    ]
    c.add("crown", [stack(items, "crown", pivot=(256, 330), p=bob(256, 336, 6, T), r=sway(3, T), s=[108, 108])])
    c.add("sparkles", [
        twinkle(150, 70, 16, 10, 30, halo=False),
        twinkle(376, 64, 20, 56, 32, halo=False),
        twinkle(462, 270, 14, 118, 28, halo=False),
        twinkle(52, 282, 14, 150, 28, halo=False),
    ])
    return c
