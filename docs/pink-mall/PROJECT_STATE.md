# PINK MALL — project state

Updated: PM-038 and PM-039 publication.
Status: **PM-001…PM-039 PUBLISHED.**

This file records the real state. Trust it over any summary, and verify the
canonical build by hash before treating it as canonical.

## Canonical

| | |
|---|---|
| CANONICAL BRANCH | `claude/pink-mall-development` |
| CANONICAL WEBSITE | `PINKMALL.html` |
| CANONICAL WEBSITE SHA-256 | `9a58db3bb69135ecca41283b60b23a3745a4d6a7b2e6d815bc9b7d67ff3325cc` |
| CANONICAL WEBSITE BYTES | 2580381 |

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
| PUBLIC CATALOG | PM-001 … PM-039 |
| NEXT ID | PM-040 |
| JQ4556 | **PUBLISHED as PM-025** on 2026-08-25 |
| GC515KI | **PUBLISHED as PM-026** on 2026-08-25 |
| A08745C | **PUBLISHED as PM-027** on 2026-08-25 |
| JR5952 | **PUBLISHED as PM-028** on 2026-08-25 |
| PGS30614 | **PUBLISHED as PM-029** on 2026-08-26 |
| 398855 | **PUBLISHED as PM-030** on 2026-08-26 |
| HC.RBGLOW01 | **PUBLISHED as PM-031** on 2026-08-27 |
| 27733247 | **PUBLISHED as PM-032** on 2026-08-27 |
| TU0A28Z0699 | **PUBLISHED as PM-033** on 2026-08-27 |
| V69WBAG152 | **PUBLISHED as PM-034** on 2026-08-28 |
| 30S4SBAL2L | **PUBLISHED as PM-035** on 2026-08-28 |
| 35F4G2VC5L | **PUBLISHED as PM-036** on 2026-08-28 |
| 134-200-409 | **PUBLISHED as PM-037** on 2026-08-28 — unblocked by owner-supplied photographs |
| 40754650 (supplied alias 40754) | **PUBLISHED as PM-038** on 2026-08-29 |
| 4AR165 | **PUBLISHED as PM-039** on 2026-08-29 |

## Media acquisition automation

| | |
|---|---|
| AUTOMATION | PASS — `tools/media_acquisition/`, `.github/workflows/media-acquisition.yml` |
| SELF-TEST | PASS — `python tools/media_acquisition/selftest.py`, 94/94 guards |
| PUBLICATION REGRESSION | PASS — `tools/regression/product_regression.js`; PM-038 and PM-039, production + standalone |
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
| SHA-256 | `1808971957464d5d275158b75a45a5354de14c952bfc2d3114c865fbb450be64` |
| BYTES | 10463663 |
| LAST PUBLICATION VALIDATION | PASS — GitHub Actions run `33246543092`, PM-038 + PM-039 production and standalone |
| DEVELOPMENT REBUILD | PASS — GitHub Actions run `33246626108` |
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

## PM-029 — published

| | |
|---|---|
| PUBLISHED | 2026-08-26 |
| BRAND / MODEL | Pepe Jeans / Ben Band |
| MANUFACTURER ITEM | PGS30614 (full article PGS30614327) |
| RETAILER REFERENCE | PPJ-PGS30614-327 |
| PUBLIC COLOUR | Pink / Black (manufacturer: `factory pink`) |
| MATERIAL | **omitted** — not established by this pipeline |
| PRICE | €34, no SALE |
| INVENTORY MODE | availability |
| SIZES | 39 — available. **No sold-out sizes asserted** |
| EXACT-MODEL SIZE RUN | **PROVEN 32–40, contains 39** → `SIZE_CONFIRMED` |
| NEW UNTIL | 2026-09-09 (14 days from publication) |
| MAIN | IMAGE 01 — lateral side profile |
| GALLERY ORDER | 01 → 02 → 04 → 05 → 03 |
| LIVE MEDIA | `assets/pink-mall/products/PM-029/` — 1920×2652, 2× 1600×2210, 2× 1200×1658 |
| MEDIA TIER | **OFFICIAL** — `images.pepejeans.com`, manufacturer CDN |
| ACQUISITION | **zero-seed** — no user URL, no user images |
| VARIANT | `VARIANT_CONFIDENCE_PASS` |
| PACKAGE | `checkpoints/PM029_PGS30614_APPROVAL_PREVIEW.md` |

**Second product in the catalogue with manufacturer-tier imagery**, after
PM-026. PM-025, PM-027 and PM-028 all rest on trusted-retailer media.

Every original filename carries the full article code
`PGS30614_327_<view>_FL.jpg`, so each asset is self-evidencing on its own URL.
Resolution was raised by rewriting only the CDN's own `?sw=` sizing query; the
asset path is never touched and nothing was upscaled.

This is also the first product whose exact size scale was **proven** rather than
assumed. The manufacturer's 32–40 ladder is independently evidenced and contains
39, so `sizeState` is `SIZE_CONFIRMED` instead of `SIZE_SCALE_NOT_PROVEN`. Only
the user-supplied size is published; retailer stock state never touched PINK
MALL availability.

Identity rests on two independent provenance classes that agree: Claude's own
research across three official Pepe Jeans locale URLs and two retailers, and a
`REVIEWER_VERIFIED` read of the live Deporvillage product document. Reviewer
media was acquired and validated cleanly at 1600×2000 but is **not** used — the
source hierarchy puts manufacturer media above retailer media, and the selector
now enforces that rather than leaving it to routing.

Material omitted: retailers repeat a "70% sustainable cotton" line, which is a
sustainability claim rather than a composition, and all three official locale
URLs return 404.

One non-blocking gap: manufacturer view 03 was not recovered. Its opaque
`dw<hash>` path segment cannot be derived from the others and was not guessed.

The junior-series classification is internal only and appears nowhere in the
build.

## PM-030 — published

| | |
|---|---|
| PUBLISHED | 2026-08-26 |
| BRAND / MODEL | Puma / Palermo Moda |
| MANUFACTURER ITEM | 398855, colour suffix **-11** |
| PUBLIC COLOUR | Pink / Aqua (manufacturer: `Poised Pink / Aqua`) |
| MATERIAL | **omitted** — not established by this pipeline |
| PRICE | €44, no SALE |
| INVENTORY MODE | availability |
| SIZES | 37.5, 38, 38.5, 39 — all available. **No sold-out sizes asserted** |
| EXACT-MODEL SIZE RUN | NOT VERIFIED — non-blocking |
| NEW UNTIL | 2026-09-09 |
| MAIN | IMAGE 01 — lateral side profile |
| GALLERY ORDER | 01 → 05 → 03 → 04 → 02 |
| LIVE MEDIA | `assets/pink-mall/products/PM-030/` — 5 × 2000×2000 WebP **with alpha** |
| MEDIA TIER | **OFFICIAL** — `images.puma.com`, manufacturer CDN |
| MEDIA FORM | transparent cut-outs; `media.surface` omitted by design |
| ACQUISITION | **zero-seed**, by CDN probe |
| VARIANT | `VARIANT_CONFIDENCE_PASS` |
| PACKAGE | `checkpoints/PM030_398855_APPROVAL_PREVIEW.md` |

Third product with manufacturer-tier imagery, after PM-026 and PM-029.

**Two mis-targetings were caught by visual review before anything was staged**,
and neither would have been caught by status alone — every automated signal read
PASS in both cases.

The first was the wrong article: 401489 Club II Era was carried to acquisition
before the contact sheet showed `401489-04` to be an aquatic-primary shoe with a
pink formstripe rather than a pink shoe.

The second was the wrong colourway of the right article. 398855 ships eleven
colourways and the colour suffix was evidenced nowhere reachable; a first pass
selected five views of `398855-01`, Puma White / Puma Black, because the
official page serves the default colourway and its images outranked the sweep.
A reconnaissance pass then fetched one hero per colour code and put all eleven
on one sheet, which made `-11` unambiguous. The decoys sat beside it — `01`
white/black, `03` mint/mauve, `07` coral, `10` cream with a pale pink stripe —
and each would have satisfied a check that verified only the article number.

Identity is pinned twice: article number and colour suffix both appear in every
acquired asset path.

`media.surface` is omitted deliberately. These are transparent cut-outs, so the
mall's own neutral token shows through rather than the `#47704C` the pipeline
originally derived by flattening a transparent PNG.

## PM-031 — published

| | |
|---|---|
| PUBLISHED | 2026-08-27 |
| BRAND / MODEL | Colors of California / Glossy rainboot |
| MANUFACTURER ITEM | HC.RBGLOW01, colour code **FUX**, season code F24 |
| CATEGORY | SHOES > **Boots** — new subcategory, approved by the user |
| PUBLIC COLOUR | Pink (manufacturer: `Fuxia`) |
| MATERIAL | **omitted** — no composition string was read from the source |
| PRICE | €64, no SALE |
| INVENTORY MODE | availability |
| SIZES | 36, 37, 38, 39, 40 — all available. **No sold-out sizes asserted** |
| EXACT-MODEL SIZE RUN | `SIZE_SCALE_NOT_PROVEN` — non-blocking |
| NEW UNTIL | 2026-09-09 |
| MAIN | IMAGE 01 — lateral side profile |
| GALLERY ORDER | 01 → 02 → 03 → 05 → 04 |
| LIVE MEDIA | `assets/pink-mall/products/PM-031/` — 5 × 1200×1200 WebP, opaque |
| MEDIA TIER | **OFFICIAL** — `hub2.artcrafts.it`, the brand owner's own CDN |
| MEDIA FORM | photographs on white; `media.surface: '#FFFFFF'` |
| ACQUISITION | **zero-seed**, four passes |
| VARIANT | `VARIANT_CONFIDENCE_PASS` |
| WARNINGS | one, non-blocking — 1200×1200, above the 1000 px preference, below the 1600 px ideal |
| PACKAGE | `checkpoints/PM031_HCRBGLOW01_APPROVAL_PREVIEW.md` |

**First non-sneaker product**, and the first to use `SHOES > Boots`. The
storefront reads `subcategory` in exactly one place — the search haystack — so
the new value is additive and needed no engine change; this was checked rather
than assumed, and the SHOES category's Bulgarian terms already included
`ботуши`.

Fourth product with manufacturer-tier imagery, after PM-026, PM-029 and PM-030.
The tier is a verified claim rather than an inference from the hostname:
Artcrafts International S.p.A. owns and operates Colors of California, so
`hub2.artcrafts.it` is the brand owner's host — the same standing already
accepted for `images.pepejeans.com` and `nb.scene7.com`.

The colour code resolved itself. Fetching the bare product URL redirected to
`?color=FUX`, so the source chose the colourway — a cleaner outcome than the
eleven-colourway reconnaissance sweep PM-030 needed.

Two pipeline defects were found and fixed by this product:

The identity gate had been rejecting the manufacturer's own images.
`HC.RBGLOW01` is not a substring of `HC.F24.RBGLOW01-FUX-1.jpg`, because the
season code is inserted mid-code. `sku_signal()` now also matches aliases
carried on evidenced documents, so a source that renames its own article code
cannot lock the pipeline out of that source's media.

The tier classifier read `artcrafts.it` as a trusted retailer. It is the brand
owner, and misreading it would have understated the provenance of correct media.

### Publication was redone after a container recycle

The working clone was reclaimed mid-publication, before the work was committed.
Everything was rebuilt from the committed originals and **all five live files
reproduced byte-for-byte**, which is the useful fact: the JPEG → WebP
conversion is deterministic, so the live media is a pure function of the
acquired sources rather than of one machine's state.

The lesson taken from it is in the next section.

## Publication regression is now a committed tool

`tools/regression/product_regression.js` drives real Chromium against a served
copy of the site and asserts what a reviewer would look for: the record, the
media, the card, search, the PDP, the order path, and that no previously
published product moved. It runs against **both** builds — the canonical file
with its `assets/` tree, and the portable standalone from an empty directory —
and reads its expectations from `tools/regression/expect/<ID>.json`.

Before this, the suite was rewritten by hand for each publication and lost with
the container each time; it was written three times for PM-031 alone.

Three things it does that the earlier throwaway versions got wrong:

**Frames are identified by the SHA-256 of their bytes, never by filename.** The
portable build inlines every image as a `data:` URI, so a filename check there
tests the harness's assumptions instead of the artifact. Hashing works in both
builds and additionally proves the inlined bytes *are* the live files' bytes.

**It waits on the image decode, not on a guessed interval.** Cards are
`loading="lazy"`; a fixed sleep made the check flake under load.

**Every 4xx is recorded with its URL.** A bare console `404` carries no URL, so
an intermittent miss was previously unattributable. One such 404 was seen
during PM-031's runs and never reproduced under instrumentation; it is not
suppressed — if it recurs, the run fails and names the URL.

Known-clean exception: this container's egress proxy resets
`fonts.googleapis.com`. Verified identical on builds predating the product, so
it is an environment fact, not a product defect.

## PM-032 — published

| | |
|---|---|
| PUBLISHED | 2026-08-27 |
| BRAND | Scotch & Soda — **confirmed from the product itself** |
| MODEL | `Celest` — **owner-asserted, not evidenced by any source reached** |
| MANUFACTURER ITEM | 27733247 (colour code: brief `34A` vs supplier `S059`) |
| CATEGORY | SHOES > Sneakers |
| PUBLIC COLOUR | Pink (manufacturer: `Rose`) |
| MATERIAL | **omitted** |
| PRICE | €69, no SALE |
| INVENTORY MODE | availability |
| SIZES | 37, 38, 39, 40 — all available. **41 held by the owner but not offered**, under the Mall's EU 36-40 cap |
| SIZE STATE | `SIZE_CONFIRMED` against the line's declared EU 36-42 scale |
| NEW UNTIL | 2026-09-10 |
| MAIN | IMAGE 01 — three-quarter front, pair |
| GALLERY ORDER | 01 → 02 → 03 |
| LIVE MEDIA | `assets/pink-mall/products/PM-032/` — 3 × **480×720** WebP |
| MEDIA TIER | **USER_SUPPLIED** — not manufacturer, not retailer CDN |
| MEDIA FORM | grey studio gradient; `media.surface: '#D2D5D7'`, measured |
| WARNINGS | lowest-resolution media in the catalogue; no side profile; 3 images is the policy minimum |
| PACKAGE | `checkpoints/PM032_27733247_APPROVAL_PREVIEW.md` |

**The first product whose media came from the owner rather than a supply
chain.** Every automated route was walled, so the owner supplied three
photographs directly and approved publication with the shortfalls stated.

Resolution is the known weakness. Measured against the storefront's real render
boxes, the PDP hero is 36% short on desktop @2x and **54% short on phone @3x**;
cards are effectively fine. Nothing was upscaled — that rule does not bend
because a source is small. Larger files would fix this in one step.

`media.surface` is measured rather than chosen: the backdrop is a grey gradient
so no flat colour could be derived, and `#D2D5D7` is the median border tone.
Without it the Mall's lighter neutral would have drawn a bright rectangle
around every photograph.

Identity is deliberately split in the record. The brand is confirmed from the
product — tongue patch and the circular Amsterdam insole monogram. The **model
name is not**, and the supplier names models for other shoes of this brand
while leaving this article unnamed, and every Celest listing found is
multicolour where this shoe is monochrome. "Celest" stands because the owner
knows their own stock, not because a source said so.

## How it got here — DISCOVERY_TRANSPORT_BLOCKED

| | |
|---|---|
| STATE | resolved by owner-supplied media; see PM-032 above |
| BRAND / MODEL | Scotch & Soda / Celest |
| SUPPLIED | article 27733247, colour "34A Rose", €69, sizes 37-41 |
| PUBLISHABLE SIZES | 37, 38, 39, 40 — the user chose to keep the Mall's EU 36-40 cap, so the supplied 41 is not listed |
| SIZE STATE | `SIZE_CONFIRMED` against the line's declared EU 36-42 scale |
| PASSES | 4 runner passes, ~25 research queries |
| STATUS | `DISCOVERY_TRANSPORT_BLOCKED` — refusal **not** permitted by the gate |

**Who owns the number.** 27733247 is a **MODIVO S.A. / eobuwie group** article
number, not a Scotch & Soda code. The brand's own Shopify store indexes
`78-XXXX-XX` style codes and returns no product for the 8-digit form. The group
runs one catalogue across obuvki.bg, eobuwie.com.pl, modivo.pl and formerly
efootwear.eu.

That is also why no other retailer can be searched for it: Zalando, About You
and GLAMI each use their own numbering, so the article number simply does not
exist outside MODIVO's catalogue.

**Why it is blocked rather than absent.** Every MODIVO URL returns 404 to the
runner — *including the brand listing page that demonstrably exists*. A 404 on
a page known to exist is bot protection, not evidence of absence. Separately,
eskor.se now serves `/b/closedsite`, and the archive routes timed out on the
runner, so `INDEXED_OUTBOUND_MEDIA` and `INDEXED_SOURCE_EVIDENCE` never
answered. The refusal gate therefore correctly refuses to permit a refusal:
these are transport failures, not evidence failures.

**What research did establish**: the 8-digit MODIVO numbering and its series
for this line (18733464, 19733142/4/5, 21731101, 22733693, 22733735, 23733437/8,
24733608); that the trailing token is a Scotch & Soda colour code, so "34A"
reads as colour rather than size; that a Celest colourway named "Rose" exists;
the official EU 36-42 scale; and the model's construction — cow suede and nylon
panels, customised rubber sole, recycled mesh lining.

**What it did not establish**, and what nothing may be published without: that
article 27733247 *is* the Rose / 34A colourway. At least ten other Celest
articles sit in the same catalogue, several of them pink.

### Pass 4: the user's own supplier document, also blocked

The user supplied their supplier's eMAG listing for this exact article and
asked for photos to be retrieved from it. It is a genuine product document —
eMAG's grammar is
`scotch-soda-<type>-<colours>-<size>-<ARTICLE>-<COLOURCODE>-<size>/pd/<id>/`,
matching sibling listings such as `21733094-s441` and `19739108-s145` — and it
is the first document in four passes to carry 27733247 in a product path
rather than a query string.

**eMAG returns HTTP 511 to the runner.** That is Network Authentication
Required: the site actively declining automated access. MODIVO returns 404 to
the same client on pages that demonstrably exist. archive.org is blocked from
the container and times out from the runner.

Every automated transport is now walled by commercial bot protection. **No
browser-driven bypass will be built for this.** A 511 is the site stating that
automated access is not permitted, and defeating it would be circumventing an
access control rather than solving a discovery problem. That is a line, not a
missing feature.

Two identity facts remain open and must not be smoothed over:

- **Colour code.** The brief says `34A Rose`; the supplied URL says `S059`.
  Both readings agree the shoe is pink suede, and the article number is the
  anchor, but the codes are not the same.
- **Model name.** eMAG's title for this article is only "Спортни обувки с
  велур" with no model. That retailer *does* name models when it has them —
  `Кецове Sylvie`, `Спортни обувки Vivi` — so its silence here is not proof of
  "Celest", which so far rests on the user's brief alone.

The one remaining route is the image files themselves, supplied directly. That
involves no circumvention.

### A false acceptance was caught and fixed here

Pass 1 returned `PARTIAL` at **OFFICIAL tier** carrying a Scotch & Soda
knitwear close-up as if it were the sneaker.

`page_has_sku` tested the page's whole URL, so `/search?q=27733247` "named the
SKU" because the article number sat in the query string **we supplied** — our
own query reflected back and read as the page's assertion — and `og:image`
counts as an authoritative declaration. The gate was half right: it had already
rejected that identical asset when it arrived via `html-scan`.

A search or listing route now lends no identity to its own images. That is not
a tightening of evidence but a correction of what the route is for: its value
is the product links it yields, which link-target recovery already follows to
real product pages. Nine guards pin the recognised search forms and, equally,
that genuine product routes are not caught by them.

An audit of every previously acquired image confirmed **no published media was
affected**: all of PM-025 through PM-031 rest on either `asset-url` evidence or
`source-page` evidence from genuine product documents.

This is the mirror of the false-refusal work, and the more dangerous direction:
with three such images the run would have reached PASS and put knitwear on the
storefront as a pink sneaker at official provenance.

## PM-033 — published

| | |
|---|---|
| PUBLISHED | 2026-08-27 |
| BRAND / MODEL | Stella McCartney / **Pineapple Bucket Bag** |
| ITEM | TU0A28Z0699 (designer `TU0A28Z0699 226VI`; Giglio `401012.003`) |
| CATEGORY | BAGS, `subcategory: null` — **first non-shoe pipeline product** |
| PUBLIC COLOUR | `Yellow` — frames show yellow WITH pink waves; see below |
| COMPOSITION | **`100% Polyurethane` — PUBLISHED**, a catalogue first |
| DIMENSIONS | omitted — no exact-product evidence |
| PRICE | €109, no SALE |
| AVAILABILITY | ONE SIZE, verified against the live engine |
| NEW UNTIL | 2026-09-10 |
| MAIN | IMAGE 01 · GALLERY 01 → 02 → 04 → 03 |
| LIVE MEDIA | `assets/pink-mall/products/PM-033/` — 4 × 1125×1500 WebP |
| MEDIA TIER | **TRUSTED_RETAILER** — Giglio, not manufacturer media |
| MEDIA FORM | studio white ~`#ECECEC`; `media.surface` **omitted**, not chosen |
| VARIANT | `VARIANT_CONFIDENCE_PASS` |
| WARNINGS | 1500 px longest edge — above the 1000 px preference, below the 1600 px ideal |
| PACKAGE | `checkpoints/PM033_TU0A28Z0699_APPROVAL_PREVIEW.md` |

**First product to publish a composition.** PM-026 through PM-032 all omitted
one because no exact-product source stated it; here the exact-SKU document
does, so the PDP renders a material row for the first time.

Reached PASS through the reviewer-verified transport after every direct route
was walled — four exact observed link targets, put through the full pipeline
rather than trusted on sight.

**A colour correction to my own earlier reporting.** I had said this product
was "yellow, not pink" and would be the catalogue's first non-pink supplier
item. That was wrong, and drawn from retailer text rather than the photographs:
the body carries a pink scalloped wave print over roughly half its visible
surface, with a green pineapple-leaf drawstring and a lilac strap. `Yellow /
Pink` would be more accurate; that was put to the user rather than changed
unilaterally, and the alt text names all four colours.

### Two harness defects the first BAGS product exposed

The regression suite had been written entirely against multi-size shoes:

- It asked for `sizes[1]`, which is `undefined` on a ONE SIZE product, so the
  whole order path failed on a product whose order path was fine.
- It scanned the entire PDP for sold-out text, but the sheet renders a
  related-products strip — a sold-out neighbour there is not a claim about this
  item. The check is now scoped to the product's own availability.
- It required price monotonicity across the whole sorted list, which
  contradicts the engine's documented sold-out-bottom ordering. Monotonicity
  now holds across available products, and sold-out ones are asserted to come
  last.

Composition expectation is now declared per product instead of assumed absent.

## TU0A28Z0699 — approval record

| | |
|---|---|
| STATE | acquired, staged, **not published** |
| BRAND / MODEL | Stella McCartney / **Pineapple Bucket Bag** |
| ITEM | TU0A28Z0699 (designer `TU0A28Z0699 226VI`; Giglio `401012.003`) |
| CATEGORY | BAGS, `subcategory: null` — first BAGS product from the pipeline |
| COLOUR | `Yellow` as specified; **frames show yellow WITH pink waves** |
| COMPOSITION | **`100% Polyurethane` — published**, from the exact-SKU document |
| DIMENSIONS | omitted — no exact-product evidence |
| PRICE | €109, no SALE |
| AVAILABILITY | ONE SIZE, verified against the live engine |
| MEDIA | 4 × 1125×1500 from `img.giglio.com` |
| TIER | **TRUSTED_RETAILER** — not manufacturer media |
| VARIANT | `VARIANT_CONFIDENCE_PASS` |
| PACKAGE | `checkpoints/PM033_TU0A28Z0699_APPROVAL_PREVIEW.md` |

First product to publish a composition: PM-026 through PM-032 all omitted one
because no exact-product source stated it. Here the exact-SKU document does.

**Two things the visual review corrected in my own earlier reporting.** I said
this product was "yellow, not pink" and would be the first non-pink supplier
product — wrong, and based on retailer text rather than the photographs; the
body carries a pink scalloped wave print over roughly half its visible surface.
An early search summary claiming a "purple waves print" was also wrong: the
waves are pink and the strap is lilac.

`media.surface` is omitted rather than asserted. Three frames sit on a studio
white of about `#ECECEC` and the fourth is a tight crop with no backdrop, so no
consensus existed; the Mall neutral is within three levels of that white.

## Two authority defects fixed here

**`allowed_hosts` was being read as authority.** `_authority_tier` seeded
OFFICIAL from the *network permission* list, so every trusted retailer in a
brand's registry read as manufacturer media — these Giglio routes among them.
The damage went past mislabelling: the same function decides whether to keep
hunting for official media, so a retailer answering "yes, I am official"
silently switched official discovery off, inverting the source hierarchy.

Manufacturer authority is now declared explicitly and nowhere else —
`official_hosts` on the brand, `officialHostSuffixes` on the request for an
evidenced CDN. Everything merely allowed defaults to TRUSTED_RETAILER. The real
CDNs keep their standing because each was evidenced rather than assumed;
`cdn.shopify.com` is deliberately excluded as a shared platform host.

**Identity was tied to media.** `exactProductDocument` was written twice in one
dict literal, and the surviving write required media or sizes — so a document
whose gallery is client-rendered stopped counting as exact identity. Exactness
is now an explicit `skuInBody` assertion from a transport that read the body,
never inferred from a SKU in a path we chose to request.

## PM-037 — published (previously BLOCKED)

| | |
|---|---|
| PUBLISHED | 2026-08-28 |
| BRAND / MODEL | VEE Collective / **Porter Messenger Mini** |
| ITEM | 134-200-409, variant `Seashell Pink` |
| CATEGORY | BAGS, `subcategory: null` |
| PUBLIC COLOUR | `Pink` (manufacturer: Seashell Pink) |
| COMPOSITION | omitted — no exact-product source states one |
| PRICE | €59, no SALE |
| AVAILABILITY | ONE SIZE |
| NEW UNTIL | 2026-09-11 |
| MAIN | SUPPLIED 02 · GALLERY main → 02 → 03 |
| LIVE MEDIA | `assets/pink-mall/products/PM-037/` — 3 × 1200×1500 WebP |
| IDENTITY TIER | TRUSTED_RETAILER — `tootsies.com`, `VARIANT_CONFIDENCE_PASS` |
| MEDIA TIER | **USER_SUPPLIED** — recorded separately from identity |
| SURFACE | `#E8E8E8`, measured median border |

This clears the last standing **BLOCKED — PHOTO SET INCOMPLETE** record. The
article had one unique exact-SKU image where the policy needs three; the owner
supplied three, and they were checked against the evidenced image rather than
taken on trust — same quilted body, same knotted straps, same pale pink, and
every pair perceptually distinct at a minimum distance of 57 where a duplicate
scores 4 or below.

Identity and media are recorded as separate claims. Identity is trusted-retailer
and established the model name, variant and `O/S` scale; the photographs carry
no source URL and establish nothing but themselves, so the media tier is
USER_SUPPLIED and does not inherit the retailer's standing.

The evidenced 1600×1600 tootsies image stays on record but is out of the
gallery: it is 1:1 where the supplied frames are 4:5, and one gallery should not
mix aspect ratios.

Files were copied rather than re-encoded — they were already WebP, and a second
pass would only have cost quality — so the live hashes equal the originals'.

## SPARKS/G/S 8CQ — PHOTO SET INCOMPLETE (identity established)

| | |
|---|---|
| STATE | **not staged, not published** |
| BRAND / MODEL | Jimmy Choo / Sparks (Safilo licence) |
| ITEM | `SPARKS/G/S`, colourway **8CQ** (sold as 8CQ/U1), 55-17-140 |
| CATEGORY | ACCESSORIES, `subcategory: null` |
| PRICE / AVAILABILITY | €71 · ONE SIZE (user source of truth) |
| IDENTITY | **ESTABLISHED** — exact-SKU, asset-url evidence via the colour-scoped alias |
| MEDIA | **1 unique image** at 800×800; policy minimum is 3 |
| TIER | TRUSTED_RETAILER (`cdn2.jomashop.com`) |
| PASSES | 4, across 6 retailer catalogues and 3 official URLs |

**The colour is not pink, and that matters for the listing.** The acquired frame
is translucent **plum / wine-purple with rose-pink lenses** and a crystal-set
CHOO logo on the temple. Retailer text agrees on the purple reading — eBay via
Otticanet says VIOLET, SmartBuyGlasses says Transparent Purple with Pink
lenses, Go-Optic says Cherry — against Jomashop and Timepiece, which say
"pink" and appear to be describing the lenses. The user's brief said "Jimmy
Choo Pink". The public colour must follow the frame and the exact wording is
the user's to choose.

**Why only one image.** Four passes reached jomashop, timepiece,
smartbuyglasses, designerframesoutlet, occhialando and three jimmychoo.com
URLs. Retailers carry a single catalogue shot for this discontinued frame:
timepiece yielded 13 candidates and designerframesoutlet 64, none carrying the
article code in the asset path. The official route returned **403 on all three
URLs** — bot protection, recorded as unreachable rather than as evidence that
no official media exists.

Resolution is capped at 800×800 by the retailer's baked cache path. That is a
real ceiling on that asset, not a missed transform.

### Three generic defects this product exposed, all fixed

1. **Slashed article codes broke the output path.** `SPARKS/G/S` joined onto a
   path silently created nested directories instead of one product folder. Only
   the path is sanitised; the code keeps its slashes wherever identity is
   judged. The folder now also carries the colour code, because this model
   ships 8CQ, 8CO and 1N5 and two colourways would have overwritten each other.
2. **Entity-escaped URLs were fetched verbatim.** The asset URL carried
   `?width=800&amp;height=800`, so the second parameter reached the server named
   `amp;height` and was ignored. Scraped URLs are now decoded wherever
   candidates are assembled.
3. **The size-transform regex was too narrow.** It covered Scene7's `wid`/`hei`
   but not the spelled-out `width`/`height` a Magento storefront uses, so a
   larger copy of the asset was never requested and 800px was accepted as
   though it were all the CDN had.

### What would complete it

Three product photographs, as for VEE Collective 134-200-409. Padding the
gallery with the same shot twice, or borrowing a neighbouring colourway, are
both excluded.

## Bounded SPA rendering — built, proven, and refused by one site

`tools/media_acquisition/render.py` renders ONE already evidenced product URL
when a client-side storefront hides its gallery behind JavaScript. It is not a
crawler and not a search engine.

**Every precondition must hold**: allowed host, 2xx, OFFICIAL or
TRUSTED_RETAILER, the article named in the **body** rather than only in the path
we requested, no usable media in the served HTML, and the page classified as a
shell. Rendering an arbitrary search result because the article appears in its
query string is refused by that gate.

**Bounds**: navigation, hydration and overall timeouts; no downloads, no login,
no form submission; popups closed on open; a render that ends on another origin
is discarded rather than read. Sub-resources load normally — that is how the
gallery appears and how a CDN host gets observed instead of guessed.

**Rendering approves nothing.** Discovered URLs are recorded as the
non-authoritative method `js-rendered` and go through the unchanged pipeline:
allow-list, bytes, MIME, dimensions, non-product and banner guards, exact SKU or
evidenced alias, hash, dedupe, perceptual uniqueness, tier selection, variant
confidence. A rendered retailer gallery does not suppress official routes.

**Refusal semantics**: `JS_RENDERED_PAGE` is an audited route. An identified
exact-SKU shell whose render has *not been tried* forbids refusal outright,
reports `spaRenderPending`, sets `userInputPermitted: false` and yields status
`SPA_RENDER_REQUIRED`. A render that ran and was refused is **unreachable, not
pending** — conflating the two would report a route that answered as one that
never ran.

The self-test round is hermetic. Its fixture shell fetches the gallery at
runtime, so the HTTP parser is genuinely blind to it, and the round proves: the
parser finds nothing, the renderer finds all four assets, those reach normal
acquisition and PASS, the banner is still rejected, a URL-only SKU match and an
untrusted tier do not qualify, and a render timeout is a transport failure
rather than an answer.

### Against Giglio specifically: the site declines the browser

Four render attempts, each failing earlier in the stack than the last, and each
correctly recorded as a transport failure rather than an answer:

| Attempt | Result | Cause |
|---|---|---|
| 1 | `ERR_HTTP2_PROTOCOL_ERROR` | h2 handshake; fixed with `--disable-http2`, a protocol flag that leaves our identity intact |
| 2 | navigation timeout | our own blanket request interception; origin guard moved post-navigation |
| 3 | timeout at `commit` | server never begins responding |
| 4 | timeout at `commit`, **control page renders fine** | **the site does not answer this client** |

The control check is the decisive one: the runner's Chromium loads a neutral
page normally, and the plain HTTP fetcher gets **200** from the very same
Giglio URL. Only the headless browser is left unanswered.

**No further attempt will be made.** Getting past this requires user-agent
spoofing or fingerprint masking — disguising who is asking. That is the same
line drawn at eMAG's HTTP 511, and `--disable-http2` does not cross it because
it changes protocol negotiation, not identity.

### What remains established for TU0A28Z0699

Pineapple-shaped bag, Stella McCartney Kids line, yellow, ONE SIZE, composition
`100% Polyurethane` from the exact-SKU Giglio document. ONE SIZE verified
against the live engine. Dimensions remain unpublishable. The bag is **yellow,
not pink**, and the child-series classification stays internal.

Media: **none acquired.** Identity is established; media is not.

## Stella McCartney TU0A28Z0699 — earlier record

| | |
|---|---|
| STATE | identity established; media not acquired; nothing staged or published |
| BRAND | Stella McCartney (Kids line — internal only, never public) |
| PRODUCT | Pineapple-shaped bag |
| SUPPLIED | article TU0A28Z0699, €109, ONE SIZE |
| EXACT-SKU SOURCE | **Giglio — reachable, and its body names the article** |
| BLOCKER | the retailer is a client-side app; the runner receives a ~2.4 kB bootstrap shell |
| PASSES | 7 |

### The earlier DISCOVERY_TRANSPORT_BLOCKED conclusion was WRONG

It was corrected by review, and the correction was right. An exact-SKU document
existed the whole time on a trusted retailer that had **never entered the
candidate set** — not unreachable, simply never searched for. Discovery had run
against a fixed list of already-known hosts, and exhausting that list was
treated as exhausting discovery.

Two further claims made at the time were also overstated and are withdrawn:

- "Stella's own search not returning the code proves it is a wholesale code" —
  it supports that hypothesis and proves nothing. Recorded as inference.
- "Official media can never clear the identity gate" — not established.

### Four defects this product exposed, all generic, all fixed

1. **Discovery treated a known-host list as exhaustive.** `NEW_RETAILER_DISCOVERY`
   is now a refusal route, satisfied only by a ledger entry from a domain
   outside the run's starting host set. Suffix-aware, so a subdomain of a known
   host is not a new source, and an unreachable new domain does not satisfy it.
2. **Relative image references were invisible.** `//cdn/x.jpg` and `/media/x.jpg`
   are now recovered and resolved against the page URL.
3. **JSON-escaped URLs were invisible.** `https:\/\/host\/x.jpg`, the form modern
   storefronts ship galleries in, is now normalised before matching.
4. **`page_has_sku` conflated two different facts.** A hit in the requested URL
   is partly our own doing; a hit in the body is the document naming the
   article. `sku_match_where` now reports which, alongside the served HTML size
   and a shell flag.

Each was masked by the one before it, which is why they surfaced one at a time.

### Where it actually stands

The Giglio product URL resolves, and `sku_evidence_where: body` — the served
document **does** name the article. But `html_bytes` is ~2,390 on every Giglio
URL including the product pages, with zero image references in any form after
three parsing fixes.

That is a client-side application: the real document, gallery included, is
assembled by JavaScript after load. **This is a capability limit of an
HTTP-only fetcher, not a parsing gap, not bot protection, and not evidence of
absence.** Giglio returns 200 and blocks nothing.

Two honest ways forward, neither taken unilaterally:

- **Render the page.** A JavaScript-rendering fallback for pages flagged
  `shell_suspected` would fix this permanently and would fix every SPA
  storefront after it. It is a real capability addition, so it is a decision to
  take deliberately rather than mid-onboarding.
- **Take the four observed asset URLs from the reviewer transport**, which has
  the page readable. The host `img.giglio.com`, the product code `401012.003`
  and views `_1`–`_4` are already recorded; only the path prefix is missing.
  Constructing it was explicitly ruled out, and constructing it would be
  guessing.

### Established for this article

Pineapple-shaped bag, Stella McCartney Kids line, yellow, ONE SIZE, composition
`100% Polyurethane` from the exact-SKU Giglio document. ONE SIZE was verified
against the live engine: availability mode yields stock state `ok`, is
orderable, and refuses any other size, so no calibration is needed.

Dimensions remain unpublishable — the widely repeated `14 × 17 × 11 cm` appears
only in search paraphrase and on a Smallable page that does not name the
article. Smallable is corroborating model evidence only (`Pineapple Seal Bag`,
yellow, ONE SIZE, polyurethane).

The bag is **yellow, not pink**, and it is a child-series article: the
classification stays internal, and the honest size signal for a buyer is
dimensions, which cannot yet be published.

## Stella McCartney TU0A28Z0699 — superseded record

| | |
|---|---|
| STATE | **no media acquired, nothing staged, nothing published** |
| BRAND | Stella McCartney (Kids line — internal only, never public) |
| PRODUCT | Pineapple-shaped crossbody bag |
| SUPPLIED | article TU0A28Z0699, €109, ONE SIZE |
| CATEGORY | BAGS, `subcategory: null` |
| PASSES | 3 runner passes across ~10 hosts |
| STATUS | `DISCOVERY_TRANSPORT_BLOCKED` — refusal **not** permitted by the gate |

**The split that blocks this product.** Every page that names the article is
unreachable, and every reachable page does not name the article.

| Host | Reachable | Names TU0A28Z0699 |
|---|---|---|
| littletagsluxury.com | 404 (all 3 URL forms) | **yes** — only known document |
| italist.com | 404 (both regions) | likely |
| farfetch.com | **403 Forbidden** | likely |
| childrensalon.com | 404 | unknown |
| kids21.com | 404 | unknown |
| smallable.com | **yes** | **no** (`page_has_sku: False`) |
| modesens.com | **yes** | **no** |
| stellamccartney.com | **yes** | **no** |

Stella's own search returning nothing is the decisive measurement:
**TU0A28Z0699 is a wholesale style code, not the brand's e-commerce ID.** The
brand indexes K-codes such as `K03231PK02407203`. So official media cannot
clear the identity gate for this article no matter how many passes are run —
the gate is working, not failing.

The colon in the Little Tags URL was tested and ruled out: it 404s
percent-encoded, literal, and via that site's own search.

Established routes are exhausted. `INDEXED_OUTBOUND_MEDIA` and
`INDEXED_SOURCE_EVIDENCE` have still never answered on this runner, a
structural limitation already documented across earlier products; aiming them
would mean re-engineering the index budget, which is architecture work and out
of scope for a normal onboarding.

**What is established** (identity, not media): the product is a pineapple-shaped
crossbody bag from the Stella McCartney Kids line, yellow, ONE SIZE, and the
brand's own copy for the same-theme bag describes Alter Mat — its vegan
alternative to animal leather — with scallop prints and a green drawstring
shaped like a pineapple top.

**What is NOT established**: any media bound to this article, and the widely
repeated `14 × 17 × 11 cm` / `100% polyurethane` figures, which appear only in
search-engine paraphrase and therefore may not be published as specifications.
An early summary also claimed a "purple waves print" that contradicts the
brand's own green-drawstring description and appears in no document.

Two things a human should note when this resumes: the bag is **yellow, not
pink**, which would make it the first non-pink real supplier product; and it is
a **child-series article**, so the classification stays internal and the honest
size signal for a buyer is dimensions — publishable only once a document
states them.

## Next step

Next Mall ID is **PM-033**, unallocated until a product is actually published.
Nothing is awaiting approval: the approval queue is empty.

Eight real supplier products now exist — PM-025 through PM-032. Four have
manufacturer-official media (PM-026, PM-029, PM-030, PM-031); PM-025, PM-027
and PM-028 rest on trusted-retailer evidence; **PM-032 is the first on
owner-supplied media**. Upgrading any of them if an official route opens
remains available, and PM-032 is the one that would gain most — larger files
alone would fix its only real weakness.

**A standing caution from PM-032:** commercial bot protection now walls the
runner at both eMAG (HTTP 511) and the MODIVO group (404 to automated
clients). No bypass will be built for either. Where a retailer declines
automated access, the owner-supplied route is the answer, and its weaker
provenance must be stated in the package rather than dressed up.


## PM-034 — published

| | |
|---|---|
| PUBLISHED | 2026-08-28 |
| BRAND / MODEL | 19V69 ITALIA / LIERNA |
| MANUFACTURER ITEM | V69WBAG152 |
| PUBLIC COLOUR | Pink |
| COMPOSITION | 80% Polyamide / 20% Polyurethane |
| PRICE | €74, no SALE |
| INVENTORY MODE | availability |
| SIZES | ONE SIZE — available |
| NEW UNTIL | 2026-09-11 |
| MEDIA | 4 official exact-product frames, selected from acquisition PASS |
| TIER | OFFICIAL |
| VARIANT | VARIANT_CONFIDENCE_PASS |

## PM-035 — published

| | |
|---|---|
| PUBLISHED | 2026-08-28 |
| BRAND / MODEL | Michael Kors / Colby Medium Leather Shoulder Bag |
| MANUFACTURER ITEM | 30S4SBAL2L |
| PUBLIC COLOUR | Smokey Rose |
| COMPOSITION | 100% Leather |
| PRICE | €119, no SALE |
| INVENTORY MODE | availability |
| SIZES | ONE SIZE — available |
| NEW UNTIL | 2026-09-11 |
| MEDIA | 4 trusted-retailer exact-variant frames; person-containing IMAGE 02 excluded |
| TIER | TRUSTED_RETAILER — Giglio |
| VARIANT | VARIANT_CONFIDENCE_PASS |

## PM-036 — published

| | |
|---|---|
| PUBLISHED | 2026-08-28 |
| BRAND / MODEL | Michael Kors / Vincent Small Saffiano Leather Crossbody Bag with Signature Logo Card Case |
| MANUFACTURER ITEM | 35F4G2VC5L |
| PUBLIC COLOUR | Powder Blush |
| COMPOSITION | 100% Leather |
| PRICE | €104, no SALE |
| INVENTORY MODE | availability |
| SIZES | ONE SIZE — available |
| NEW UNTIL | 2026-09-11 |
| MEDIA | 4 official exact-SKU frames from assets.michaelkors.com |
| TIER | OFFICIAL |
| VARIANT | VARIANT_CONFIDENCE_PASS |

## PM-038 — published

| | |
|---|---|
| PUBLISHED | 2026-08-29 |
| BRAND / MODEL | Dr. Martens / Metallic Shift Leather Heart Shaped Bag |
| MANUFACTURER ITEM | 40754650; supplied alias/base style 40754 |
| CATEGORY | BAGS, `subcategory: null` |
| PUBLIC COLOUR | Powder Pink / Gold |
| COMPOSITION | PU Coated Suede |
| PRICE | €104, no SALE |
| INVENTORY MODE | availability |
| SIZES | ONE SIZE — available |
| NEW UNTIL | 2026-09-12 |
| MAIN | IMAGE 02 — whole-product view selected during visual review |
| GALLERY ORDER | 02 → 01 → 03 → 04 |
| LIVE MEDIA | `assets/pink-mall/products/PM-038/` — 4 × 576×721 WebP, native aspect |
| MEDIA TIER | OFFICIAL — drmartens.com |
| VARIANT | VARIANT_CONFIDENCE_PASS |
| VALIDATION | 73/73 production + 73/73 standalone, GitHub Actions run 33246543092 |

The supplied `40754` is retained as an evidenced alias/base style; the exact
manufacturer item number is `40754650`. All four official frames are below the
1000 px preference and were published at their native 576×721 size — no
upscaling and no manufactured canvas.

## PM-039 — published

| | |
|---|---|
| PUBLISHED | 2026-08-29 |
| BRAND / MODEL | Polo Ralph Lauren / Cotton Drawstring Shoulder Bag |
| MANUFACTURER ITEM | 4AR165 |
| CATEGORY | BAGS, `subcategory: null` |
| PUBLIC COLOUR | Green |
| COMPOSITION | 100% Cotton |
| PRICE | €44, no SALE |
| INVENTORY MODE | availability |
| SIZES | ONE SIZE — available |
| NEW UNTIL | 2026-09-12 |
| MAIN | IMAGE 01 |
| GALLERY ORDER | 01 → 02 → 03 → 04 |
| LIVE MEDIA | `assets/pink-mall/products/PM-039/` — 4 × 700×1050 WebP, native aspect |
| MEDIA TIER | TRUSTED_RETAILER — answear.com |
| VARIANT | VARIANT_CONFIDENCE_PASS |
| VALIDATION | 73/73 production + 73/73 standalone, GitHub Actions run 33246543092 |

IMAGE 05 was excluded because it contains a mannequin/person-like silhouette.
The source's child-series classification is internal only; it is absent from
the public name, description, tags, alt text and category, and the browser
regression verifies that no child/junior marker is rendered.
