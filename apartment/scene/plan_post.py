"""Overlay architectural walls, windows and door swings on the orthographic plan render."""
import sys, math
from PIL import Image, ImageDraw

src, dst = sys.argv[1], sys.argv[2]
base = Image.open(src).convert("RGB")
W, H = base.size
S = 2
img = base.resize((W * S, H * S), Image.LANCZOS)
d = ImageDraw.Draw(img)


def P(x, y):
    return ((x + 0.30) / 4.5 * W * S, (8.55 - y) / 9.0 * H * S)


def rect(x0, x1, y0, y1, fill, outline=None, w=0):
    a, b = P(x0, y1), P(x1, y0)
    d.rectangle([a[0], a[1], b[0], b[1]], fill=fill, outline=outline, width=w)


WALL = (46, 52, 48)
for r in ((-0.25, 0, -0.25, 8.35), (-0.25, 0.30, 8.10, 8.35), (3.60, 4.15, 8.10, 8.35),
          (3.90, 4.15, -0.25, 4.75), (3.90, 4.15, 5.40, 5.60), (3.90, 4.15, 6.25, 8.35),
          (-0.25, 2.69, -0.25, 0), (3.59, 4.15, -0.25, 0), (3.60, 3.90, 6.90, 7.20),
          (0, 2.16, 1.84, 1.96), (2.04, 2.16, 0, 0.15), (2.04, 2.16, 0.78, 1.16), (1.24, 2.16, 1.04, 1.16),
          (1.24, 1.36, 1.16, 1.84)):
    rect(*r, WALL)
# chimney (hatched) and closed pocket
rect(0, 0.40, 1.96, 2.26, (120, 126, 122))
rect(0.40, 0.70, 1.96, 2.26, (236, 233, 227), WALL, 3)
a, b = P(0.40, 2.26), P(0.70, 1.96)
for i in range(-6, 7):
    t = i / 6
    d.line([(a[0] + (b[0] - a[0]) * max(0, t), a[1] + (b[1] - a[1]) * max(0, -t)),
            (a[0] + (b[0] - a[0]) * min(1, 1 + t), a[1] + (b[1] - a[1]) * min(1, 1 - t))], fill=WALL, width=2)
# windows: frame + glass lines in the wall thickness
GLASS = (250, 250, 248)


def win_h(x0, x1, y0, y1):
    rect(x0, x1, y0, y1, GLASS, WALL, 3)
    for f in (0.42, 0.58):
        yy = y0 + (y1 - y0) * f
        d.line([P(x0, yy), P(x1, yy)], fill=WALL, width=2)


def win_v(x0, x1, y0, y1):
    rect(x0, x1, y0, y1, GLASS, WALL, 3)
    for f in (0.42, 0.58):
        xx = x0 + (x1 - x0) * f
        d.line([P(xx, y0), P(xx, y1)], fill=WALL, width=2)


win_h(0.30, 3.60, 8.10, 8.35)
for i in range(1, 5):
    x = 0.30 + i * 0.66
    d.line([P(x, 8.10), P(x, 8.35)], fill=WALL, width=2)
win_v(3.90, 4.15, 4.75, 5.40)
win_v(3.90, 4.15, 5.60, 6.25)
# door swings
ARC = (60, 66, 62)


def arc(cx, cy, r, a0, a1):
    x0, y0 = P(cx - r, cy + r)
    x1, y1 = P(cx + r, cy - r)
    d.arc([x0, y0, x1, y1], a0, a1, fill=ARC, width=3)


arc(3.59, 0.0, 0.90, 180, 270)   # B1: from west (closed) to north (open), PIL angles clockwise from +x on screen
d.line([P(3.59, 0.0), P(3.59, 0.90)], fill=ARC, width=4)
arc(2.10, 0.15, 0.63, 180, 270)
d.line([P(2.10, 0.15), P(1.47, 0.15)], fill=ARC, width=4)
out = img.resize((W, H), Image.LANCZOS)
out.save(dst, quality=92)
print("plan ok", dst)
