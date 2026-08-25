# Current Store Calibration Requirements

This skill must work with the current PINK MALL source rather than assuming a brand-new commerce engine.

Before first real publish:
- inspect current source;
- prove what is already supported;
- add only minimal backward-compatible calibration needed for real products.

## Preserve current commerce architecture

Do not redesign or replace:
- PINK MALL single-page world;
- product cards;
- PDP shared modal/overlay;
- search/filter state;
- wishlist;
- related-product behavior;
- Viber order contract;
- consent/analytics protections;
- Hero/mannequin architecture;
- campaign systems.

Do not create:
- cart;
- checkout;
- account;
- payment flow.

## Quantity mode must survive

Legacy/demo and any true quantity-based products may use numeric per-size inventory.

Do not break:
- `soldout`;
- `last`;
- `limited`;
- `ok`;
- sold-out-bottom sorting;
- order validation;
- ONE SIZE behavior.

## Add availability mode truthfully

Current quantity-only helpers may assume numeric values.

For real supplier products, add an availability mode without inventing quantities.

Required behaviors for `inventoryMode:'availability'`:
- size list comes from the official model scale + Mall category range;
- user-listed exact sizes orderable;
- other allowed sizes sold out;
- explicit one-unit size may show size-specific `ПОСЛЕДНА БРОЙКА`;
- no general `ПОСЛЕДНИ БРОЙКИ`;
- no general `МАЛКО РАЗМЕРИ`;
- fully sold-out remains `ИЗЧЕРПАН`;
- sold-out sorting still works.

All variant/order helpers must understand both modes.

## Global delivery

Global rule:

`4–7 работни дни`

Preferred config:

```js
shipping: {
  country: 'България',
  couriers: ['Econt', 'Speedy'],
  payment: 'Наложен платеж',
  returns: '...',
  deliveryEstimate: '4–7 работни дни'
}
```

Render it from shared config.

Do not duplicate per product.

## NEW date calibration

Current legacy products may use boolean `isNew`.

For new real products:
- support a date-based expiry;
- first publish + 14 days;
- centralized helper;
- legacy fallback preserved.

Do not rewrite all demo data merely to introduce this support.

## Optional real-product specs

Real products do not need fake legacy fields.

PDP must safely omit:
- material when unconfirmed;
- color when unconfirmed;
- care/fit when not used.

Do not render `null`, `undefined`, or placeholder claims.

## Brand and color

Real product schema should support:
- `brand`;
- `color`;

without forcing a broad visual redesign.

If adding brand presentation:
- keep it restrained;
- preserve existing card/PDP hierarchy.

## Media + alt

Current media helpers may assume:
- one `media.image`;
- optional gallery strings;
- generic alt from product name.

Calibrate minimally so real products can carry:
- local MAIN;
- 2–4 local gallery images;
- per-image factual alt;
- maximum 5 canonical images.

Preserve legacy media behavior.

## Archived state

Do not implement archive infrastructure prematurely if no archive action is being performed.

When required:
- add a minimal status/visibility mechanism;
- public discovery excludes archived;
- internal ID lookup can retain archived records safely;
- wishlist should not surface archived items.

## Taxonomy

Primary categories remain locked.

For v1:
`shoes > sneakers` is the calibrated first subcategory.

Do not add extra visible nav/filter UI unless required and explicitly approved.

## New output rule

Any store calibration implementation must be saved to a new HTML output.

Never overwrite the stable approved source.
