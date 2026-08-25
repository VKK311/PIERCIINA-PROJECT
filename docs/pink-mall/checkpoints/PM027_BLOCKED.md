# PINK MALL — PM-027 (JR5952) — MEDIA ACQUISITION BLOCKED

**STATUS: BLOCKED — identity resolved, media unavailable. Not published.**

---

## 1. Identity — resolved

| | |
|---|---|
| Brand | **adidas** |
| Model | Gazelle Bold Shoes |
| Manufacturer item | JR5952 |
| Colour | Pink |
| Category | SHOES > Sneakers |
| Official page | `https://www.adidas.com/us/gazelle-bold-shoes-kids/JR5952.html` |
| Proposed Mall ID | PM-027 |
| Price | €59 |

**One correction to the input.** You gave the brand as *Gazelle Bold*. That is
adidas's model name, not a brand — `JR5952` resolves to **adidas** Gazelle Bold
Shoes in Pink. Recorded as brand `adidas`, model `Gazelle Bold Shoes`.

Neighbouring SKUs are different colourways and must not be substituted:
`JR5951` Blue, `JR5953` Burgundy.

adidas's own copy describes a smooth leather upper with suede accents. That is
model-level marketing copy rather than a confirmed composition field, so it is
not treated as material.

The manufacturer classifies this as a juniors series item. Internal only.

## 2. Sizes — no blocker

Supplied: `36, 37 1/3, 38, 38 2/3`. All are exact values on adidas's fractional
EU scale, so nothing needs normalising and nothing is blocked. Under the
ladder-evidence rule the published ladder would carry these four only, since the
exact-model size run cannot be read from a page that will not load.

## 3. Media — BLOCKED

Zero candidates discovered. Zero images acquired. Every route in the approved
source hierarchy was tried and failed.

| Tier | Route | Result |
|---|---|---|
| 1–3 official storefront | `adidas.com/us/gazelle-bold-shoes-kids/JR5952.html` | `403 Forbidden` |
| | `adidas.de/en/JR5952.html` | read timeout |
| | `adidas.com/us/JR5952.html` | `403 Forbidden` |
| | `adidas.co.uk/JR5952.html` | read timeout |
| official product API | `adidas.com/api/products/JR5952` | `403 Forbidden` |
| | `adidas.de/api/products/JR5952` | `403 Forbidden` |
| 4 official CDN | `assets.adidas.com` | not addressable — adidas asset paths carry an opaque hash, so they cannot be derived from the SKU, and none were discovered to follow |
| 5 trusted retailer, exact SKU | searched | none found carrying `JR5952` |

The only non-adidas sources carrying anything similar are resell marketplaces
(StockX, Limited Resell). The skill excludes marketplaces as primary media
sources, and in any case those listings are for **different** SKUs — `IE0420`,
`ID6997`, `H06125` — not `JR5952`.

**Why JR5952 blocks where GC515KI succeeded.** New Balance publishes on Scene7
under the style code itself, so the CDN was addressable directly from the SKU
without ever loading a page. adidas hashes its asset paths, so the only way to
learn them is to read a page or API — and adidas refuses the runner on all of
them. This is a structural difference between the two brands, not a transient
failure.

## 4. What would unblock this

Any one of these is enough:

1. **Image files** for JR5952 in Pink — attach 3–5 and the rest of the pipeline
   runs unchanged.
2. **Official asset URLs** from `assets.adidas.com` — copied from the product
   page in a normal browser. Paste them and the automation downloads,
   validates, deduplicates and builds the contact sheet as usual.
3. **A trusted retailer page** that carries exactly `JR5952`, if you know one.

Nothing has been invented, substituted or approximated in the meantime.
