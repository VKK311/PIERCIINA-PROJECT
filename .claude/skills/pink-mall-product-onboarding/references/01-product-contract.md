# Product Contract

## Required user input

Exactly four required commercial fields:

```text
brand/manufacturer
manufacturer item number
PINK MALL price in EUR
available sizes
```

Accepted daily format:

```text
adidas / JQ4556 / 54 EUR / 36, 37 1/3, 38 2/3, 40
```

Optional size-specific scarcity:

```text
adidas / JQ4556 / 54 EUR / 36, 37 1/3 - 1 бр., 38 2/3, 40
```

Do not require category, name, color, material, photos, tags, Mall ID, sister selection, or NEW status.

## Customer-facing real-product fields

Prepare only the useful fields:

- Brand
- Model name
- Category/subcategory
- Color if confirmed
- Material if confirmed
- Price EUR
- Size choices/status
- Short PINK MALL description
- 3–5 canonical images
- Mall Product ID
- NEW badge/status

Internal:
- manufacturer item number
- search tags
- source provenance
- source URLs
- source image provenance
- inventory mode
- publish/new expiry metadata

## Backward-compatible catalog shape

The current PINK MALL catalog may have legacy demo fields.

For a real product, adapt the current schema minimally and backwards-compatibly.

Preferred conceptual fields:

```js
{
  id: 'PM-025',
  brand: 'adidas',
  manufacturerItemNo: 'JQ4556',

  name: 'VL Court Bold Shoes',
  slug: 'adidas-vl-court-bold-shoes',

  category: 'shoes',
  subcategory: 'sneakers',

  color: 'Pink / Silver / Gold',
  composition: 'Leather / Textile / Rubber',

  priceEUR: 54,
  oldPriceEUR: null,

  description: '...',
  selectedBy: null,

  tags: ['adidas', 'vl court bold', 'sneakers', 'pink', 'leather'],

  featured: false,
  campaign: null,

  // for new real products:
  newUntil: 'YYYY-MM-DD',

  inventoryMode: 'availability',
  availability: {
    '36': 'available',
    '36 2/3': 'soldout',
    '37 1/3': 'available',
    '38': 'soldout',
    '38 2/3': 'available',
    '39 1/3': 'soldout',
    '40': 'available'
  },

  media: {
    image: 'assets/pink-mall/products/PM-025/PM-025-main.webp',
    imageAlt: '...',
    gallery: [
      'assets/pink-mall/products/PM-025/PM-025-02.webp',
      'assets/pink-mall/products/PM-025/PM-025-03.webp'
    ],
    galleryAlt: [
      '...',
      '...'
    ]
  },

  source: {
    manufacturerUrl: '...',
    verifiedAt: 'YYYY-MM-DD'
  }
}
```

This is a conceptual target, not permission to replace current architecture wholesale.

If the live source uses a different compatible representation:
- preserve the existing architecture;
- add the smallest truthful extension.

## Optional fields

If color or material is not confirmed:
- do not invent;
- leave null/omit;
- customer UI should hide it.

Do not invent fit/care/details merely because the legacy demo schema has them.

If the current PDP hard-renders unconfirmed legacy fields, calibrate it so optional fields can be omitted safely.

## Brand and model name

Store brand separately.

Public model name:
- preserve official model name;
- remove age-series markers only;
- do not invent a marketing replacement.

## Price / sale

`priceEUR` is exactly user supplied.

`oldPriceEUR:null` unless user explicitly supplies sale/old-price data.

Do not infer a SALE state from manufacturer/retailer promotions.

## Search

Search should include confirmed brand + model + internal tags.

Internal search tags are not a public product spec.

## NEW implementation

Real product NEW should be date-based.

Preferred behavior:
- on first approved publish, compute `newUntil = publication date + 14 days`;
- use one central helper to determine whether NEW is active;
- preserve legacy demo `isNew` behavior as fallback if required;
- do not require manual edit after 14 days.

Do not mark a staged/unpublished product NEW merely because research happened.
