#!/usr/bin/env python3
"""Render acquisition result manifests as a GitHub Actions job summary."""
import glob
import json
import sys


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "docs/pink-mall/media-acquisition"
    out = ["## Pink Mall media acquisition", ""]
    files = sorted(glob.glob(root + "/*/result.json"))
    if not files:
        out.append("_No result manifests were produced._")
    for f in files:
        with open(f, encoding="utf-8") as fh:
            m = json.load(fh)
        out.append("### %s %s — **%s**" % (m["brand"], m["sku"], m["status"]))
        out.append("")
        c = m["counts"]
        out.append("Acquired %d, kept %d unique, collapsed %d duplicate(s). "
                   "Proposed MAIN: `%s`"
                   % (c["acquired"], c["unique_selected"], c["duplicates_collapsed"],
                      m.get("proposedMain") or "—"))
        out.append("")
        if m["images"]:
            out.append("| # | role | size | KB | source | method | sha256 |")
            out.append("|---|---|---|---|---|---|---|")
            for e in m["images"]:
                out.append("| %02d | %s | %d×%d | %.0f | %s | %s | `%s…` |" % (
                    e["index"], e["role"], e["width"], e["height"], e["bytes"] / 1024,
                    e["source_domain"], e["discovery_method"], e["sha256"][:16]))
            out.append("")
        fails = [l for l in m.get("log", []) if l.get("ok") is False]
        if fails:
            out.append("<details><summary>%d rejected candidate(s)</summary>" % len(fails))
            out.append("")
            for l in fails[:40]:
                out.append("- `%s` — %s" % (l.get("stage"), str(l.get("error"))[:160]))
            out.append("")
            out.append("</details>")
            out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
