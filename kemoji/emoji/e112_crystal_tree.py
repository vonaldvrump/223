"""112 · Хрустальная ёлка — ice-crystal fir with twinkling garland lights and a
shining crystal star."""

from .. import geom as G
from ..lottie import OUT, SINE, Anim, Comp, fill
from ..style import (SKY, WHITE, blink, dgrad, glow, lines, outlined, shape, sheen, snowfall, stack, twinkle, vgrad)

NAME = "crystal_tree"
TITLE = "Хрустальная ёлка"
EMOJI = "🎄"
HERO = 48

TIERS = [  # apex_y, base_y, half width at base
    (200, 398, 150),
    (138, 302, 112),
    (86, 212, 76),
]
BULB_COLORS = ["#ffffff", "#ffd35a", "#c9b8ff", "#ff9fd2", "#8fe3ff"]


def tier(apex_y, base_y, hw):
    pts = [(256, apex_y), (256 + hw, base_y), (256 - hw, base_y)]
    return G.rounded(pts, [16, 22, 22])


def snow_cap(base_y, hw, n):
    """Wavy snow band hugging the bottom of a tier."""
    top = base_y - 18
    x0, x1 = 256 - hw + 14, 256 + hw - 14
    pts = [(x0 - 6, base_y - 6), (x0 + 10, top + 6)]
    pts.append((x1 - 10, top + 6))
    pts.append((x1 + 6, base_y - 6))
    for k in range(n, -1, -1):
        x = x0 + (x1 - x0) * k / n
        pts.append((x, base_y + (10 if k % 2 == 0 else 1)))
    return G.smooth(pts, t=1.0)


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 270, 220, SKY, 0.3, opacity=Anim((0, 70), (90, 100), (180, 70)))])

    items = []
    mound = G.svg("M 96 444 C 110 414 180 404 256 404 C 332 404 402 414 416 444 Z")[0]
    trunk = G.rounded([(232, 384), (280, 384), (280, 424), (232, 424)], 6)
    items.append(outlined(trunk, dgrad("#7a8fbd", "#3b4f86", (232, 384), (280, 424)), ow=8, nm="trunk"))
    items.append(outlined(mound, vgrad(WHITE, "#cfe3fa", 404, 444), ow=9, nm="mound"))

    bulb_specs = []
    for k, (ay, by, hw) in enumerate(TIERS):
        t = tier(ay, by, hw)
        items.append(outlined(t, dgrad("#bfe4ff", "#1f4dbb", (256 - hw, ay), (256 + hw * 0.6, by + 10), mid="#4a8ff0"),
                              nm="tier"))
        # right half a touch darker -> faceted crystal look
        flat = G.flatten(t, 12)
        half = G.poly(G.clip(flat, [(256, ay - 10), (256 + hw + 20, ay - 10), (256 + hw + 20, by + 20), (256, by + 20)]))
        items.append(shape(half, fill("#0b2a7a", 16), nm="shade"))
        items.append(lines([G.line((256, ay + 12), (256, by - 18))], WHITE, 3, 35, nm="ridge"))
        items.append(outlined(snow_cap(by, hw, 6 if k == 0 else 4), vgrad(WHITE, "#d9eafc", by - 18, by + 10), ow=6,
                              nm="snow"))
        # garland across the tier
        ya = ay + (by - ay) * 0.55
        wa = hw * 0.55
        g = G.svg("M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f" % (256 - wa, ya - 8, 236, ya + 24, 276, ya + 24, 256 + wa,
                                                                   ya - 14))[0]
        items.append(lines(g, WHITE, 4, 70, nm="garland"))
        pts = G.flatten(g, 24)
        n_b = 3 + k % 2 if k < 2 else 2
        for j in range(n_b + 1):
            if k == 2 and j == 1:
                continue
            p = pts[int(j * (len(pts) - 1) / n_b)]
            bulb_specs.append(p)

    for j, (x, y) in enumerate(bulb_specs):
        col = BULB_COLORS[j % len(BULB_COLORS)]
        t0 = (j * 23) % 150
        items.append(glow(x, y, 26, col, 0.8, opacity=blink(t0, 40, 15, 100)))
        items.append(outlined(G.circle(x, y, 9.5), fill(col), ow=4, nm="bulb"))
        items.append(shape(G.circle(x - 3, y - 3, 3), fill(WHITE, 90), nm="bhl"))

    items.append(sheen([tier(*tt) for tt in TIERS], 110, 150, angle=30, width=44, alpha=0.5))

    # crystal star topper
    sp = G.star_points(256, 76, 48, 23, 5, -90)
    star = G.rounded(sp, [10 if k % 2 == 0 else 4 for k in range(10)])
    sflat = G.flatten(star, 10)
    star_items = [glow(256, 76, 60, "#fff4c2", 0.75, opacity=Anim((0, 60), (45, 100), (90, 60), (135, 100), (180, 60))),
                  outlined(star, fill("#ffe58a"), ow=8, nm="star")]
    for k in range(5):
        tip = sp[2 * k]
        star_items.append(shape(G.poly(G.clip(sflat, [(256, 76), tip, sp[(2 * k + 1) % 10]])), fill("#ffcf4d"), nm="f"))
        star_items.append(shape(G.poly(G.clip(sflat, [(256, 76), sp[(2 * k - 1) % 10], tip])), fill("#fff6cf"), nm="f"))
    star_items.append(twinkle(240, 56, 22, 30, 30))
    items.append(stack(star_items, "topper", pivot=(256, 76),
                       r=Anim((0, -6), (90, 6), (180, -6)),
                       s=Anim((0, [100, 100]), (40, [100, 100], OUT), (48, [112, 112], SINE), (64, [100, 100]),
                              (180, [100, 100]))))
    c.add("tree", [stack(items, "tree", pivot=(256, 440), r=Anim((0, -1.5), (90, 1.5), (180, -1.5)))])
    c.add("snow", snowfall([(70, 120, 0), (446, 160, 50), (96, 300, 100), (430, 330, 140), (380, 60, 20)],
                           T, dur=120, fall=110, r=12))
    return c
