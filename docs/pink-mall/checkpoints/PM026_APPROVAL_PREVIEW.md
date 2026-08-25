# PINK MALL — PM-026 approval preview

**STATUS: READY FOR APPROVAL — NOT PUBLISHED**

First **zero-seed** onboarding: the user supplied brand, SKU, price and sizes
and nothing else — no product URL, no image URLs, no files. Identity, media
discovery and binary acquisition were all automatic.

---

## 1. Product

| | |
|---|---|
| Brand | New Balance |
| Model | 515 V1 |
| Manufacturer item | GC515KI |
| Mall ID | PM-026 (proposed) |
| Category | SHOES > Sneakers |
| Manufacturer colour | Rose Sugar |
| Public colour | Pink |
| Material | *not confirmed* — see warnings |
| Price | €54 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| NEW | 14 days from first approved publication; `newUntil` not assigned yet |
| Delivery | global — `4–7 работни дни` |

The user wrote the brand as "New Balance PINK". Read as brand **New Balance**
with *pink* describing the colourway, since New Balance is the manufacturer and
`GC515KI` resolves to its 515 V1 in Rose Sugar. Correct me at approval if a
sub-label was meant.

`GC515KD` is a **different** pink 515. Every accepted asset carries `gc515ki`
in its own URL, so that neighbouring colourway could not slip in.

## 2. Sizes

User-supplied availability: **37, 38, 40** — all exact whole values on the
official EU scale, so nothing was normalised and nothing is blocked.

```text
36     — ИЗЧЕРПАН
36.5   — ИЗЧЕРПАН
37     — available
37.5   — ИЗЧЕРПАН
38     — available
38.5   — ИЗЧЕРПАН
39     — ИЗЧЕРПАН
40     — available
```

`inventoryMode: 'availability'`. No quantities supplied, so none are invented:
no `ПОСЛЕДНА БРОЙКА`, no product-level scarcity.

## 3. Media — 5 unique images, acquired automatically

MAIN is **IMAGE 01**. Proposed gallery order puts full-product views first and
the technical outsole last.

| Position | Source image | View | Size |
|---|---|---|---|
| MAIN | IMAGE 01 | lateral side profile (outside) | 1600×1600 |
| `gallery[0]` | IMAGE 04 | three-quarter front angle | 1600×1600 |
| `gallery[1]` | IMAGE 02 | medial side profile (inside) | 1600×1600 |
| `gallery[2]` | IMAGE 03 | top-down — lacing, tongue, collar | 1600×1600 |
| `gallery[3]` | IMAGE 05 | outsole, non-marking rubber | 1600×1600 |

| Image | SHA-256 |
|---|---|
| 01 | `7e6b3ca5e42a2a8a2a4a3138…` |
| 02 | `725a211faa3f24c13e18fda0…` |
| 03 | `906e2a9022c80d3419b86ce2…` |
| 04 | `d2ad6f90bb526f5569d90dac…` |
| 05 | `b1cf2b686f12c2063334ee67…` |

All from `nb.scene7.com`, New Balance's official media CDN, at native 1600×1600.
Detected backdrop `#F1F1F1`, which becomes `media.surface`. Native aspect ratio
throughout — no canvas manufactured; the storefront fits with `media.fit`.

Contact sheet: `docs/pink-mall/media-acquisition/GC515KI/CONTACT_SHEET.webp`
Full provenance: `docs/pink-mall/media-acquisition/GC515KI/result.json`

Identity confirmed visually on every frame: pale pink mesh-and-suede-look upper,
vivid pink `N`, vivid pink heel patch, white midsole, vivid pink non-marking
outsole, cream laces. IMAGE 03 shows the `515` tongue label. Product-only, no
people, 0 rejects, 0 duplicates.

## 4. Alt text — Bulgarian, canonical schema

```text
imageAlt      — Розови New Balance 515 маратонки с наситено розово N и бяла подметка, страничен изглед
galleryAlt[0] — Розови New Balance 515 маратонки, изглед под ъгъл отпред
galleryAlt[1] — Розови New Balance 515 маратонки, изглед от вътрешната страна
galleryAlt[2] — Розови New Balance 515 маратонки, изглед отгоре с връзки и език
galleryAlt[3] — Външна подметка на New Balance 515 маратонки, изглед отдолу
```

No `kids` / `junior` / `youth` / `girls`. No comfort, fit, performance or care claims.

## 5. Mall copy

```text
New Balance 515 в бледо розово с наситено розово N и бяла подметка. Retro runner
силует — clean, но определено не тих.
```

## 6. Internal search tags — never rendered as public specs

```text
new balance, 515, sneakers, shoes, pink, rose sugar, retro, runner, classic
```

## 7. Staged product object — NOT PUBLISHED

```js
{
    id: 'PM-026',
    brand: 'New Balance',
    manufacturerItemNo: 'GC515KI',
    name: '515 V1',
    slug: 'new-balance-515-v1-pink',
    category: 'shoes', subcategory: 'sneakers',
    color: 'Pink',
    /* composition intentionally omitted — not confirmed from an official source */
    priceEUR: 54,
    oldPriceEUR: null,
    description: 'New Balance 515 в бледо розово с наситено розово N и бяла подметка. '
               + 'Retro runner силует — clean, но определено не тих.',
    selectedBy: null,
    tags: ['new balance','515','sneakers','shoes','pink','rose sugar',
           'retro','runner','classic'],
    featured: false,
    campaign: null,
    related: ['PM-025'],

    isNew: false,
    newUntil: null,          /* set at first approved publication + 14 days */

    inventoryMode: 'availability',
    availability: {
        '36':   'soldout',
        '36.5': 'soldout',
        '37':   'available',
        '37.5': 'soldout',
        '38':   'available',
        '38.5': 'soldout',
        '39':   'soldout',
        '40':   'available'
    },

    media: {
        image:      'assets/pink-mall/products/PM-026/PM-026-main.webp',
        imageAlt:   'Розови New Balance 515 маратонки с наситено розово N и бяла подметка, страничен изглед',
        gallery:   ['assets/pink-mall/products/PM-026/PM-026-02.webp',
                    'assets/pink-mall/products/PM-026/PM-026-03.webp',
                    'assets/pink-mall/products/PM-026/PM-026-04.webp',
                    'assets/pink-mall/products/PM-026/PM-026-05.webp'],
        galleryAlt:['Розови New Balance 515 маратонки, изглед под ъгъл отпред',
                    'Розови New Balance 515 маратонки, изглед от вътрешната страна',
                    'Розови New Balance 515 маратонки, изглед отгоре с връзки и език',
                    'Външна подметка на New Balance 515 маратонки, изглед отдолу'],
        fit: 'contain', surface: '#F1F1F1',
        ph: 'shoes', field: 'blush'
    }
}
```

## 8. Warnings — two, neither blocking

**1. Material not confirmed.** Every New Balance product page returned `403` to
the runner, so composition could not be read from an official source. A trusted
retailer carrying the exact SKU describes a mesh and synthetic upper, EVA
midsole and rubber outsole. That is retailer-derived, not official, so the field
is **omitted** rather than published on weaker evidence. Say the word and I will
add `Mesh / Synthetic / Rubber` on that basis.

**2. Sold-out ladder is size-chart derived.** The user's three available sizes
are certain. The surrounding in-range sizes shown as ИЗЧЕРПАН come from the
New Balance grade-school EU size chart rather than the official product page,
for the same `403` reason. `39.5` is deliberately **not** shown, as it was not
evidenced. Confirm or correct the ladder at approval.

Not a warning, but worth stating: the manufacturer classifies this as a
grade-school series item. That is internal only and appears nowhere in the
public record above.

## 9. Approval preview

```text
STATUS:
READY FOR APPROVAL

BRAND:
New Balance

MODEL:
515 V1

MANUFACTURER ITEM:
GC515KI

MALL ID:
PM-026 (proposed)

CATEGORY:
SHOES > Sneakers

COLOR:
Pink   (manufacturer: Rose Sugar)

MATERIAL:
not confirmed

PRICE:
€54

SIZES:
36 — ИЗЧЕРПАН
36.5 — ИЗЧЕРПАН
37 — available
37.5 — ИЗЧЕРПАН
38 — available
38.5 — ИЗЧЕРПАН
39 — ИЗЧЕРПАН
40 — available

NEW:
YES for 14 days after first approved publication

SHORT MALL COPY:
New Balance 515 в бледо розово с наситено розово N и бяла подметка. Retro runner
силует — clean, но определено не тих.

PHOTO MATERIAL:
docs/pink-mall/media-acquisition/GC515KI/CONTACT_SHEET.webp
5 images, 1600×1600, official New Balance media, automatically acquired

MAIN:
IMAGE 01

GALLERY ORDER:
IMAGE 01 (MAIN) → IMAGE 04 → IMAGE 02 → IMAGE 03 → IMAGE 05

SOURCE STATUS:
EXACT OFFICIAL GC515KI — official New Balance CDN

WARNINGS:
1. Material not confirmed from an official source; field omitted.
2. Sold-out ladder derived from the size chart, not the product page.
```

**Awaiting explicit instruction:** `APPROVE` / `CHANGE MAIN TO IMAGE 0X` /
`REMOVE IMAGE 0X` / `REORDER` / `CHANGE COPY` / `ADD MATERIAL` / `REJECT`.
