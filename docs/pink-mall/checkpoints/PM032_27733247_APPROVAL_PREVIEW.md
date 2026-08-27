# PINK MALL — Scotch & Soda 27733247 approval preview (PM-032 proposed)

**STATUS: READY FOR APPROVAL — NOT PUBLISHED**
media tier: **USER-SUPPLIED** · `HUMAN_VARIANT_REVIEW_REQUIRED`

This one did not come from the pipeline. Four runner passes were walled by bot
protection at every retailer, and the media here is the three photographs you
supplied directly. That changes what can be claimed about it, and §6, §7 and
§10 are the parts worth your attention rather than the field list.

---

## 1. Product

| | |
|---|---|
| Brand | Scotch & Soda — **confirmed from the product itself** |
| Model | `Celest` — **asserted in your brief, not evidenced by any source I reached** (§6) |
| Manufacturer item | 27733247 |
| Colour code | your brief says `34A`; your supplier URL says `S059` (§6) |
| Mall ID | PM-032 (proposed — allocated only on publish) |
| Category | SHOES > Sneakers |
| Public colour | Pink (manufacturer: `Rose`) |
| Material | **omitted** — see §8 |
| Price | €69 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| NEW | 14 days from first approved publication |
| Delivery | global — `4–7 работни дни` |

A monochrome pale-pink chunky sneaker: suede-look overlays over mesh panels,
flat tonal laces, a small circular logo at the side, and a thick sculpted
midsole. Everything in that sentence is visible in your photographs.

## 2. Sizes

```text
37 — available
38 — available
39 — available
40 — available
```

`inventoryMode: 'availability'`, no sold-out ladder asserted, no quantities.

**Size 41 is not listed.** You supplied it and it is a real size for this shoe,
but PINK MALL's public ladder stops at EU 40 and you chose to keep that cap.
That pair simply will not be orderable through the Mall. Flagging it once more
because it is stock you hold that the storefront will not sell.

`SIZE_CONFIRMED` — all four sit inside the EU 36–42 scale the brand declares
for this line. That scale is line-level evidence, not a document about this
exact article.

## 3. Media — 3 images

| Position | Image | View |
|---|---|---|
| MAIN | 01 | three-quarter front, pair |
| `gallery[0]` | 02 | top-down, upper and branding |
| `gallery[1]` | 03 | head-on front, toe and sole |

| Image | SHA-256 of the file you sent |
|---|---|
| 01 | `97597171d7edb62aa24e0b240e4952136f0ae7f503cd2bac881d23b0c83fa63f` |
| 02 | `385fc75ff6d9591cd7e141cb0ff025ff1c09ca7df87267d53ac896ab7df10745` |
| 03 | `1dd0b4d0daedad6aaf469e86f97067a9de7b4b240e713f6cd004c1056732b30a` |

Three unique shots, confirmed distinct by perceptual hash (pairwise distances
103–142; duplicates would score ≤4). Product-only, no people. Three is the
minimum the media policy allows, so there is no room to drop one.

**There is no side profile and no heel view.** Every product PM-025 through
PM-031 leads with a lateral shot. This set has none, so MAIN is the
three-quarter pair instead — the only frame showing the whole shoe in profile-ish
form. If your supplier has a side and a back view, adding them would make this
set materially better.

Backdrop is a grey studio sweep with a gradient rather than a flat colour, so
no single backdrop could be derived. `media.surface` is set to `#D2D5D7`, the
median border tone across all three, so the letterboxed area matches the
photographs instead of drawing a bright box edge around them.

## 4. Resolution — the main reason to think twice

Native **480 × 720**. Measured against what the storefront actually renders:

| Context | Needs | Have | Short by |
|---|---|---|---|
| Card, desktop @2x | 496 px | 480 | ~0% |
| Card, phone @3x | 594 px | 480 | 19% |
| PDP hero, desktop @2x | 752 px | 480 | 36% |
| **PDP hero, phone @3x** | **1044 px** | **480** | **54%** |

Cards are fine. **The PDP hero will look soft, most of all on phones.**

For scale: PM-031 at 1200×1200 was flagged as the catalogue's weakest, and this
is well under half that. It is the lowest-resolution product media PINK MALL
would carry.

Nothing was upscaled. No AI enlargement, no sharpening, no generative edit —
the rule against those does not bend because the source is small, and an
upscale would invent detail the photograph never had.

## 5. Provenance

**Transport: `USER_SUPPLIED`. Tier: NOT official manufacturer media.**

You sent these directly after every automated route was blocked. They carry no
source URL, so unlike PM-026 or PM-031 there is no manufacturer CDN path
standing behind them. That is not a defect in the photographs — they are clean
studio product shots — but the provenance claim is weaker and the package says
so rather than dressing it up.

## 6. Two identity facts that are NOT settled

**The model name.** "Celest" comes from your brief. Nothing I reached confirms
it, and there is mild evidence against it:

- Your supplier's own title for this article is just "Спортни обувки с велур" —
  no model name. That retailer *does* name models when it has them, listing
  `Кецове Sylvie` and `Спортни обувки Vivi` for other Scotch & Soda shoes.
- The Celest listings I found are characteristically **multicolour** — Candy
  Pink Multi, Camel/Black, Cream/Yellow, Coral Multi, Off-White Multi. Your
  shoe is **monochrome** pale pink.

It may well still be a Celest colourway. But publishing a model name the
sources do not support is inventing a product name, so I want you to confirm it.

**The colour code.** Your brief says `34A`; your supplier URL says `S059`. The
article number anchors the product and both agree it is pink, but the codes
differ. The code is internal only — the public colour reads `Pink` either way.

## 7. Alt text — Bulgarian

```text
imageAlt      — Розови маратонки Scotch & Soda с масивна подметка, изглед под ъгъл отпред
galleryAlt[0] — Розови маратонки Scotch & Soda, изглед отгоре с лого на езика
galleryAlt[1] — Розови маратонки Scotch & Soda, изглед отпред
```

No comfort, fit, performance or care claims. No material word, deliberately —
see §8.

## 8. Material — omitted

Your supplier's URL slug says "велур" (suede) and the brand describes this line
as cow suede with nylon panels, but the pipeline never read a composition
string from a page, and suede versus synthetic suede is not something a
photograph settles. Same standard as PM-026 through PM-031: `composition` is
omitted and the PDP renders no material row.

Unlike PM-031, where "гумени" described an unmistakable moulded rubber boot, I
kept the material word out of the alt text too.

## 9. Mall copy and tags

```text
Scotch & Soda в пудрено розово — масивни маратонки в един тон, от подметката
до връзките. Тихият флекс, който върви с всичко.
```

```text
scotch & soda, scotch and soda, celest, sneakers, shoes, pink, pale pink,
blush, chunky, monochrome
```

Internal only. `celest` is included so the item is findable under the name you
use for it, whatever §6 concludes.

## 10. Staged product object — NOT PUBLISHED

```js
{
    id: 'PM-032',
    brand: 'Scotch & Soda',
    manufacturerItemNo: '27733247',
    name: 'Celest',
    slug: 'scotch-and-soda-celest-pink',
    category: 'shoes', subcategory: 'sneakers',
    color: 'Pink',
    /* composition omitted — not established by this pipeline */
    priceEUR: 69,
    oldPriceEUR: null,
    description: 'Scotch & Soda в пудрено розово — масивни маратонки в един '
               + 'тон, от подметката до връзките. Тихият флекс, който върви '
               + 'с всичко.',
    selectedBy: null,
    tags: ['scotch & soda','scotch and soda','celest','sneakers','shoes',
           'pink','pale pink','blush','chunky','monochrome'],
    featured: false, campaign: null, related: ['PM-030','PM-025'],
    isNew: false, newUntil: '2026-09-10',
    inventoryMode: 'availability',
    availability: { '37':'available', '38':'available',
                    '39':'available', '40':'available' },
    media: {
        image:      'assets/pink-mall/products/PM-032/PM-032-main.webp',
        gallery:   ['assets/pink-mall/products/PM-032/PM-032-02.webp',
                    'assets/pink-mall/products/PM-032/PM-032-03.webp'],
        fit: 'contain', surface: '#D2D5D7',
        ph: 'shoes', field: 'blush'
    }
}
```

## 11. Approval preview

```text
STATUS:   READY FOR APPROVAL
BRAND:    Scotch & Soda            (confirmed from the product)
MODEL:    Celest                   ← NOT source-evidenced, please confirm
ITEM:     27733247                 (colour code: brief 34A vs supplier S059)
MALL ID:  PM-032 (proposed)
CATEGORY: SHOES > Sneakers
COLOR:    Pink   (manufacturer: Rose)
MATERIAL: omitted — not established by this pipeline
PRICE:    €69
SIZES:    37, 38, 39, 40 — all available.  41 dropped by your Mall-cap decision
MAIN:     IMAGE 01
GALLERY:  01 (MAIN) → 02 → 03
MEDIA:    3 images, native 480x720, surface #D2D5D7, fit contain
TIER:     USER-SUPPLIED — not official manufacturer media
WARNINGS: 1. 480x720 is the lowest-resolution media in the catalogue; PDP hero
             is 54% short on phones
          2. model name unconfirmed
          3. no side profile, no heel view; 3 images is the policy minimum
```

**Awaiting:** `APPROVE` / `CHANGE MAIN TO IMAGE 0X` / `REORDER` /
`CHANGE COPY` / `CHANGE MODEL NAME TO …` / `REJECT`.
