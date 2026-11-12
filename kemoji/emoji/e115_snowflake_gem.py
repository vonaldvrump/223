"""115 · Снежинка-алмаз — six crystal blades with gem tips around a faceted
hexagon core; turns 60° per loop and pulses."""
import math

from .. import geom as G
from ..lottie import LIN, OUT, SINE, Anim, Comp, fill
from ..style import (SKY, WHITE, dgrad, glow, lines, outlined, shape, stack, twinkle)

NAME = "snowflake_gem"
TITLE = "Снежинка-алмаз"
EMOJI = "❄️"
HERO = 0

C = (256, 256)


def rot(p, deg):
    a = math.radians(deg)
    x, y = p
    return (C[0] + x * math.cos(a) - y * math.sin(a), C[1] + x * math.sin(a) + y * math.cos(a))


def blade(length, width, start=0.0):
    """Blade along -y in local coords: list of points of a long hexagonal crystal."""
    return [(0, -start), (width, -start - width * 1.2), (width * 0.8, -length + width * 1.6), (0, -length),
            (-width * 0.8, -length + width * 1.6), (-width, -start - width * 1.2)]


def arm_items(deg):
    out = []
    main = blade(196, 24, 40)
    pts = [rot(p, deg) for p in main]
    outline = G.rounded(pts, [3, 6, 6, 8, 6, 6])
    out.append(outlined(outline, fill("#a9d6ff"), ow=11, nm="blade"))
    flat = G.flatten(outline, 8)
    axis_end = rot((0, -196), deg)
    axis_start = rot((0, -40), deg)
    left = [rot(p, deg) for p in [(0, -40), (0, -196), (-40, -196), (-40, -40)]]
    right = [rot(p, deg) for p in [(0, -40), (40, -40), (40, -196), (0, -196)]]
    out.append(shape(G.poly(G.clip(flat, left)), dgrad("#ffffff", "#cfe7ff", axis_start, axis_end), nm="lit"))
    out.append(shape(G.poly(G.clip(flat, right)), dgrad("#8cc4fb", "#4a8ff0", axis_start, axis_end), nm="shade"))
    for side in (-1, 1):
        attach = rot((0, -112), deg)
        b = [(attach[0] + p[0] - C[0], attach[1] + p[1] - C[1])
             for p in (rot(q, deg + side * 52) for q in blade(72, 13, 0))]
        ob = G.rounded(b, [2, 4, 4, 6, 4, 4])
        out.append(outlined(ob, dgrad("#ffffff", "#7fb7f5", b[0], b[3]), ow=8, nm="branch"))
    out.append(lines([G.line(rot((0, -52), deg), rot((0, -182), deg))], WHITE, 3, 70, nm="ridge"))
    return out


def tip_gem(deg):
    cx, cy = rot((0, -206), deg)
    w, h = 30, 40
    pts = [rot(p, deg) for p in [(0, -206 - h / 2), (w / 2, -206), (0, -206 + h / 2), (-w / 2, -206)]]
    o = G.rounded(pts, 3)
    flat = G.flatten(o, 6)
    return [outlined(o, fill("#c9b8ff"), ow=7, nm="tip"),
            shape(G.poly(G.clip(flat, [pts[0], pts[1], (cx, cy)])), fill("#ffffff"), nm="tf"),
            shape(G.poly(G.clip(flat, [pts[3], pts[0], (cx, cy)])), fill("#e2d7ff"), nm="tf"),
            shape(G.poly(G.clip(flat, [pts[2], pts[3], (cx, cy)])), fill("#9b82f5"), nm="tf"),
            shape(G.poly(G.clip(flat, [pts[1], pts[2], (cx, cy)])), fill("#7b5cf0"), nm="tf")]


def core():
    P = G.regular(C[0], C[1], 62, 6, rot=-90)
    Q = G.regular(C[0], C[1], 32, 6, rot=-90)
    o = G.rounded(P, 8)
    flat = G.flatten(o, 8)
    items = [outlined(o, fill("#4a8ff0"), ow=11, nm="core")]
    shades = ["#ffffff", "#d3e9ff", "#8cc4fb", "#4a8ff0", "#6fa9f2", "#b8dcff"]
    for k in range(6):
        quad = [P[k], P[(k + 1) % 6], Q[(k + 1) % 6], Q[k]]
        items.append(shape(G.poly(G.clip(flat, quad)), fill(shades[k]), nm="cf"))
    items.append(shape(G.poly(Q), dgrad("#e9f5ff", "#7fb7f5", Q[5], Q[2]), nm="table"))
    items.append(lines([G.line(P[k], Q[k]) for k in range(6)] + [G.poly(Q)], WHITE, 3, 60, nm="edges"))
    return items


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 256, 236, SKY, 0.33, opacity=Anim((0, 100), (45, 70), (90, 100), (135, 70), (180, 100)))])
    arms = []
    for k in range(6):
        arms += arm_items(k * 60)
    tips = []
    for k in range(6):
        tips += tip_gem(k * 60)
    glints = [twinkle(*rot((0, -206), k * 60), 22, 20 + k * 22, 28) for k in range(6)]
    # only the 6-fold symmetric arms turn (60deg per loop); the hub stays put
    arms_g = stack(arms + tips + glints, "arms", pivot=C, r=Anim((0, 0, LIN), (T, 60)))
    flake = stack([arms_g] + core(), "flake", pivot=C,
                  s=Anim((0, [100, 100], OUT), (10, [105, 105], SINE), (40, [100, 100]), (90, [100, 100], OUT),
                         (100, [105, 105], SINE), (130, [100, 100]), (180, [100, 100])))
    c.add("flake", [flake])
    c.add("sparkles", [twinkle(80, 90, 16, 30, 30, halo=False), twinkle(440, 110, 18, 90, 30, halo=False),
                       twinkle(430, 430, 14, 140, 28, halo=False), twinkle(70, 420, 14, 10, 28, halo=False)])
    return c
