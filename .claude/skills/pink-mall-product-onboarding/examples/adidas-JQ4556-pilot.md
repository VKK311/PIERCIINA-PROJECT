# Calibrated Pilot Example — adidas JQ4556

This example encodes expected skill behavior. Runtime research must still be performed fresh.

## User input

```text
adidas / JQ4556 / 54 EUR / 36, 37, 38 2/3, 40
```

Global Mall rule:
`Доставка: 4–7 работни дни`

## Exact identity expected from official adidas evidence

Manufacturer:
`adidas`

Manufacturer Item Number:
`JQ4556`

Official model:
`VL Court Bold Shoes`

Official color:
`Clear Pink / Silver Metallic / Gold Metallic`

Public PINK MALL model:
`VL Court Bold Shoes`

Public brand:
`adidas`

Do not publicly mention manufacturer child/junior classification.

## Simplified public fields

Proposed color:
`Pink / Silver / Gold`

Proposed material:
`Leather / Textile / Rubber`

Category:
`SHOES > Sneakers`

PINK MALL price:
`€54`

Never substitute adidas retail price.

## Size-scale calibration

Official adidas youth/teen EU sizing evidence historically includes:

`35.5, 36, 36 2/3, 37 1/3, 38, 38 2/3, 39 1/3, 40, 40 2/3`

PINK MALL shoe range 36–40 yields:

`36, 36 2/3, 37 1/3, 38, 38 2/3, 39 1/3, 40`

The user supplied:
`36, 37, 38 2/3, 40`

`37` does not equal `37 1/3`.

Under strict sizing rules, expected workflow result is:

```text
STATUS: BLOCKED
BLOCKER: SIZE CONFIRMATION REQUIRED
USER SIZE: 37
OFFICIAL EXACT SIZE SCALE: 37 1/3
```

Do not silently convert.

If current fresh source evidence unexpectedly proves whole EU 37 is exact for this SKU/variant, follow the fresh evidence instead of forcing this historical expectation.

## Conditional size display after user confirmation

Only if the user confirms that supplier `37` means official adidas `37 1/3`, the visible scale would become:

```text
36       — available
36 2/3   — sold out
37 1/3   — available
38       — sold out
38 2/3   — available
39 1/3   — sold out
40       — available
```

Do not apply this condition before confirmation.

## Inventory

Mode:
`availability`

No quantities were supplied.

Do not create:
`36:1`, `37:1`, etc.

No product-level low-stock/limited claims.

## Photography

Prepare:
- 3–5 unique high-quality product-only images;
- no people/models;
- MAIN clean product shot;
- secondary order chosen by Claude;
- deduplicate;
- exact variant only.

Official adidas media/CDN should be preferred when available.

Create a visual contact sheet for approval.

Do not hotlink live product media.

Do not generatively alter the shoe.

## Copy

Example tone only:

`Pink, chunky and not here to behave. VL Court Bold влиза с layered sole и точно толкова attitude, колкото трябва.`

Before using this exact copy, verify every factual reference against current exact-product evidence.

Do not add comfort/fit/performance claims unless confirmed and deliberately needed.

## NEW

At staging:
- not yet active.

At first approved publish:
- NEW active for 14 days.

## Sister selection

Not supplied.

Use:
`selectedBy:null`

## Dry-run expected status

Because of the size mismatch:

`BLOCKED`

The correct behavior is to finish research/media preparation and present the blocker, but not publish.
