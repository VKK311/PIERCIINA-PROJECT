# PINK MALL — Stella McCartney TU0A28Z0699 approval preview (PM-033 proposed)

**STATUS: READY FOR APPROVAL — NOT PUBLISHED**
`VARIANT_CONFIDENCE_PASS` · media tier: **TRUSTED_RETAILER**

First BAGS product from the automated pipeline, and the first to reach PASS
through the reviewer-verified transport after every direct route was walled.

Read §3 and §6 before approving: the visual review corrected two things I had
told you earlier, and one of them affects the public colour.

---

## 1. Product

| | |
|---|---|
| Brand | Stella McCartney |
| Model | **Pineapple Bucket Bag** |
| Manufacturer item | TU0A28Z0699 (designer code `TU0A28Z0699 226VI`) |
| Retailer code | Giglio `401012`, colour variant `.003` |
| Mall ID | PM-033 (proposed — allocated only on publish) |
| Category | BAGS, `subcategory: null` |
| Public colour | **Yellow** — but see §3 |
| Composition | **`100% Polyurethane`** — publishable, see §5 |
| Dimensions | **omitted** — see §5 |
| Price | €109 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| Availability | **ONE SIZE** |
| NEW | until 2026-09-10 |
| Delivery | global — `4–7 работни дни` |

A small cylindrical bucket bag in yellow with a pink scalloped wave print, a
green drawstring top gathered into pineapple leaves, and a lilac adjustable
shoulder strap. Every one of those details is visible in the acquired frames.

**Model naming.** `Pineapple Bucket Bag` is the most defensible reading: it is
the brand's own wording for this design, and it is corroborated independently.
Retailers also list it as "Pineapple-Shaped Crossbody Bag" and "Pineapple Seal
Bag"; those are retailer names, not the manufacturer's, so they are not used.

## 2. ONE SIZE

```text
ONE SIZE — available
```

`inventoryMode: 'availability'`. Verified against the live storefront rather
than assumed: availability mode with `{'ONE SIZE': 'available'}` yields stock
state `ok`, is orderable at ONE SIZE, and correctly refuses any other size. No
engine calibration was needed. No sold-out variants invented, and no retailer
stock state imported.

## 3. Colour — a correction you should decide on

**Your brief lists the colour as Yellow, and the staged object uses `Yellow`.**

The frames show the body is yellow **printed with pink scalloped waves**, with
a green top and a lilac strap. Pink is not a trim detail here; it is roughly
half the visible surface.

I earlier told you this product was "yellow, not pink" and that it would be the
catalogue's first non-pink supplier product. **That was wrong**, and it was
based on retailer text rather than the photographs. An early search summary
also claimed a "purple waves print"; the waves are pink and the *strap* is
lilac, so that summary was wrong too. The frames settle it.

`Yellow / Pink` would be the more accurate public colour, and for this
storefront in particular. I have left `Yellow` as you specified — say the word
and it is a one-field change.

## 4. Media — 4 images

| Position | Image | View |
|---|---|---|
| MAIN | 01 | front, whole bag, strap tucked |
| `gallery[0]` | 02 | side profile, full crossbody strap |
| `gallery[1]` | 04 | open top, green pineapple leaves |
| `gallery[2]` | 03 | print and strap-attachment detail |

| Image | SHA-256 |
|---|---|
| 01 | `2bf52fedd7f50dbdefae063016b78599…` |
| 02 | `93c8283988f0f92d2220ef0ca0da7012…` |
| 03 | `3394eafdf694c5b6ca29da706bfd3fa8…` |
| 04 | `5d820a1b62677982246789fe47bc3aac…` |

Native **1125 × 1500** (3:4), four unique frames, product-only, no people.
MAIN is IMAGE 01 on review: the only frame showing the whole bag square-on. The
tight print detail sits last so the gallery does not open on a crop.

**`media.surface` is omitted.** Images 01, 02 and 04 sit on a studio white of
about `#ECECEC`; image 03 is a tight crop with no backdrop at all, which is why
no consensus backdrop could be derived. The Mall's own neutral `#EDEFF0` is
within three levels of that white, so the letterboxed area matches without
asserting a colour the set does not agree on.

One warning, non-blocking: **1500 px longest edge** — above the 1000 px
preference, below the 1600 px ideal. Nothing was upscaled.

## 5. What is published, and what is not

**Composition IS published: `100% Polyurethane`.** It is stated on the
exact-SKU Giglio document, which is a document about *this* article. This is
the first pipeline product to publish a composition — PM-026 through PM-032 all
omitted it because no exact-product source ever stated one.

**Dimensions are NOT published.** The widely repeated `14 × 17 × 11 cm` appears
only in search-engine paraphrase and on a Smallable page that does not name the
article (measured: `page_has_sku` False). No exact-product document read so far
states them, so no dimensions are rendered.

## 6. Provenance — TRUSTED_RETAILER, and why that label is now trustworthy

Media comes from `img.giglio.com`, the image CDN of Giglio, an established
Italian retailer. **This is not manufacturer media and is not presented as
such.**

That distinction only became reliable during this task. `_authority_tier` had
been seeding OFFICIAL from `allowed_hosts` — the *network permission* list — so
every trusted retailer in a brand's registry read as manufacturer media, and
these Giglio routes were being recorded as OFFICIAL. Worse, that same function
decides whether to keep hunting for official media, so a retailer answering
"yes, I am official" was silently switching official discovery off. Manufacturer
authority is now declared explicitly and nowhere else.

The four gallery URLs are **exact observed link targets** from the
reviewer-read product document. They were not constructed and not guessed, and
no template was extrapolated from them. Reviewer verification was not treated
as byte validation: each URL went through host check, fetch, MIME, dimensions,
non-product guards, identity, hash, dedupe, perceptual uniqueness, variant
confidence and backdrop detection.

Identity holds on the **asset URL itself** via the colour-scoped alias
`401012.003`. Bare `401012` is deliberately unused: the `.003` suffix is the
colour variant, and dropping it would let a sibling colourway through.

`VARIANT_CONFIDENCE_PASS`, with the official colour term found in the frames.

## 7. Alt text — Bulgarian

```text
imageAlt      — Жълта чанта Stella McCartney с розови вълни и зелена връзка във формата на ананас, изглед отпред
galleryAlt[0] — Жълта чанта Stella McCartney с лилава презрамка, страничен изглед
galleryAlt[1] — Жълта чанта Stella McCartney, отворен горен край със зелени листа
galleryAlt[2] — Жълта чанта Stella McCartney, детайл на щампата и закопчаването на презрамката
```

No comfort, capacity, fit or care claims. No age-series marker.

## 8. Mall copy and tags

```text
Stella McCartney ананас в чанта — жълто с розови вълни, зелени листа отгоре и
лилава презрамка. Малка, но напълно самоуверена.
```

```text
stella mccartney, pineapple, bucket bag, crossbody, bags, yellow, pink, green,
lilac, polyurethane, drawstring
```

Internal only, never rendered as public specs.

## 9. Staged product object — NOT PUBLISHED

```js
{
    id: 'PM-033',
    brand: 'Stella McCartney',
    manufacturerItemNo: 'TU0A28Z0699',
    name: 'Pineapple Bucket Bag',
    slug: 'stella-mccartney-pineapple-bucket-bag',
    category: 'bags', subcategory: null,
    color: 'Yellow',
    composition: '100% Polyurethane',
    priceEUR: 109,
    oldPriceEUR: null,
    description: 'Stella McCartney ананас в чанта — жълто с розови вълни, '
               + 'зелени листа отгоре и лилава презрамка. Малка, но напълно '
               + 'самоуверена.',
    selectedBy: null,
    tags: ['stella mccartney','pineapple','bucket bag','crossbody','bags',
           'yellow','pink','green','lilac','polyurethane','drawstring'],
    featured: false, campaign: null, related: ['PM-007','PM-010'],
    isNew: false, newUntil: '2026-09-10',
    inventoryMode: 'availability',
    availability: { 'ONE SIZE': 'available' },
    media: {
        image:      'assets/pink-mall/products/PM-033/PM-033-main.webp',
        imageAlt:   'Жълта чанта Stella McCartney с розови вълни и зелена връзка във формата на ананас, изглед отпред',
        gallery:   ['assets/pink-mall/products/PM-033/PM-033-02.webp',
                    'assets/pink-mall/products/PM-033/PM-033-03.webp',
                    'assets/pink-mall/products/PM-033/PM-033-04.webp'],
        galleryAlt:['Жълта чанта Stella McCartney с лилава презрамка, страничен изглед',
                    'Жълта чанта Stella McCartney, отворен горен край със зелени листа',
                    'Жълта чанта Stella McCartney, детайл на щампата и закопчаването на презрамката'],
        /* surface omitted deliberately — see §4 */
        fit: 'contain',
        ph: 'bags', field: 'blush'
    }
}
```

## 10. Approval preview

```text
STATUS:   READY FOR APPROVAL
VARIANT:  VARIANT_CONFIDENCE_PASS
BRAND:    Stella McCartney
MODEL:    Pineapple Bucket Bag
ITEM:     TU0A28Z0699   (designer TU0A28Z0699 226VI · Giglio 401012.003)
MALL ID:  PM-033 (proposed)
CATEGORY: BAGS
COLOR:    Yellow        ← frames show yellow WITH pink waves; see §3
MATERIAL: 100% Polyurethane   ← published, from the exact-SKU document
DIMENSIONS: omitted — no exact-product evidence
PRICE:    €109
SIZES:    ONE SIZE — available
NEW:      until 2026-09-10
MAIN:     IMAGE 01
GALLERY:  01 (MAIN) → 02 → 04 → 03
MEDIA:    4 images, native 1125×1500, fit contain, no surface asserted
TIER:     TRUSTED_RETAILER — Giglio, NOT manufacturer media
WARNINGS: 1500px longest edge (above 1000px preference, below 1600px ideal)
```

**Awaiting:** `APPROVE` / `CHANGE COLOR TO YELLOW / PINK` / `CHANGE MAIN TO IMAGE 0X` /
`REORDER` / `CHANGE COPY` / `REJECT`.
