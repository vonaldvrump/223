"""116 · Колокольчики — two snow-capped sapphire bells under a satin bow that
swing, clang and ring."""
from .. import geom as G
from ..gems import brilliant
from ..lottie import OUT, SINE, Anim, Comp, fill, group, path, stroke
from ..style import (INK, SILVER, SILVER_LO, SKY, WHITE, dgrad, glow, lines, outlined, shape, sheen, stack,
                     twinkle, vgrad)

NAME = "jingle_bells"
TITLE = "Колокольчики"
EMOJI = "🔔"
HERO = 28

BELL = ("M -24 -100 C -58 -100 -72 -72 -74 -38 C -76 -4 -84 22 -102 42 C -110 52 -104 60 -92 60 "
        "L 92 60 C 104 60 110 52 102 42 C 84 22 76 -4 74 -38 C 72 -72 58 -100 24 -100 Z")
CAP = [(-52, -84), (-34, -106), (0, -112), (34, -106), (52, -84), (56, -66), (42, -72), (32, -54), (20, -70),
       (2, -62), (-12, -74), (-26, -56), (-40, -74), (-56, -66)]


def bell(clapper_r):
    body = G.svg(BELL)[0]
    items = [
        stack([outlined(G.circle(0, 82, 17), dgrad(WHITE, SILVER_LO, (-17, 65), (17, 99)), ow=7, nm="ball")],
              "clapper", pivot=(0, 30), r=clapper_r),
        outlined(body, dgrad("#b5dcff", "#1f4dbb", (-80, -100), (70, 60), mid="#4a8ff0"), nm="bell"),
        shape(G.svg("M -50 -56 C -54 -24 -60 4 -74 28")[0], stroke(WHITE, 11, 70), nm="hl"),
        outlined(G.rounded([(-100, 38), (100, 38), (100, 62), (-100, 62)], 11), vgrad(WHITE, SILVER_LO, 38, 62), ow=7,
                 nm="rim"),
        outlined(G.smooth(CAP), vgrad(WHITE, "#d6e8fb", -112, -54), ow=7, nm="snow"),
        shape(G.circle(-22, -96, 4), fill("#cfe3fa"), nm="dot"),
        sheen(body, 120, 150, angle=30, width=30, alpha=0.6),
    ]
    knob = [shape(G.circle(0, -120, 12), stroke(INK, 18), nm="knob-ink"),
            shape(G.circle(0, -120, 12), stroke(SILVER, 8), nm="knob")]
    return knob + items


def ring_arcs(side, t0):
    x = 256 + side * 186
    arcs = [G.svg("M %d 286 C %d 306 %d 330 %d 350" % (x, x + side * 14, x + side * 14, x))[0],
            G.svg("M %d 270 C %d 300 %d 336 %d 366" % (x + side * 22, x + side * 42, x + side * 42, x + side * 22))[0]]
    o = Anim((t0, 0, OUT), (t0 + 5, 100, SINE), (t0 + 24, 0))
    s = Anim((t0, [70, 70], OUT), (t0 + 24, [118, 118]))
    return group([path(a) for a in arcs] + [stroke(WHITE, 8, 90)], "ring", pivot=(x, 318), o=o, s=s)


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 300, 214, SKY, 0.3, opacity=Anim((0, 70), (22, 100), (60, 70), (112, 100), (150, 70), (180, 70)))])
    swing = Anim((0, 24, SINE), (22, 3, OUT), (29, 12, SINE), (48, 24, SINE), (90, 24, SINE), (112, 3, OUT),
                 (119, 12, SINE), (138, 24, SINE), (180, 24))
    clap = Anim((0, 0), (22, -14, OUT), (34, 16, SINE), (52, 0), (112, -14, OUT), (124, 16, SINE), (142, 0), (180, 0))
    left = stack(bell(clap), "bellL", p=(222, 168), a=(0, -120), s=[74, 74], r=swing)
    right = stack(bell(clap.map(lambda v: -v)), "bellR", p=(290, 168), a=(0, -120), s=[74, 74],
                  r=swing.map(lambda v: -v))

    loop_l = G.svg("M 256 150 C 230 112 176 104 182 140 C 186 164 228 162 256 150 Z")[0]
    tail_l = G.svg("M 248 152 C 236 170 222 188 204 196 L 220 210 C 236 196 248 176 256 156 Z")[0]
    bow = stack([outlined([tail_l, G.mirror(tail_l)], dgrad("#c9b8ff", "#6a4be0", (204, 150), (300, 210)), ow=6, nm="tails"),
                 outlined([loop_l, G.mirror(loop_l)], dgrad("#d9ccff", "#7b5cf0", (182, 110), (330, 166)), ow=7,
                          nm="loops"),
                 lines([G.svg("M 248 146 C 230 128 206 124 198 136")[0], G.mirror(G.svg("M 248 146 C 230 128 206 124 198 136")[0])],
                       "#5a3fd0", 5, 70, nm="folds")],
                "bow", pivot=(256, 150), s=Anim((0, [100, 100]), (22, [100, 100], OUT), (28, [108, 94], SINE), (40, [100, 100]),
                                                (112, [100, 100], OUT), (118, [108, 94], SINE), (130, [100, 100]), (180, [100, 100])))
    gem, _ = brilliant(256, 142, 20, "blue", ow=6)
    c.add("bells", [stack([left, right, bow, gem, twinkle(246, 128, 18, 60, 28)], "bells",
                          pivot=(256, 150), r=Anim((0, 0), (22, 0, OUT), (26, 2, SINE), (32, -1.5), (40, 0),
                                                   (112, 0, OUT), (116, -2, SINE), (122, 1.5), (130, 0), (180, 0)))])
    c.add("rings", [ring_arcs(-1, 22), ring_arcs(1, 22), ring_arcs(-1, 112), ring_arcs(1, 112)])
    c.add("sparkles", [twinkle(256, 446, 22, 24, 30), twinkle(256, 446, 22, 114, 30),
                       twinkle(90, 120, 16, 60, 28, halo=False), twinkle(424, 112, 18, 150, 28, halo=False)])
    return c
