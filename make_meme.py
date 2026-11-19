#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme: a GTA 'WASTED' death-screen parody.

Joke: after 13 years of waiting, GTA 6 is finally out -- and the player is
already WASTED, still stuck on the download. The make.fun ghost stands in
the scene as the one character who did NOT waste its time: it already got
paid on make.fun while the download runs. The ghost mark is the real press
asset (mark-1024.png), pasted large at the bottom right; the make.fun name
is drawn big at the bottom left, so the brand is unmissable at 480 px.

Output: meme.png, 1024x1024, square.
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
GHOST_PATH = "/tmp/mark-1024.png"

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_text_center(draw, cx, y, text, font, fill, stroke=0):
    """Draw text centred on cx, top at y. Returns its bounding box."""
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    w = bbox[2] - bbox[0]
    draw.text((cx - w / 2 - bbox[0], y - bbox[1]), text, font=font,
              fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    return (cx - w / 2, y, cx + w / 2, y + (bbox[3] - bbox[1]))


def draw_palm(draw, base_x, base_y, top_x, top_y, lean, size):
    """A simple black palm silhouette: curved trunk + drooping fronds."""
    dark = (16, 5, 30)
    # Trunk: quadratic curve from base to top, drawn as thick segments.
    pts = []
    steps = 24
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * base_x + 2 * (1 - t) * t * (base_x + lean) + t ** 2 * top_x
        y = (1 - t) ** 2 * base_y + 2 * (1 - t) * t * (base_y - (base_y - top_y) * 0.55) + t ** 2 * top_y
        pts.append((x, y))
    draw.line(pts, fill=dark, width=22, joint="curve")
    # Fronds: arcs drooping out from the crown.
    crown = (top_x, top_y)
    for angle_deg in (-160, -130, -100, -70, -40, -10, 20):
        a = math.radians(angle_deg)
        tip = (crown[0] + math.cos(a) * size, crown[1] + math.sin(a) * size * 0.55 + size * 0.45)
        mid = (crown[0] + math.cos(a) * size * 0.55, crown[1] + math.sin(a) * size * 0.30 - size * 0.08)
        curve = []
        for i in range(13):
            t = i / 12
            x = (1 - t) ** 2 * crown[0] + 2 * (1 - t) * t * mid[0] + t ** 2 * tip[0]
            y = (1 - t) ** 2 * crown[1] + 2 * (1 - t) * t * mid[1] + t ** 2 * tip[1]
            curve.append((x, y))
        draw.line(curve, fill=dark, width=13, joint="curve")


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # --- Vice City sunset sky: deep purple -> magenta -> orange. ---
    sky_stops = [
        (0.00, (24, 6, 58)),
        (0.35, (92, 18, 108)),
        (0.60, (198, 38, 118)),
        (0.80, (255, 110, 58)),
        (1.00, (255, 178, 96)),
    ]
    horizon = 800
    for y in range(horizon):
        t = y / horizon
        for i in range(len(sky_stops) - 1):
            t0, c0 = sky_stops[i]
            t1, c1 = sky_stops[i + 1]
            if t0 <= t <= t1:
                col = lerp(c0, c1, (t - t0) / (t1 - t0))
                break
        draw.line([(0, y), (W, y)], fill=col)

    # --- Retro sun with horizontal slits, low in the sky. ---
    # Drawn as horizontal slices of the circle, skipping slit rows, so the
    # gaps show the sky gradient through them.
    sun_cx, sun_cy, sun_r = 512, 300, 128
    slits = [(330, 336), (352, 360), (378, 388), (408, 420)]
    y = sun_cy - sun_r
    while y < sun_cy + sun_r:
        step = 4
        y1 = min(y + step, sun_cy + sun_r)
        if not any(s0 <= y < s1 for s0, s1 in slits):
            dy = (y + y1) / 2 - sun_cy
            hw = math.sqrt(max(0, sun_r * sun_r - dy * dy))
            draw.rectangle([sun_cx - hw, y, sun_cx + hw, y1],
                           fill=(255, 206, 84))
        y = y1

    # --- Horizon glow + dark ground (street / beach at night). ---
    draw.rectangle([0, horizon - 4, W, horizon + 4], fill=(255, 140, 70))
    draw.rectangle([0, horizon + 4, W, H], fill=(18, 7, 34))
    # No reflection streaks: the dark ground stays clean so the pitch line
    # and the make.fun name read without anything behind them.
    img = img.convert("RGBA")
    draw = ImageDraw.Draw(img)

    # --- Palm silhouettes framing the scene. ---
    draw_palm(draw, 95, 830, 55, 330, -40, 210)
    draw_palm(draw, 945, 840, 985, 370, 45, 200)

    # --- Top line: set the scene, GTA 6 launch day. ---
    top_font = load_font(52)
    draw_text_center(draw, 512, 52, "GTA 6 LAUNCH DAY", top_font,
                     (255, 255, 255), stroke=3)

    # --- The WASTED death screen, dead centre. ---
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(band)
    bdraw.rectangle([0, 428, W, 592], fill=(0, 0, 0, 150))
    img = Image.alpha_composite(img, band)
    draw = ImageDraw.Draw(img)
    # Letter-spaced WASTED, auto-fitted so it spans the frame like the
    # game's screen but never runs off the edges.
    word = "WASTED"
    gap = 10
    size = 210
    while size > 60:
        f = load_font(size)
        widths = []
        total = 0
        for ch in word:
            bb = draw.textbbox((0, 0), ch, font=f, stroke_width=8)
            wch = bb[2] - bb[0]
            widths.append(wch)
            total += wch
        total += gap * (len(word) - 1)
        if total <= 940:
            break
        size -= 6
    wasted_font = load_font(size)
    x = (W - total) / 2
    y = 436
    for ch, wch in zip(word, widths):
        draw.text((x, y), ch, font=wasted_font, fill=(172, 172, 172),
                  stroke_width=8, stroke_fill=(0, 0, 0))
        x += wch + gap

    # --- The punchline, two big lines under WASTED. ---
    joke_font = load_font(68)
    draw_text_center(draw, 512, 622, "13 YEARS WAITING.", joke_font,
                     (255, 255, 255), stroke=4)
    draw_text_center(draw, 512, 706, "STILL DOWNLOADING.", joke_font,
                     (255, 255, 255), stroke=4)

    # --- make.fun ghost, large in the scene, bottom right. ---
    if not os.path.exists(GHOST_PATH):
        print(f"ghost asset missing: {GHOST_PATH}", file=sys.stderr)
        sys.exit(1)
    ghost = Image.open(GHOST_PATH).convert("RGBA")
    ghost = ghost.resize((240, 240), Image.LANCZOS)
    img.paste(ghost, (764, 784), ghost)

    # --- Bottom-left: the pitch + the make.fun name. ---
    pitch_font = load_font(38)
    draw.text((44, 838), "MY AGENT ALREADY GOT PAID", font=pitch_font,
              fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    name_font = load_font(80)
    # "make.fun" with a magenta dot, drawn in three parts.
    x0, y0 = 44, 900
    draw.text((x0, y0), "make", font=name_font, fill=(255, 255, 255),
              stroke_width=4, stroke_fill=(0, 0, 0))
    w_make = draw.textbbox((0, 0), "make", font=name_font,
                           stroke_width=4)[2]
    draw.text((x0 + w_make, y0), ".", font=name_font, fill=(230, 0, 150),
              stroke_width=4, stroke_fill=(0, 0, 0))
    w_dot = draw.textbbox((0, 0), ".", font=name_font,
                          stroke_width=4)[2]
    draw.text((x0 + w_make + w_dot, y0), "fun", font=name_font,
              fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))

    out = os.path.join(HERE, "meme.png")
    img.convert("RGB").save(out, "PNG")
    print(f"wrote {out} {img.size}")


if __name__ == "__main__":
    main()
