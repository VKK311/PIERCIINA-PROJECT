# PINK MALL — Jimmy Choo SPARKS/G/S 8CQ approval preview (PM-040 proposed)

**STATUS: READY FOR APPROVAL — NOT PUBLISHED**
identity: **confirmed from the frame itself** · media tier: **USER_SUPPLIED**

First ACCESSORIES product from the automated pipeline. Read §3 first — it
corrects something I told you earlier.

---

## 1. Product

| | |
|---|---|
| Brand | Jimmy Choo (eyewear under Safilo licence) |
| Model | **Sparks** |
| Manufacturer item | `SPARKS/G/S`, colourway **8CQ** (sold as 8CQ/U1) |
| Eyewear measurement | 55–17–140 |
| Mall ID | PM-040 (proposed — allocated only on publish) |
| Category | ACCESSORIES, `subcategory: null` |
| Public colour | **Pink** — see §3 |
| Composition | **omitted** — see §6 |
| Price | €71 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| Availability | **ONE SIZE** |
| Delivery | global — `4–7 работни дни` |

An angular cat-eye sunglass in translucent rose acetate, with a crystal-set
CHOO logo at the temple and rose-tinted lenses.

## 2. Identity — confirmed from the product, not inferred

Your photo of the inner temple carries the compliance print, and it reads
**`SPARKSGS 8CQ…U1 55▫17 140`**. That is the model and the exact colourway,
printed on the frame itself — the strongest identity evidence available, and
better than anything the retailers gave.

It is independently corroborated: an exact-SKU retailer image acquired earlier
from `cdn2.jomashop.com` shows the same frame, same crystal CHOO logo, same
lens tint. That image is **not** in the gallery (see §4) but stays on record as
the identity anchor.

`SPARKS/G/S` ships at least three pink-ish colourways — 8CQ, 8CO and 1N5 — so
the code alone never pinned one. You chose 8CQ, and the frame's own print
agrees.

## 3. Colour — I got this wrong, and here is the correction

**I told you this frame was "plum / wine-purple, not pink". That was an
overstatement**, drawn from a single darker retailer photograph.

Measured across both your photos and the retailer image, the frame sits at
**hue 325–336°** with low saturation (0.12–0.20). That is the rose/magenta
band, not the violet one — violet would be 270–300°. It is a muted **rose-mauve**:
dusty pink with a faint purple cast.

So **`Pink` is defensible** and matches your brief. `Pink / Mauve` would be
more precise if you want the nuance on the card. The alt text describes the
rose tone either way.

Worth keeping in view: retailers genuinely disagree about this colourway —
eBay via Otticanet says *violet*, SmartBuyGlasses *transparent purple with pink
lenses*, Go-Optic *cherry*, Jomashop and Timepiece *pink*. Your photographs
settle it, and they land on the pink side.

## 4. Media — 3 images

| Position | Image | View |
|---|---|---|
| MAIN | 01 | three-quarter front, whole frame |
| `gallery[0]` | 02 | rear three-quarter, temple and compliance print |
| `gallery[1]` | 03 | crystal CHOO logo detail |

| Image | SHA-256 |
|---|---|
| 01 | `c538df51fe609a7f777026577664f16805885864cae5f9d9d9e75e44741ffe23` |
| 02 | `04cb75ed6fba6c98baae8e20018204677a152e02dcddeb4f029c1a98c4f63de5` |
| 03 | `50112031dd8e9b96451dcc09ef72c88fc62b0e870ce4e406c5b3575284894008` |

Native **~1284 × 1333–1404**, three unique shots confirmed by perceptual hash
(closest pair 56, where a duplicate scores ≤4), product-only, no people,
consistent `#F1F1F1` studio backdrop. Aspect 1.04–1.09, inside the 2.2 limit.

**The acquired retailer image is deliberately excluded.** It is 800×800 (1:1)
on a `#FFFFFF` ground where yours are ~1284px on `#F1F1F1`; mixing resolution,
aspect and backdrop in one gallery looks broken. Yours are also the better
images. It stays on record as independent exact-SKU corroboration.

`media.surface: '#F1F1F1'`, measured and identical across all three.

No warnings: 1284 px clears the 1000 px preference.

## 5. Provenance — identity and media are separate claims

| | |
|---|---|
| **Identity** | the frame's own temple print, corroborated by an exact-SKU retailer image (`cdn2.jomashop.com`, TRUSTED_RETAILER) |
| **Media** | **USER_SUPPLIED** — your three photographs, no source URL |

The media does not inherit the retailer's standing, and is not manufacturer
media. Four acquisition passes across six retailer catalogues and three
official URLs produced exactly one usable frame, so the gallery is yours.

## 6. What is not published

- **Composition** — omitted. Retailers describe the frame as plastic/acetate
  with polycarbonate lenses, but no exact-product source states a composition
  for this article, so no material row is rendered. Same standard as PM-026
  onward.
- **Retailer stock state** — not imported. `ONE SIZE — available` is the whole
  availability truth.
- **The 55–17–140 measurement** — recorded here for provenance, not published:
  it is an eyewear fitting measurement, not a Mall size, and ONE SIZE is what
  the customer chooses.

## 7. Alt text — Bulgarian

```text
imageAlt      — Розови слънчеви очила Jimmy Choo Sparks с котешка форма и кристално лого, изглед под ъгъл
galleryAlt[0] — Розови слънчеви очила Jimmy Choo Sparks, изглед отзад с дръжките
galleryAlt[1] — Розови слънчеви очила Jimmy Choo Sparks, детайл на кристалното лого CHOO
```

## 8. Mall copy and tags

```text
Jimmy Choo Sparks в опушено розово — котешка форма, кристално CHOO на дръжката.
Дискретен блясък, който не се извинява.
```

```text
jimmy choo, sparks, sunglasses, cat eye, accessories, pink, mauve, rose,
crystal, choo, safilo
```

## 9. Staged product object — NOT PUBLISHED

```js
{
    id: 'PM-040',
    brand: 'Jimmy Choo',
    manufacturerItemNo: 'SPARKS/G/S',
    variantCode: '8CQ',
    name: 'Sparks',
    slug: 'jimmy-choo-sparks-pink',
    category: 'accessories', subcategory: null,
    color: 'Pink',
    /* composition omitted — not established by this pipeline */
    priceEUR: 71,
    oldPriceEUR: null,
    description: 'Jimmy Choo Sparks в опушено розово — котешка форма, '
               + 'кристално CHOO на дръжката. Дискретен блясък, който не се '
               + 'извинява.',
    selectedBy: null,
    tags: ['jimmy choo','sparks','sunglasses','cat eye','accessories','pink',
           'mauve','rose','crystal','choo','safilo'],
    featured: false, campaign: null, related: ['PM-015','PM-033'],
    isNew: false, newUntil: '<publish date + 14>',
    inventoryMode: 'availability',
    availability: { 'ONE SIZE': 'available' },
    media: {
        image:      'assets/pink-mall/products/PM-040/PM-040-main.webp',
        gallery:   ['assets/pink-mall/products/PM-040/PM-040-02.webp',
                    'assets/pink-mall/products/PM-040/PM-040-03.webp'],
        fit: 'contain', surface: '#F1F1F1',
        ph: 'accessories', field: 'blush'
    }
}
```

## 10. Approval preview

```text
STATUS:   READY FOR APPROVAL
BRAND:    Jimmy Choo
MODEL:    Sparks
ITEM:     SPARKS/G/S  ·  colourway 8CQ (8CQ/U1)  ·  55-17-140
IDENTITY: CONFIRMED from the frame's own temple print
MALL ID:  PM-040 (proposed)
CATEGORY: ACCESSORIES
COLOR:    Pink        ← corrected; measured hue 325-336°, rose not violet
MATERIAL: omitted — not established by this pipeline
PRICE:    €71
SIZES:    ONE SIZE — available
MAIN:     IMAGE 01     GALLERY: 01 → 02 → 03
MEDIA:    3 images, native ~1284px, surface #F1F1F1, fit contain
TIER:     USER_SUPPLIED — not manufacturer, not retailer media
WARNINGS: none
```

**Awaiting:** `APPROVE` / `CHANGE COLOR TO PINK / MAUVE` / `CHANGE MAIN TO IMAGE 0X` /
`REORDER` / `CHANGE COPY` / `REJECT`.
