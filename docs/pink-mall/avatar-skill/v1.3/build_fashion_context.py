#!/usr/bin/env python3
"""Generate CURRENT_PINK_MALL_FASHION_CONTEXT at task time.

Fashion direction is NOT frozen into the Avatar Skill. This reads the current
canonical catalogue and emits a context instance the prompt assembler uses as
`wardrobeSource: CURRENT_PINK_MALL_CATALOGUE`.

    python build_fashion_context.py --catalogue /path/to/PINKMALL.html \
                                    --out /tmp/fashion_context.json
                                    [--as-of YYYY-MM-DD]

`newIn` follows the canonical storefront freshness rule, not the raw isNew
flag (see is_product_new below). `--as-of` pins the evaluation date so the
result is reproducible in tests; it defaults to today.

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


class CatalogueError(Exception):
    """Structural drift in the canonical catalogue. Never swallowed."""


ARRAY_MARKER = "var PINK_MALL_PRODUCTS = ["

# Required for wardrobe authority. A record missing one of these is drift,
# not a product we may quietly style from.
REQUIRED_FIELDS = ("id", "name", "category")


def is_product_new(product, as_of):
    """The canonical storefront rule, mirrored exactly.

    PINKMALL.html decides freshness with:

        function isProductNew(p){
            if (!p) return false;
            if (p.newUntil) {
                var until = Date.parse(p.newUntil + 'T23:59:59');
                if (isFinite(until)) return Date.now() <= until;
            }
            return !!p.isNew;
        }

    So a parseable `newUntil` wins outright and is INCLUSIVE through the end
    of that day; raw `isNew` is only the fallback when `newUntil` is absent,
    empty or unparseable. Comparing whole dates is equivalent to comparing
    against 23:59:59 on the same day.
    """
    if not product:
        return False
    nu = product.get("newUntil")
    if nu:
        try:
            return as_of <= datetime.date.fromisoformat(nu)
        except (ValueError, TypeError):
            pass
    return bool(product.get("isNew"))


def parse_catalogue(html):
    """Slice PINK_MALL_PRODUCTS out of the canonical build and read each record.

    Every structural assumption raises CatalogueError rather than returning a
    short list. A partially parsed catalogue emitted as wardrobe authority is
    worse than no context at all: styling would silently narrow to whatever
    survived the drift.
    """
    start = html.find(ARRAY_MARKER)
    if start < 0:
        raise CatalogueError(
            "PINK_MALL_PRODUCTS array not found — expected the literal "
            f"{ARRAY_MARKER!r}. The catalogue structure has changed.")

    i = html.index("[", start)
    depth, j, n = 0, i, len(html)
    closed = False
    while j < n:
        if html[j] == "[":
            depth += 1
        elif html[j] == "]":
            depth -= 1
            if depth == 0:
                closed = True
                break
        j += 1
    if not closed:
        raise CatalogueError("PINK_MALL_PRODUCTS array is never closed — truncated catalogue.")
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
            # Raw flag preserved for provenance; freshness is decided by
            # is_product_new(), which date-gates it the way the store does.
            "isNew": _bool(seg, "isNew"),
            "newUntil": _str(seg, "newUntil"),
            "tags": _list(seg, "tags"),
        })

    if not products:
        raise CatalogueError("no products parsed — refusing to emit an empty wardrobe authority")

    seen, dupes = set(), []
    for p in products:
        if p["id"] in seen:
            dupes.append(p["id"])
        seen.add(p["id"])
    if dupes:
        raise CatalogueError(f"duplicate product ids in the catalogue: {sorted(set(dupes))}")

    incomplete = [p["id"] for p in products if any(not p.get(f) for f in REQUIRED_FIELDS)]
    if incomplete:
        raise CatalogueError(
            f"products missing required field(s) {list(REQUIRED_FIELDS)}: {incomplete}")

    return products


def _as_of(value):
    """Strict YYYY-MM-DD. A silently mis-parsed date would mis-date the whole
    wardrobe authority, so anything else is rejected outright."""
    try:
        return datetime.date.fromisoformat(value)
    except (ValueError, TypeError):
        raise argparse.ArgumentTypeError(
            f"--as-of must be an ISO date (YYYY-MM-DD), got {value!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalogue", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--as-of", dest="as_of", type=_as_of, default=None,
                    help="evaluate freshness as of this ISO date (default: today)")
    a = ap.parse_args()
    as_of = a.as_of or datetime.date.today()
    if not os.path.exists(a.catalogue):
        sys.exit(f"catalogue not found: {a.catalogue}")
    raw = open(a.catalogue, "rb").read()
    html = raw.decode("utf-8", "replace")
    try:
        products = parse_catalogue(html)
    except CatalogueError as e:
        sys.exit(f"catalogue contract broken: {e}")

    cats = collections.Counter(p["category"] for p in products if p["category"])
    words = collections.Counter()
    for p in products:
        for t in p["tags"]:
            if t: words[t.lower()] += 1

    ctx = {
        "schemaVersion": 1,
        "version": "CURRENT_PINK_MALL_FASHION_CONTEXT_v1.3",
        "generatedAt": datetime.date.today().isoformat(),
        "asOfDate": as_of.isoformat(),
        "catalogueSource": {"path": os.path.basename(a.catalogue),
                            "sha256": hashlib.sha256(raw).hexdigest(),
                            "bytes": len(raw)},
        "catalogueSize": len(products),
        "activeCategories": dict(cats.most_common()),
        "assortment": products,
        "activeCampaigns": sorted({p["campaign"] for p in products if p["campaign"]}),
        # Date-gated, matching the storefront. Using the raw isNew flag here
        # would call a product NEW after its badge and NEW IN membership had
        # already expired in the Mall, giving the avatar skill a wardrobe
        # authority the customer never sees.
        "newIn": [p["id"] for p in products if is_product_new(p, as_of)],
        "newInPolicy": ("newUntil inclusive through end of day when parseable, "
                        "otherwise the raw isNew flag — mirrors isProductNew() "
                        "in PINKMALL.html"),
        "vocabulary": dict(words.most_common(40)),
        "wardrobeAuthorityStatus": "VALID",
        "usage": ("Pass as wardrobeSource=CURRENT_PINK_MALL_CATALOGUE. Styling must come from this "
                  "assortment. Never fall back to avatar calibration clothing."),
    }
    json.dump(ctx, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {a.out}: {len(products)} products, {len(cats)} categories, "
          f"{len(ctx['activeCampaigns'])} campaigns, "
          f"{len(ctx['newIn'])} new in as of {as_of.isoformat()}")

if __name__ == "__main__":
    main()
