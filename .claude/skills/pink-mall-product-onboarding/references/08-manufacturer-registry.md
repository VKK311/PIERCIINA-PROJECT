# Manufacturer Registry

This registry provides preferred official source patterns. It does not replace exact runtime verification.

## Generic default

Source priority:

1. European official storefront
2. global official brand site
3. other official regional storefront
4. trusted distributor/retailer fallback

Media:
- official brand/CDN first;
- trusted exact-match fallback allowed;
- no random marketplace sourcing.

## adidas

Preferred official product source:
- `adidas.de`
- other official European adidas storefronts when appropriate
- `adidas.com` global/official fallback

Preferred official media:
- `assets.adidas.com`

Official size sources:
- official adidas product size guide;
- official adidas footwear/kids/youth size charts when needed for the exact product scale.

Important:
- manufacturer child/youth classification may be used internally for size validation;
- never expose it in PINK MALL public content;
- strict exact Product Code match is required;
- fractional EU sizing must be preserved exactly;
- do not use adidas retail price or adidas availability as PINK MALL truth.
