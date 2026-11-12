"""Text as plain vector paths (Telegram forbids text layers)."""
import json
import os

_DATA = None


def _font():
    global _DATA
    if _DATA is None:
        with open(os.path.join(os.path.dirname(__file__), "data", "glyphs.json")) as fh:
            _DATA = json.load(fh)
    return _DATA


def glyphs(text, x, baseline, cap_h, tracking=0.0, center_x=None):
    """Lay out `text`; returns [(char, [bezier...], (x0, y0, x1, y1))].
    cap_h is the cap height in px; tracking is extra spacing in px."""
    f = _font()
    s = cap_h / f["cap"]
    width = sum(f["glyphs"][ch]["adv"] * s for ch in text) + tracking * (len(text) - 1)
    if center_x is not None:
        x = center_x - width / 2
    out = []
    pen = x
    for ch in text:
        g = f["glyphs"][ch]
        bs = []
        for c in g["contours"]:
            bs.append({"c": True,
                       "v": [[pen + vx * s, baseline - vy * s] for vx, vy in c["v"]],
                       "i": [[ix * s, -iy * s] for ix, iy in c["i"]],
                       "o": [[ox * s, -oy * s] for ox, oy in c["o"]]})
        xs = [p[0] for b in bs for p in b["v"]]
        ys = [p[1] for b in bs for p in b["v"]]
        out.append((ch, bs, (min(xs), min(ys), max(xs), max(ys))))
        pen += g["adv"] * s + tracking
    return out


def text_paths(text, x, baseline, cap_h, tracking=0.0, center_x=None):
    return [b for _, bs, _ in glyphs(text, x, baseline, cap_h, tracking, center_x) for b in bs]
