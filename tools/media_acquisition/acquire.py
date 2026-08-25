#!/usr/bin/env python3
"""PINK MALL — exact product media acquisition.

Turns a request manifest into validated local image files plus a provenance
manifest. Designed to run on a GitHub-hosted runner, because the Claude
execution container cannot reach brand CDNs (CONNECT 403 at the egress proxy)
while it can always reach GitHub.

Pipeline, deliberately separated so that "we found a URL" is never mistaken
for "we have the bytes":

    discover -> upgrade resolution -> acquire -> validate -> dedupe
             -> select -> derive previews -> contact sheet -> manifest

Usage:
    python acquire.py --request docs/pink-mall/media-requests/JQ4556.request.json
                      --out     docs/pink-mall/media-acquisition
"""

import argparse
import datetime
import hashlib
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brands import brand_rule  # noqa: E402

# ── Guards ────────────────────────────────────────────────────────────────
TIMEOUT = 25
MAX_REDIRECTS = 4
MAX_BYTES = 25 * 1024 * 1024
MIN_BYTES = 1024
MAX_PAGE_BYTES = 6 * 1024 * 1024
MAX_CANDIDATES = 60
OK_MIME = {"image/jpeg", "image/png", "image/webp", "image/avif"}
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Selection thresholds
IDEAL_EDGE = 1600
PREFERRED_EDGE = 1000
MIN_EDGE = 400
DUPLICATE_DISTANCE = 8      # dHash bits; <= is the same shot
MAX_KEEP = 5
MIN_KEEP = 3


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Network ───────────────────────────────────────────────────────────────
class Refused(Exception):
    pass


def _check_url(url, allowed):
    """allowed is (exact_hosts, host_suffixes). Suffixes let a request permit a
    retailer's media subdomains without having to guess their names, while
    still never opening the door to an arbitrary host."""
    exact, suffixes = allowed
    p = urllib.parse.urlsplit(url)
    if p.scheme not in ("http", "https"):
        raise Refused("scheme %r not allowed" % p.scheme)
    host = (p.hostname or "").lower()
    if not host:
        raise Refused("no host")
    if host in exact:
        return host
    for suf in suffixes:
        if host == suf or host.endswith("." + suf):
            return host
    raise Refused("host %s not in allow-list" % host)


class _NoAutoRedirect(urllib.request.HTTPRedirectHandler):
    """Follow redirects manually so every hop is re-checked against the
    allow-list. An open redirect off an official domain must not become a
    way to fetch arbitrary bytes."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_opener = urllib.request.build_opener(_NoAutoRedirect)


def http_get(url, allowed, max_bytes=MAX_BYTES, accept="*/*"):
    seen = 0
    while True:
        _check_url(url, allowed)
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": accept,
            "Accept-Language": "en-GB,en;q=0.9",
        })
        try:
            resp = _opener.open(req, timeout=TIMEOUT)
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308):
                loc = e.headers.get("Location")
                if not loc:
                    raise Refused("redirect without Location")
                seen += 1
                if seen > MAX_REDIRECTS:
                    raise Refused("too many redirects")
                url = urllib.parse.urljoin(url, loc)
                continue
            raise
        with resp:
            ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            declared = resp.headers.get("Content-Length")
            if declared and int(declared) > max_bytes:
                raise Refused("content-length %s exceeds ceiling" % declared)
            body = resp.read(max_bytes + 1)
            if len(body) > max_bytes:
                raise Refused("body exceeds ceiling")
            return resp.geturl(), ctype, body


# ── Discovery ─────────────────────────────────────────────────────────────
IMG_RE = re.compile(r"https?://[^\s\"'\\<>]+?\.(?:jpg|jpeg|png|webp|avif)(?:\?[^\s\"'\\<>]*)?", re.I)
SRCSET_RE = re.compile(r"srcset\s*=\s*[\"']([^\"']+)[\"']", re.I)
OG_RE = re.compile(r"<meta[^>]+property=[\"']og:image[\"'][^>]+content=[\"']([^\"']+)[\"']", re.I)
JSONLD_RE = re.compile(r"<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", re.I | re.S)


def _from_jsonld(html):
    out = []
    for blob in JSONLD_RE.findall(html):
        try:
            data = json.loads(blob.strip())
        except Exception:
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                img = node.get("image")
                if isinstance(img, str):
                    out.append((img, "json-ld"))
                elif isinstance(img, list):
                    out += [(u, "json-ld") for u in img if isinstance(u, str)]
                stack += list(node.values())
            elif isinstance(node, list):
                stack += node
    return out


def discover_from_page(url, allowed, log):
    """Pull image candidates out of one product page, authoritative sources
    first. Returns [(url, method)]."""
    try:
        final, ctype, body = http_get(url, allowed,
                                      max_bytes=MAX_PAGE_BYTES, accept="text/html,*/*")
    except Exception as e:
        log.append({"stage": "discover", "url": url, "ok": False, "error": "%s: %s" % (type(e).__name__, e)})
        return []
    if "html" not in (ctype or ""):
        log.append({"stage": "discover", "url": url, "ok": False, "error": "not html (%s)" % ctype})
        return []
    html = body.decode("utf-8", "replace")
    found = []
    found += _from_jsonld(html)
    found += [(u, "og:image") for u in OG_RE.findall(html)]
    for ss in SRCSET_RE.findall(html):
        for part in ss.split(","):
            u = part.strip().split(" ")[0]
            if u.startswith("http"):
                found.append((u, "srcset"))
    found += [(u, "html-scan") for u in IMG_RE.findall(html)]
    log.append({"stage": "discover", "url": final, "ok": True, "raw_candidates": len(found)})
    return found


# ── Resolution upgrade ────────────────────────────────────────────────────
TRANSFORM_RE = re.compile(r"(/images/)([^/]*?w_)(\d+)([^/]*/)", re.I)


def _decode_transform(url):
    """adidas URLs sometimes arrive percent-encoded (w_500%2Cf_auto). Decode
    only the transform segment so the rest of the path is untouched."""
    return url.replace("%2C", ",").replace("%2c", ",")


def resolution_variants(url, ladder):
    """Same asset, larger width. Only the transform segment changes; the asset
    hash and filename are left alone, so this can never yield a different
    product or colorway."""
    u = _decode_transform(url)
    m = TRANSFORM_RE.search(u)
    if not m:
        return []
    current = int(m.group(3))
    out = []
    for w in ladder:
        if w <= current:
            continue
        out.append(TRANSFORM_RE.sub(lambda mm, w=w: "%s%s%d%s" % (mm.group(1), mm.group(2), w, mm.group(4)), u, count=1))
    return out


# ── Validation ────────────────────────────────────────────────────────────
def dhash(img, size=16):
    g = img.convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(g.getdata())
    bits = 0
    for r in range(size):
        for c in range(size):
            bits = (bits << 1) | (1 if px[r * (size + 1) + c] > px[r * (size + 1) + c + 1] else 0)
    return bits


def hamming(a, b):
    return bin(a ^ b).count("1")


def validate_bytes(body, ctype):
    """Decode and measure. Rejects an HTML error page saved with an image
    content-type, a truncated file, or anything Pillow cannot open."""
    if len(body) < MIN_BYTES:
        return None, "too small (%d B)" % len(body)
    head = body[:64].lstrip()[:15].lower()
    if head.startswith(b"<!doctype") or head.startswith(b"<html"):
        return None, "HTML served as image"
    try:
        img = Image.open(io.BytesIO(body))
        img.load()
    except Exception as e:
        return None, "undecodable: %s" % e
    w, h = img.size
    if w < 1 or h < 1:
        return None, "zero dimension"
    fmt = (img.format or "").lower()
    mime = {"jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}.get(fmt, ctype or "")
    if mime not in OK_MIME:
        return None, "mime %r not allowed" % mime
    return {
        "width": w, "height": h, "longest_edge": max(w, h),
        "mime": mime, "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "dhash": "%064x" % dhash(img.convert("RGB")),
        "_img": img.convert("RGB"),
    }, None


def sku_signal(url, sku):
    return sku.lower() in urllib.parse.unquote(url).lower()


# ── Main ──────────────────────────────────────────────────────────────────
def acquire(request, outroot, log):
    sku = request["manufacturerItemNo"].strip()
    brand = request["brand"].strip()
    rule = brand_rule(brand)

    allowed = (
        frozenset([h.lower() for h in rule["allowed_hosts"]] +
                  [h.lower() for h in request.get("allowedHosts", [])]),
        tuple(sorted({h.lower().lstrip(".") for h in request.get("allowedHostSuffixes", [])})),
    )
    ladder = request.get("resolution", {}).get("widthLadder") or rule["width_ladder"]

    # 1. DISCOVER ---------------------------------------------------------
    candidates = []
    for seed in request.get("candidateMedia", []):
        u = seed["url"] if isinstance(seed, dict) else seed
        candidates.append((u, "request-seed"))

    pages = list(request.get("discoveryPages", []))
    if request.get("officialProductPage"):
        pages.insert(0, request["officialProductPage"])
    for tpl in rule["page_templates"]:
        pages.append(tpl.format(sku=sku))
    seen_pages = set()
    for page in pages:
        if page in seen_pages:
            continue
        seen_pages.add(page)
        candidates += discover_from_page(page, allowed, log)

    # normalise, de-dup by URL, keep discovery order
    ordered, seen_url = [], set()
    for u, method in candidates:
        u = _decode_transform(u.strip())
        if not u.lower().startswith(("http://", "https://")):
            continue
        try:
            _check_url(u, allowed)
        except Refused as e:
            log.append({"stage": "filter", "url": u[:160], "ok": False, "error": str(e)})
            continue
        if u in seen_url:
            continue
        seen_url.add(u)
        ordered.append((u, method))
    ordered = ordered[:MAX_CANDIDATES]
    log.append({"stage": "discover", "total_unique_candidates": len(ordered)})

    # 2. ACQUIRE (with resolution upgrade per asset) -----------------------
    def grab(u):
        """Download and validate one URL. Returns meta or None."""
        try:
            final, ctype, body = http_get(u, allowed, accept="image/*,*/*")
        except Exception as e:
            log.append({"stage": "acquire", "url": u[:160], "ok": False,
                        "error": "%s: %s" % (type(e).__name__, e)})
            return None
        meta, err = validate_bytes(body, ctype)
        if not meta:
            log.append({"stage": "validate", "url": u[:160], "ok": False, "error": err})
            return None
        meta["url"] = final
        meta["requested_url"] = u
        meta["_body"] = body
        return meta

    acquired = []
    for url, method in ordered:
        # The discovered URL is the anchor: it is the image we actually found
        # on the source. Every larger variant is then checked against it.
        # Anchoring on "whichever variant downloaded first" would let a CDN
        # that serves something else at a different width slip through
        # unchecked, so the order here matters.
        anchor = grab(url)
        best = anchor
        notes = []
        if anchor is None:
            notes.append("anchor image unavailable; resolution variant accepted unverified")

        for variant in resolution_variants(url, ladder):
            meta = grab(variant)
            if meta is None:
                continue
            if anchor is not None:
                d = hamming(int(anchor["dhash"], 16), int(meta["dhash"], 16))
                if d > DUPLICATE_DISTANCE:
                    log.append({"stage": "resolution", "url": variant[:160], "ok": False,
                                "error": "variant differs from anchor (dHash %d); rejected" % d})
                    continue
            if best is None or meta["longest_edge"] > best["longest_edge"]:
                best = meta

        if best:
            best["discovery_method"] = method
            best["acquired_at"] = now()
            best["sku_in_url"] = sku_signal(best["url"], sku)
            best["anchor_url"] = url
            best["notes"] = notes
            acquired.append(best)
            log.append({"stage": "acquire", "url": best["url"][:160], "ok": True,
                        "size": "%dx%d" % (best["width"], best["height"]),
                        "bytes": best["bytes"],
                        "upgraded_from": None if best["requested_url"] == url else url[:160]})

    if not acquired:
        return None, acquired

    # 3. DEDUPE -----------------------------------------------------------
    acquired.sort(key=lambda m: (-m["longest_edge"], -m["bytes"]))
    unique = []
    for m in acquired:
        dup_of = None
        for k in unique:
            if m["sha256"] == k["sha256"]:
                dup_of = k
                break
            if hamming(int(m["dhash"], 16), int(k["dhash"], 16)) <= DUPLICATE_DISTANCE:
                dup_of = k
                break
        if dup_of:
            dup_of.setdefault("duplicates", []).append(
                {"url": m["url"], "size": "%dx%d" % (m["width"], m["height"]), "sha256": m["sha256"]})
        else:
            unique.append(m)

    # 4. SELECT -----------------------------------------------------------
    usable = [m for m in unique if m["longest_edge"] >= MIN_EDGE]
    usable.sort(key=lambda m: (-m["longest_edge"], m["url"]))
    selected = usable[:MAX_KEEP]
    return selected, acquired


# ── Output ────────────────────────────────────────────────────────────────
def view_key(url, view_re):
    """Brand-specific view token, used only for ordering. Unknown -> 99."""
    if not view_re:
        return 99
    m = re.search(view_re, urllib.parse.unquote(url), re.I)
    return int(m.group(1)) if m else 99


def contact_sheet(entries, header, out_path):
    """A real sheet: every tile is a downloaded asset. No placeholders."""
    from PIL import ImageDraw, ImageFont
    FD = "/usr/share/fonts/truetype/dejavu/"
    B = lambda s: ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", s)
    R = lambda s: ImageFont.truetype(FD + "DejaVuSans.ttf", s)
    BG, INK, MUTE = (255, 252, 253), (24, 20, 22), (120, 112, 116)
    PINK, WARN, LINE = (233, 86, 150), (176, 104, 0), (226, 218, 222)

    CELL, PAD, CAP, COLS = 460, 30, 150, 2
    TW, TH = CELL + PAD * 2, CELL + CAP + PAD * 2
    HEAD, FOOT = 176, 96
    rows = (len(entries) + COLS - 1) // COLS
    W, H = TW * COLS, HEAD + TH * rows + FOOT
    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)

    def wrap(t, f, mw):
        out, cur = [], ""
        for w in t.split(" "):
            c = (cur + " " + w).strip()
            if d.textlength(c, font=f) <= mw:
                cur = c
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
        return out

    def block(x, y, t, f, fill, mw, lh):
        for ln in wrap(t, f, mw):
            d.text((x, y), ln, font=f, fill=fill)
            y += lh
        return y

    d.rectangle([0, 0, W, HEAD - 1], fill=(255, 240, 246))
    d.line([0, HEAD - 1, W, HEAD - 1], fill=PINK, width=3)
    # Shrink the title until it fits; SKUs and brand names vary in length.
    tf = B(38)
    while d.textlength(header["title"], font=tf) > W - PAD * 2 and tf.size > 20:
        tf = B(tf.size - 2)
    d.text((PAD, 26 + (38 - tf.size) // 2), header["title"], font=tf, fill=INK)
    d.text((PAD, 82), header["line2"], font=R(21), fill=INK)
    d.text((PAD, 114), header["line3"], font=R(19), fill=MUTE)

    for i, e in enumerate(entries):
        ox, oy = (i % COLS) * TW, HEAD + (i // COLS) * TH
        im = Image.open(e["_preview_path"]).convert("RGB")
        im.thumbnail((CELL, CELL), Image.LANCZOS)
        px, py = ox + PAD + (CELL - im.width) // 2, oy + PAD + (CELL - im.height) // 2
        if e["role"] == "MAIN":
            d.rectangle([ox + PAD - 8, oy + PAD - 8, ox + PAD + CELL + 7, oy + PAD + CELL + 7],
                        outline=PINK, width=5)
        else:
            d.rectangle([ox + PAD - 1, oy + PAD - 1, ox + PAD + CELL, oy + PAD + CELL],
                        outline=LINE, width=1)
        sheet.paste(im, (px, py))

        x, y = ox + PAD, oy + PAD + CELL + 14
        label = "IMAGE %02d" % e["index"]
        d.text((x, y), label, font=B(26), fill=INK)
        if e["role"] == "MAIN":
            bx = x + int(d.textlength(label, font=B(26))) + 14
            tw = d.textlength("PROPOSED MAIN", font=B(17))
            d.rectangle([bx, y + 2, bx + tw + 20, y + 28], fill=PINK)
            d.text((bx + 10, y + 6), "PROPOSED MAIN", font=B(17), fill=(255, 255, 255))
        y += 34
        y = block(x, y, "%d x %d  ·  %s  ·  %.0f KB" % (
            e["width"], e["height"], e["mime"].split("/")[-1].upper(), e["bytes"] / 1024),
            R(18), INK, CELL, 24)
        y = block(x, y, "Source: %s  ·  %s" % (e["source_domain"], e["discovery_method"]),
                  R(15), MUTE, CELL, 20)
        y = block(x, y, "sha256 %s…" % e["sha256"][:24], R(14), MUTE, CELL, 20)
        if e.get("warnings"):
            block(x, y, "⚠ " + "; ".join(e["warnings"]), R(15), WARN, CELL, 20)

    fy = H - FOOT
    d.line([0, fy, W, fy], fill=LINE, width=2)
    y = block(PAD, fy + 14, header["footer1"], R(17), INK, W - PAD * 2, 23)
    block(PAD, y + 2, header["footer2"], R(15), MUTE, W - PAD * 2, 21)
    sheet.save(out_path, "WEBP", quality=92, method=6)
    return sheet.size


def write_outputs(request, selected, all_acquired, log, outroot):
    sku = request["manufacturerItemNo"].strip()
    brand = request["brand"].strip()
    rule = brand_rule(brand)
    base = os.path.join(outroot, sku)
    src_dir, prev_dir = os.path.join(base, "source"), os.path.join(base, "preview")
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(prev_dir, exist_ok=True)

    selected.sort(key=lambda m: (view_key(m["url"], rule.get("view_re")), -m["longest_edge"]))

    entries = []
    for i, m in enumerate(selected, 1):
        ext = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}[m["mime"]]
        # Filenames are derived from SKU and index only — never from the
        # remote URL — so a hostile path can never escape the output dir.
        sfile = "%s-%02d-original.%s" % (re.sub(r"[^A-Za-z0-9_-]", "", sku), i, ext)
        pfile = "%s-%02d.webp" % (re.sub(r"[^A-Za-z0-9_-]", "", sku), i)
        spath, ppath = os.path.join(src_dir, sfile), os.path.join(prev_dir, pfile)
        with open(spath, "wb") as fh:
            fh.write(m["_body"])
        prev = m["_img"].copy()
        prev.thumbnail((1600, 1600), Image.LANCZOS)
        prev.save(ppath, "WEBP", quality=90, method=6)

        warnings = []
        if m["longest_edge"] < PREFERRED_EDGE:
            warnings.append("%dpx longest edge — below the %dpx preference"
                            % (m["longest_edge"], PREFERRED_EDGE))
        elif m["longest_edge"] < IDEAL_EDGE:
            warnings.append("%dpx longest edge — usable, %dpx ideal"
                            % (m["longest_edge"], IDEAL_EDGE))
        if not m["sku_in_url"]:
            warnings.append("SKU not present in asset URL")
        warnings += m.get("notes", [])

        entries.append({
            "index": i,
            "role": "MAIN" if i == 1 else "gallery",
            "file": os.path.relpath(spath, base),
            "preview": os.path.relpath(ppath, base),
            "_preview_path": ppath,
            "source_url": m["url"],
            "requested_url": m["requested_url"],
            "anchor_url": m.get("anchor_url"),
            "source_domain": urllib.parse.urlsplit(m["url"]).hostname,
            "discovery_method": m["discovery_method"],
            "acquired_at": m["acquired_at"],
            "width": m["width"], "height": m["height"],
            "longest_edge": m["longest_edge"],
            "mime": m["mime"], "bytes": m["bytes"],
            "sha256": m["sha256"], "dhash": m["dhash"],
            "sku_in_url": m["sku_in_url"],
            "duplicates_collapsed": m.get("duplicates", []),
            "validation": "PASS",
            "warnings": warnings,
        })

    status = "PASS" if len(entries) >= MIN_KEEP else ("PARTIAL" if entries else "BLOCKED")
    sheet_rel = None
    if entries:
        sheet_path = os.path.join(base, "CONTACT_SHEET.webp")
        best = max(e["longest_edge"] for e in entries)
        contact_sheet(entries, {
            "title": "PINK MALL — %s %s — ACQUIRED MEDIA" % (brand.upper(), sku),
            "line2": "%s  /  %s  /  %s" % (brand, request.get("model", "—"), request.get("variant", "—")),
            "line3": "Automated acquisition · %d unique images · best %dpx · NOT PUBLISHED" % (len(entries), best),
            "footer1": "Every tile is a downloaded asset. No placeholders, no generative edits, "
                       "no upscaling — only the CDN's own larger copy of the same photograph.",
            "footer2": "Proposed MAIN is a filename-order heuristic. Visual confirmation by the "
                       "onboarding skill is still required before approval.",
        }, sheet_path)
        sheet_rel = "CONTACT_SHEET.webp"

    for e in entries:
        e.pop("_preview_path", None)

    manifest = {
        "schemaVersion": 1,
        "status": status,
        "sku": sku,
        "brand": brand,
        "model": request.get("model"),
        "variant": request.get("variant"),
        "officialProductPage": request.get("officialProductPage"),
        "generatedAt": now(),
        "generatedBy": "tools/media_acquisition/acquire.py",
        "runner": os.environ.get("GITHUB_RUN_ID") and {
            "githubRunId": os.environ.get("GITHUB_RUN_ID"),
            "githubRepository": os.environ.get("GITHUB_REPOSITORY"),
            "githubSha": os.environ.get("GITHUB_SHA"),
        } or {"local": True},
        "counts": {
            "acquired": len(all_acquired),
            "unique_selected": len(entries),
            "duplicates_collapsed": sum(len(e["duplicates_collapsed"]) for e in entries),
        },
        "proposedMain": entries[0]["file"] if entries else None,
        "contactSheet": sheet_rel,
        "images": entries,
        "log": log,
        "notes": [
            "Media is acquired but NOT published. Live assets live under "
            "assets/pink-mall/products/<PM-ID>/ and only after explicit approval.",
            "Resolution upgrades rewrite only the CDN transform segment of the same "
            "asset URL and are accepted only if perceptually identical to the base image.",
        ],
    }
    with open(os.path.join(base, "result.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return manifest, base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", required=True)
    ap.add_argument("--out", default="docs/pink-mall/media-acquisition")
    args = ap.parse_args()

    with open(args.request, encoding="utf-8") as fh:
        request = json.load(fh)
    for k in ("brand", "manufacturerItemNo"):
        if not request.get(k):
            print("request is missing %r" % k, file=sys.stderr)
            return 2

    log = []
    selected, all_acquired = acquire(request, args.out, log)
    manifest, base = write_outputs(request, selected or [], all_acquired or [], log, args.out)
    print(json.dumps({"status": manifest["status"], "sku": manifest["sku"],
                      "selected": manifest["counts"]["unique_selected"],
                      "acquired": manifest["counts"]["acquired"],
                      "out": base}, indent=2))
    return 0 if manifest["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
