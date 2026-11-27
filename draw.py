#!/usr/bin/env python3
"""Draw the front page for Thursday 26 November 2026.

Renders a 1024x1024 newspaper front page (masthead with the date, six
story cards in a 2x3 grid, an "ALSO TODAY" strip and a footer) to
entry.png in this directory. Deterministic: no timestamps, no random
input, fixed fonts and fixed layout, so repeated runs are byte-identical.

Run: python3 draw.py
Requires: Pillow (local build tool only; the entry program is main.ts).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (24, 24, 24)
GREY = (92, 92, 88)
NAVY = (26, 42, 74)
GOLD = (233, 196, 88)
RED_RULE = (178, 34, 34)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_flame(d, x, y, s):
    """Simple flame icon, red/orange."""
    d.polygon([(x + s * 0.5, y), (x + s * 0.95, y + s * 0.55),
               (x + s * 0.8, y + s), (x + s * 0.2, y + s),
               (x + s * 0.05, y + s * 0.55)], fill=(178, 34, 34))
    d.ellipse([x + s * 0.32, y + s * 0.55, x + s * 0.68, y + s * 0.92],
              fill=(233, 196, 88))


def draw_star(d, x, y, s):
    """Five-point star, dark blue."""
    import math
    pts = []
    for i in range(10):
        r = s * 0.5 if i % 2 == 0 else s * 0.2
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((x + s * 0.5 + r * math.cos(a),
                    y + s * 0.5 + r * math.sin(a)))
    d.polygon(pts, fill=(26, 42, 74))


def draw_laser(d, x, y, s):
    """Laser beam: triangle + target rings, purple."""
    d.polygon([(x, y + s * 0.5), (x + s, y + s * 0.15),
               (x + s, y + s * 0.85)], fill=(90, 40, 140))
    d.ellipse([x + s * 0.55, y + s * 0.3, x + s * 0.95, y + s * 0.7],
              outline=(90, 40, 140), width=3)
    d.ellipse([x + s * 0.68, y + s * 0.43, x + s * 0.82, y + s * 0.57],
              fill=(90, 40, 140))


def draw_ballot(d, x, y, s):
    """Ballot box with a slip, teal."""
    d.rectangle([x + s * 0.08, y + s * 0.35, x + s * 0.92, y + s * 0.95],
                fill=(14, 120, 110))
    d.rectangle([x + s * 0.02, y + s * 0.25, x + s * 0.98, y + s * 0.4],
                fill=(10, 90, 82))
    d.rectangle([x + s * 0.35, y + s * 0.02, x + s * 0.65, y + s * 0.3],
                fill=(255, 255, 255))
    d.line([x + s * 0.42, y + s * 0.14, x + s * 0.58, y + s * 0.14],
           fill=(14, 120, 110), width=3)


def draw_storm(d, x, y, s):
    """Storm cloud with rain, dark green-grey."""
    d.ellipse([x + s * 0.05, y + s * 0.15, x + s * 0.55, y + s * 0.6],
              fill=(60, 90, 70))
    d.ellipse([x + s * 0.4, y + s * 0.05, x + s * 0.9, y + s * 0.55],
              fill=(60, 90, 70))
    d.rectangle([x + s * 0.1, y + s * 0.45, x + s * 0.85, y + s * 0.6],
                fill=(60, 90, 70))
    for i, rx in enumerate((0.2, 0.45, 0.7)):
        # Short rain strokes that stay clear of the card's footer rule.
        d.line([x + s * rx, y + s * 0.68, x + s * (rx - 0.05), y + s * 0.88],
               fill=(40, 110, 160), width=4)


def draw_satellite(d, x, y, s):
    """Satellite with two panels, maroon."""
    d.rectangle([x + s * 0.38, y + s * 0.35, x + s * 0.62, y + s * 0.65],
                fill=(122, 31, 52))
    d.polygon([(x + s * 0.5, y + s * 0.3), (x + s * 0.62, y + s * 0.5),
               (x + s * 0.5, y + s * 0.7), (x + s * 0.38, y + s * 0.5)],
              fill=(233, 196, 88))
    d.rectangle([x, y + s * 0.42, x + s * 0.32, y + s * 0.58],
                fill=(122, 31, 52))
    d.rectangle([x + s * 0.68, y + s * 0.42, x + s, y + s * 0.58],
                fill=(122, 31, 52))


STORIES = [
    ("MIDDLE EAST", (178, 34, 34), "Houthis strike Saudi Red Sea ports",
     "Jizan port hit; drone downed near Jeddah, missiles stopped.",
     draw_flame),
    ("UNITED STATES", (26, 42, 74), "Trump: victory over Iran is \u201cat hand\u201d",
     "Thanksgiving call to troops; Tehran warned of a \u201cvery traumatic\u201d outcome if no deal.",
     draw_star),
    ("UKRAINE", (90, 40, 140), "Kyiv downs drone with a laser weapon",
     "Ukraine says it shot down a Russian jet drone with a laser system, a first.",
     draw_laser),
    ("NEW ZEALAND", (14, 120, 110), "Coalition one seat short of a majority",
     "Final count leaves Luxon needing centrist Opportunity to govern.",
     draw_ballot),
    ("WEATHER", (40, 90, 70), "Thanksgiving storm floods US, delays flights",
     "Heavy rain and floods hit the holiday weekend; airports back up.",
     draw_storm),
    ("SPACE", (122, 31, 52), "Million-satellite SpaceX plan approved",
     "Musk\u2019s plan to put a million data satellites in orbit wins approval.",
     draw_satellite),
]

ALSO = ("Depardieu to stand trial over 2018 rape claim  \u2022  "
        "Thai\u2013Cambodia fighting paused after truce  \u2022  "
        "SoftBank to invest $2bn in Intel")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    f_mast = font(SERIF_B, 40)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 14), t,
           font=f_mast, fill=(255, 255, 255))
    f_date = font(SANS_B, 44)
    t = "THURSDAY, 26 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=f_date)) / 2, 62), t,
           font=f_date, fill=GOLD)
    f_sub = font(SANS, 21)
    t = "Six stories that defined the day  \u2022  World news in one image"
    d.text(((W - d.textlength(t, font=f_sub)) / 2, 114), t,
           font=f_sub, fill=(220, 220, 220))
    d.rectangle([0, 148, W, 154], fill=RED_RULE)

    # Story cards, 2 x 3
    margin, gutter = 24, 16
    cw = (W - 2 * margin - gutter) // 2
    ch = 232
    top0 = 168
    row_gap = 14
    f_cat = font(SANS_B, 22)
    f_head = font(SERIF_B, 33)
    f_sum = font(SANS, 19)
    f_foot = font(SANS_B, 16)

    for i, (cat, color, head, summ, icon) in enumerate(STORIES):
        x = margin + (i % 2) * (cw + gutter)
        y = top0 + (i // 2) * (ch + row_gap)
        # card body
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=8,
                            fill=(255, 255, 255), outline=(170, 160, 140),
                            width=2)
        # category bar
        d.rounded_rectangle([x, y, x + cw, y + 36], radius=8, fill=color)
        d.rectangle([x, y + 20, x + cw, y + 36], fill=color)
        d.text((x + 14, y + 6), cat, font=f_cat, fill=(255, 255, 255))
        # headline, up to 2 lines
        lines = wrap(d, head, f_head, cw - 28)[:2]
        hy = y + 48
        for ln in lines:
            d.text((x + 14, hy), ln, font=f_head, fill=INK)
            hy += 40
        # summary, up to 2 lines
        slines = wrap(d, summ, f_sum, cw - 130)[:2]
        sy = y + 48 + 2 * 40 + 6
        for ln in slines:
            d.text((x + 14, sy), ln, font=f_sum, fill=GREY)
            sy += 25
        # icon bottom-right
        icon(d, x + cw - 78, y + ch - 78, 62)
        # footer rule + date
        d.line([x + 14, y + ch - 30, x + cw - 14, y + ch - 30],
               fill=(200, 190, 170), width=1)
        d.text((x + 14, y + ch - 26), "26 NOV 2026", font=f_foot, fill=color)

    # Also today strip
    ay = top0 + 3 * ch + 2 * row_gap + 12
    f_also_h = font(SANS_B, 22)
    d.text((margin, ay), "ALSO TODAY:", font=f_also_h, fill=INK)
    f_also = font(SANS, 19)
    lines = wrap(d, ALSO, f_also, W - 2 * margin)
    ly = ay + 30
    for ln in lines:
        d.text((margin, ly), ln, font=f_also, fill=INK)
        ly += 25

    # Footer
    f_foot2 = font(SANS, 17)
    t = "26 November 2026 \u2014 the world\u2019s news in one image"
    d.text(((W - d.textlength(t, font=f_foot2)) / 2, H - 30), t,
           font=f_foot2, fill=GREY)

    img.save(os.path.join(HERE, "entry.png"), "PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
