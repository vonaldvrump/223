"""107 · Сундук с сокровищами — the lid flips open, light pours out and gems
jump out and fall back in."""
import math

from .. import geom as G
from ..gems import brilliant, kite_gem, round_gem
from ..lottie import HOLD, IN, LIN, OUT, SINE, Anim, Comp, ellipse, fill, gradient, group, path, stroke
from ..style import (INK, SILVER_LO, SKY, WHITE, arc_keys, dgrad, glow, lines, outlined, shape, sheen,
                     stack, twinkle, vgrad)

NAME = "treasure_chest"
TITLE = "Сундук с сокровищами"
EMOJI = "🧰"
HERO = 72

HINGE = 258


def strap(x0, x1, y0, y1, clip_to=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    if clip_to is not None:
        return G.poly(G.clip(G.flatten(clip_to, 12), pts))
    return G.rounded(pts, 4)


def closed_lid():
    lid = G.svg("M 100 266 L 100 214 C 100 180 128 158 162 158 L 350 158 C 384 158 412 180 412 214 L 412 266 Z")[0]
    items = [outlined(lid, dgrad("#8cc4ff", "#2a5fd0", (120, 158), (300, 280)), nm="lid")]
    items.append(lines([G.svg("M 104 214 L 408 214")[0]], INK, 5, 30, nm="plank"))
    straps = [strap(136, 166, 150, 270, lid), strap(346, 376, 150, 270, lid)]
    items.append(outlined(straps, dgrad(WHITE, SILVER_LO, (136, 158), (170, 270)), ow=5, nm="straps"))
    items.append(shape(G.svg("M 124 206 C 126 186 140 174 162 172 L 220 172")[0],
                       stroke(WHITE, 9, 80), nm="hl"))
    rim = G.rounded([(92, 248), (420, 248), (420, 272), (92, 272)], 10)
    items.append(outlined(rim, vgrad(WHITE, SILVER_LO, 248, 272), ow=7, nm="rim"))
    items.append(sheen(lid, 140, 176, angle=30, width=40, alpha=0.6))
    return items


def open_lid():
    face = G.rounded([(108, 252), (404, 252), (426, 124), (86, 124)], [6, 6, 16, 16])
    items = [outlined(face, dgrad("#3a73dc", "#163a8f", (100, 250), (300, 110)), nm="inner")]
    items.append(lines([G.line((100, 210), (412, 210)), G.line((94, 168), (418, 168))], INK, 5, 30, nm="planks"))
    items.append(shape(face, gradient([(0, "#cfe8ff", 0.65), (1, "#cfe8ff", 0)], [256, 252], [256, 150]), nm="lit"))
    rim = G.rounded([(80, 112), (432, 112), (432, 134), (80, 134)], 10)
    items.append(outlined(rim, vgrad(WHITE, SILVER_LO, 112, 134), ow=7, nm="rim"))
    return items


def box():
    body = G.rounded([(100, 262), (412, 262), (412, 426), (100, 426)], [6, 6, 18, 18])
    items = [outlined(body, dgrad("#5b9df6", "#1f4dbb", (110, 262), (330, 440)), nm="body")]
    items.append(lines([G.line((104, 318), (408, 318)), G.line((104, 372), (408, 372))], INK, 5, 30, nm="planks"))
    straps = [strap(136, 166, 262, 426, body), strap(346, 376, 262, 426, body)]
    items.append(outlined(straps, dgrad(WHITE, SILVER_LO, (136, 262), (170, 426)), ow=5, nm="straps"))
    for x in (151, 361):
        for y in (300, 352, 400):
            items.append(shape(G.circle(x, y, 4.5), fill(INK, 55), nm="rivet"))
    base = G.rounded([(90, 410), (422, 410), (422, 438), (90, 438)], 12)
    items.append(outlined(base, vgrad(WHITE, SILVER_LO, 410, 438), ow=7, nm="base"))
    plate = G.rounded([(222, 256), (290, 256), (290, 318), (222, 318)], 14)
    items.append(outlined(plate, dgrad(WHITE, SILVER_LO, (222, 256), (290, 318)), ow=7, nm="lock"))
    gem, _ = kite_gem(256, 287, 34, 44, "#cfe7ff", "#4a8ff0", "#1f4dbb", ow=5)
    items.append(gem)
    return items


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 280, 220, SKY, 0.3,
                        opacity=Anim((0, 60), (36, 60), (52, 100), (110, 100), (130, 60), (180, 60)))])

    open_s = Anim((0, [100, 0], HOLD), (32, [100, 0], OUT), (44, [100, 108], SINE), (52, [100, 100]),
                  (112, [100, 100], IN), (122, [100, 0], HOLD), (180, [100, 0]))
    lid_back = stack(open_lid(), "lid-open", pivot=(256, HINGE), s=open_s)

    hole = G.rounded([(110, 248), (402, 248), (402, 282), (110, 282)], 14)
    light = Anim((0, 0, HOLD), (30, 0, OUT), (50, 100), (108, 100, IN), (126, 0), (180, 0))
    inside = stack([
        shape(hole, fill("#0d1d4d"), nm="dark"),
        group([ellipse([256, 266], [300, 64]),
               gradient([(0, WHITE, 1), (0.5, "#bfe3ff", 0.7), (1, "#bfe3ff", 0)], [256, 266], [406, 266], radial=True)],
              "glow", o=light),
    ], "inside")

    rays = []
    for k, a in enumerate((-128, -109, -90, -71, -52)):
        L = 200 if k % 2 else 236
        w = 7 if k % 2 else 9
        pa = (256 + L * math.cos(math.radians(a - w)), 262 + L * math.sin(math.radians(a - w)))
        pb = (256 + L * math.cos(math.radians(a + w)), 262 + L * math.sin(math.radians(a + w)))
        rays.append(G.poly([(256, 270), pa, pb]))
    beams = group([*[path(r) for r in rays],
                   gradient([(0, WHITE, 0.9), (0.5, WHITE, 0.32), (1, WHITE, 0)], [256, 266], [256, 40])],
                  "beams", pivot=(256, 266), o=light,
                  s=Anim((0, [60, 20], HOLD), (30, [60, 20], OUT), (54, [100, 100]), (108, [100, 100], IN),
                         (126, [80, 40], HOLD), (180, [60, 20])))

    gems = []
    d, _ = brilliant(0, 0, 34, "blue")
    gems.append(stack([d], "g1", p=Anim(*(arc_keys((256, 330), (262, 330), 250, 40, 104, 12) + [(180, [262, 330])])),
                      r=Anim((40, -14, LIN), (104, 16))))
    g2, _ = round_gem(0, 0, 24, "#d3e9ff", "#2f6be0", ow=7)
    gems.append(stack([g2], "g2", p=Anim(*(arc_keys((218, 330), (194, 340), 220, 46, 100, 12) + [(180, [194, 340])]))))
    g3, _ = round_gem(0, 0, 21, "#e2d7ff", "#7b5cf0", ow=7)
    gems.append(stack([g3], "g3", p=Anim(*(arc_keys((294, 330), (330, 340), 230, 50, 106, 12) + [(180, [330, 340])]))))

    lid_front = stack(closed_lid(), "lid", pivot=(256, HINGE),
                      s=Anim((0, [100, 100], HOLD), (22, [100, 100], IN), (32, [100, 0], HOLD), (122, [100, 0], OUT),
                             (132, [100, 106], SINE), (140, [100, 100]), (180, [100, 100])))

    chest = stack([lid_back, inside, group([beams], "b")] + gems + box() + [lid_front], "chest",
                  pivot=(256, 438),
                  r=Anim((0, 0), (6, -2.5), (12, 2.5), (18, -2), (24, 0), (180, 0)),
                  s=Anim((0, [100, 100]), (130, [100, 100], OUT), (136, [104, 96], SINE), (146, [100, 100]),
                         (180, [100, 100])))
    c.add("chest", [chest])
    c.add("sparkles", [
        twinkle(150, 150, 22, 50, 30), twinkle(372, 120, 26, 60, 32), twinkle(420, 236, 16, 78, 28),
        twinkle(86, 214, 16, 88, 28), twinkle(256, 470, 14, 134, 26, halo=False),
        twinkle(110, 452, 12, 140, 26, halo=False), twinkle(402, 452, 12, 146, 26, halo=False),
    ])
    return c
