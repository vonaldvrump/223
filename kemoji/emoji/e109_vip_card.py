"""109 · VIP-карта — sapphire card with a platinum chip, a diamond and holo sheen."""
from .. import geom as G
from ..gems import brilliant
from ..glyphs import glyphs, text_paths
from ..lottie import Anim, Comp, fill
from ..style import (INK, SILVER, SILVER_LO, SKY, WHITE, bob, dgrad, glow, lines, outlined, shape, sheen,
                     stack, twinkle, vgrad)

NAME = "vip_card"
TITLE = "VIP-карта"
EMOJI = "💳"
HERO = 83


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 270, 226, SKY, 0.3, opacity=Anim((0, 75), (90, 100), (180, 75)))])

    card = G.rounded([(66, 148), (446, 148), (446, 392), (66, 392)], 34)
    flat = G.flatten(card, 12)
    items = [outlined(card, dgrad("#5a9cf5", "#16348a", (66, 148), (420, 400), mid="#2f6be0"), nm="card")]
    bands = [G.poly(G.clip(flat, [(150, 140), (230, 140), (110, 400), (30, 400)])),
             G.poly(G.clip(flat, [(262, 140), (296, 140), (176, 400), (142, 400)]))]
    items.append(shape(bands, fill(WHITE, 9), nm="stripes"))
    items.append(lines(G.rounded([(82, 164), (430, 164), (430, 376), (82, 376)], 24), WHITE, 3, 35, nm="border"))

    chip = G.rounded([(102, 194), (172, 194), (172, 248), (102, 248)], 11)
    items.append(outlined(chip, dgrad(WHITE, SILVER_LO, (102, 194), (172, 248), mid=SILVER), ow=6, nm="chip"))
    items.append(lines([G.line((102, 221), (172, 221)), G.line((126, 194), (126, 248)), G.line((148, 194), (148, 248)),
                        G.rounded([(122, 208), (152, 208), (152, 234), (122, 234)], 5)], INK, 3, 45, nm="contacts"))
    arcs = [G.svg("M %d 205 C %d 214 %d 228 %d 237" % (194 + k * 12, 200 + k * 13, 200 + k * 13, 194 + k * 12))[0]
            for k in range(3)]
    items.append(lines(arcs, WHITE, 5, 80, nm="nfc"))

    vip = text_paths("VIP", 0, 344, 98, tracking=8, center_x=256)
    items.append(outlined(vip, vgrad(WHITE, "#bcd6f7", 246, 344), ow=9, nm="vip"))
    dots = []
    for g0 in (100, 162):
        for k in range(4):
            dots.append(G.circle(g0 + k * 12, 368, 4.2))
    items.append(shape(dots, fill(WHITE, 70), nm="dots"))
    year = [b for _, bs, _ in glyphs("2027", 0, 377, 20, tracking=2, center_x=268) for b in bs]
    items.append(shape(year, fill(WHITE, 75), nm="year"))

    gem, gem_outline = brilliant(386, 198, 30, "ice", wave=60, step=4, ow=8)
    items.append(gem)
    items += [
        sheen(card, 24, 64, angle=30, width=60, alpha=0.5),
        sheen(card, 112, 152, angle=30, width=70, alpha=0.45, color="#d9ccff"),
        sheen(vip, 80, 112, angle=30, width=30, alpha=0.8),
        twinkle(372, 182, 26, 70, 30),
        twinkle(108, 186, 18, 140, 28),
    ]
    tilt = Anim((0, -11), (90, -5), (180, -11))
    c.add("card", [stack(items, "vip", pivot=(256, 270), p=bob(256, 268, 8, T), r=tilt)])
    c.add("sparkles", [twinkle(70, 110, 18, 16, 30, halo=False), twinkle(452, 96, 20, 90, 32, halo=False),
                       twinkle(450, 420, 14, 120, 28, halo=False), twinkle(62, 430, 16, 156, 22, halo=False)])
    return c
