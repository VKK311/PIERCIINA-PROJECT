---
name: pink-mall-product-onboarding
description: Safely research, verify, stage, approve, publish, and update real PINK MALL products from four user-supplied facts: brand/manufacturer, manufacturer item number, PINK MALL price, and available sizes. Use for new product onboarding, product updates, availability refreshes, media refreshes, and batch imports. The skill is universal for PINK MALL; SHOES > Sneakers is the first fully calibrated product type.
---

# PINK MALL Product Onboarding

## Mission

Make real-product onboarding extremely lightweight for the user while keeping product identity, price, availability, sizing, photography, and publishing safe.

The standard user input is only:

`BRAND / MANUFACTURER ITEM NUMBER / OUR PRICE / AVAILABLE SIZES`

Example:

`adidas / JQ4556 / 54 EUR / 36, 37 1/3, 38 2/3, 40`

If one specific size has only one unit:

`adidas / JQ4556 / 54 EUR / 36, 37 1/3 - 1 бр., 38 2/3, 40`

Do not require the user to supply product name, category, color, material, images, Mall ID, tags, NEW status, or product description.

## Read before acting

Read these references before processing a real product:

1. `references/00-locked-behavior.md`
2. `references/01-product-contract.md`
3. `references/02-sourcing-and-identity.md`
4. `references/03-media-policy.md`
5. `references/04-inventory-and-sizing.md`
6. `references/05-taxonomy-copy-new.md`
7. `references/06-approval-publishing.md`
8. `references/07-store-calibration.md`
9. `references/08-manufacturer-registry.md`

For the first calibrated example, also read:

`examples/adidas-JQ4556-pilot.md`

## Core truth hierarchy

1. User-supplied PINK MALL price is the only price source of truth.
2. User-supplied available sizes are the only availability source of truth.
3. Exact manufacturer identity and factual product attributes come from reliable external sources.
4. Never invent missing commercial or product facts.
5. Never publish a new product or commercial/media change without explicit approval.

## Public child-series suppression

A product may originate from a manufacturer child/junior/kids series.

This classification may be used internally only when needed for:
- exact source validation;
- official size-scale validation;
- conversion/QA.

Never expose child-series markers publicly.

Do not use public terms such as:
- Kids
- Junior
- Juniors
- JR
- Boys
- Girls
- child
- children
- teens

Do not place them in:
- product name;
- Mall copy;
- visible category/subcategory;
- search tags;
- image alt text;
- public badges;
- customer-facing metadata.

Also do not make the opposite unsupported claim that the product is adult/unisex if the source does not establish it.

## Standard workflow

### 1. Parse
Parse the four user fields exactly.

### 2. Detect CREATE vs UPDATE
If the same manufacturer item number already exists in PINK MALL:
- treat as UPDATE;
- preserve the same `PM-###`;
- show a short diff-based UPDATE PREVIEW.

Otherwise:
- propose the next free `PM-###`;
- the proposed ID becomes allocated only after approval/publish.

### 3. Research
Use the locked source hierarchy and exact-match gates.

### 4. Validate identity and variant
Require exact manufacturer item number and exact variant/color.

### 5. Validate sizes
Use official EU size information and the category-specific sizing rules.
Never silently normalize a user size.

### 6. Build photographic set
Prepare 3–5 unique, high-quality, product-only canonical images.
Create a visual contact sheet.
Propose one clean product shot as MAIN.

Do not ask the user to download, rename or upload images. Use the media
acquisition layer:

1. Write `docs/pink-mall/media-requests/<SKU>.request.json` from the researched
   identity — brand, item number, variant, official page, candidate seeds.
2. Commit and push to the development branch. The push triggers acquisition on
   a hosted runner, because the execution container cannot reach brand CDNs.
3. Pull, then read `docs/pink-mall/media-acquisition/<SKU>/result.json`.
4. `PASS` → visually confirm exact variant and view roles against the contact
   sheet, then continue. `PARTIAL` / `BLOCKED` → read the log and report the
   blocker. Manual upload is the fallback, never the first move.

The layer acquires and validates bytes. It does not decide product identity,
variant, or MAIN — those remain judgement calls made here, and publication
still requires explicit user approval.

See `docs/pink-mall/MEDIA_ACQUISITION.md` for request and result formats.

### 7. Normalize product content
Prepare:
- brand;
- exact public model name;
- category/subcategory;
- simplified confirmed color;
- simplified confirmed material;
- PINK MALL price;
- public sizes/status;
- short Mall copy;
- internal search tags;
- proposed Mall ID;
- NEW status logic.

### 8. Return one workflow status
Only:
- `READY FOR APPROVAL`
- `BLOCKED`
- `UNRESOLVED`

### 9. Approval-first
Do not publish until the user explicitly approves.

### 10. Publish safely
After approval:
- create a NEW output from the latest approved Mall source;
- never overwrite the stable baseline;
- store canonical images locally;
- validate the live result;
- regenerate the portable review artifact
  (`python tools/build_standalone_review.py`) and verify it from an empty
  directory — production verification is not review verification;
- report `PUBLISHED` only after BOTH pass.

## Universal skill / calibrated scope

This is one universal PINK MALL onboarding skill.

The first fully calibrated category-specific implementation is:

`SHOES > Sneakers`

Do not create separate skills per category.

Future category-specific rules should be added inside this skill for:
- Clothing
- Bags
- Accessories
- Home
- Candles
- other approved subcategories.

## Never do these

- Never use manufacturer/retailer price as PINK MALL price.
- Never use manufacturer/retailer stock as PINK MALL availability.
- Never guess a size conversion.
- Never substitute a similar SKU or colorway.
- Never create a new category/subcategory without approval.
- Never choose INA'S PICKS / SIS' FAVES unless the user explicitly tells you.
- Never generatively alter a canonical product image.
- Never use foreign human models in the canonical product gallery.
- Never hotlink live product images after approval.
- Never silently replace a live photo set.
- Never publish directly into the stable baseline.
- Never announce `PUBLISHED` before post-publish validation passes.
- Never start Final Release Audit as part of a product onboarding task unless explicitly instructed.
- Never commit, push, merge, or create a pull request unless explicitly instructed.
