# Canonical Product Media Policy

## Canonical gallery standard

Each publishable product needs:

- minimum: 3 unique high-quality images
- maximum: 5 images

If fewer than 3 remain after exact-match validation and deduplication:
`PHOTO SET INCOMPLETE`

## No people in canonical gallery

Canonical product media must be product-only.

Do not use:
- foreign models;
- influencer images;
- on-body/on-foot shots with people;
- manufacturer lifestyle images containing people.

Future creative/on-model work belongs to the separate Creative OS and may use only locked INA/SIS Digital Twins.

## Lifestyle without people

Allowed as secondary gallery media if:
- no people are present;
- exact SKU/variant is clear;
- product is clearly visible;
- scene is not misleading.

Lifestyle/product-only media can never be MAIN.

## MAIN image

MAIN must be:
- clean product shot;
- whole product clearly visible;
- preferably front / 3/4 / side depending on product.

Claude chooses one proposed MAIN.

If two are equally good:
- choose one;
- do not create unnecessary A/B approval.

User may override MAIN before APPROVE.

## Secondary order

Claude chooses the order autonomously based on:
- clarity;
- commercial usefulness;
- complementary views;
- avoiding repetition.

No fixed side/back/detail sequence is required.

## Source mixing

It is allowed to combine media from more than one reliable source when:
- exact Manufacturer Item Number matches;
- exact variant/color matches;
- visual product identity matches;
- each image retains source provenance.

## Weak official photo set

If official source is incomplete:
- continue through locked source hierarchy;
- use only exact-match sources;
- stop if 3 unique high-quality images cannot be established.

## Visual deduplication

If the same image exists from several sources:
- treat as one shot;
- keep highest-quality version;
- do not count duplicates toward the minimum;
- show only unique shots in approval preview.

## Product fidelity

Canonical ecommerce images may not be generatively altered.

Forbidden:
- recolor;
- reshape;
- change logo;
- change print;
- change sole;
- add/remove hardware;
- change stitching;
- change proportions;
- hallucinate another angle;
- remove or add product features.

Allowed technical transformations:
- download;
- safe crop;
- resize;
- compression;
- WebP conversion;
- thumbnails/derivatives;
- adding neutral breathing space when needed.

## Storage lifecycle

### Before APPROVE

Use a staging area outside live product assets, for example:

```text
.pink-mall-staging/JQ4556/
    source/
    preview/
    contact-sheet.webp
```

Do not publish/hotlink remote URLs in the live product object.

### After APPROVE

Use:

```text
assets/pink-mall/products/PM-025/
    source/
        original-01.jpg
        original-02.jpg
        original-03.jpg

    PM-025-main.webp
    PM-025-02.webp
    PM-025-03.webp
```

Rules:
- preserve original downloads untouched in `/source/`;
- never overwrite originals;
- optimized files are separate;
- live Mall uses local paths only;
- retain source URL metadata internally.

## Technical image preset

Live:
- WebP as primary format;
- compression without visible quality loss;
- appropriate responsive dimensions.

Product cards:
- standardized 3:4 framing.

PDP:
- fidelity-first framing;
- preserve near-original composition;
- do not cut important product areas;
- use breathing space instead of aggressive crop.

## Alt text

Generate concise factual alt text per image.

Example:
`Pink adidas VL Court Bold sneakers, side view`

Rules:
- use confirmed facts only;
- identify view where useful;
- no marketing copy;
- no child-series markers;
- different images should have appropriately different alt text.

### Canonical alt schema

Authored alt text is carried by the media object itself:

```js
media: {
  image:      '...',        // MAIN
  imageAlt:   '...',        // alt for MAIN
  gallery:    ['...','...'],
  galleryAlt: ['...','...'] // galleryAlt[n] belongs to gallery[n]
}
```

`imageAlt` belongs to `image`. `galleryAlt[n]` belongs to `gallery[n]`; the
pairing is by index, so a gap in one array must not shift the other.

Do not introduce a different alt field name. See
`references/01-product-contract.md` for the full product shape.

Legacy string-only media carries no authored alt and must keep working: the
renderer falls back to a safe generated alt for those entries.

## Approval contact sheet

Approval preview must include a visual contact sheet showing all proposed 3–5 images.

For each image, identify:
- image number;
- proposed MAIN when applicable;
- view/role;
- source type/domain;
- quality warning if any.

Do not make the user approve a photo set based only on filenames or image count.

## Media-use operating rule

Exact-match product imagery from official brand/CDN, official distributor, or trusted retailer may be used unless the source explicitly prohibits it.

This is an operational workflow assumption, not legal advice or a legal guarantee.
