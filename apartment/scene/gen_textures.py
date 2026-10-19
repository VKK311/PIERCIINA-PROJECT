"""Procedural textures for the apartment scene (wallpaper, bedding, rug, TV image)."""
import math, random, os, sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

OUT = sys.argv[1] if len(sys.argv) > 1 else "tex"
os.makedirs(OUT, exist_ok=True)


def leaf_poly(cx, cy, length, width, ang, n=14):
    """Pointed leaf outline starting at (cx,cy) pointing along ang."""
    pts_l, pts_r = [], []
    ca, sa = math.cos(ang), math.sin(ang)
    for i in range(n + 1):
        t = i / n
        w = width * math.sin(math.pi * t) ** 0.85 * (1 - 0.25 * t)
        ax, ay = t * length, 0
        for side, arr in ((1, pts_l), (-1, pts_r)):
            px, py = ax, side * w / 2
            arr.append((cx + px * ca - py * sa, cy + px * sa + py * ca))
    return pts_l + pts_r[::-1]


def bez(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]


def sprig(d, r, x, y, scale, leaf_cols, stem_col, blossom=None, stem_w=3):
    ang = r.uniform(0, 2 * math.pi)
    L = scale * r.uniform(0.8, 1.2)
    bend = r.uniform(-0.5, 0.5)
    p0 = (x, y)
    p2 = (x + L * math.cos(ang), y + L * math.sin(ang))
    p1 = ((p0[0] + p2[0]) / 2 + bend * L * math.cos(ang + math.pi / 2) * 0.5,
          (p0[1] + p2[1]) / 2 + bend * L * math.sin(ang + math.pi / 2) * 0.5)
    pts = bez(p0, p1, p2)
    d.line(pts, fill=stem_col, width=stem_w)
    nleaf = r.randint(5, 9)
    for i in range(1, nleaf + 1):
        t = i / (nleaf + 1)
        k = int(t * (len(pts) - 1))
        (ax, ay), (bx, by) = pts[k], pts[min(k + 1, len(pts) - 1)]
        da = math.atan2(by - ay, bx - ax)
        side = 1 if i % 2 else -1
        la = da + side * r.uniform(0.6, 1.0)
        ll = scale * r.uniform(0.22, 0.34) * (1.1 - 0.4 * t)
        d.polygon(leaf_poly(ax, ay, ll, ll * r.uniform(0.32, 0.45), la), fill=r.choice(leaf_cols))
    tip = pts[-1]
    d.polygon(leaf_poly(tip[0], tip[1], scale * 0.25, scale * 0.1, ang + bend * 0.5), fill=r.choice(leaf_cols))
    if blossom:
        for _ in range(r.randint(0, 2)):
            k = r.randint(4, len(pts) - 1)
            bx, by = pts[k]
            rr = scale * 0.045
            for p in range(5):
                a = p * 2 * math.pi / 5
                d.ellipse([bx + math.cos(a) * rr - rr * 0.8, by + math.sin(a) * rr - rr * 0.8,
                           bx + math.cos(a) * rr + rr * 0.8, by + math.sin(a) * rr + rr * 0.8], fill=blossom)
            d.ellipse([bx - rr * 0.5, by - rr * 0.5, bx + rr * 0.5, by + rr * 0.5], fill=(214, 180, 120))


def tiled_pattern(size, bg, n, scale, leaf_cols, stem_col, blossom, seed, stem_w):
    S = size * 2  # supersample
    img = Image.new("RGB", (S, S), bg)
    d = ImageDraw.Draw(img)
    r = random.Random(seed)
    for _ in range(n):
        x, y = r.uniform(0, S), r.uniform(0, S)
        st = r.getstate()
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                r.setstate(st)
                sprig(d, r, x + ox, y + oy, scale * 2, leaf_cols, stem_col, blossom, stem_w)
    return img.resize((size, size), Image.LANCZOS)


# Botanical wallpaper: soft sage leaves on warm white (concept wallpaper).
wp = tiled_pattern(2048, (238, 233, 224), 38, 230,
                   [(160, 176, 156), (139, 158, 136), (181, 193, 175), (122, 141, 121)],
                   (128, 146, 124), (221, 178, 168), 11, 4)
wp.save(f"{OUT}/wallpaper.png")

# Bedding: white botanical on near-black, like the HEMNES display set.
bd = tiled_pattern(2048, (29, 33, 31), 46, 210,
                   [(232, 230, 224), (206, 208, 200), (245, 244, 240)],
                   (225, 224, 218), None, 23, 3)
bd.save(f"{OUT}/bedding.png")

# Vintage rug 2.0 x 2.5 m in faded rose / sage / sand.
W, H = 1600, 2000
rng = np.random.default_rng(5)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
base = np.array([214, 196, 176], np.float32)
img = np.ones((H, W, 3), np.float32) * base
rose = np.array([196, 140, 128], np.float32)
sage = np.array([139, 156, 136], np.float32)
deep = np.array([108, 92, 86], np.float32)
cream = np.array([236, 226, 210], np.float32)


def band(m, inset, width, col, a=1.0):
    inner = (xx > inset) & (xx < W - inset) & (yy > inset) & (yy < H - inset)
    inner2 = (xx > inset + width) & (xx < W - inset - width) & (yy > inset + width) & (yy < H - inset - width)
    sel = inner & ~inner2
    m[sel] = m[sel] * (1 - a) + col * a


band(img, 0, 40, deep)
band(img, 40, 70, rose)
band(img, 110, 14, cream)
band(img, 124, 60, sage)
band(img, 184, 14, cream)
# border motif: small diamonds in the rose band
for cx in range(55, W, 70):
    for cy in (75, H - 75):
        sel = (np.abs(xx - cx) + np.abs(yy - cy)) < 22
        img[sel] = cream
for cy in range(55, H, 70):
    for cx in (75, W - 75):
        sel = (np.abs(xx - cx) + np.abs(yy - cy)) < 22
        img[sel] = cream
# field lattice
field = (xx > 198) & (xx < W - 198) & (yy > 198) & (yy < H - 198)
u = (xx - W / 2) / 120.0
v = (yy - H / 2) / 120.0
lat = (np.abs(((u + v) % 2) - 1) < 0.07) | (np.abs(((u - v) % 2) - 1) < 0.07)
img[field & lat] = img[field & lat] * 0.35 + rose * 0.65
cell = (np.abs(((u + v + 1) % 2) - 1) + np.abs(((u - v + 1) % 2) - 1))
flower = field & (cell < 0.35)
img[flower] = img[flower] * 0.3 + sage * 0.7
center = field & (np.abs((xx - W / 2) / 420) + np.abs((yy - H / 2) / 560) < 1) & (np.abs((xx - W / 2) / 420) + np.abs((yy - H / 2) / 560) > 0.93)
img[center] = deep
med = (np.abs((xx - W / 2) / 300) + np.abs((yy - H / 2) / 400) < 1)
img[med] = img[med] * 0.55 + rose * 0.45
# wear / abrash
noise = rng.normal(0, 1, (H // 8, W // 8)).astype(np.float32)
noise = np.array(Image.fromarray(((noise * 30) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 128 - 1
streak = np.array(Image.fromarray((rng.normal(128, 30, (H // 40, 1))).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 128 - 1
img = img * (1 + 0.06 * noise[..., None] + 0.05 * streak[..., None])
grain = rng.normal(0, 7, (H, W, 1))
img = img + grain
fade = 0.82
img = img * fade + np.array([225, 214, 200]) * (1 - fade)
Image.fromarray(img.clip(0, 255).astype(np.uint8)).save(f"{OUT}/rug.png")

# Fine bump for the rug pile
bump = (rng.normal(128, 40, (H // 2, W // 2))).clip(0, 255).astype(np.uint8)
Image.fromarray(bump).resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.8)).save(f"{OUT}/rug_bump.png")

# TV picture: calm mountain lake at dusk
W2, H2 = 1600, 900
tv = Image.new("RGB", (W2, H2))
d = ImageDraw.Draw(tv)
for y in range(H2):
    t = y / H2
    c0, c1 = np.array([244, 196, 170]), np.array([120, 150, 178])
    c = c1 * (1 - t) + c0 * t if t < 0.55 else np.array([96, 120, 130]) * 0.8
    d.line([(0, y), (W2, y)], fill=tuple(int(v) for v in c))
r = random.Random(3)
for layer, (col, base_y, amp) in enumerate([((148, 150, 168), 420, 120), ((110, 122, 140), 470, 90), ((70, 86, 92), 500, 60)]):
    pts = [(0, H2)]
    for x in range(0, W2 + 40, 40):
        pts.append((x, base_y - amp * (0.5 + 0.5 * math.sin(x / 210 + layer * 2.1)) - r.uniform(0, amp * 0.3)))
    pts.append((W2, H2))
    d.polygon(pts, fill=col)
d.rectangle([0, 500, W2, H2], fill=(84, 104, 112))
for y in range(500, H2, 6):
    d.line([(r.uniform(0, W2), y), (r.uniform(0, W2), y)], fill=(150, 160, 170), width=1)
d.ellipse([1050, 250, 1130, 330], fill=(255, 224, 190))
tv.filter(ImageFilter.GaussianBlur(1.2)).save(f"{OUT}/tv.png")
print("textures ok")
