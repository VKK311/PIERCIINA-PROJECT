# PINK MALL — project state

Updated: PM-027 publication.
Status: **PM-001…PM-027 PUBLISHED.**

This file records the real state. Trust it over any summary, and verify the
canonical build by hash before treating it as canonical.

## Canonical

| | |
|---|---|
| CANONICAL BRANCH | `claude/pink-mall-development` |
| CANONICAL WEBSITE | `PINKMALL.html` |
| CANONICAL WEBSITE SHA-256 | `fa04b28f840e8a7423cc9c6138b53bad88f994c8dac9b0b2966355f5f597b4fa` |
| CANONICAL WEBSITE BYTES | 2549676 |

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
| PUBLIC CATALOG | PM-001 … PM-027 |
| NEXT ID | PM-028 |
| JQ4556 | **PUBLISHED as PM-025** on 2026-08-25 |
| GC515KI | **PUBLISHED as PM-026** on 2026-08-25 |
| A08745C | **PUBLISHED as PM-027** on 2026-08-25 |

## Media acquisition automation

| | |
|---|---|
| AUTOMATION | PASS — `tools/media_acquisition/`, `.github/workflows/media-acquisition.yml` |
| SELF-TEST | PASS — `python tools/media_acquisition/selftest.py`, 19/19 guards |
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
| SHA-256 | `ac7bb3a695a2fde2f0f712c3f1d9d4b0b89a1cd1d49e913578e3666e5f496889` |
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

## PM-027 — published

| | |
|---|---|
| PUBLISHED | 2026-08-25 |
| BRAND / MODEL | Converse / Chuck Taylor All Star Move |
| MANUFACTURER ITEM | A08745C |
| PUBLIC COLOUR | Pink |
| MATERIAL | **omitted** — not established by this pipeline |
| PRICE | €49, no SALE |
| INVENTORY MODE | availability |
| SIZES | 36, 37.5, 38, 39 — all available. **No sold-out sizes asserted** |
| EXACT-MODEL SIZE RUN | NOT VERIFIED |
| NEW UNTIL | 2026-09-08 (14 days from first publication) |
| MAIN | IMAGE 01 — lateral side profile |
| GALLERY ORDER | 01 → 05 → 02 → 04 → 03 |
| LIVE MEDIA | `assets/pink-mall/products/PM-027/` — 1 × 1500², 4 × 670² WebP, native aspect |
| ORIGINALS | `docs/pink-mall/media-acquisition/A08745C/source/` (hash-recorded) |
| ACQUISITION | **zero-seed** — no user URL, no user images |
| VARIANT | `VARIANT_CONFIDENCE_PASS` |
| PACKAGE | `checkpoints/PM027_A08745C_APPROVAL_PREVIEW.md` |

**Media tier: trusted retailer fallback, not manufacturer-official.** Every
official Converse route failed — `converse.com` 403 ×4, the reachable regional
category pages carried no A08745C link, one-hop link following reached no
official target. Media came from `akn-spx.a-cdn.akinoncdn.com` via the
spx.com.tr product page, with SKU evidence carried by that page's `og:image`
and JSON-LD declarations. **There is no official image anchor for this SKU.**
Provenance is retained internally and is never presented to a customer as
official media.

Four of the five images are 670×670, below the 1000 px preference. They are
published at their native size; nothing was upscaled and no canvas was
manufactured. Higher-resolution official copies remain preferred if an official
route ever opens.

Material was omitted rather than asserted: `100% TEKSTIL` reached the project
through reviewer evidence, not through the pipeline's own discovery, so the
customer-facing record carries no material row.

The manufacturer's youth-series classification is internal only and appears
nowhere in the build — verified with base64 payloads excluded.

### Supporting engine change

`sizeSortKey()` previously matched the fractional form (`37 1/3`) but not the
decimal form (`37.5`), so a decimal half-size fell through to a lexicographic
comparison and the size row was ordered by string, not by number. PM-027 is the
first SKU to use decimal half-sizes. The key now accepts both forms; the size
**label** is still never rewritten — only the ordering key is computed.

## Pending approval — not published

### adidas JR5952 — READY FOR APPROVAL

| | |
|---|---|
| Model | Gazelle Bold Shoes |
| Manufacturer colour | Almost Pink / Court Green / Gold Metallic |
| Public colour | Pink / Green / Gold |
| Price | €59 |
| Sizes | 36, 37 1/3, 38, 38 2/3 — available only; no sold-out states asserted |
| Variant | `VARIANT_CONFIDENCE_PASS` — all three official colour terms in frame |
| Images | 5 accepted, 560×746 |
| Media tier | **trusted retailer fallback** — no official image anchor |
| User media required | **no** |
| Material | omitted — not established by this pipeline |
| Proposed Mall ID | **PM-028** |
| Published | **no** |
| Package | `checkpoints/JR5952_APPROVAL_PREVIEW.md` |

The earlier rejection of JR5952 as "a white-and-green Gazelle Bold, not pink"
was wrong: `Almost Pink` is a very pale tint and `Court Green` is part of the
official colourway. Correct media was discarded on a subjective colour read.
That case is now a permanent regression fixture.

The earlier BLOCKED / UNRESOLVED records for JR5952 and A08745C are
**superseded**; see `checkpoints/SUPERSEDED_*.md`, kept only as a record of how
those conclusions were reached and why they were wrong.

## Next step

Next Mall ID is **PM-028**, unallocated until a product is actually published.
JR5952 is the only product awaiting approval and would take PM-028 on publish.
