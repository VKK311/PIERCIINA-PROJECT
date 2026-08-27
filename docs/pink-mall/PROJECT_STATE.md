# PINK MALL — project state

Updated: PM-031 publication.
Status: **PM-001…PM-031 PUBLISHED.**

This file records the real state. Trust it over any summary, and verify the
canonical build by hash before treating it as canonical.

## Canonical

| | |
|---|---|
| CANONICAL BRANCH | `claude/pink-mall-development` |
| CANONICAL WEBSITE | `PINKMALL.html` |
| CANONICAL WEBSITE SHA-256 | `0d939a9bfc12328acf759704b07ae85febbb9ea0cfea33c92f44cd04ca958c03` |
| CANONICAL WEBSITE BYTES | 2561908 |

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
| PUBLIC CATALOG | PM-001 … PM-031 |
| NEXT ID | PM-032 |
| JQ4556 | **PUBLISHED as PM-025** on 2026-08-25 |
| GC515KI | **PUBLISHED as PM-026** on 2026-08-25 |
| A08745C | **PUBLISHED as PM-027** on 2026-08-25 |
| JR5952 | **PUBLISHED as PM-028** on 2026-08-25 |
| PGS30614 | **PUBLISHED as PM-029** on 2026-08-26 |
| 398855 | **PUBLISHED as PM-030** on 2026-08-26 |
| HC.RBGLOW01 | **PUBLISHED as PM-031** on 2026-08-27 |

## Media acquisition automation

| | |
|---|---|
| AUTOMATION | PASS — `tools/media_acquisition/`, `.github/workflows/media-acquisition.yml` |
| SELF-TEST | PASS — `python tools/media_acquisition/selftest.py`, 94/94 guards |
| PUBLICATION REGRESSION | PASS — `tools/regression/product_regression.js`, 78/78 on both builds |
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
| SHA-256 | `af627ed471913c03ace643347138890bbb7216cd548f1621d78d43e691cfd805` |
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

## Scotch & Soda Celest 27733247 — DISCOVERY_TRANSPORT_BLOCKED

| | |
|---|---|
| STATE | **not acquired, not staged, not published** |
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

## Next step

Next Mall ID is **PM-032**, unallocated until a product is actually published.
Nothing is awaiting approval: the approval queue is empty.

Seven products now come from the automated pipeline — PM-025 through PM-031.
Four have manufacturer-official media (PM-026, PM-029, PM-030, PM-031); PM-025,
PM-027 and PM-028 rest on trusted-retailer evidence. Upgrading those three to
official imagery remains open if an official route ever opens.
