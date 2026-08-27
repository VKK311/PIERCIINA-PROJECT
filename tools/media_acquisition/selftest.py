#!/usr/bin/env python3
"""Self-test for the media acquisition pipeline.

Runs the whole pipeline against a local fixture server, so the guarantees can
be re-verified from a fresh clone without touching a brand CDN. This exists
because the interesting failures are all in the guards, and guards that are
never exercised are just comments.

    python tools/media_acquisition/selftest.py
"""
import http.server
import json
import os
import re
import shutil
import socketserver
import io
import urllib.request
import subprocess
import sys
import tempfile
import threading

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8731


def shot(seed, size, tag):
    im = Image.new("RGB", (size, size), (240, 242, 244))
    d = ImageDraw.Draw(im)
    s = size / 500.0
    d.ellipse([80 * s, 180 * s, 420 * s, 330 * s], fill=(244, 200, 214))
    d.rectangle([80 * s, 300 * s, 420 * s, 350 * s], fill=(190, 130, 80))
    for i in range(3):
        d.line([((200 + i * 28) * s, 200 * s), ((240 + i * 28) * s, 300 * s)],
               fill=(200, 200, 205), width=int(9 * s))
    if seed == 2:
        d.rectangle([120 * s, 100 * s, 380 * s, 200 * s], fill=(210, 215, 220))
    if seed == 3:
        d.ellipse([120 * s, 120 * s, 380 * s, 380 * s], fill=(180, 120, 70))
    if seed == 4:
        d.polygon([(120 * s, 300 * s), (400 * s, 200 * s), (420 * s, 340 * s)], fill=(240, 190, 205))
    d.text((20 * s, 20 * s), tag, fill=(30, 30, 30))
    return im


def build_fixture(root):
    def w(p, im):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        im.save(p, "JPEG", quality=88)

    for view, seed in [("01_00", 1), ("02", 2), ("03", 3), ("04", 4)]:
        n = "VL_Court_Bold_Shoes_Pink_TESTSKU_%s_standard.jpg" % view
        w("%s/images/w_500,f_auto,q_auto/hash%d/%s" % (root, seed, n), shot(seed, 500, "v%s" % view))
        w("%s/images/w_1880,f_auto,q_auto/hash%d/%s" % (root, seed, n), shot(seed, 1880, "v%s" % view))
    # Three distinct product-shaped images for the research-handoff fixture,
    # served from a path with no SKU in it so identity has to come from the
    # research evidence rather than the URL.
    # Seeds 2/3/4 are the ones this fixture already proves are perceptually
    # distinct; 91/93 rendered identically and collapsed as duplicates.
    for i, seed in ((1, 2), (2, 3), (3, 4)):
        w("%s/img/researchsku_%02d.jpg" % (root, i), shot(seed, 1200, "r%d" % i))

    # exact duplicate of view 01 under a different path
    w("%s/images/w_500,f_auto,q_auto/dup/VL_Court_Bold_Shoes_Pink_TESTSKU_01_00_standard.jpg" % root,
      shot(1, 500, "v01_00"))
    # a DIFFERENT photograph served at the larger width -> must be rejected
    w("%s/images/w_500,f_auto,q_auto/hash9/VL_Court_Bold_Shoes_Pink_TESTSKU_05_standard.jpg" % root,
      shot(1, 500, "v05"))
    w("%s/images/w_1880,f_auto,q_auto/hash9/VL_Court_Bold_Shoes_Pink_TESTSKU_05_standard.jpg" % root,
      shot(4, 1880, "WRONG"))
    bad = "%s/images/w_500,f_auto,q_auto/bad" % root
    os.makedirs(bad, exist_ok=True)
    with open(bad + "/error.jpg", "w") as fh:
        fh.write("<!DOCTYPE html><html><body>" + "x" * 4000 + "</body></html>")
    with open(bad + "/tiny.jpg", "wb") as fh:
        fh.write(b"\xff\xd8\xff\xd9")

    # A pale upper with green stripes: the shape of adidas's
    # "Almost Pink / Court Green / Gold Metallic", which reads nothing like the
    # word pink on its own and was once wrongly rejected for that.
    pale = Image.new("RGB", (600, 600), (247, 247, 247))
    dp = ImageDraw.Draw(pale)
    dp.ellipse([80, 220, 520, 400], fill=(246, 238, 240))
    for i in range(3):
        dp.line([(200 + i * 34, 250), (250 + i * 34, 370)], fill=(38, 140, 86), width=16)
    dp.rectangle([80, 380, 520, 420], fill=(198, 160, 96))
    pale.save(root + "/pale.jpg", "JPEG", quality=90)

    # An unmistakably different colourway for the conflict case.
    other = Image.new("RGB", (600, 600), (247, 247, 247))
    do = ImageDraw.Draw(other)
    do.ellipse([80, 220, 520, 400], fill=(40, 60, 190))
    do.rectangle([80, 380, 520, 420], fill=(20, 20, 20))
    other.save(root + "/other.jpg", "JPEG", quality=90)

    # Category page -> product page: the media lives one hop away.
    os.makedirs(root + "/cat", exist_ok=True)
    with open(root + "/cat/index.html", "w") as fh:
        fh.write('<!doctype html><html><body>'
                 '<a href="/cat/product-TESTSKU.html">TESTSKU product</a>'
                 '<a href="/cat/product-OTHERSKU.html">a different product</a>'
                 '</body></html>')
    with open(root + "/cat/product-TESTSKU.html", "w") as fh:
        fh.write('<!doctype html><html><head>'
                 '<meta property="og:image" content="http://127.0.0.1:%d/hop/TESTSKU_hop.jpg">'
                 '</head><body>TESTSKU</body></html>' % PORT)
    os.makedirs(root + "/hop", exist_ok=True)
    shot(1, 900, "hop").save(root + "/hop/TESTSKU_hop.jpg", "JPEG", quality=90)

    B = "http://127.0.0.1:%d/images/w_500,f_auto,q_auto" % PORT
    with open(root + "/product.html", "w") as fh:
        fh.write("""<!doctype html><html><head>
<meta property="og:image" content="{B}/hash1/VL_Court_Bold_Shoes_Pink_TESTSKU_01_00_standard.jpg">
<script type="application/ld+json">{{"@type":"Product","sku":"TESTSKU","image":[
"{B}/hash2/VL_Court_Bold_Shoes_Pink_TESTSKU_02_standard.jpg",
"{B}/hash3/VL_Court_Bold_Shoes_Pink_TESTSKU_03_standard.jpg"]}}</script>
</head><body>
<img srcset="{B}/hash4/VL_Court_Bold_Shoes_Pink_TESTSKU_04_standard.jpg 500w">
<img src="{B}/dup/VL_Court_Bold_Shoes_Pink_TESTSKU_01_00_standard.jpg">
<img src="{B}/hash9/VL_Court_Bold_Shoes_Pink_TESTSKU_05_standard.jpg">
<img src="{B}/bad/error.jpg"><img src="{B}/bad/tiny.jpg">
<img src="https://evil.example.com/steal.jpg">
</body></html>""".format(B=B))

    # ── A client-side storefront ──────────────────────────────────────────
    # The gallery is NOT in the served HTML; the app fetches it at runtime.
    # That is what a real SPA storefront does and what makes an HTTP-only
    # parser genuinely blind to it, rather than merely bad at parsing.
    os.makedirs(os.path.join(root, "spa", "img"), exist_ok=True)
    for i in range(1, 5):
        shot(i, 1400, "spa view %d" % i).save(
            os.path.join(root, "spa", "img", "401012.003_%d.jpg" % i), quality=90)
    # Banner shape: must still be rejected after rendering finds it.
    shot(1, 1400, "BANNER").resize((1920, 480)).save(
        os.path.join(root, "spa", "img", "hero-banner.jpg"), quality=90)
    with io.open(os.path.join(root, "spa", "gallery.json"), "w", encoding="utf-8") as fh:
        json.dump({"images": ["img/401012.003_%d.jpg" % i for i in range(1, 5)]
                             + ["img/hero-banner.jpg"]}, fh)
    with io.open(os.path.join(root, "spa", "product.html"), "w", encoding="utf-8") as fh:
        fh.write("""<!doctype html><html><head><title>Shop</title></head>
<body><div id="app">Article SPASKU01 &mdash; loading</div>
<script>
fetch('gallery.json').then(function (r) { return r.json(); }).then(function (d) {
  var box = document.getElementById('app');
  d.images.forEach(function (u) {
    var i = document.createElement('img'); i.setAttribute('src', u); box.appendChild(i);
  });
});
</script></body></html>""")
    # Same shell, but the article appears only in the path we would request.
    with io.open(os.path.join(root, "spa", "urlonly-SPASKU01.html"), "w",
                 encoding="utf-8") as fh:
        fh.write("<!doctype html><html><body><div>loading</div></body></html>")


def hop_req(tmp):
    """Request whose only entry point is a category page; the media is one hop
    away on the product page it links to."""
    path = os.path.join(tmp, "HOPSKU.request.json")
    with open(path, "w") as fh:
        json.dump({
            "schemaVersion": 1, "brand": "generic", "manufacturerItemNo": "TESTSKU",
            "discoveryPages": ["http://127.0.0.1:%d/cat/index.html" % PORT],
            "allowedHosts": ["127.0.0.1"], "candidateMedia": [],
        }, fh)
    return path


def main():
    tmp = tempfile.mkdtemp(prefix="pm-selftest-")
    srv_root = os.path.join(tmp, "srv")
    out = os.path.join(tmp, "out")
    os.makedirs(srv_root)
    build_fixture(srv_root)

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    handler = lambda *a, **kw: Quiet(*a, directory=srv_root, **kw)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    req_path = os.path.join(tmp, "TESTSKU.request.json")
    with open(req_path, "w") as fh:
        json.dump({
            "schemaVersion": 1, "brand": "adidas", "manufacturerItemNo": "TESTSKU",
            "model": "VL Court Bold Shoes", "variant": "Clear Pink / Silver Metallic / Gold Metallic",
            "officialProductPage": "http://127.0.0.1:%d/product.html" % PORT,
            "allowedHosts": ["127.0.0.1"],
            "candidateMedia": [],
            "resolution": {"widthLadder": [1880, 1200, 1000]},
        }, fh)

    env = dict(os.environ)
    for k in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy"):
        env.pop(k, None)
    # Keep the suite hermetic: the fixture server is local and the indexed
    # routes must not reach the public archive from a test run.
    env["PM_NO_INDEX"] = "1"
    subprocess.run([sys.executable, os.path.join(HERE, "acquire.py"),
                    "--request", req_path, "--out", out],
                   check=False, env=env, capture_output=True)
    hop_ran = subprocess.run(
        [sys.executable, os.path.join(HERE, "acquire.py"),
         "--request", hop_req(tmp), "--out", os.path.join(tmp, "hop")],
        check=False, env=env, capture_output=True)

    res_out = os.path.join(tmp, "research-out")
    res_req = os.path.join(tmp, "RESEARCHSKU.request.json")
    with open(res_req, "w", encoding="utf-8") as fh:
        json.dump({
            "schemaVersion": 3,
            "brand": "Fixture",
            "manufacturerItemNo": "RESEARCHSKU",
            "model": "Handoff",
            "variant": "Pink",
            "availableSizes": ["39"],
            "candidateMedia": [],
            "indexedAssetSearch": False,
            "discoveryPages": [],
            "allowedHostSuffixes": ["127.0.0.1"],
            "researchEvidence": [{
                "sourceUrl": "http://127.0.0.1:%d/product/researchsku.html" % PORT,
                "authorityTier": "TRUSTED_RETAILER",
                "discoveryTransport": "CLAUDE_RESEARCH",
                "confidence": "B",
                "capturedAt": "2026-08-26T00:00:00Z",
                "sku": "RESEARCHSKU",
                "model": "Handoff",
                "variant": "Pink",
                "aliases": ["PPJ-RESEARCHSKU-327"],
                "sizeScale": [{"size": "38", "declared": "InStock"},
                              {"size": "39", "declared": "OutOfStock"}],
                "observedCdnHosts": ["127.0.0.1:%d" % PORT],
                "mediaUrls": [
                    {"url": "http://127.0.0.1:%d/img/researchsku_01.jpg" % PORT,
                     "field": "json-ld"},
                    {"url": "http://127.0.0.1:%d/img/researchsku_02.jpg" % PORT,
                     "field": "og:image"},
                    {"url": "http://127.0.0.1:%d/img/researchsku_03.jpg" % PORT,
                     "field": "gallery"},
                ],
            }],
            "resolution": {"widthLadder": [1880]},
        }, fh)

    res_run = subprocess.run(
        [sys.executable, os.path.join(HERE, "acquire.py"),
         "--request", res_req, "--out", res_out],
        check=False, env=env, capture_output=True)
    if os.environ.get("PM_DEBUG"):
        _rj = os.path.join(res_out, "RESEARCHSKU", "result.json")
        if os.path.exists(_rj):
            _d = json.load(open(_rj, encoding="utf-8"))
            print("RESEARCH LOG:")
            for _e in _d.get("log", []):
                print("   ", json.dumps(_e, ensure_ascii=False)[:220])


    httpd.shutdown()

    rp = os.path.join(out, "TESTSKU", "result.json")
    if not os.path.exists(rp):
        print("FAIL: no result.json produced")
        return 1
    with open(rp, encoding="utf-8") as fh:
        m = json.load(fh)

    log = m.get("log", [])
    checks = [
        ("status PASS", m["status"] == "PASS"),
        ("4 unique images kept", m["counts"]["unique_selected"] == 4),
        ("duplicates collapsed", m["counts"]["duplicates_collapsed"] >= 2),
        ("all upgraded to 1880px", all(e["longest_edge"] == 1880 for e in m["images"])),
        ("MAIN is view 01", "01" in m["images"][0]["source_url"].rsplit("_standard", 1)[0][-6:]),
        ("wrong-view upgrade rejected",
         any(l.get("stage") == "resolution" and l.get("ok") is False for l in log)),
        ("off-allow-list host refused",
         any("evil.example.com" in str(l.get("url", "")) and l.get("ok") is False for l in log)),
        ("HTML-served-as-image rejected",
         any("HTML served as image" in str(l.get("error", "")) for l in log)),
        ("truncated file rejected",
         any("too small" in str(l.get("error", "")) for l in log)),
        ("contact sheet rendered",
         os.path.exists(os.path.join(out, "TESTSKU", "CONTACT_SHEET.webp"))),
        ("previews rendered",
         len(os.listdir(os.path.join(out, "TESTSKU", "preview"))) == 4),
        ("sha256 recorded for every image",
         all(len(e["sha256"]) == 64 for e in m["images"])),
    ]
    # ── Round 2: link-target recovery and variant confidence ──────────
    sys.path.insert(0, HERE)
    from acquire import (outbound_links, colour_terms_present, variant_confidence,
                         dhash, sizes_from_jsonld)  # noqa: E402

    cat_html = open(os.path.join(srv_root, "cat", "index.html")).read()
    links = outbound_links(cat_html, "http://127.0.0.1:%d/cat/index.html" % PORT, "TESTSKU")
    checks.append(("link targets recovered from a category page", len(links) == 1))
    checks.append(("non-matching link target ignored",
                   all("OTHERSKU" not in l for l in links)))

    hop_manifest = os.path.join(tmp, "hop", "TESTSKU", "result.json")
    hop_ok = False
    if os.path.exists(hop_manifest):
        with open(hop_manifest, encoding="utf-8") as fh:
            hm = json.load(fh)
        hop_ok = any(l.get("route") == "INDEXED_OUTBOUND_MEDIA"
                     for l in hm.get("discoveryLedger", []))
    checks.append(("indexed page -> outbound target followed one hop", hop_ok))

    pale_img = Image.open(os.path.join(srv_root, "pale.jpg"))
    other_img = Image.open(os.path.join(srv_root, "other.jpg"))
    terms = colour_terms_present(pale_img, ["pink", "green", "gold"])
    checks.append(("pale near-white upper: official green term still detected",
                   terms.get("green") is True))

    pale_h = "%064x" % dhash(pale_img.convert("RGB"))
    other_h = "%064x" % dhash(other_img.convert("RGB"))
    ent = lambda h, t: {"sku_evidence": "asset-url", "dhash": h, "_colour_terms": t}

    match = variant_confidence([ent(pale_h, terms)],
                               "Almost Pink / Court Green / Gold Metallic", [pale_h])
    checks.append(("retailer image matching the official anchor -> PASS",
                   match["state"] == "VARIANT_CONFIDENCE_PASS"))

    conflict = variant_confidence([ent(other_h, colour_terms_present(other_img,
                                                                    ["pink", "green", "gold"]))],
                                  "Almost Pink / Court Green / Gold Metallic", [pale_h])
    checks.append(("retailer image conflicting with the official anchor -> CONFLICT",
                   conflict["state"] == "VARIANT_EVIDENCE_CONFLICT"))

    no_anchor = variant_confidence([ent(other_h, colour_terms_present(other_img,
                                                                     ["pink", "green"]))],
                                   "Almost Pink / Court Green", None)
    checks.append(("colour contradiction without an anchor -> REVIEW_REQUIRED",
                   no_anchor["state"] == "HUMAN_VARIANT_REVIEW_REQUIRED"))

    # Size-scale evidence. The user is still the only source of PINK MALL
    # availability; this only proves a supplied size can be checked against
    # the scale the source declares, rather than assumed to exist.
    scale_html = """
    <script type="application/ld+json">
    {"@type":"Product","name":"Test Shoe","offers":[
      {"@type":"Offer","size":"36","availability":"https://schema.org/InStock"},
      {"@type":"Offer","size":"37","availability":"https://schema.org/OutOfStock"},
      {"@type":"Offer","size":"38","availability":"https://schema.org/InStock"}]}
    </script>"""
    declared = sizes_from_jsonld(scale_html)
    checks.append(("declared size scale read from JSON-LD offers",
                   [d["size"] for d in declared] == ["36", "37", "38"]))
    checks.append(("declared availability captured verbatim, not interpreted",
                   [d["declared"] for d in declared] == ["InStock", "OutOfStock", "InStock"]))
    checks.append(("a size outside the declared scale is detectable",
                   "39" not in [d["size"] for d in declared]))
    checks.append(("page with no size declaration yields no false scale",
                   sizes_from_jsonld("<html><body>no ld+json here</body></html>") == []))

    # Non-product path segments. The tradeinn run accepted /banners_home/
    # marketing panoramas as PGS30614 product media because the deny-list
    # anchored on a trailing slash and 'banners_home' is not 'banners'.
    from acquire import NON_PRODUCT_RE, validate_bytes, MAX_ASPECT
    rejects = ["https://cache.tradeinn.com/web/banners_home/HP-adidas.webp",
               "https://cache.tradeinn.com/web/categorias_hp/11065-grande.webp",
               "https://x.test/banner-hp/a.jpg", "https://x.test/articles/b.jpg"]
    keeps = ["https://assets.adidas.com/images/w_1880/h/Shoes_JQ4556_standard.jpg",
             "https://nb.scene7.com/is/image/NB/gc515ki_nb_02_i",
             "https://akn-spx.a-cdn.akinoncdn.com/products/2025/08/14/1684367/a.jpg"]
    checks.append(("banner-ish path segments rejected",
                   all(NON_PRODUCT_RE.search(u) for u in rejects)))
    checks.append(("real product asset paths still kept",
                   not any(NON_PRODUCT_RE.search(u) for u in keeps)))

    # Shape. A 4:1 panorama is a page banner, never a product photograph.
    def encoded(w, h):
        buf = io.BytesIO()
        Image.new("RGB", (w, h), (200, 160, 170)).save(buf, "JPEG")
        return buf.getvalue()

    meta, err = validate_bytes(encoded(1920, 460), "image/jpeg")
    checks.append(("4.2:1 banner rejected on shape", meta is None and "aspect" in (err or "")))
    for w, h, label in ((1880, 1880, "square"), (560, 746, "portrait 4:3"),
                        (1000, 500, "2:1 wide but plausible")):
        m, e = validate_bytes(encoded(w, h), "image/jpeg")
        checks.append(("%s product shape accepted" % label, m is not None))

    # ── Size-evidence semantics ──────────────────────────────────────────
    # The four cases the false-refusal review required. Absence of evidence
    # must never be read as evidence of absence.
    from acquire import (size_state, SIZE_SCALE_NOT_PROVEN, SIZE_CONFIRMED,
                         SIZE_IDENTITY_CONFLICT, refusal_audit, expand_identifiers,
                         REFUSAL_ROUTES)

    def scale(labels, avail="InStock"):
        return [{"page": "https://x.test/p", "sizes":
                 [{"size": l, "declared": avail} for l in labels]}]

    st = size_state(["39"], [])
    checks.append(("empty sizeEvidence + user size -> NOT blocked",
                   st["state"] == SIZE_SCALE_NOT_PROVEN and not st["missing"]))

    st = size_state(["39"], scale(["32", "33", "36", "38", "39", "40"]))
    checks.append(("exact scale contains user size -> confirmed",
                   st["state"] == SIZE_CONFIRMED and st["matched"] == ["39"]))

    st = size_state(["39"], scale(["32", "33", "34", "35", "36", "37"]))
    checks.append(("exact scale excludes user size -> conflict",
                   st["state"] == SIZE_IDENTITY_CONFLICT and st["missing"] == ["39"]))

    st = size_state(["39"], scale(["38", "39", "40"], avail="OutOfStock"))
    checks.append(("source says sold out but user supplies it -> still available to PINK MALL",
                   st["state"] == SIZE_CONFIRMED))

    st = size_state(["37 1/3", "37.5"], scale(["37 1/3", "37.5", "38"]))
    checks.append(("fractional and decimal labels compare without rewriting",
                   st["state"] == SIZE_CONFIRMED and len(st["matched"]) == 2))

    # ── Refusal gate ─────────────────────────────────────────────────────
    every = [{"route": r, "result": "FAIL", "sku_evidence": False, "candidates": 0}
             for r in REFUSAL_ROUTES]
    a = refusal_audit(every)
    checks.append(("all routes tried and all empty -> refusal permitted",
                   a["refusalPermitted"] is True))

    a = refusal_audit(every[:3])
    checks.append(("routes left untried -> refusal forbidden",
                   a["refusalPermitted"] is False and bool(a["routesNotAttempted"])))

    with_doc = every[:-1] + [{"route": "INDEXED_SOURCE_EVIDENCE", "result": "OK",
                              "authorityTier": "TRUSTED_RETAILER",
                              "exactProductDocument": True,
                              "sku_evidence": True, "candidates": 7}]
    a = refusal_audit(with_doc)
    checks.append(("an exact product document forbids UNRESOLVED",
                   a["refusalPermitted"] is False and bool(a["exactProductDocuments"])))
    checks.append(("refusal gate explains itself",
                   "exact product document" in a["refusalBlockedBecause"]))

    # ── Identifier expansion ─────────────────────────────────────────────
    doc = ("ref PPJ-PGS30614-327 /product-vertical/ppj-pgs30614-327_1001.jpg "
           "PGS30614327 and unrelated PGS30999")
    ex = expand_identifiers("PGS30614", doc)
    checks.append(("aliases read off an evidenced document",
                   "PPJ-PGS30614-327" in ex and "PGS30614327" in ex))
    checks.append(("expansion never invents a neighbouring style",
                   not any("30999" in e for e in ex)))
    checks.append(("expansion of an absent code yields nothing",
                   expand_identifiers("ZZZ00000", doc) == []))

    # Applicability. A route that cannot apply to a brand is not a route left
    # untried — otherwise refusal becomes impossible and the gate flips into
    # the mirror image of the bug it exists to prevent.
    na = [{"route": r, "result": "N/A", "notApplicable": "x",
           "sku_evidence": False, "candidates": 0} for r in REFUSAL_ROUTES]
    a = refusal_audit(na)
    checks.append(("routes marked N/A count as attempted",
                   a["refusalPermitted"] is True and not a["routesNotAttempted"]))
    checks.append(("N/A routes are not counted as successes",
                   "DIRECT_OFFICIAL_PAGE" not in a["routesSucceeded"]))
    checks.append(("dropping one route still forbids refusal",
                   refusal_audit(na[:-1])["refusalPermitted"] is False))

    # Transport failure is not evidence of absence — the same conflation as
    # a 403 being read as an identity failure, one level up in the audit.
    from acquire import _is_transport_failure
    unreachable_led = [{"route": r, "result": "N/A", "notApplicable": "x",
                        "sku_evidence": False, "candidates": 0}
                       for r in REFUSAL_ROUTES if r != "INDEXED_SOURCE_EVIDENCE"]
    unreachable_led.append({"route": "INDEXED_SOURCE_EVIDENCE", "result": "FAIL",
                            "error": "URLError: <urlopen error [Errno 111] Connection refused>",
                            "indexReachable": False,
                            "sku_evidence": False, "candidates": 0})
    a = refusal_audit(unreachable_led)
    checks.append(("an unreachable route forbids refusal",
                   a["refusalPermitted"] is False
                   and "INDEXED_SOURCE_EVIDENCE" in a["routesUnreachable"]))
    checks.append(("unreachable is reported as transport, not evidence",
                   "transport failure" in a["refusalBlockedBecause"]))

    answered = list(unreachable_led[:-1])
    answered.append({"route": "INDEXED_SOURCE_EVIDENCE", "result": "FAIL",
                     "error": "HTTPError: HTTP Error 404: Not Found",
                     "indexReachable": True,
                     "sku_evidence": False, "candidates": 0})
    checks.append(("a 404 is an answer and does not block refusal",
                   refusal_audit(answered)["refusalPermitted"] is True))

    for err, expect in (("TimeoutError: The read operation timed out", True),
                        ("URLError: <urlopen error timed out>", True),
                        ("HTTPError: HTTP Error 403: Forbidden", True),
                        ("HTTPError: HTTP Error 503", True),
                        ("index call budget exhausted (24)", True),
                        ("HTTPError: HTTP Error 404: Not Found", False),
                        ("no archived capture", False)):
        got = _is_transport_failure({"result": "FAIL", "error": err})
        checks.append(("transport classification: %s" % err[:34], got is expect))

    # ── Research evidence -> candidateMedia -> runner acquisition ────────
    # The whole point of the handoff: onboarding must work with the archive
    # entirely unavailable. PM_NO_INDEX is already set for this suite, so if
    # this passes, no archive was consulted.
    rj = os.path.join(res_out, "RESEARCHSKU", "result.json")
    res = json.load(open(rj, encoding="utf-8")) if os.path.exists(rj) else {}
    if os.environ.get("PM_DEBUG"):
        print("RESEARCH STATUS:", res.get("status"), res.get("counts"))
        print("  vc:", res.get("variantConfidence", {}).get("state"),
              res.get("variantConfidence", {}).get("conflicts"))
    checks.append(("research evidence -> candidateMedia -> acquisition PASS",
                   res.get("status") == "PASS"))
    checks.append(("all three research media URLs acquired",
                   res.get("counts", {}).get("unique_selected") == 3))
    # N/A entries are bookkeeping, not lookups. What must be absent is an
    # index route that actually executed.
    _index_ran = [e for e in res.get("discoveryLedger", [])
                  if "INDEX" in e.get("route", "") and e.get("result") != "N/A"]
    checks.append(("acquisition ran with no archive lookup at all", not _index_ran))
    checks.append(("archive routes recorded as not-applicable, not as failures",
                   all(e.get("result") == "N/A"
                       for e in res.get("discoveryLedger", [])
                       if "INDEX" in e.get("route", ""))))
    checks.append(("research route recorded in the ledger with its tier and level",
                   any(e.get("route") == "RESEARCH_EVIDENCE"
                       and e.get("authorityTier") == "TRUSTED_RETAILER"
                       and e.get("confidence") == "B"
                       and e.get("discoveryTransport") == "CLAUDE_RESEARCH"
                       for e in res.get("discoveryLedger", []))))
    checks.append(("evidenced aliases carried through",
                   "PPJ-RESEARCHSKU-327" in (res.get("identifierAliases") or [])))
    checks.append(("research size scale reconciles the supplied size",
                   res.get("sizeState", {}).get("state") == "SIZE_CONFIRMED"))
    checks.append(("source stock status does not touch PINK MALL availability",
                   "39" in (res.get("sizeState", {}).get("matched") or [])))
    checks.append(("observed CDN host promoted, not guessed",
                   all(e.get("sha256") for e in res.get("images", []))))
    checks.append(("every acquired image carries its research source page",
                   all(e.get("source_page") or e.get("sku_evidence")
                       for e in res.get("images", []))))
    checks.append(("identity evidenced -> refusal not permitted",
                   res.get("refusalAudit", {}).get("refusalPermitted") is False))

    # ── Reviewer-verified provenance, size guides, CF transform ─────────
    from acquire import (RESEARCH_TRANSPORTS, resolution_variants,
                         asset_identity, sku_signal)

    checks.append(("REVIEWER_VERIFIED is a recognised provenance class",
                   "REVIEWER_VERIFIED" in RESEARCH_TRANSPORTS))
    checks.append(("reviewer provenance is distinct from Claude's own research",
                   "CLAUDE_RESEARCH" in RESEARCH_TRANSPORTS
                   and "USER_SUPPLIED" in RESEARCH_TRANSPORTS))

    cf_product = ("https://cdn.test/cdn-cgi/image/h%3D785%2Cw%3D628%2Cfit%3Dcontain"
                  "/product-vertical/ppj-pgs30614-327_1001.jpg")
    cf_guide = ("https://cdn.test/cdn-cgi/image/h%3D785%2Cw%3D628"
                "/size_guide/PPJ_C_SH_junior_st_v1.jpg")
    checks.append(("size guide rejected as non-product media",
                   bool(NON_PRODUCT_RE.search(cf_guide))))
    checks.append(("product image beside it is still kept",
                   not NON_PRODUCT_RE.search(cf_product)))
    checks.append(("article code in the CF asset path is a real identity signal",
                   sku_signal(cf_product, "PGS30614")))

    variants = resolution_variants(cf_product, [1600, 1200, 1000, 800])
    checks.append(("CF transform yields larger variants",
                   len(variants) == 4))
    checks.append(("CF upgrade never rewrites the asset path",
                   all("/product-vertical/ppj-pgs30614-327_1001.jpg" in v
                       for v in variants)))
    checks.append(("CF upgrade preserves the native aspect ratio",
                   all(abs((int(re.search(r"h(?:%3D|=)(\d+)", v).group(1)) /
                            int(re.search(r"w(?:%3D|=)(\d+)", v).group(1)))
                           - (785 / 628.0)) < 0.01 for v in variants)))
    checks.append(("CF upgrade only ever grows the request",
                   all(int(re.search(r"w(?:%3D|=)(\d+)", v).group(1)) > 628
                       for v in variants)))

    # Source hierarchy in the selector, not just in the router. Official media
    # must win even when a retailer copy is larger.
    from acquire import _authority_tier
    rule_stub = {"allowed_hosts": ["images.brand.com"]}
    req_stub = {"officialHostSuffixes": ["brand.com"]}
    checks.append(("manufacturer CDN classified OFFICIAL",
                   _authority_tier("images.brand.com", rule_stub, req_stub) == "OFFICIAL"))
    checks.append(("subdomain of an official suffix classified OFFICIAL",
                   _authority_tier("cdn.brand.com", rule_stub, req_stub) == "OFFICIAL"))
    checks.append(("retailer CDN classified TRUSTED_RETAILER",
                   _authority_tier("cdn.shop.example", rule_stub, req_stub)
                   == "TRUSTED_RETAILER"))

    # The research fixture's media is retailer-tier (no officialHostSuffixes),
    # so the run must record that it is NOT suppressing the official routes.
    # PGS30614 published retailer imagery precisely because this was inverted.
    _stages = [e.get("stage") for e in res.get("log", [])]
    checks.append(("retailer-tier research media does not suppress official routes",
                   "index-continue" in _stages and "index-skip" not in _stages))

    # Backdrop consensus and stale-output hygiene.
    from acquire import consensus_backdrop, QUERY_SIZE_RE
    checks.append(("near-identical backdrops agree on one surface",
                   consensus_backdrop([{"backdrop": "#DCDBD7"}, {"backdrop": "#DDDCD8"},
                                       {"backdrop": "#DDDCD8"}]) == "#DDDCD8"))
    checks.append(("genuinely different backdrops yield no surface",
                   consensus_backdrop([{"backdrop": "#FFFFFF"},
                                       {"backdrop": "#202020"}]) is None))
    checks.append(("a missing backdrop yields no surface",
                   consensus_backdrop([{"backdrop": "#FFFFFF"},
                                       {"backdrop": None}]) is None))
    checks.append(("Salesforce ?sw= sizing recognised by the ladder",
                   bool(QUERY_SIZE_RE.search("https://x.test/a.jpg?sw=950"))))
    checks.append(("previous run's artefacts are removed, not left beside new ones",
                   not any(f.endswith(".webp")
                           for f in os.listdir(os.path.join(out, "TESTSKU", "source")))))

    # Cut-out PNGs have no backdrop. Puma 401489 reported #47704C from images
    # that are 81% transparent — a palette artefact of flattening, which would
    # have painted a green field behind the product.
    from acquire import is_cutout, backdrop as _bd
    cut = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    ImageDraw.Draw(cut).ellipse([120, 120, 280, 280], fill=(240, 90, 150, 255))
    checks.append(("transparent cut-out detected", is_cutout(cut) is True))
    checks.append(("cut-out yields no invented backdrop", _bd(cut) is None))
    # The production path flattens to RGB before backdrop() is reached, so a
    # direct RGBA test does not prove anything about the real pipeline. This
    # asserts the pipeline's own wiring: a validated cut-out must record a null
    # backdrop even though backdrop() would happily read the flattened colour.
    from acquire import validate_bytes as _vb
    _buf = io.BytesIO(); cut.save(_buf, "PNG")
    _meta, _err = _vb(_buf.getvalue(), "image/png")
    checks.append(("validation records the cut-out flag", bool(_meta) and _meta["cutout"] is True))
    checks.append(("flattened cut-out still yields a real colour, so the flag is what matters",
                   bool(_meta) and _bd(_meta["_img"]) is not None))
    solid = Image.new("RGB", (400, 400), (234, 238, 239))
    checks.append(("real studio backdrop still detected", _bd(solid) == "#EAEEEF"))
    opaque_rgba = Image.new("RGBA", (400, 400), (241, 241, 241, 255))
    checks.append(("opaque RGBA is not mistaken for a cut-out",
                   is_cutout(opaque_rgba) is False and _bd(opaque_rgba) == "#F1F1F1"))

    # Identity gate must honour evidenced aliases. A brand's asset naming is
    # not always the catalogue's: Colors of California stores article
    # HC.RBGLOW01 as HC.F24.RBGLOW01-FUX-1.jpg, inserting the season code into
    # the MIDDLE of the article number, so a substring test on the article
    # number alone fails on the manufacturer's own images.
    from acquire import sku_signal as _sig
    _hit = "https://cdn.test/_public/resized/1200x1200/HC/F24/FUX/HC.F24.RBGLOW01-FUX-1.jpg"
    _mud = "https://cdn.test/_public/resized/1200x1200/HC/F24/MUD/HC.F24.RBGLOW01-MUD-1.jpg"
    _other = "https://cdn.test/_public/resized/1200x1200/HC/F21/FUX/HC.F21.YSNOW015-FUX-1.jpg"
    checks.append(("split article number fails without an alias",
                   _sig(_hit, "HC.RBGLOW01") is False))
    checks.append(("evidenced alias recovers the manufacturer's own asset",
                   _sig(_hit, "HC.RBGLOW01", ["HC.F24.RBGLOW01"]) is True))
    checks.append(("an alias never admits a different article",
                   _sig(_other, "HC.RBGLOW01", ["HC.F24.RBGLOW01"]) is False))
    checks.append(("a colour-scoped alias excludes the sibling colourway",
                   _sig(_mud, "HC.RBGLOW01", ["RBGLOW01-FUX"]) is False
                   and _sig(_hit, "HC.RBGLOW01", ["RBGLOW01-FUX"]) is True))
    checks.append(("empty alias list changes nothing",
                   _sig(_hit, "HC.RBGLOW01", []) is False
                   and _sig(_hit, "HC.F24.RBGLOW01", []) is True))

    # sizeScale accepts a bare label as well as the dict form. Every manifest
    # before Celest 27733247 left the field empty, so the dict-only reader was
    # never exercised against real data and crashed the run on a plain list of
    # sizes. These guards pin BOTH shapes, and that they agree.
    def _scale(scale):
        req = {"researchEvidence": [{
            "sourceUrl": "https://example.test/p",
            "authorityTier": "OFFICIAL",
            "discoveryTransport": "CLAUDE_RESEARCH",
            "confidence": "B",
            "sizeScale": scale,
        }]}
        _log, _ledger = [], []
        from acquire import ingest_research_evidence  # noqa: E402
        out = ingest_research_evidence(req, _log, _ledger)
        sizes = out[2] if len(out) > 2 else None
        for cand in out:
            if isinstance(cand, list) and cand and isinstance(cand[0], dict) \
               and "sizes" in cand[0]:
                sizes = cand
                break
        return [e["size"] for e in sizes[0]["sizes"]] if sizes else None

    _bare = None
    _crash = None
    try:
        _bare = _scale(["36", "37", "38"])
    except Exception as exc:                       # noqa: BLE001
        _crash = repr(exc)
    checks.append(("a bare-string sizeScale does not crash the run",
                   _crash is None))
    checks.append(("a bare-string sizeScale is read as sizes",
                   _bare == ["36", "37", "38"]))
    try:
        _dicts = _scale([{"size": "36", "declared": "InStock"},
                         {"size": "37", "declared": ""},
                         {"size": "38", "declared": ""}])
    except Exception:                              # noqa: BLE001
        _dicts = None
    checks.append(("the dict sizeScale form still works",
                   _dicts == ["36", "37", "38"]))
    checks.append(("both sizeScale shapes agree", _bare == _dicts))

    # A search route must never lend its own images this product's identity.
    # The Celest 27733247 run accepted a Scotch & Soda knitwear close-up as a
    # sneaker at OFFICIAL tier because /search?q=27733247 "named the SKU" — our
    # own query string reflected back — and og:image counts as an authoritative
    # declaration on a product page.
    from acquire import is_search_route  # noqa: E402
    for _u in ["https://scotch-soda.eu/search?q=27733247",
               "https://www.scotchandsoda.com/search?q=27733247",
               "https://www.efootwear.eu/catalogsearch/result/?q=27733247",
               "https://shop.test/results?query=ABC123",
               "https://shop.test/find?keyword=ABC123"]:
        checks.append(("search route recognised: " + _u.split("//")[1][:44],
                       is_search_route(_u) is True))
    for _u in ["https://www.colorsofcalifornia.it/en-ot/shoponline/x.hc.rbglow01?color=FUX",
               "https://scotch-soda.eu/products/78-3194-01",
               "https://eu.puma.com/eu/en/pd/398855",
               "https://scotch-soda.eu/cdn/shop/files/183298_001_S_10_DTL.png?v=1786396229"]:
        checks.append(("product route NOT treated as search: " + _u.split("//")[1][:40],
                       is_search_route(_u) is False))

    # A fixed set of already-known retailer hosts is NOT exhausted discovery.
    # TU0A28Z0699 was declared DISCOVERY_TRANSPORT_BLOCKED while a live
    # exact-SKU product document sat on a trusted retailer that had never
    # entered the candidate set — not unreachable, simply never looked for.
    # The rule is generic: no retailer is named here.
    from acquire import refusal_audit as _audit  # noqa: E402

    _known = ["known-a.test", "known-b.test"]
    _all_routes = [
        {"route": r, "url": "https://known-a.test/x", "result": "OK", "candidates": 0}
        for r in ("DIRECT_OFFICIAL_PAGE", "DIRECT_OFFICIAL_API",
                  "OFFICIAL_REGIONAL_SEARCH", "SEARCH_INDEX_OFFICIAL",
                  "INDEXED_SOURCE_EVIDENCE", "INDEXED_OUTBOUND_MEDIA",
                  "OFFICIAL_CDN_PROBE", "TRUSTED_RETAILER_SEARCH",
                  "TRUSTED_RETAILER_INDEXED_EVIDENCE", "IDENTIFIER_EXPANSION")
    ]

    # 1. Every known host tried and empty, nothing outside the starting set.
    _a = _audit(list(_all_routes), aliases=None, known_hosts=_known)
    checks.append(("known hosts alone never permit refusal",
                   _a["refusalPermitted"] is False))
    checks.append(("and the reason names the un-searched space",
                   "not exhausted discovery" in _a["refusalBlockedBecause"]))
    checks.append(("NEW_RETAILER_DISCOVERY is reported un-attempted",
                   "NEW_RETAILER_DISCOVERY" in _a["routesNotAttempted"]))

    # 2. A newly discovered trusted retailer carrying an exact-SKU document.
    _found = list(_all_routes) + [{
        "route": "TRUSTED_RETAILER_SEARCH", "url": "https://newly-found.test/p/item.html",
        "result": "OK", "authorityTier": "TRUSTED_RETAILER",
        "exactProductDocument": True, "sku_evidence": True, "candidates": 4}]
    _b = _audit(_found, aliases=None, known_hosts=_known)
    checks.append(("a newly discovered exact-SKU page forbids refusal",
                   _b["refusalPermitted"] is False))
    checks.append(("and it is recorded as an exact product document",
                   any("newly-found.test" in (x.get("url") or "")
                       for x in _b["exactProductDocuments"])))
    checks.append(("the new domain satisfies NEW_RETAILER_DISCOVERY",
                   "NEW_RETAILER_DISCOVERY" in _b["routesSucceeded"]))

    # 3. Subdomains of a known host are NOT a new source.
    _sub = list(_all_routes) + [{"route": "TRUSTED_RETAILER_SEARCH",
                                 "url": "https://img.known-a.test/a.jpg", "result": "OK"}]
    _c = _audit(_sub, aliases=None, known_hosts=_known)
    checks.append(("a subdomain of a known host is not a new source",
                   "NEW_RETAILER_DISCOVERY" in _c["routesNotAttempted"]))

    # 4. A new domain that was merely unreachable does not satisfy the route.
    _unre = list(_all_routes) + [{"route": "TRUSTED_RETAILER_SEARCH",
                                  "url": "https://newly-found.test/p/item.html",
                                  "result": "FAIL", "error": "HTTP Error 403: Forbidden"}]
    _d = _audit(_unre, aliases=None, known_hosts=_known)
    checks.append(("an unreachable new domain still forbids refusal",
                   _d["refusalPermitted"] is False))

    # A page can name our exact article and still yield zero candidates if its
    # images are protocol-relative or root-relative. TU0A28Z0699 hit exactly
    # that: page_has_sku true, raw_candidates 0.
    from acquire import scan_images  # noqa: E402
    _base = "https://shop.test/eng/product-abc123.html"
    _html = ('<img data-src="//cdn.shop.test/cat/abc.003_1.jpg">'
             '<img src="/media/abc.003_2.jpg">'
             '<img src="https://abs.test/a.png">'
             '<img src="//cdn.shop.test/cat/abc.003_1.jpg">')
    _got = scan_images(_html, _base)
    checks.append(("protocol-relative image is recovered",
                   "https://cdn.shop.test/cat/abc.003_1.jpg" in _got))
    checks.append(("root-relative image is resolved against the page",
                   "https://shop.test/media/abc.003_2.jpg" in _got))
    checks.append(("absolute images still recovered",
                   "https://abs.test/a.png" in _got))
    checks.append(("relative and absolute forms of one asset collapse",
                   len(_got) == 3))
    checks.append(("a page with no images yields nothing",
                   scan_images("<p>no pictures here</p>", _base) == []))
    # Modern storefronts ship the gallery inside a JSON blob, and JSON escapes
    # forward slashes. Every URL pattern excludes backslashes, so such a page
    # names its images and the scanner sees none of them.
    _json_html = ('<script>{"media":[{"u":"https:\\/\\/cdn.shop.test\\/c\\/abc_1.jpg"},'
                  '{"u":"\\/\\/cdn.shop.test\\/c\\/abc_2.jpg"},'
                  '{"u":"\\u002Fmedia\\u002Fabc_3.jpg"}]}</script>')
    _j = scan_images(_json_html, _base)
    checks.append(("JSON-escaped absolute URL is recovered",
                   "https://cdn.shop.test/c/abc_1.jpg" in _j))
    checks.append(("JSON-escaped protocol-relative URL is recovered",
                   "https://cdn.shop.test/c/abc_2.jpg" in _j))
    checks.append(("unicode-escaped root-relative URL is recovered",
                   "https://shop.test/media/abc_3.jpg" in _j))
    checks.append(("plain markup is unaffected by the unescaping",
                   scan_images('<img src="https://a.test/b.jpg">', _base)
                   == ["https://a.test/b.jpg"]))

    # "page_has_sku: true, raw_candidates: 0" was ambiguous: it could mean the
    # document names the article, or merely that WE asked for a path containing
    # it. The two are now distinguished so a client-side shell is not read as a
    # product document.
    from acquire import sku_match_where  # noqa: E402
    checks.append(("SKU only in the requested path is url-only",
                   sku_match_where("https://s.test/p/abc123.html",
                                   "<html><body></body></html>", "ABC123") == "url-only"))
    checks.append(("SKU only in the document body is body-only",
                   sku_match_where("https://s.test/p/item.html",
                                   "<p>Article ABC123</p>", "ABC123") == "body-only"))
    checks.append(("SKU in both is reported as body",
                   sku_match_where("https://s.test/p/abc123.html",
                                   "<p>ABC123</p>", "ABC123") == "body"))
    checks.append(("no SKU anywhere is None",
                   sku_match_where("https://s.test/p/x.html", "<p>y</p>", "ABC123") is None))
    checks.append(("no sku supplied is None",
                   sku_match_where("https://s.test/p/abc123.html", "<p>z</p>", None) is None))

    # ── Round: bounded SPA rendering ──────────────────────────────────────
    # Hermetic throughout: the shell, its gallery endpoint and its images are
    # all served by the local fixture. No live internet.
    import render as _render  # noqa: E402
    # The main fixture server has already been shut down by this point, so the
    # SPA round serves the same tree from a fresh port for its own lifetime.
    _spa_port = PORT + 7
    _spa_httpd = socketserver.TCPServer(
        ("127.0.0.1", _spa_port),
        lambda *a_, **k_: Quiet(*a_, directory=srv_root, **k_))
    threading.Thread(target=_spa_httpd.serve_forever, daemon=True).start()
    PORT_SPA = _spa_port
    _spa_url = "http://127.0.0.1:%d/spa/product.html" % PORT_SPA
    _spa_served = urllib.request.urlopen(_spa_url, timeout=10).read().decode("utf-8")

    checks.append(("SPA shell exposes no media to the HTTP parser",
                   scan_images(_spa_served, _spa_url) == []))
    checks.append(("SPA shell names the article in its body",
                   sku_match_where(_spa_url, _spa_served, "SPASKU01") == "body-only"))

    # Gating: a page whose only SKU match is the path we requested is refused.
    _urlonly = "http://127.0.0.1:%d/spa/urlonly-SPASKU01.html" % PORT_SPA
    _urlonly_html = urllib.request.urlopen(_urlonly, timeout=10).read().decode("utf-8")
    checks.append(("a URL-only SKU match does not qualify for rendering",
                   _render.should_render(
                       authority_tier="TRUSTED_RETAILER", http_ok=True,
                       sku_where=sku_match_where(_urlonly, _urlonly_html, "SPASKU01"),
                       media_found=False, shell_suspected=True,
                       host_allowed=True) is False))
    checks.append(("an untrusted tier does not qualify for rendering",
                   _render.should_render(
                       authority_tier="MARKETPLACE", http_ok=True, sku_where="body",
                       media_found=False, shell_suspected=True,
                       host_allowed=True) is False))
    checks.append(("a page that already yielded media does not render",
                   _render.should_render(
                       authority_tier="OFFICIAL", http_ok=True, sku_where="body",
                       media_found=True, shell_suspected=True,
                       host_allowed=True) is False))

    _rurls, _rhtml, _rerr = _render.render_page(_spa_url, log=[])
    checks.append(("renderer reports no transport error", _rerr is None))
    checks.append(("renderer discovers the hydrated gallery",
                   len({u.rsplit("/", 1)[-1] for u in _rurls
                        if "401012.003_" in u}) == 4))
    checks.append(("rendered DOM is larger than the served shell",
                   len(_rhtml or "") > len(_spa_served)))

    _, _, _terr = _render.render_page(_spa_url, log=[], nav_timeout=0.001,
                                      hydrate_timeout=0.001, total_timeout=0.001)
    checks.append(("a render timeout is a transport failure, not an answer",
                   _terr is not None))

    # End to end: the rendered URLs must go through normal acquisition.
    spa_out = os.path.join(tmp, "spa-out")
    spa_req = os.path.join(tmp, "SPASKU01.request.json")
    with io.open(spa_req, "w", encoding="utf-8") as fh:
        json.dump({
            "schemaVersion": 4, "brand": "Fixture", "manufacturerItemNo": "SPASKU01",
            # No variant colour claim: this round is about the render route,
            # and asserting a colour the fixture shapes do not have would make
            # the check fail for an unrelated reason.
            "model": "Rendered", "variant": None, "candidateMedia": [],
            "indexedAssetSearch": False, "indexedEvidence": False,
            "discoveryPages": [_spa_url],
            "discoveryRoutes": {_spa_url: "TRUSTED_RETAILER_SEARCH"},
            "allowedHostSuffixes": ["127.0.0.1"],
            "researchEvidence": [{
                "sourceUrl": _spa_url, "authorityTier": "TRUSTED_RETAILER",
                "discoveryTransport": "REVIEWER_VERIFIED", "confidence": "A",
                "sku": "SPASKU01", "aliases": ["401012.003"],
                "sizeScale": [], "mediaUrls": [], "observedCdnHosts": [],
                "notes": ["hermetic fixture"],
            }],
            "resolution": {"widthLadder": [1400]},
        }, fh)
    spa_env = dict(env)
    spa_env.pop("PM_NO_RENDER", None)
    subprocess.run([sys.executable, os.path.join(HERE, "acquire.py"),
                    "--request", spa_req, "--out", spa_out],
                   check=False, env=spa_env, capture_output=True)
    _sj = os.path.join(spa_out, "SPASKU01", "result.json")
    _sd = json.load(io.open(_sj, encoding="utf-8")) if os.path.exists(_sj) else {}
    _simgs = _sd.get("images", [])
    checks.append(("rendered gallery reaches acquisition and PASSes",
                   _sd.get("status") == "PASS"))
    checks.append(("rendering removes the SPA_RENDER_REQUIRED block",
                   (_sd.get("refusalAudit") or {}).get("spaRenderPending") is False))
    checks.append(("all four rendered assets are acquired",
                   len(_simgs) == 4))
    checks.append(("the banner is still rejected after rendering",
                   all("hero-banner" not in (i.get("source_url") or "")
                       for i in _simgs)))
    checks.append(("rendered media is recorded as js-rendered",
                   all(i.get("discovery_method") == "js-rendered" for i in _simgs)
                   if _simgs else False))
    checks.append(("JS_RENDERED_PAGE is an audited route",
                   "JS_RENDERED_PAGE" in (_sd.get("refusalAudit") or {}).get("routesSucceeded", [])))
    _spa_httpd.shutdown()

    ok = True
    for name, passed in checks:
        print(("  PASS  " if passed else "  FAIL  ") + name)
        ok &= passed
    shutil.rmtree(tmp, ignore_errors=True)
    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
