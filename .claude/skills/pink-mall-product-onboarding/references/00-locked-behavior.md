# Locked PINK MALL Product-Onboarding Behavior

Status: FINAL INTERVIEW LOCK
Date: 2026-08-24

This file is the compact source of truth for the product-onboarding decisions confirmed with the user.

## Input

The only required user facts for a normal product are:

1. Brand / Manufacturer
2. Manufacturer Item Number
3. Our Price
4. Available Sizes

Optional:
- `1 бр.` on a specific size;
- sister selection if explicitly desired;
- product-specific delivery override if explicitly desired;
- other notes.

## Claude prepares

Claude prepares only what PINK MALL needs:

- exact public model name;
- category/subcategory;
- color;
- material;
- canonical photos;
- photo order;
- Mall Product ID;
- internal search tags;
- NEW status;
- short playful Mall description.

Do not bloat the public product record with unnecessary source details.

## Child-series rule

Never publicly mention that a product belongs to a child/kids/junior series.

Internal use is allowed only for source identity, size-scale validation, and QA.

No public `kids`, `junior`, `JR`, `girls`, `boys`, etc. in name, copy, tags, alt text, categories, or badges.

## Sources

Priority:
1. EU/European official storefront
2. global official brand site
3. other official regional storefront
4. trusted distributor/retailer fallback

Prefer official manufacturer CDN/media assets for images.

Random shops, marketplaces, eBay, Pinterest, and social posts are never primary sources.

If exact SKU/variant cannot be established:
- do not guess;
- use `UNRESOLVED`;
- request the smallest extra input.

## Product identity

Strict:
- exact Manufacturer Item Number;
- exact variant/color;
- no similar SKU;
- no other colorway;
- no season/version substitution.

If the official page is gone, a trusted retailer/distributor may be used only with exact SKU + exact variant/color.

## Pricing

User price is absolute source of truth.

Never import:
- MSRP;
- current manufacturer price;
- retailer price;
- sale price;
- discount percentage.

No SALE/old price unless user explicitly supplies it.

## Availability

User availability is absolute source of truth.

External stock is ignored.

Default mode:
`availability-only`

User-listed sizes = available.
Allowed official sizes not supplied by user = sold out.

Never invent quantity.

If user says one specific size has `1 бр.`:
- mark only that size `ПОСЛЕДНА БРОЙКА`;
- do not infer counts for other sizes;
- do not create a general product-level last/limited badge from that one size.

## Shoes sizing

Public sizing = EU only.

For shoes:
- public Mall range is EU 36 through EU 40 inclusive;
- use the exact official size scale for the exact model;
- fractional sizes inside the range are valid and visible;
- sizes below 36 or above 40 are not added to the Mall;
- in-range official sizes not supplied by the user are visible as `ИЗЧЕРПАН`.

Strict mismatch rule:
- user `37` vs official `37 1/3` => BLOCKED;
- never normalize automatically.

If only UK/US data is available, use an official brand conversion source.
If conversion is not unambiguous:
`SIZE CONFIRMATION REQUIRED`.

## Photography

Canonical gallery:
- minimum 3;
- maximum 5;
- unique high-quality images;
- product-only;
- no foreign people/models.

Lifestyle is allowed only when:
- there are no people;
- exact product is clear;
- it is secondary, never MAIN.

MAIN:
- clean product shot;
- Claude proposes it;
- user may change it before approval.

Claude orders secondary photos autonomously.

If source set is weak:
- continue through trusted exact-match source hierarchy;
- mix sources only if exact SKU/variant matches;
- show source per image;
- deduplicate visually;
- keep the highest-quality duplicate;
- if fewer than 3 usable unique images remain => `PHOTO SET INCOMPLETE`.

Canonical product fidelity is strict:
- no generative product edits;
- no color/shape/logo/print/hardware/proportion changes.

Future creative images may use INA/SIS Digital Twins after their exact avatars are locked, while preserving product fidelity.

## Media storage

Before approval:
- stage assets outside live product assets.

After approval:
- download/store locally;
- never hotlink live images;
- product folder by `PM-###`;
- preserve untouched originals in `/source/`;
- optimized Mall files are separate;
- original files are never overwritten.

Technical image processing may be automatic:
- WebP live format;
- resize;
- compression without visible loss;
- safe crop;
- thumbnails/variants as needed.

Card:
- standardized 3:4.

PDP:
- fidelity-first framing;
- do not force crop;
- add breathing space rather than cutting the product.

Generate factual per-image alt text automatically.

## Media-use operating rule

If exact-match images come from:
- official brand site/CDN;
- official distributor;
- trusted retailer;

they may be used in the workflow unless the source explicitly prohibits it.

This is an operational workflow rule, not a legal guarantee.

## Naming / color / material

Product name:
- preserve official model name;
- strip public age-series markers;
- do not invent a new marketing name;
- brand is stored separately.

COLOR:
- English terms are allowed;
- may simplify long manufacturer color names;
- never invent or flatten a materially important nuance.

MATERIAL:
- English terms are allowed;
- may simplify for readability;
- preserve meaningful specificity such as `100% Cotton`, `Sterling Silver`, `Soy Wax`, `Genuine Leather`.

Missing secondary field:
- do not block;
- do not infer visually;
- hide/omit the unconfirmed field;
- show `not confirmed` in approval preview.

## Copy

Short product copy:
- 1–2 short sentences;
- primarily Bulgarian;
- controlled English slang allowed;
- playful/strange PINK MALL tone;
- only confirmed product facts;
- no invented fit, comfort, performance, care, or functional claims.

## Search tags

Claude generates internal search tags automatically.

Tags:
- are not publicly displayed;
- use only confirmed facts;
- never include child-series markers.

## NEW

A first-time published product is NEW for 14 days from first publication in PINK MALL.

NEW means new to PINK MALL, not a new manufacturer collection.

Do not restart NEW automatically when an old product is reactivated.

## Sister selection

Claude never chooses INA/SIS/BOTH.

Default:
`selectedBy:null`

Only user instruction may change it.

## Taxonomy

Use only approved PINK MALL taxonomy.

Do not create categories/subcategories automatically.

If main category fits but required subcategory does not exist:
- continue preparing the product;
- mark `TAXONOMY APPROVAL REQUIRED`;
- propose `SUGGESTED SUBCATEGORY`;
- do not publish until approved.

For v1 of this skill:
`SHOES > Sneakers` is the first approved/calibrated product type.

## Delivery

Global PINK MALL delivery estimate:
`4–7 работни дни`

Store/render it globally.

Do not duplicate it in every product object.

A product may override only if the user explicitly supplies another delivery estimate.

## IDs

Mall Product ID:
- permanent sequential `PM-###`;
- next free ID for new products;
- Manufacturer Item Number stored separately;
- no published/archived Mall ID is ever reused;
- reactivation preserves the same ID.

## Existing SKU updates

Same Manufacturer Item Number = UPDATE, not duplicate product.

Preserve:
- same PM ID;
- no automatic NEW restart.

Allowed proposed updates:
- price;
- available/sold-out sizes;
- size-specific last piece when supplied;
- improved exact-match photo set;
- better-confirmed color/material;
- search tags;
- short Mall copy.

Do not silently change:
- product name;
- category;
- Manufacturer Item Number.

If one appears wrong:
- BLOCK update;
- request confirmation.

Update preview is diff-based and short.

Media refresh:
- never automatic on live product;
- show old vs proposed set;
- require APPROVE.

## Sold out / archived

Temporarily fully sold out:
- remains public;
- same PM ID;
- all variants disabled;
- order CTA unavailable;
- sorts below available products.

Permanently discontinued:
- mark internal `ARCHIVED`;
- remove from public Mall/search/category/wishlist results;
- keep PM ID, images, source metadata;
- may later reactivate with same ID.

Do not maintain a separate per-product change log.

## Approval

Approval-first is mandatory.

Standard approval preview:
- STATUS;
- Brand;
- Model;
- Manufacturer Item;
- Mall ID;
- Category;
- Color;
- Material;
- Price;
- full relevant size scale and availability state;
- NEW;
- short Mall copy;
- visual contact sheet;
- proposed MAIN;
- source status;
- only relevant warnings/blockers.

No unnecessary technical dump.

Batch approvals are allowed:
- `APPROVE ALL`
- `APPROVE PM-041, PM-043`
- `REJECT PM-042`
- `CHANGE PM-044 MAIN TO IMAGE 03`

Only approved products publish.

## Statuses

Only:
- `READY FOR APPROVAL`
- `BLOCKED`
- `UNRESOLVED`

Typical blockers:
- `SIZE CONFIRMATION REQUIRED`
- `PHOTO SET INCOMPLETE`
- `TAXONOMY APPROVAL REQUIRED`
- `VARIANT MATCH BLOCKED`

## Publishing

Never overwrite the stable approved HTML directly.

Always:
1. take latest approved source;
2. create a new output;
3. apply only approved changes;
4. validate;
5. promote only after PASS.

Previous source remains rollback baseline.

After APPROVE, validate:
- product card;
- PDP;
- sizes/states;
- price;
- NEW;
- images;
- search;
- category;
- mobile layout;
- browser console;
- no unrelated regression.

Return `PUBLISHED` only after PASS.

If a technical issue occurs, Claude may self-fix without reapproval only when it does not change approved commercial/media data.

Technical self-fix examples:
- image path/filename;
- card/PDP layout;
- search indexing;
- mobile overflow;
- alt text wiring;
- technical NEW badge issue.

Require new APPROVE if fixing would change:
- price;
- sizes;
- photo set;
- MAIN;
- category;
- product name;
- variant.
