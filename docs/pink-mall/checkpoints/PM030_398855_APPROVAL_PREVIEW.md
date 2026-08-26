# PINK MALL — Puma 398855 approval preview (PM-030 proposed)

**STATUS: READY FOR APPROVAL — NOT PUBLISHED**
`VARIANT_CONFIDENCE_PASS` · **media tier: OFFICIAL** · transparent cut-outs

Zero-seed onboarding. Human input was four fields —
`Puma / 398855 / €44 / 37.5, 38, 38.5, 39` — plus one correction of my
mis-targeting, described in §2.

---

## 1. Product

| | |
|---|---|
| Brand | Puma |
| Model | Palermo Moda |
| Manufacturer item | 398855 |
| Colour suffix | **-11** |
| Mall ID | PM-030 (proposed — allocated only on publish) |
| Category | SHOES > Sneakers |
| Public colour | Pink / Aqua |
| Manufacturer colour name | `Poised Pink / Aqua` |
| Material | **omitted** — see §7 |
| Price | €44 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| NEW | 14 days from first approved publication |
| Delivery | global — `4–7 работни дни` |

A dusty pink suede terrace low-top with a light aqua formstripe, a small gold
Puma wordmark and a gum platform sole. Every attribute above is visible in the
acquired frames.

## 2. Identity — and the correction that got here

The first attempt targeted the wrong article. `401489` Club II Era was
onboarded to the point of acquisition before visual review showed `401489-04`
to be an **aquatic-primary** shoe — turquoise with a pink formstripe — not a
pink shoe. That manifest was withdrawn.

`398855` then presented its own version of the same trap. The colourway was
named (`poised pink / aqua`, from Zalando's own URL slug) but the Puma colour
suffix was evidenced nowhere reachable, and this article ships **eleven**
colourways. A first pass selected five views of `398855-01` — Puma White /
Puma Black — because the official product page serves the default colourway and
its images outranked everything else.

So a reconnaissance sweep fetched one hero view per colour code, `01`–`14`, and
put all eleven on a contact sheet. `-11` is the pink one. The decoys were
visible in the same sheet and are worth naming, because any of them would have
satisfied a check that verified only the article number:

| Code | Colourway |
|---|---|
| 01 | white, black formstripe |
| 03 | mint, mauve formstripe |
| 07 | coral, pink formstripe |
| 10 | cream, **pale pink** formstripe |
| **11** | **pink, aqua formstripe** ← this product |

Identity is now pinned twice over: both the article number **and** the colour
suffix appear in every acquired asset path.

## 3. Sizes — user-supplied only

```text
37.5 — available
38   — available
38.5 — available
39   — available
```

`inventoryMode: 'availability'`. No source declared an exact size scale for this
article, so under the ladder-evidence rule the supplied labels stand as
availability truth and **no sold-out ladder is asserted**. No quantities, no
scarcity. Decimal half-sizes are ordered numerically and the labels are never
rewritten.

## 4. Media — 5 images, official manufacturer tier

| Position | Image | View | Size |
|---|---|---|---|
| MAIN | 01 | lateral side profile, single shoe | 2000×2000 |
| `gallery[0]` | 05 | pair, three-quarter | 2000×2000 |
| `gallery[1]` | 03 | medial side profile | 2000×2000 |
| `gallery[2]` | 04 | heel and platform detail | 2000×2000 |
| `gallery[3]` | 02 | top-down and outsole | 2000×2000 |

| Image | SHA-256 |
|---|---|
| 01 | `9bcd9f343aa9469f31601ab9664240cbe7d1ef2c6da52fa8f50eaceeed7bc7c3` |
| 02 | `07ea5ddb917150518fe387e75794ba8361cf7b0ce7bfe365fa2186f462c5ab08` |
| 03 | `97edeb05484454dbdfef833977fb4bcdaf0ba6abc1016d80f3e8c0f9caeb3cf0` |
| 04 | `120bebe751c510bd29856336d9614306277753f55eda19227ef3f7d7e048b5f0` |
| 05 | `1b488470747571cc0a49581084215639fc29bcb39c0f49cc2336cbf53e570582` |

MAIN is IMAGE 01, matching the automation's proposal and correct on review:
the whole shoe, lateral, legible at thumbnail size. The combined top-down and
outsole frame sits last, as the outsole does on PM-025 through PM-029.

**These are transparent cut-outs, not photographs on a backdrop.** `media.surface`
is therefore **omitted** and the storefront's own neutral field (`#EDEFF0`)
shows through. That is deliberate: the acquisition pipeline originally reported
a backdrop of `#47704C`, a dark green produced by flattening a transparent PNG,
which would have painted a green field behind the product. `media.fit: 'contain'`.
Native 2000×2000, no canvas manufactured. Product-only, no people.

Contact sheet: `docs/pink-mall/media-acquisition/398855/CONTACT_SHEET.webp`
Provenance: `docs/pink-mall/media-acquisition/398855/result.json`

## 5. Provenance

**PRIMARY MEDIA TIER: OFFICIAL manufacturer media** — `images.puma.com`.

Third product in the catalogue with manufacturer-tier imagery, after PM-026 and
PM-029. PM-025, PM-027 and PM-028 rest on trusted-retailer media.

Discovery was by **CDN probe**, not by archive lookup. A probe is a lead, never
evidence: it becomes a candidate only if it downloads, decodes and carries the
exact article number in its own path. Here both the article number and the
colour suffix are in every path, so a probe could reach neither another product
nor another colourway.

## 6. Alt text — Bulgarian

```text
imageAlt      — Розови велурени Puma Palermo Moda кецове с аква лента и gum платформа, страничен изглед
galleryAlt[0] — Розови Puma Palermo Moda кецове, чифт под ъгъл
galleryAlt[1] — Розови Puma Palermo Moda кецове, изглед от вътрешната страна
galleryAlt[2] — Розови Puma Palermo Moda кецове, детайл на петата и платформата
galleryAlt[3] — Розови Puma Palermo Moda кецове, изглед отгоре и външна подметка
```

No child-series markers. No comfort, fit, performance or care claims.

## 7. Material — deliberately omitted

The official page describes a suede upper with suede and synthetic overlays,
mesh collar lining and a rubber midsole and outsole. That reached this project
through a **search summary of the page**, not through the pipeline reading the
page itself, so it is provenance rather than an established fact.

`composition` is omitted and the PDP renders no material row, consistent with
PM-026 through PM-029.

## 8. Mall copy and tags

```text
Puma Palermo Moda в розов велур с аква лента и златно лого, върху gum платформа.
Terrace класика с малко повече сладост.
```

```text
puma, palermo, palermo moda, sneakers, shoes, pink, aqua, suede, platform, gum sole, terrace, retro
```

Internal only, never rendered as public specs.

## 9. Warnings — one, non-blocking

1. **The public colour is Pink / Aqua, not simply Pink.** The upper is pink and
   the formstripe is a clear light aqua. Stated honestly rather than flattened
   to "pink" because the store is pink-themed.

The manufacturer classifies this line as a big-kids / junior series item, and
the supplied model name carried "Jr". Internal only; neither appears in the
name, colour, copy, tags, alt text or any public field.

## 10. Staged product object — NOT PUBLISHED

```js
{
    id: 'PM-030',
    brand: 'Puma',
    manufacturerItemNo: '398855',
    name: 'Palermo Moda',
    slug: 'puma-palermo-moda-pink-aqua',
    category: 'shoes', subcategory: 'sneakers',
    color: 'Pink / Aqua',
    /* composition omitted — not established by this pipeline */
    priceEUR: 44,
    oldPriceEUR: null,
    description: 'Puma Palermo Moda в розов велур с аква лента и златно лого, '
               + 'върху gum платформа. Terrace класика с малко повече сладост.',
    selectedBy: null,
    tags: ['puma','palermo','palermo moda','sneakers','shoes','pink','aqua',
           'suede','platform','gum sole','terrace','retro'],
    featured: false, campaign: null, related: ['PM-029','PM-027'],
    isNew: false, newUntil: null,
    inventoryMode: 'availability',
    availability: { '37.5':'available', '38':'available',
                    '38.5':'available', '39':'available' },
    media: {
        image:      'assets/pink-mall/products/PM-030/PM-030-main.webp',
        imageAlt:   'Розови велурени Puma Palermo Moda кецове с аква лента и gum платформа, страничен изглед',
        gallery:   ['assets/pink-mall/products/PM-030/PM-030-02.webp',
                    'assets/pink-mall/products/PM-030/PM-030-03.webp',
                    'assets/pink-mall/products/PM-030/PM-030-04.webp',
                    'assets/pink-mall/products/PM-030/PM-030-05.webp'],
        galleryAlt:['Розови Puma Palermo Moda кецове, чифт под ъгъл',
                    'Розови Puma Palermo Moda кецове, изглед от вътрешната страна',
                    'Розови Puma Palermo Moda кецове, детайл на петата и платформата',
                    'Розови Puma Palermo Moda кецове, изглед отгоре и външна подметка'],
        /* surface omitted deliberately: transparent cut-outs, so the mall's
           own neutral field shows through rather than an invented colour */
        fit: 'contain',
        ph: 'shoes', field: 'blush'
    }
}
```

## 11. Approval preview

```text
STATUS:   READY FOR APPROVAL
VARIANT:  VARIANT_CONFIDENCE_PASS
BRAND:    Puma
MODEL:    Palermo Moda
ITEM:     398855   (colour suffix -11)
MALL ID:  PM-030 (proposed)
CATEGORY: SHOES > Sneakers
COLOR:    Pink / Aqua   (manufacturer: Poised Pink / Aqua)
MATERIAL: omitted — not established by this pipeline
PRICE:    €44
SIZES:    37.5, 38, 38.5, 39 — all available (no sold-out states asserted)
NEW:      YES for 14 days after first approved publication
MAIN:     IMAGE 01
GALLERY ORDER: 01 (MAIN) → 05 → 03 → 04 → 02
MEDIA TIER: OFFICIAL — images.puma.com, manufacturer CDN
MEDIA FORM: transparent cut-outs; media.surface omitted by design
WARNINGS: public colour is Pink / Aqua, not simply Pink
```

**Awaiting:** `APPROVE` / `CHANGE MAIN TO IMAGE 0X` / `REORDER` /
`REMOVE IMAGE 0X` / `CHANGE COPY` / `REJECT`.
