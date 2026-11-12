"""Tiny Lottie / Telegram TGS authoring layer.

Only the subset Telegram allows for animated stickers and emoji is exposed:
shape layers, paths, ellipses, rectangles, solid and gradient fills, solid
strokes, trim paths and plain (non-skewed) transforms.  No masks, mattes,
expressions, star shapes, repeaters, gradient strokes, images or text.
"""
import gzip
import json

FPS = 60
SIZE = 512

# Easing = cubic-bezier(x1, y1, x2, y2) of the segment that starts at a key.
LIN = (0.0, 0.0, 1.0, 1.0)
SINE = (0.37, 0.0, 0.63, 1.0)
EASE = (0.65, 0.0, 0.35, 1.0)
OUT = (0.33, 1.0, 0.68, 1.0)
IN = (0.32, 0.0, 0.67, 0.0)
BACK = (0.34, 1.56, 0.64, 1.0)
HOLD = "hold"


class Anim:
    """Keyframed value: Anim((t, value[, ease]), ...)."""

    def __init__(self, *keys):
        ks = []
        for k in keys:
            ks.append((k[0], k[1], k[2] if len(k) > 2 else SINE))
        ks.sort(key=lambda k: k[0])
        self.keys = ks

    def map(self, fn):
        return Anim(*[(t, fn(v), e) for t, v, e in self.keys])

    def shift(self, dt):
        return Anim(*[(t + dt, v, e) for t, v, e in self.keys])


def rgba(c, a=1.0):
    if isinstance(c, (list, tuple)):
        return list(c)
    c = c.lstrip("#")
    return [round(int(c[i:i + 2], 16) / 255, 3) for i in (0, 2, 4)] + [a]


def _num(x, nd):
    x = round(float(x), nd)
    return int(x) if x == int(x) else x


def _clean(v, nd):
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return _num(v, nd)
    if isinstance(v, (list, tuple)):
        return [_clean(x, nd) for x in v]
    if isinstance(v, dict):
        return {k: _clean(x, nd) for k, x in v.items()}
    return v


def _wrap(v):
    if isinstance(v, dict):
        return [v]
    if isinstance(v, (list, tuple)):
        return list(v)
    return [v]


def prop(v, nd=2):
    if isinstance(v, Anim):
        out = []
        n = len(v.keys)
        for i, (t, val, ease) in enumerate(v.keys):
            kf = {"t": _num(t, 2), "s": _clean(_wrap(val), nd)}
            if i + 1 < n:
                if ease == HOLD:
                    kf["h"] = 1
                else:
                    x1, y1, x2, y2 = ease
                    kf["o"] = {"x": [x1], "y": [y1]}
                    kf["i"] = {"x": [x2], "y": [y2]}
                    # Explicit end values keep older rlottie builds happy.
                    kf["e"] = _clean(_wrap(v.keys[i + 1][1]), nd)
            out.append(kf)
        return {"a": 1, "k": out}
    return {"a": 0, "k": _clean(v, nd)}


def _col(c):
    return c.map(rgba) if isinstance(c, Anim) else rgba(c)


# ---------------------------------------------------------------- shapes

def path(b, nm="path"):
    return {"ty": "sh", "nm": nm, "ks": prop(b)}


def ellipse(c, size, nm="ellipse"):
    return {"ty": "el", "nm": nm, "d": 1, "p": prop(c), "s": prop(size)}


def rect(c, size, r=0, nm="rect"):
    return {"ty": "rc", "nm": nm, "d": 1, "p": prop(c), "s": prop(size), "r": prop(r)}


def fill(color, opacity=100, rule=1, nm="fill"):
    return {"ty": "fl", "nm": nm, "c": prop(_col(color), 3), "o": prop(opacity), "r": rule}


def stroke(color, width, opacity=100, cap=2, join=2, nm="stroke"):
    return {"ty": "st", "nm": nm, "c": prop(_col(color), 3), "o": prop(opacity),
            "w": prop(width), "lc": cap, "lj": join, "ml": 4}


def gradient(stops, start, end, radial=False, opacity=100, rule=1, nm="grad"):
    """stops: [(pos, color[, alpha])].  Opacity stops reuse the colour positions."""
    st = [(s[0], s[1], s[2] if len(s) > 2 else 1.0) for s in stops]
    vals = []
    for pos, c, _ in st:
        vals += [pos] + rgba(c)[:3]
    if any(a < 1 for _, _, a in st):
        for pos, _, a in st:
            vals += [pos, a]
    g = {"ty": "gf", "nm": nm, "o": prop(opacity), "r": rule, "s": prop(start),
         "e": prop(end), "t": 2 if radial else 1, "g": {"p": len(st), "k": prop(vals, 3)}}
    if radial:
        g["h"] = prop(0)
        g["a"] = prop(0)
    return g


def trim(start=0, end=100, offset=0, nm="trim"):
    return {"ty": "tm", "nm": nm, "s": prop(start), "e": prop(end), "o": prop(offset), "m": 1}


def transform(p=(0, 0), a=(0, 0), s=(100, 100), r=0, o=100):
    return {"ty": "tr", "p": prop(p), "a": prop(a), "s": prop(s), "r": prop(r),
            "o": prop(o), "sk": prop(0), "sa": prop(0)}


def group(items, nm="group", p=None, a=None, s=(100, 100), r=0, o=100, pivot=None):
    """Group with its own transform.  `pivot` sets the anchor (and, unless `p` is
    given, the position) so scale/rotation happen around that canvas point."""
    if pivot is not None:
        a = pivot
        if p is None:
            p = pivot
    p = (0, 0) if p is None else p
    a = (0, 0) if a is None else a
    return {"ty": "gr", "nm": nm, "it": list(items) + [transform(p, a, s, r, o)]}


# ---------------------------------------------------------------- layers

def _v3(v, z):
    if isinstance(v, Anim):
        return v.map(lambda x: [x[0], x[1], z])
    return [v[0], v[1], z]


class Comp:
    """Composition; layers are added back-to-front."""

    def __init__(self, name, frames=180):
        self.name = name
        self.frames = frames
        self.layers = []

    def add(self, nm, shapes, p=(0, 0), a=(0, 0), s=(100, 100), r=0, o=100, pivot=None):
        if pivot is not None:
            a = pivot
            if p == (0, 0):
                p = pivot
        self.layers.append({
            "ddd": 0, "ty": 4, "nm": nm, "sr": 1,
            "ks": {"o": prop(o), "r": prop(r), "p": prop(_v3(p, 0)),
                   "a": prop(_v3(a, 0)), "s": prop(_v3(s, 100))},
            "ao": 0, "shapes": list(shapes), "ip": 0, "op": self.frames, "st": 0, "bm": 0,
        })
        return self

    def json(self):
        layers = []
        for i, layer in enumerate(reversed(self.layers)):
            layer = dict(layer)
            layer["ind"] = i + 1
            layers.append(layer)
        return {"tgs": 1, "v": "5.5.2", "fr": FPS, "ip": 0, "op": self.frames,
                "w": SIZE, "h": SIZE, "nm": self.name, "ddd": 0, "assets": [],
                "layers": layers}


def dumps(comp):
    return json.dumps(comp.json(), separators=(",", ":"), ensure_ascii=False)


def save_tgs(comp, file_path):
    raw = dumps(comp).encode("utf-8")
    with open(file_path, "wb") as fh:
        with gzip.GzipFile(fileobj=fh, mode="wb", compresslevel=9, mtime=0) as gz:
            gz.write(raw)
    return len(raw)
