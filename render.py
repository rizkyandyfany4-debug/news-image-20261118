#!/usr/bin/env python3
"""Draw the front page of 18 November 2026 as a 1024x1024 PNG.

Stories (all reported on Wednesday 18 November 2026, wire-first):
  LEAD  Trump, Xi and Putin meet in Shenzhen (Reuters / BBC / AP)
  GULF  US strikes Qeshm Island; Iran hits US sites in Kuwait and Bahrain
        (Reuters / BBC)
  US    Peltola wins Alaska; Democrats take a 56-44 Senate majority (AP / BBC)
  TECH  Nvidia posts record results, revenue more than doubled (Reuters)
  ALSO  Jeffries nominated for Speaker (BBC); Israeli ground operation in
        Gaza (BBC); EU EUR45bn Ukraine loan (Reuters); Waymo pulls
        driverless cars from US freeways (BBC); Cyclone Akvan nears India (IMD)

Deterministic: fixed fonts, fixed layout, no timestamps, no randomness.
Running this script any number of times produces byte-identical output.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 40
PAPER = (248, 244, 234)
INK = (26, 26, 26)
NAVY = (31, 58, 95)
RED = (176, 42, 48)
GRAY = (107, 107, 107)
RULE = (201, 194, 174)
SKY = (214, 228, 240)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    """Draw lines starting at (x, y); return the y below the last line."""
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, y, weight=2):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=weight)


def skyline(draw, x0, y0, x1, y1):
    """Simple Shenzhen skyline silhouette with a sun and three flags."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    base = y1
    heights = [40, 62, 48, 74, 56, 44, 66, 52, 78, 60, 46, 70, 54, 42]
    n = len(heights)
    bw = (x1 - x0) / n
    for i, h in enumerate(heights):
        bx = x0 + i * bw
        draw.rectangle([bx + 3, base - h, bx + bw - 3, base], fill=NAVY)
    # sun drawn after the buildings so it sits in front of them
    draw.ellipse([x1 - 118, y0 + 10, x1 - 62, y0 + 66], fill=(240, 196, 90))
    # three flag poles: US, China, Russia
    poles = [
        ([(176, 42, 48), (255, 255, 255), (176, 42, 48), (255, 255, 255)], None),
        ([(222, 41, 16)], None),
        ([(255, 255, 255), (0, 57, 166), (213, 0, 50)], None),
    ]
    fx = x0 + 30
    for stripes, _ in poles:
        px = fx
        draw.line([(px, y0 + 18), (px, y0 + 62)], fill=INK, width=3)
        fh = 34 / len(stripes)
        for j, col in enumerate(stripes):
            draw.rectangle(
                [px, y0 + 18 + j * fh, px + 46, y0 + 18 + (j + 1) * fh],
                fill=col, outline=INK, width=1,
            )
        fx += 92


def ship_icon(draw, x0, y0, x1, y1):
    """Simple tanker on waves."""
    mid = (y0 + y1) // 2
    draw.polygon(
        [(x0 + 10, mid), (x1 - 10, mid), (x1 - 26, mid + 22),
         (x0 + 26, mid + 22)], fill=NAVY,
    )
    draw.rectangle([x0 + 34, mid - 22, x0 + 62, mid], fill=RED)
    draw.rectangle([x0 + 70, mid - 14, x0 + 92, mid], fill=INK)
    for k, wy in enumerate((y1 - 8, y1 - 2)):
        for sx in range(x0, x1, 26):
            draw.arc([sx, wy, sx + 24, wy + 10], 0, 180, fill=NAVY, width=2)


def ballot_icon(draw, x0, y0, x1, y1):
    """Simple ballot box with a tick."""
    draw.rectangle([x0 + 18, y0 + 26, x1 - 18, y1 - 6], fill=NAVY)
    draw.rectangle([x0 + 34, y0 + 18, x1 - 34, y0 + 30], fill=INK)
    draw.line([(x0 + 36, y0 + 58), (x0 + 52, y0 + 74),
               (x0 + 84, y0 + 34)], fill=(255, 255, 255), width=5)


def bar_chart(draw, x0, y0, x1, y1):
    """Four rising bars for the earnings story."""
    vals = [22, 38, 54, 76]
    n = len(vals)
    bw = (x1 - x0) / n
    for i, v in enumerate(vals):
        bx = x0 + i * bw + 8
        top = y1 - v
        col = RED if i == n - 1 else NAVY
        draw.rectangle([bx, top, bx + bw - 16, y1], fill=col)
    draw.line([(x0, y1), (x1, y1)], fill=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 20

    # Masthead
    f_mast = font(SANS_B, 26)
    mast = " ".join("THE WORLD IN ONE IMAGE")
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, y), mast,
           font=f_mast, fill=NAVY)
    y += 36

    # Date line
    f_date = font(SERIF_B, 46)
    date = "WEDNESDAY 18 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, y), date,
           font=f_date, fill=INK)
    y += 56

    # Double rule
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    d.line([(MARGIN, y + 5), (W - MARGIN, y + 5)], fill=INK, width=1)
    y += 16

    # Kicker
    f_kick = font(SANS_B, 17)
    kick = "THE DAY IN BRIEF  ·  SHENZHEN  ·  THE GULF  ·  WASHINGTON"
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, y), kick,
           font=f_kick, fill=RED)
    y += 24

    # Lead headline
    f_head = font(SERIF_B, 41)
    head = "TRUMP, XI AND PUTIN\nMEET IN SHENZHEN"
    y = draw_lines(d, head.split("\n"), f_head, MARGIN, y, INK, 47)
    y += 4

    # Lead subhead
    f_sub = font(SANS, 21)
    sub = ("Xi greets Trump on the tarmac a day before the first-ever "
           "three-way summit")
    y = draw_lines(d, wrap(d, sub, f_sub, W - 2 * MARGIN), f_sub,
                   MARGIN, y, NAVY, 25)
    y += 8

    # Lead illustration
    skyline(d, MARGIN, y, W - MARGIN, y + 92)
    y += 92 + 8

    # Lead body
    f_body = font(SERIF, 19)
    lead = ("Chinese leader Xi Jinping and Russian President Vladimir Putin "
            "opened talks in Shenzhen on Wednesday, a day before a "
            "first-ever trilateral summit with US President Donald Trump at "
            "the APEC meeting. Xi broke protocol to greet Trump at the foot "
            "of Air Force One.")
    y = draw_lines(d, wrap(d, lead, f_body, W - 2 * MARGIN), f_body,
                   MARGIN, y, INK, 23)
    y += 10
    hrule(d, y)
    y += 10

    # Two-column row: Gulf (left) and Senate (right)
    col_w = (W - 2 * MARGIN - 36) // 2
    col_top = y
    f_col_h = font(SANS_B, 24)
    f_col_b = font(SERIF, 18)

    # left column
    x = MARGIN
    ship_icon(d, x, col_top, x + 130, col_top + 62)
    d.text((x + 142, col_top + 16), "GULF ON EDGE", font=f_col_h, fill=RED)
    by = col_top + 76
    gulf = ("US fighter jets struck an Iranian missile site on Qeshm Island "
            "in the Strait of Hormuz. Iran said it hit US drone and missile "
            "sites in Kuwait and Bahrain; Kuwait says it repelled the "
            "attack, and a UAE ship was hit in the strait, leaving one crew "
            "member missing.")
    by = draw_lines(d, wrap(d, gulf, f_col_b, col_w), f_col_b, x, by, INK, 22)

    # right column
    x = MARGIN + col_w + 36
    ballot_icon(d, x, col_top, x + 130, col_top + 62)
    d.text((x + 142, col_top + 16), "DEMOCRATS TAKE", font=f_col_h, fill=NAVY)
    d.text((x + 142, col_top + 44), "THE SENATE", font=f_col_h, fill=NAVY)
    by2 = col_top + 76
    senate = ("Mary Peltola beat Republican Dan Sullivan in Alaska, the last "
             "Senate race of the midterms, giving Democrats a 56-44 "
             "majority \u2014 their largest since 2009, the Associated "
             "Press reports.")
    by2 = draw_lines(d, wrap(d, senate, f_col_b, col_w), f_col_b, x, by2,
                     INK, 22)

    y = max(by, by2) + 10
    hrule(d, y)
    y += 10

    # Nvidia band
    f_nv_h = font(SANS_B, 24)
    d.text((MARGIN, y), "NVIDIA POSTS RECORD RESULTS", font=f_nv_h, fill=INK)
    bar_chart(d, W - MARGIN - 190, y + 2, W - MARGIN, y + 84)
    f_nv_b = font(SERIF, 18)
    nv = ("Revenue more than doubled to $115.8bn in its first report since "
          "Jensen Huang's exit, with data-centre sales leading; the "
          "chipmaker guided to about $130bn next quarter.")
    y = draw_lines(d, wrap(d, nv, f_nv_b, W - 2 * MARGIN - 210), f_nv_b,
                   MARGIN, y + 32, INK, 22)
    y += 8
    hrule(d, y)
    y += 10

    # ALSO strip
    f_also = font(SANS_B, 17)
    d.text((MARGIN, y), "ALSO", font=f_also, fill=RED)
    y += 22
    f_item = font(SANS, 17)
    items = [
        "Democrats nominate Hakeem Jeffries for Speaker \u2014 the first Black lawmaker to lead the House (BBC)",
        "Israeli ground operation in Gaza beyond the ceasefire line (BBC)",
        "EU proposes a \u20ac45bn loan to Ukraine, repaid only after Russian reparations (Reuters)",
        "Waymo pulls its driverless cars from US freeways (BBC)",
        "Cyclone Akvan strengthens in the Bay of Bengal, landfall due Friday (IMD)",
    ]
    for it in items:
        lines = wrap(d, "\u2022  " + it, f_item, W - 2 * MARGIN)
        y = draw_lines(d, lines, f_item, MARGIN, y, INK, 20)
    y += 6
    hrule(d, y)
    y += 8

    # Footer
    f_foot = font(SANS, 14)
    foot = ("Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 NYT \u00b7 Al Jazeera  "
            "\u2014  all events reported on 18 November 2026")
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, y), foot,
           font=f_foot, fill=GRAY)
    y += 22

    assert y <= H - 4, f"layout overflow: final y={y}"
    img.save("entry.png", format="PNG", optimize=False)
    print(f"wrote entry.png, final y={y}")


if __name__ == "__main__":
    main()
