#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

Deterministic: fixed layout, fixed text, fixed palette; Pillow only.
Run: python3 tools/generate_image.py  -> writes entry.png next to main.ts.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (158, 28, 28)
BLUE = (24, 64, 110)
GREY = (96, 90, 80)
LIGHT = (233, 227, 212)
RULE = (60, 55, 45)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 62)
F_KICK = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSerif-Bold.ttf", 34)
F_HEAD2 = font("DejaVuSerif-Bold.ttf", 27)
F_HEAD3 = font("DejaVuSerif-Bold.ttf", 24)
F_DECK = font("DejaVuSerif.ttf", 20)
F_BODY = font("DejaVuSerif.ttf", 18)
F_SMALL = font("DejaVuSans.ttf", 15)
F_TINY = font("DejaVuSans.ttf", 13)
F_CAP = font("DejaVuSans-Bold.ttf", 13)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.32)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def headline(draw, x, y, width, text, fnt, fill=INK, leading=None):
    return para(draw, x, y, width, text, fnt, fill=fill, leading=leading)


def hrule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def vrule(draw, x, y0, y1, width=1, fill=RULE):
    draw.line([(x, y0), (x, y1)], fill=fill, width=width)


def kicker(draw, x, y, text, color=RED):
    draw.text((x, y), text, font=F_KICK, fill=color)
    return y + 24


def draw_gulf_map(draw, x, y, w, h):
    """Schematic Gulf as a wide strip: sea, two struck bases, Hormuz arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 236), outline=RULE, width=1)
    draw.polygon([(x + 8, y + h - 6), (x + 8, y + 12), (x + int(w * 0.38), y + 8),
                  (x + int(w * 0.46), y + h - 6)], fill=(226, 216, 188))
    draw.polygon([(x + int(w * 0.62), y + 8), (x + w - 8, y + 6),
                  (x + w - 8, y + h - 6), (x + int(w * 0.66), y + h - 6)],
                 fill=(226, 216, 188))
    draw.line([(x + int(w * 0.52), y + h - 12), (x + w - 26, y + 12)],
              fill=BLUE, width=3)
    draw.polygon([(x + w - 26, y + 12), (x + w - 40, y + 12), (x + w - 30, y + 22)],
                 fill=BLUE)
    kx, ky = x + int(w * 0.20), y + int(h * 0.58)
    bx, by = x + int(w * 0.44), y + int(h * 0.58)
    for cx, cy in ((kx, ky), (bx, by)):
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED, outline=INK, width=1)
    draw.text((x + 10, y + 4), "THE GULF", font=F_CAP, fill=GREY)
    draw.text((kx - 22, ky - 22), "KUWAIT", font=F_CAP, fill=INK)
    draw.text((bx - 24, by - 22), "BAHRAIN", font=F_CAP, fill=INK)
    draw.text((x + w - 150, y + h - 20), "STRAIT OF HORMUZ", font=F_CAP, fill=BLUE)


def draw_bridge(draw, x, y, w, h):
    """Kerch bridge schematic: two towers, a collapsed middle span."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 222, 208), outline=RULE, width=1)
    draw.text((x + 10, y + 4), "KERCH BRIDGE — ROAD SPAN DOWN", font=F_CAP, fill=RED)
    base = y + h - 14
    draw.line([(x + 10, base), (x + w - 10, base)], fill=INK, width=3)
    # towers
    for tx in (x + int(w * 0.22), x + int(w * 0.72)):
        draw.line([(tx, base), (tx, y + 26)], fill=INK, width=4)
        draw.line([(tx - 16, y + 26), (tx + 16, y + 26)], fill=INK, width=3)
    # deck: left intact, middle dropped, right intact
    draw.line([(x + 10, y + 40), (x + int(w * 0.44), y + 40)], fill=INK, width=5)
    draw.line([(x + int(w * 0.60), y + 40), (x + w - 10, y + 40)], fill=INK, width=5)
    # fallen span pieces in the water
    draw.line([(x + int(w * 0.44), y + 40), (x + int(w * 0.50), base)],
              fill=RED, width=4)
    draw.line([(x + int(w * 0.60), y + 40), (x + int(w * 0.54), base)],
              fill=RED, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # double outer border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)
    d.rectangle([16, 16, W - 17, H - 17], outline=RULE, width=1)

    # ---- masthead ----
    d.text((W // 2, 34), "ONE DAY  •  ONE PAGE  •  THE WORLD'S NEWS",
           font=F_SMALL, fill=GREY, anchor="ma")
    d.text((W // 2, 58), "THE WORLD IN ONE PAGE", font=F_TITLE, fill=INK, anchor="ma")
    hrule(d, 28, 132, W - 28, 3)
    d.text((28, 142), "SUNDAY, 22 NOVEMBER 2026", font=F_KICK, fill=INK)
    d.text((W // 2, 142), "WORLD NEWS OF THE DAY", font=F_KICK, fill=RED, anchor="ma")
    d.text((W - 28, 142), "No. 326", font=F_KICK, fill=INK, anchor="ra")
    hrule(d, 28, 168, W - 28, 2)

    # ---- LEAD: Gulf (left, wide) ----
    lx, lw = 28, 640
    y = kicker(d, lx, 182, "THE GULF  —  LEAD STORY")
    y = headline(d, lx, y, lw, "IRAN HITS U.S. BASES IN BAHRAIN", F_HEAD)
    y = headline(d, lx, y + 2, lw,
                 "Kuwait repels drone attack on Ali Al Salem air base",
                 F_DECK, fill=GREY)
    y = para(d, lx, y + 8, lw,
             "Iran's Revolutionary Guards attacked two U.S. bases in Bahrain "
             "— Sheikh Isa air base and the Juffair facility, home of the "
             "Fifth Fleet. Bahrain said its defences intercepted the strikes; "
             "a civilian site caught fire. Kuwait repelled drones aimed at "
             "Ali Al Salem air base.", F_BODY, max_lines=4)
    draw_gulf_map(d, lx, 444, lw, 56)

    # ---- Ukraine (right column) ----
    rx, rw = 696, 300
    vrule(d, 680, 182, 492)
    y = kicker(d, rx, 182, "UKRAINE")
    y = headline(d, rx, y, rw, "BRIDGES BECOME THE BATTLEFIELD", F_HEAD2)
    y = para(d, rx, y + 8, rw,
             "Ukraine's strikes collapsed the Kerch Bridge road span to "
             "Crimea. Russia hit back with 80-plus missiles and 400 drones: "
             "three Kyiv bridges hit, 2 killed, 60 wounded in Kryvyi Rih.",
             F_BODY, max_lines=6)
    draw_bridge(d, rx, 436, rw, 64)
    hrule(d, 28, 508, W - 28, 2)

    # ---- Row 2: Mexico | Peru ----
    y = kicker(d, 28, 522, "MEXICO")
    y = headline(d, 28, y, 452, "FBI FUGITIVE 'EL CHAPO ISIDRO' CAPTURED", F_HEAD2)
    para(d, 28, y + 6, 452,
         "Mexican special forces seized cartel boss Fausto Isidro Meza Flores "
         "in Guasave, Sinaloa. Four soldiers and seven gunmen were killed; "
         "cartel roadblocks and burning trucks followed.",
         F_BODY, max_lines=4)

    vrule(d, 508, 522, 700)
    y = kicker(d, 524, 522, "PERU  —  EARTHQUAKE")
    y = headline(d, 524, y, 472, "MAGNITUDE 6.9 SHAKES THE ANDES", F_HEAD2)
    para(d, 524, y + 6, 472,
         "A deep quake struck near Junin on Friday evening, felt in Lima, "
         "where residents rushed into the streets. No casualties or damage "
         "were immediately reported.",
         F_BODY, max_lines=4)
    hrule(d, 28, 716, W - 28, 2)

    # ---- Row 3: COP31 | India | Sport ----
    y = kicker(d, 28, 724, "CLIMATE  —  COP31")
    y = headline(d, 28, y, 312, "CLIMATE TALKS RUN INTO OVERTIME", F_HEAD3)
    para(d, 28, y + 6, 312,
         "Nearly 200 nations in Antalya stayed deadlocked over naming fossil "
         "fuels; finance for poorer countries was unresolved too.",
         F_BODY, max_lines=4)

    vrule(d, 356, 724, 916)
    y = kicker(d, 372, 724, "INDIA")
    y = headline(d, 372, y, 288, "MODI OPENS NITISH SETU", F_HEAD3)
    para(d, 372, y + 6, 288,
         "A 19.7 km six-lane bridge over the Ganga links Patna and Vaishali "
         "in Bihar, at about \u20b94,280 crore.",
         F_BODY, max_lines=4)

    vrule(d, 676, 724, 916)
    y = kicker(d, 692, 724, "SPORT")
    y = headline(d, 692, y, 304, "ENGLAND ROUT THE ALL BLACKS", F_HEAD3)
    para(d, 692, y + 6, 304,
         "Five tries at Twickenham in a record 37–12 win over New Zealand — "
         "England's biggest margin ever.",
         F_BODY, max_lines=4)

    # ---- Also today strip + footer ----
    hrule(d, 28, 928, W - 28, 2)
    d.text((28, 940), "ALSO TODAY", font=F_KICK, fill=RED)
    para(d, 168, 940, W - 28 - 168,
         "Estonia to shut all road crossings with Russia from 1 December, "
         "citing sabotage plots.  •  A tanker was hit off Oman; Iran blamed "
         "a naval mine in the Strait of Hormuz.",
         F_BODY, max_lines=2)
    hrule(d, 28, 986, W - 28, 1)
    d.text((28, 994), "Sources: Reuters, AP, BBC, USGS — checked 22 November 2026.",
           font=F_TINY, fill=GREY)
    d.text((W - 28, 994), "THE WORLD IN ONE PAGE", font=F_TINY, fill=GREY, anchor="ra")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
