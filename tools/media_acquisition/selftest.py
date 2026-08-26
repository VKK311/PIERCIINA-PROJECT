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
import shutil
import socketserver
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
    subprocess.run([sys.executable, os.path.join(HERE, "acquire.py"),
                    "--request", req_path, "--out", out],
                   check=False, env=env, capture_output=True)
    hop_ran = subprocess.run(
        [sys.executable, os.path.join(HERE, "acquire.py"),
         "--request", hop_req(tmp), "--out", os.path.join(tmp, "hop")],
        check=False, env=env, capture_output=True)

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

    ok = True
    for name, passed in checks:
        print(("  PASS  " if passed else "  FAIL  ") + name)
        ok &= passed
    shutil.rmtree(tmp, ignore_errors=True)
    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
