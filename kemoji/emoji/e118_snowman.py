"""118 · Снеговик-джентльмен — top hat with a diamond, monocle, diamond buttons;
he tips his hat and winks."""
from .. import geom as G
from ..gems import brilliant, kite_gem
from ..lottie import IN, OUT, SINE, Anim, Comp, fill, stroke
from ..style import (INK, SILVER, SILVER_LO, SKY, WHITE, dgrad, glow, lines, outlined, shape, snowfall, stack,
                     twinkle, vgrad)

NAME = "snowman"
TITLE = "Снеговик-джентльмен"
EMOJI = "☃️"
HERO = 50

COAL = "#1b2550"
TWIG = "#6b4a33"


def arm(points):
    b = G.poly(points, closed=False)
    return [shape(b, stroke(INK, 20, cap=2, join=2), nm="arm-ink"), shape(b, stroke(TWIG, 9, cap=2, join=2), nm="arm")]


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 300, 220, SKY, 0.28, opacity=Anim((0, 70), (90, 100), (180, 70)))])

    body = []
    body += arm([(184, 346), (112, 300), (90, 270)]) + arm([(126, 310), (104, 316)])
    wave = Anim((0, 0), (40, 0, SINE), (52, -16, SINE), (64, 4, SINE), (76, -12, SINE), (90, 0), (180, 0))
    body.append(stack(arm([(328, 346), (400, 296), (420, 262)]) + arm([(388, 304), (414, 306)]), "armR",
                      pivot=(328, 346), r=wave))
    body.append(outlined(G.circle(256, 380, 100), dgrad(WHITE, "#c3daf6", (180, 290), (330, 480)), nm="belly"))
    for y in (338, 384, 430):
        g, _ = kite_gem(256, y, 22, 28, "#d9eeff", "#4a8ff0", "#1f4dbb", ow=5)
        body.append(g)
    body.append(outlined(G.circle(256, 224, 74), dgrad(WHITE, "#c9ddf6", (196, 160), (320, 300)), nm="head"))
    body.append(shape([G.circle(214, 246, 12), G.circle(298, 246, 12)], fill("#ff9fc6", 45), nm="cheeks"))
    # face
    eye_l = stack([shape(G.circle(228, 214, 10, 12), fill(COAL)), shape(G.circle(224, 209, 3.5), fill(WHITE))], "eyeL",
                  pivot=(228, 214), s=Anim((0, [100, 100]), (96, [100, 100], IN), (101, [100, 12], OUT), (108, [100, 100]),
                                          (180, [100, 100])))
    body.append(eye_l)
    body.append(shape(G.circle(284, 214, 10, 12), fill(COAL), nm="eyeR"))
    body.append(shape(G.circle(280, 209, 3.5), fill(WHITE), nm="eyeRhl"))
    body.append(shape(G.circle(284, 214, 21), stroke(INK, 13), nm="mono-ink"))
    body.append(shape(G.circle(284, 214, 21), stroke(SILVER, 6), nm="mono"))
    body.append(shape(G.svg("M 304 224 C 316 244 318 262 312 282")[0], stroke(SILVER_LO, 3.5), nm="chain"))
    nose = G.rounded([(250, 228), (262, 242), (324, 246)], [4, 4, 6])
    body.append(outlined(nose, dgrad("#ffc27a", "#f07a1e", (250, 228), (320, 250)), ow=6, nm="carrot"))
    for k, (x, y) in enumerate([(222, 254), (236, 264), (256, 268), (276, 264), (290, 254)]):
        body.append(shape(G.circle(x, y, 5), fill(COAL), nm="smile"))
    # scarf
    tail = G.rounded([(282, 292), (316, 290), (330, 366), (298, 370)], 8)
    body.append(outlined(tail, dgrad("#7fbaf7", "#1f4dbb", (282, 290), (330, 370)), ow=8, nm="tail"))
    body.append(lines([G.line((292, 330), (322, 328)), G.line((296, 350), (326, 348))], WHITE, 6, 90, nm="stripes"))
    wrap = G.rounded([(184, 272), (328, 272), (330, 306), (182, 306)], 16)
    body.append(outlined(wrap, dgrad("#a9d6ff", "#2f6be0", (184, 272), (330, 310)), ow=8, nm="scarf"))
    body.append(lines([G.line((214, 274), (210, 304)), G.line((240, 274), (238, 306))], WHITE, 6, 90, nm="wstripes"))

    hat = [outlined(G.rounded([(206, 64), (306, 64), (310, 150), (202, 150)], [10, 10, 4, 4]),
                    dgrad("#3a4f8f", "#121c45", (206, 64), (310, 150)), nm="crown"),
           shape(G.svg("M 220 76 L 222 138")[0], stroke(WHITE, 7, 35), nm="sheen"),
           outlined(G.rounded([(204, 116), (308, 116), (309, 140), (203, 140)], 3), vgrad(WHITE, SILVER_LO, 116, 140),
                    ow=6, nm="band"),
           outlined(G.circle(256, 150, 86, 16), dgrad("#3a4f8f", "#121c45", (170, 134), (342, 166)), ow=11, nm="brim")]
    gem, gem_o = brilliant(256, 124, 15, "blue", ow=5)
    hat += [gem, twinkle(248, 112, 18, 58, 26)]
    tip = stack(hat, "hat", pivot=(256, 150),
                p=Anim((0, [256, 150]), (36, [256, 150], OUT), (48, [256, 124], SINE), (66, [256, 128], IN), (76, [256, 150], OUT),
                       (82, [256, 146], SINE), (88, [256, 150]), (180, [256, 150])),
                r=Anim((0, -8), (36, -8, OUT), (48, -20, SINE), (66, -18, IN), (76, -8), (180, -8)))
    body.append(tip)
    c.add("snowman", [stack(body, "snowman", pivot=(256, 478),
                            s=Anim((0, [100, 100]), (76, [100, 100], OUT), (80, [103, 97], SINE), (90, [100, 100]),
                                   (180, [100, 100])))])
    c.add("snow", snowfall([(70, 100, 0), (446, 120, 40), (80, 300, 80), (440, 300, 120), (380, 30, 160)],
                           T, dur=120, fall=120, r=12))
    return c
