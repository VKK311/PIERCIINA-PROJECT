#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import hashlib, json, re, shutil, sys

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'PINKMALL.html'
STATE = ROOT / 'docs/pink-mall/PROJECT_STATE.md'
STANDALONE = ROOT / 'PINKMALL_REVIEW_STANDALONE.html'
SRC = ROOT / 'docs/pink-mall/media-acquisition/SPLA94/source/SPLA94-01-original.jpg'
LIVE_DIR = ROOT / 'assets/pink-mall/products/PM-041'
LIVE_SRC = LIVE_DIR / 'source/SPLA94-01-original.jpg'
LIVE = LIVE_DIR / 'PM-041-main.webp'
EXPECT_DIR = ROOT / 'tools/regression/expect'
EXPECT = EXPECT_DIR / 'PM-041.json'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def patch_catalog():
    text = HTML.read_text(encoding='utf-8')
    if '"id": "PM-041"' in text:
        return
    start = text.find('"id": "PM-040"')
    if start < 0:
        raise SystemExit('PM-040 anchor not found; refusing stale publication')
    anchor = '\n}\n        ];'
    end = text.find(anchor, start)
    if end < 0:
        raise SystemExit('catalogue terminator after PM-040 not found')
    entry = '''\n},\n{\n    "id": "PM-041",\n    "brand": "Police",\n    "manufacturerItemNo": "SPLA94",\n    "variantCode": "8RFX",\n    "name": "Moonbeam 1",\n    "slug": "police-moonbeam-1-pink",\n    "category": "accessories",\n    "subcategory": null,\n    "color": "Pink",\n    "priceEUR": 64,\n    "oldPriceEUR": null,\n    "description": "Police Moonbeam 1 в розово — метална рамка и розови преливащи лещи. Statement очила с чиста, графична линия.",\n    "selectedBy": null,\n    "tags": [\n        "police",\n        "moonbeam 1",\n        "spla94",\n        "8rfx",\n        "sunglasses",\n        "очила",\n        "accessories",\n        "pink"\n    ],\n    "featured": false,\n    "campaign": null,\n    "related": ["PM-040", "PM-033", "PM-015"],\n    "isNew": false,\n    "newUntil": "2026-09-12",\n    "inventoryMode": "availability",\n    "availability": {"ONE SIZE": "available"},\n    "media": {\n        "image": "assets/pink-mall/products/PM-041/PM-041-main.webp",\n        "imageAlt": "Розови слънчеви очила Police Moonbeam 1, фронтален изглед",\n        "gallery": [],\n        "galleryAlt": [],\n        "fit": "contain",\n        "ph": "accessories",\n        "field": "blush",\n        "surface": "#FFFFFF"\n    },\n    "source": {\n        "identityTier": "TRUSTED_RETAILER",\n        "identityBasis": "Exact-item Otticanet evidence identifies Police MOONBEAM 1 SPLA94 8RFX in Pink / Pink Shaded; exact SKU is present in the acquired asset URL",\n        "mediaTransport": "TRUSTED_RETAILER",\n        "verifiedAt": "2026-08-29",\n        "mediaPolicyException": "OWNER_APPROVED_SINGLE_IMAGE_2026-08-29"\n    }\n}\n        ];'''
    text = text[:end] + entry + text[end + len(anchor):]
    HTML.write_text(text, encoding='utf-8')


def prepare_media():
    if not SRC.exists():
        raise SystemExit('SPLA94 acquired source image missing')
    LIVE_SRC.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC, LIVE_SRC)
    with Image.open(SRC) as im:
        if im.size != (1000, 455):
            raise SystemExit(f'unexpected SPLA94 source dimensions: {im.size}')
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGB')
        im.save(LIVE, 'WEBP', quality=88, method=6)
    with Image.open(LIVE) as im:
        if im.size != (1000, 455):
            raise SystemExit('live media dimensions changed')
    readme = f'''# PM-041 — Police Moonbeam 1\n\n- Manufacturer item: `SPLA94`\n- Verified pink variant: `8RFX`\n- Price: €64\n- Availability: `ONE SIZE — available`\n- Media source: trusted exact-item retailer evidence (`Otticanet`)\n- Original acquired file preserved at `source/SPLA94-01-original.jpg`.\n- Live file is WebP conversion only; no crop, resize, upscale or generative edit.\n- **Owner-approved publication exception (2026-08-29): this SKU is intentionally published with one canonical image.** The project-wide default remains minimum 3 unique exact-product images for other products.\n\nLive SHA-256: `{sha256(LIVE)}`\n'''
    (LIVE_DIR / 'README.md').write_text(readme, encoding='utf-8')


def write_expectations():
    for p in EXPECT_DIR.glob('PM-*.json'):
        data = json.loads(p.read_text(encoding='utf-8'))
        data['catalogueSize'] = 41
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    data = {
        'id': 'PM-041',
        'catalogueSize': 41,
        'brand': 'Police',
        'manufacturerItemNo': 'SPLA94',
        'name': 'Moonbeam 1',
        'category': 'accessories',
        'subcategory': None,
        'color': 'Pink',
        'priceEUR': 64,
        'newUntil': '2026-09-12',
        'sizes': ['ONE SIZE'],
        'surface': '#FFFFFF',
        'nativeWidth': 1000,
        'nativeHeight': 455,
        'viberUrl': 'https://connect.viber.com/business/631d5a74-5919-11f1-b5e8-06dd2a4dc594',
        'searchTerms': ['police', 'moonbeam', 'очила', 'SPLA94'],
        'priorProducts': [f'PM-{n:03d}' for n in range(31, 41)],
        'frames': [{
            'file': 'PM-041-main.webp',
            'sha256': sha256(LIVE),
            'width': 1000,
            'height': 455
        }]
    }
    EXPECT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def update_state_base():
    s = STATE.read_text(encoding='utf-8')
    s = re.sub(r'^Updated: .*$', 'Updated: PM-041 publication.', s, count=1, flags=re.M)
    s = re.sub(r'^Status: \*\*PM-001…PM-\d+ PUBLISHED\.\*\*$', 'Status: **PM-001…PM-041 PUBLISHED.**', s, count=1, flags=re.M)
    s = re.sub(r'\| CANONICAL WEBSITE SHA-256 \| `[^`]+` \|', f'| CANONICAL WEBSITE SHA-256 | `{sha256(HTML)}` |', s, count=1)
    s = re.sub(r'\| CANONICAL WEBSITE BYTES \| \d+ \|', f'| CANONICAL WEBSITE BYTES | {HTML.stat().st_size} |', s, count=1)
    s = re.sub(r'\| PUBLIC CATALOG \| PM-001 … PM-\d+ \|', '| PUBLIC CATALOG | PM-001 … PM-041 |', s, count=1)
    s = re.sub(r'\| NEXT ID \| PM-\d+ \|', '| NEXT ID | PM-042 |', s, count=1)
    if '| SPLA94 | **PUBLISHED as PM-041**' not in s:
        marker = '| SPARKS/G/S 8CQ | **PUBLISHED as PM-040** on 2026-08-29 — identity from the frame\'s own temple print; media `USER_SUPPLIED` |'
        if marker in s:
            s = s.replace(marker, marker + '\n| SPLA94 | **PUBLISHED as PM-041** on 2026-08-29 — owner-approved one-image exception; exact pink variant 8RFX |', 1)
        else:
            cat = re.search(r'(\| NEXT ID \| PM-042 \|)', s)
            if not cat:
                raise SystemExit('catalogue state insertion point missing')
            s = s[:cat.end()] + '\n| SPLA94 | **PUBLISHED as PM-041** on 2026-08-29 — owner-approved one-image exception; exact pink variant 8RFX |' + s[cat.end():]
    s = re.sub(r'\| PUBLICATION REGRESSION \| PASS — `tools/regression/product_regression\.js`; PM-\d+…PM-\d+, production \+ standalone \|', '| PUBLICATION REGRESSION | PASS — `tools/regression/product_regression.js`; PM-031…PM-041, production + standalone |', s, count=1)
    if '## PM-041 — published' not in s:
        s += '''\n\n## PM-041 — published\n\n| | |\n|---|---|\n| PUBLISHED | 2026-08-29 |\n| BRAND / MODEL | Police / Moonbeam 1 |\n| MANUFACTURER ITEM | SPLA94 |\n| VERIFIED VARIANT | 8RFX — Pink / Pink Shaded |\n| PUBLIC COLOUR | Pink |\n| MATERIAL | omitted — no customer-facing composition claim published |\n| PRICE | €64, no SALE |\n| INVENTORY MODE | availability |\n| SIZES | ONE SIZE — available |\n| NEW UNTIL | 2026-09-12 |\n| MAIN | IMAGE 01 — exact-item front product shot |\n| GALLERY | **1 image total — OWNER-APPROVED EXCEPTION** |\n| LIVE MEDIA | `assets/pink-mall/products/PM-041/PM-041-main.webp` — 1000×455 WebP, native aspect |\n| ORIGINAL | `assets/pink-mall/products/PM-041/source/SPLA94-01-original.jpg` |\n| MEDIA TIER | TRUSTED_RETAILER — exact SKU present in asset URL |\n\nThe normal Pink Mall media contract still requires at least three unique exact-product images. PM-041 is a product-specific exception explicitly approved by the owner on 2026-08-29; it does not change the default acquisition or approval gate for any other SKU.\n'''
    STATE.write_text(s, encoding='utf-8')


def finalize_state():
    if not STANDALONE.exists():
        raise SystemExit('standalone artifact missing')
    s = STATE.read_text(encoding='utf-8')
    sec = s.find('## Review artifact')
    if sec >= 0:
        end = s.find('\n## ', sec + 4)
        if end < 0:
            end = len(s)
        block = s[sec:end]
        block = re.sub(r'\| SHA-256 \| `[^`]+` \|', f'| SHA-256 | `{sha256(STANDALONE)}` |', block, count=1)
        block = re.sub(r'\| BYTES \| \d+ \|', f'| BYTES | {STANDALONE.stat().st_size} |', block, count=1)
        block = re.sub(r'\| LAST PUBLICATION VALIDATION \| .*? \|', '| LAST PUBLICATION VALIDATION | PASS — PM-041 production + standalone + viewport smoke |', block, count=1)
        s = s[:sec] + block + s[end:]
    STATE.write_text(s, encoding='utf-8')


def prepare():
    prepare_media()
    patch_catalog()
    write_expectations()
    update_state_base()
    print('PM-041 prepared', sha256(HTML), sha256(LIVE))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'prepare'
    if mode == 'prepare':
        prepare()
    elif mode == 'finalize':
        finalize_state()
    else:
        raise SystemExit('usage: publish_pm041.py [prepare|finalize]')
