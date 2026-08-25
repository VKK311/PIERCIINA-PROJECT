# PINK MALL — Real Product Store Calibration Report

Date: 2026-08-24
Scope: engine calibration only. JQ4556 NOT published. Catalog unchanged.

## Files

| | |
|---|---|
| SOURCE | `PINKMALL_PRE_RELEASE_AUTOPLAY_FIXED_RECONSTRUCTED.html` |
| SOURCE SHA-256 | `37b74632a5fa405f2bee3a857f99424a8bb6a1fd4fb0289e6180178395a4a9a7` |
| Source untouched | verified byte-for-byte after edit |
| OUTPUT | `PINKMALL_REAL_PRODUCT_CALIBRATION.html` |
| OUTPUT SHA-256 | `dc7050ba22862b4f4f1a07cae0365e6f648dde9d726475223279fd839962a2f0` |
| OUTPUT bytes | 2537910 |

---

## Exact changes made

All changes are additive and sit **beside** the existing engine.

### 1. Dual inventory model
Added an adapter layer every downstream consumer goes through:

- `isAvailabilityMode(p)` — true when `inventoryMode:'availability'` + `availability{}`
- `sizeState(p,size)` → canonical `'available' | 'last' | 'soldout'`
- `hasSize(p,size)` — mode-aware key existence
- `sizesOf`, `inStockSizes`, `canOrder`, `matchesSizes` rewired through the adapter
- `stockTotal(p)` returns `null` in availability mode — quantities are unknown and are never invented

Legacy quantity products take an unchanged code path. In quantity mode
`sizeState` derives `last` from `n===1`, preserving existing semantics.

### 2. Product-level stock logic
`getStockState` branches by mode:

- **availability**: any non-soldout size → `ok` with **empty label**; all soldout → `soldout` / ИЗЧЕРПАН. No ПОСЛЕДНИ БРОЙКИ, no МАЛКО РАЗМЕРИ — ever.
- **quantity**: byte-identical logic to before (soldout / last / limited / ok).

`last` in availability mode originates only from explicit input; it is never derived.

### 3. Fractional EU sizes
Added `sizeSortKey(s)` — parses `"37 1/3"` into an ordering key **only**.
The label itself is never converted, rounded or normalised anywhere:
stored, compared, rendered, selected and sent to Viber as the exact string.

`sortSizes` now orders `36 < 36 2/3 < 37 1/3 < 38 < 38 2/3 < 39 1/3 < 40`.
Whole sizes and ONE SIZE behave exactly as before.

### 4. Date-based NEW
Added central helper `isProductNew(p)`:
- `newUntil` present → date comparison
- otherwise → legacy boolean `isNew`

All 7 consumers rerouted (category, sort, filter, badge, directory count,
rivalry stats, NEW rail). No demo data was rewritten.

### 5. Global delivery
`CONFIG.shipping.deliveryEstimate = '4–7 работни дни'` plus helper
`deliveryEstimate(product)` — global by default, per-product override only
if explicitly supplied. Rendered once in the existing PDP shipping line.
Country / couriers / cash-on-delivery / returns unchanged.

### 6. Optional real-product fields
Supported: `brand`, `color`, `manufacturerItemNo`, `inventoryMode`,
`availability`, `newUntil`, `deliveryEstimate`.
Every PDP spec row is now conditional — an unconfirmed field renders nothing.
No `null`/`undefined`/placeholder text. Brand renders restrained above the
product name on card and PDP; existing hierarchy untouched.

### 7. Media / alt readiness
Existing gallery already supports MAIN + gallery array + per-image alt
(`media.image`, `media.gallery[]`, arrows, thumbs, counter, swipe, keyboard).
No change was required and none was made. No JQ4556 media inserted, no hotlinks.

### 8. Search
Index extended with `brand`, `manufacturerItemNo`, `color`.
Tags remain internal — not rendered publicly. No child-series metadata is
present anywhere to leak.

---

## Two real bugs found and fixed

The calibration fixture caught two defects that static reading missed:

1. **`resolveOrder` threw on availability products.** It called
   `hasOwnProperty.call(p.inventory, size)` directly; availability products
   have no `inventory` object at all → `TypeError`. This is the order-safety
   gate, so the failure would have been on the ordering path. Rewired to `hasSize()`.

2. **`matchesSizes` silently excluded availability products.** It read
   `p.inventory[s] > 0` → `undefined > 0` → `false`, so a real product would
   never appear under a size filter. Rewired to `sizeState()`.

---

## Test fixture result (§18)

Non-public fixture exposed only as `PinkMallStore.__calibrationFixture`.
It is **not** in `PINK_MALL_PRODUCTS`, not rendered, not searchable, not filterable.

Proven with the fixture temporarily injected at runtime (file never contained it):

| Check | Result |
|---|---|
| Ladder renders exactly | `36, 36 2/3, 37 1/3, 38, 38 2/3, 39 1/3, 40` |
| Sold-out controls disabled | exactly `36 2/3, 38, 39 1/3` |
| Available fractional selectable | `37 1/3` selected |
| Product-level scarcity badge | **none** |
| `getStockState().total` | `null` — no invented quantities |
| Order message | `Искам VL Court Bold Shoes / размер 37 1/3 / Product ID …` |
| Exact size string survives | yes — no `37`, no `37.33`, no `37⅓` |
| Viber URL | unchanged, no `?text=` |
| Sold-out size order | blocked |
| Non-existent size `37` | blocked |
| Click sold-out | selection unchanged |
| All sizes soldout | `soldout` / ИЗЧЕРПАН, no scarcity |
| Explicit `last` | size shows last; product label still empty |
| Catalog after removal | 24 products, fixture gone |

---

## Full regression result (§17)

| | Check | Result |
|---|---|---|
| A | Catalog 24, PM-001..PM-024, no PM-025 | PASS |
| B | Quantity mode: soldout/last/limited/ok all present | PASS |
| C | ONE SIZE: PM-007 auto `ONE SIZE`, PM-010 `null` | PASS |
| D | Sold-out bottom in all 4 sorts | PASS |
| E | Search (`чанти` → 4) | PASS |
| F | Filters: `both`, `availability:'out'` → 4 | PASS |
| G | Wishlist sanitizer → `PM-001,PM-002` | PASS |
| H | PDP renders, no `null`/`undefined` | PASS |
| I | Viber destination unchanged, no `?text=`, exact message | PASS |
| J | Hero 3000 ms, no hover pause (real mouse) | PASS |
| K | Campaign 3000 ms, no hover pause, 0 controls | PASS |
| L | 8 viewports, hScroll 0 everywhere | PASS |
| M | Zero console/page errors | PASS |

Legacy spot-check: PM-011 still renders whole sizes `36–41` with
`МАЛКО РАЗМЕРИ` — quantity behaviour untouched.

---

## Catalog state

| | |
|---|---|
| Products | 24 |
| Range | PM-001 … PM-024 |
| PM-025 present | no |
| Next proposed Mall ID | **PM-025** |
| JQ4556 in catalog | no |

## Final status

```text
REAL PRODUCT CALIBRATION: PASS
```
