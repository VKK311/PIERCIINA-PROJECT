# adidas JR5952 — MEDIA DISCOVERY BLOCKED

**IDENTITY: RESOLVED. MEDIA: BLOCKED. Not staged, not published.**

| | |
|---|---|
| Brand | adidas |
| Model | Gazelle Bold Shoes |
| Manufacturer item | JR5952 |
| Colourway | Pink / "Almost Pink" |
| Sizes supplied | 36, 37 1/3, 38, 38 2/3 — valid, no size blocker |

## Why blocked

Expanded discovery worked as transport: search-index queries in Polish found
four mainstream retailers carrying the exact SKU in their page URLs — eobuwie,
modivo, shooos, nuumi — and the runner reached all four. 483 raw candidates.

But every image the pipeline accepted was **the wrong colourway**.

The eobuwie/modivo product page for `jr5952-rozowy` serves JSON-LD whose
gallery is a **white-and-green** Gazelle Bold, not the pink JR5952. The page
identifies itself with the right SKU; its declared media does not match its own
product.

Two automated safeguards were added during this pass and neither could save it:

1. **Page-sweep rejection** — correct and necessary, but these images came via
   JSON-LD, an authoritative declaration, not a sweep.
2. **Decorative-slug rejection** — correct and necessary, but it only demoted
   the evidence class; the images still qualified on page evidence.

What caught it, three times out of three, was **looking at the contact sheet**.

## Status, precisely

- `IDENTITY UNRESOLVED` — **no**. Identity is solid.
- `DIRECT SOURCE BLOCKED` — yes for adidas.com and its API, but not terminal.
- `MEDIA DISCOVERY BLOCKED` — **yes**, and this is the state.

adidas hashes its CDN asset paths, so `assets.adidas.com` is not addressable
from the SKU; the official routes all `403`; and the retailer route, though
reachable and exact-SKU, is not variant-faithful for this product.

## What would unblock it

- Official `assets.adidas.com` URLs copied from the product page in a browser, or
- image files for JR5952 in Pink, or
- a retailer page whose declared gallery actually shows the pink colourway.

The false-positive acquisition output has been removed from the repository so it
cannot be mistaken for approved media. The request manifest is withdrawn so the
workflow stops regenerating it.
