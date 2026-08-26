# PINK MALL — Pepe Jeans PGS30614 approval preview (PM-029 proposed)

**STATUS: APPROVED AND PUBLISHED as PM-029 on 2026-08-26.**

Published exactly as recorded below — MAIN IMAGE 01, gallery 01 → 02 → 04 → 05
→ 03, €34, size 39 only, material omitted, official manufacturer media. Live
media is at `assets/pink-mall/products/PM-029/`; the file-to-image mapping is in
that directory's `README.md`.

**Original approval state:**
`VARIANT_CONFIDENCE_PASS` · `SIZE_CONFIRMED` · **media tier: OFFICIAL**

Zero-seed onboarding: human input was the original four fields only —
`Pepe Jeans / PGS30614 / €34 / 39`.

---

## 1. Product

| | |
|---|---|
| Brand | Pepe Jeans |
| Model | Ben Band |
| Manufacturer item | PGS30614 |
| Full article code | PGS30614327 (base + colour `327`) |
| Retailer reference | PPJ-PGS30614-327 |
| Mall ID | **PM-029 — allocated at publication, 2026-08-26** |
| Category | SHOES > Sneakers |
| Public colour | Pink / Black |
| Manufacturer colour name | `factory pink` |
| Material | **omitted** — see §7 |
| Price | €34 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| NEW | until 2026-09-09 (14 days from publication) |
| Delivery | global — `4–7 работни дни` |

A pink canvas low-top on a chunky cream vulcanised cupsole, with a navy toe
bumper and heel panel and the multicoloured PEPE JEANS wordmark across the
midsole. Every attribute above is visible in the acquired frames.

## 2. Identity — how it was established

Two independent provenance classes agree, and neither was taken on assertion.

| Transport | Source | Establishes | Level |
|---|---|---|---|
| `CLAUDE_RESEARCH` | pepejeans.com `it_it` / `pl_pl` / `pt_pt` | `PGS30614` + colour `327`; colour name `factory pink` | B |
| `CLAUDE_RESEARCH` | deporvillage.net | public model **Ben Band**; variant Pink / Black | B |
| `CLAUDE_RESEARCH` | esdemarca.com | corroborates SKU + model + colour | C |
| `REVIEWER_VERIFIED` | deporvillage.net (live read) | exact reference `PPJ-PGS30614-327`; full 32–40 size ladder | A |
| `DIRECT_FETCH` | **images.pepejeans.com** | the media itself, hash-verified | **A** |

Every acquired filename carries the full article code
`PGS30614_327_<view>_FL.jpg`, so each asset is self-evidencing on its own URL.

## 3. Sizes

```text
39 — available
```

The manufacturer's exact scale for this article is **32–40**, independently
evidenced, and it **contains 39** → `SIZE_CONFIRMED`.

`inventoryMode: 'availability'`. Only the user-supplied size is published. No
sold-out ladder is asserted, no quantities, no scarcity. **Retailer stock state
is not PINK MALL availability** — the size run above is a scale, not a stock
report.

## 4. Media — 5 images, official manufacturer tier

| Position | Image | View | Size |
|---|---|---|---|
| MAIN | 01 | lateral side profile, single shoe | 1920×2652 |
| `gallery[0]` | 02 | pair, top-down | 1600×2210 |
| `gallery[1]` | 04 | three-quarter, platform and midsole logo | 1200×1658 |
| `gallery[2]` | 05 | heel and back quarter | 1200×1658 |
| `gallery[3]` | 03 | outsole | 1600×2210 |

| Image | SHA-256 |
|---|---|
| 01 | `08748a215fc7f5b4df43c1740dcb4f84ee186be870ce9fc9fa37186c5789ae52` |
| 02 | `49e789f52fabac596f06dadfc4fac5197b07423fa93c063f99e60ed16ab30644` |
| 03 | `36895cb0a3aaee9d75726bd4dc405ea757fdcabcb267eda3e49406fd7eb5095f` |
| 04 | `632ed69341838688fecd259bd4e40a2591e7f594f95a49f60051b9cc235bb8d8` |
| 05 | `be25d57b61bc5675bc838751353275bc9978827a93338760ca47c183b926fabc` |

MAIN is IMAGE 01 and this matches the automation's proposal — on review it is
also the right choice: the whole shoe, lateral, highest resolution, legible at
thumbnail size. Outsole sits last, as on PM-025, PM-026 and PM-028.

Detected backdrop `#DDDCD8` → `media.surface`. `media.fit: 'contain'`. Native
aspect ratio, no canvas manufactured. Product-only, no people.

Contact sheet: `docs/pink-mall/media-acquisition/PGS30614/CONTACT_SHEET.webp`
Provenance: `docs/pink-mall/media-acquisition/PGS30614/result.json`

## 5. Provenance

**PRIMARY MEDIA TIER: OFFICIAL manufacturer media** —
`images.pepejeans.com`, Pepe Jeans' own Salesforce Commerce Cloud CDN.

This is the second product in the catalogue with manufacturer-tier imagery
(PM-026 was the first). PM-025, PM-027 and PM-028 all rest on retailer media.

Resolution was raised by rewriting only the CDN's own sizing query
(`?sw=950` → `?sw=1600` / `?sw=1200`); the asset path is never touched, so the
bytes are the same photograph at a larger size. No upscaling.

Reviewer-verified Deporvillage media was acquired and validated cleanly at
1600×2000, but is **not** used: the source hierarchy puts manufacturer media
above retailer media, and the selector now enforces that. Its evidence still
did decisive work on identity and the size scale.

## 6. Alt text — Bulgarian

```text
imageAlt      — Розови Pepe Jeans Ben Band кецове от канава с тъмносин кант и кремава платформа, страничен изглед
galleryAlt[0] — Розови Pepe Jeans Ben Band кецове, изглед отгоре с връзки и език
galleryAlt[1] — Розови Pepe Jeans Ben Band кецове, детайл на платформата и цветното лого
galleryAlt[2] — Розови Pepe Jeans Ben Band кецове, изглед от петата
galleryAlt[3] — Външна подметка на Pepe Jeans Ben Band кецове, изглед отдолу
```

No child-series markers. No comfort, fit, performance, material or care claims.

## 7. Material — deliberately omitted

Retailers describe the upper as a cotton twill and repeat a "made with at least
70% sustainable cotton" line. That is a sustainability marketing claim, not a
composition, and the official product page was never read by this pipeline —
all three locale URLs return `404`.

So `composition` is omitted and the PDP renders no material row, consistent
with PM-026, PM-027 and PM-028.

## 8. Mall copy and tags

```text
Pepe Jeans Ben Band в розово — канава с тъмносин кант, кремава вулканизирана
платформа и цветно лого отстрани. Retro sneaker силует с повече характер.
```

```text
pepe jeans, ben band, sneakers, shoes, pink, navy, canvas, platform, cupsole, retro
```

Internal only, never rendered as public specs.

## 9. Warnings — one, non-blocking

1. **View 03 of the manufacturer's own set is absent.** Views 01, 02, 04, 05
   and 06 were recovered; the 03 asset sits behind an opaque `dw<hash>` path
   segment that cannot be derived from the others, and it will not be guessed.
   Five images is a complete gallery by this project's standard.

The manufacturer classifies this line as a junior series item. Internal only;
it appears nowhere above, in the tags, in the alt text or in the copy.

## 10. Published product object

```js
{
    id: 'PM-029',
    brand: 'Pepe Jeans',
    manufacturerItemNo: 'PGS30614',
    name: 'Ben Band',
    slug: 'pepe-jeans-ben-band-pink',
    category: 'shoes', subcategory: 'sneakers',
    color: 'Pink / Black',
    /* composition omitted — not established by this pipeline */
    priceEUR: 34,
    oldPriceEUR: null,
    description: 'Pepe Jeans Ben Band в розово — канава с тъмносин кант, '
               + 'кремава вулканизирана платформа и цветно лого отстрани. '
               + 'Retro sneaker силует с повече характер.',
    selectedBy: null,
    tags: ['pepe jeans','ben band','sneakers','shoes','pink','navy',
           'canvas','platform','cupsole','retro'],
    featured: false, campaign: null, related: ['PM-027','PM-028'],
    isNew: false, newUntil: '2026-09-09',
    inventoryMode: 'availability',
    availability: { '39':'available' },
    media: {
        image:      'assets/pink-mall/products/PM-029/PM-029-main.webp',
        imageAlt:   'Розови Pepe Jeans Ben Band кецове от канава с тъмносин кант и кремава платформа, страничен изглед',
        gallery:   ['assets/pink-mall/products/PM-029/PM-029-02.webp',
                    'assets/pink-mall/products/PM-029/PM-029-03.webp',
                    'assets/pink-mall/products/PM-029/PM-029-04.webp',
                    'assets/pink-mall/products/PM-029/PM-029-05.webp'],
        galleryAlt:['Розови Pepe Jeans Ben Band кецове, изглед отгоре с връзки и език',
                    'Розови Pepe Jeans Ben Band кецове, детайл на платформата и цветното лого',
                    'Розови Pepe Jeans Ben Band кецове, изглед от петата',
                    'Външна подметка на Pepe Jeans Ben Band кецове, изглед отдолу'],
        fit: 'contain', surface: '#DDDCD8',
        ph: 'shoes', field: 'blush'
    }
}
```

## 11. Published summary

```text
STATUS:   PUBLISHED as PM-029 on 2026-08-26
VARIANT:  VARIANT_CONFIDENCE_PASS
BRAND:    Pepe Jeans
MODEL:    Ben Band
ITEM:     PGS30614  (full article PGS30614327)
MALL ID:  PM-029
CATEGORY: SHOES > Sneakers
COLOR:    Pink / Black   (manufacturer: factory pink)
MATERIAL: omitted — not established by this pipeline
PRICE:    €34
SIZES:    39 — available.  Exact scale 32–40 evidenced and contains 39.
NEW:      YES until 2026-09-09
MAIN:     IMAGE 01
GALLERY ORDER: 01 (MAIN) → 02 → 04 → 05 → 03
MEDIA TIER: OFFICIAL — images.pepejeans.com, manufacturer CDN
WARNINGS: manufacturer view 03 not recovered
```

**Approved and published.** Nothing here awaits a decision.

## 12. Publication verification — 2026-08-26

| Check | Result |
|---|---|
| Canonical `PINKMALL.html` SHA-256 | `851534665fa9c02cc3d1096343f2c8e87d4f429ba716bc014f105f49db8b71ac` |
| PM-029 in `PINK_MALL_PRODUCTS` | exactly once; catalogue PM-001…PM-029, 29 unique ids |
| Production regression | **PASS** — 206/206 across PM-025…PM-029 |
| Portable review regression | **PASS** — 208/208, standalone alone in an empty directory |
| Live media | 5 WebP at native size; no upscale, no canvas |
| Size truth | 39 only, not sold out, no quantities; exact 32–40 scale proven |
| Material | no `Състав` row on the PDP |
| Junior classification | absent from all rendered text |
| Supplier names | absent from all rendered text |
| PM-025 … PM-028 | unchanged — ladders, sold-out sets, media dimensions, spec rows |
