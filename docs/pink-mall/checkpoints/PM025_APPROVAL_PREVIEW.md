# PINK MALL — PM-025 APPROVAL PREVIEW

**STATUS: READY FOR APPROVAL**
Staging only. PM-025 is **not** published, the calibrated HTML is **not** modified,
nothing is committed.

---

## 1. SOURCE GATE

| Check | Result |
|---|---|
| SHA-256 of attached calibrated HTML | `dc7050ba22862b4f4f1a07cae0365e6f648dde9d726475223279fd839962a2f0` — exact match | 
| Catalog IDs | PM-001 → PM-024, contiguous, 24 total |
| PM-025 in catalog | Absent (0 occurrences) |
| JQ4556 in public catalog | Absent |
| Next proposed ID | PM-025 |

**Note:** the string `JQ4556` occurs once in the file, at line 13531, inside
`__calibrationFixture` (`id: 'FIXTURE-AVAIL'`) — the non-public availability-mode test
object added during calibration. It is not in `PINK_MALL_PRODUCTS`, is not rendered,
searched, filtered or counted. **It must be deleted at publication time.**

---

## 2. MEDIA VALIDATION

Four images supplied locally. All four inspected visually, individually.

| # | View | Exact SKU | Exact variant | Product-only | Unique | Verdict |
|---|---|---|---|---|---|---|
| 01 | Lateral side, left profile | ✅ | ✅ | ✅ | ✅ | **ACCEPT — PROPOSED MAIN** |
| 02 | Top-down, lacing / tongue / collar | ✅ | ✅ | ✅ | ✅ | ACCEPT |
| 03 | Outsole, gum rubber tread | ✅ | ✅ | ✅ | ✅ | ACCEPT |
| 04 | Three-quarter front angle | ✅ | ✅ | ✅ | ✅ | ACCEPT |

**Rejects: 0. Duplicates: 0.**

Uniqueness was checked byte-wise (4 distinct SHA-256) and perceptually
(16×16 dHash, minimum pairwise Hamming distance 48/256 — well clear of duplicate range).

Identity markers confirmed in-frame: pink upper, **silver metallic 3-stripes**,
**gold adidas wordmark badge** on the quarter panel, **gum platform midsole** with
embossed `adidas`, periwinkle heel tab. Consistent across all four frames.

| File | Format | Size | Bytes | SHA-256 (first 16) |
|---|---|---|---|---|
| `JQ4556-01-original.jpg` | JPEG RGB | 500×500 | 9 164 | `3940078ed620b96e` |
| `JQ4556-02-original.jpg` | JPEG RGB | 500×500 | 9 790 | `a4b11cc7d6075598` |
| `JQ4556-03-original.jpg` | JPEG RGB | 500×500 | 10 290 | `7109e8007d878498` |
| `JQ4556-04-original.jpg` | JPEG RGB | 500×500 | 10 242 | `36c7c06e99cebbe8` |

Technical operations applied: **JPEG → WebP re-encode only**, quality 90, at the
original 500×500. No resize, no crop, no retouch, no generative change.

---

## 3. STAGING TREE

```text
.pink-mall-staging/JQ4556/
    PINK_MALL_JQ4556_CONTACT_SHEET.webp     (copy, see note)
    source/
        JQ4556-01-original.jpg              (untouched)
        JQ4556-02-original.jpg              (untouched)
        JQ4556-03-original.jpg              (untouched)
        JQ4556-04-original.jpg              (untouched)
    preview/
        JQ4556-01.webp
        JQ4556-02.webp
        JQ4556-03.webp
        JQ4556-04.webp
        PINK_MALL_JQ4556_CONTACT_SHEET.webp
```

`assets/pink-mall/products/PM-025/` was **not** created, as instructed.

**Path note:** section F places the contact sheet under `preview/`, section M names it at
`.pink-mall-staging/JQ4556/`. The two disagree, so the identical file exists at both paths.

---

## 4. CONTACT SHEET

`.pink-mall-staging/JQ4556/preview/PINK_MALL_JQ4556_CONTACT_SHEET.webp`
1136 × 1720, 143 KB, 2×2 grid.

Every tile is a real supplied asset — no placeholder tiles. Each tile carries: image
number, view/role, provenance, and a quality note. IMAGE 01 is marked `PROPOSED MAIN`
with a pink frame and badge.

---

## 5. PROPOSED MAIN

**IMAGE 01 — lateral side view.**

Rationale: it is the only frame that shows the complete silhouette unobstructed — upper,
stripe placement, gold badge and the full gum platform stack all read at card size.
It is the frame that survives being scaled down to a grid thumbnail. IMAGE 04 is the
runner-up; IMAGE 03 (outsole) is deliberately last, being a technical view.

---

## 6. ALT TEXT

Written in Bulgarian, matching the language of the rest of the storefront, so Bulgarian
screen readers announce it correctly. (Section H's example was English; if you want
English alt text instead, say so and it is a one-line change.)

```text
01 — Розови adidas VL Court Bold Shoes със сребърни ленти и gum платформа, страничен изглед
02 — Розови adidas VL Court Bold Shoes, изглед отгоре с връзки и език
03 — Външна подметка от gum гума на adidas VL Court Bold Shoes, изглед отдолу
04 — Розови adidas VL Court Bold Shoes, изглед под ъгъл отпред
```

No `kids` / `junior` / `youth` / `J` anywhere. No comfort, fit, performance or care claims.

---

## 7. SHORT MALL COPY

```text
Розово adidas VL Court Bold върху дебела gum платформа, със сребърни метални ленти
и златно лого. Court силует, вдигнат нагоре — full pink mall energy.
```

Every concrete noun is visually confirmed or comes from the locked facts. Nothing is
claimed about comfort, fit, performance, exclusivity or care.

---

## 8. INTERNAL SEARCH TAGS (never rendered as public specs)

```text
adidas, VL Court Bold, sneakers, shoes, pink, silver, gold, leather,
skate-inspired, platform, gum sole, court
```

No `kids`, `junior`, `boys`, `girls`, `youth`.

---

## 9. STAGED PRODUCT OBJECT — NOT PUBLISHED

```js
{
    id: 'PM-025',
    brand: 'adidas',
    manufacturerItemNo: 'JQ4556',
    name: 'VL Court Bold Shoes',
    slug: 'adidas-vl-court-bold-pink',
    category: 'shoes', subcategory: 'sneakers',
    color: 'Pink / Silver / Gold',
    composition: 'Leather / Textile / Rubber',
    priceEUR: 54,
    oldPriceEUR: null,
    description: 'Розово adidas VL Court Bold върху дебела gum платформа, със сребърни '
               + 'метални ленти и златно лого. Court силует, вдигнат нагоре — full pink mall energy.',
    selectedBy: null,
    tags: ['adidas','VL Court Bold','sneakers','shoes','pink','silver','gold',
           'leather','skate-inspired','platform','gum sole','court'],
    featured: false,
    campaign: null,
    related: [],

    /* NEW: to be switched on at first approved publication, for 14 days.
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
        image:   'assets/pink-mall/products/PM-025/PM-025-01.webp',
        gallery: ['assets/pink-mall/products/PM-025/PM-025-02.webp',
                  'assets/pink-mall/products/PM-025/PM-025-03.webp',
                  'assets/pink-mall/products/PM-025/PM-025-04.webp'],
        alt: ['Розови adidas VL Court Bold Shoes със сребърни ленти и gum платформа, страничен изглед',
              'Розови adidas VL Court Bold Shoes, изглед отгоре с връзки и език',
              'Външна подметка от gum гума на adidas VL Court Bold Shoes, изглед отдолу',
              'Розови adidas VL Court Bold Shoes, изглед под ъгъл отпред'],
        ph: 'shoes', field: 'blush'
    }
}
```

Media paths are **proposed future** locations. Those files do not exist yet.

---

## 10. OPEN POINTS FOR YOUR DECISION

Three things surfaced during validation. None blocks approval; all need a decision before
publication.

1. **Per-image alt is not consumable by the current engine.** `galleryOf()` returns bare
   strings, and both `mediaHTML()` and `detailMediaHTML()` synthesise alt text as
   `p.name + ' — снимка N от M'`. The staged `media.alt` array is therefore inert until a
   small engine change reads it. That change is an HTML edit, which this turn forbids.

2. **Image resolution is 500×500.** These are the `w_500` web derivatives. Fine for grid
   cards and a modest PDP, but they will visibly soften on a large desktop PDP or under
   zoom. Higher-resolution originals would be worth requesting before launch.

3. **A periwinkle/purple heel tab is clearly visible** on images 01, 02 and 04. The locked
   colour string is `Pink / Silver / Gold`, which I have kept exactly as specified — but
   the product has a fourth visible accent colour that the string does not mention.

---

## 11. APPROVAL PREVIEW

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
Розово adidas VL Court Bold върху дебела gum платформа, със сребърни метални ленти
и златно лого. Court силует, вдигнат нагоре — full pink mall energy.

PHOTO MATERIAL:
.pink-mall-staging/JQ4556/preview/PINK_MALL_JQ4556_CONTACT_SHEET.webp

MAIN:
IMAGE 01

ALT TEXT:
01 — Розови adidas VL Court Bold Shoes със сребърни ленти и gum платформа, страничен изглед
02 — Розови adidas VL Court Bold Shoes, изглед отгоре с връзки и език
03 — Външна подметка от gum гума на adidas VL Court Bold Shoes, изглед отдолу
04 — Розови adidas VL Court Bold Shoes, изглед под ъгъл отпред

SOURCE STATUS:
EXACT OFFICIAL JQ4556

WARNINGS:
1. Per-image alt not consumable by current engine (needs a small change at publication).
2. Images are 500x500 web derivatives — soft at large PDP zoom.
3. Visible periwinkle heel tab not covered by the locked colour string.
```

---

## 12. NOT DONE, DELIBERATELY

- PM-025 not published, not added to `PINK_MALL_PRODUCTS`.
- Calibrated HTML not modified — still `dc7050ba…`.
- `assets/pink-mall/products/PM-025/` not created.
- No `newUntil` date assigned.
- Final Release Audit not started.
- Nothing committed, pushed, merged, or opened as a pull request.

**Awaiting explicit instruction:** `APPROVE` / `CHANGE MAIN TO IMAGE 0X` /
`REMOVE IMAGE 0X` / `REORDER` / `CHANGE COPY` / `REJECT`.
