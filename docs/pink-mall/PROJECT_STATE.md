# PINK MALL — project state

Updated: PM-028 publication.
Status: **PM-001…PM-028 PUBLISHED.**

This file records the real state. Trust it over any summary, and verify the
canonical build by hash before treating it as canonical.

## Canonical

| | |
|---|---|
| CANONICAL BRANCH | `claude/pink-mall-development` |
| CANONICAL WEBSITE | `PINKMALL.html` |
| CANONICAL WEBSITE SHA-256 | `7f088253c01c94c04100e111746b4bcc2153e4d68a3344790a37c3af9b07d2a5` |
| CANONICAL WEBSITE BYTES | 2552740 |

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
| PUBLIC CATALOG | PM-001 … PM-028 |
| NEXT ID | PM-029 |
| JQ4556 | **PUBLISHED as PM-025** on 2026-08-25 |
| GC515KI | **PUBLISHED as PM-026** on 2026-08-25 |
| A08745C | **PUBLISHED as PM-027** on 2026-08-25 |
| JR5952 | **PUBLISHED as PM-028** on 2026-08-25 |

## Media acquisition automation

| | |
|---|---|
| AUTOMATION | PASS — `tools/media_acquisition/`, `.github/workflows/media-acquisition.yml` |
| SELF-TEST | PASS — `python tools/media_acquisition/selftest.py`, 78/78 guards |
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
| SHA-256 | `451029462cd743edcf4c11b31facf8da7de0edec43ba8d35f2bdf48bdae8c60a` |
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

## PM-028 — published

| | |
|---|---|
| PUBLISHED | 2026-08-25 |
| BRAND / MODEL | adidas / Gazelle Bold Shoes |
| MANUFACTURER ITEM | JR5952 |
| MANUFACTURER COLOUR | Almost Pink / Court Green / Gold Metallic |
| PUBLIC COLOUR | Pink / Green / Gold |
| MATERIAL | **omitted** — not established by this pipeline |
| PRICE | €59, no SALE |
| INVENTORY MODE | availability |
| SIZES | 36, 37 1/3, 38, 38 2/3 — all available. **No sold-out sizes asserted** |
| EXACT-MODEL SIZE RUN | NOT VERIFIED |
| NEW UNTIL | 2026-09-08 (14 days from first publication) |
| MAIN | **IMAGE 02** — automation proposed 01; changed on visual review |
| GALLERY ORDER | 02 → 01 → 05 → 04 → 03 |
| LIVE MEDIA | `assets/pink-mall/products/PM-028/` — 5 × 560×746 WebP, native aspect |
| ORIGINALS | `docs/pink-mall/media-acquisition/JR5952/source/` (hash-recorded) |
| ACQUISITION | **zero-seed** — no user URL, no user images |
| VARIANT | `VARIANT_CONFIDENCE_PASS` |
| PACKAGE | `checkpoints/JR5952_APPROVAL_PREVIEW.md` |

**Media tier: trusted retailer fallback, not manufacturer-official.** adidas
product pages and both API regions returned `403` or timed out across five
attempts, and `assets.adidas.com` is not addressable by style code because
adidas hashes its asset paths. Media came from `img.eobuwie.cloud` with SKU
evidence carried by the source page's JSON-LD declaration. Marketplaces holding
the same SKU (Allegro, ERLI) were excluded as primary media per the source
hierarchy. **There is no official image anchor**, so variant confidence rests on
exact-SKU evidence plus agreement with the official colour text — materially
weaker than PM-026's manufacturer-CDN media. Provenance is retained internally
and never presented to a customer as official media.

All five images are 560×746, longest edge below the 1000 px preference. They are
published at native size; nothing was upscaled and no canvas was manufactured.
These are portrait frames, not squares, and none was padded to become square.

MAIN is IMAGE 02 rather than the automation's filename-order proposal of
IMAGE 01 — on visual review IMAGE 02 reads better at thumbnail size, and
IMAGE 04 is a cropped upper detail, so it sits late in the gallery.

The manufacturer's juniors-series classification is internal only and appears
nowhere in the build.

### The correction this product records

An earlier pass rejected exactly this media as "a white-and-green Gazelle Bold,
not the pink JR5952". **That rejection was wrong.** `Almost Pink` is a very pale
tint and `Court Green` is part of the official colourway, so the imagery matched
the official variant precisely — correct media was discarded on a subjective
read of colour. The variant gate now reaches its conclusion from evidence rather
than impression, and the case is a permanent regression fixture.

The earlier BLOCKED / UNRESOLVED records for JR5952 and A08745C are
**superseded**; see `checkpoints/SUPERSEDED_*.md`, kept only as a record of how
those conclusions were reached and why they were wrong.

## Next step

Next Mall ID is **PM-029**, unallocated until a product is actually published.
Nothing is awaiting approval: the approval queue is empty.

Four products now come from the automated pipeline — PM-025, PM-026, PM-027,
PM-028. Only PM-026 has manufacturer-official media; the other three rest on
trusted-retailer evidence. Upgrading PM-027 and PM-028 to official imagery
remains open if an official route ever opens.
