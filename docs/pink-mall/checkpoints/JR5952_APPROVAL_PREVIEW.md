# PINK MALL — adidas JR5952 approval package (published as PM-028)

**STATUS: APPROVED AND PUBLISHED as PM-028 on 2026-08-25.**

This package is the approved record. It was published exactly as written below —
MAIN IMAGE 02, gallery order 02 → 01 → 05 → 04 → 03, material omitted, sizes
36 / 37 1/3 / 38 / 38 2/3 all available. Live media is at
`assets/pink-mall/products/PM-028/`; the file-to-image mapping is in that
directory's `README.md`.

**Original approval state:**
`VARIANT_CONFIDENCE_PASS` — exact-SKU evidence on every image, and all three
official colour terms (`pink`, `green`, `gold`) detected in frame.

**Mall ID: PM-028 — allocated at publication, 2026-08-25.**

---

## 1. Product

| | |
|---|---|
| Brand | adidas |
| Model | Gazelle Bold Shoes |
| Manufacturer item | JR5952 |
| Manufacturer colour | Almost Pink / Court Green / Gold Metallic |
| Public colour | Pink / Green / Gold |
| Category | SHOES > Sneakers |
| Material | omitted — not established by this pipeline |
| Price | €59 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| NEW | until 2026-09-08 (14 days from publication) |
| Delivery | global — `4–7 работни дни` |

Pale pink upper, green three-stripes, gold `GAZELLE` lettering, gum platform
sole. All four attributes are visible across the acquired frames.

## 2. A correction, recorded

An earlier pass rejected this media as *"a white-and-green Gazelle Bold, not the
pink JR5952"*. **That rejection was wrong.** `Almost Pink` is a very pale tint
and `Court Green` is part of the official colourway, so the imagery matched the
official variant precisely. Correct media was discarded on a subjective read of
colour.

The confidence gate now reaches the conclusion from evidence rather than
impression, and the case is a permanent regression fixture.

## 3. Sizes — user-supplied only

```text
36     — available
37 1/3 — available
38     — available
38 2/3 — available
```

All are exact values on adidas's fractional EU scale — nothing normalised,
nothing blocked. The exact-model size run was not proven, so no sold-out sizes
are asserted. `inventoryMode: 'availability'`, no quantities, no scarcity.

## 4. Media — 5 images

MAIN is **IMAGE 02**, not the automation's proposal. The pipeline proposes MAIN
by filename order and offered IMAGE 01; on review, IMAGE 02 is the stronger card
image — both shoes complete, three-quarter front, silhouette and stripe
placement legible at thumbnail size. IMAGE 04 is a cropped detail and is placed
late for that reason.

| Position | Image | View | Size |
|---|---|---|---|
| MAIN | 02 | pair, three-quarter front | 560×746 |
| `gallery[0]` | 01 | pair, lateral and heel-on | 560×746 |
| `gallery[1]` | 05 | pair, top-down | 560×746 |
| `gallery[2]` | 04 | upper detail — stripes and platform | 560×746 |
| `gallery[3]` | 03 | outsole, gum rubber | 560×746 |

| Image | SHA-256 |
|---|---|
| 01 | `0cab3a34b5f9a5b50f8149f95b3e29ba…` |
| 02 | `c5df8c2eaa320046a6510603be2e4498…` |
| 03 | `0e964d27e5d27cf88aa70cdb0f9a6ece…` |
| 04 | `d011be115e80fc4b317861c44459bca5…` |
| 05 | `d4e22ea87c8ed1de787de54058f9f930…` |

Detected backdrop `#FFFFFF` → `media.surface`. `media.fit: 'contain'`. Native
aspect ratio; no aspect-ratio canvas manufactured. Product-only, no people.

Contact sheet: `docs/pink-mall/media-acquisition/JR5952/CONTACT_SHEET.webp`
Provenance: `docs/pink-mall/media-acquisition/JR5952/result.json`

## 5. Provenance

**PRIMARY MEDIA TIER: trusted retailer fallback (tier 5) — not official
manufacturer media.**

| Route | Result |
|---|---|
| `DIRECT_OFFICIAL_PAGE` adidas ×5 (pages + both API regions) | `403` / timeout |
| `OFFICIAL_CDN_PROBE` assets.adidas.com | not addressable — adidas hashes its asset paths |
| `TRUSTED_RETAILER_SEARCH` eobuwie, modivo, shooos | OK — SKU evidenced in page URL |

Marketplaces carrying the same SKU (Allegro, ERLI) were **excluded** as primary
media per the source hierarchy.

## 6. Alt text — Bulgarian

```text
imageAlt      — Бледорозови adidas Gazelle Bold маратонки със зелени ленти и gum платформа, изглед под ъгъл отпред
galleryAlt[0] — Бледорозови adidas Gazelle Bold маратонки, страничен изглед и изглед от петата
galleryAlt[1] — Бледорозови adidas Gazelle Bold маратонки, изглед отгоре
galleryAlt[2] — Бледорозови adidas Gazelle Bold маратонки, детайл на зелените ленти и платформата
galleryAlt[3] — Външна подметка от gum гума на adidas Gazelle Bold маратонки, изглед отдолу
```

No child-series markers. No comfort, fit, performance, material or care claims.

## 7. Mall copy and tags

```text
adidas Gazelle Bold в бледо розово със зелени ленти и златно лого, върху дебела
gum платформа. Retro terrace силует — вдигнат и малко нахален.
```

```text
adidas, gazelle bold, sneakers, shoes, pink, green, gold, platform, gum sole, retro, terrace
```

Internal only, never rendered as public specs.

## 8. Warnings — three, none blocking

1. **Resolution.** All five are 560×746 — longest edge 746 px, below the
   1000 px preference. Acceptable for approval and card preview; higher
   resolution preferred before launch. Do not upscale.
2. **Media source is trusted-retailer fallback**, not official manufacturer
   media.
3. **No official image anchor exists.** adidas hashes its CDN paths and every
   adidas route returns 403, so variant confidence rests on exact-SKU evidence
   plus agreement with the official colour text. That is materially weaker than
   PM-026, whose media came from the manufacturer's own CDN.

The manufacturer classifies this as a juniors series item. Internal only; it
appears nowhere above.

## 9. Published summary

```text
STATUS:   PUBLISHED as PM-028 on 2026-08-25
VARIANT:  VARIANT_CONFIDENCE_PASS
BRAND:    adidas
MODEL:    Gazelle Bold Shoes
ITEM:     JR5952
MALL ID:  PM-028
CATEGORY: SHOES > Sneakers
COLOR:    Pink / Green / Gold  (manufacturer: Almost Pink / Court Green / Gold Metallic)
MATERIAL: omitted — not established by this pipeline
PRICE:    €59
SIZES:    36, 37 1/3, 38, 38 2/3 — all available (no sold-out states asserted)
NEW:      YES until 2026-09-08
MAIN:     IMAGE 02  (automation proposed 01; changed on visual review)
GALLERY ORDER: 02 (MAIN) → 01 → 05 → 04 → 03
MEDIA TIER: trusted retailer fallback — no official image anchor
WARNINGS: 560×746 resolution; retailer-tier source; no official anchor
```

**Approved and published.** Nothing here awaits a decision.

## 10. Published product object

```js
{
    id: 'PM-028',
    brand: 'adidas',
    manufacturerItemNo: 'JR5952',
    name: 'Gazelle Bold Shoes',
    slug: 'adidas-gazelle-bold-pink-green-gold',
    category: 'shoes', subcategory: 'sneakers',
    color: 'Pink / Green / Gold',
    /* composition omitted — not established by this pipeline */
    priceEUR: 59,
    oldPriceEUR: null,
    selectedBy: null,
    isNew: false, newUntil: '2026-09-08',
    inventoryMode: 'availability',
    availability: { '36':'available', '37 1/3':'available',
                    '38':'available', '38 2/3':'available' },
    media: {
        image:    'assets/pink-mall/products/PM-028/PM-028-main.webp',   /* IMAGE 02 */
        gallery: ['assets/pink-mall/products/PM-028/PM-028-02.webp',     /* IMAGE 01 */
                  'assets/pink-mall/products/PM-028/PM-028-03.webp',     /* IMAGE 05 */
                  'assets/pink-mall/products/PM-028/PM-028-04.webp',     /* IMAGE 04 */
                  'assets/pink-mall/products/PM-028/PM-028-05.webp'],    /* IMAGE 03 */
        fit: 'contain', surface: '#FFFFFF',
        ph: 'shoes', field: 'blush'
    },
    related: ['PM-025','PM-027']
}
```

`related` is the one field the approval package did not specify: PM-025 is the
other adidas platform sneaker and PM-027 the other pink platform sneaker, so
both were used.

## 11. Publication verification — 2026-08-25

| Check | Result |
|---|---|
| Canonical `PINKMALL.html` SHA-256 | `7f088253c01c94c04100e111746b4bcc2153e4d68a3344790a37c3af9b07d2a5` |
| PM-028 in `PINK_MALL_PRODUCTS` | exactly once; catalogue PM-001…PM-028, 28 unique ids |
| Production regression | **PASS** — 168/168, covering PM-025 / PM-026 / PM-027 / PM-028 |
| Portable review regression | **PASS** — 170/170, standalone file alone in an empty directory |
| Live media | 5 WebP at native 560×746; no upscale, no canvas, portrait frames unpadded |
| Size truth | 36, 37 1/3, 38, 38 2/3 in numeric order, none sold out, no quantities |
| Material | no `Състав` row on the PDP |
| Juniors classification | absent from all rendered text |
| MAIN override | IMAGE 02 renders as `media.image`; IMAGE 04 renders at `gallery[2]` |
| PM-025 / PM-026 / PM-027 | unchanged — ladders, sold-out sets, media dimensions and spec rows all verified |

No engine change was required: `sizeSortKey()` already handled the fractional
adidas scale (`37 1/3`, `38 2/3`); the decimal branch added for PM-027 is
untouched by this product.
