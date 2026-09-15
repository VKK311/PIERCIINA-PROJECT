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
# Deliberately NOT the builder's code path. The builder walks the array once
# and slices each record as it goes; this one first collects every top-level
# record, then reports the ids found in each, so it can answer a question the
# builder cannot be asked to answer about itself: how many records are there,
# and does every one of them carry exactly one id?
#
# Counting records rather than ids is the point. An extractor that only
# appends when it finds an id would let an id-less record disappear from both
# sides and still agree.
#
# The catalogue is written in two styles: early records use a bare `id:` key,
# records from PM-034 onward use JSON-style `"id":`. Both are accepted.
ID_IN_RECORD = re.compile(r"""["']?id["']?\s*:\s*["'](PM-\d+)["']""")


def _records(region):
    """Every top-level {...} record in the array, quote-aware."""
    out, buf, depth = [], None, 0
    quote, esc, arr = None, False, 0
    for ch in region:
        if buf is not None:
            buf.append(ch)
        if quote:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                quote = None
            continue
        if ch in "'\"`":
            quote = ch
            continue
        if ch == "[":
            arr += 1
        elif ch == "]":
            arr -= 1
        elif ch == "{":
            if depth == 0 and arr == 1:
                buf = [ch]
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and buf is not None:
                out.append("".join(buf))
                buf = None
    return out


def independent_extract(html):
    """(records, ids_per_record, region) or None if the array is not found."""
    at = html.find("var PINK_MALL_PRODUCTS")
    if at < 0:
        return None
    start = html.index("[", at)
    depth, k, quote, esc = 0, start, None, False
    while k < len(html):
        ch = html[k]
        if quote:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                quote = None
        elif ch in "'\"`":
            quote = ch
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                break
        k += 1
    else:
        return None
    region = html[start:k + 1]
    recs = _records(region)
    return recs, [ID_IN_RECORD.findall(r) for r in recs], region


_STRICT = re.compile(r"\A(\d{4})-(\d{2})-(\d{2})\Z")


def independent_is_new(raw_is_new, new_until, as_of):
    """The canonical rule, written out again from PINKMALL.html's isProductNew.

    Only an exact YYYY-MM-DD calendar date counts; anything else is treated as
    unparseable and falls through to the raw flag, mirroring the storefront's
    isFinite(Date.parse(...)) guard for the catalogue's date format.
    """
    if new_until:
        m = _STRICT.match(new_until) if isinstance(new_until, str) else None
        if m:
            try:
                return as_of <= datetime.date(int(m.group(1)), int(m.group(2)),
                                              int(m.group(3)))
            except ValueError:
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

    ind = independent_extract(html)
    if not check("   independent extractor located the array", ind is not None):
        print("\nFASHION CONTEXT CONTRACT: FAIL (cannot continue)")
        sys.exit(1)
    ind_recs, ind_per_rec, _region = ind
    ind_ids = [g[0] for g in ind_per_rec if g]

    # Record-level structure, independent of the builder entirely.
    check("   every top-level record carries exactly one PM id",
          all(len(g) == 1 for g in ind_per_rec),
          f"idless={sum(1 for g in ind_per_rec if not g)} "
          f"multi={sum(1 for g in ind_per_rec if len(g) > 1)}")
    check("   no id-less top-level record", all(g for g in ind_per_rec),
          f"{sum(1 for g in ind_per_rec if not g)} id-less")

    products = bfc.parse_catalogue(html)
    ids = [p["id"] for p in products]

    check("   independent record count equals builder product count",
          len(ind_recs) == len(products), f"records={len(ind_recs)} products={len(products)}")

    # 2 — non-empty
    check("2. parser output is non-empty", len(products) > 0, f"{len(products)} products")
    # 3 — unique
    check("3. all PM ids are unique", len(set(ids)) == len(ids),
          f"{len(ids) - len(set(ids))} duplicates")
    # 4 — matches the independent view, in order
    check("4. parsed id sequence matches the independent extraction",
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
    check("   catalogueSize equals the independent RECORD count",
          ctx["catalogueSize"] == len(ind_recs),
          f"{ctx['catalogueSize']} vs {len(ind_recs)} records")
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

    print("  -- structural drift (mutation tests) --")
    expect_raise("11. renamed array fails loudly",
                 html.replace(bfc.ARRAY_MARKER, "var SOMETHING_ELSE = ["))
    expect_raise("    empty catalogue fails loudly", "var PINK_MALL_PRODUCTS = [];")
    expect_raise("12. duplicate id fails loudly", _with_duplicate(html, bfc))
    expect_raise("13. truncated array fails loudly — no partial success",
                 _truncated(html, bfc))
    expect_raise("    id-less record fails loudly", _drop_field(html, bfc, 1, "id"))
    expect_raise("    missing-name record fails loudly", _drop_field(html, bfc, 1, "name"))
    expect_raise("    missing-category record fails loudly",
                 _drop_field(html, bfc, 1, "category"))

    # ── cross-record field bleed ──────────────────────────────────────────
    # The defect this replaced: parsing took a fixed 4000-character window from
    # each id match, and every record is shorter than that, so a product
    # missing a field silently inherited the NEXT product's value. Proven here
    # on an OPTIONAL field, because a required one would (correctly) raise
    # before the value could be observed.
    print("  -- cross-record field bleed --")
    real = bfc.parse_catalogue(html)
    # Pick a record that actually carries the optional field, and whose
    # neighbour carries a DIFFERENT value for it — otherwise a bleed would be
    # indistinguishable from a correct read.
    victim = next((i for i in range(len(real) - 1)
                   if real[i]["brand"] and real[i + 1]["brand"]
                   and real[i]["brand"] != real[i + 1]["brand"]), None)
    if victim is None:
        check("    a usable bleed fixture exists", False, "no adjacent pair with distinct brands")
        victim = 0
    donor = victim + 1
    mutated_html = _drop_field(html, bfc, victim, "brand")
    try:
        mutated = bfc.parse_catalogue(mutated_html)
        check("    catalogue still parses with one optional field removed",
              len(mutated) == len(real), f"{len(mutated)} vs {len(real)}")
        got = mutated[victim]["brand"]
        check("    a record missing an optional field yields None, not a value",
              got is None, f"{real[victim]['id']} brand={got!r}")
        check("    the missing field is NOT borrowed from the next record",
              got != real[donor]["brand"],
              f"{real[donor]['id']} brand={real[donor]['brand']!r}, got {got!r}")
        check("    every other record is unaffected by the mutation",
              [q["id"] for q in mutated] == [q["id"] for q in real]
              and all(mutated[i]["brand"] == real[i]["brand"]
                      for i in range(len(real)) if i != victim))
    except bfc.CatalogueError as e:                               # noqa: BLE001
        check("    optional-field mutation parses without raising", False, str(e)[:80])

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

    # Today the two sets can coincide — every newUntil window in the catalogue
    # happens to have closed. That must not be mistaken for the two rules being
    # equivalent, so prove the divergence on a date when a window was open.
    dated_days = sorted({p["newUntil"] for p in dated if p["newUntil"]})
    if dated_days:
        open_day = datetime.date.fromisoformat(dated_days[-1])
        on_open, _r, _l = newin_for(open_day.isoformat())
        raw_on_open = {p["id"] for p in products if p["isNew"]}
        check("    the two rules genuinely differ when a NEW window is open",
              on_open is not None and on_open != raw_on_open,
              f"as of {open_day}: gated={len(on_open or [])} rawFlag={len(raw_on_open)} "
              f"only-gated={sorted((on_open or set()) - raw_on_open)}")

    # ── strict YYYY-MM-DD, for --as-of and for newUntil alike ─────────────
    print("  -- date shape --")
    for bad_date, why in (("2026-13-99", "impossible calendar date"),
                          ("20260915", "no separators"),
                          ("2026-W38-2", "ISO week date"),
                          ("2026-9-15", "single-digit month/day"),
                          ("2026-09-15T00:00:00", "datetime, not a date")):
        rcx, _dx, logx = run_builder(catalogue, bad_date)
        check(f"    --as-of rejects {bad_date} ({why})", rcx != 0,
              (logx.strip().splitlines() or [""])[-1][:70])
    check("    --as-of accepts a well-formed date",
          run_builder(catalogue, datetime.date.today().isoformat())[0] == 0)

    # A newUntil that is not exactly YYYY-MM-DD must fall back to raw isNew,
    # never be coerced into a date. Checked directly against the builder's rule.
    print("  -- malformed newUntil falls back to raw isNew --")
    for bad_nu in ("20260915", "2026-W38-2", "2026-9-15", "2026-09-15T00:00:00",
                   "not-a-date", "2026-13-99"):
        for flag in (True, False):
            got = bfc.is_product_new({"id": "X", "isNew": flag, "newUntil": bad_nu}, today)
            check(f"    newUntil={bad_nu!r} isNew={flag} -> {flag} (fallback)",
                  got is flag, f"got={got}")
    check("    a well-formed future newUntil still overrides isNew=False",
          bfc.is_product_new(
              {"id": "X", "isNew": False,
               "newUntil": (today + datetime.timedelta(days=1)).isoformat()}, today) is True)
    check("    a well-formed past newUntil still overrides isNew=True",
          bfc.is_product_new(
              {"id": "X", "isNew": True,
               "newUntil": (today - datetime.timedelta(days=1)).isoformat()}, today) is False)

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


def _nth_record_span(html, bfc, n):
    """Byte span of the nth (0-based) top-level record in the product array."""
    at = html.index(bfc.ARRAY_MARKER)
    start = html.index("[", at)
    depth, k, quote, esc = 0, start, None, False
    while k < len(html):
        ch = html[k]
        if quote:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                quote = None
        elif ch in "'\"`":
            quote = ch
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                break
        k += 1
    region_start, region_end = start, k + 1
    recs, spans, buf_start, depth = [], [], None, 0
    quote, esc, arr = None, False, 0
    for i in range(region_start, region_end):
        ch = html[i]
        if quote:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                quote = None
            continue
        if ch in "'\"`":
            quote = ch
            continue
        if ch == "[":
            arr += 1
        elif ch == "]":
            arr -= 1
        elif ch == "{":
            if depth == 0 and arr == 1:
                buf_start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and buf_start is not None:
                spans.append((buf_start, i + 1))
                buf_start = None
    return spans[n]


def _drop_field(html, bfc, n, field):
    """Remove one `field: value,` pair from the nth top-level record."""
    a, b = _nth_record_span(html, bfc, n)
    rec = html[a:b]
    pat = re.compile(r"""["']?%s["']?\s*:\s*(?:"[^"]*"|'[^']*'|[^,}]+)\s*,?""" % field)
    m = pat.search(rec)
    if not m:
        raise AssertionError(f"field {field!r} not found in record #{n + 1}")
    return html[:a] + rec[:m.start()] + rec[m.end():] + html[b:]


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
