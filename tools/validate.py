"""Validate every dist/tgs/*.tgs against Telegram's animated emoji rules.

Checks: gzip size <= 64 KB, 512x512 canvas, 60 fps, <= 180 frames (3 s),
no forbidden Lottie features (masks, mattes, expressions, effects, star
shapes, gradient strokes, repeaters, merge paths, skew, 3D, images, text,
solids, time remap), nothing drawn on the canvas border in any frame, and a
seamless loop (frame 0 == frame `op` rendered from an extended copy).
python-lottie's TGS validator is run as a second opinion.
"""
import glob
import gzip
import json
import os
import sys

import numpy as np
from rlottie_python import LottieAnimation

from lottie.exporters.tgs_validator import Severity, TgsValidator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORBIDDEN_SHAPES = {"sr": "star shape", "gs": "gradient stroke", "rp": "repeater", "mm": "merge paths"}


def walk(o, issues, where="root"):
    if isinstance(o, dict):
        if "x" in o and isinstance(o.get("x"), str):
            issues.append("expression at %s" % where)
        ty = o.get("ty")
        if isinstance(ty, str) and ty in FORBIDDEN_SHAPES:
            issues.append("%s at %s" % (FORBIDDEN_SHAPES[ty], where))
        if ty == "tr":
            sk = o.get("sk", {"a": 0, "k": 0})
            if sk.get("a") or sk.get("k"):
                issues.append("skew at %s" % where)
        for k, v in o.items():
            walk(v, issues, where + "." + str(k))
    elif isinstance(o, list):
        for k, v in enumerate(o):
            walk(v, issues, "%s[%d]" % (where, k))


def check_layers(data, issues):
    for layer in data["layers"]:
        name = layer.get("nm")
        if layer.get("ty") != 4:
            issues.append("layer %s has type %s (only shape layers used)" % (name, layer.get("ty")))
        if layer.get("masksProperties"):
            issues.append("mask on %s" % name)
        if layer.get("tt") or layer.get("td"):
            issues.append("track matte on %s" % name)
        if layer.get("ef"):
            issues.append("effects on %s" % name)
        if layer.get("ddd"):
            issues.append("3D layer %s" % name)
        if layer.get("ao"):
            issues.append("auto-orient on %s" % name)
        if layer.get("tm"):
            issues.append("time remap on %s" % name)
        if layer.get("sr", 1) != 1:
            issues.append("time stretch on %s" % name)


def render_all(data, frames, size=512):
    anim = LottieAnimation.from_data(json.dumps(data))
    for f in range(frames):
        yield f, np.asarray(anim.render_pillow_frame(frame_num=f, width=size, height=size))


def validate(path):
    issues = []
    size = os.path.getsize(path)
    if size > 64 * 1024:
        issues.append("file is %.1f KB (> 64 KB)" % (size / 1024))
    with gzip.open(path, "rb") as fh:
        data = json.loads(fh.read())
    if data.get("tgs") != 1:
        issues.append("missing tgs=1")
    if data["w"] != 512 or data["h"] != 512:
        issues.append("canvas %sx%s" % (data["w"], data["h"]))
    if data["fr"] != 60:
        issues.append("fps %s" % data["fr"])
    frames = int(data["op"] - data["ip"])
    if frames > 180:
        issues.append("%d frames (> 180)" % frames)
    check_layers(data, issues)
    walk(data, issues)

    v = TgsValidator(Severity.Note)
    v.check_file(path)
    issues += ["python-lottie: %s" % e for e in v.errors]

    # nothing may touch the canvas border
    worst = (0, None)
    first = None
    for f, px in render_all(data, frames):
        a = px[:, :, 3]
        edge = max(a[:2, :].max(), a[-2:, :].max(), a[:, :2].max(), a[:, -2:].max())
        if edge > worst[0]:
            worst = (int(edge), f)
        if f == 0:
            first = px.astype(int)
    if worst[0] > 6:
        issues.append("drawn on canvas border (alpha %d at frame %d)" % worst)

    # loop seam: render frame `op` from an extended copy and compare to frame 0
    ext = json.loads(json.dumps(data))
    ext["op"] = frames + 1
    for layer in ext["layers"]:
        layer["op"] = frames + 1
    anim = LottieAnimation.from_data(json.dumps(ext))
    last = np.asarray(anim.render_pillow_frame(frame_num=frames, width=512, height=512)).astype(int)
    # 2x2 box average first: rotated high-contrast edges re-rasterise with a
    # few levels of anti-aliasing noise, a real seam covers an area
    def ds(im):
        return im.reshape(256, 2, 256, 2, 4).mean(axis=(1, 3))
    seam = np.abs(ds(last) - ds(first)).max()
    if seam > 40:
        issues.append("loop seam: frame %d differs from frame 0 (max diff %d)" % (frames, seam))
    return size, frames, issues, int(seam)


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "dist", "tgs", "*.tgs")))
    if len(sys.argv) > 1:
        files = [f for f in files if os.path.basename(f)[:3] in sys.argv[1:]]
    bad = 0
    for f in files:
        size, frames, issues, seam = validate(f)
        status = "OK " if not issues else "ERR"
        bad += bool(issues)
        print("%s %-26s %5.1f KB  %3d frames  seam=%d" % (status, os.path.basename(f), size / 1024, frames, seam))
        for i in issues:
            print("      - " + i)
    print("%d file(s), %d with problems" % (len(files), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
