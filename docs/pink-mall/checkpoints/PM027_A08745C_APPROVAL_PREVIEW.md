# PINK MALL — A08745C approval preview (PM-027 proposed)

**STATUS: READY FOR APPROVAL — NOT PUBLISHED**

Zero-seed onboarding. Human input remained the original four fields; identity,
media discovery and acquisition were all automatic.

---

## 1. Product

| | |
|---|---|
| Brand | Converse |
| Model | Chuck Taylor All Star Move |
| Manufacturer item | A08745C |
| Mall ID | PM-027 (proposed — allocated only on publish) |
| Category | SHOES > Sneakers |
| Public colour | Pink |
| Material | *not confirmed* |
| Price | €49 |
| oldPriceEUR | null — no SALE |
| selectedBy | null |
| NEW | 14 days from first approved publication |
| Delivery | global — `4–7 работни дни` |

A platform high-top: pink canvas upper, white All Star patch, white lace-up
eyelets, white platform midsole. Verified on every frame.

## 2. Sizes — user-supplied only

```text
36   — available
37.5 — available
38   — available
39   — available
```

`inventoryMode: 'availability'`. The exact-model size run could not be proven,
so under the ladder-evidence rule no sold-out sizes are asserted. No quantities,
no scarcity.

## 3. Media — 5 images, discovered and acquired automatically

| Position | Image | View | Size |
|---|---|---|---|
| MAIN | 01 | lateral side profile, single shoe | 1500×1500 |
| gallery[0] | 05 | pair, three-quarter front | 670×670 |
| gallery[1] | 02 | pair, angled | 670×670 |
| gallery[2] | 04 | medial side profile, single shoe | 670×670 |
| gallery[3] | 03 | pair, flat and top-down | 670×670 |

| Image | SHA-256 |
|---|---|
| 01 | `231e637a1117092ba8a436e8d723c33964063100f1fce008827ae37dc41067f2` |
| 02 | `a5be621bd2b3abd96e7e3d47190fd22d7228c78467a32de516bc46b46be7dca3` |
| 03 | `91628dbf5104a03d8974836d6f378f7126af34148c7ccc589afe38d749b2eba1` |
| 04 | `fd5a1a2f274ba1670374cf0005624dad53f71eb03e72917cdfb1d4f4ba5f8c04` |
| 05 | `8b96c65f238d57f0dd8ff4d727341668c2bb803875c375dd1cc3499c111975d3` |

Detected backdrop `#FFFFFF` → `media.surface`. Native aspect ratio; no canvas
manufactured. All product-only, no people, 0 duplicates after collapse.

## 4. Provenance — discovery ledger

| Route | Result |
|---|---|
| `DIRECT_OFFICIAL_PAGE` converse.com ×4 (global, /uk/en, /nl/en, API) | `403` |
| `OFFICIAL_REGIONAL_SEARCH` converse.com.tr ×2 | `404` — search path guessed wrong |
| `TRUSTED_RETAILER_SEARCH` ayakkabidunyasi.com.tr | timeout |
| `TRUSTED_RETAILER_SEARCH` **spx.com.tr** | **OK — SKU evidenced, 252 candidates** |
| `TRUSTED_RETAILER_SEARCH` superstep.com.tr | OK — SKU evidenced, 53 candidates |

**PRIMARY SOURCE: trusted retailer fallback.** Converse's own storefront never
loaded for the runner, so this is tier 5 of the hierarchy, not official media.

Identity gate rejections on this run: 47 page-sweep candidates and 7
editorial/chrome assets refused.

## 5. Alt text — Bulgarian

```text
imageAlt      — Розови Converse Chuck Taylor All Star Move високи кецове на платформа, страничен изглед
galleryAlt[0] — Розови Converse Chuck Taylor All Star Move, изглед под ъгъл отпред
galleryAlt[1] — Розови Converse Chuck Taylor All Star Move, чифт под ъгъл
galleryAlt[2] — Розови Converse Chuck Taylor All Star Move, изглед от вътрешната страна
galleryAlt[3] — Розови Converse Chuck Taylor All Star Move, изглед отгоре
```

No child-series markers. No comfort, fit, performance or care claims.

## 6. Mall copy

```text
Converse Chuck Taylor All Star Move в розово, на платформа. Класическият
силует, но вдигнат — high-top energy без излишна драма.
```

## 7. Internal tags

```text
converse, chuck taylor, all star, move, sneakers, shoes, pink, platform, high-top, canvas
```

## 8. Warnings — three, none blocking

1. **Resolution.** Four images are 670×670, below the 1000 px preference; only
   MAIN is 1500×1500. Acceptable for approval and card preview; higher-resolution
   official copies preferred before launch. Do not upscale.
2. **Primary source is a retailer, not Converse.** Every official route failed.
   Media is exact-SKU and visually verified, but it is tier-5 evidence.
3. **Material not confirmed** — omitted rather than guessed.

The manufacturer classifies this line as a youth/junior series item. Internal
only; it appears nowhere above.

## 9. Approval preview

```text
STATUS: READY FOR APPROVAL
BRAND:  Converse
MODEL:  Chuck Taylor All Star Move
ITEM:   A08745C
MALL ID: PM-027 (proposed)
CATEGORY: SHOES > Sneakers
COLOR:  Pink
MATERIAL: not confirmed
PRICE:  €49
SIZES:  36, 37.5, 38, 39 — all available (no sold-out states asserted)
NEW:    YES for 14 days after first approved publication
MAIN:   IMAGE 01
GALLERY ORDER: 01 (MAIN) → 05 → 02 → 04 → 03
SOURCE STATUS: EXACT SKU A08745C — trusted retailer fallback (spx.com.tr,
               superstep.com.tr); Converse official routes all 403
WARNINGS: 670px on four images; retailer-tier source; material unconfirmed
```

**Awaiting:** `APPROVE` / `CHANGE MAIN TO IMAGE 0X` / `REORDER` / `REMOVE IMAGE 0X` /
`CHANGE COPY` / `REJECT`.
