#!/usr/bin/env python3
"""The World in One Day — Tuesday, 24 November 2026.

Draws a 1024x1024 newspaper front page summarising 24 November 2026 world
news in one image: 40 stories from 6 regions. Deterministic: no network,
no randomness, no timestamps. Two runs produce byte-identical PNGs.

Usage: python3 generate.py [output.png]
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (30, 32, 46)
NAVY = (18, 38, 74)
RED = (158, 32, 32)
GOLD = (176, 124, 32)
TEAL = (18, 110, 105)
GREY = (96, 90, 78)
RULE = (150, 138, 112)
LIGHT = (233, 226, 210)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = "LiberationSerif-Bold.ttf"
SERIF = "LiberationSerif-Regular.ttf"
SERIF_I = "LiberationSerif-Italic.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS = "LiberationSans-Regular.ttf"
SANS_I = "LiberationSans-Italic.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text, truncating with an ellipsis to max_lines lines."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_w:
        lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else ""
    lines[-1] = (lines[-1] + " ...").strip()
    return lines


def text_block(draw, x, y, lines, fnt, fill, spacing, align="left", width=None):
    """Draw lines of text; returns y just below the last line."""
    for line in lines:
        if align == "center" and width is not None:
            lx = x + (width - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += spacing
    return y


def rule(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def section_header(draw, x, y, w, label, color=NAVY):
    fnt = font(SANS_B, 14)
    draw.text((x, y), label, font=fnt, fill=color)
    rule(draw, x, x + w, y + 19, fill=color, width=2)
    return y + 24


# ---------------------------------------------------------------- scenes
def scene_chip(draw, x, y, w, h):
    """A processor chip with circuit traces and a rising market line."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 231, 214), outline=RULE)
    cx, cy = x + w // 2, y + h // 2 + 4
    s = 44
    # pins
    for i in range(5):
        px = cx - s // 2 + 6 + i * 8
        draw.line([(px, cy - s // 2 - 8), (px, cy - s // 2)], fill=GOLD, width=2)
        draw.line([(px, cy + s // 2), (px, cy + s // 2 + 8)], fill=GOLD, width=2)
        py = cy - s // 2 + 6 + i * 8
        draw.line([(cx - s // 2 - 8, py), (cx - s // 2, py)], fill=GOLD, width=2)
        draw.line([(cx + s // 2, py), (cx + s // 2 + 8, py)], fill=GOLD, width=2)
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                   fill=NAVY, outline=GOLD, width=2)
    draw.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=GOLD)
    draw.text((cx - 7, cy - 7), "AI", font=font(SANS_B, 12), fill=NAVY)
    # rising line chart
    pts = [(x + 14, y + h - 22), (x + 34, y + h - 34), (x + 54, y + h - 30),
           (x + 74, y + h - 44), (x + 94, y + h - 40), (x + 114, y + h - 56)]
    draw.line(pts, fill=TEAL, width=3)
    draw.polygon([(x + 114, y + h - 56), (x + 106, y + h - 52),
                  (x + 114, y + h - 46)], fill=TEAL)
    draw.text((x + w - 52, y + 8), "+6% +9%", font=font(SANS_B, 12), fill=TEAL)


def scene_scales(draw, x, y, w, h):
    """Scales of justice over a court bench line."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 231, 214), outline=RULE)
    cx, cy = x + w // 2, y + h // 2 + 6
    # pillar and beam
    draw.line([(cx, cy - 34), (cx, cy + 26)], fill=NAVY, width=4)
    draw.line([(cx - 52, cy - 30), (cx + 52, cy - 30)], fill=NAVY, width=4)
    draw.polygon([(cx - 6, cy - 40), (cx + 6, cy - 40), (cx, cy - 30)], fill=GOLD)
    # left pan
    draw.line([(cx - 52, cy - 30), (cx - 52, cy - 8)], fill=NAVY, width=2)
    draw.line([(cx - 66, cy - 8), (cx - 52, cy - 30)], fill=NAVY, width=2)
    draw.line([(cx - 38, cy - 8), (cx - 52, cy - 30)], fill=NAVY, width=2)
    draw.arc([cx - 66, cy - 14, cx - 38, cy + 6], 0, 180, fill=NAVY, width=3)
    # right pan
    draw.line([(cx + 52, cy - 30), (cx + 52, cy - 8)], fill=NAVY, width=2)
    draw.line([(cx + 38, cy - 8), (cx + 52, cy - 30)], fill=NAVY, width=2)
    draw.line([(cx + 66, cy - 8), (cx + 52, cy - 30)], fill=NAVY, width=2)
    draw.arc([cx + 38, cy - 14, cx + 66, cy + 6], 0, 180, fill=NAVY, width=3)
    # base
    draw.line([(cx - 34, cy + 26), (cx + 34, cy + 26)], fill=NAVY, width=4)
    draw.text((x + 10, y + h - 14), "ICJ  ·  14 NATIONS", font=font(SANS_B, 11), fill=RED)


def scene_globe(draw, x, y, w, h):
    """A cracked globe: the climate talks broke apart."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 231, 214), outline=RULE)
    cx, cy = x + w // 2, y + h // 2 + 2
    r = 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 228, 226),
                 outline=TEAL, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=TEAL, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=TEAL, width=2)
    draw.arc([cx - r, cy - 18, cx + r, cy + 18], 200, 340, fill=TEAL, width=2)
    # crack zig-zag
    crack = [(cx - 8, cy - r + 2), (cx + 2, cy - 16), (cx - 6, cy - 2),
             (cx + 6, cy + 12), (cx - 2, cy + 24), (cx + 8, cy + r - 2)]
    draw.line(crack, fill=RED, width=3)
    # broken shard
    draw.polygon([(cx + 22, cy - 30), (cx + 34, cy - 22), (cx + 26, cy - 12)],
                 fill=GOLD, outline=RED)
    draw.text((x + 10, y + 8), "COP31  ·  NO DEAL", font=font(SANS_B, 11), fill=RED)


# ---------------------------------------------------------------- content
LEADS = [
    ("NVIDIA CHIEF RETURNS AS TRUMP STEPS IN",
     "Jensen Huang is reinstated as chief executive after presidential "
     "intervention; Asian chip stocks soar — Seoul up 6%, Nikkei 3.9%, "
     "Taiwan 9%.",
     scene_chip),
    ("WORLD BACKS ROHINGYA RULING",
     "Fourteen nations affirm the court's genocide ruling against Myanmar; "
     "Britain sanctions its generals as Malaysia prepares to return "
     "Rohingya refugees.",
     scene_scales),
    ("CLIMATE TALKS COLLAPSE IN ANTALYA",
     "COP31 ends without a deal after some 50 hours of overtime; more "
     "than 90 nations reject a draft that never once named fossil fuels.",
     scene_globe),
]

FEATURED = [
    ("SEA DRONES SINK RUSSIAN WARSHIP OFF LIBYA",
     "Ukrainian drones sink the corvette Merkury near Benghazi; Tripoli demands an explanation from Kyiv."),
    ("MEDVEDEV WARNS OF PREVENTIVE NUCLEAR STRIKE",
     "Moscow's warning comes as reports of a Russian nuclear satellite push NATO to vow to defend space."),
    ("RUSSIA WARNS ESTONIA OF \u201cOPEN WAR\u201d",
     "Tallinn will shut its border with Russia for six months from 1 December as tensions spike."),
    ("14 KILLED AS RUSSIAN STRIKES HIT UKRAINE",
     "A Zaporizhzhia attack kills two and wounds 22; a strike on Dymer kills 11."),
    ("GAZA WAR ERASES 77 YEARS OF PROGRESS, UN SAYS",
     "Israeli strikes kill at least three, including an UNRWA worker; Oxfam calls Gaza a \u201ctoxic land\u201d."),
    ("US LOSES MEASLES-FREE STATUS",
     "America loses elimination status after 25 years; Pennsylvania records a ninth measles death."),
    ("SANOFI TO BUY INSMED FOR $41 BILLION",
     "The French drugmaker agrees its largest deal in years, a $41bn takeover of the US biotech."),
    ("US STATES SUE MUSK OVER GROK IMAGES",
     "Oregon and Virginia sue SpaceX over sexualised images generated by the Grok chatbot."),
    ("SOLOMONS TO END CHINA SECURITY PACT",
     "The Solomon Islands will scrap its pact with Beijing and replace it with an Australian treaty."),
    ("NETANYAHU URGES NEW STRIKES ON IRAN",
     "Israel's leader presses Trump to resume attacks; Iran vows to counter any Hormuz blockade as tankers are hit by mines."),
]

NUMBERED = [
    "Nepal: 5.6-magnitude quake near China border.",
    "Houthis: Saudi airstrike kills 17 in Hodeida, Yemen.",
    "DR Congo: Ebola teams trapped by fighting.",
    "South Sudan: 21 killed in Tonj East camp attack.",
    "South Sudan: 50,000+ sit secondary school exams.",
    "Colombia: car bomb wrecks Villavicencio buildings.",
    "Mexico to try \u201cEl Chapo Isidro\u201d despite US request.",
    "El Salvador names 3 troops killed in Haiti mission.",
    "Argentina asks tribunal to halt Falklands oil work.",
    "China: first foreign astronaut joins Tiangong.",
    "Astronomers find most distant glowing black hole.",
    "FDA approves first limb-girdle dystrophy drug.",
    "UN: 47,000 women killed by partners in 2025.",
    "WFP: wars put food aid for 7.3m more at risk.",
    "Armenia drops Karabakh from draft constitution.",
    "EU proposes 22nd Russia sanctions package.",
    "Trump to meet NATO chief Rutte in Florida.",
    "Hanoi explosion kills six.",
    "UAE bus-truck crash kills 11 in Ras Al Khaimah.",
    "Nigeria: Borno school enrolment nearly doubles.",
    "Egypt and Iraq scrap mutual entry visas.",
    "Indonesia and the Mecca pact: a new security turn.",
    "GTA 6 sets record: $3.8bn in first-day sales.",
    "North Korea threatens to shut Swiss office.",
    "China navy to unveil JL-15 trainer at Zhuhai.",
    "Arm extends CEO Rene Haas' tenure to 2033.",
    "US blacklists Megaspeed amid Nvidia probe.",
]

DATE_CHECK = [
    "COP31 collapse was decided late 23 Nov — 24 Nov is the fallout.",
    "ICJ Rohingya ruling was 19 Nov — 24 Nov brings affirmations and sanctions.",
    "Merkury sinking happened 23 Nov, first reported 24 Nov.",
    "Russian missiles in Poland: 20 Nov, not today.",
    "Democrats' midterm majorities: decided 3 Nov, not 24 Nov news.",
]

# Continents as ellipses in map coordinates (u right, v down), map area 972x92.
CONTINENTS = [
    (140, 26, 78, 22),   # North America
    (248, 58, 34, 18),   # South America
    (468, 18, 30, 13),   # Europe
    (486, 52, 36, 24),   # Africa
    (655, 24, 118, 24),  # Asia
    (755, 58, 40, 8),    # SE Asia islands
    (825, 68, 38, 12),   # Australia
]
# Gold markers: (u, v) story locations.
MARKERS = [(790, 22), (505, 26), (495, 40), (500, 16), (520, 38)]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 231, 214), outline=RULE)
    step = 5
    for gy in range(y + 5, y + h - 18, step):
        for gx in range(x + 5, x + w - 4, step):
            u, v = gx - x, gy - y
            inside = False
            for (cu, cv, ru, rv) in CONTINENTS:
                if ((u - cu) / ru) ** 2 + ((v - cv) / rv) ** 2 <= 1.0:
                    inside = True
                    break
            if inside:
                draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=NAVY)
    for (mu, mv) in MARKERS:
        mx, my = x + mu, y + mv
        draw.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=GOLD, outline=RED)
    draw.text((x + 8, y + h - 13), "Markers: Seoul · Antalya · Benghazi · Kyiv · Gaza",
              font=font(SANS_I, 10), fill=GREY)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    MX = 26
    CW = W - 2 * MX  # 972

    # ---- masthead ----
    y = 16
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 48)
    draw.text(((W - draw.textlength(title, font=tf)) / 2, y), title,
              font=tf, fill=NAVY)
    y += 56
    sub = "Tuesday, 24 November 2026"
    sf = font(SERIF_I, 18)
    draw.text(((W - draw.textlength(sub, font=sf)) / 2, y), sub,
              font=sf, fill=INK)
    y += 28
    rule(draw, MX, W - MX, y, fill=NAVY, width=2)
    y += 5
    rule(draw, MX, W - MX, y, fill=NAVY, width=1)
    y += 9

    # ---- stats strip ----
    stats = "40 STORIES  ·  6 REGIONS"
    stf = font(SANS_B, 13)
    draw.text(((W - draw.textlength(stats, font=stf)) / 2, y), stats,
              font=stf, fill=RED)
    y += 18
    regions = ("Europe 8   ·   Middle East 6   ·   Asia-Pacific 8   ·   "
               "Americas 6   ·   Africa 5   ·   Science / Tech / Business 7")
    rf = font(SANS, 12)
    draw.text(((W - draw.textlength(regions, font=rf)) / 2, y), regions,
              font=rf, fill=GREY)
    y += 20
    rule(draw, MX, W - MX, y)
    y += 7

    # ---- lead stories ----
    y = section_header(draw, MX, y, CW, "LEAD STORIES")
    col_w = (CW - 2 * 12) // 3  # 316
    lead_top = y
    for i, (headline, body, scene) in enumerate(LEADS):
        cx = MX + i * (col_w + 12)
        scene(draw, cx, lead_top, col_w, 76)
        hy = lead_top + 82
        hl = fit_lines(draw, headline, font(SERIF_B, 18), col_w, 2)
        hy = text_block(draw, cx, hy, hl, font(SERIF_B, 18), NAVY, 20)
        bl = fit_lines(draw, body, font(SERIF, 13), col_w, 3)
        text_block(draw, cx, hy + 3, bl, font(SERIF, 13), INK, 15)
    y = lead_top + 82 + 2 * 20 + 3 + 3 * 15 + 6
    rule(draw, MX, W - MX, y)
    y += 7

    # ---- featured stories ----
    y = section_header(draw, MX, y, CW, "THE DAY IN BRIEF — TEN STORIES")
    fcol_w = (CW - 16) // 2  # 478
    row_h = 46
    for i, (headline, body) in enumerate(FEATURED):
        r, c = divmod(i, 2)
        fx = MX + c * (fcol_w + 16)
        fy = y + r * row_h
        hl = fit_lines(draw, headline, font(SANS_B, 13), fcol_w, 1)
        text_block(draw, fx, fy, hl, font(SANS_B, 13), NAVY, 16)
        bl = fit_lines(draw, body, font(SANS, 12), fcol_w, 2)
        text_block(draw, fx, fy + 16, bl, font(SANS, 12), INK, 13)
    y += 5 * row_h + 4
    rule(draw, MX, W - MX, y)
    y += 7

    # ---- world dot map ----
    y = section_header(draw, MX, y, CW, "THE WORLD AT A GLANCE")
    draw_map(draw, MX, y, CW, 76)
    y += 76 + 7
    rule(draw, MX, W - MX, y)
    y += 7

    # ---- numbered list ----
    y = section_header(draw, MX, y, CW, "AND 27 MORE STORIES")
    ncol_w = (CW - 2 * 14) // 3  # 314
    nf = font(SANS, 12)
    for i, item in enumerate(NUMBERED):
        c, r = divmod(i, 9)
        nx = MX + c * (ncol_w + 14)
        ny = y + r * 14
        line = "%d. %s" % (i + 14, item)
        line = fit_lines(draw, line, nf, ncol_w, 1)[0]
        draw.text((nx, ny), line, font=nf, fill=INK)
    y += 9 * 14 + 5
    assert y <= 900, "numbered list ends too low: %d" % y

    # ---- date check box ----
    box_h = H - 18 - y
    draw.rectangle([MX, y, W - MX, y + box_h], fill=(233, 226, 210),
                   outline=RED, width=2)
    by = y + 7
    draw.text((MX + 12, by), "DATE CHECK — WHAT IS NOT 24 NOVEMBER NEWS",
              font=font(SANS_B, 12), fill=RED)
    by += 18
    df = font(SANS, 11)
    for line in DATE_CHECK:
        draw.text((MX + 12, by), "•  " + line, font=df, fill=INK)
        by += 13

    # footer
    draw.text((MX, H - 15), "Compiled from wires reporting Tuesday 24 November 2026.",
              font=font(SANS_I, 9), fill=GREY)
    img.save(out, format="PNG")


if __name__ == "__main__":
    main()
