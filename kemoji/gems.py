"""Cut gemstones shared by several emoji (all lists are in painter's order)."""
from . import geom as G
from .lottie import fill
from .style import OW, WHITE, dgrad, lines, outlined, shape, shimmer, stack

PALETTES = {
    # crown facets (5) and pavilion facets (4): (light, dark) pairs
    "blue": {
        "crown": [("#f4faff", "#d2eaff"), ("#d3e9ff", "#a8d3ff"), ("#ffffff", "#e3f1ff"),
                  ("#b8dcff", "#8bc3fb"), ("#95c9fb", "#67a6f2")],
        "pav": [("#b5dcff", "#6aa7f3"), ("#7cb9f9", "#3f7fe6"), ("#3a74de", "#1c46ad"),
                ("#5d99ef", "#2a5fd0")],
    },
    "violet": {
        "crown": [("#f7f3ff", "#ddd2ff"), ("#e2d7ff", "#bfaaff"), ("#ffffff", "#ece6ff"),
                  ("#c9b8ff", "#a48af7"), ("#ad97fb", "#8366ef")],
        "pav": [("#c9b8ff", "#8f74f2"), ("#9c86f6", "#6a4be0"), ("#5a3fd0", "#3a23a3"),
                ("#7a62e8", "#4c32c0")],
    },
    "ice": {
        "crown": [("#ffffff", "#e9f5ff"), ("#eaf5ff", "#cde6fb"), ("#ffffff", "#f1f8ff"),
                  ("#d6ebfd", "#b4d6f6"), ("#c2e0fb", "#95c3ef")],
        "pav": [("#d4ebff", "#9fcaf4"), ("#a9d2f9", "#6ea7ea"), ("#6d9fe6", "#3f72c9"),
                ("#8dbaf0", "#5687d6")],
    },
}


def brilliant(cx, gy, hw, palette="blue", wave=None, step=5, ow=OW, edge_w=None,
              fire=False, nm="brilliant"):
    """Front view of a brilliant cut.  (cx, gy) is the girdle centre, hw the
    half width.  `wave` = start frame of a left-to-right facet shimmer.
    Returns (group, outline_bezier)."""
    pal = PALETTES[palette]
    s = hw

    def P(x, y):
        return (cx + x * s, gy + y * s)

    TL, TR = P(-0.46, -0.44), P(0.46, -0.44)
    GL, GR = P(-1, 0), P(1, 0)
    B = P(0, 1.2)
    g1, g2, g3 = P(-0.57, 0), P(0, 0), P(0.57, 0)
    outline = G.rounded([TL, TR, GR, B, GL], [0.06 * s, 0.06 * s, 0.07 * s, 0.09 * s, 0.07 * s])

    crown = [[GL, TL, g1], [TL, g2, g1], [TL, TR, g2], [TR, g3, g2], [TR, GR, g3]]
    pav = [[GL, g1, B], [g1, g2, B], [g2, g3, B], [g3, GR, B]]

    items = [outlined(outline, fill(pal["pav"][1][1]), ow=ow, nm="outline")]
    facets = []
    for tri, (c0, c1) in list(zip(crown, pal["crown"])) + list(zip(pav, pal["pav"])):
        fb = G.facet(outline, tri)
        x0, y0, x1, y1 = G.bbox(fb["v"])
        facets.append(fb)
        items.append(shape(fb, dgrad(c0, c1, (x0, y0), (x1 * 0.3 + x0 * 0.7, y1)), nm="facet"))

    if fire:
        # tiny dispersion slivers: the "fire" of a real diamond
        items.append(shape(G.poly([P(-0.5, 0.06), P(-0.08, 0.06), P(-0.2, 0.42)]), fill("#e3d9ff", 50), nm="fire"))
        items.append(shape(G.poly([P(0.1, 0.07), P(0.5, 0.07), P(0.18, 0.5)]), fill("#c9f6ff", 35), nm="fire"))

    ew = edge_w if edge_w is not None else max(2.0, 3.2 * s / 186)
    edges = [G.line(TL, g1), G.line(TL, g2), G.line(TR, g2), G.line(TR, g3), G.line(g1, B),
             G.line(g2, B), G.line(g3, B), G.line(P(-0.98, 0), P(0.98, 0))]
    items.append(lines(edges, WHITE, ew, 55, nm="edges"))

    items.append(shape(G.poly([P(-0.3, -0.37), P(-0.12, -0.37), P(-0.34, -0.12)]), fill(WHITE, 85), nm="hl"))
    items.append(shape(G.circle(*P(-0.66, -0.2), 0.05 * s), fill(WHITE, 90), nm="hl"))

    if wave is not None:
        order = sorted(range(len(facets)), key=lambda k: G.centroid(facets[k]["v"])[0])
        for rank, k in enumerate(order):
            items.append(shimmer(facets[k], wave + rank * step, 24, 58 if k < 5 else 46))
    return stack(items, nm), outline


def round_gem(cx, cy, r, c_light, c_dark, ow=8, star=True, nm="gem"):
    """Round gem seen from above, with star facets."""
    outline = G.circle(cx, cy, r)
    items = [outlined(outline, dgrad(c_light, c_dark, (cx - r, cy - r), (cx + r * 0.6, cy + r)), ow=ow)]
    if star:
        pts = G.regular(cx, cy, r * 0.5, 8, rot=-90)
        items.append(shape(G.poly(pts), fill(WHITE, 28), nm="table"))
        spokes = [G.line(p, (cx + (p[0] - cx) * 1.85, cy + (p[1] - cy) * 1.85)) for p in pts]
        items.append(lines(spokes, WHITE, max(1.5, r * 0.07), 35, nm="spokes"))
    items.append(shape(G.circle(cx - r * 0.36, cy - r * 0.38, r * 0.2), fill(WHITE, 90), nm="hl"))
    return stack(items, nm), outline


def kite_gem(cx, cy, w, h, c_light, c_mid, c_dark, ow=8, nm="kite"):
    """Rhombus gem with four facets meeting in the middle."""
    T, R, Bm, L = (cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)
    C = (cx, cy)
    outline = G.rounded([T, R, Bm, L], max(2, w * 0.06))
    items = [
        outlined(outline, fill(c_dark), ow=ow),
        shape(G.facet(outline, [T, C, L]), fill(c_light), nm="f"),
        shape(G.facet(outline, [T, R, C]), fill(c_mid), nm="f"),
        shape(G.facet(outline, [L, C, Bm]), fill(c_mid), nm="f"),
        shape(G.facet(outline, [C, R, Bm]), fill(c_dark), nm="f"),
        shape(G.poly([(cx - w * 0.2, cy - h * 0.1), (cx - w * 0.07, cy - h * 0.3), (cx - w * 0.04, cy - h * 0.1)]),
              fill(WHITE, 85), nm="hl"),
    ]
    return stack(items, nm), outline
