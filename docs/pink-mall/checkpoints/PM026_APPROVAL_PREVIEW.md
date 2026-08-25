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
| Size ladder | user-supplied sizes only — exact-model run NOT VERIFIED |
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

## 2. Sizes — user-supplied only

```text
37 — available
38 — available
40 — available
```

`inventoryMode: 'availability'`. No quantities supplied, so none are invented:
no `ПОСЛЕДНА БРОЙКА`, no product-level scarcity.

**No sold-out sizes are shown, and that is deliberate.** A previous revision of
this package listed 36, 36.5, 37.5, 38.5 and 39 as `ИЗЧЕРПАН`, derived from the
New Balance grade-school size chart. That chart maps EU to UK to cm — it says
nothing about which sizes **GC515KI** was actually offered in. Showing those
states would have claimed inventory history this SKU may never have had.

A final automated attempt to prove the exact-model size run was made across
three independent networks and failed:

| Route | Result |
|---|---|
| Official NB pages and search, from the runner | `403` on all four |
| Official NB hosts, from the execution container | `000` — egress blocked |
| Exact-SKU official structured data, via search | not found |
| Another official NB regional source for this SKU | not found |

`EXACT MODEL SIZE SCALE: NOT VERIFIED`, so the truthful fallback applies: the
ladder carries only the three sizes you supplied. If you can confirm the real
size run, I will expand the ladder and mark the rest sold out.

Strict size matching is untouched: had you supplied a size that conflicted with
a proven exact-model scale, this would still be `BLOCKED`.

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
    /* Only the user-supplied sizes. The exact-model size run could not be
       proven, so no sold-out states are asserted. */
    availability: {
        '37': 'available',
        '38': 'available',
        '40': 'available'
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

## 8. Warnings — one, non-blocking

**Material not confirmed.** Every New Balance product page returned `403` to the
runner, so composition could not be read from an official source. A trusted
retailer carrying the exact SKU describes a mesh and synthetic upper, EVA
midsole and rubber outsole — retailer-derived, not official, so the field is
**omitted** rather than published on weaker evidence. Say `ADD MATERIAL` and I
will include `Mesh / Synthetic / Rubber` on that basis.

The size-ladder warning from the previous revision is **resolved**, not carried
forward: the unsupported sold-out states were removed rather than annotated.
Unsupported sold-out states: **0**.

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
37 — available
38 — available
40 — available
(exact-model size run NOT VERIFIED; no sold-out states asserted)

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
```

**Awaiting explicit instruction:** `APPROVE` / `CHANGE MAIN TO IMAGE 0X` /
`REMOVE IMAGE 0X` / `REORDER` / `CHANGE COPY` / `ADD MATERIAL` / `REJECT`.
