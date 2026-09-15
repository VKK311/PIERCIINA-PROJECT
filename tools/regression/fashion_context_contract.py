#!/usr/bin/env python3
"""Contract test for the seam between PINKMALL.html and build_fashion_context.py.

    python tools/regression/fashion_context_contract.py [PINKMALL.html]

The Avatar Skill reads the canonical catalogue by regex: build_fashion_context.py
locates `var PINK_MALL_PRODUCTS = [` and slices the array out of the storefront.
Nothing in the build enforces that seam, so a rename, a reshape or a truncation
would not break a build — it would quietly narrow the wardrobe authority the
skill styles from, and the first visible symptom would be wrong clothes in a
generated campaign image.

This proves the seam instead:

  * the builder still finds and fully reads the catalogue;
  * what it reports matches an INDEPENDENT extraction of the same array, so the
    builder is never merely compared against itself;
  * freshness in the emitted context follows the storefront's own rule, checked
    on deterministic as-of dates either side of the boundary;
  * structural drift fails loudly rather than emitting a partial catalogue.

The observed catalogue size is reported, never asserted against a constant:
PM-047 and beyond must not break this test.
"""
import datetime, hashlib, importlib.util, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BUILDER = os.path.join(ROOT, "docs", "pink-mall", "avatar-skill", "v1.3",
                       "build_fashion_context.py")

passed, failed = 0, 0


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS  {name}" + (f"  — {detail}" if detail else ""))
    else:
        failed += 1
        print(f"  FAIL  {name}" + (f"  — {detail}" if detail else ""))
    return bool(cond)


def load_builder():
    spec = importlib.util.spec_from_file_location("bfc", BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── independent extraction ────────────────────────────────────────────────
# Deliberately NOT the builder's code path. The builder scans the whole array
# with one regex; this splits the array into top-level {...} records first and
# reads one id out of each. Different algorithm, same source, so agreement is
# evidence rather than a tautology — and record-wise walking also proves the
# array really holds one id per record.
#
# The catalogue is written in two styles: early records use a bare `id:` key,
# records from PM-034 onward use JSON-style `"id":`. Both are accepted here.
ID_IN_RECORD = re.compile(r"""["']?id["']?\s*:\s*["'](PM-\d+)["']""")


def independent_ids(html):
    at = html.find("var PINK_MALL_PRODUCTS")
    if at < 0:
        return None
    start = html.index("[", at)
    depth, k = 0, start
    while k < len(html):
        ch = html[k]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                break
        k += 1
    else:
        return None
    region = html[start:k + 1]

    # Split into top-level records by brace depth, then read each record's id.
    ids, depth, rec_start = [], 0, None
    for idx, ch in enumerate(region):
        if ch == "{":
            if depth == 0:
                rec_start = idx
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and rec_start is not None:
                m = ID_IN_RECORD.search(region[rec_start:idx + 1])
                if m:
                    ids.append(m.group(1))
                rec_start = None
    return ids, region


def independent_is_new(raw_is_new, new_until, as_of):
    """The canonical rule, written out again from PINKMALL.html's isProductNew."""
    if new_until:
        try:
            return as_of <= datetime.date.fromisoformat(new_until)
        except (ValueError, TypeError):
            pass
    return bool(raw_is_new)


def run_builder(catalogue, as_of=None):
    out = tempfile.mktemp(suffix=".json")
    cmd = [sys.executable, BUILDER, "--catalogue", catalogue, "--out", out]
    if as_of:
        cmd += ["--as-of", as_of]
    r = subprocess.run(cmd, capture_output=True, text=True)
    data = None
    if r.returncode == 0 and os.path.exists(out):
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
        os.unlink(out)
    return r.returncode, data, (r.stdout + r.stderr)


def main():
    catalogue = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "PINKMALL.html")
    if not os.path.exists(catalogue):
        sys.exit(f"catalogue not found: {catalogue}")
    raw = open(catalogue, "rb").read()
    html = raw.decode("utf-8", "replace")
    bfc = load_builder()

    print(f"== fashion-context contract: {os.path.basename(catalogue)} ==")

    # 1 — the array is discoverable
    check("1. PINK_MALL_PRODUCTS array is discoverable",
          bfc.ARRAY_MARKER in html, bfc.ARRAY_MARKER)

    ind = independent_ids(html)
    if not check("   independent extractor located the array", ind is not None):
        print("\nFASHION CONTEXT CONTRACT: FAIL (cannot continue)")
        sys.exit(1)
    ind_ids, _region = ind

    products = bfc.parse_catalogue(html)
    ids = [p["id"] for p in products]

    # 2 — non-empty
    check("2. parser output is non-empty", len(products) > 0, f"{len(products)} products")
    # 3 — unique
    check("3. all PM ids are unique", len(set(ids)) == len(ids),
          f"{len(ids) - len(set(ids))} duplicates")
    # 4 — matches the independent view
    check("4. parsed ids match the independent extraction",
          ids == ind_ids, f"builder={len(ids)} independent={len(ind_ids)}")
    # 5 — nothing disappears
    missing, extra = set(ind_ids) - set(ids), set(ids) - set(ind_ids)
    check("5. no product disappears silently", not missing and not extra,
          f"missing={sorted(missing)} extra={sorted(extra)}")
    # 6 — required fields
    bad = [p["id"] for p in products if any(not p.get(f) for f in bfc.REQUIRED_FIELDS)]
    check("6. every product carries the fields the context needs", not bad, str(bad))

    rc, ctx, log = run_builder(catalogue)
    if not check("   builder ran successfully", rc == 0 and ctx is not None, log.strip()[:200]):
        print("\nFASHION CONTEXT CONTRACT: FAIL (cannot continue)")
        sys.exit(1)

    # 7 — category counts internally consistent
    recount = {}
    for p in products:
        if p["category"]:
            recount[p["category"]] = recount.get(p["category"], 0) + 1
    check("7. activeCategories counts are internally consistent",
          ctx["activeCategories"] == recount,
          f"context={ctx['activeCategories']} recount={recount}")
    check("   every category total sums to the catalogue size",
          sum(ctx["activeCategories"].values()) == len([p for p in products if p["category"]]))
    # 8 — catalogueSize
    check("8. catalogueSize equals the parsed catalogue count",
          ctx["catalogueSize"] == len(products), f"{ctx['catalogueSize']} vs {len(products)}")
    check("   catalogueSize equals the independent count",
          ctx["catalogueSize"] == len(ind_ids))
    # 9 — source sha
    check("9. catalogueSource.sha256 matches the input file",
          ctx["catalogueSource"]["sha256"] == hashlib.sha256(raw).hexdigest(),
          ctx["catalogueSource"]["sha256"][:16] + "…")
    check("   catalogueSource.bytes matches the input file",
          ctx["catalogueSource"]["bytes"] == len(raw))
    # 10 — status
    check("10. wardrobeAuthorityStatus is VALID",
          ctx.get("wardrobeAuthorityStatus") == "VALID", str(ctx.get("wardrobeAuthorityStatus")))
    check("    assortment carries every parsed product",
          [p["id"] for p in ctx["assortment"]] == ids)
    check("    raw isNew and newUntil are preserved for provenance",
          all("isNew" in p and "newUntil" in p for p in ctx["assortment"]))

    # ── 11/12/13 — structural drift must fail loudly ──────────────────────
    def expect_raise(label, broken_html):
        try:
            bfc.parse_catalogue(broken_html)
            return check(label, False, "parse_catalogue returned instead of raising")
        except bfc.CatalogueError as e:
            return check(label, True, str(e)[:70])
        except Exception as e:                                   # noqa: BLE001
            return check(label, False, f"wrong exception: {type(e).__name__}: {e}")

    print("  -- structural drift --")
    expect_raise("11. renamed/absent array fails loudly",
                 html.replace(bfc.ARRAY_MARKER, "var SOMETHING_ELSE = ["))
    expect_raise("    empty catalogue fails loudly", "var PINK_MALL_PRODUCTS = [];")
    expect_raise("12. duplicate ids fail loudly", _with_duplicate(html, bfc))
    expect_raise("13. truncated array fails loudly — no partial success",
                 _truncated(html, bfc))

    rc2, _d, log2 = run_builder_on_text(bfc, "var PINK_MALL_PRODUCTS = [];")
    check("    the CLI itself refuses a broken catalogue", rc2 != 0, log2.strip()[:90])

    # ── 14-17 — freshness, on deterministic dates ─────────────────────────
    print("  -- freshness (deterministic as-of dates) --")
    dated = [p for p in products if p.get("newUntil")]
    check("    catalogue carries date-gated products to test",
          len(dated) > 0, f"{len(dated)} of {len(products)} have newUntil")

    def newin_for(as_of_str):
        rc, c, lg = run_builder(catalogue, as_of_str)
        return (set(c["newIn"]) if c else None), rc, lg

    today = datetime.date.today()
    for label, day in (("today", today),
                       ("one year back", today - datetime.timedelta(days=365)),
                       ("one year ahead", today + datetime.timedelta(days=365))):
        got, rc, lg = newin_for(day.isoformat())
        want = {p["id"] for p in products
                if independent_is_new(p["isNew"], p.get("newUntil"), day)}
        check(f"14. newIn matches the canonical rule as of {day} ({label})",
              got == want,
              f"context={len(got or [])} independent={len(want)} diff={sorted((got or set()) ^ want)[:5]}")

    # 15 — a product leaves newIn the day after its newUntil
    sample = sorted(dated, key=lambda p: p["newUntil"])[0] if dated else None
    if sample:
        nu = datetime.date.fromisoformat(sample["newUntil"])
        on, _r, _l = newin_for(nu.isoformat())
        after, _r, _l = newin_for((nu + datetime.timedelta(days=1)).isoformat())
        before, _r, _l = newin_for((nu - datetime.timedelta(days=1)).isoformat())
        check("15. an expired product leaves newIn the day after newUntil",
              sample["id"] in (on or set()) and sample["id"] not in (after or set()),
              f"{sample['id']} newUntil={sample['newUntil']}")
        # 16 — the boundary day itself is inclusive, as isProductNew() is
        check("16. the newUntil day itself still counts as NEW (inclusive boundary)",
              sample["id"] in (on or set()), f"{sample['id']} on {sample['newUntil']}")
        check("    and it was NEW the day before", sample["id"] in (before or set()))
        # 17 — unexpired behaviour
        future, _r, _l = newin_for((nu - datetime.timedelta(days=7)).isoformat())
        check("17. an unexpired product is present in newIn",
              sample["id"] in (future or set()))

    # raw-vs-gated divergence is the defect this contract exists to catch
    raw_new = {p["id"] for p in products if p["isNew"]}
    gated = {p["id"] for p in products if independent_is_new(p["isNew"], p.get("newUntil"), today)}
    check("    newIn is date-gated, not the raw isNew flag",
          set(ctx["newIn"]) == gated,
          f"gated={len(gated)} rawFlag={len(raw_new)} divergence={sorted(raw_new ^ gated)}")

    # bad --as-of must be rejected
    rc3, _d3, log3 = run_builder(catalogue, "2026-13-99")
    check("    --as-of rejects a malformed date", rc3 != 0, log3.strip().splitlines()[-1][:80] if log3.strip() else "")

    print(f"\nobserved catalogue size: {len(products)} products "
          f"(reported, not asserted — new publications must not break this test)")
    print(f"FASHION CONTEXT CONTRACT: {'PASS' if not failed else 'FAIL'} "
          f"({passed} passed, {failed} failed)")
    sys.exit(1 if failed else 0)


def _with_duplicate(html, bfc):
    """Clone the first product record so the array carries a duplicate id."""
    at = html.find(bfc.ARRAY_MARKER)
    start = html.index("{", at)
    depth, k = 0, start
    while k < len(html):
        if html[k] == "{":
            depth += 1
        elif html[k] == "}":
            depth -= 1
            if depth == 0:
                break
        k += 1
    record = html[start:k + 1]
    return html[:k + 1] + "," + record + html[k + 1:]


def _truncated(html, bfc):
    """Cut the file off inside the product array so it is never closed."""
    at = html.index(bfc.ARRAY_MARKER)
    return html[:at + 4000]


def run_builder_on_text(bfc, text):
    tmp = tempfile.mktemp(suffix=".html")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    rc, data, log = run_builder(tmp)
    os.unlink(tmp)
    return rc, data, log


if __name__ == "__main__":
    main()
