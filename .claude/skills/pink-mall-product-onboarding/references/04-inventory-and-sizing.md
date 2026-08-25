# Inventory and Sizing

## Availability source of truth

Only user-supplied availability controls PINK MALL availability.

Never use:
- manufacturer stock;
- retailer stock;
- supplier website availability discovered externally;

unless the user explicitly supplied that information as PINK MALL truth.

## Default real-product inventory mode

Default:
`availability`

This means:
- user says which sizes are available;
- unit quantity is unknown;
- do not invent numeric counts.

Do not map every available size to quantity `1`.

## Size-specific last piece

If user says:

`37 1/3 - 1 бр.`

then only that size may show:
`ПОСЛЕДНА БРОЙКА`

Do not:
- infer quantities for other sizes;
- generate product-level `ПОСЛЕДНИ БРОЙКИ`;
- generate product-level `МАЛКО РАЗМЕРИ` for availability-only products.

For availability-mode product-level stock state:
- no available size => sold out;
- otherwise product-level state should remain orderable without unit-count scarcity claims.

## Quantity mode

If the user explicitly supplies exact quantities for every relevant size, quantity mode may be used.

Preserve existing quantity semantics for legacy/quantity products.

Do not remove the existing quantity model.

## Shoes — calibrated v1 rules

Public shoe size system:
EU only.

Public range:
EU 36 through EU 40 inclusive.

### Build the visible ladder

1. Find the official EU size scale for the exact model.
2. Keep all official sizes >= 36 and <= 40.
3. Fractional official sizes are preserved exactly.
4. Exclude every official size below 36 or above 40.
5. Mark user-supplied exact sizes as available.
6. Mark remaining in-range official sizes as `ИЗЧЕРПАН`.

Example official scale:

`35.5, 36, 36 2/3, 37 1/3, 38, 38 2/3, 39 1/3, 40, 40 2/3`

PINK MALL visible scale:

`36, 36 2/3, 37 1/3, 38, 38 2/3, 39 1/3, 40`

Do not add:
- 35.5
- 40 2/3

## Ladder evidence — what may be shown as sold out

A size shown as `ИЗЧЕРПАН` is a claim: *this product was offered in this size
and is currently out of stock.* It needs evidence like any other claim.

Two cases, and only two:

**Exact-model scale proven** → render the full in-range ladder. User-supplied
sizes are `available`; the remaining proven in-range sizes are `soldout`.

Proof means the size run for the **exact SKU**: official product data, page
state or API; exact-SKU official structured data; another official regional
source for the same SKU; or authoritative manufacturer data for that SKU.

**Exact-model scale not proven** → render **only the user-supplied sizes**.

A generic brand size-conversion chart is **not** proof. It shows how the brand
maps EU to UK to cm; it says nothing about which sizes this particular SKU was
manufactured in. Deriving a sold-out ladder from one invents inventory states
for sizes that may never have existed.

Never pad a ladder to look complete. A short truthful ladder beats a full
invented one.

## Strict user-size matching

Never silently normalize.

Example:

User:
`37`

Official exact model scale:
`37 1/3`

Result:
`BLOCKED`
`SIZE CONFIRMATION REQUIRED`

Do not assume supplier shorthand.

## EU conversion

If a reliable exact product source shows only UK/US:
- use official manufacturer conversion information;
- do not use a random conversion chart.

If conversion is ambiguous:
`SIZE CONFIRMATION REQUIRED`

## Suggested availability representation

For a backwards-compatible store calibration, a truthful conceptual representation is:

```js
inventoryMode: 'availability',
availability: {
  '36': 'available',
  '36 2/3': 'soldout',
  '37 1/3': 'last',      // only if user explicitly said 1 бр.
  '38': 'soldout',
  '38 2/3': 'available',
  '39 1/3': 'soldout',
  '40': 'available'
}
```

Allowed states:
- `available`
- `last`
- `soldout`

This is preferred over fake numeric quantities.

If current architecture chooses an equivalent representation, preserve truth and backward compatibility.

## Fully sold out

Temporarily fully sold out product:
- remains public;
- all size controls disabled;
- Viber/order CTA disabled;
- sorts after available products;
- keeps same PM ID.
