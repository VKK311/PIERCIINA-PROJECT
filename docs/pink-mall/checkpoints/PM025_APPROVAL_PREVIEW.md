# PINK MALL — PM-025 approval preview

**STATUS: APPROVED AND PUBLISHED — 2026-08-25**

Published as PM-025 on 2026-08-25 with the media package below. This file is now
the historical record of what was approved; live state is in `PROJECT_STATE.md`.


---

## 1. Product

| | |
|---|---|
| Brand | adidas |
| Model | VL Court Bold Shoes |
| Manufacturer item | JQ4556 |
| Mall ID | PM-025 (proposed) |
| Category | SHOES > Sneakers |
| Color | Pink / Silver / Gold |
| Material | Leather / Textile / Rubber |
| Price | €54 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| NEW | active for 14 days from first approved publication; `newUntil` not yet assigned |
| Delivery | global — `4–7 работни дни` |

Manufacturer colour of record is `Clear Pink / Silver Metallic / Gold Metallic`,
simplified for the Mall per the skill's naming rules. No fourth public colour is
claimed.

## 2. Sizes — resolved

```text
36       — available
36 2/3   — ИЗЧЕРПАН
37 1/3   — available
38       — ИЗЧЕРПАН
38 2/3   — available
39 1/3   — ИЗЧЕРПАН
40       — available
```

`inventoryMode: 'availability'`. No quantities are known and none are invented,
so there is no `ПОСЛЕДНА БРОЙКА` and no product-level scarcity claim. Size
labels are canonical strings; `37 1/3` is never normalised to `37`.

## 3. Media — approved set and order

MAIN is **IMAGE 01**. Gallery order **01 → 04 → 02 → 03**, unchanged.

| Position | Source image | Role | Size | Future path |
|---|---|---|---|---|
| MAIN | IMAGE 01 | lateral side profile, full product | 1880×1880 | `assets/pink-mall/products/PM-025/PM-025-main.webp` |
| `gallery[0]` | IMAGE 04 | three-quarter front angle, full product | 1880×1880 | `assets/pink-mall/products/PM-025/PM-025-02.webp` |
| `gallery[1]` | IMAGE 02 | top-down — lacing, tongue, collar | 1880×1880 | `assets/pink-mall/products/PM-025/PM-025-03.webp` |
| `gallery[2]` | IMAGE 03 | outsole, gum rubber tread | 1880×1880 | `assets/pink-mall/products/PM-025/PM-025-04.webp` |

Full-product frames lead; the technical outsole view is last. All four are
exact-SKU, exact-variant, product-only, no people. Rejects: 0. Duplicates: 0.

| Image | SHA-256 |
|---|---|
| 01 | `cd35da4bc75864eb854c1735d69ef07c2fbf1a4d6335e975c3fef6be67fad7f4` |
| 04 | `d7cb5f1b4a8eb723e937bf765a574e7c45c9f88340f6e65c07d8928f3b328f94` |
| 02 | `0a0270dc1c9f63a5526c16db855c8d99c52774ebd80092476cd88505ad5bc96d` |
| 03 | `656cd37b2912f1a35136cc9c1dfa2685f9a9e3cba71ebf776052bba645be1bfb` |

Archive: `docs/pink-mall/approval-media/PM-025/`
Provenance: `docs/pink-mall/media-acquisition/JQ4556/result.json`

Acquired automatically from `assets.adidas.com` — no manual download, rename or
upload. Seeded at `w_500`, upgraded to `w_1880` by rewriting only the CDN
transform segment, each upgrade verified perceptually against its 500px anchor.
No AI upscaling, no generative edits.

`assets/` paths are **proposed future** locations. Those files do not exist and
will not until publication.

## 4. Alt text — canonical schema

Bulgarian, matching the storefront language. Carried as `media.imageAlt` and
`media.galleryAlt[]`, and rendered by the engine.

```text
imageAlt      — Розови adidas VL Court Bold Shoes със сребърни ленти и gum платформа, страничен изглед
galleryAlt[0] — Розови adidas VL Court Bold Shoes, изглед под ъгъл отпред
galleryAlt[1] — Розови adidas VL Court Bold Shoes, изглед отгоре с връзки и език
galleryAlt[2] — Външна подметка от gum гума на adidas VL Court Bold Shoes, изглед отдолу
```

No `kids` / `junior` / `youth` / `J`. No comfort, fit, performance or care claims.

## 5. Mall copy

```text
adidas VL Court Bold в розово, със сребърни метални ленти, златно лого и дебела
gum подметка. Court silhouette с повече attitude — full PINK MALL energy.
```

## 6. Internal search tags — never rendered as public specs

```text
adidas, VL Court Bold, sneakers, shoes, pink, silver, gold, leather,
skate-inspired, platform, gum sole, court
```

## 7. Staged product object — NOT PUBLISHED

```js
{
    id: 'PM-025',
    brand: 'adidas',
    manufacturerItemNo: 'JQ4556',
    name: 'VL Court Bold Shoes',
    slug: 'adidas-vl-court-bold-shoes',
    category: 'shoes', subcategory: 'sneakers',
    color: 'Pink / Silver / Gold',
    composition: 'Leather / Textile / Rubber',
    priceEUR: 54,
    oldPriceEUR: null,
    description: 'adidas VL Court Bold в розово, със сребърни метални ленти, златно '
               + 'лого и дебела gum подметка. Court silhouette с повече attitude — '
               + 'full PINK MALL energy.',
    selectedBy: null,
    tags: ['adidas','VL Court Bold','sneakers','shoes','pink','silver','gold',
           'leather','skate-inspired','platform','gum sole','court'],
    featured: false,
    campaign: null,
    related: [],

    /* NEW switches on at first approved publication, for 14 days.
       newUntil is deliberately NOT assigned yet. */
    isNew: false,
    newUntil: null,

    inventoryMode: 'availability',
    availability: {
        '36':     'available',
        '36 2/3': 'soldout',
        '37 1/3': 'available',
        '38':     'soldout',
        '38 2/3': 'available',
        '39 1/3': 'soldout',
        '40':     'available'
    },

    media: {
        image:      'assets/pink-mall/products/PM-025/PM-025-main.webp',
        imageAlt:   'Розови adidas VL Court Bold Shoes със сребърни ленти и gum платформа, страничен изглед',
        gallery:   ['assets/pink-mall/products/PM-025/PM-025-02.webp',
                    'assets/pink-mall/products/PM-025/PM-025-03.webp',
                    'assets/pink-mall/products/PM-025/PM-025-04.webp'],
        galleryAlt:['Розови adidas VL Court Bold Shoes, изглед под ъгъл отпред',
                    'Розови adidas VL Court Bold Shoes, изглед отгоре с връзки и език',
                    'Външна подметка от gum гума на adidas VL Court Bold Shoes, изглед отдолу'],
        ph: 'shoes', field: 'blush'
    }
}
```

## 8. Warnings

**None.** The 500×500 resolution warning is withdrawn: the 1880×1880 set fully
replaces it and is adequate for card, PDP and zoom.

## 9. Approval preview

```text
STATUS:
READY FOR APPROVAL

BRAND:
adidas

MODEL:
VL Court Bold Shoes

MANUFACTURER ITEM:
JQ4556

MALL ID:
PM-025 (proposed)

CATEGORY:
SHOES > Sneakers

COLOR:
Pink / Silver / Gold

MATERIAL:
Leather / Textile / Rubber

PRICE:
€54

SIZES:
36 — available
36 2/3 — ИЗЧЕРПАН
37 1/3 — available
38 — ИЗЧЕРПАН
38 2/3 — available
39 1/3 — ИЗЧЕРПАН
40 — available

NEW:
YES for 14 days after first approved publication

SHORT MALL COPY:
adidas VL Court Bold в розово, със сребърни метални ленти, златно лого и дебела
gum подметка. Court silhouette с повече attitude — full PINK MALL energy.

PHOTO MATERIAL:
docs/pink-mall/approval-media/PM-025/PINK_MALL_JQ4556_CONTACT_SHEET.webp
4 images, 1880×1880, official adidas media, automatically acquired

MAIN:
IMAGE 01

GALLERY ORDER:
IMAGE 01 (MAIN) → IMAGE 04 → IMAGE 02 → IMAGE 03

ALT TEXT:
MAIN       — Розови adidas VL Court Bold Shoes със сребърни ленти и gum платформа, страничен изглед
gallery[0] — Розови adidas VL Court Bold Shoes, изглед под ъгъл отпред
gallery[1] — Розови adidas VL Court Bold Shoes, изглед отгоре с връзки и език
gallery[2] — Външна подметка от gum гума на adidas VL Court Bold Shoes, изглед отдолу

SOURCE STATUS:
EXACT OFFICIAL JQ4556

WARNINGS:
none
```

**Approved and published 2026-08-25.** No instruction outstanding.
