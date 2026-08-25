# PINK MALL — PM-025 approval preview

**STATUS: READY FOR APPROVAL — NOT PUBLISHED**

Reconciled during the structure-cleanup + pre-publish-hardening task.
PM-025 is not in `PINK_MALL_PRODUCTS`, and `JQ4556` appears nowhere in the
canonical `PINKMALL.html`.

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

Manufacturer color of record is `Clear Pink / Silver Metallic / Gold Metallic`,
simplified for the Mall to `Pink / Silver / Gold` per the skill's naming rules.
No fourth public color is claimed.

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

MAIN is **IMAGE 01**.

| Position | Source image | Role | Future path |
|---|---|---|---|
| MAIN | IMAGE 01 | lateral side view, full product | `assets/pink-mall/products/PM-025/PM-025-main.webp` |
| gallery[0] | IMAGE 04 | three-quarter front angle | `assets/pink-mall/products/PM-025/PM-025-02.webp` |
| gallery[1] | IMAGE 02 | top-down, lacing and collar | `assets/pink-mall/products/PM-025/PM-025-03.webp` |
| gallery[2] | IMAGE 03 | outsole, gum rubber tread | `assets/pink-mall/products/PM-025/PM-025-04.webp` |

Full-product frames lead; the technical outsole view is last. All four are
exact-SKU, exact-variant, product-only, with no people. Rejects: 0.
Duplicates: 0.

Archived originals and the contact sheet:
`docs/pink-mall/approval-media/PM-025/`

Those paths are **proposed future** locations. The files do not exist under
`assets/` and will not until publication.

## 4. Alt text — canonical schema

Bulgarian, matching the storefront language. Carried as `media.imageAlt` and
`media.galleryAlt[]`, the schema defined in the skill's product contract, and
now actually rendered by the engine.

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

**One, non-blocking.** Source media is 500×500 web derivatives. Acceptable for
approval and card preview; higher-resolution exact official duplicates are
preferred before launch and full PDP display. Do not AI-upscale. Replacement
bytes may be swapped in only after visual identity verification, preserving
image number, order and MAIN.

The per-image alt gap flagged in the previous revision is **resolved** — the
engine now renders authored `imageAlt` / `galleryAlt[n]`, proven by runtime
test with distinct Bulgarian strings across forward, backward and
thumbnail-jump navigation.

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

MAIN:
IMAGE 01

GALLERY ORDER:
IMAGE 01 (MAIN) → IMAGE 04 → IMAGE 02 → IMAGE 03

SOURCE STATUS:
EXACT OFFICIAL JQ4556

WARNINGS:
500×500 source media; higher-resolution exact duplicates preferred before launch.
```

**Awaiting explicit instruction:** `APPROVE` / `CHANGE MAIN TO IMAGE 0X` /
`REMOVE IMAGE 0X` / `REORDER` / `CHANGE COPY` / `REJECT`.
