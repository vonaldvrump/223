"""Geometry helpers that produce Lottie bezier dicts {"c","v","i","o"}."""
import math
import re

KAPPA = 0.5523


def bez(points, closed=True, ins=None, outs=None):
    n = len(points)
    return {
        "c": closed,
        "v": [[p[0], p[1]] for p in points],
        "i": [[t[0], t[1]] for t in (ins or [(0, 0)] * n)],
        "o": [[t[0], t[1]] for t in (outs or [(0, 0)] * n)],
    }


def poly(points, closed=True):
    return bez(points, closed)


def line(p0, p1):
    return bez([p0, p1], closed=False)


def rounded(points, r=12, closed=True, k=0.56):
    """Polygon with rounded corners; r is the cut length along each edge
    (scalar or per-vertex list, 0 keeps the corner sharp)."""
    n = len(points)
    rs = list(r) if isinstance(r, (list, tuple)) else [r] * n
    vs, ins, outs = [], [], []
    for idx in range(n):
        P = points[idx]
        edge = not closed and (idx == 0 or idx == n - 1)
        if edge or rs[idx] <= 0:
            vs.append(P)
            ins.append((0, 0))
            outs.append((0, 0))
            continue
        A = points[idx - 1]
        B = points[(idx + 1) % n]
        dA = math.dist(P, A)
        dB = math.dist(P, B)
        d = min(rs[idx], dA * 0.5, dB * 0.5)
        P1 = (P[0] + (A[0] - P[0]) / dA * d, P[1] + (A[1] - P[1]) / dA * d)
        P2 = (P[0] + (B[0] - P[0]) / dB * d, P[1] + (B[1] - P[1]) / dB * d)
        vs += [P1, P2]
        ins += [(0, 0), ((P[0] - P2[0]) * k, (P[1] - P2[1]) * k)]
        outs += [((P[0] - P1[0]) * k, (P[1] - P1[1]) * k), (0, 0)]
    return bez(vs, closed, ins, outs)


def smooth(points, closed=True, t=1.0, sharp=()):
    """Catmull-Rom spline through points (indices in `sharp` stay corners)."""
    n = len(points)
    vs, ins, outs = [], [], []
    for i in range(n):
        P = points[i]
        if i in sharp:
            vs.append(P)
            ins.append((0, 0))
            outs.append((0, 0))
            continue
        if closed:
            A, B = points[i - 1], points[(i + 1) % n]
        else:
            A, B = points[max(i - 1, 0)], points[min(i + 1, n - 1)]
        T = ((B[0] - A[0]) / 6 * t, (B[1] - A[1]) / 6 * t)
        vs.append(P)
        ins.append((-T[0], -T[1]))
        outs.append(T)
    if not closed:
        ins[0] = (0, 0)
        outs[-1] = (0, 0)
    return bez(vs, closed, ins, outs)


def circle(cx, cy, r, ry=None):
    ry = r if ry is None else ry
    k = KAPPA
    v = [(cx, cy - ry), (cx + r, cy), (cx, cy + ry), (cx - r, cy)]
    i = [(-k * r, 0), (0, -k * ry), (k * r, 0), (0, k * ry)]
    o = [(k * r, 0), (0, k * ry), (-k * r, 0), (0, -k * ry)]
    return bez(v, True, i, o)


def sparkle(r=40, q=0.62, cx=0, cy=0, ry=None):
    """Four-point twinkle star with concave sides (centred on cx, cy)."""
    ry = r if ry is None else ry
    tips = [(0, -ry), (r, 0), (0, ry), (-r, 0)]
    v, i, o = [], [], []
    for x, y in tips:
        t = (-x * q, -y * q)
        v.append((cx + x, cy + y))
        i.append(t)
        o.append(t)
    return bez(v, True, i, o)


def star_points(cx, cy, R, r, n=5, rot=-90):
    pts = []
    for k in range(2 * n):
        a = math.radians(rot + k * 180 / n)
        rad = R if k % 2 == 0 else r
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts


def regular(cx, cy, r, n, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + k * 360 / n)),
             cy + r * math.sin(math.radians(rot + k * 360 / n))) for k in range(n)]


# ------------------------------------------------------------ transforms

def _map(b, fp, fv):
    return {"c": b["c"], "v": [list(fp(*p)) for p in b["v"]],
            "i": [list(fv(*t)) for t in b["i"]], "o": [list(fv(*t)) for t in b["o"]]}


def translate(b, dx, dy):
    return _map(b, lambda x, y: (x + dx, y + dy), lambda x, y: (x, y))


def scale(b, sx, sy=None, cx=0.0, cy=0.0):
    sy = sx if sy is None else sy
    return _map(b, lambda x, y: (cx + (x - cx) * sx, cy + (y - cy) * sy),
                lambda x, y: (x * sx, y * sy))


def rotate(b, deg, cx=0.0, cy=0.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return _map(b, lambda x, y: (cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca),
                lambda x, y: (x * ca - y * sa, x * sa + y * ca))


def mirror(b, cx=256.0):
    return scale(b, -1, 1, cx, 0)


def reverse(b):
    v, i, o = b["v"][::-1], b["o"][::-1], b["i"][::-1]
    return {"c": b["c"], "v": v, "i": i, "o": o}


def mirror_pts(points, cx=256.0):
    return [(2 * cx - x, y) for x, y in points]


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def lerp_bez(b0, b1, t):
    """Blend two beziers with identical topology (used to build morph keys)."""
    def mix(A, B):
        return [[a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t] for a, b in zip(A, B)]
    return {"c": b0["c"], "v": mix(b0["v"], b1["v"]), "i": mix(b0["i"], b1["i"]), "o": mix(b0["o"], b1["o"])}


# ------------------------------------------------------- flatten & clip

def _cubic(p0, c1, c2, p3, t):
    u = 1 - t
    return (u * u * u * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t * t * t * p3[0],
            u * u * u * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t * t * t * p3[1])


def flatten(b, steps=10):
    v, i, o = b["v"], b["i"], b["o"]
    n = len(v)
    segs = n if b["c"] else n - 1
    pts = []
    for k in range(segs):
        p0, p3 = v[k], v[(k + 1) % n]
        c1 = (p0[0] + o[k][0], p0[1] + o[k][1])
        c2 = (p3[0] + i[(k + 1) % n][0], p3[1] + i[(k + 1) % n][1])
        straight = o[k] == [0, 0] and i[(k + 1) % n] == [0, 0]
        for s in range(1 if straight else steps):
            pts.append(_cubic(p0, c1, c2, p3, s / (1 if straight else steps)))
    if not b["c"]:
        pts.append(tuple(v[-1]))
    return pts


def bbox(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def _area(poly_pts):
    a = 0.0
    for k in range(len(poly_pts)):
        x0, y0 = poly_pts[k]
        x1, y1 = poly_pts[(k + 1) % len(poly_pts)]
        a += x0 * y1 - x1 * y0
    return a / 2


def clip(subject, clip_poly):
    """Sutherland-Hodgman: clip any polygon by a convex polygon."""
    cp = list(clip_poly)
    if _area(cp) < 0:
        cp = cp[::-1]
    out = list(subject)
    for k in range(len(cp)):
        a, b = cp[k], cp[(k + 1) % len(cp)]
        inp, out = out, []
        if not inp:
            break

        def inside(p):
            return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0

        def inter(p, q):
            x1, y1, x2, y2 = p[0], p[1], q[0], q[1]
            x3, y3, x4, y4 = a[0], a[1], b[0], b[1]
            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(den) < 1e-9:
                return q
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

        s = inp[-1]
        for e in inp:
            if inside(e):
                if not inside(s):
                    out.append(inter(s, e))
                out.append(e)
            elif inside(s):
                out.append(inter(s, e))
            s = e
    return out


def facet(outline_bez, tri, steps=12):
    """Polygon `tri` (convex) clipped by a (possibly rounded) outline."""
    return poly(clip(flatten(outline_bez, steps), tri))


def centroid(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return sum(xs) / len(xs), sum(ys) / len(ys)


# ------------------------------------------------------------- svg path

_TOK = re.compile(r"[MmLlHhVvCcSsQqZz]|-?\d*\.?\d+(?:e[-+]?\d+)?")


def svg(d):
    """Parse an SVG path (M L H V C S Q Z, abs/rel) into a list of beziers."""
    toks = _TOK.findall(d)
    out = []
    pts, ins, outs = [], [], []
    cur = (0.0, 0.0)
    start = cur
    cmd = None
    last_ctrl = None
    k = 0

    def num():
        nonlocal k
        val = float(toks[k])
        k += 1
        return val

    def flush(closed):
        nonlocal pts, ins, outs
        if pts:
            if closed and len(pts) > 1 and math.dist(pts[0], pts[-1]) < 1e-6:
                ins[0] = ins[-1]
                pts, ins, outs = pts[:-1], ins[:-1], outs[:-1]
            out.append(bez(pts, closed, ins, outs))
        pts, ins, outs = [], [], []

    while k < len(toks):
        t = toks[k]
        if re.match(r"[A-Za-z]", t):
            cmd = t
            k += 1
            if cmd in "Zz":
                flush(True)
                cur = start
                last_ctrl = None
                continue
        rel = cmd.islower()
        c = cmd.upper()
        ox, oy = cur if rel else (0.0, 0.0)
        if c == "M":
            flush(False)
            cur = (ox + num(), oy + num())
            start = cur
            pts, ins, outs = [cur], [(0, 0)], [(0, 0)]
            cmd = "l" if rel else "L"
            last_ctrl = None
        elif c in "LHV":
            if c == "L":
                p = (ox + num(), oy + num())
            elif c == "H":
                p = ((ox if rel else 0) + num(), cur[1])
            else:
                p = (cur[0], (oy if rel else 0) + num())
            pts.append(p)
            ins.append((0, 0))
            outs.append((0, 0))
            cur = p
            last_ctrl = None
        elif c in "CSQ":
            if c == "C":
                c1 = (ox + num(), oy + num())
                c2 = (ox + num(), oy + num())
            elif c == "S":
                c1 = (2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]) if last_ctrl else cur
                c2 = (ox + num(), oy + num())
            else:
                q = (ox + num(), oy + num())
                p = (ox + num(), oy + num())
                c1 = (cur[0] + 2 / 3 * (q[0] - cur[0]), cur[1] + 2 / 3 * (q[1] - cur[1]))
                c2 = (p[0] + 2 / 3 * (q[0] - p[0]), p[1] + 2 / 3 * (q[1] - p[1]))
                outs[-1] = (c1[0] - cur[0], c1[1] - cur[1])
                pts.append(p)
                ins.append((c2[0] - p[0], c2[1] - p[1]))
                outs.append((0, 0))
                cur = p
                last_ctrl = c2
                continue
            p = (ox + num(), oy + num())
            outs[-1] = (c1[0] - cur[0], c1[1] - cur[1])
            pts.append(p)
            ins.append((c2[0] - p[0], c2[1] - p[1]))
            outs.append((0, 0))
            cur = p
            last_ctrl = c2
        else:
            raise ValueError("unsupported svg command %s" % cmd)
    flush(False)
    return out
