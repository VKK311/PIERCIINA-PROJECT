# Approval and Publishing Workflow

## Three workflow statuses

Only use:

### READY FOR APPROVAL
All critical requirements pass.

### BLOCKED
Product identity is known, but a specific decision/confirmation is required.

Examples:
- `SIZE CONFIRMATION REQUIRED`
- `PHOTO SET INCOMPLETE`
- `TAXONOMY APPROVAL REQUIRED`
- `VARIANT MATCH BLOCKED`

### UNRESOLVED
Exact product/variant cannot be reliably identified.

Ask for the minimum additional user input.

## Approval-first

Never publish:
- a new product;
- a commercial change;
- a photo-set change;
- a MAIN change;

without explicit approval.

## Standard CREATE approval preview

Keep it concise and visual:

```text
STATUS:
READY FOR APPROVAL | BLOCKED | UNRESOLVED

BRAND:
...

MODEL:
...

MANUFACTURER ITEM:
...

MALL ID:
...

CATEGORY:
...

COLOR:
... | not confirmed

MATERIAL:
... | not confirmed

PRICE:
€...

SIZES:
36 — available
36 2/3 — sold out
...

NEW:
YES — 14 days from first publish

SHORT MALL COPY:
...

PHOTO MATERIAL:
[visual contact sheet: 3–5 images]

MAIN:
image 01

SOURCE STATUS:
exact manufacturer match | trusted retailer fallback

WARNINGS:
only actual blockers/warnings
```

Do not dump implementation internals into normal approval.

## Photo approval

Contact sheet is mandatory.

User may say:
- `APPROVE`
- `CHANGE MAIN TO IMAGE 03`
- request photo removal/reorder.

Claude proposes MAIN but user has final authority.

## Batch

Each product gets its own preview.

Allowed:
- `APPROVE ALL`
- `APPROVE PM-041, PM-043`
- `REJECT PM-042`
- `CHANGE PM-044 MAIN TO IMAGE 03`

Publish only approved products.

## Existing SKU update

Same Manufacturer Item Number => UPDATE.

Standard UPDATE PREVIEW is diff-based.

Example:

```text
UPDATE PREVIEW

PM-041
VL Court Bold Shoes

PRICE
€54 → €49

SIZES
36: available → sold out
38 2/3: sold out → available

MEDIA
No change proposed

NEW
No change

READY FOR APPROVAL
```

Do not repeat full product data unless necessary.

## Media refresh

If better exact-match images are found for a live product:
- show current photo set;
- show proposed photo set;
- identify proposed MAIN change;
- require approval.

Never silently refresh live product photography.

## Publishing output safety

Never modify the stable baseline in place.

For each approved publish/batch:

1. locate latest approved Mall source;
2. create a new output file;
3. apply only approved changes;
4. keep prior source untouched;
5. run validation;
6. only after PASS may the new file become the working version.

Use clear output naming, e.g.:

`PINKMALL_CATALOG_UPDATE_2026-08-24.html`

Avoid collisions by adding a sequence if necessary.

## Post-publish validation

Required:

- Product card renders
- PDP opens
- Price exact
- Brand/model correct
- Size ladder correct
- Available/sold-out/last states correct
- No unsupported stock scarcity badge
- Order CTA disabled for sold-out variant/product
- Viber contract remains unchanged
- Images load from local assets
- MAIN correct
- Gallery works
- Alt text wired
- NEW status correct
- Search finds brand/model/tags
- Category/subcategory state correct
- Sold-out sorting preserved
- Mobile layout no overflow/collision
- Browser console clean
- Existing products/filters/wishlist unaffected

Only then:

```text
PUBLISHED

PM-...
...
Card: PASS
PDP: PASS
Sizes: PASS
Images: PASS
Search: PASS
Mobile: PASS
```

If not:
`PUBLISH FAILED`

## Technical self-fix vs commercial reapproval

Claude may self-fix:
- path;
- filename;
- layout;
- indexing;
- mobile overflow;
- alt wiring;
- technical NEW logic.

Claude must re-request approval if the fix changes:
- price;
- sizes;
- photo set;
- MAIN;
- category;
- product name;
- variant.

## Archived products

Permanent discontinuation:
- internal `ARCHIVED`;
- hidden from public Mall/search/category/wishlist results;
- PM ID retained;
- media retained;
- source metadata retained;
- may reactivate with same PM ID.

No separate product change log is required.
