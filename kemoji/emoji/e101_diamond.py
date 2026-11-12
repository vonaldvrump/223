"""101 · Бриллиант — brilliant-cut diamond with a facet light-wave and glints."""
from ..gems import brilliant
from ..lottie import Anim, Comp
from ..style import SKY, bob, glow, sheen, stack, sway, twinkle

NAME = "diamond"
TITLE = "Бриллиант"
EMOJI = "💎"
HERO = 144


def build(T=180):
    c = Comp(NAME, T)
    c.add("aura", [glow(256, 284, 214, SKY, 0.36, opacity=Anim((0, 65), (90, 100), (180, 65)))])

    gem, outline = brilliant(256, 224, 186, "blue", wave=22, step=5)
    body = stack([
        gem,
        sheen(outline, 104, 140, angle=30, width=40, alpha=0.7),
        twinkle(182, 150, 34, 46, 34),
        twinkle(438, 222, 26, 88, 32),
        twinkle(256, 444, 26, 130, 32),
    ], "diamond", pivot=(256, 290), p=bob(256, 290, 7, T), r=sway(2.2, T))
    c.add("diamond", [body])

    c.add("sparkles", [
        twinkle(86, 120, 18, 12, 30, halo=False),
        twinkle(430, 96, 22, 60, 34, halo=False),
        twinkle(462, 336, 14, 104, 28, halo=False),
        twinkle(56, 306, 16, 146, 30, halo=False),
    ])
    return c
