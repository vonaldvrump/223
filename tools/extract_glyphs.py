"""One-off: extract glyph outlines from Montserrat Black (SIL OFL 1.1) into
kemoji/data/glyphs.json so the build does not need the font file.

    python tools/extract_glyphs.py /path/to/Montserrat[wght].ttf
"""
import json
import os
import sys

from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARS = "0123456789KVIPLUXNEW"


class LottiePen(BasePen):
    def __init__(self, glyphset):
        super().__init__(glyphset)
        self.contours = []
        self.cur = None

    def _moveTo(self, p):
        self.cur = {"v": [list(p)], "i": [[0, 0]], "o": [[0, 0]]}

    def _lineTo(self, p):
        self.cur["v"].append(list(p))
        self.cur["i"].append([0, 0])
        self.cur["o"].append([0, 0])

    def _curveToOne(self, c1, c2, p):
        last = self.cur["v"][-1]
        self.cur["o"][-1] = [c1[0] - last[0], c1[1] - last[1]]
        self.cur["v"].append(list(p))
        self.cur["i"].append([c2[0] - p[0], c2[1] - p[1]])
        self.cur["o"].append([0, 0])

    def _qCurveToOne(self, q, p):
        p0 = self.cur["v"][-1]
        c1 = (p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1]))
        c2 = (p[0] + 2 / 3 * (q[0] - p[0]), p[1] + 2 / 3 * (q[1] - p[1]))
        self._curveToOne(c1, c2, p)

    def _closePath(self):
        c = self.cur
        if len(c["v"]) > 1 and c["v"][0] == c["v"][-1]:
            c["i"][0] = c["i"][-1]
            for k in ("v", "i", "o"):
                c[k] = c[k][:-1]
        self.contours.append(c)
        self.cur = None

    _endPath = _closePath


def main(font_path):
    font = TTFont(font_path)
    if "fvar" in font:
        font = instantiateVariableFont(font, {"wght": 900})
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    out = {"source": "Montserrat Black (SIL Open Font License 1.1)",
           "upm": font["head"].unitsPerEm, "cap": font["OS/2"].sCapHeight, "glyphs": {}}
    for ch in CHARS:
        name = cmap[ord(ch)]
        pen = LottiePen(gs)
        gs[name].draw(pen)
        rnd = [{k: [[round(a, 1), round(b, 1)] for a, b in c[k]] for k in ("v", "i", "o")} for c in pen.contours]
        out["glyphs"][ch] = {"adv": gs[name].width, "contours": rnd}
    dst = os.path.join(ROOT, "kemoji", "data", "glyphs.json")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w") as fh:
        json.dump(out, fh, separators=(",", ":"))
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main(sys.argv[1])
