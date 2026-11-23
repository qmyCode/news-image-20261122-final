#!/usr/bin/env python3
"""NI22 builder: draws entry.png (1024x1024) — Sunday 22 November 2026.
Cream broadsheet per the NI winning formula: count-claim masthead, giant
serif date, UTC timeline, 6-stat bar, region tally, 3 mains, 12 cards,
numbered-pin world map, 23 sourced ALSO lines, DATE CHECK, sources footer.
Every story wire-verified as Sunday 22 Nov 2026 news (see story-bank.md).
Build tool only; the entrypoint is main.py (stdlib copier).
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

W = H = 1024
BG     = (247, 242, 231)
PANEL  = (255, 252, 244)
INK    = (26, 23, 18)
MUT    = (104, 95, 80)
RULE   = (60, 52, 40)
RED    = (163, 22, 33)
NAVY   = (31, 58, 95)
GOLD   = (176, 132, 40)

REG = {  # region colours
    "EU": (43, 94, 167), "ME": (179, 57, 46), "AM": (46, 125, 79),
    "AP": (203, 118, 16), "AF": (122, 74, 33), "OC": (106, 74, 158),
    "W":  (105, 105, 105),
}
REGNAME = {"EU": "EUROPE", "ME": "MIDDLE EAST", "AM": "AMERICAS",
           "AP": "ASIA-PACIFIC", "AF": "AFRICA", "OC": "OCEANIA", "W": "WORLD"}

FD = "/usr/share/fonts/truetype/dejavu/"
_fc = {}
def F(name, size):
    key = (name, size)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(FD + name, size)
    return _fc[key]
def SER(s):  return F("DejaVuSerif.ttf", s)
def SERB(s): return F("DejaVuSerif-Bold.ttf", s)
def SAN(s):  return F("DejaVuSans.ttf", s)
def SANB(s): return F("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

def tw(t, f):
    return d.textlength(t, font=f)

def wrap(t, f, maxw):
    words, lines, cur = t.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def text(x, y, t, f, fill=INK, anchor="la"):
    d.text((x, y), t, font=f, fill=fill, anchor=anchor)

def ctext(cx, y, t, f, fill=INK):
    d.text((cx, y), t, font=f, fill=fill, anchor="ma")

def para(x, y, t, f, maxw, lh, fill=INK, max_lines=None):
    lines = wrap(t, f, maxw)
    if max_lines: lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh

def rule(x0, x1, y, wdt=1, fill=RULE):
    d.line([x0, y, x1, y], fill=fill, width=wdt)

def tag(x, y, label, colour):
    """Certainty pill, returns width used."""
    f = SANB(8)
    wdt = tw(label, f) + 10
    d.rounded_rectangle([x, y, x + wdt, y + 13], 6, fill=colour)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return wdt

MX = 28            # page margin
PW = W - 2 * MX    # printable width = 968

# ---------------------------------------------------------------- masthead
y = 14
ctext(W // 2, y,
      "3 8   D A T E D   S T O R I E S   ·   7   R E G I O N S   ·   1 5   I L L U S T R A T E D   ·   E V E R Y   L I N E   S O U R C E D",
      SANB(11), RED)
y += 22
rule(MX, W - MX, y, 2); rule(MX, W - MX, y + 3, 1)
y += 10
ctext(W // 2, y, "Sunday 22 November 2026", SERB(57), INK)
y += 74
ctext(W // 2, y, "One day's news, on one page — every story below happened on Sunday 22 November 2026 and was checked against the wires. All times UTC.",
      SAN(10.5), MUT)
y += 20
rule(MX, W - MX, y, 1)
y += 6

# ---------------------------------------------------------------- timeline
TL = [
    ("01:00", "Hong Kong polls open"),
    ("02:55", "Kyiv: the barrage peaks"),
    ("05:30", "Verstappen wins in Las Vegas"),
    ("10:00", "Hong Kong polls close"),
    ("11:00", "Cikande search suspended"),
    ("16:28", "Atlanta ground delay lifted"),
    ("18:30", "Liverpool 4-0 Man Utd, FT"),
    ("19:17", "Alcaraz takes the ATP Finals"),
]
colw = PW / len(TL)
for i, (tm, lab) in enumerate(TL):
    cx = MX + colw * i + colw / 2
    ctext(cx, y, tm, SANB(10.5), NAVY)
    for j, ln in enumerate(wrap(lab, SAN(8.5), colw - 8)):
        ctext(cx, y + 15 + j * 10.5, ln, SAN(8.5), MUT)
    if i:
        d.line([MX + colw * i, y + 2, MX + colw * i, y + 34], fill=(205, 196, 175), width=1)
y += 40
rule(MX, W - MX, y, 1)
y += 7

# ---------------------------------------------------------------- stat bar
STATS = [
    ("186", "drones in the night barrage on Ukraine"),
    ("161", "drones downed, Kyiv's air force says"),
    ("44 hrs", "of overtime at COP31 — still no deal"),
    ("$120bn", "adaptation target dropped from the draft"),
    ("720/9", "India's record Test total in NZ"),
    ("50", "Wembanyama points — first 50-15-5-4 game"),
]
sw = PW / 6
for i, (num, lab) in enumerate(STATS):
    x0 = MX + sw * i
    d.rectangle([x0 + 3, y, x0 + sw - 3, y + 44], fill=PANEL, outline=(205, 196, 175))
    ctext(x0 + sw / 2, y + 4, num, SERB(19), RED if i in (0, 2, 3) else NAVY)
    for j, ln in enumerate(wrap(lab, SAN(8), sw - 14)):
        ctext(x0 + sw / 2, y + 27 + j * 9.5, ln, SAN(8), MUT)
y += 52

# ---------------------------------------------------------------- tally
TALLY = [("EU", 8), ("ME", 7), ("AM", 8), ("AP", 7), ("AF", 4), ("OC", 2), ("W", 2)]
segs = []
for code, n in TALLY:
    segs.append((code, f"{REGNAME[code]} {n}"))
total_w = sum(14 + tw(s, SANB(10)) for _, s in segs) + 22 * (len(segs) - 1) + tw("— 38 STORIES", SANB(10)) + 22
x = (W - total_w) / 2
for code, s in segs:
    d.rectangle([x, y + 2, x + 9, y + 11], fill=REG[code])
    text(x + 14, y, s, SANB(10), INK)
    x += 14 + tw(s, SANB(10)) + 22
text(x, y, "— 38 STORIES", SANB(10), RED)
y += 18
rule(MX, W - MX, y, 2)
y += 8

# ---------------------------------------------------------------- scenes
def dashed(p0, p1, fill, width=2, dash=7, gap=5):
    x0, y0 = p0; x1, y1 = p1
    dist = math.hypot(x1 - x0, y1 - y0)
    if dist == 0: return
    ux, uy = (x1 - x0) / dist, (y1 - y0) / dist
    t = 0.0
    while t < dist:
        t2 = min(t + dash, dist)
        d.line([x0 + ux * t, y0 + uy * t, x0 + ux * t2, y0 + uy * t2], fill=fill, width=width)
        t += dash + gap

def flame(cx, cy, s, base=(232, 119, 34)):
    d.polygon([(cx, cy - s), (cx + s * 0.55, cy + s * 0.35), (cx + s * 0.28, cy + s * 0.8),
               (cx - s * 0.28, cy + s * 0.8), (cx - s * 0.55, cy + s * 0.35)], fill=base)
    d.polygon([(cx, cy - s * 0.45), (cx + s * 0.3, cy + s * 0.3), (cx, cy + s * 0.7),
               (cx - s * 0.3, cy + s * 0.3)], fill=(247, 183, 49))

def drone(cx, cy, s):
    d.ellipse([cx - s, cy - s * 0.35, cx + s, cy + s * 0.35], fill=(10, 10, 14))
    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        ex, ey = cx + dx * s * 1.5, cy + dy * s * 0.8
        d.line([cx, cy, ex, ey], fill=(10, 10, 14), width=2)
        d.ellipse([ex - 3, ey - 1.5, ex + 3, ey + 1.5], outline=(200, 200, 210), width=1)

def scene_kyiv(x, y, w, h):
    for i in range(h):  # night sky gradient
        t = i / h
        d.line([x, y + i, x + w, y + i], fill=(int(14 + 26 * t), int(20 + 30 * t), int(44 + 44 * t)))
    d.ellipse([x + w - 52, y + 8, x + w - 30, y + 30], fill=(232, 228, 200))  # moon
    for bx, bw, bh in [(6, 30, 26), (44, 22, 34), (238, 26, 30), (268, 34, 22)]:  # skyline
        d.rectangle([x + bx, y + h - bh - 14, x + bx + bw, y + h - 14], fill=(8, 10, 18))
    # searchlight beams
    d.polygon([(x + 30, y + h - 12), (x + 120, y + 6), (x + 138, y + 6)], fill=(255, 250, 210, 46))
    d.polygon([(x + w - 26, y + h - 12), (x + 176, y + 4), (x + 194, y + 4)], fill=(255, 250, 210, 40))
    # the Dymer block: intact left section + collapsed right section
    bx, by, bw2, bh2 = x + 96, y + h - 78, 108, 64
    d.rectangle([bx, by, bx + 62, by + bh2], fill=(52, 48, 44))
    for r in range(5):
        for c in range(3):
            lit = (r * 3 + c) % 3 != 0
            d.rectangle([bx + 8 + c * 18, by + 7 + r * 12, bx + 18 + c * 18, by + 14 + r * 12],
                        fill=(250, 196, 92) if lit else (24, 24, 28))
    d.polygon([(bx + 62, by + 10), (bx + bw2, by + 34), (bx + bw2, by + bh2), (bx + 62, by + bh2)],
              fill=(70, 62, 54))  # collapsed section
    d.polygon([(bx + 58, by + bh2), (bx + 84, by + 30), (bx + 108, by + bh2)], fill=(88, 78, 66))
    for i in range(7):  # rubble + dust
        d.ellipse([bx + 60 + i * 7, y + h - 20 - (i % 3) * 3, bx + 70 + i * 7, y + h - 13], fill=(96, 86, 72))
    d.ellipse([bx + 56, by + 16, bx + 116, by + 40], fill=(150, 145, 135, 70))
    text(bx + 2, by - 13, "DYMER — FIVE-STOREY BLOCK", SANB(8), (235, 232, 220))
    for (dx, dy, s) in [(60, 22, 7), (150, 12, 6), (216, 30, 7)]:  # drones + trails
        dashed((x + dx - 34, y + dy - 14), (x + dx - 6, y + dy - 2), (240, 120, 110), 2)
        drone(x + dx, y + dy, s)
    d.rectangle([x, y + h - 15, x + w, y + h], fill=(8, 8, 12, 215))
    ctext(x + w / 2, y + h - 12.5, "186 IN · 161 DOWNED · 72 JET-POWERED", SANB(9.5), (255, 244, 214))

def scene_cop31(x, y, w, h):
    # ---- background: the plenary hall, dimmed, in perspective
    for i in range(64):  # wall gradient, dark teal to lit horizon
        t = i / 64
        d.line([x, y + i, x + w, y + i],
               fill=(int(22 + 34 * t), int(36 + 36 * t), int(34 + 28 * t)))
    d.rectangle([x, y + 64, x + w, y + h], fill=(52, 43, 32))  # floor
    for fx in (40, 92, 214, 266):  # floor perspective seams
        d.line([x + 153, y + 64, x + fx, y + h], fill=(38, 31, 22), width=1)
    # spotlight cones washing down over the table
    d.polygon([(x + 52, y), (x + 118, y + 62), (x + 168, y + 62)], fill=(255, 246, 200, 30))
    d.polygon([(x + 254, y), (x + 150, y + 62), (x + 200, y + 62)], fill=(255, 246, 200, 26))
    # exit doors at both edges — bright, delegates streaming out
    d.rectangle([x, y + 26, x + 13, y + 66], fill=(206, 192, 148))
    d.rectangle([x + 2, y + 29, x + 11, y + 63], fill=(120, 104, 70))
    d.rectangle([x + w - 13, y + 26, x + w, y + 66], fill=(240, 228, 176))
    d.rectangle([x + w - 11, y + 29, x + w - 2, y + 63], fill=(146, 128, 82))
    d.polygon([(x + w - 12, y + 63), (x + w - 52, y + 84), (x + w, y + 84)], fill=(255, 240, 190, 42))
    # rows of flag poles flanking the backdrop
    flag_cols = [(214, 44, 44), (44, 94, 167), (46, 125, 79), (203, 118, 16),
                 (122, 74, 33), (250, 196, 92), (163, 22, 33), (106, 74, 158)]
    for i, fdx in enumerate((14, 32, 50, 68, 224, 240, 256, 272)):
        d.line([x + fdx, y + 2, x + fdx, y + 36], fill=(168, 160, 140), width=1)
        d.rectangle([x + fdx + 1, y + 3, x + fdx + 12, y + 10], fill=flag_cols[i])
    # the COP31 Antalya backdrop banner
    d.rectangle([x + 90, y + 5, x + 216, y + 33], fill=(15, 32, 50), outline=GOLD, width=1)
    ctext(x + 153, y + 7, "COP31", SERB(14), (245, 242, 230))
    ctext(x + 153, y + 24, "ANTALYA · CLIMATE SUMMIT", SANB(6.5), (232, 196, 110))
    # the plenary overtime clock, on the left wall under the flags
    d.rectangle([x + 16, y + 14, x + 80, y + 34], fill=(10, 10, 12), outline=(120, 116, 100))
    ctext(x + 48, y + 15.5, "44:00", SANB(12), (255, 96, 60))
    ctext(x + 48, y + 28, "OVERTIME", SANB(6), (255, 178, 120))

    def fig(cx, top, hgt, tone, flip=1, briefcase=False, despair=False, gather=False):
        """Delegate silhouette: head, suit body, striding legs, optional briefcase."""
        cx += x; top += y
        hr = max(3.0, hgt * 0.11)
        hy = top + hr
        d.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=tone)
        shy, hiy = top + hgt * 0.27, top + hgt * 0.58
        swd = max(4.0, hgt * 0.13)
        d.polygon([(cx - swd, shy), (cx + swd, shy), (cx + swd - 1, hiy), (cx - swd + 1, hiy)], fill=tone)
        d.line([cx - 2, hiy, cx - flip * 2 - 3, top + hgt], fill=tone, width=3)
        d.line([cx + 2, hiy, cx + flip * 5, top + hgt], fill=tone, width=3)
        if despair:
            d.line([cx - swd, shy + 2, cx - swd - 4, top + 3], fill=tone, width=2)
            d.line([cx + swd, shy + 2, cx + swd + 4, top + 3], fill=tone, width=2)
        elif gather:
            d.line([cx + swd, shy + 2, cx + swd + 6, hiy + 3], fill=tone, width=2)
        elif briefcase:
            hx, hyy = cx + flip * (swd + 5), hiy + 1
            d.line([cx + flip * swd, shy + 2, hx, hyy], fill=tone, width=2)
            d.rectangle([hx - 5, hyy, hx + 5, hyy + 7], fill=(56, 40, 22), outline=(150, 120, 70))

    # ---- mid-ground: empty named chairs + delegates on their feet behind the table
    for ccx, nm in ((75, "EU"), (133, "UK"), (193, "PANAMA")):
        d.rounded_rectangle([x + ccx - 13, y + 49, x + ccx + 13, y + 63], 2, fill=(24, 24, 30))
        ctext(x + ccx, y + 54.5, nm, SANB(6.5), (226, 220, 200))
    fig(100, 31, 30, (18, 18, 24), despair=True)          # head in hands between EU and UK
    fig(163, 33, 29, (26, 32, 46), gather=True)           # gathering papers, centre
    fig(238, 30, 32, (18, 18, 24), flip=1, briefcase=True)  # already walking out, right
    # the long negotiation table, in perspective
    d.polygon([(x + 58, y + 60), (x + 248, y + 60), (x + 270, y + 80), (x + 36, y + 80)], fill=(116, 90, 58))
    d.polygon([(x + 36, y + 80), (x + 270, y + 80), (x + 270, y + 84), (x + 36, y + 84)], fill=(82, 62, 38))
    d.ellipse([x + 108, y + 59, x + 216, y + 71], fill=(255, 244, 200, 30))  # lamp pool
    for ccx in (75, 133, 193):  # gooseneck mics beside the empty chairs' name plates
        d.line([x + ccx - 18, y + 67, x + ccx - 15, y + 59], fill=(20, 20, 22), width=1)
        d.ellipse([x + ccx - 16.5, y + 57, x + ccx - 13.5, y + 60], fill=(20, 20, 22))
    # abandoned papers scattered on the table
    for pdx, pdy in ((66, 64), (80, 70), (222, 66), (234, 71)):
        d.polygon([(x + pdx, y + pdy), (x + pdx + 13, y + pdy - 1), (x + pdx + 14, y + pdy + 5),
                   (x + pdx + 1, y + pdy + 6)], fill=(238, 234, 222))
    # THE draft — lying unsigned on the table, fossil-fuel line struck out in red
    d.polygon([(x + 100, y + 63), (x + 170, y + 61), (x + 174, y + 79), (x + 104, y + 80)],
              fill=(250, 247, 238), outline=(150, 144, 128))
    text(x + 106, y + 63.5, "THE ANTALYA PACT", SANB(6.5), INK)
    text(x + 106, y + 70.5, "coal · oil · gas", SANB(6), (120, 30, 30))
    d.line([x + 105, y + 75, x + 150, y + 74], fill=RED, width=1)
    d.line([x + 106, y + 77.5, x + 118, y + 76.5], fill=(30, 30, 60), width=2)  # the pen, unused
    stamp = Image.new("RGBA", (46, 12), (0, 0, 0, 0))  # red UNSIGNED stamp, angled
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([0, 0, 45, 11], outline=(163, 22, 33), width=1)
    sd.text((3, 1.5), "UNSIGNED", font=SANB(7), fill=(163, 22, 33))
    stamp = stamp.rotate(16, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (int(x + 128), int(y + 66)), stamp)
    # standing placard on the table: the adaptation money, gone
    d.polygon([(x + 212, y + 54), (x + 266, y + 52), (x + 268, y + 77), (x + 214, y + 78)],
              fill=(245, 240, 224), outline=(120, 110, 92))
    text(x + 220, y + 55, "$120BN", SERB(10), (140, 26, 26))
    text(x + 220, y + 66, "ADAPTATION", SANB(6.5), INK)
    text(x + 220, y + 72.5, "DROPPED", SANB(7), RED)
    d.line([x + 219, y + 77, x + 252, y + 76], fill=RED, width=1)
    # a toppled chair on the floor, front left
    d.polygon([(x + 38, y + 71), (x + 52, y + 67), (x + 55, y + 75), (x + 41, y + 79)], fill=(24, 24, 30))
    d.line([x + 44, y + 71, x + 40, y + 63], fill=(24, 24, 30), width=2)
    d.line([x + 52, y + 69, x + 50, y + 61], fill=(24, 24, 30), width=2)
    # delegates leaving through both doors, briefcases in hand
    fig(22, 42, 42, (16, 16, 22), flip=-1, briefcase=True)
    fig(282, 40, 43, (22, 26, 38), flip=1, briefcase=True)
    # ---- foreground data strip, woven into the scene like the other mains
    d.rectangle([x, y + h - 13, x + w, y + h], fill=(13, 17, 15, 232))
    ctext(x + w / 2, y + h - 10.5, "44 HRS OVERTIME · NO DEAL · FIRST FAILURE SINCE 2009",
          SANB(8.5), (255, 244, 214))

def scene_bahrain(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 200, 218))  # the Gulf
    d.polygon([(x + w - 92, y), (x + w, y), (x + w, y + 44), (x + w - 40, y + 30)], fill=(226, 205, 160))  # Iran shore
    text(x + w - 44, y + 6, "IRAN", SANB(8.5), (120, 96, 40))
    d.polygon([(x, y + h - 20), (x + 74, y + h - 30), (x + 96, y + h), (x, y + h)], fill=(226, 205, 160))
    text(x + 8, y + h - 16, "SAUDI COAST", SAN(7), (120, 96, 40))
    # Bahrain island
    ix, iy = x + 128, y + 28
    d.ellipse([ix, iy, ix + 74, iy + 52], fill=(233, 214, 165), outline=(150, 128, 84))
    ctext(ix + 37, iy + 40, "BAHRAIN", SANB(8), (110, 88, 40))
    for (sx, sy, lab, ldx) in [(ix + 22, iy + 16, "AL-RIFFA", 9), (ix + 52, iy + 30, "AWALI", -34)]:
        d.polygon([(sx, sy - 6), (sx + 2, sy - 1.5), (sx + 6, sy), (sx + 2, sy + 1.5),
                   (sx, sy + 6), (sx - 2, sy + 1.5), (sx - 6, sy), (sx - 2, sy - 1.5)], fill=RED)
        text(sx + ldx, sy - 5, lab, SANB(7.5), (90, 20, 20))
    for (ex, ey) in [(x + w - 30, y + 16), (x + w - 58, y + 8)]:  # dashed strike arcs
        dashed((ex, ey), (ix + 40, iy + 18), RED, 2)
    text(x + w - 118, y + 22, "MISSILES + DRONES", SANB(7.5), (140, 30, 30))
    flame(ix + 88, iy + 46, 11)  # Sitra fire
    d.ellipse([ix + 92, iy + 20, ix + 116, iy + 34], fill=(120, 120, 120, 110))
    text(ix + 84, iy + 60, "SITRA FIRE — 2 HURT", SANB(7.5), (90, 40, 20))
    # Hormuz inset
    hx, hy, hw, hh = x + 8, y + 8, 118, 46
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(240, 246, 250), outline=NAVY)
    text(hx + 5, hy + 3, "STRAIT OF HORMUZ", SANB(7.5), NAVY)
    for tx in (hx + 14, hx + 62):
        d.polygon([(tx, hy + 32), (tx + 34, hy + 32), (tx + 29, hy + 38), (tx + 5, hy + 38)], fill=(60, 70, 84))
        d.rectangle([tx + 22, hy + 26, tx + 30, hy + 32], fill=(60, 70, 84))
    text(hx + 5, hy + 40 - 9, "TANKERS HIT, SAME NIGHT", SAN(6.5), MUT)
    d.rectangle([x, y + h - 15, x + w, y + h], fill=(20, 26, 40, 215))
    ctext(x + w / 2, y + h - 12.5, "2 PATRIOT RADARS CLAIMED DESTROYED — BAHRAIN DENIES", SANB(8.5), (255, 244, 214))

def main_panel(x, y, w, reg, head, scene_fn, caption, taglabel, tagcol):
    d.rectangle([x, y, x + w, y + 196], fill=PANEL, outline=(190, 180, 158))
    d.rectangle([x, y, x + w, y + 15], fill=REG[reg])
    text(x + 7, y + 2.5, REGNAME[reg], SANB(8.5), (255, 255, 255))
    twd = tw(taglabel, SANB(8)) + 10
    d.rounded_rectangle([x + w - twd - 5, y + 1.5, x + w - 5, y + 13.5], 5, fill=(255, 255, 255))
    text(x + w - twd, y + 3.5, taglabel, SANB(8), tagcol)
    yy = y + 19
    for ln in wrap(head, SERB(14.5), w - 14):
        text(x + 7, yy, ln, SERB(14.5), INK); yy += 17
    scene_fn(x + 5, y + 56, w - 10, 96)
    para(x + 7, y + 157, caption, SAN(9), w - 14, 11.5, INK, 3)

MW3 = (PW - 20) // 3
main_panel(MX, y, MW3, "EU",
           "KYIV: 186 DRONES IN — A BLOCK DESTROYED AT DYMER",
           scene_kyiv,
           "The air force counted 186 drones in, 161 downed, strikes at 18 locations. At Dymer a whole section of a five-storey block was destroyed: 3 dead, 14 unaccounted for.",
           "REPORTED", NAVY)
main_panel(MX + MW3 + 10, y, MW3, "EU",
           "COP31 COLLAPSES: 44 HOURS OF OVERTIME, NO DEAL",
           scene_cop31,
           "The closing plenary ran 44 hours into overtime — the longest COP ever — and still failed: the draft never named coal, oil or gas. “Unconscionable,” said O'Brien, for the EU.",
           "CONFIRMED", (46, 125, 79))
main_panel(MX + 2 * (MW3 + 10), y, MW3, "ME",
           "IRAN CLAIMS TWO US RADARS HIT IN BAHRAIN",
           scene_bahrain,
           "The IRGC says two Patriot radars were destroyed at Al-Riffa and Awali on Saturday night. Bahrain says its defences intercepted the attack; a civilian site at Sitra caught fire.",
           "CLAIM", RED)
y += 204

# ---------------------------------------------------------------- card scenes
def mini_ballot(x, y, w, h):
    d.rounded_rectangle([x + 12, y + 8, x + w - 12, y + 34], 3, outline=INK, width=2)
    d.rectangle([x + 20, y + 14, x + w - 20, y + 18], fill=INK)
    d.polygon([(x + 18, y + 2), (x + w - 18, y + 2), (x + w - 24, y + 12), (x + 24, y + 12)], fill=(240, 235, 220), outline=INK)
    ctext(x + w / 2, y + 40, "723", SERB(17), NAVY)
    ctext(x + w / 2, y + 60, "SEATS", SANB(7), MUT)

def mini_score(x, y, w, h):
    d.rectangle([x + 4, y + 6, x + w - 4, y + h - 6], fill=(24, 62, 40))
    ctext(x + w / 2, y + 10, "INDIA", SANB(8), (200, 230, 200))
    ctext(x + w / 2, y + 22, "720/9", SERB(16), (255, 255, 255))
    ctext(x + w / 2, y + 44, "DECLARED", SAN(7.5), (200, 230, 200))

def mini_f1(x, y, w, h):
    for r in range(3):
        for c in range(5):
            if (r + c) % 2 == 0:
                d.rectangle([x + 8 + c * 9, y + 6 + r * 9, x + 17 + c * 9, y + 15 + r * 9], fill=INK)
    d.polygon([(x + 8, y + 52), (x + 20, y + 44), (x + 38, y + 44), (x + 50, y + 52), (x + 50, y + 58), (x + 8, y + 58)], fill=RED)
    d.ellipse([x + 13, y + 54, x + 23, y + 64], fill=INK); d.ellipse([x + 36, y + 54, x + 46, y + 64], fill=INK)
    ctext(x + w / 2, y + 34, "P1", SANB(9), RED)

def mini_wemby(x, y, w, h):
    ctext(x + w / 2, y + 2, "50", SERB(27), NAVY)
    d.ellipse([x + 16, y + 40, x + w - 16, y + 48], outline=RED, width=2)
    for i in range(4):
        d.line([x + 19 + i * 6, y + 46, x + 22 + i * 4, y + 58], fill=MUT, width=1)
    ctext(x + w / 2, y + 60, "PTS", SANB(7.5), MUT)

def mini_ship(x, y, w, h):
    d.polygon([(x + 6, y + 40), (x + w - 8, y + 40), (x + w - 14, y + 50), (x + 12, y + 50)], fill=(60, 70, 84))
    d.rectangle([x + 16, y + 30, x + 30, y + 40], fill=(60, 70, 84))
    flame(x + 40, y + 22, 10)
    dashed((x + w - 6, y + 44), (x + w - 1, y + 44), NAVY, 2)
    ctext(x + w / 2, y + 54, "TOWED OUT", SANB(7), NAVY)

def mini_board(x, y, w, h):
    d.rectangle([x + 5, y + 6, x + w - 5, y + h - 8], fill=(22, 26, 34))
    text(x + 9, y + 9, "MONDAY", SANB(8), (250, 200, 90))
    for i in range(3):
        yy = y + 24 + i * 13
        d.line([x + 10, yy + 3, x + 34, yy + 3], fill=(150, 160, 175), width=2)
        text(x + 38, yy - 3, "✗", SANB(10), RED)

def mini_hosp(x, y, w, h):
    d.ellipse([x + 14, y + 4, x + w - 14, y + 34], fill=RED)
    d.rectangle([x + w / 2 - 3, y + 10, x + w / 2 + 3, y + 28], fill=(255, 255, 255))
    d.rectangle([x + w / 2 - 9, y + 16, x + w / 2 + 9, y + 22], fill=(255, 255, 255))
    pts = [(x + 6, y + 52), (x + 18, y + 52), (x + 24, y + 42), (x + 31, y + 60), (x + 37, y + 52), (x + w - 6, y + 52)]
    d.line(pts, fill=(46, 125, 79), width=2)
    ctext(x + w / 2, y + 62, "ICU · DAY 3", SANB(7), MUT)

def mini_bottles(x, y, w, h):
    for i, bx in enumerate([x + 10, x + 24, x + 38]):
        d.rectangle([bx, y + 14, bx + 9, y + 44], fill=(90, 70, 40) if i != 1 else (60, 60, 60))
        d.rectangle([bx + 2, y + 8, bx + 7, y + 14], fill=INK)
    d.polygon([(x + w / 2, y + 46), (x + w / 2 + 11, y + 64), (x + w / 2 - 11, y + 64)], outline=RED, width=2)
    ctext(x + w / 2, y + 52, "!", SANB(11), RED)

def mini_factory(x, y, w, h):
    d.polygon([(x + 6, y + 34), (x + 18, y + 24), (x + 30, y + 34), (x + 42, y + 24), (x + 52, y + 34),
               (x + 52, y + 54), (x + 6, y + 54)], fill=(70, 66, 60))
    d.rectangle([x + 44, y + 8, x + 50, y + 26], fill=(70, 66, 60))
    flame(x + 24, y + 14, 11)
    ctext(x + w / 2, y + 57, "34 MISSING", SANB(7.5), RED)

def mini_quake(x, y, w, h):
    d.polygon([(x + 4, y + 40), (x + 22, y + 12), (x + 34, y + 28), (x + 44, y + 16), (x + w - 4, y + 40)], fill=(120, 104, 84))
    d.line([(x + 24, y + 20), (x + 20, y + 30), (x + 27, y + 38), (x + 23, y + 48)], fill=RED, width=2)
    ctext(x + w / 2, y + 50, "853 HOMELESS", SANB(7.5), (122, 74, 33))

def mini_trophy(x, y, w, h):
    d.polygon([(x + 18, y + 8), (x + w - 18, y + 8), (x + w - 24, y + 30), (x + 24, y + 30)], fill=GOLD)
    d.arc([x + 8, y + 10, x + 22, y + 28], 90, 270, fill=GOLD, width=3)
    d.arc([x + w - 22, y + 10, x + w - 8, y + 28], 270, 90, fill=GOLD, width=3)
    d.rectangle([x + w / 2 - 3, y + 30, x + w / 2 + 3, y + 40], fill=GOLD)
    d.rectangle([x + w / 2 - 11, y + 40, x + w / 2 + 11, y + 45], fill=GOLD)
    ctext(x + w / 2, y + 50, "6-2 · 7-6(7)", SANB(8.5), NAVY)

def mini_liv(x, y, w, h):
    ctext(x + w / 2, y + 6, "4–0", SERB(23), RED)
    d.rectangle([x + w / 2 - 6, y + 42, x + w / 2 + 6, y + 58], fill=(214, 40, 40))
    ctext(x + w / 2, y + 61, "RED CARD 8'", SANB(6.5), MUT)

CARDS = [
    ("AP", "HONG KONG VOTES", "856 candidates for 723 Election Committee seats; turnout 98.79% — 5,640 ballots, polls 09:00–18:00.", "CONFIRMED", (46, 125, 79), mini_ballot),
    ("OC", "INDIA'S RECORD 720/9 AT WELLINGTON", "Rahul 136, Pant 128, Gill 98 — highest Test total in NZ. NZ 368 & 119/2, trail by 233.", "CONFIRMED", (46, 125, 79), mini_score),
    ("AM", "VERSTAPPEN FROM POLE IN LAS VEGAS", "1:27:39.624 — Norris +0.639, Piastri +1.529 from 17th. 35 lead changes; his 75th win.", "CONFIRMED", (46, 125, 79), mini_f1),
    ("AM", "WEMBANYAMA'S 50-POINT NIGHT", "50 pts (32 in the 1st half), 19 reb, 5 blk, 4 stl. Spurs 114–91 Pelicans — first 50-15-5-4 game.", "CONFIRMED", (46, 125, 79), mini_wemby),
    ("EU", "SPARTA II TOWED CLEAR OF FINLAND", "Seven vessels (3 FI, 2 EE, 2 RU) fought the fire; 16 crew safe; Murman tows her out.", "REPORTED", NAVY, mini_ship),
    ("EU", "BELGIUM'S SKIES CLOSE MONDAY", "ATC strike: Brussels & Charleroi cancel every Monday flight, 07:00–21:00. Announced Sunday.", "CONFIRMED", (46, 125, 79), mini_board),
    ("AM", "BOLSONARO IN INTENSIVE CARE, DAY 3", "Acute bowel obstruction; stable and conscious in Brasília. Sunday's decision: surgery or not.", "REPORTED", NAVY, mini_hosp),
    ("AP", "MANIPUR LIQUOR TOLL: 19 REPORTED", "Official toll 17; ~600 hospitalised, 6 arrested. Methanol suspected, not yet confirmed.", "REPORTED", NAVY, mini_bottles),
    ("AP", "CIKANDE: 34 STILL MISSING", "Candy-factory fire: 3 dead; 24 body bags recovered, toll unconfirmed. Search suspended 18:00.", "REPORTED", NAVY, mini_factory),
    ("AM", "PERU QUAKE TOLL PUBLISHED", "INDECI's running assessment of Friday's Junín quake: 1 dead, 16 injured, 853 homeless.", "REPORTED", NAVY, mini_quake),
    ("EU", "ALCARAZ TAKES THE ATP FINALS", "6-2, 7-6(7) over world No.1 Zverev in Turin — first Finals title; 4th man with Slam + Finals set.", "CONFIRMED", (46, 125, 79), mini_trophy),
    ("EU", "LIVERPOOL 4–0 MANCHESTER UNITED", "Yoro off 8'; Szoboszlai 10', Wirtz 13', Ngumoha 66', Muñoz 82'. Pochettino's debut.", "CONFIRMED", (46, 125, 79), mini_liv),
]

CW4 = (PW - 24) // 4
CH = 72
for idx, (reg, head, body, taglabel, tagcol, scene_fn) in enumerate(CARDS):
    cx = MX + (idx % 4) * (CW4 + 8)
    cy = y + (idx // 4) * (CH + 6)
    d.rectangle([cx, cy, cx + CW4, cy + CH], fill=PANEL, outline=(190, 180, 158))
    d.rectangle([cx, cy, cx + 56, cy + CH], fill=(238, 231, 214))
    scene_fn(cx, cy, 56, CH)
    d.rectangle([cx, cy, cx + CW4, cy + 3], fill=REG[reg])
    tx = cx + 62
    yy = cy + 7
    for ln in wrap(head, SERB(10.5), CW4 - 68):
        text(tx, yy, ln, SERB(10.5), INK); yy += 13
    para(tx, yy + 1, body, SAN(8.5), CW4 - 68, 10.5, (52, 48, 42), 3)
    twd = tw(taglabel, SANB(7)) + 8
    d.rounded_rectangle([cx + CW4 - twd - 4, cy + CH - 14, cx + CW4 - 4, cy + CH - 3], 4, outline=tagcol)
    text(cx + CW4 - twd, cy + CH - 12, taglabel, SANB(7), tagcol)
y += 3 * CH + 2 * 6 + 8

# ---------------------------------------------------------------- bottom split
text(MX, y, "WHERE IT HAPPENED — THE DAY ON THE MAP", SANB(11), NAVY)
text(468, y, "ALSO SUNDAY — 23 MORE STORIES, EVERY ONE SOURCED", SANB(11), RED)
y += 16
MAPX, MAPY, MAPW, MAPH = MX, y, 424, 150
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], fill=(213, 225, 235), outline=(150, 140, 118))

def proj(lon, lat):
    return (MAPX + (lon + 180) / 360 * MAPW, MAPY + (75 - lat) / 135 * MAPH)

LAND = (233, 223, 197)
def landmass(pts):
    d.polygon([proj(lon, lat) for lon, lat in pts], fill=LAND, outline=(168, 156, 126))

landmass([(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66), (-80, 73), (-75, 62), (-65, 60), (-55, 52), (-65, 45), (-70, 42), (-76, 35), (-80, 32), (-80, 26), (-84, 22), (-90, 20), (-97, 16), (-94, 17), (-86, 13), (-79, 9), (-85, 11), (-95, 16), (-105, 20), (-114, 28), (-122, 37), (-124, 46), (-130, 54), (-145, 60), (-166, 60)])
landmass([(-79, 9), (-70, 12), (-62, 10), (-55, 6), (-50, 0), (-44, -3), (-35, -8), (-39, -13), (-41, -22), (-48, -27), (-52, -33), (-58, -38), (-62, -41), (-67, -50), (-71, -54), (-73, -44), (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 1)])
landmass([(-9, 37), (-9, 43), (-2, 44), (-5, 48), (-1, 50), (3, 51), (7, 54), (8, 57), (18, 56), (21, 59), (25, 60), (25, 66), (30, 70), (50, 69), (70, 70), (90, 70), (110, 70), (130, 71), (150, 70), (170, 68), (178, 66), (162, 60), (158, 55), (145, 50), (142, 45), (135, 40), (130, 38), (122, 38), (120, 32), (115, 25), (110, 20), (108, 15), (106, 9), (103, 6), (100, 8), (98, 13), (92, 20), (89, 22), (86, 20), (80, 13), (77, 8), (75, 13), (72, 20), (66, 25), (57, 27), (52, 28), (49, 30), (50, 26), (56, 27), (59, 22), (55, 17), (52, 15), (45, 12), (43, 12), (39, 20), (37, 24), (35, 29), (34, 31), (36, 36), (30, 36), (27, 37), (23, 36), (20, 40), (16, 38), (12, 44), (10, 44), (7, 44), (3, 43), (0, 39), (-2, 37), (-6, 36)])
landmass([(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (34, 28), (38, 20), (40, 15), (43, 12), (48, 11), (51, 12), (48, 5), (42, -2), (40, -8), (40, -15), (36, -22), (33, -27), (30, -31), (25, -34), (20, -35), (17, -32), (15, -27), (13, -20), (12, -15), (9, -5), (9, 0), (6, 4), (0, 5), (-8, 5), (-13, 8), (-17, 12), (-17, 15), (-16, 20), (-15, 25), (-13, 28), (-9, 31)])
landmass([(113, -22), (115, -34), (124, -33), (132, -32), (135, -35), (139, -37), (145, -38), (150, -37), (153, -30), (153, -25), (149, -15), (146, -12), (142, -11), (142, -17), (139, -25), (136, -15), (132, -11), (126, -14), (118, -20)])
landmass([(95, 5), (100, 0), (106, -6), (102, -4), (97, 2)])
landmass([(109, 1), (113, 4), (117, 6), (119, 2), (117, -2), (113, -3), (110, -2)])
landmass([(106, -6), (110, -7), (114, -8), (114, -9), (106, -8)])
landmass([(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (141, -8), (136, -4), (132, -3)])
landmass([(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44), (140, 43), (138, 38), (135, 34), (131, 32)])
landmass([(-5, 50), (-3, 53), (-5, 55), (-3, 58), (-1, 57), (0, 53), (1, 51)])
landmass([(167, -45), (170, -43), (172, -41), (174, -39), (176, -38), (174, -41), (172, -43), (169, -46)])
landmass([(44, -16), (47, -15), (50, -18), (48, -22), (45, -25), (44, -22), (43, -18)])

PINS = [
    (1, 30.5, 50.4, "EU", 4, 0), (2, 30.7, 36.9, "EU", 2, 5), (3, 50.6, 26.2, "ME", 0, 0),
    (4, 114.2, 22.3, "AP", 0, 0), (5, 174.8, -41.3, "OC", 0, 0), (6, -115.1, 36.2, "AM", 0, 0),
    (7, -98.5, 29.4, "AM", 0, 0), (8, 27.5, 59.8, "EU", 3, -4), (9, 4.35, 50.85, "EU", 5, 2),
    (10, -47.9, -15.8, "AM", 0, 0), (11, 93.9, 24.8, "AP", 0, 0), (12, 106.3, -6.2, "AP", 0, 0),
    (13, -75.2, -11.5, "AM", 0, 0), (14, 7.7, 45.1, "EU", 2, 6), (15, -3.0, 53.4, "EU", -4, -3),
    (16, 20.1, 32.1, "AF", 0, 0), (17, 32.5, 15.6, "AF", 0, 0),
]
for num, lon, lat, reg, nx, ny in PINS:
    px, py = proj(lon, lat)
    px += nx; py += ny
    d.ellipse([px - 6.5, py - 6.5, px + 6.5, py + 6.5], fill=REG[reg], outline=(255, 255, 255), width=1)
    d.text((px, py - 4.5), str(num), font=SANB(7.5), fill=(255, 255, 255), anchor="ma")

legend = ("1 Kyiv · 2 Antalya · 3 Bahrain · 4 Hong Kong · 5 Wellington · 6 Las Vegas · 7 San Antonio · "
          "8 Gulf of Finland · 9 Brussels · 10 Brasília · 11 Manipur · 12 Cikande · 13 Junín · 14 Turin · "
          "15 Liverpool · 16 Benghazi · 17 Khartoum")
para(MAPX, MAPY + MAPH + 6, legend, SAN(8), MAPW, 10.5, MUT)

ALSO = [
    ("EU", "Márquez wins his 8th MotoGP title in Portugal, passing Rossi's record (Euronews)"),
    ("EU", "Pope Leo XIV lunches with 1,300 poor guests for the World Day of the Poor (Vatican News)"),
    ("ME", "Tehran starts rolling power cuts, up to 2 hours a day (Reuters)"),
    ("ME", "Araghchi: the Islamabad MOU is “no longer on the table” (Iran newspaper via CNBC)"),
    ("ME", "Eisenkot's Yashar and Likud open marathon coalition talks in Herzliya (AFP)"),
    ("ME", "Hamas seeks urgent mediators' meeting after strike kills 3 soup-kitchen workers (MEM)"),
    ("ME", "Fire at Hartha power station near Basra kills at least 4, injures 35 (Al Jazeera)"),
    ("ME", "Suspected settlers torch 12 vehicles in four West Bank villages (Reuters)"),
    ("AM", "FBI probes apparent NCIC database hack; Washington pauses gun checks (AP)"),
    ("AM", "Delta outage delays 1,600+ flights; Atlanta ground stop lifted by afternoon (WSJ)"),
    ("AM", "Mexico captures cartel boss “El Chapo Isidro” in Sinaloa; 11 killed (AP)"),
    ("AM", "Pentagon memo curbs US–Canada defence ties, Post reports (Washington Post)"),
    ("AP", "Nepal PM Balendra Shah lands in New Delhi; Modi talks Monday (Nepal MoFA)"),
    ("AP", "M5.6 quake deep in the Celebes Sea off Sarangani; no damage (PHIVOLCS)"),
    ("AP", "Lahore again the world's most polluted big city: AQI 538 (Dawn)"),
    ("AP", "Okinawa celebrates Shuri Castle's restored main hall (AP)"),
    ("AF", "Russian corvette Merkury capsizes at Benghazi after suspected drone hit (Reuters)"),
    ("AF", "Bayelsa funeral-boat death toll rises to 29 (Channels TV)"),
    ("AF", "Ethiopia launches polio drive for 11.3 million children (PANA)"),
    ("AF", "Dawn drone strikes hit Khartoum; UN facility damaged, 3 dead in Omdurman (AP)"),
    ("OC", "Thirty 1956 Olympians reunite at the MCG, 70 years on (ABC)"),
    ("W",  "Bitcoin holds above $60,000 after Saturday's $55.1k flush; $1.8bn liquidated (CoinGecko)"),
    ("W",  "Gold steadies near $3,540, a 14-month low, after Friday's 3.1% rout (Reuters)"),
]
ax = 468
ay = y + 2
for i, (reg, line) in enumerate(ALSO):
    yy = ay + i * 9.4
    d.rectangle([ax, yy + 1, ax + 7, yy + 8], fill=REG[reg])
    text(ax + 12, yy, f"{i + 1}.", SANB(9), REG[reg])
    text(ax + 32, yy, line, SAN(9), (43, 39, 33))
y = ay + len(ALSO) * 9.4 + 8

# ---------------------------------------------------------------- date check + footer
d.rectangle([MX, y, W - MX, y + 40], fill=(238, 231, 214), outline=(190, 180, 158))
text(MX + 8, y + 5, "DATE CHECK", SANB(9.5), RED)
DC = ("Famous, but NOT Sunday — so not counted above: Sparta II was hit on Saturday (Sunday's news was the firefight and the tow) · "
      "the Cikande fire broke out Saturday 17:00 · Trump said “permanent deal” to Fox News on Saturday · Cricket Australia backed captain "
      "Cummins on Saturday · BepiColombo reached Mercury's orbit on Saturday · Bitcoin's $55.1k low was Saturday — on Sunday it held $60k.")
para(MX + 76, y + 4.5, DC, SAN(9), PW - 88, 11.5, (52, 48, 42), 3)
y += 46
para(MX, y,
     "SOURCES — Reuters · AP · AFP · Al Jazeera · BBC · WSJ · CNN · Euronews · Dawn · PANA · Channels TV · ABC · Vatican News · PHIVOLCS · INDECI · Nepal MoFA · Middle East Monitor · CoinGecko · FlightAware · ATP · Sky Sports",
     SAN(7.5), PW, 9.5, MUT, 1)
para(MX, y + 10,
     "CERTAINTY — CONFIRMED: agreed by the wires · REPORTED: official or single-agency figures · CLAIM: asserted, and denied or unproven · Checked against the wires on Sunday night, 22 November 2026.",
     SAN(7.5), PW, 9.5, MUT, 1)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out)
img.resize((300, 300), Image.LANCZOS).save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry-300.png"))
print("saved", out, os.path.getsize(out), "bytes")
