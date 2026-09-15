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

# A key must not be matched as the tail of a longer one. Without the guard,
# `category` also matches inside `subcategory`, and the right value is only
# returned because `category:` happens to be written first in every record.
# Reorder the fields, or omit `category`, and the product would silently take
# its subcategory as its category.
_KEY_BOUNDARY = r"(?<![A-Za-z0-9_$])"


def _str(seg, key):
    m = re.search(_KEY_BOUNDARY + r"""["']?%s["']?\s*:\s*(?:["']([^"']*)["']|(\d+))""" % key, seg)
    return (m.group(1) or m.group(2)) if m else None


def _bool(seg, key):
    m = re.search(_KEY_BOUNDARY + r"""["']?%s["']?\s*:\s*(\w+)""" % key, seg)
    return bool(m) and m.group(1).lower() == "true"


def _list(seg, key):
    m = re.search(_KEY_BOUNDARY + r"""["']?%s["']?\s*:\s*\[(.*?)\]""" % key, seg, re.S)
    return [t.strip(" '\"") for t in m.group(1).split(",") if t.strip()] if m else []


# The catalogue and the CLI both document YYYY-MM-DD. datetime.date.fromisoformat
# is broader than that on modern Pythons — it accepts 20260915, 2026-W38-2 and
# full datetimes — so a value that is not the documented shape would be read as
# a date instead of being treated as unparseable. One strict parser is used for
# both --as-of and newUntil so the two can never drift apart.
_ISO_DATE = re.compile(r"\A(\d{4})-(\d{2})-(\d{2})\Z")


def parse_iso_date(value):
    """Exactly YYYY-MM-DD and a real calendar date, else None."""
    if not isinstance(value, str):
        return None
    m = _ISO_DATE.match(value)
    if not m:
        return None
    try:
        return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


class CatalogueError(Exception):
    """Structural drift in the canonical catalogue. Never swallowed."""


ARRAY_MARKER = "var PINK_MALL_PRODUCTS = ["

# Required for wardrobe authority. A record missing one of these is drift,
# not a product we may quietly style from.
REQUIRED_FIELDS = ("id", "name", "category")

ID_PATTERN = re.compile(r"""["']?id["']?\s*:\s*["'](PM-\d+)["']""")


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
        until = parse_iso_date(nu)
        # A newUntil that is not exactly YYYY-MM-DD is treated as unparseable
        # and falls through to the raw flag, mirroring the storefront's
        # isFinite(Date.parse(newUntil + 'T23:59:59')) guard.
        if until is not None:
            return as_of <= until
    return bool(product.get("isNew"))


def _scan_structure(text, start, open_ch, close_ch):
    """Return the index of the delimiter closing the one at `start`.

    String-aware: quotes suspend structural meaning, so a brace or bracket
    inside a name, an alt text or a base64 data URI cannot be mistaken for
    structure. Returns None if it is never closed.
    """
    depth, i, n = 0, start, len(text)
    quote, esc = None, False
    while i < n:
        ch = text[i]
        if quote:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                quote = None
        elif ch in "'\"`":
            quote = ch
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i
            if depth < 0:
                return None
        i += 1
    return None


def split_records(blob):
    """Split the product array into its top-level {...} records.

    Each record is returned whole and separately. This is what makes parsing
    record-bounded: a field is only ever read from the object that owns it.
    """
    records, i, n = [], 0, len(blob)
    quote, esc, depth = None, False, 0
    while i < n:
        ch = blob[i]
        if quote:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                quote = None
            i += 1
            continue
        if ch in "'\"`":
            quote = ch
            i += 1
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        elif ch == "{" and depth == 1:
            close = _scan_structure(blob, i, "{", "}")
            if close is None:
                raise CatalogueError(
                    f"product record starting at offset {i} is never closed")
            records.append(blob[i:close + 1])
            i = close + 1
            continue
        i += 1
    if quote is not None:
        raise CatalogueError("unterminated string literal inside the product array")
    return records


def parse_catalogue(html):
    """Slice PINK_MALL_PRODUCTS out of the canonical build and read each record.

    Every field is read from within its own top-level record. An earlier
    version took a fixed 4000-character window from each id match, but every
    record in the catalogue is shorter than that (max 2463 characters), so a
    product missing a field would silently inherit the next product's value —
    a wrong brand or category reaching the wardrobe authority with nothing
    flagged. Record-bounded parsing makes that impossible.

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
    close = _scan_structure(html, i, "[", "]")
    if close is None:
        raise CatalogueError("PINK_MALL_PRODUCTS array is never closed — truncated catalogue.")
    blob = html[i:close + 1]

    products = []
    for pos, record in enumerate(split_records(blob)):
        found = ID_PATTERN.findall(record)
        if not found:
            raise CatalogueError(
                f"product record #{pos + 1} carries no PM-* id — "
                "a record without an id would vanish from the catalogue silently")
        if len(found) > 1:
            raise CatalogueError(
                f"product record #{pos + 1} carries more than one PM-* id: {found}")
        products.append({
            "id": found[0],
            "brand": _str(record, "brand"),
            "name": _str(record, "name"),
            "category": _str(record, "category"),
            "subcategory": _str(record, "subcategory"),
            "priceEUR": _str(record, "priceEUR"),
            "campaign": _str(record, "campaign"),
            # Raw flag preserved for provenance; freshness is decided by
            # is_product_new(), which date-gates it the way the store does.
            "isNew": _bool(record, "isNew"),
            "newUntil": _str(record, "newUntil"),
            "tags": _list(record, "tags"),
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
    d = parse_iso_date(value)
    if d is None:
        raise argparse.ArgumentTypeError(
            f"--as-of must be exactly YYYY-MM-DD, got {value!r}")
    return d


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
