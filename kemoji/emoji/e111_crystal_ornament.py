"""111 · Хрустальный шар — sapphire bauble with a jewelled platinum band,
swinging on its ribbon."""

from .. import geom as G
from ..gems import kite_gem, round_gem
from ..lottie import Anim, Comp, fill, stroke
from ..style import (INK, SILVER, SILVER_LO, SKY, WHITE, dgrad, glow, lines, outlined, shape, sheen, snowfall,
                     stack, twinkle, vgrad)

NAME = "crystal_ornament"
TITLE = "Хрустальный шар"
EMOJI = "🎄"
HERO = 145

BC = (256, 304)
BR = 146


def band_y(x, y_edge, y_mid):
    u = (x - BC[0]) / BR
    return y_edge + (y_mid - y_edge) * (1 - u * u)


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 300, 214, SKY, 0.33, opacity=Anim((0, 70), (90, 100), (180, 70)))])

    ball = G.circle(BC[0], BC[1], BR)
    flat = G.flatten(ball, 16)
    items = [outlined(ball, dgrad("#a6d4ff", "#1c46ad", (150, 170), (360, 450), mid="#3f82ee"), nm="ball")]
    # faint meridians of a cut-crystal ball
    mer = [G.svg("M 256 160 C 196 210 196 400 256 448")[0], G.svg("M 256 160 C 316 210 316 400 256 448")[0],
           G.svg("M 256 160 C 150 220 150 390 256 448")[0], G.svg("M 256 160 C 362 220 362 390 256 448")[0]]
    items.append(lines(mer, WHITE, 3, 28, nm="meridians"))

    xs = [BC[0] - BR + 4 + k * (2 * BR - 8) / 40 for k in range(41)]
    top = [(x, band_y(x, 276, 304)) for x in xs]
    bot = [(x, band_y(x, 316, 346)) for x in xs]
    band_poly = top + bot[::-1]
    band = G.poly(G.clip(band_poly, flat))
    items.append(outlined(band, vgrad(WHITE, SILVER_LO, 276, 346), ow=7, nm="band"))
    for k, x in enumerate((150, 203, 256, 309, 362)):
        u = abs(x - BC[0]) / BR
        y = band_y(x, 296, 325)
        w = 40 * (1 - 0.45 * u * u)
        if k % 2 == 0:
            g, _ = kite_gem(x, y, w, w * 1.05, "#d9eeff", "#4a8ff0", "#1f4dbb", ow=5)
        else:
            g, _ = round_gem(x, y, w * 0.42, WHITE, "#9fc6f2", ow=5)
        items.append(g)
    items.append(shape(G.svg("M 150 236 C 160 200 192 176 228 168 C 200 190 182 214 174 244 Z")[0],
                       fill(WHITE, 80), nm="hl"))
    items.append(shape(G.circle(330, 196, 9), fill(WHITE, 70), nm="hl2"))
    items.append(sheen(ball, 100, 140, angle=30, width=46, alpha=0.6))

    # cap and ribbon
    cap = G.rounded([(224, 140), (288, 140), (292, 172), (220, 172)], 8)
    items.append(outlined(cap, dgrad(WHITE, SILVER_LO, (220, 140), (292, 176), mid=SILVER), ow=8, nm="cap"))
    items.append(lines([G.line((238, 146), (238, 168)), G.line((256, 146), (256, 168)), G.line((274, 146), (274, 168))],
                       INK, 3, 40, nm="ridges"))
    items.append(shape(G.circle(256, 126, 14), stroke(INK, 14), nm="loop-ink"))
    items.append(shape(G.circle(256, 126, 14), stroke(SILVER, 7), nm="loop"))
    ribbon = G.line((256, 112), (256, 52))
    items.insert(0, shape(ribbon, stroke(INK, 16), nm="ribbon-ink"))
    items.insert(1, shape(ribbon, stroke("#7b5cf0", 8), nm="ribbon"))
    bow_l = G.svg("M 256 56 C 236 36 210 38 214 56 C 218 72 240 66 256 56 Z")[0]
    bow_r = G.mirror(bow_l)
    items.append(outlined([bow_l, bow_r], dgrad("#b9a8ff", "#6a4be0", (210, 36), (300, 72)), ow=6, nm="bow"))
    items.append(outlined(G.circle(256, 56, 8), fill("#e2d7ff"), ow=5, nm="knot"))

    for k, (x, t0) in enumerate(((150, 30), (203, 44), (256, 58), (309, 72), (362, 86))):
        items.append(twinkle(x - 6, band_y(x, 290, 318) - 6, 20, t0, 28))
    items.append(twinkle(190, 214, 30, 132, 32))
    c.add("ornament", [stack(items, "swing", pivot=(256, 56), r=Anim((0, -7), (90, 7), (180, -7)))])
    c.add("snow", snowfall([(70, 150, 0), (450, 120, 60), (90, 330, 120), (440, 340, 30), (60, 60, 90)],
                           T, dur=120, fall=110, r=12))
    return c
