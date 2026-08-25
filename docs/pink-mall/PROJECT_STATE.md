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
| JQ4556 PILOT | **PASS** — 4 exact official images, 1880×1880, zero manual preparation |

Acquired media: `docs/pink-mall/media-acquisition/JQ4556/`

| Image | Role | Size | SHA-256 |
|---|---|---|---|
| 01 | proposed MAIN — lateral | 1880×1880 | `cd35da4bc75864eb854c1735d69ef07c2fbf1a4d6335e975c3fef6be67fad7f4` |
| 02 | top-down | 1880×1880 | `0a0270dc1c9f63a5526c16db855c8d99c52774ebd80092476cd88505ad5bc96d` |
| 03 | outsole | 1880×1880 | `656cd37b2912f1a35136cc9c1dfa2685f9a9e3cba71ebf776052bba645be1bfb` |
| 04 | three-quarter front | 1880×1880 | `d7cb5f1b4a8eb723e937bf765a574e7c45c9f88340f6e65c07d8928f3b328f94` |

All four came from `assets.adidas.com`, seeded at `w_500` and upgraded to
`w_1880` — the CDN's own larger copy of the same photograph, each verified
perceptually against its 500px anchor. No AI upscaling. SKU present in every
asset URL. Visually confirmed as the exact pink / silver / gold variant,
product-only.

Two runs produced byte-identical images; only timestamps and run id differ,
so the pipeline is idempotent.

**Known limitation:** adidas product *pages* return 403 to the GitHub runner
(bot protection on datacenter IPs), and the courir fallback URL 404s. Page
scraping therefore contributed nothing; all four candidates came from
research-derived CDN seeds in the request manifest. For a SKU whose asset URLs
are not already known, discovery would need a different route.

## Proposed PM-025 media upgrade — needs APPROVE

The approved PM-025 set is the 500×500 archive under
`docs/pink-mall/approval-media/PM-025/`. The newly acquired set is the same
four views at 1880×1880, which resolves the standing resolution warning.

This is **not** applied. Per the onboarding skill, a photo-set change on an
approved product requires explicit approval. Say `APPROVE MEDIA UPGRADE PM-025`
to swap the approval package to the 1880px set, keeping MAIN and gallery order.

## Known non-blocking issue

Staged PM-025 product media is 500×500 web-derivative resolution. Acceptable
for approval and card preview; higher-resolution exact official duplicates are
preferred before launch and full PDP display. Do not AI-upscale.

## Next step

Explicit PM-025 approval, then a publication task.
