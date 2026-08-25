# PINK MALL — project state

Updated: structure cleanup + pre-publish hardening.
Status: **STRUCTURE CLEAN / HARDENING PASS.**

This file records the real state. Trust it over any summary, and verify the
canonical build by hash before treating it as canonical.

## Canonical

| | |
|---|---|
| CANONICAL BRANCH | `claude/pink-mall-development` |
| CANONICAL WEBSITE | `PINKMALL.html` |
| CANONICAL WEBSITE SHA-256 | `fa639d3c87f80cfff062114b2b2602fed282754f642e2a07eb7e5a7b38aa12c9` |
| CANONICAL WEBSITE BYTES | 2537658 |

## Engine

| | |
|---|---|
| REAL PRODUCT ENGINE | PASS |
| PER-IMAGE ALT | PASS — canonical `media.imageAlt` / `media.galleryAlt[]` |
| CALIBRATION FIXTURE | REMOVED |

## Catalog

| | |
|---|---|
| PUBLIC CATALOG | PM-001 … PM-024 |
| NEXT ID | PM-025 |
| JQ4556 | staged, awaiting final human approval — NOT PUBLISHED |

## Media acquisition automation

| | |
|---|---|
| AUTOMATION | PASS — `tools/media_acquisition/`, `.github/workflows/media-acquisition.yml` |
| SELF-TEST | PASS — `python tools/media_acquisition/selftest.py`, 12/12 guards |
| JQ4556 PILOT | PASS — 4 exact official images, 1880×1880, zero manual preparation |

Provenance: `docs/pink-mall/media-acquisition/JQ4556/result.json`

All four came from `assets.adidas.com`, seeded at `w_500` and upgraded to
`w_1880` — the CDN's own larger copy of the same photograph, each verified
perceptually against its 500px anchor. No AI upscaling. SKU present in every
asset URL. Three runs; images byte-identical across runs, so the pipeline is
idempotent.

**Known limitation:** adidas product *pages* return 403 to the GitHub runner
(bot protection on datacenter IPs) and the courir fallback URL 404s. Page
scraping therefore contributed nothing; all four candidates came from
research-derived CDN seeds in the request manifest. For a SKU whose asset URLs
are not already known, discovery would need a different route.

## PM-025 media

| | |
|---|---|
| APPROVED SET | 1880×1880, four exact official images |
| MAIN | IMAGE 01 — lateral side profile |
| GALLERY ORDER | 01 → 04 → 02 → 03 |
| ARCHIVE | `docs/pink-mall/approval-media/PM-025/` |
| RESOLUTION WARNING | withdrawn — the 500×500 set has been fully replaced |
| PUBLISHED | no |

The media upgrade was approved on 2026-08-25. Product facts, price, sizes,
colour, copy, tags, alt text, MAIN and gallery order are all unchanged; only
the image bytes and their resolution changed.

## Next step

Explicit PM-025 approval, then a publication task.
