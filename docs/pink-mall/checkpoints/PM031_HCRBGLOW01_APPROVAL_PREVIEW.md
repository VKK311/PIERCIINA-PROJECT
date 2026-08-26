# PINK MALL — Colors of California HC.RBGLOW01 approval preview (PM-031 proposed)

**STATUS: READY FOR APPROVAL — NOT PUBLISHED**
`VARIANT_CONFIDENCE_PASS` · **media tier: OFFICIAL**

Zero-seed onboarding: human input was the four fields only —
`Colors of California / HC.RBGLOW01 / €64 / 36, 37, 38, 39, 40`.

**First non-sneaker product in the catalogue**, and the first to use the new
`SHOES > Boots` subcategory you approved.

---

## 1. Product

| | |
|---|---|
| Brand | Colors of California |
| Model | Glossy rainboot |
| Manufacturer item | HC.RBGLOW01 |
| Colour code | **FUX** |
| Season code in assets | F24 |
| Mall ID | PM-031 (proposed — allocated only on publish) |
| Category | SHOES > **Boots** |
| Public colour | Pink |
| Manufacturer colour name | `Fuxia` |
| Material | **omitted** — see §7 |
| Price | €64 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| NEW | 14 days from first approved publication |
| Delivery | global — `4–7 работни дни` |

A glossy fuchsia rubber Chelsea-style ankle rain boot: elastic side gores, a
pull tab at the heel, and a chunky lugged outsole. Every attribute above is
visible in the acquired frames.

## 2. Product type — the reason this one is different

`HC.RBGLOW01` is a **rubber rain boot**, not a sneaker. The `RB` prefix runs
consistently through this brand's rainboot line — `rbnew03` is
`chelsie-rainboot`, `rbnew012` is `chelsea-rainboot`, `rb0041` is
`rainboot-with-neoprene-collar` — and the official product name is literally
"Glossy rainboot".

Every product this pipeline had onboarded before this one was a sneaker, and
`SHOES > Sneakers` was the only calibrated subcategory. Creating a new one
required your approval, which you gave: **`SHOES > Boots`**.

Checked before relying on it: the storefront consumes `subcategory` in exactly
one place — the search haystack — so a new value is purely additive and needs
no engine change. The `SHOES` category's Bulgarian search terms already include
`ботуши`.

## 3. Identity — and the colour the site chose

| Transport | Source | Establishes | Level |
|---|---|---|---|
| `CLAUDE_RESEARCH` | colorsofcalifornia.it | official model name **Glossy rainboot**; the site's URL grammar | B |
| `DIRECT_OFFICIAL_PAGE` | the product page itself | the media, and the colour | **A** |
| `CLAUDE_RESEARCH` | eBay listing | corroborates a pink colourway exists; EU 36–41 | C |

**The colour code was resolved by the source, not by me.** Fetching the bare
product URL redirected to `?color=FUX`, so the site itself selected fuxia as
this article's default. That is a better outcome than the reconnaissance sweep
PM-030 needed to resolve its colourway.

The eBay listing is identity corroboration **only**. Marketplaces are barred as
primary media by the source hierarchy and it contributed no image.

## 4. Sizes — user-supplied only

```text
36 — available
37 — available
38 — available
39 — available
40 — available
```

`inventoryMode: 'availability'`. No source declared an exact size scale that
the pipeline itself read, so under the ladder-evidence rule the supplied labels
stand as availability truth and **no sold-out ladder is asserted**. No
quantities, no scarcity.

## 5. Media — 5 images, official manufacturer tier

| Position | Image | View | Size |
|---|---|---|---|
| MAIN | 01 | lateral side profile | 1200×1200 |
| `gallery[0]` | 02 | three-quarter front | 1200×1200 |
| `gallery[1]` | 03 | medial side | 1200×1200 |
| `gallery[2]` | 05 | three-quarter, raised | 1200×1200 |
| `gallery[3]` | 04 | heel and back | 1200×1200 |

| Image | SHA-256 |
|---|---|
| 01 | `e8b2cb59f77350535b4b9620a35bb5e1bfdba26836f773c4344ed435c3ee61fa` |
| 02 | `039078f3e85d04f3f731055272032134eee801bb056f1087add103e53c5d8892` |
| 03 | `83147aa9fd6e05f9b27bbc3ffc816ca0a5abc67207bbc7431bab03c6f7f47d3b` |
| 04 | `92a03de1e9f2a90fafb87176467f5c034359aeb5dafd48dcfee384f68f4a1333` |
| 05 | `2e7b67682f450e841b2d83064a35acdd67a5f0dbb4d5dca2e360316692533691` |

MAIN is IMAGE 01, matching the automation's proposal and correct on review: the
whole boot, lateral, legible at thumbnail size. The straight-on back view sits
last.

Detected backdrop `#FFFFFF` → `media.surface`. `media.fit: 'contain'`. Native
1200×1200, no canvas manufactured. Product-only, no people.

Contact sheet: `docs/pink-mall/media-acquisition/HC.RBGLOW01/CONTACT_SHEET.webp`
Provenance: `docs/pink-mall/media-acquisition/HC.RBGLOW01/result.json`

## 6. Provenance

**PRIMARY MEDIA TIER: OFFICIAL manufacturer media** — `hub2.artcrafts.it`.

That host is not a third-party retailer's. Colors of California was founded in
Florence in 1989 as the sportswear brand of **Artcrafts International S.p.A.**,
which owns and operates it, so this is the brand owner's own media host — the
same situation already accepted for `images.pepejeans.com` on Salesforce
Commerce Cloud and `nb.scene7.com` on Scene7. The ownership was verified rather
than assumed, because the tier is a provenance claim.

Fourth product in the catalogue with manufacturer-tier imagery, after PM-026,
PM-029 and PM-030.

Asset paths are self-evidencing twice over —
`/_public/resized/1200x1200/HC/F24/FUX/HC.F24.RBGLOW01-FUX-<n>.jpg` carries both
the article code and the colour code — so a candidate could be neither another
product nor the sibling `MUD` colourway.

## 7. Alt text — Bulgarian

```text
imageAlt      — Розови гумени ботуши Colors of California Glossy rainboot с грайферна подметка, страничен изглед
galleryAlt[0] — Розови гумени ботуши Colors of California, изглед под ъгъл отпред
galleryAlt[1] — Розови гумени ботуши Colors of California, изглед от вътрешната страна
galleryAlt[2] — Розови гумени ботуши Colors of California, изглед под ъгъл отгоре
galleryAlt[3] — Розови гумени ботуши Colors of California, изглед от петата
```

No comfort, fit, performance, waterproofing or care claims.

## 8. Material — deliberately omitted

The boot is plainly a moulded rubber-type material and the brand's own category
is "rain boots", but the pipeline never extracted a composition string from the
page it read. Under the same standard applied to PM-026 through PM-030,
`composition` is omitted and the PDP renders no material row.

The word "гумени" (rubber) does appear in the alt text — that is a description
of what is visible in the photograph, not a published composition claim.

## 9. Mall copy and tags

```text
Colors of California Glossy rainboot в наситено розово — гланцирани гумени
ботуши с грайферна подметка. За дъждовни дни, но определено не за скучни.
```

```text
colors of california, glossy rainboot, rainboot, boots, shoes, pink, fuxia, rubber, glossy, chelsea, lug sole
```

Internal only, never rendered as public specs.

## 10. Warnings — one, non-blocking

1. **Resolution is 1200×1200** — above the 1000 px preference, below the 1600 px
   ideal. That is what the source serves for this article; the page also
   declares 400×570 and 220×200, both smaller. Nothing was upscaled.

## 11. Staged product object — NOT PUBLISHED

```js
{
    id: 'PM-031',
    brand: 'Colors of California',
    manufacturerItemNo: 'HC.RBGLOW01',
    name: 'Glossy rainboot',
    slug: 'colors-of-california-glossy-rainboot-pink',
    category: 'shoes', subcategory: 'boots',
    color: 'Pink',
    /* composition omitted — not established by this pipeline */
    priceEUR: 64,
    oldPriceEUR: null,
    description: 'Colors of California Glossy rainboot в наситено розово — '
               + 'гланцирани гумени ботуши с грайферна подметка. За дъждовни '
               + 'дни, но определено не за скучни.',
    selectedBy: null,
    tags: ['colors of california','glossy rainboot','rainboot','boots','shoes',
           'pink','fuxia','rubber','glossy','chelsea','lug sole'],
    featured: false, campaign: null, related: ['PM-011','PM-030'],
    isNew: false, newUntil: null,
    inventoryMode: 'availability',
    availability: { '36':'available', '37':'available', '38':'available',
                    '39':'available', '40':'available' },
    media: {
        image:      'assets/pink-mall/products/PM-031/PM-031-main.webp',
        imageAlt:   'Розови гумени ботуши Colors of California Glossy rainboot с грайферна подметка, страничен изглед',
        gallery:   ['assets/pink-mall/products/PM-031/PM-031-02.webp',
                    'assets/pink-mall/products/PM-031/PM-031-03.webp',
                    'assets/pink-mall/products/PM-031/PM-031-04.webp',
                    'assets/pink-mall/products/PM-031/PM-031-05.webp'],
        galleryAlt:['Розови гумени ботуши Colors of California, изглед под ъгъл отпред',
                    'Розови гумени ботуши Colors of California, изглед от вътрешната страна',
                    'Розови гумени ботуши Colors of California, изглед под ъгъл отгоре',
                    'Розови гумени ботуши Colors of California, изглед от петата'],
        fit: 'contain', surface: '#FFFFFF',
        ph: 'shoes', field: 'blush'
    }
}
```

## 12. Approval preview

```text
STATUS:   READY FOR APPROVAL
VARIANT:  VARIANT_CONFIDENCE_PASS
BRAND:    Colors of California
MODEL:    Glossy rainboot
ITEM:     HC.RBGLOW01   (colour FUX, season F24)
MALL ID:  PM-031 (proposed)
CATEGORY: SHOES > Boots        ← new subcategory, approved
COLOR:    Pink   (manufacturer: Fuxia)
MATERIAL: omitted — not established by this pipeline
PRICE:    €64
SIZES:    36, 37, 38, 39, 40 — all available (no sold-out states asserted)
NEW:      YES for 14 days after first approved publication
MAIN:     IMAGE 01
GALLERY ORDER: 01 (MAIN) → 02 → 03 → 05 → 04
MEDIA TIER: OFFICIAL — hub2.artcrafts.it, brand owner's CDN
WARNINGS: 1200×1200, above the 1000px preference and below the 1600px ideal
```

**Awaiting:** `APPROVE` / `CHANGE MAIN TO IMAGE 0X` / `REORDER` /
`REMOVE IMAGE 0X` / `CHANGE COPY` / `REJECT`.
