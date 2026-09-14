#!/usr/bin/env python3
"""Generate CURRENT_PINK_MALL_FASHION_CONTEXT at task time.

Fashion direction is NOT frozen into the Avatar Skill. This reads the current
canonical catalogue and emits a context instance the prompt assembler uses as
`wardrobeSource: CURRENT_PINK_MALL_CATALOGUE`.

    python build_fashion_context.py --catalogue /path/to/PINKMALL.html \
                                    --out /tmp/fashion_context.json

The instance is deliberately NOT committed: it is a snapshot, and a stale
snapshot silently becomes wrong. Regenerate per task.
"""
import argparse, collections, datetime, hashlib, json, os, re, sys

def _str(seg, key):
    m = re.search(r"""["']?%s["']?\s*:\s*(?:["']([^"']*)["']|(\d+))""" % key, seg)
    return (m.group(1) or m.group(2)) if m else None


def _bool(seg, key):
    m = re.search(r"""["']?%s["']?\s*:\s*(\w+)""" % key, seg)
    return bool(m) and m.group(1).lower() == "true"


def _list(seg, key):
    m = re.search(r"""["']?%s["']?\s*:\s*\[(.*?)\]""" % key, seg, re.S)
    return [t.strip(" '\"") for t in m.group(1).split(",") if t.strip()] if m else []


def parse_catalogue(html):
    """Slice PINK_MALL_PRODUCTS out of the canonical build and read each record."""
    start = html.index("var PINK_MALL_PRODUCTS = [")
    i = html.index("[", start)
    depth, j = 0, i
    while True:
        if html[j] == "[":
            depth += 1
        elif html[j] == "]":
            depth -= 1
            if depth == 0:
                break
        j += 1
    blob = html[i:j + 1]

    products = []
    for m in re.finditer(r"""["']?id["']?\s*:\s*["'](PM-\d+)["']""", blob):
        seg = blob[m.start():m.start() + 4000]
        products.append({
            "id": m.group(1),
            "brand": _str(seg, "brand"),
            "name": _str(seg, "name"),
            "category": _str(seg, "category"),
            "subcategory": _str(seg, "subcategory"),
            "priceEUR": _str(seg, "priceEUR"),
            "campaign": _str(seg, "campaign"),
            "isNew": _bool(seg, "isNew"),
            "tags": _list(seg, "tags"),
        })
    return products


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalogue", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if not os.path.exists(a.catalogue):
        sys.exit(f"catalogue not found: {a.catalogue}")
    raw = open(a.catalogue, "rb").read()
    html = raw.decode("utf-8", "replace")
    products = parse_catalogue(html)
    if not products:
        sys.exit("no products parsed — refusing to emit an empty wardrobe authority")

    cats = collections.Counter(p["category"] for p in products if p["category"])
    words = collections.Counter()
    for p in products:
        for t in p["tags"]:
            if t: words[t.lower()] += 1

    ctx = {
        "schemaVersion": 1,
        "version": "CURRENT_PINK_MALL_FASHION_CONTEXT_v1.3",
        "generatedAt": datetime.date.today().isoformat(),
        "catalogueSource": {"path": os.path.basename(a.catalogue),
                            "sha256": hashlib.sha256(raw).hexdigest(),
                            "bytes": len(raw)},
        "catalogueSize": len(products),
        "activeCategories": dict(cats.most_common()),
        "assortment": products,
        "activeCampaigns": sorted({p["campaign"] for p in products if p["campaign"]}),
        "newIn": [p["id"] for p in products if p["isNew"]],
        "vocabulary": dict(words.most_common(40)),
        "wardrobeAuthorityStatus": "VALID",
        "usage": ("Pass as wardrobeSource=CURRENT_PINK_MALL_CATALOGUE. Styling must come from this "
                  "assortment. Never fall back to avatar calibration clothing."),
    }
    json.dump(ctx, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {a.out}: {len(products)} products, {len(cats)} categories, "
          f"{len(ctx['activeCampaigns'])} campaigns")

if __name__ == "__main__":
    main()
