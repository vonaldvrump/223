"""119 · ★ Полночь — royal pocket watch: the hands race round and strike
midnight, the watch jolts and fireworks burst around it (special: made to be
worn as an emoji status in the New Year days)."""
import math

from .. import geom as G
from ..gems import kite_gem, round_gem
from ..glyphs import text_paths
from ..lottie import EASE, HOLD, LIN, OUT, SINE, Anim, Comp, ellipse, fill, gradient, group, path, stroke, trim
from ..style import (INK, SILVER, SILVER_LO, WHITE, dgrad, drift, glow, lines, outlined, shape, sheen, stack,
                     twinkle, vgrad)

NAME = "midnight_clock"
TITLE = "Полночь"
EMOJI = "🕛"
HERO = 34
SPECIAL = True

C = (256, 300)


def burst(cx, cy, t0, color, n=10, r0=14, r1=64, T=180):
    rays = []
    for k in range(n):
        a = math.radians(k * 360 / n + 9)
        rays.append(G.line((cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * r1, cy + math.sin(a) * r1)))
    e = Anim((t0, 0, OUT), (t0 + 16, 100), (T, 100))
    s = Anim((t0, 0, HOLD), (t0 + 8, 0, SINE), (t0 + 30, 100), (T, 100))
    o = Anim((t0, 0, HOLD), (t0 + 1, 100, LIN), (t0 + 26, 100, LIN), (t0 + 32, 0), (T, 0))
    items = [group([path(r) for r in rays] + [trim(s, e), stroke(color, 7, cap=2)], "rays", o=o)]
    for k in range(n):
        a = math.radians(k * 360 / n + 27)
        items += drift([shape(G.circle(0, 0, 5), fill(WHITE))], (cx + math.cos(a) * 20, cy + math.sin(a) * 20),
                       (cx + math.cos(a) * (r1 - 6), cy + math.sin(a) * (r1 - 6) + 10), t0 + 4, 34, T, fade=0.2,
                       s0=120, s1=40)
    items.append(twinkle(cx, cy, 20, t0, 24))
    return items


def hand(length, width, tail=18):
    pts = [(C[0] - width / 2, C[1] + tail), (C[0] - width * 0.32, C[1] - length + 10), (C[0], C[1] - length),
           (C[0] + width * 0.32, C[1] - length + 10), (C[0] + width / 2, C[1] + tail)]
    return G.rounded(pts, [4, 3, 5, 3, 4])


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(C[0], C[1] - 10, 218, "#9fc4ff", 0.36,
                        opacity=Anim((0, 100, OUT), (20, 80), (60, 65), (166, 65, SINE), (180, 100)))])
    fw = (burst(110, 112, 4, "#ffd35a") + burst(402, 108, 16, "#c9b8ff") + burst(78, 268, 30, "#8fe3ff", r1=56) +
          burst(436, 276, 42, "#ff9fd2", r1=56) + burst(256, 62, 58, "#ffffff", n=12, r1=44))
    c.add("fireworks", fw)

    items = []
    # bow ring and crown knob
    items.append(shape(G.circle(256, 116, 26, 22), stroke(INK, 22), nm="bow-ink"))
    items.append(shape(G.circle(256, 116, 26, 22), stroke(SILVER, 10), nm="bow"))
    knob = G.rounded([(234, 132), (278, 132), (278, 160), (234, 160)], 7)
    items.append(outlined(knob, dgrad(WHITE, SILVER_LO, (234, 132), (278, 160)), ow=8, nm="knob"))
    items.append(lines([G.line((242, 136), (242, 156)), G.line((256, 136), (256, 156)), G.line((270, 136), (270, 156))],
                       INK, 3, 45, nm="knurl"))
    case = G.circle(C[0], C[1], 146)
    items.append(outlined(case, dgrad(WHITE, SILVER_LO, (130, 170), (380, 440), mid=SILVER), nm="case"))
    items.append(shape(G.circle(C[0], C[1], 134), stroke(WHITE, 4, 70), nm="bezel"))
    face = G.circle(C[0], C[1], 122)
    items.append(outlined(face, gradient([(0, "#4f8ff2"), (0.7, "#1f4dbb"), (1, "#142f7c")], [C[0] - 40, C[1] - 50],
                                         [C[0] + 120, C[1]], radial=True), ow=8, nm="face"))
    ticks = []
    for k in range(12):
        if k % 3 == 0:
            continue
        a = math.radians(-90 + k * 30)
        ticks.append(G.line((C[0] + math.cos(a) * 100, C[1] + math.sin(a) * 100),
                            (C[0] + math.cos(a) * 112, C[1] + math.sin(a) * 112)))
    items.append(lines(ticks, WHITE, 7, 90, nm="ticks"))
    for k in range(4):
        a = math.radians(-90 + k * 90)
        x, y = C[0] + math.cos(a) * 102, C[1] + math.sin(a) * 102
        g, _ = kite_gem(x, y, 20 if k else 24, 26 if k else 32, WHITE, "#cfe7ff", "#8cc4fb", ow=5)
        items.append(g)
    year = text_paths("2027", 0, C[1] + 66, 22, tracking=2, center_x=C[0])
    items.append(shape(year, fill(WHITE, 75), nm="year"))
    items.append(shape(G.svg("M 168 250 C 180 214 214 190 252 184 C 222 202 200 224 190 256 Z")[0], fill(WHITE, 28),
                       nm="glass"))

    minute = Anim((0, 0, HOLD), (90, 0, EASE), (170, 720), (180, 720))
    hour = Anim((0, 0, HOLD), (90, 0, EASE), (170, 360), (180, 360))
    items.append(stack([outlined(hand(66, 18), vgrad(WHITE, SILVER, C[1] - 66, C[1] + 18), ow=6, nm="hour")],
                       "hour", pivot=C, r=hour))
    items.append(stack([outlined(hand(98, 13), vgrad(WHITE, SILVER, C[1] - 98, C[1] + 18), ow=6, nm="minute")],
                       "minute", pivot=C, r=minute))
    cap, _ = round_gem(C[0], C[1], 13, "#d3e9ff", "#2f6be0", ow=5)
    items.append(cap)
    items.append(sheen(case, 104, 140, angle=30, width=40, alpha=0.55))
    items.append(twinkle(196, 214, 26, 120, 30))
    flash = group([ellipse(list(C), [250, 250]), gradient([(0, WHITE, 0.9), (1, WHITE, 0)], list(C), [C[0] + 125, C[1]],
                                                          radial=True)], "flash",
                  o=Anim((0, 0, OUT), (4, 80, SINE), (26, 0), (180, 0)))
    items.append(flash)
    watch = stack(items, "watch", pivot=(256, 300),
                  s=Anim((0, [100, 100], OUT), (6, [108, 108], SINE), (20, [100, 100]), (180, [100, 100])),
                  r=Anim((0, 0, OUT), (5, -5, SINE), (12, 4, SINE), (20, -2, SINE), (28, 0), (180, 0)))
    c.add("watch", [watch])
    return c
