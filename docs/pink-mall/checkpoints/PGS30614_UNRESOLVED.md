# PINK MALL — Pepe Jeans PGS30614 onboarding

**STATUS: UNRESOLVED — NOT STAGED, NOT PUBLISHED, NO MALL ID ALLOCATED.**

Next Mall ID remains **PM-029**, unallocated.

## What the user supplied

| | |
|---|---|
| Brand | Pepe Jeans (pink) |
| Manufacturer item | PGS30614 |
| PINK MALL price | €34 |
| Available sizes | 39 |

## What is known, and how well

Search located a consistent identity: **Pepe Jeans "Ben Band"**, full article
code **PGS30614327** (base style `PGS30614` + colour `327`), a cotton twill
cupsole sneaker in pink, described by retailers as part of a **kids line**.

That identity comes from **search index snippets only**. Under this project's
own doctrine search is a *transport*, not evidence — it points at pages, and
the pages are what count. Every page it pointed at is gone or refuses us:

| Route | URL | Result |
|---|---|---|
| `DIRECT_OFFICIAL_PAGE` | pepejeans.com `/it_it/…PGS30614327.html` | **404** |
| `DIRECT_OFFICIAL_PAGE` | pepejeans.com `/pl_pl/…PGS30614327.html` | **404** |
| `DIRECT_OFFICIAL_PAGE` | pepejeans.com `/pt_pt/…PGS30614327.html` | **404** |
| `SEARCH_INDEX_OFFICIAL` | pepejeans.com `/en_be/women/womens-sneakers` | redirected to site root; 64 candidates, **no SKU on the page** |
| `TRUSTED_RETAILER_SEARCH` | esdemarca.com product page | **404** |
| `TRUSTED_RETAILER_SEARCH` | deporvillage.net product page | **403** |
| `TRUSTED_RETAILER_SEARCH` | tradeinn.com search + category | reachable; 164 candidates, **no SKU on the page** |

**404, not 403, on every official URL.** The hosts are reachable and the pages
do not exist. The most likely reading is that this article has been delisted
from Pepe Jeans' own storefronts and from the retailers that carried it, and
the search index is still serving cached entries for pages that are gone.

**No page reachable by the runner names PGS30614.** Zero images were acquired
in the second pass. That is the correct outcome, not a failure to try: the
first pass did return five images and every one was a tradeinn homepage
marketing banner, which is why two guards were added (see below).

## Why this is UNRESOLVED rather than BLOCKED

- `BLOCKED` would mean a reliable SKU exists and something about it conflicts.
- `UNRESOLVED` means no reliable exact identity can be established.

A cached search snippet is not a reliable exact identity. Nothing here ties
the SKU to a product on a live page, so nothing may be staged.

## The size question, separately

The supplied size is **39**. Retailers describe this article as a kids line,
and one snippet gives its scale as 32–37 while another gives 32–40. Those
contradict each other and neither is a source.

`sizeEvidence` in `result.json` is **empty** across both passes — no reachable
page declared a size scale for this SKU. So even if media were recovered, size
39 would still be unevidenced, and under the ladder-evidence rule a size that
no source confirms is a size-identity question for you, not something to
publish quietly.

## What would resolve it — the minimum

Any **one** of these is enough to restart:

1. A **live link** to the product on the supplier's site (any language).
2. A **supplier screenshot** showing the article code and the size run.
3. The **supplier's own code** for it, if it differs from PGS30614.
4. One or more **product photos** from the supplier.

If the supplier confirms **39** is genuinely offered, say so and it can be
published as the only available size — the user is always the source of truth
for availability. What is missing is not permission, it is a live source.

## What this run produced anyway

Two real defects in the pipeline, found and fixed:

- **`NON_PRODUCT_RE` anchored on a trailing slash**, so `/banners/` was caught
  and `/banners_home/` was not. Now matches any path segment *beginning* with
  a banner-ish word, and covers promo, campaign, hero and category segments.
- **No shape check.** A 1920×460 panorama is a page banner, never a studio
  product photograph. `validate_bytes` now rejects above 2.2:1.

Verified against reality: all 19 published live assets across PM-025…PM-028
still validate, and the genuine adidas, New Balance and Akinon asset paths are
still kept. Self-test 23 → 29.

Also added earlier in this task: **size-scale evidence** (`sizes_from_jsonld`),
which records the sizes a source declares for the exact SKU. It found nothing
here — which is itself the finding.
