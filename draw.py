#!/usr/bin/env python3
"""WORLD NEWS - 24 November 2026 infographic (1024x1024)."""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W = H = 1024
FD = "/usr/share/fonts/truetype/dejavu/"
def font(n, s): return ImageFont.truetype(FD + n, s)

BG     = (16, 18, 24)
PANEL  = (26, 29, 38)
LINE   = (48, 53, 66)
INK    = (235, 238, 244)
BODY_C = (202, 208, 218)
DIM    = (148, 156, 170)
RED, AMBER, BLUE, ORANGE = (229, 72, 64), (232, 168, 56), (86, 156, 240), (238, 130, 66)

F_TITLE = font("DejaVuSans-Bold.ttf", 44)
F_DATE  = font("DejaVuSans-Bold.ttf", 21)
F_SUB   = font("DejaVuSans.ttf", 17)
F_HEAD  = font("DejaVuSans-Bold.ttf", 23)
F_BODY  = font("DejaVuSans.ttf", 18)
F_TAG   = font("DejaVuSans-Bold.ttf", 14)
F_KICK  = font("DejaVuSans-Bold.ttf", 16)
F_FOOT  = font("DejaVuSans.ttf", 15)
F_FOOTB = font("DejaVuSans-Bold.ttf", 14)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 58
def wrap(t, w): return textwrap.wrap(t, width=w)
def tw(f, s): return d.textlength(s, font=f)

# masthead
d.rectangle([0, 0, W, 6], fill=RED)
y = 38
d.text((M, y), "WORLD NEWS", font=F_TITLE, fill=INK)
d.text((M + tw(F_TITLE, "WORLD NEWS") + 20, y + 24), "24 November 2026", font=F_DATE, fill=AMBER)
y += 56
d.text((M, y), "Tuesday's biggest stories \u2014 the day in four cards", font=F_SUB, fill=DIM)
y += 28
d.line([M, y, W - M, y], fill=LINE, width=2)
y += 16

cards = [
    (RED, "WAR / ENERGY",
     "Iran tightens the noose on Hormuz",
     "Army commander: strait stays closed 'further day by day' until Washington meets Tehran's seven conditions. IRGC: three tankers hit naval mines and burned despite US escort. US widens shadow-banking sanctions; Brent crude near $89.",
     "Qatar's PM met Rubio and Vance to push US\u2013Iran talks."),
    (AMBER, "RUSSIA / UKRAINE",
     "Putin: retaliation is 'inevitable'",
     "Ukrainian drones cut Russian refining ~45% since late October. Navy drones sank corvette Merkury off Benghazi; cargo ship hit in Gulf of Finland. Poland summoned Russia's envoy; Moscow accuses Estonia of brink of war.",
     "Zaporizhzhia overnight: 2 killed, 40 wounded."),
    (BLUE, "TECH / AI",
     "Huang back at Nvidia after 11 days",
     "Trump personally lobbied the board after Jensen Huang's resignation over scandal, calling him 'a national treasure'; reinstated as CEO and shares surged. Yet AI stocks tumbled Tuesday and Anthropic fell below its $83 IPO.",
     "UN chief: global AI-oversight framework within a year."),
    (ORANGE, "MIDEAST",
     "Houthis push toward Aden",
     "Advance of ~60 km toward Aden; Yemen's army declares 'Aden is a red line'. Israeli strikes killed nine in Gaza, among them Hamas's interior-security chief.",
     "Riyadh financial tower attacked again \u2014 11 injured."),
]

FOOT_TOP = H - 160   # footer occupies FOOT_TOP .. H-40
GAP = 10
heights = [12 + 22 + 6 + 30 + len(wrap(c[3], 88)) * 22 + 2 + 24 + 10 for c in cards]
total = sum(heights) + GAP * 3
assert y + total <= FOOT_TOP, f"cards overflow: {y+total} > {FOOT_TOP}"

for i, (color, tag, head, body, kicker) in enumerate(cards):
    ch = heights[i]
    d.rectangle([M, y, W - M, y + ch], fill=PANEL)
    d.rectangle([M, y, M + 5, y + ch], fill=color)
    x0 = M + 20
    yy = y + 12
    d.rectangle([x0, yy, x0 + tw(F_TAG, tag) + 16, yy + 22], fill=color)
    d.text((x0 + 8, yy + 3), tag, font=F_TAG, fill=(10, 10, 12))
    yy += 28
    d.text((x0, yy), head, font=F_HEAD, fill=INK)
    yy += 30
    for ln in wrap(body, 88):
        d.text((x0, yy), ln, font=F_BODY, fill=BODY_C)
        yy += 22
    yy += 2
    d.text((x0, yy), "\u25b8 " + kicker, font=F_KICK, fill=color)
    assert yy + 22 <= y + ch
    y += ch + GAP

# footer
fy = FOOT_TOP
d.rectangle([M, fy, W - M, H - 36], fill=(30, 33, 42))
d.rectangle([M, fy, M + 5, H - 36], fill=AMBER)
d.text((M + 20, fy + 8), "ALSO ON THE WIRE", font=F_FOOTB, fill=AMBER)
ff = fy + 32
foot = [
    "\u2022 Qatar protested Iran summoning its diplomat over a Doha\u2013Berlin statement",
    "\u2022 Libya and Italy condemned the strike on the Russian-linked ship in Libyan waters",
    "\u2022 Moscow: Estonia's NATO moves are 'on the verge of unleashing open war'",
    "\u2022 US Treasury widened sanctions on Iran's shadow-banking networks",
]
for ln in foot:
    d.text((M + 20, ff), ln, font=F_FOOT, fill=DIM)
    ff += 19

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "last card bottom:", y - GAP)
