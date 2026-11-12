"""106 · Алмазная галочка — rotating faceted sapphire rosette with a platinum check."""
import math

from .. import geom as G
from ..lottie import LIN, OUT, SINE, Anim, Comp, ellipse, fill, group, stroke
from ..style import (DEEP, INK, MID, OW, SKY, WHITE, dgrad, glow, lines, shape, sheen, stack,
                     twinkle)
from ..lottie import path

NAME = "verified_gem"
TITLE = "Алмазная галочка"
EMOJI = "✅"
HERO = 46

CX, CY = 256, 256
BUMPS = 12


def rosette(rot=0.0, R=186, r=164):
    pts = []
    for k in range(BUMPS * 2):
        a = math.radians(-90 + rot + k * 180 / BUMPS)
        rad = R if k % 2 == 0 else r
        pts.append((CX + rad * math.cos(a), CY + rad * math.sin(a)))
    return G.smooth(pts, t=1.15)


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 256, 244, SKY, 0.24, opacity=Anim((0, 100), (40, 70), (180, 100)))])
    # ping ring
    ring = group([ellipse([CX, CY], Anim((0, [392, 392], OUT), (44, [478, 478]))),
                  stroke(WHITE, Anim((0, 14, OUT), (44, 2)), Anim((0, 0, OUT), (6, 55, SINE), (44, 0), (180, 0)))],
                 "ping")
    c.add("ping", [ring])

    # silhouette turns 60deg per loop (wedge pattern period) via path keys so the gradient stays put
    keys = [(t, rosette(60 * t / T)) for t in range(0, T + 1, 30)]
    sil = Anim(*[(t, b, LIN) for t, b in keys])
    body = group([path(sil), dgrad(SKY, DEEP, (100, 90), (380, 440), mid=MID), stroke(INK, OW * 2)], "badge")

    wedges = []
    for k in range(BUMPS):
        a0 = math.radians(-90 + k * 30)
        a1 = math.radians(-90 + (k + 1) * 30)
        p0 = (CX + 200 * math.cos(a0), CY + 200 * math.sin(a0))
        p1 = (CX + 200 * math.cos(a1), CY + 200 * math.sin(a1))
        wedges.append((G.poly([(CX, CY), p0, p1]), k % 2))
    light = shape([w for w, s in wedges if s == 0], fill(WHITE, 16), nm="light")
    dark = shape([w for w, s in wedges if s == 1], fill("#0a2a7a", 14), nm="dark")
    spokes = lines([G.line((CX + 118 * math.cos(math.radians(-90 + k * 30)), CY + 118 * math.sin(math.radians(-90 + k * 30))),
                           (CX + 166 * math.cos(math.radians(-90 + k * 30)), CY + 166 * math.sin(math.radians(-90 + k * 30))))
                    for k in range(BUMPS)], WHITE, 3, 45, nm="spokes")
    spin = stack([light, dark, spokes], "spin", pivot=(CX, CY), r=Anim((0, 0, LIN), (T, 60)))
    table = stack([
        shape(G.circle(CX, CY, 122), dgrad("#8cc4ff", "#2a5fd0", (150, 140), (330, 380)), nm="table"),
        lines(G.circle(CX, CY, 122), WHITE, 4, 55, nm="rim"),
        shape(G.svg("M 160 214 C 170 172 204 146 244 140 C 214 156 192 180 184 216 Z")[0], fill(WHITE, 75), nm="hl"),
    ], "table")

    check = G.poly([(178, 262), (232, 314), (340, 202)], closed=False)
    tick = stack([
        shape(check, stroke(INK, 78, cap=2, join=2), nm="ink"),
        shape(check, stroke("#c7dcf6", 52, cap=2, join=2), nm="base"),
        shape(G.translate(check, -2, -5), stroke(WHITE, 38, cap=2, join=2), nm="top"),
    ], "check", pivot=(256, 262),
        s=Anim((0, [100, 100], OUT), (10, [118, 118], SINE), (26, [100, 100]), (180, [100, 100])))
    items = [body, spin, table, tick,
             sheen(rosette(), 64, 104, angle=30, width=50, alpha=0.45),
             twinkle(172, 128, 30, 112, 32), twinkle(392, 330, 24, 140, 30), twinkle(344, 196, 22, 34, 28)]
    c.add("badge", [stack(items, "verified", pivot=(CX, CY),
                          s=Anim((0, [100, 100], OUT), (8, [104, 104], SINE), (24, [100, 100]), (180, [100, 100])))])
    return c
