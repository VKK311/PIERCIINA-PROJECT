# PINK MALL — project state

Updated: PM-026 publication.
Status: **PM-001…PM-026 PUBLISHED.**

This file records the real state. Trust it over any summary, and verify the
canonical build by hash before treating it as canonical.

## Canonical

| | |
|---|---|
| CANONICAL BRANCH | `claude/pink-mall-development` |
| CANONICAL WEBSITE | `PINKMALL.html` |
| CANONICAL WEBSITE SHA-256 | `11a75766466dfc16656e3a0f952bccc35b9c21ad1b302ad20f7cea501fdad748` |
| CANONICAL WEBSITE BYTES | 2546247 |

## Engine

| | |
|---|---|
| REAL PRODUCT ENGINE | PASS |
| PER-IMAGE ALT | PASS — canonical `media.imageAlt` / `media.galleryAlt[]` |
| MEDIA PRESENTATION | PASS — `media.fit` adapter; storefront owns card/PDP fitting |
| CALIBRATION FIXTURE | REMOVED |

## Catalog

| | |
|---|---|
| PUBLIC CATALOG | PM-001 … PM-026 |
| NEXT ID | PM-027 |
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
| LIVE MEDIA | `assets/pink-mall/products/PM-025/` — 4 × 1880×1880 WebP, native aspect |
| ORIGINALS | `docs/pink-mall/approval-media/PM-025/source/` (1880×1880, hash-recorded) |

Live WebP are the originals at their native 1880×1880, format-converted only.
The storefront fits them with `media.fit:'contain'` and `surface:'#EAEEEF'`,
the backdrop the acquisition pipeline detected. No per-SKU canvas is prepared.

The manufacturer's juniors-series classification is internal only and appears
nowhere in the build — verified with base64 payloads excluded.

## Review artifact

| | |
|---|---|
| FILE | `PINKMALL_REVIEW_STANDALONE.html` (generated — never canonical) |
| SHA-256 | `f84b25de0227f11badab1ad49d4db33e0a4618ed780741937e3e8c7f62d548f3` |
| BUILDER | `python tools/build_standalone_review.py` |
| AUTOMATION | `.github/workflows/standalone-review.yml`, on any change to `PINKMALL.html` or `assets/` |

**Production verification is not portable review verification.** Both must PASS
before a publication is considered reviewed:

- **Production** — fresh clone, `PINKMALL.html` + `assets/`
- **Portable review** — the standalone file alone in an empty directory

## PM-026 — published

| | |
|---|---|
| PUBLISHED | 2026-08-25 |
| BRAND / MODEL | New Balance / 515 V1 |
| MANUFACTURER ITEM | GC515KI (Rose Sugar) |
| PUBLIC COLOUR | Pink |
| MATERIAL | omitted — never confirmed from an official source |
| PRICE | €54, no SALE |
| INVENTORY MODE | availability |
| SIZES | 37, 38, 40 — available. **No sold-out sizes asserted** |
| EXACT-MODEL SIZE RUN | NOT VERIFIED |
| NEW UNTIL | 2026-09-08 |
| MAIN | IMAGE 01 |
| GALLERY ORDER | 01 → 04 → 02 → 03 → 05 |
| LIVE MEDIA | `assets/pink-mall/products/PM-026/` — 5 × 1600×1600 WebP, byte-identical to the acquired originals |
| ACQUISITION | **zero-seed** — no user URL, no user images |

First product published end-to-end from four facts. The size ladder carries only
the supplied sizes because the exact-model run could not be proven; a generic
brand size chart is not evidence of what this SKU was offered in.

## PM-027 (JR5952) — BLOCKED

| | |
|---|---|
| BRAND / MODEL | adidas / Gazelle Bold Shoes |
| MANUFACTURER ITEM | JR5952 (Pink) |
| PRICE | €59 |
| SIZES | 36, 37 1/3, 38, 38 2/3 — valid, no size blocker |
| IDENTITY | RESOLVED |
| MEDIA | **BLOCKED** — 0 candidates, 0 acquired |
| REPORT | `docs/pink-mall/checkpoints/PM027_BLOCKED.md` |

Every adidas route refused the runner: product page, both product-API regions
and three page templates, all `403` or timeout. adidas hashes its CDN asset
paths, so unlike New Balance the CDN cannot be addressed from the SKU alone.
No trusted retailer carrying the exact SKU was found; only resell marketplaces,
which the skill excludes and which list different SKUs.

Unblocks on user-supplied images or official asset URLs.

## Next step

Next Mall ID is **PM-027**.
