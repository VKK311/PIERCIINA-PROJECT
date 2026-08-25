#!/usr/bin/env python3
"""Build the portable standalone review artifact.

    python tools/build_standalone_review.py

Production stays as it is: PINKMALL.html plus a real assets/ tree. That is the
right architecture for a site — the browser caches images separately, and the
HTML stays diffable.

But a reviewer who downloads PINKMALL.html on its own gets a file with dangling
relative paths and no product photography. Repository regression passing is not
the same as the file a human opens actually working. This script closes that
gap by emitting a second, generated artifact whose images are inlined as data:
URIs, so it renders correctly from an empty directory.

    canonical HTML
      -> find every local asset reference
      -> inline each one as a data: URI
      -> write PINKMALL_REVIEW_STANDALONE.html
      -> verify no required local path survives

The canonical file is opened read-only and never written.
"""

import argparse
import base64
import hashlib
import io
import mimetypes
import os
import re
import sys

# Only these are inlined. Anything remote (http, //, data:) is left alone —
# notably Google Fonts, which keeps its existing offline fallback.
INLINE_EXT = {
    ".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg", ".gif": "image/gif", ".avif": "image/avif",
    ".svg": "image/svg+xml", ".woff": "font/woff", ".woff2": "font/woff2",
    ".ttf": "font/ttf", ".otf": "font/otf",
}

# A path-like token with at least one slash, so bare words never match.
PATH_RE = re.compile(
    r"(?<![A-Za-z0-9._/\-])"
    r"((?:\./)?(?:[A-Za-z0-9._\-]+/)+[A-Za-z0-9._\-]+"
    r"\.(?:webp|png|jpe?g|gif|avif|svg|woff2?|ttf|otf))"
    r"(?![A-Za-z0-9._\-])"
)

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def comment_spans(text):
    return [m.span() for m in COMMENT_RE.finditer(text)]


def inside(spans, pos):
    return any(a <= pos < b for a, b in spans)


def safe_resolve(root, rel):
    """Resolve rel under root, refusing anything that escapes it."""
    root = os.path.realpath(root)
    p = os.path.realpath(os.path.join(root, rel))
    if p != root and not p.startswith(root + os.sep):
        return None
    return p if os.path.isfile(p) else None


def build(src_path, out_path):
    root = os.path.dirname(os.path.abspath(src_path)) or "."
    with io.open(src_path, encoding="utf-8") as fh:
        html = fh.read()

    src_sha = hashlib.sha256(io.open(src_path, "rb").read()).hexdigest()
    spans = comment_spans(html)

    refs = {}          # rel path -> [positions]
    for m in PATH_RE.finditer(html):
        refs.setdefault(m.group(1), []).append(m.start())

    inlined, missing_live, missing_doc, skipped = [], [], [], []
    for rel, positions in sorted(refs.items()):
        ext = os.path.splitext(rel)[1].lower()
        if ext not in INLINE_EXT:
            skipped.append((rel, "extension not inlined"))
            continue
        real = safe_resolve(root, rel.lstrip("./") if rel.startswith("./") else rel)
        if real is None:
            # A reference that resolves to nothing is only acceptable if every
            # occurrence sits inside an HTML comment — i.e. it is documentation
            # of a config shape, not a live asset.
            (missing_doc if all(inside(spans, p) for p in positions)
             else missing_live).append(rel)
            continue
        with open(real, "rb") as fh:
            blob = fh.read()
        mime = INLINE_EXT[ext] or mimetypes.guess_type(real)[0] or "application/octet-stream"
        uri = "data:%s;base64,%s" % (mime, base64.b64encode(blob).decode("ascii"))
        # Bytes are copied verbatim: no decode, no re-encode, no resize.
        html = html.replace(rel, uri)
        inlined.append((rel, len(blob), hashlib.sha256(blob).hexdigest()))

    if missing_live:
        print("FAIL: local asset(s) referenced outside comments but not found:", file=sys.stderr)
        for r in missing_live:
            print("   " + r, file=sys.stderr)
        return None, 2

    with io.open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    # Verification: no inlinable local path may survive in the output, except
    # inside comments where it is documentation.
    out_spans = comment_spans(html)
    leftover = []
    for m in PATH_RE.finditer(html):
        rel = m.group(1)
        if os.path.splitext(rel)[1].lower() not in INLINE_EXT:
            continue
        if inside(out_spans, m.start()):
            continue
        leftover.append(rel)
    if leftover:
        print("FAIL: unresolved local asset path(s) remain in the output:", file=sys.stderr)
        for r in sorted(set(leftover)):
            print("   " + r, file=sys.stderr)
        return None, 3

    report = {
        "source": src_path, "source_sha256": src_sha,
        "output": out_path,
        "output_sha256": hashlib.sha256(io.open(out_path, "rb").read()).hexdigest(),
        "output_bytes": os.path.getsize(out_path),
        "inlined": inlined, "documented_only": missing_doc, "skipped": skipped,
    }
    return report, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="PINKMALL.html")
    ap.add_argument("--out", default="PINKMALL_REVIEW_STANDALONE.html")
    args = ap.parse_args()

    before = hashlib.sha256(io.open(args.source, "rb").read()).hexdigest()
    report, rc = build(args.source, args.out)
    after = hashlib.sha256(io.open(args.source, "rb").read()).hexdigest()
    if before != after:
        print("FAIL: canonical source was modified", file=sys.stderr)
        return 4
    if rc:
        return rc

    print("source : %s  %s" % (report["source"], report["source_sha256"]))
    print("output : %s  %s" % (report["output"], report["output_sha256"]))
    print("         %d bytes" % report["output_bytes"])
    print("inlined: %d asset(s)" % len(report["inlined"]))
    for rel, n, sha in report["inlined"]:
        print("   %-52s %8d B  %s…" % (rel, n, sha[:16]))
    if report["documented_only"]:
        print("comment-only references (not assets, left as text):")
        for r in report["documented_only"]:
            print("   " + r)
    print("canonical source unchanged: yes")
    print("STANDALONE BUILD: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
