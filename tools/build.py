"""Build the whole pack.

    python tools/build.py            # TGS + PNG + preview sheet (PNG + MP4) + zip
    python tools/build.py --no-video # skip the animated preview

Outputs (dist/):
    tgs/<id>.tgs            animated emoji, 512x512 Lottie, 60 fps, 3 s loop
    png/100/<id>.png        static emoji for Telegram (100x100)
    png/512/<id>.png        hi-res static version / sticker
    preview/sheet.png       contact sheet in the KRONOS style
    preview/sheet.mp4       all 20 animations playing (2 loops)
    manifest.json           names, titles, suggested emoji, sizes
    KRONOS_PREMIUM_20_emoji.zip
"""
import argparse
import json
import math
import os
import random
import subprocess
import sys
import zipfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from rlottie_python import LottieAnimation  # noqa: E402

from kemoji.emoji import ident, modules  # noqa: E402
from kemoji.lottie import save_tgs  # noqa: E402

DIST = os.path.join(ROOT, "dist")
FONT = os.path.join(ROOT, "assets", "fonts", "Montserrat[wght].ttf")
ZIP_NAME = "KRONOS_PREMIUM_20_emoji.zip"

COLS, CELL, EMO, MARGIN = 5, 260, 190, 40
TITLE_H, SEC_H = 112, 50
W = COLS * CELL + 2 * MARGIN
H = TITLE_H + 2 * (SEC_H + 2 * CELL) + 26
GOLD = (255, 211, 90)


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight])
    return f


def background():
    rng = random.Random(2027)
    y = np.linspace(0, 1, H)[:, None, None]
    x = np.linspace(-1, 1, W)[None, :, None]
    top, bot = np.array([18, 38, 92.0]), np.array([6, 14, 38.0])
    img = top * (1 - y) + bot * y
    img = img * (1 - 0.32 * x ** 2)
    base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8).repeat(1, axis=0).reshape(H, W, 3), "RGB")
    over = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    for _ in range(26):  # big faint snowflakes
        cx, cy, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(26, 70)
        a0 = rng.uniform(0, 60)
        for k in range(6):
            a = math.radians(a0 + k * 60)
            ex, ey = cx + math.cos(a) * r, cy + math.sin(a) * r
            d.line([(cx, cy), (ex, ey)], fill=(190, 215, 255, 34), width=3)
            for s in (-1, 1):
                bx, by = cx + math.cos(a) * r * 0.6, cy + math.sin(a) * r * 0.6
                b = a + s * math.radians(40)
                d.line([(bx, by), (bx + math.cos(b) * r * 0.3, by + math.sin(b) * r * 0.3)], fill=(190, 215, 255, 30),
                       width=2)
    over = over.filter(ImageFilter.GaussianBlur(1.6))
    d = ImageDraw.Draw(over)
    for _ in range(420):  # snow specks
        px, py, pr = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.6, 2.2)
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(230, 240, 255, rng.randint(50, 170)))
    return Image.alpha_composite(base.convert("RGBA"), over)


def star(d, cx, cy, r, fill):
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rad = r if k % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(a) * rad, cy + math.sin(a) * rad))
    d.polygon(pts, fill=fill)


def cell_xy(idx):
    sec, k = divmod(idx, 10)
    row, col = divmod(k, COLS)
    x = MARGIN + col * CELL
    y = TITLE_H + sec * (SEC_H + 2 * CELL) + SEC_H + row * CELL
    return x, y


def decorate(img, mods):
    d = ImageDraw.Draw(img)
    title = "KRONOS PREMIUM  ·  20 emoji"
    f = font(44, 800)
    tw = d.textlength(title, font=f)
    d.text(((W - tw) / 2, 34), title, font=f, fill=(245, 249, 255))
    sub = font(19, 600)
    for sec, label in enumerate(("ПРЕМИУМ", "НОВЫЙ ГОД 2027")):
        y = TITLE_H + sec * (SEC_H + 2 * CELL) + 10
        d.text((MARGIN + 8, y), label, font=sub, fill=(169, 214, 255))
        lw = d.textlength(label, font=sub)
        d.line([(MARGIN + 20 + lw, y + 13), (W - MARGIN - 8, y + 13)], fill=(80, 120, 200), width=2)
    note = "— особые: для статуса и профиля"
    nf = font(16, 600)
    nw = d.textlength(note, font=nf)
    nx = W - MARGIN - nw - 8
    d.text((nx, TITLE_H - 22), note, font=nf, fill=GOLD)
    star(d, nx - 14, TITLE_H - 12, 9, GOLD)
    lf = font(17, 600)
    for idx, mod in enumerate(mods):
        x, y = cell_xy(idx)
        label = ident(mod).replace("_", " ", 1)
        special = getattr(mod, "SPECIAL", False)
        lw = d.textlength(label, font=lf) + (22 if special else 0)
        lx = x + (CELL - lw) / 2
        ly = y + 14 + EMO + 18
        if special:
            star(d, lx + 8, ly + 11, 9, GOLD)
            lx += 22
        d.text((lx, ly), label, font=lf, fill=GOLD if special else (223, 233, 255))
    return img


def render_static(path, frame):
    anim = LottieAnimation.from_tgs(path)
    return anim.render_pillow_frame(frame_num=frame, width=512, height=512)


def build_video(mods, tgs_paths, bg, out_path, loops=2):
    anims = [LottieAnimation.from_tgs(p) for p in tgs_paths]
    frames = [[a.render_pillow_frame(frame_num=f, width=EMO, height=EMO) for f in range(180)] for a in anims]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", "60",
           "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
           "-movflags", "+faststart", out_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(180 * loops):
        canvas = bg.copy()
        for idx in range(len(mods)):
            x, y = cell_xy(idx)
            im = frames[idx][f % 180]
            canvas.alpha_composite(im, (x + (CELL - EMO) // 2, y + 14))
        proc.stdin.write(canvas.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg failed")


INSTRUCTIONS = """KRONOS PREMIUM · 20 emoji

tgs/      — анимированные эмодзи (.tgs: 512x512, 60 fps, 3 c петля, < 64 КБ)
png_100/  — статичные эмодзи 100x100 PNG (формат Telegram для статичных эмодзи)
png_512/  — те же картинки 512x512 (стикеры, аватарки, превью)
preview/  — общий лист и видео со всеми анимациями

Как загрузить в Telegram:
1. Откройте @Stickers и отправьте /newemojipack
2. Выберите тип: «Анимированные» (файлы из tgs/) или «Статичные» (файлы из png_100/)
3. Отправьте название набора, затем по очереди: файл -> эмодзи из подсказки в manifest.json
4. /publish -> (иконка набора, можно /skip) -> короткое имя ссылки

Особые (★) — 104 winged_heart, 110 kronos_crystal, 119 midnight_clock, 120 snow_globe:
хорошо смотрятся как эмодзи-статус в профиле (Telegram Premium).
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-video", action="store_true")
    args = ap.parse_args()
    for sub in ("tgs", "png/100", "png/512", "preview"):
        os.makedirs(os.path.join(DIST, sub), exist_ok=True)

    mods = modules()
    manifest, tgs_paths = [], []
    for mod in mods:
        eid = ident(mod)
        p = os.path.join(DIST, "tgs", eid + ".tgs")
        save_tgs(mod.build(), p)
        tgs_paths.append(p)
        im = render_static(p, mod.HERO)
        im.save(os.path.join(DIST, "png", "512", eid + ".png"), optimize=True)
        im.resize((100, 100), Image.LANCZOS).save(os.path.join(DIST, "png", "100", eid + ".png"), optimize=True)
        manifest.append({"id": eid, "title": mod.TITLE, "emoji": mod.EMOJI, "special": getattr(mod, "SPECIAL", False),
                         "tgs_bytes": os.path.getsize(p)})
        print("%-24s %5.1f KB  %s" % (eid, os.path.getsize(p) / 1024, mod.TITLE))
    with open(os.path.join(DIST, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    bg = decorate(background(), mods)
    sheet = bg.copy()
    for idx, mod in enumerate(mods):
        x, y = cell_xy(idx)
        hero = Image.open(os.path.join(DIST, "png", "512", ident(mod) + ".png")).resize((EMO, EMO), Image.LANCZOS)
        sheet.alpha_composite(hero, (x + (CELL - EMO) // 2, y + 14))
    sheet.convert("RGB").save(os.path.join(DIST, "preview", "sheet.png"), optimize=True)
    print("sheet.png", sheet.size)
    video = os.path.join(DIST, "preview", "sheet.mp4")
    if not args.no_video:
        build_video(mods, tgs_paths, bg, video)
        print("sheet.mp4 %.1f MB" % (os.path.getsize(video) / 2 ** 20))

    zpath = os.path.join(DIST, ZIP_NAME)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("KRONOS_PREMIUM/README.txt", INSTRUCTIONS)
        z.write(os.path.join(DIST, "manifest.json"), "KRONOS_PREMIUM/manifest.json")
        for eid in (ident(m) for m in mods):
            z.write(os.path.join(DIST, "tgs", eid + ".tgs"), "KRONOS_PREMIUM/tgs/%s.tgs" % eid)
            z.write(os.path.join(DIST, "png", "100", eid + ".png"), "KRONOS_PREMIUM/png_100/%s.png" % eid)
            z.write(os.path.join(DIST, "png", "512", eid + ".png"), "KRONOS_PREMIUM/png_512/%s.png" % eid)
        z.write(os.path.join(DIST, "preview", "sheet.png"), "KRONOS_PREMIUM/preview/sheet.png")
        if os.path.exists(video):
            z.write(video, "KRONOS_PREMIUM/preview/sheet.mp4")
    print("%s %.1f MB" % (ZIP_NAME, os.path.getsize(zpath) / 2 ** 20))


if __name__ == "__main__":
    main()
