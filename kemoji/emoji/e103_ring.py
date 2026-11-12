"""103 · Кольцо с бриллиантом — platinum ring, big brilliant, travelling glints."""
from .. import geom as G
from ..gems import brilliant
from ..lottie import Anim, Comp, fill, stroke
from ..style import (INK, OW, SILVER, SILVER_LO, SKY, WHITE, bob, dgrad, glow, outlined, shape, sheen,
                     stack, sway, twinkle)
from ..lottie import gradient, group, path

NAME = "ring"
TITLE = "Кольцо с бриллиантом"
EMOJI = "💍"
HERO = 66


def band():
    outer = G.circle(256, 350, 138, 118)
    inner = G.circle(256, 360, 98, 80)
    return outer, inner


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 268, 220, SKY, 0.33, opacity=Anim((0, 70), (90, 100), (180, 70)))])

    outer, inner = band()
    items = []
    # band (even-odd fill makes the hole)
    items.append(group([path(outer), path(inner),
                        gradient([(0, WHITE), (0.45, SILVER), (1, SILVER_LO)], [150, 240], [360, 470], rule=2),
                        stroke(INK, OW * 2)], "band"))
    # inner surface of the far side of the band
    items.append(group([path(inner), path(G.circle(256, 372, 92, 66)), fill("#8ea6cf", 100, rule=2)], "inside"))
    items.append(group([path(inner), stroke(INK, 8)], "inner-line"))
    # specular arcs on the band
    items.append(shape(G.svg("M 150 290 C 170 262 206 246 240 242")[0],
                       stroke(WHITE, 12, 85), nm="arc"))
    items.append(shape(G.svg("M 372 392 C 362 418 342 434 318 444")[0], stroke(WHITE, 8, 55), nm="arc"))
    items.append(sheen([outer, inner], 64, 104, angle=35, width=40, alpha=0.6, rule=2))

    # small cup setting under the stone; only the culet hides inside it
    cup = G.rounded([(194, 206), (318, 206), (288, 270), (224, 270)], [10, 10, 12, 12])
    gem, gem_outline = brilliant(256, 142, 102, "blue", wave=20, step=5)
    items.append(gem)
    for s in (-1, 1):
        claw = G.line((256 + s * 62, 216), (256 + s * 94, 146))
        items.append(shape(claw, stroke(INK, 30), nm="claw"))
        items.append(shape(claw, stroke(SILVER, 17), nm="claw"))
        items.append(shape(G.line((256 + s * 66, 204), (256 + s * 88, 156)), stroke(WHITE, 6, 90), nm="clawhl"))
    items.append(outlined(cup, dgrad(WHITE, SILVER_LO, (200, 206), (300, 270)), nm="cup"))
    items.append(shape(G.rounded([(210, 213), (302, 213), (298, 220), (214, 220)], 3), fill(WHITE, 75), nm="cuphl"))
    items.append(sheen(gem_outline, 112, 146, angle=30, width=30, alpha=0.7))

    items += [
        twinkle(196, 108, 44, 52, 34),
        twinkle(356, 146, 30, 134, 32),
        twinkle(140, 286, 22, 94, 30),
    ]
    c.add("ring", [stack(items, "ring", pivot=(256, 300), p=bob(256, 300, 7, T), r=sway(4, T))])
    c.add("sparkles", [
        twinkle(96, 96, 18, 14, 30, halo=False),
        twinkle(430, 86, 22, 70, 32, halo=False),
        twinkle(452, 300, 14, 118, 28, halo=False),
        twinkle(60, 360, 14, 148, 28, halo=False),
    ])
    return c
