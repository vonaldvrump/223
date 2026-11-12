"""113 · Подарок — sapphire gift box that hops, pops its lid and throws confetti."""
import math

from .. import geom as G
from ..gems import brilliant
from ..lottie import IN, LIN, OUT, SINE, Anim, Comp, ellipse, fill, group, rect, stroke
from ..style import (INK, SILVER, SILVER_LO, SKY, WHITE, arc_keys, dgrad, glow, lines, outlined, shape,
                     sheen, stack, twinkle, vgrad)

NAME = "gift_box"
TITLE = "Подарок"
EMOJI = "🎁"
HERO = 0

CONFETTI = ["#ffffff", "#a9d6ff", "#c9b8ff", "#ff9fd2", "#ffd35a", "#8fe3ff"]


def body_items():
    body = G.rounded([(136, 262), (376, 262), (376, 430), (136, 430)], [4, 4, 16, 16])
    items = [outlined(body, dgrad("#7fbaf7", "#1f4dbb", (136, 262), (360, 440), mid="#3f82ee"), nm="box")]
    items.append(shape(G.poly(G.clip(G.flatten(body, 8), [(256, 250), (390, 250), (390, 440), (256, 440)])),
                       fill("#0b2a7a", 14), nm="shade"))
    rib = G.rounded([(236, 262), (276, 262), (276, 430), (236, 430)], 2)
    items.append(outlined(rib, vgrad(WHITE, SILVER, 262, 430), ow=6, nm="ribbon"))
    items.append(sheen(body, 130, 166, angle=30, width=40, alpha=0.55))
    return items


def lid_items():
    lid = G.rounded([(118, 214), (394, 214), (394, 270), (118, 270)], 12)
    items = [outlined(lid, dgrad("#a9d6ff", "#2f6be0", (118, 214), (330, 280)), nm="lid")]
    rib = G.rounded([(232, 214), (280, 214), (280, 270), (232, 270)], 2)
    items.append(outlined(rib, vgrad(WHITE, SILVER, 214, 270), ow=6, nm="ribbon"))
    items.append(shape(G.rounded([(132, 222), (222, 222), (222, 230), (132, 230)], 4), fill(WHITE, 60), nm="hl"))
    loop_l = G.svg("M 256 212 C 226 160 160 150 168 196 C 174 226 226 222 256 212 Z")[0]
    loop_r = G.mirror(loop_l)
    tail_l = G.svg("M 248 214 C 236 230 222 246 206 252 L 222 266 C 236 252 248 236 256 218 Z")[0]
    tail_r = G.mirror(tail_l)
    bow = stack([outlined([tail_l, tail_r], vgrad(WHITE, SILVER_LO, 212, 266), ow=6, nm="tails"),
                 outlined([loop_l, loop_r], dgrad(WHITE, SILVER, (168, 150), (340, 220), mid="#eef5ff"), ow=7,
                          nm="loops"),
                 lines([G.svg("M 248 206 C 226 182 196 176 190 192")[0], G.mirror(G.svg("M 248 206 C 226 182 196 176 190 192")[0])],
                       "#93a9cf", 5, 80, nm="folds")],
                "bow", pivot=(256, 212),
                s=Anim((0, [100, 100]), (36, [100, 100], OUT), (44, [112, 92], SINE), (56, [94, 106], SINE),
                       (68, [100, 100]), (180, [100, 100])))
    items.append(bow)
    gem, _ = brilliant(256, 196, 24, "blue", ow=6)
    items.append(gem)
    items.append(twinkle(244, 178, 22, 40, 28))
    return items


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 300, 214, SKY, 0.3, opacity=Anim((0, 70), (40, 100), (100, 70), (180, 70)))])

    lid = stack(lid_items(), "lid", pivot=(256, 270),
                p=Anim((0, [256, 270]), (22, [256, 270], OUT), (40, [256, 214], SINE), (52, [256, 222], IN),
                       (64, [256, 270], OUT), (70, [256, 264], SINE), (78, [256, 270]), (180, [256, 270])),
                r=Anim((0, 0), (22, 0, OUT), (40, -8, SINE), (56, 4, SINE), (66, 0), (180, 0)))

    pieces = []
    for k in range(10):
        a = -150 + k * 13.3
        dx = math.cos(math.radians(a)) * (140 + 30 * (k % 3))
        h = 120 + 30 * ((k * 7) % 3)
        p0 = (256 + dx * 0.15, 250)
        p1 = (256 + dx, 330 + 20 * (k % 2))
        piece = group([rect([0, 0], [14, 22], 3) if k % 2 else ellipse([0, 0], [14, 14]),
                       fill(CONFETTI[k % len(CONFETTI)]), stroke(INK, 3)], "c")
        t0 = 36 + (k % 4) * 2
        keys = arc_keys(p0, p1, h, t0, t0 + 64, 10)
        op = Anim((t0, 0, LIN), (t0 + 4, 100, LIN), (t0 + 50, 100, LIN), (t0 + 64, 0))
        pieces.append(group([piece], "confetti", p=Anim(*keys), o=op,
                            r=Anim((t0, 0, LIN), (t0 + 64, 300 if k % 2 else -300))))

    gift = stack(body_items() + [lid], "gift", pivot=(256, 432),
                 p=Anim((0, [256, 432]), (10, [256, 432], OUT), (18, [256, 432], OUT), (34, [256, 402], IN),
                        (48, [256, 432]), (180, [256, 432])),
                 s=Anim((0, [100, 100]), (10, [108, 92], OUT), (18, [96, 105], SINE), (34, [100, 100], IN),
                        (48, [110, 90], OUT), (58, [96, 104], SINE), (70, [100, 100]), (124, [100, 100], SINE),
                        (130, [104, 96], SINE), (136, [98, 102], SINE), (142, [100, 100]), (180, [100, 100])))
    c.add("gift", [gift])
    c.add("confetti", pieces)
    c.add("sparkles", [twinkle(96, 140, 20, 44, 30), twinkle(420, 120, 22, 52, 30), twinkle(440, 300, 16, 100, 28, halo=False),
                       twinkle(70, 330, 14, 150, 26, halo=False)])
    return c
