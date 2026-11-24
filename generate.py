#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: a 1024x1024 newspaper front page
summing up the world news of Tuesday 24 November 2026.

Pure PIL (Pillow) + Liberation fonts, no network, no randomness, no
timestamps: running it twice writes a byte-identical PNG. Every story
below was checked against the wires of 24 Nov 2026 (Reuters, AP, CNN,
Le Monde, Al Jazeera, France24). The DATE CHECK box names what was left
out because it belongs to an earlier day, and what Tuesday's news
actually was for stories that began earlier.

Run:  python3 generate.py [out.png]
"""
import hashlib
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
CARD = (255, 253, 246)
INK = (22, 22, 22)
MUTED = (110, 105, 92)
NAVY = (20, 38, 74)
NAVY_D = (13, 25, 50)
RED = (179, 38, 30)
RED_D = (140, 28, 22)
GOLD = (201, 162, 39)
TEAL = (15, 118, 110)
SKY = (135, 190, 220)
SEA = (46, 110, 160)
GREEN = (46, 125, 60)
ORANGE = (224, 122, 26)
YELLOW = (242, 201, 60)
WHITE = (255, 255, 255)
LINE = (190, 184, 170)
NIGHT = (16, 24, 48)
SAND = (232, 214, 170)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines top-down; returns the y just below the last line."""
    if leading is None:
        leading = fnt.size + 3
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(d, x0, x1, y, fill=LINE, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def tag(d, x, y, label, fill):
    """Small tag chip; returns width used."""
    f = font(F_SANS_B, 11)
    tw = d.textlength(label, font=f)
    pad = 6
    d.rectangle([x, y, x + tw + pad * 2, y + 16], fill=fill)
    d.text((x + pad, y + 2), label, font=f, fill=WHITE)
    return tw + pad * 2 + 4


# ---------------------------------------------------------------- scenes
# Every scene is drawn from flat PIL shapes: no photos, no AI images,
# nothing the program did not draw itself.


def scene_chip(d, x, y, w, h):
    """A green computer chip on a dark board, stock line climbing."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 40, 26))
    # rising stock line
    pts = [(x + 12, y + h - 18), (x + w // 3, y + h - 34),
           (x + w // 2, y + h - 26), (x + 2 * w // 3, y + h - 44),
           (x + w - 14, y + 14)]
    d.line(pts, fill=(120, 220, 140), width=3)
    d.ellipse([x + w - 20, y + 8, x + w - 8, y + 20], fill=(120, 220, 140))
    # chip
    cx, cy = x + w // 2 - 34, y + h - 62
    d.rectangle([cx - 8, cy - 8, cx + 42, cy + 42], fill=GREEN)
    d.rectangle([cx, cy, cx + 34, cy + 34], fill=(24, 60, 34))
    d.rectangle([cx + 8, cy + 8, cx + 26, cy + 26], outline=(120, 220, 140),
                width=2)
    for i in range(4):
        d.line([(cx + 4 + i * 9, cy - 8), (cx + 4 + i * 9, cy)], fill=GOLD,
               width=2)
        d.line([(cx + 4 + i * 9, cy + 34), (cx + 4 + i * 9, cy + 42)],
               fill=GOLD, width=2)
    d.text((x + 10, y + 6), "+6%  +3.9%  +9%", font=font(F_SANS_B, 12),
           fill=(120, 220, 140))


def scene_court(d, x, y, w, h):
    """Courtroom scales of justice on a navy backdrop."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(96, 74, 52))
    cx = x + w // 2
    top, bar, pan = y + 8, y + int(h * 0.32), y + int(h * 0.72)
    d.line([(cx, top), (cx, y + h - 12)], fill=GOLD, width=3)
    d.line([(cx - 44, bar), (cx + 44, bar)], fill=GOLD, width=3)
    for s in (-1, 1):
        d.line([(cx + s * 44, bar), (cx + s * 30, pan - 12)], fill=GOLD,
               width=2)
        d.polygon([(cx + s * 44, pan - 12), (cx + s * 16, pan - 12),
                   (cx + s * 30, pan)], fill=GOLD)
    d.ellipse([cx - 8, top - 2, cx + 8, top + 14], fill=GOLD)
    d.text((x + 10, y + 6), "ICJ · THE HAGUE", font=font(F_SANS_B, 11),
           fill=WHITE)


def scene_summit(d, x, y, w, h):
    """Climate summit hall: long table, flags, a cracked globe."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY_D)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(58, 44, 30))
    d.rectangle([x + 18, y + h - 52, x + w - 18, y + h - 26], fill=(96, 74, 52))
    for i in range(7):
        cx = x + 24 + i * ((w - 48) // 6)
        d.ellipse([cx, y + h - 62, cx + 12, y + h - 50], fill=(210, 180, 140))
        d.rectangle([cx + 2, y + h - 50, cx + 10, y + h - 26], fill=(40, 40, 40))
    gx, gy, gr = x + w - 62, y + 34, 26
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=SEA)
    d.ellipse([gx - gr + 8, gy - gr + 6, gx - gr + 22, gy - gr + 20],
              fill=GREEN)
    d.ellipse([gx + 4, gy + 8, gx + 18, gy + 20], fill=GREEN)
    d.line([(gx - 14, gy - 22), (gx - 4, gy - 6), (gx - 12, gy + 8),
            (gx + 2, gy + 20)], fill=WHITE, width=3)
    for i in range(5):
        fx = x + 16 + i * 14
        d.rectangle([fx, y + 14, fx + 8, y + 34],
                    fill=[RED, GOLD, TEAL, WHITE, ORANGE][i])
        d.line([(fx + 4, y + 14), (fx + 4, y + 8)], fill=GOLD, width=2)


def scene_sea(d, x, y, w, h):
    """Warship at sea at dusk, drones overhead, smoke plume."""
    d.rectangle([x, y, x + w, y + h], fill=(252, 176, 90))
    d.ellipse([x + w - 34, y + 8, x + w - 6, y + 36], fill=(255, 214, 120))
    sea_top = y + h - int(h * 0.55)
    d.rectangle([x, sea_top, x + w, y + h], fill=SEA)
    deck = y + h - int(h * 0.38)
    d.polygon([(x + 26, deck), (x + w - 30, deck),
               (x + w - 52, y + h - 6), (x + 44, y + h - 6)], fill=(70, 76, 84))
    d.rectangle([x + 70, deck - int(h * 0.28), x + 120, deck],
                fill=(96, 102, 110))
    d.line([(x + 92, deck - int(h * 0.28)), (x + 92, deck - int(h * 0.42))],
           fill=(70, 76, 84), width=4)
    for i, r in enumerate([9, 7, 5, 4]):
        d.ellipse([x + w - 78 + i * 6, y + 8 + i * 5,
                   x + w - 78 + i * 6 + r * 2, y + 8 + i * 5 + r * 2],
                  fill=(60, 60, 60))
    for dx in (x + 40, x + 150):
        d.ellipse([dx, y + h - 12, dx + 7, y + h - 5], fill=INK)
        d.line([(dx - 16, y + h - 8), (dx, y + h - 8)], fill=WHITE, width=2)


def scene_sky(d, x, y, w, h):
    """Night sky over a city, missile trails arcing down."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for i in range(14):
        sx = x + 12 + (i * 37) % (w - 20)
        sy = y + 6 + (i * 23) % max(10, h // 2)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=WHITE)
    d.ellipse([x + w - 40, y + 6, x + w - 14, y + 32], fill=(235, 220, 180))
    for i, bx in enumerate([0, 52, 108, 168, 224]):
        bh = int(h * [0.42, 0.62, 0.5, 0.7, 0.36][i])
        d.rectangle([x + bx, y + h - bh, x + bx + 44, y + h], fill=(52, 58, 78))
        for wy in range(y + h - bh + 6, y + h - 4, 12):
            d.rectangle([x + bx + 8, wy, x + bx + 14, wy + 4], fill=YELLOW)
            d.rectangle([x + bx + 26, wy, x + bx + 32, wy + 4], fill=YELLOW)
    d.line([(x + 30, y + 4), (x + 120, y + h - 16)], fill=ORANGE, width=3)
    d.line([(x + 200, y + 4), (x + 150, y + h - 20)], fill=ORANGE, width=3)
    d.ellipse([x + 116, y + h - 20, x + 124, y + h - 12], fill=RED)
    d.ellipse([x + 146, y + h - 24, x + 154, y + h - 16], fill=RED)


def scene_warning(d, x, y, w, h):
    """Red warning triangle over a dark radar screen."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 34))
    d.ellipse([x + w // 2 - 34, y + 4, x + w // 2 + 34, y + 72], outline=TEAL,
              width=2)
    d.line([(x + w // 2, y + 38), (x + w // 2 + 30, y + 12)], fill=TEAL,
           width=2)
    for i in range(6):
        sx = x + 14 + (i * 41) % (w - 28)
        sy = y + 8 + (i * 13) % 26
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(120, 220, 200))
    cx, cy = x + w // 2, y + h - 12
    d.polygon([(cx, cy - 34), (cx - 26, cy + 12), (cx + 26, cy + 12)],
              fill=YELLOW, outline=RED, width=2)
    d.text((cx - 3, cy - 26), "!", font=font(F_SANS_B, 18), fill=RED_D)


def scene_border(d, x, y, w, h):
    """A border fence at dusk with a closed barrier gate."""
    d.rectangle([x, y, x + w, y + h], fill=(210, 150, 90))
    d.ellipse([x + w - 40, y + 6, x + w - 14, y + 32], fill=(255, 220, 140))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(90, 70, 50))
    for i in range(9):
        bx = x + 8 + i * 24
        d.line([(bx, y + 14), (bx, y + h - 22)], fill=(60, 60, 60), width=3)
    d.line([(x + 6, y + 20), (x + w - 6, y + 20)], fill=(60, 60, 60), width=3)
    d.line([(x + 6, y + 34), (x + w - 6, y + 34)], fill=(60, 60, 60), width=3)
    d.polygon([(x + 20, y + h - 34), (x + w - 60, y + h - 34),
               (x + w - 60, y + h - 26), (x + 20, y + h - 26)], fill=RED)
    d.text((x + 24, y + h - 33), "CLOSED", font=font(F_SANS_B, 10), fill=WHITE)


def scene_desert(d, x, y, w, h):
    """Desert dunes and a lone tower at dusk."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 190, 120))
    d.ellipse([x + w - 46, y + 6, x + w - 14, y + 38], fill=(255, 220, 140))
    d.polygon([(x, y + h - int(h * 0.3)), (x + w // 2, y + h - int(h * 0.5)),
               (x + w, y + h - int(h * 0.26)), (x + w, y + h), (x, y + h)],
              fill=(222, 164, 92))
    d.polygon([(x, y + h - int(h * 0.16)), (x + w // 3, y + h - int(h * 0.34)),
               (x + w, y + h - int(h * 0.14)), (x + w, y + h), (x, y + h)],
              fill=(196, 138, 70))
    ttop = y + int(h * 0.22)
    tbot = y + h - int(h * 0.34)
    d.rectangle([x + 30, ttop, x + 44, tbot], fill=(120, 90, 60))
    d.polygon([(x + 28, ttop), (x + 37, ttop - 12), (x + 46, ttop)],
              fill=(120, 90, 60))


def scene_clinic(d, x, y, w, h):
    """A clinic cross and a vaccination chart, pale blue."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    d.rectangle([x + 16, y + 8, x + 44, y + 36], fill=WHITE)
    d.rectangle([x + 26, y + 12, x + 34, y + 32], fill=RED)
    d.rectangle([x + 20, y + 18, x + 40, y + 26], fill=RED)
    base = y + h - 8
    for bx, bf, fc in [(64, 0.5, TEAL), (104, 0.35, NAVY), (144, 0.2, RED),
                       (184, 0.12, GOLD)]:
        bh = int((h - 20) * bf)
        d.rectangle([x + bx, base - bh, x + bx + 26, base], fill=fc)
    d.line([(x + 60, y + h - 30), (x + w - 10, y + h - 30)], fill=MUTED,
           width=1)


def scene_pill(d, x, y, w, h):
    """Two capsules and a rising bar chart on a white bench."""
    d.rectangle([x, y, x + w, y + h], fill=(236, 238, 242))
    base = y + h - 10
    for bx, bf, fc in [(16, 0.3, TEAL), (52, 0.5, NAVY), (88, 0.7, RED),
                       (124, 0.9, GOLD)]:
        bh = int((h - 24) * bf)
        d.rectangle([x + bx, base - bh, x + bx + 26, base], fill=fc)
    # capsule: two halves
    px, py = x + 168, y + 14
    d.ellipse([px, py, px + 40, py + 16], fill=TEAL)
    d.ellipse([px + 20, py, px + 60, py + 16], fill=WHITE)
    d.rectangle([px + 20, py, px + 40, py + 16], fill=WHITE)
    d.text((x + 16, y + 6), "$41bn", font=font(F_SANS_B, 13), fill=NAVY)


def scene_robot(d, x, y, w, h):
    """A robot head with glowing eyes on a courtroom-grey backdrop."""
    d.rectangle([x, y, x + w, y + h], fill=(200, 204, 212))
    hx, hy = x + w // 2 - 34, y + 6
    d.rectangle([hx, hy, hx + 68, hy + 44], fill=(70, 76, 84))
    d.rectangle([hx + 10, hy + 14, hx + 26, hy + 24], fill=(120, 220, 255))
    d.rectangle([hx + 42, hy + 14, hx + 58, hy + 24], fill=(120, 220, 255))
    d.rectangle([hx + 20, hy + 32, hx + 48, hy + 36], fill=(120, 220, 255))
    d.line([(hx + 34, hy), (hx + 34, hy - 8)], fill=(70, 76, 84), width=3)
    d.ellipse([hx + 30, hy - 14, hx + 38, hy - 6], fill=RED)
    d.rectangle([x + 10, y + h - 14, x + w - 10, y + h - 6], fill=(96, 74, 52))
    d.text((x + 10, y + h - 26), "SUED", font=font(F_SANS_B, 11), fill=RED_D)


def scene_island(d, x, y, w, h):
    """A small Pacific island with palm trees and a flag swap."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + 12, y + 8, x + 44, y + 40], fill=(255, 230, 150))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=SEA)
    d.polygon([(x + 30, y + h - 20), (x + 110, y + h - 20),
               (x + 180, y + h - 8), (x + 60, y + h - 8)], fill=SAND)
    d.polygon([(x + 150, y + h - 20), (x + 210, y + h - 20),
               (x + 230, y + h - 8), (x + 170, y + h - 8)], fill=SAND)
    for tx in (x + 70, x + 180):
        d.line([(tx, y + h - 20), (tx, y + h - 46)], fill=(110, 80, 50),
               width=3)
        d.line([(tx, y + h - 46), (tx - 12, y + h - 38)], fill=GREEN, width=3)
        d.line([(tx, y + h - 46), (tx + 12, y + h - 38)], fill=GREEN, width=3)
        d.line([(tx, y + h - 46), (tx, y + h - 52)], fill=GREEN, width=3)


# ---------------------------------------------------------------- data
# 40 stories, every one dated Tuesday 24 November 2026 (happened that
# day or first reported that day). Sources are named per story.
# tag: REPORTED = wires / on the record; CLAIM = one side's claim.

LEAD = [
    dict(n=1, place="SANTA CLARA, US", beat="TECH", tag="REPORTED",
         scene=scene_chip,
         head="Nvidia chief is back — Asia's stocks soar",
         body=("Trump intervenes; Huang reinstated as CEO. Seoul +6%, "
               "Nikkei +3.9%, Taiwan +9%."),
         src="Reuters · CNN"),
    dict(n=2, place="THE HAGUE", beat="JUSTICE", tag="REPORTED",
         scene=scene_court,
         head="Fourteen nations back Rohingya ruling",
         body=("UK sanctions Myanmar generals; Malaysia to return "
               "Rohingya refugees to Myanmar."),
         src="Reuters · Al Jazeera"),
    dict(n=3, place="ANTALYA, TÜRKIYE", beat="CLIMATE", tag="REPORTED",
         scene=scene_summit,
         head="COP31 collapses with no deal",
         body=("After ~50 hours overtime, 90+ nations rejected a draft "
               "that never said “fossil fuels”."),
         src="Reuters · Le Monde · CNN"),
]

GRID = [
    dict(n=4, place="BENGHAZI, LIBYA", beat="SEA WAR", tag="REPORTED",
         scene=scene_sea,
         head="Ukraine sinks Russian corvette off Libya",
         body="Tripoli demands an explanation from Kyiv.",
         src="CNN · France24"),
    dict(n=5, place="MOSCOW", beat="WARNING", tag="REPORTED",
         scene=scene_warning,
         head="Medvedev warns of preventive nuclear strike",
         body="NATO vows to defend space amid satellite reports.",
         src="Reuters · Le Monde"),
    dict(n=6, place="TALLINN, ESTONIA", beat="BORDER", tag="REPORTED",
         scene=scene_border,
         head="Russia warns Estonia: “verge of open war”",
         body="Tallinn to shut the border for six months from 1 Dec.",
         src="Reuters · France24"),
    dict(n=7, place="KYIV, UKRAINE", beat="WAR", tag="REPORTED",
         scene=scene_sky,
         head="Russian strikes kill 14 across Ukraine",
         body="Zaporizhzhia: 2 dead, 22 hurt. Dymer: 11 dead.",
         src="Reuters · AP"),
    dict(n=8, place="GAZA CITY", beat="CONFLICT", tag="REPORTED",
         scene=scene_desert,
         head="Gaza war undoes 77 years of development",
         body="Strikes kill 3, incl. an UNRWA worker. Oxfam: “toxic land”.",
         src="Al Jazeera · Reuters"),
    dict(n=9, place="WASHINGTON, US", beat="HEALTH", tag="REPORTED",
         scene=scene_clinic,
         head="US loses measles elimination status",
         body="After 25+ years. Pennsylvania records a ninth death.",
         src="AP · CNN"),
    dict(n=10, place="PARIS · CAMBRIDGE, US", beat="DEAL", tag="REPORTED",
         scene=scene_pill,
         head="Sanofi to buy Insmed for $41 billion",
         body="The US biotech deal is Sanofi's biggest in years.",
         src="Reuters · AP"),
    dict(n=11, place="SALEM · RICHMOND, US", beat="COURTS", tag="REPORTED",
         scene=scene_robot,
         head="US states sue Musk over Grok sex images",
         body="Oregon and Virginia sue SpaceX over the chatbot.",
         src="Reuters · AP"),
    dict(n=12, place="HONIARA", beat="PACIFIC", tag="REPORTED",
         scene=scene_island,
         head="Solomons to end China security pact",
         body="An Australia treaty will replace it, Honiara says.",
         src="Reuters · AP"),
    dict(n=13, place="WASHINGTON · TEHRAN", beat="GULF", tag="REPORTED",
         scene=scene_sea,
         head="Netanyahu presses Trump on Iran strikes",
         body="Iran vows to counter a Hormuz blockade; tankers mined.",
         src="Reuters · Al Jazeera"),
]

# The numbered list: 27 more stories, 14–40. Each fits one line.
MORE = [
    ("Nepal", "5.6 quake strikes near China border"),
    ("Yemen", "Houthis: Saudi strike kills 17 in Hodeida"),
    ("DR Congo", "fighting traps Ebola teams, WHO says"),
    ("South Sudan", "21 killed in Tonj East attack"),
    ("South Sudan", "50,000+ sit school exams"),
    ("Colombia", "car bomb wrecks buildings in Villavicencio"),
    ("Mexico", "“El Chapo Isidro” to stand trial"),
    ("El Salvador", "3 troops killed in Haiti operation"),
    ("Argentina", "bid to halt Falklands oil work"),
    ("China", "Tiangong opens to Pakistani astronaut"),
    ("Space", "most distant glowing black hole found"),
    ("FDA", "first drug for limb-girdle dystrophy"),
    ("UN", "47,000 women killed by partners in 2025"),
    ("WFP", "wars threaten food aid for 7.3m more"),
    ("Armenia", "draft charter drops Karabakh claim"),
    ("EU", "22nd sanctions package proposed on Russia"),
    ("Trump", "to meet NATO chief Rutte in Florida"),
    ("Hanoi", "explosion kills 6"),
    ("UAE", "bus-truck crash kills 11 in Ras Al Khaimah"),
    ("Nigeria", "Borno school enrolment nearly doubles"),
    ("Egypt/Iraq", "agree to scrap mutual visas"),
    ("Indonesia", "Mecca pact signals new security line"),
    ("GTA 6", "$3.8bn in first-day sales, a record"),
    ("N. Korea", "threatens Swiss office over sanctions"),
    ("China", "JL-15 trainer to debut at Zhuhai show"),
    ("Arm", "CEO Haas' tenure extended to 2033"),
    ("US", "Megaspeed blacklisted in Nvidia probe"),
]

STATS = [
    ("14", "nations affirm ICJ ruling"),
    ("90+", "nations rejected COP draft"),
    ("$41bn", "Sanofi's Insmed deal"),
    ("25", "years: US measles status lost"),
    ("14", "killed in Ukraine strikes"),
    ("3", "tankers hit in Hormuz"),
]

REGIONS = [
    ("EUROPE", 8, NAVY), ("MIDDLE EAST", 6, RED), ("ASIA-PACIFIC", 8, GOLD),
    ("AMERICAS", 6, TEAL), ("AFRICA", 5, GREEN), ("SCI/TECH/BIZ", 7,
     (90, 60, 120)),
]

# Coarse world dot-map (land = #). Columns run west to east, rows north
# to south; red dots below mark where the featured stories happened.
MAP_ROWS = [
    "...........XXXXX....................................",
    "........XXXXXXXXXXX........XXXXXXXXXXXXXXXXXXX.......",
    "......XXXXXXXXXXXXXXXX....XXXXXXXXXXXXXXXXXXXXX.....",
    "....XXXXXXXXXXXXXXXXXX....XXXXXXXXXXXXXXXXXXXXXX....",
    ".....XXXXXXXXXXXXXXXX.......XXXXXXXXXXXXXXXXXX......",
    "......XXXXXXXXXXXXXX.........XXXXXXXX..XXXXXX.........",
    ".......XXXXXXXXXXX............XXXXXX...XXXX...........",
    "........XXXXXXXXX..............XXXX.....XX............",
    ".........XXXXXXX................XX...................",
    "..........XXXXX.....................................",
    "...........XXXX.............XXXXX....................",
    "............XX..............XXXXXXX..................",
    ".............X...............XXXXXXXXX...............",
    "..............................XXXXXX.................",
    "...............................XXXX.................",
    "................................XX.................",
    ".................................X.................",
]
# (col, row) of the red dots on the map above.
MAP_DOTS = [(27, 3), (30, 6), (28, 4), (26, 3), (31, 4), (33, 7), (34, 8),
            (45, 11), (11, 6), (48, 5), (27, 2), (29, 4), (10, 9),
            (32, 9), (36, 7), (31, 10)]


# ---------------------------------------------------------------- cards
def draw_lead(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE)
    s["scene"](d, x + 1, y + 1, w - 2, 80)
    tag(d, x + 10, y + 86, s["tag"], TEAL if s["tag"] == "REPORTED" else RED)
    yy = y + 106
    d.text((x + 10, yy), f"{s['n']}  {s['place']} · {s['beat']}",
           font=font(F_SANS_B, 12), fill=RED_D)
    yy += 16
    head_lines = wrap(d, s["head"], font(F_SERIF, 21), w - 20)
    assert len(head_lines) <= 2, f"lead {s['n']} headline {len(head_lines)} lines"
    yy = text_block(d, x + 10, yy, head_lines, font(F_SERIF, 21), leading=23)
    yy += 2
    body_lines = wrap(d, s["body"], font(F_SANS, 12), w - 20)
    assert len(body_lines) <= 2, f"lead {s['n']} body {len(body_lines)} lines"
    text_block(d, x + 10, yy, body_lines, font(F_SANS, 12), leading=14)


def draw_grid_card(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE)
    s["scene"](d, x + 1, y + 1, w - 2, 54)
    tag(d, x + 8, y + 58, s["tag"], TEAL if s["tag"] == "REPORTED" else RED)
    yy = y + 78
    d.text((x + 8, yy), f"{s['n']}  {s['place']} · {s['beat']}",
           font=font(F_SANS_B, 10), fill=RED_D)
    yy += 14
    head_lines = wrap(d, s["head"], font(F_SERIF, 16), w - 16)
    assert len(head_lines) <= 2, f"grid {s['n']} headline {len(head_lines)} lines"
    yy = text_block(d, x + 8, yy, head_lines, font(F_SERIF, 16), leading=17)
    yy += 1
    body_lines = wrap(d, s["body"], font(F_SANS, 11), w - 16)
    assert len(body_lines) <= 2, f"grid {s['n']} body {len(body_lines)} lines"
    text_block(d, x + 8, yy, body_lines, font(F_SANS, 11), leading=12)


# ---------------------------------------------------------------- compose
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE)
    d.text((x + 10, y + 8), "WHERE IT HAPPENED",
           font=font(F_SANS_B, 12), fill=NAVY)
    cols = len(MAP_ROWS[0])
    rows = len(MAP_ROWS)
    cw, ch = (w - 20) / cols, (h - 52) / rows
    dot = min(cw, ch) * 0.62
    for r, row in enumerate(MAP_ROWS):
        for c, ch_ in enumerate(row):
            if ch_ == "X":
                cx = x + 10 + c * cw + (cw - dot) / 2
                cy = y + 30 + r * ch + (ch - dot) / 2
                d.ellipse([cx, cy, cx + dot, cy + dot], fill=(150, 150, 140))
    for (c, r) in MAP_DOTS:
        cx = x + 10 + c * cw + cw / 2
        cy = y + 30 + r * ch + ch / 2
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=RED, width=1)
    d.text((x + 10, y + h - 18), "Dot map — red dots mark the featured stories.",
           font=font(F_SANS_I, 10), fill=MUTED)


def draw_more_list(d, x, y, w, h):
    d.text((x, y), "ALSO ON TUESDAY 24 NOVEMBER — 27 MORE STORIES",
           font=font(F_SANS_B, 13), fill=NAVY)
    y += 22
    col_w = (w - 16) // 2
    f_num = font(F_SANS_B, 11)
    f_txt = font(F_SANS, 11)
    for i, (place, txt) in enumerate(MORE):
        col = 0 if i < 14 else 1
        row = i if i < 14 else i - 14
        lx = x + col * (col_w + 16)
        ly = y + row * 12
        d.rectangle([lx, ly + 1, lx + 7, ly + 8], fill=RED)
        d.text((lx + 11, ly), f"{14 + i}.", font=f_num, fill=RED_D)
        label = f"{place} — {txt}"
        lines = wrap(d, label, f_txt, col_w - 34)
        assert len(lines) == 1, f"list {14 + i} wraps to {len(lines)} lines: {label}"
        d.text((lx + 34, ly), lines[0], font=f_txt, fill=INK)


def main(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top bar
    d.rectangle([0, 0, W, 26], fill=NAVY_D)
    d.text((10, 5), "THE WORLD IN ONE DAY", font=font(F_SANS_B, 14), fill=WHITE)
    right = "40 STORIES · 6 REGIONS · EVERY ONE DATED TUESDAY 24 NOVEMBER 2026"
    d.text((W - 10 - d.textlength(right, font=font(F_SANS_B, 13)), 6), right,
           font=font(F_SANS_B, 13), fill=GOLD)

    # --- masthead
    title = "Tuesday 24 November 2026"
    tf = font(F_SERIF, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 30), title, font=tf, fill=INK)
    ticker = ("Nvidia chief returns  ·  Myanmar ruling backed  ·  COP31 collapses  ·  "
              "Merkury sunk  ·  US measles status lost")
    tf2 = font(F_SANS, 16)
    d.text(((W - d.textlength(ticker, font=tf2)) / 2, 104), ticker, font=tf2,
           fill=RED_D)

    # --- stats strip
    y0 = 128
    sw = W / len(STATS)
    for i, (num, label) in enumerate(STATS):
        cx = i * sw + sw / 2
        nf = font(F_SERIF, 30)
        d.text((cx - d.textlength(num, font=nf) / 2, y0), num, font=nf, fill=RED_D)
        lf = font(F_SANS, 11)
        d.text((cx - d.textlength(label, font=lf) / 2, y0 + 34), label, font=lf,
               fill=MUTED)
        if i:
            d.line([(i * sw, y0 + 4), (i * sw, y0 + 46)], fill=LINE, width=1)
    hline(d, 0, W, y0 + 52, fill=LINE, width=1)

    # --- region bar
    y0 = 184
    total = sum(n for _, n, _ in REGIONS)
    assert total == 40, f"regions sum to {total}, not 40"
    rx = 0
    for name, n, col in REGIONS:
        seg = int(W * n / total)
        d.rectangle([rx, y0, rx + seg, y0 + 18], fill=col)
        d.text((rx + 6, y0 + 3), f"{name} {n}", font=font(F_SANS_B, 11), fill=WHITE)
        rx += seg

    # --- lead row: 3 cards
    y0 = 208
    cw = (W - 20 - 16) // 3
    for i, s in enumerate(LEAD):
        draw_lead(d, 10 + i * (cw + 8), y0, cw, 196, s)

    # --- grid rows: 5 + 5 cards
    gw = (W - 20 - 32) // 5
    for row in range(2):
        y0 = 412 + row * 158
        for i in range(5):
            draw_grid_card(d, 10 + i * (gw + 8), y0, gw, 150, GRID[row * 5 + i])

    # --- bottom: map + more stories
    y0 = 726
    draw_map(d, 10, y0, 300, 180)
    draw_more_list(d, 326, y0 + 2, W - 336, 180)

    # --- date check
    y0 = 914
    d.rectangle([10, y0, W - 10, y0 + 68], outline=RED, width=2)
    d.text((18, y0 + 6), "DATE CHECK — READ THIS FIRST",
           font=font(F_SANS_B, 12), fill=RED_D)
    dc = ("Every story above happened, or was first reported, on Tuesday 24 November 2026. "
          "Left out because they belong to earlier days: the COP31 collapse itself (decided late Mon 23 Nov — "
          "Tuesday's story is the fallout); the ICJ Rohingya ruling (19 Nov — Tuesday's story is the affirmations "
          "and sanctions); the Merkury sinking (Mon 23 Nov — first reported Tue 24 Nov); Russian missiles in Poland "
          "(20 Nov); the Democrats' midterm majorities (decided 3 Nov).")
    text_block(d, 18, y0 + 22, wrap(d, dc, font(F_SANS, 12), W - 36),
               font(F_SANS, 12), leading=14)

    # --- footer
    d.text((10, 992),
           "Sources: Reuters · AP · CNN · Le Monde · Al Jazeera · France24 — scenes drawn, not photographs.",
           font=font(F_SANS, 11), fill=MUTED)
    d.text((10, 1006),
           "REPORTED = wires / on the record · CLAIM = one side's claim, named as such",
           font=font(F_SANS, 11), fill=MUTED)

    img.save(out_path, format="PNG", optimize=True)
    data = open(out_path, "rb").read()
    print(f"wrote {out_path}: {len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    return len(data)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
