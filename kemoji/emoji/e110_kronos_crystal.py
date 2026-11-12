"""110 · ★ Кристалл KRONOS — the brand "K" set in a faceted sapphire-amethyst
hexagon under a crown, with a satellite gem orbiting it and slowly turning
light rays behind (special: made to be worn as an emoji status)."""
import math

from .. import geom as G
from ..gems import kite_gem
from ..glyphs import text_paths
from ..lottie import HOLD, LIN, Anim, Comp, fill, gradient, group, path, stroke, trim
from ..style import (DEEP, MID, SILVER, WHITE, bob, dgrad, glow, lines, outlined, shape, sheen, stack,
                     twinkle, vgrad)

NAME = "kronos_crystal"
TITLE = "Кристалл KRONOS"
EMOJI = "💠"
HERO = 52
SPECIAL = True

C = (256, 286)
LIGHT = (-0.55, -0.84)
ORBIT = dict(cx=256, cy=300, rx=214, ry=54, tilt=-12)


def mix(c0, c1, f):
    a = [int(c0[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(x + (y - x) * f) for x, y in zip(a, b))


def ramp(f):
    return mix("#3a2db4", "#5c7cf0", f / 0.5) if f < 0.5 else mix("#5c7cf0", "#dcecff", (f - 0.5) / 0.5)


def orbit_point(theta):
    o = ORBIT
    x = o["rx"] * math.cos(theta)
    y = o["ry"] * math.sin(theta)
    a = math.radians(o["tilt"])
    return (o["cx"] + x * math.cos(a) - y * math.sin(a), o["cy"] + x * math.sin(a) + y * math.cos(a))


def half_orbit(front):
    o = ORBIT
    full = G.rotate(G.circle(o["cx"], o["cy"], o["rx"], o["ry"]), o["tilt"], o["cx"], o["cy"])
    idx = [1, 2, 3] if front else [3, 0, 1]
    v = [full["v"][i] for i in idx]
    ins = [full["i"][i] for i in idx]
    outs = [full["o"][i] for i in idx]
    ins[0] = [0, 0]
    outs[-1] = [0, 0]
    return G.bez(v, False, ins, outs)


def satellite(front, T):
    keys_p, keys_s = [], []
    for t in range(0, T + 1, 6):
        th = 2 * math.pi * t / T
        keys_p.append((t, list(orbit_point(th)), LIN))
        k = 100 + 22 * math.sin(th)
        keys_s.append((t, [k, k], LIN))
    if front:
        op = Anim((0, 100, HOLD), (T / 2, 0, HOLD), (T, 0))
    else:
        op = Anim((0, 0, HOLD), (T / 2, 100, HOLD), (T, 100))
    star = stack([glow(0, 0, 34, WHITE, 0.7), shape(G.sparkle(18, 0.55), fill(WHITE)),
                  shape(G.circle(0, 0, 5), fill("#cfe8ff"))], "sat")
    return group([star], "satellite", p=Anim(*keys_p), s=Anim(*keys_s), o=op)


def crown():
    pts = [(208, 152), (198, 108), (230, 128), (256, 92), (282, 128), (314, 108), (304, 152)]
    body = G.rounded(pts, [4, 7, 6, 7, 6, 7, 4])
    items = [outlined(body, vgrad(WHITE, SILVER, 92, 152), ow=8, nm="crown")]
    items.append(shape(G.poly([(256, 92), (282, 128), (304, 152), (256, 152)]), fill("#93a9cf", 30), nm="shade"))
    band = G.rounded([(200, 140), (312, 140), (312, 162), (200, 162)], 9)
    items.append(outlined(band, dgrad(MID, DEEP, (200, 140), (300, 166)), ow=7, nm="band"))
    for x, y, r in ((198, 104, 8), (256, 86, 10), (314, 104, 8)):
        items.append(outlined(G.circle(x, y, r), fill(WHITE), ow=5))
        items.append(shape(G.circle(x - r * 0.3, y - r * 0.35, r * 0.3), fill("#cfe0f7")))
    g, _ = kite_gem(256, 151, 22, 18, WHITE, "#cfe7ff", "#8cc4fb", ow=4)
    items.append(g)
    return items


def emblem(T):
    R, r = 146, 84
    P = G.regular(C[0], C[1], R, 6, rot=-90)
    Q = G.regular(C[0], C[1], r, 6, rot=-90)
    outline = G.rounded(P, 16)
    flat = G.flatten(outline, 12)
    items = [outlined(outline, fill("#4b4fd8"), nm="hex")]
    for k in range(6):
        quad = [P[k], P[(k + 1) % 6], Q[(k + 1) % 6], Q[k]]
        mid = math.radians(-60 + 60 * k)
        b = math.cos(mid) * LIGHT[0] + math.sin(mid) * LIGHT[1]
        f = (b + 1) / 2
        fb = G.poly(G.clip(flat, quad))
        x0, y0, x1, y1 = G.bbox(fb["v"])
        items.append(shape(fb, dgrad(ramp(min(1, f + 0.08)), ramp(max(0, f - 0.12)), (x0, y0), (x1, y1)), nm="facet"))
    table = G.poly(Q)
    items.append(shape(table, dgrad("#9fd0ff", "#4a4fd6", (200, 210), (320, 360)), nm="table"))
    items.append(lines([G.line(P[k], Q[k]) for k in range(6)] + [table], WHITE, 3.5, 55, nm="edges"))
    items.append(shape(G.poly([P[5], (P[5][0] + 30, P[5][1] - 17), (Q[5][0] + 10, Q[5][1] - 6), Q[5]]),
                       fill(WHITE, 55), nm="hl"))
    K = text_paths("K", 0, C[1] + 60, 120, center_x=C[0] + 4)
    items.append(outlined(K, vgrad(WHITE, "#c4d8f6", C[1] - 60, C[1] + 60), ow=10, nm="K"))
    items.append(sheen(outline, 34, 72, angle=30, width=46, alpha=0.6))
    items.append(sheen(K, 104, 134, angle=30, width=26, alpha=0.9))
    for k, t0 in zip(range(6), (40, 64, 88, 112, 136, 150)):
        items.append(twinkle(P[k][0], P[k][1], 20, t0, 28))
    return items


def build(T=180):
    c = Comp(NAME, T)
    rays = []
    for k in range(12):
        a = math.radians(-90 + k * 30)
        L = 208 if k % 2 == 0 else 164
        w = math.radians(5.5 if k % 2 == 0 else 4)
        rays.append(G.poly([C, (C[0] + L * math.cos(a - w), C[1] + L * math.sin(a - w)),
                            (C[0] + L * math.cos(a + w), C[1] + L * math.sin(a + w))]))
    ray_grad = gradient([(0, WHITE, 0.55), (0.55, "#bcd2ff", 0.28), (1, "#bcd2ff", 0)], list(C), [C[0] + 210, C[1]],
                        radial=True)
    c.add("rays", [group([path(r) for r in rays] + [ray_grad], "rays", pivot=C, r=Anim((0, 0, LIN), (T, 60)))])
    c.add("aura", [glow(C[0], C[1], 200, "#9d8cff", 0.4, opacity=Anim((0, 70), (90, 100), (180, 70)))])

    back = stack([lines(half_orbit(False), WHITE, 5, 45, nm="orbit-back"), satellite(False, T)], "back")
    # trimmed ends: at the crossing points only the back line exists, so the z-swap is invisible
    front = stack([group([path(half_orbit(True)), trim(6, 94), stroke(WHITE, 6, 75)], "orbit-front"),
                   satellite(True, T)], "front")
    body = stack([back] + emblem(T) + crown() + [front], "emblem", pivot=(256, 290), p=bob(256, 290, 6, T))
    c.add("emblem", [body])
    c.add("sparkles", [twinkle(84, 120, 18, 20, 30, halo=False), twinkle(430, 96, 20, 76, 32, halo=False),
                       twinkle(448, 430, 14, 120, 28, halo=False), twinkle(70, 440, 16, 150, 28, halo=False)])
    return c
