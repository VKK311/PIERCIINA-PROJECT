# PINK MALL — A08745C approval preview (PM-027 proposed)

**STATUS: READY FOR APPROVAL — NOT PUBLISHED**
`VARIANT_CONFIDENCE_PASS` — exact-SKU evidence on every image, official colour
term `pink` detected in frame.

Zero-seed onboarding: human input was the original four fields only.

---

## 1. Product

| | |
|---|---|
| Brand | Converse |
| Model | Chuck Taylor All Star Move |
| Manufacturer item | A08745C |
| Mall ID | PM-027 (proposed — allocated only on publish) |
| Category | SHOES > Sneakers |
| Public colour | Pink |
| Material | **omitted** — see §7 |
| Price | €49 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| NEW | 14 days from first approved publication |
| Delivery | global — `4–7 работни дни` |

A platform high-top in pink: white All Star patch, white eyelets, white
platform midsole. Every attribute above is visible in the acquired frames.

## 2. Sizes — user-supplied only

```text
36   — available
37.5 — available
38   — available
39   — available
```

`inventoryMode: 'availability'`. The exact-model size run was not proven, so
under the ladder-evidence rule no sold-out sizes are asserted. No quantities,
no scarcity.

## 3. Media — 5 images

| Position | Image | View | Size |
|---|---|---|---|
| MAIN | 01 | lateral side profile, single shoe | 1500×1500 |
| `gallery[0]` | 05 | pair, three-quarter front | 670×670 |
| `gallery[1]` | 02 | pair, angled | 670×670 |
| `gallery[2]` | 04 | medial side profile, single shoe | 670×670 |
| `gallery[3]` | 03 | pair, flat and top-down | 670×670 |

| Image | SHA-256 |
|---|---|
| 01 | `231e637a1117092ba8a436e8d723c33964063100f1fce008827ae37dc41067f2` |
| 02 | `a5be621bd2b3abd96e7e3d47190fd22d7228c78467a32de516bc46b46be7dca3` |
| 03 | `91628dbf5104a03d8974836d6f378f7126af34148c7ccc589afe38d749b2eba1` |
| 04 | `fd5a1a2f274ba1670374cf0005624dad53f71eb03e72917cdfb1d4f4ba5f8c04` |
| 05 | `8b96c65f238d57f0dd8ff4d727341668c2bb803875c375dd1cc3499c111975d3` |

Detected backdrop `#FFFFFF` → `media.surface`. `media.fit: 'contain'`. Native
aspect ratio — no aspect-ratio canvas was manufactured. Product-only, no people.

Contact sheet: `docs/pink-mall/media-acquisition/A08745C/CONTACT_SHEET.webp`
Provenance: `docs/pink-mall/media-acquisition/A08745C/result.json`

## 4. Provenance

**PRIMARY MEDIA TIER: trusted retailer fallback (tier 5) — not official
manufacturer media.**

| Route | Result |
|---|---|
| `DIRECT_OFFICIAL_PAGE` converse.com ×4 | `403` |
| `SEARCH_INDEX_OFFICIAL` converse.com.tr category pages | loaded, but carried no A08745C link to follow |
| `INDEXED_OUTBOUND_MEDIA` one-hop link following | no official target reached |
| `TRUSTED_RETAILER_SEARCH` **spx.com.tr** | **OK — SKU evidenced** |
| `TRUSTED_RETAILER_SEARCH` superstep.com.tr | OK — SKU evidenced |

No official image anchor exists for this SKU.

## 5. Alt text — Bulgarian

```text
imageAlt      — Розови Converse Chuck Taylor All Star Move високи кецове на платформа, страничен изглед
galleryAlt[0] — Розови Converse Chuck Taylor All Star Move, изглед под ъгъл отпред
galleryAlt[1] — Розови Converse Chuck Taylor All Star Move, чифт под ъгъл
galleryAlt[2] — Розови Converse Chuck Taylor All Star Move, изглед от вътрешната страна
galleryAlt[3] — Розови Converse Chuck Taylor All Star Move, изглед отгоре
```

No child-series markers. No comfort, fit, performance, material or care claims.

## 6. Mall copy and tags

```text
Converse Chuck Taylor All Star Move в розово, на платформа. Класическият
силует, но вдигнат — high-top energy без излишна драма.
```

```text
converse, chuck taylor, all star, move, sneakers, shoes, pink, platform, high-top
```

Internal only, never rendered as public specs.

## 7. Material — deliberately omitted

`100% TEKSTIL` appears on the official regional Converse page, but **this
pipeline never reached that page** — the material fact entered through reviewer
evidence, not through the automation's own discovery.

For a pure zero-seed operational test, the customer-facing record must contain
only what the pipeline itself established. So `composition` is **omitted** from
the staged product, and the PDP simply renders no material row. The fact is
retained here as provenance and can be added later on official evidence.

## 8. Warnings — two, neither blocking

1. **Resolution.** Four gallery images are 670×670, below the 1000 px
   preference; only MAIN is 1500×1500. Acceptable for approval and card
   preview; higher-resolution official copies preferred before launch. Do not
   upscale.
2. **Media source is trusted-retailer fallback, not official manufacturer
   media.** Every Converse official route failed. Images are exact-SKU and
   visually verified, but this is tier-5 evidence with no official anchor.

Material is not a warning: it is simply absent.

The manufacturer classifies this line as a youth series item. Internal only; it
appears nowhere above.

## 9. Staged product object — NOT PUBLISHED

```js
{
    id: 'PM-027',
    brand: 'Converse',
    manufacturerItemNo: 'A08745C',
    name: 'Chuck Taylor All Star Move',
    slug: 'converse-chuck-taylor-all-star-move-pink',
    category: 'shoes', subcategory: 'sneakers',
    color: 'Pink',
    /* composition omitted — not established by this pipeline */
    priceEUR: 49,
    oldPriceEUR: null,
    description: 'Converse Chuck Taylor All Star Move в розово, на платформа. '
               + 'Класическият силует, но вдигнат — high-top energy без излишна драма.',
    selectedBy: null,
    tags: ['converse','chuck taylor','all star','move','sneakers','shoes',
           'pink','platform','high-top'],
    featured: false, campaign: null, related: ['PM-025','PM-026'],
    isNew: false, newUntil: null,
    inventoryMode: 'availability',
    availability: { '36':'available', '37.5':'available',
                    '38':'available', '39':'available' },
    media: {
        image:      'assets/pink-mall/products/PM-027/PM-027-main.webp',
        imageAlt:   'Розови Converse Chuck Taylor All Star Move високи кецове на платформа, страничен изглед',
        gallery:   ['assets/pink-mall/products/PM-027/PM-027-02.webp',
                    'assets/pink-mall/products/PM-027/PM-027-03.webp',
                    'assets/pink-mall/products/PM-027/PM-027-04.webp',
                    'assets/pink-mall/products/PM-027/PM-027-05.webp'],
        galleryAlt:['Розови Converse Chuck Taylor All Star Move, изглед под ъгъл отпред',
                    'Розови Converse Chuck Taylor All Star Move, чифт под ъгъл',
                    'Розови Converse Chuck Taylor All Star Move, изглед от вътрешната страна',
                    'Розови Converse Chuck Taylor All Star Move, изглед отгоре'],
        fit: 'contain', surface: '#FFFFFF',
        ph: 'shoes', field: 'blush'
    }
}
```

## 10. Approval preview

```text
STATUS:   READY FOR APPROVAL
VARIANT:  VARIANT_CONFIDENCE_PASS
BRAND:    Converse
MODEL:    Chuck Taylor All Star Move
ITEM:     A08745C
MALL ID:  PM-027 (proposed)
CATEGORY: SHOES > Sneakers
COLOR:    Pink
MATERIAL: omitted — not established by this pipeline
PRICE:    €49
SIZES:    36, 37.5, 38, 39 — all available (no sold-out states asserted)
NEW:      YES for 14 days after first approved publication
MAIN:     IMAGE 01
GALLERY ORDER: 01 (MAIN) → 05 → 02 → 04 → 03
MEDIA TIER: trusted retailer fallback — no official image anchor
WARNINGS: four gallery images at 670×670; retailer-tier media source
```

**Awaiting:** `APPROVE` / `CHANGE MAIN TO IMAGE 0X` / `REORDER` /
`REMOVE IMAGE 0X` / `CHANGE COPY` / `REJECT`.
