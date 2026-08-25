#!/usr/bin/env bash
# Copy ONLY the standalone file into an empty directory and confirm every
# local reference resolves from that single file. Cheap structural check —
# the browser-level check lives in the review regression suite.
set -euo pipefail

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cp PINKMALL_REVIEW_STANDALONE.html "$tmp/"

python - "$tmp/PINKMALL_REVIEW_STANDALONE.html" <<'PY'
import io, os, re, sys
p = sys.argv[1]
html = io.open(p, encoding="utf-8").read()
COMMENT = re.compile(r"<!--.*?-->", re.S)
spans = [m.span() for m in COMMENT.finditer(html)]
PATH = re.compile(r"(?<![A-Za-z0-9._/\-])((?:\./)?(?:[A-Za-z0-9._\-]+/)+"
                  r"[A-Za-z0-9._\-]+\.(?:webp|png|jpe?g|gif|avif|svg|woff2?|ttf|otf))"
                  r"(?![A-Za-z0-9._\-])")
bad = [m.group(1) for m in PATH.finditer(html)
       if not any(a <= m.start() < b for a, b in spans)]
if bad:
    print("FAIL: local paths survive in the standalone build:", file=sys.stderr)
    for r in sorted(set(bad)):
        print("   " + r, file=sys.stderr)
    raise SystemExit(1)
n = html.count("data:image/")
print("standalone verified in an empty directory: %d inlined image(s), 0 local paths" % n)
PY
