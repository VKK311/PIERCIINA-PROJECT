#!/usr/bin/env python3
import argparse, datetime as dt, hashlib, json, os, re, shutil
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SHA = "af8e2ff7bad66534f05bd5bf63909f9b7a9331566c5361920bb5d41bf2d8e13d"
PUB_DATE = "2026-08-28"
NEW_UNTIL = "2026-09-11"
CANDIDATE = ROOT / "PINKMALL_CATALOG_UPDATE_2026-08-28.html"
CANON = ROOT / "PINKMALL.html"
STATE = ROOT / "docs/pink-mall/PROJECT_STATE.md"
STANDALONE = ROOT / "PINKMALL_REVIEW_STANDALONE.html"

PRODUCTS = [
    {
        "id": "PM-034", "sku": "V69WBAG152", "brand": "19V69 ITALIA",
        "name": "LIERNA", "slug": "19v69-italia-lierna", "color": "Pink",
        "composition": "80% Polyamide / 20% Polyurethane", "priceEUR": 74,
        "description": "Hot pink, кафяви акценти и tennis mood отвън. LIERNA влиза шумно и няма намерение да се извинява.",
        "tags": ["19v69 italia","lierna","bags","bag","pink","polyamide","polyurethane"],
        "source_page": "https://www.19v69-italia.com/en/products/v69wbag152",
        "source_indices": [4,2,3,1],
        "surface": None,
        "alts": [
            "Розова чанта 19V69 ITALIA LIERNA, цял изглед отпред",
            "Розова чанта 19V69 ITALIA LIERNA, втори продуктов изглед",
            "Розова чанта 19V69 ITALIA LIERNA, изглед към вътрешността",
            "Розова чанта 19V69 ITALIA LIERNA, детайл на предната част",
        ],
        "views": ["front, whole bag","secondary product view","interior view","front detail"],
        "media_tier": "OFFICIAL",
        "expected_status": "PASS",
    },
    {
        "id": "PM-035", "sku": "30S4SBAL2L", "brand": "Michael Kors",
        "name": "Colby Medium Leather Shoulder Bag",
        "slug": "michael-kors-colby-medium-leather-shoulder-bag",
        "color": "Smokey Rose", "composition": "100% Leather", "priceEUR": 119,
        "description": "Smokey Rose, чист силует и голяма катарама отпред. Colby е розова, но хич не е тиха.",
        "tags": ["michael kors","colby","shoulder bag","bags","smokey rose","pink","leather"],
        "source_page": "https://www.michaelkors.global/bg/en/colby-medium-leather-shoulder-bag/30S4SBAL2L.html",
        "source_indices": [1,3,4,5],
        "surface": None,
        "alts": [
            "Розова кожена чанта Michael Kors Colby, изглед отпред",
            "Розова кожена чанта Michael Kors Colby, втори продуктов изглед",
            "Розова кожена чанта Michael Kors Colby, детайл на конструкцията",
            "Розова кожена чанта Michael Kors Colby, детайл на катарамата",
        ],
        "views": ["front, whole bag","secondary product view","construction detail","buckle detail"],
        "media_tier": "TRUSTED_RETAILER",
        "expected_status": "PASS",
    },
    {
        "id": "PM-036", "sku": "35F4G2VC5L", "brand": "Michael Kors",
        "name": "Vincent Small Saffiano Leather Crossbody Bag with Signature Logo Card Case",
        "slug": "michael-kors-vincent-small-saffiano-leather-crossbody-bag",
        "color": "Powder Blush", "composition": "100% Leather", "priceEUR": 104,
        "description": "Powder Blush + Saffiano leather + златисти детайли. Малка crossbody чанта с detachable card case за extra drama.",
        "tags": ["michael kors","vincent","crossbody bag","bags","powder blush","pink","saffiano leather","card case"],
        "source_page": "https://www.michaelkors.com/ca/en/vincent-small-saffiano-leather-crossbody-bag-with-signature-logo-card-case/785370099.html",
        "source_indices": [1,2,3,4],
        "surface": "#F6F6F6",
        "alts": [
            "Розова чанта Michael Kors Vincent от Saffiano кожа, основен продуктов изглед",
            "Розова чанта Michael Kors Vincent, втори продуктов изглед",
            "Розова чанта Michael Kors Vincent, изглед отпред",
            "Розова чанта Michael Kors Vincent, детайл с картодържател",
        ],
        "views": ["main product view","secondary product view","front view","card-case detail"],
        "media_tier": "OFFICIAL",
        "expected_status": "PASS",
    },
]
BLOCKED_SKU = "134-200-409"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def find_object_end(text, id_literal):
    pos = text.find(id_literal)
    if pos < 0:
        raise RuntimeError(f"{id_literal} not found")
    start = text.rfind("{", 0, pos)
    if start < 0:
        raise RuntimeError("object start not found")
    depth = 0
    i = start
    quote = None
    line_comment = False
    block_comment = False
    escape = False
    while i < len(text):
        ch = text[i]
        nxt = text[i+1] if i+1 < len(text) else ""
        if line_comment:
            if ch == "\n": line_comment = False
        elif block_comment:
            if ch == "*" and nxt == "/":
                block_comment = False; i += 1
        elif quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = None
        else:
            if ch in ("'", '"', "`"):
                quote = ch
            elif ch == "/" and nxt == "/":
                line_comment = True; i += 1
            elif ch == "/" and nxt == "*":
                block_comment = True; i += 1
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return start, i + 1
        i += 1
    raise RuntimeError("unterminated product object")

def patch_regression_harness():
    path = ROOT / "tools/regression/product_regression.js"
    s = path.read_text(encoding="utf-8")
    if "const dimsFor = " not in s:
        s = s.replace(
            "const NAMES = EXPECT.frames.map(f => f.file);\nconst LIVE = {};",
            "const NAMES = EXPECT.frames.map(f => f.file);\n"
            "const dimsFor = (name) => {\n"
            "  const f = EXPECT.frames.find(x => x.file === name) || {};\n"
            "  return { w: f.width || EXPECT.nativeWidth, h: f.height || EXPECT.nativeHeight };\n"
            "};\n"
            "const LIVE = {};",
            1,
        )
        old = """    is(r.ok && r.bytes > 5000 && r.w === EXPECT.nativeWidth && r.h === EXPECT.nativeHeight,
       `native ${EXPECT.nativeWidth}×${EXPECT.nativeHeight}: ` + (await nameOf(u)),
       r.ok ? `${r.bytes}B ${r.w}×${r.h} ${r.type}` : 'status ' + r.status);"""
        new = """    const nm = await nameOf(u);
    const d = dimsFor(nm);
    is(r.ok && r.bytes > 5000 && r.w === d.w && r.h === d.h,
       `native ${d.w}×${d.h}: ` + nm,
       r.ok ? `${r.bytes}B ${r.w}×${r.h} ${r.type}` : 'status ' + r.status);"""
        if old not in s:
            raise RuntimeError("media dimension assertion not found in regression harness")
        s = s.replace(old, new, 1)
        old2 = """    is(card.natural && card.natural[0] === EXPECT.nativeWidth, 'card image decoded', String(card.natural));"""
        new2 = """    const md = dimsFor(NAMES[0]);
    is(card.natural && card.natural[0] === md.w && card.natural[1] === md.h,
       'card image decoded', String(card.natural));"""
        if old2 not in s:
            raise RuntimeError("card dimension assertion not found in regression harness")
        s = s.replace(old2, new2, 1)
        path.write_text(s, encoding="utf-8")

def validate_acquisition(p):
    result_path = ROOT / f"docs/pink-mall/media-acquisition/{p['sku']}/result.json"
    data = json.loads(result_path.read_text(encoding="utf-8"))
    if data.get("status") != p["expected_status"]:
        raise RuntimeError(f"{p['sku']} acquisition is {data.get('status')}, not PASS")
    if data.get("variantConfidence",{}).get("state") != "VARIANT_CONFIDENCE_PASS":
        raise RuntimeError(f"{p['sku']} variant confidence not PASS")
    if data.get("mediaTier") != p["media_tier"]:
        raise RuntimeError(f"{p['sku']} media tier drifted: {data.get('mediaTier')}")
    images = {int(x["index"]): x for x in data["images"]}
    for idx in p["source_indices"]:
        if idx not in images:
            raise RuntimeError(f"{p['sku']} missing approved image index {idx}")
        if images[idx].get("validation") != "PASS":
            raise RuntimeError(f"{p['sku']} image {idx} validation not PASS")
    return data, images

def make_live_assets(p, result, images):
    out = ROOT / f"assets/pink-mall/products/{p['id']}"
    srcdir = out / "source"
    if out.exists():
        raise RuntimeError(f"{out} already exists")
    srcdir.mkdir(parents=True)
    frames = []
    rows = []
    for slot, src_idx in enumerate(p["source_indices"], start=1):
        item = images[src_idx]
        acquired = ROOT / f"docs/pink-mall/media-acquisition/{p['sku']}/{item['file']}"
        if not acquired.exists():
            raise RuntimeError(f"missing acquired original {acquired}")
        src_name = f"original-{slot:02d}{acquired.suffix.lower()}"
        live_src = srcdir / src_name
        shutil.copy2(acquired, live_src)
        live_name = f"{p['id']}-main.webp" if slot == 1 else f"{p['id']}-{slot:02d}.webp"
        live = out / live_name
        with Image.open(acquired) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGB")
            im.save(live, "WEBP", quality=88, method=6)
        with Image.open(live) as chk:
            w, h = chk.size
        frames.append({"file": live_name, "sha256": sha256(live), "width": w, "height": h})
        rows.append({
            "slot": "media.image" if slot == 1 else f"gallery[{slot-2}]",
            "live": live_name, "source_index": src_idx, "source_file": acquired.name,
            "source_url": item.get("source_url"), "original_sha256": sha256(live_src),
            "live_sha256": sha256(live), "width": w, "height": h,
            "view": p["views"][slot-1],
        })
    return out, frames, rows

def product_js(p):
    base = {
        "id": p["id"],
        "brand": p["brand"],
        "manufacturerItemNo": p["sku"],
        "name": p["name"],
        "slug": p["slug"],
        "category": "bags",
        "subcategory": None,
        "color": p["color"],
        "composition": p["composition"],
        "priceEUR": p["priceEUR"],
        "oldPriceEUR": None,
        "description": p["description"],
        "selectedBy": None,
        "tags": p["tags"],
        "featured": False,
        "campaign": None,
        "related": ["PM-033"],
        "isNew": False,
        "newUntil": NEW_UNTIL,
        "inventoryMode": "availability",
        "availability": {"ONE SIZE": "available"},
        "media": {
            "image": f"assets/pink-mall/products/{p['id']}/{p['id']}-main.webp",
            "imageAlt": p["alts"][0],
            "gallery": [f"assets/pink-mall/products/{p['id']}/{p['id']}-{i:02d}.webp" for i in range(2, len(p["source_indices"])+1)],
            "galleryAlt": p["alts"][1:],
            "fit": "contain",
            "ph": "bags",
            "field": "blush",
        },
        "source": {"manufacturerUrl": p["source_page"], "verifiedAt": PUB_DATE},
    }
    if p["surface"]:
        base["media"]["surface"] = p["surface"]
    return json.dumps(base, ensure_ascii=False, indent=4)

def write_expect(p, frames):
    main = frames[0]
    expect = {
        "id": p["id"], "catalogueSize": 36, "brand": p["brand"],
        "manufacturerItemNo": p["sku"], "name": p["name"],
        "category": "bags", "subcategory": None, "color": p["color"],
        "composition": p["composition"], "priceEUR": p["priceEUR"],
        "newUntil": NEW_UNTIL, "sizes": ["ONE SIZE"], "surface": p["surface"],
        "nativeWidth": main["width"], "nativeHeight": main["height"],
        "viberUrl": "https://connect.viber.com/business/631d5a74-5919-11f1-b5e8-06dd2a4dc594",
        "searchTerms": [p["brand"].lower(), p["name"].split()[0].lower(), "чанта", p["sku"]],
        "priorProducts": [f"PM-{i:03d}" for i in range(25,34)],
        "frames": frames,
    }
    path = ROOT / f"tools/regression/expect/{p['id']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(expect, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def write_readme(p, rows):
    out = ROOT / f"assets/pink-mall/products/{p['id']}/README.md"
    lines = [
        f"# {p['id']} — live product media", "",
        f"{p['brand']} {p['sku']} · {p['name']} · published {PUB_DATE}", "",
        "| Live file | Slot | Acquisition image | View | Native size |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| `{r['live']}` | `{r['slot']}` | IMAGE {r['source_index']:02d} | {r['view']} | {r['width']}×{r['height']} |")
    lines += [
        "", f"Media tier: **{p['media_tier']}**. `VARIANT_CONFIDENCE_PASS` in the acquisition result.",
        f"Source manifest: `docs/pink-mall/media-acquisition/{p['sku']}/result.json`.", "",
        "## Hashes", "",
        "| Live file | Original SHA-256 | Live WebP SHA-256 |",
        "|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| `{r['live']}` | `{r['original_sha256']}` | `{r['live_sha256']}` |")
    lines += [
        "", "Original selected downloads are copied unchanged under `source/`.",
        "Live files are JPEG → WebP quality 88 at each source image's native dimensions.",
        "No resize, crop, canvas, upscaling, recolouring or generative edit was applied.",
        "", "PINK MALL availability is `ONE SIZE — available` from the user.",
        "No retailer/manufacturer stock state was imported.",
    ]
    out.write_text("\n".join(lines)+"\n", encoding="utf-8")

def write_checkpoint(p, rows):
    path = ROOT / f"docs/pink-mall/checkpoints/{p['id'].replace('-','')}_{p['sku']}_APPROVAL_PREVIEW.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    order = " → ".join(f"IMAGE {r['source_index']:02d}" for r in rows)
    txt = f"""# PINK MALL — {p['id']} approval record

**STATUS: APPROVED FOR PUBLICATION — user approved in batch on {PUB_DATE}**

| | |
|---|---|
| Brand | {p['brand']} |
| Model | {p['name']} |
| Manufacturer item | `{p['sku']}` |
| Mall ID | {p['id']} |
| Category | BAGS |
| Color | {p['color']} |
| Composition | {p['composition']} |
| Price | €{p['priceEUR']} |
| Availability | ONE SIZE — available |
| NEW | until {NEW_UNTIL} |
| Media tier | {p['media_tier']} |
| Variant | VARIANT_CONFIDENCE_PASS |

Approved photo order: **{order}**

Short Mall copy:

> {p['description']}

No external stock state imported. `oldPriceEUR:null`; `selectedBy:null`.
"""
    path.write_text(txt, encoding="utf-8")

def prepare():
    if sha256(CANON) != BASELINE_SHA:
        raise RuntimeError("Canonical PINKMALL.html hash moved; refusing to publish over a changed baseline")
    html = CANON.read_text(encoding="utf-8")
    for p in PRODUCTS:
        if p["id"] in html or p["sku"] in html:
            raise RuntimeError(f"{p['id']}/{p['sku']} already present in canonical")
    if BLOCKED_SKU in html:
        raise RuntimeError("Blocked VEE SKU is already present in canonical")
    vee = json.loads((ROOT / f"docs/pink-mall/media-acquisition/{BLOCKED_SKU}/result.json").read_text(encoding="utf-8"))
    if vee.get("status") == "PASS":
        raise RuntimeError("VEE status changed to PASS; current approval explicitly excluded it, so stop for re-review")
    patch_regression_harness()
    records = []
    for p in PRODUCTS:
        result, images = validate_acquisition(p)
        _, frames, rows = make_live_assets(p, result, images)
        write_expect(p, frames)
        write_readme(p, rows)
        write_checkpoint(p, rows)
        records.append((p, frames, rows))
    anchor_id = "id: 'PM-033'" if "id: 'PM-033'" in html else '"id": "PM-033"'
    _, end = find_object_end(html, anchor_id)
    insertion = ",\n" + ",\n".join(product_js(p) for p,_,_ in records)
    candidate = html[:end] + insertion + html[end:]
    for p in PRODUCTS:
        if candidate.count(p["sku"]) < 1 or candidate.count(p["id"]) < 1:
            raise RuntimeError(f"failed to insert {p['id']}")
    if BLOCKED_SKU in candidate:
        raise RuntimeError("blocked VEE leaked into candidate")
    CANDIDATE.write_text(candidate, encoding="utf-8")
    print("PREPARED candidate", CANDIDATE.name, sha256(CANDIDATE))

def promote():
    if not CANDIDATE.exists():
        raise RuntimeError("candidate missing")
    shutil.copy2(CANDIDATE, CANON)
    CANDIDATE.unlink()
    print("PROMOTED candidate to canonical worktree", sha256(CANON))

def update_state():
    s = STATE.read_text(encoding="utf-8")
    if "PM-001…PM-033 PUBLISHED" not in s:
        raise RuntimeError("project state no longer has expected PM-033 baseline")
    canon_sha = sha256(CANON); canon_bytes = CANON.stat().st_size
    standalone_sha = sha256(STANDALONE)
    s = s.replace("Updated: PM-033 publication.", "Updated: PM-034–PM-036 publication.", 1)
    s = s.replace("Status: **PM-001…PM-033 PUBLISHED.**", "Status: **PM-001…PM-036 PUBLISHED.**", 1)
    s = re.sub(r"\| CANONICAL WEBSITE SHA-256 \| `[^`]+` \|",
               f"| CANONICAL WEBSITE SHA-256 | `{canon_sha}` |", s, count=1)
    s = re.sub(r"\| CANONICAL WEBSITE BYTES \| \d+ \|",
               f"| CANONICAL WEBSITE BYTES | {canon_bytes} |", s, count=1)
    s = s.replace("| PUBLIC CATALOG | PM-001 … PM-033 |", "| PUBLIC CATALOG | PM-001 … PM-036 |", 1)
    s = s.replace("| NEXT ID | PM-034 |", "| NEXT ID | PM-037 |", 1)
    anchor = "| TU0A28Z0699 | **PUBLISHED as PM-033** on 2026-08-27 |"
    add = anchor + "\n" + "\n".join([
        "| V69WBAG152 | **PUBLISHED as PM-034** on 2026-08-28 |",
        "| 30S4SBAL2L | **PUBLISHED as PM-035** on 2026-08-28 |",
        "| 35F4G2VC5L | **PUBLISHED as PM-036** on 2026-08-28 |",
        "| 134-200-409 | **BLOCKED — PHOTO SET INCOMPLETE**; 1 unique exact-SKU image |",
    ])
    if anchor not in s:
        raise RuntimeError("catalog anchor missing in project state")
    s = s.replace(anchor, add, 1)
    s = re.sub(
        r"\| PUBLICATION REGRESSION \| PASS — .*? \|",
        "| PUBLICATION REGRESSION | PASS — `tools/regression/product_regression.js`; PM-034, PM-035, PM-036, production + standalone |",
        s, count=1,
    )
    s = re.sub(
        r"(\| FILE \| `PINKMALL_REVIEW_STANDALONE\.html`[^\n]*\n\| SHA-256 \| `)[0-9a-f]{64}(` \|)",
        lambda m: m.group(1)+standalone_sha+m.group(2), s, count=1,
    )
    appendix = f"""

## PM-034 — published

| | |
|---|---|
| PUBLISHED | 2026-08-28 |
| BRAND / MODEL | 19V69 ITALIA / LIERNA |
| MANUFACTURER ITEM | V69WBAG152 |
| PUBLIC COLOUR | Pink |
| COMPOSITION | 80% Polyamide / 20% Polyurethane |
| PRICE | €74, no SALE |
| INVENTORY MODE | availability |
| SIZES | ONE SIZE — available |
| NEW UNTIL | {NEW_UNTIL} |
| MEDIA | 4 official exact-product frames, selected from acquisition PASS |
| TIER | OFFICIAL |
| VARIANT | VARIANT_CONFIDENCE_PASS |

## PM-035 — published

| | |
|---|---|
| PUBLISHED | 2026-08-28 |
| BRAND / MODEL | Michael Kors / Colby Medium Leather Shoulder Bag |
| MANUFACTURER ITEM | 30S4SBAL2L |
| PUBLIC COLOUR | Smokey Rose |
| COMPOSITION | 100% Leather |
| PRICE | €119, no SALE |
| INVENTORY MODE | availability |
| SIZES | ONE SIZE — available |
| NEW UNTIL | {NEW_UNTIL} |
| MEDIA | 4 trusted-retailer exact-variant frames; person-containing IMAGE 02 excluded |
| TIER | TRUSTED_RETAILER — Giglio |
| VARIANT | VARIANT_CONFIDENCE_PASS |

## PM-036 — published

| | |
|---|---|
| PUBLISHED | 2026-08-28 |
| BRAND / MODEL | Michael Kors / Vincent Small Saffiano Leather Crossbody Bag with Signature Logo Card Case |
| MANUFACTURER ITEM | 35F4G2VC5L |
| PUBLIC COLOUR | Powder Blush |
| COMPOSITION | 100% Leather |
| PRICE | €104, no SALE |
| INVENTORY MODE | availability |
| SIZES | ONE SIZE — available |
| NEW UNTIL | {NEW_UNTIL} |
| MEDIA | 4 official exact-SKU frames from assets.michaelkors.com |
| TIER | OFFICIAL |
| VARIANT | VARIANT_CONFIDENCE_PASS |

## Pending media — 134-200-409

VEE Collective `134-200-409` remains **BLOCKED — PHOTO SET INCOMPLETE**.
Identity and variant pass, but only one unique exact-SKU image survived
deduplication. It was deliberately excluded from the approved publication batch.
"""
    if "## PM-034 — published" not in s:
        s += appendix
    STATE.write_text(s, encoding="utf-8")
    print("UPDATED PROJECT_STATE", canon_sha, canon_bytes, standalone_sha)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["prepare","promote","state"])
    args = ap.parse_args()
    {"prepare": prepare, "promote": promote, "state": update_state}[args.mode]()

if __name__ == "__main__":
    main()
