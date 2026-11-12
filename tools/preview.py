"""Dev preview: build selected emoji and render a frame strip.

    python tools/preview.py 101 102 --frames 0,30,60,90,120,150 --out /tmp/prev
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from rlottie_python import LottieAnimation  # noqa: E402

from kemoji.emoji import ident, modules  # noqa: E402
from kemoji.lottie import save_tgs  # noqa: E402


def render(tgs_path, frames, size):
    anim = LottieAnimation.from_tgs(tgs_path)
    out = [anim.render_pillow_frame(frame_num=f, width=size, height=size) for f in frames]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--frames", default="0,30,60,90,120,150")
    ap.add_argument("--size", type=int, default=256)
    ap.add_argument("--out", default="/tmp/prev")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    tgs_dir = os.path.join(ROOT, "dist", "tgs")
    os.makedirs(tgs_dir, exist_ok=True)
    frames = [int(x) for x in args.frames.split(",")]
    for mod in modules():
        eid = ident(mod)
        if args.ids and eid[:3] not in args.ids:
            continue
        comp = mod.build()
        p = os.path.join(tgs_dir, eid + ".tgs")
        raw = save_tgs(comp, p)
        imgs = render(p, frames, args.size)
        S = args.size
        strip = Image.new("RGB", (S * len(frames), S + S // 2 + 18), "#0d1a3d")
        light = Image.new("RGB", (S * len(frames), S // 2), "#eef3f9")
        strip.paste(light, (0, S + 18))
        d = ImageDraw.Draw(strip)
        for k, (f, im) in enumerate(zip(frames, imgs)):
            strip.paste(im, (k * S, 0), im)
            small = im.resize((S // 2, S // 2), Image.LANCZOS)
            strip.paste(small, (k * S + S // 4, S + 18), small)
            d.text((k * S + 4, S + 3), "f%d" % f, fill="#9fb6e0")
        strip.save(os.path.join(args.out, eid + ".png"))
        print("%s raw=%.1fKB tgs=%.1fKB" % (eid, raw / 1024, os.path.getsize(p) / 1024))


if __name__ == "__main__":
    main()
