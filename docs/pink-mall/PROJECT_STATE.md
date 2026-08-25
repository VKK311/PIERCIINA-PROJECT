# PINK MALL — project state

Updated: PM-025 publication.
Status: **PM-025 PUBLISHED.**

This file records the real state. Trust it over any summary, and verify the
canonical build by hash before treating it as canonical.

## Canonical

| | |
|---|---|
| CANONICAL BRANCH | `claude/pink-mall-development` |
| CANONICAL WEBSITE | `PINKMALL.html` |
| CANONICAL WEBSITE SHA-256 | `0ffda5450dd92a3e4262da6767999e486b43be260932b878a33543ea06519c32` |
| CANONICAL WEBSITE BYTES | 2539946 |

## Engine

| | |
|---|---|
| REAL PRODUCT ENGINE | PASS |
| PER-IMAGE ALT | PASS — canonical `media.imageAlt` / `media.galleryAlt[]` |
| CALIBRATION FIXTURE | REMOVED |

## Catalog

| | |
|---|---|
| PUBLIC CATALOG | PM-001 … PM-025 |
| NEXT ID | PM-026 |
| JQ4556 | **PUBLISHED as PM-025** on 2026-08-25 |

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

## PM-025 — published

| | |
|---|---|
| PUBLISHED | 2026-08-25 |
| BRAND / MODEL | adidas / VL Court Bold Shoes |
| MANUFACTURER ITEM | JQ4556 |
| PRICE | €54, no SALE |
| INVENTORY MODE | availability — no quantities invented |
| NEW UNTIL | 2026-09-08 (14 days from first publication) |
| MAIN | IMAGE 01 — lateral side profile |
| GALLERY ORDER | 01 → 04 → 02 → 03 |
| LIVE MEDIA | `assets/pink-mall/products/PM-025/` — 4 × 1440×1920 WebP |
| ORIGINALS | `docs/pink-mall/approval-media/PM-025/source/` (1880×1880, hash-recorded) |

Live WebP are the 1880×1880 originals composited onto a 3:4 canvas on the
sources' own studio background, so neither the 3:4 card nor the 4:5 PDP crops
the product. No site CSS was changed.

The manufacturer's juniors-series classification is internal only and appears
nowhere in the build — verified with base64 payloads excluded.

## Next step

Explicit PM-025 approval, then a publication task.
