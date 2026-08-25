# Taxonomy, Copy, Search, NEW, and Sister Selection

## Primary taxonomy

Existing PINK MALL primary categories remain locked:

- NEW IN
- CLOTHING
- BAGS
- SHOES
- ACCESSORIES
- HOME
- CANDLES

Do not create a new top-level category automatically.

## Subcategories

Claude may classify into an already approved subcategory.

Claude may not create a new subcategory autonomously.

If required subcategory is missing:
- continue preparing all other product data/media;
- mark `TAXONOMY APPROVAL REQUIRED`;
- propose `SUGGESTED SUBCATEGORY`;
- do not publish until approved.

## v1 calibrated product type

For this skill version:

`SHOES > Sneakers`

is approved as the first calibrated product type.

This does not authorize arbitrary new shoe subcategories.

## Naming

Store:
- `brand` separately;
- official model name without public age-series markers.

Example:

Manufacturer:
`adidas VL Court Bold Shoes Kids`

Public:
- Brand: `adidas`
- Model: `VL Court Bold Shoes`

Do not invent a new marketing name.

## Color

English color terms are allowed.

Claude may simplify:
`Clear Pink / Silver Metallic / Gold Metallic`
to:
`Pink / Silver / Gold`

But do not flatten a meaningful nuance if it could mislead.

Preserve important tones such as:
- Burgundy
- Cream White
- Dusty Rose

when relevant.

## Material

English terms are allowed.

Claude may simplify:
`Leather upper / textile lining / rubber outsole / synthetic overlays`
to:
`Leather / Textile / Rubber`

Preserve important specificity:
- `100% Cotton`
- `Genuine Leather`
- `Sterling Silver`
- `Soy Wax`

Do not infer material from appearance.

## Missing secondary fields

Color/material missing:
- not a blocker;
- do not invent;
- omit/hide from customer PDP;
- approval preview says `not confirmed`.

## Short Mall copy

Required:
- 1–2 short sentences;
- primarily Bulgarian;
- controlled English slang allowed;
- playful, strange PINK MALL tone;
- factual base only.

Allowed style:
`Pink, chunky and not here to behave.`

Not allowed:
- invented comfort;
- invented performance;
- invented fit;
- invented care;
- invented exclusivity;
- unsupported claims.

## Search tags

Generate automatically.

Internal only.

May include:
- brand;
- model;
- category/subcategory;
- confirmed color;
- confirmed material;
- useful confirmed style term.

Never include:
- kids;
- junior;
- boys;
- girls;
- child-series labels.

## NEW

Definition:
new to PINK MALL.

On first approved publication:
- NEW active for 14 days.

Preferred implementation:
- date-based (`newUntil`);
- one centralized helper;
- no manual catalog cleanup after 14 days.

Reactivation:
- do not restart NEW automatically.

## Sister selection

Claude never chooses.

Default:
`selectedBy:null`

Only explicit user input may set:
- `ina`
- `sis`
- `both`

## SALE

No SALE unless explicitly supplied by the user.

External retail promotions do not create PINK MALL SALE.
