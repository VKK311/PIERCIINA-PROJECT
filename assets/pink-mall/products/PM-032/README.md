# PM-032 — live product media

Scotch & Soda 27733247 · published 2026-08-27

| File | Slot | Source image | View | Native size |
|---|---|---|---|---|
| `PM-032-main.webp` | `media.image` | IMAGE 01 | three-quarter front, pair | 480×720 |
| `PM-032-02.webp` | `gallery[0]` | IMAGE 02 | top-down, upper and branding | 480×720 |
| `PM-032-03.webp` | `gallery[1]` | IMAGE 03 | head-on front, toe and sole | 480×720 |

## These photographs came from the owner, not from a supply chain

This is the first PINK MALL product whose media did not come through the
acquisition pipeline. Four runner passes were walled by commercial bot
protection — eMAG answers HTTP 511 (Network Authentication Required) and the
MODIVO group answers 404 to automated clients on pages that demonstrably
exist — so the owner supplied the three photographs directly.

No bypass was built for either wall, and none should be: a 511 is the site
stating that automated access is not permitted, and defeating it would be
circumventing an access control rather than solving discovery.

**Provenance is therefore `USER_SUPPLIED`, not manufacturer or retailer CDN.**
There is no source URL behind these files. That is a weaker provenance claim
than PM-026, PM-029, PM-030 or PM-031 carry, and it should not be described as
official brand media.

Validation that *was* possible, and passed: three unique shots by perceptual
hash (pairwise distance 103–142, where duplicates score ≤4), aspect 1.5 inside
the 2.2 shape limit, product-only with no people, and no cut-out alpha.

## Resolution — the known weakness

Native **480 × 720**, the lowest-resolution media in the catalogue. Measured
against the storefront's real render boxes:

| Context | Needs | Have | Short by |
|---|---|---|---|
| Card, desktop @2x | 496 px | 480 | ~0% |
| Card, phone @3x | 594 px | 480 | 19% |
| PDP hero, desktop @2x | 752 px | 480 | 36% |
| PDP hero, phone @3x | 1044 px | 480 | 54% |

Cards are fine; the PDP hero is soft, most of all on phones. This was approved
with the shortfall stated rather than hidden.

**Nothing was upscaled.** No AI enlargement, no sharpening, no generative edit.
The rule against those does not bend because a source is small — an upscale
would invent detail the photograph never had. If larger files ever arrive,
regenerate from them; that single change fixes the biggest weakness here.

## Conversion

Format conversion only — JPEG → WebP quality 88 at each original's native
480×720. No resize, no crop, no canvas.

`media.fit: 'contain'`. `media.surface: '#D2D5D7'`.

That surface is measured, not chosen: the studio backdrop is a grey **gradient**
sweep rather than a flat colour, so `backdrop()` correctly derived nothing.
`#D2D5D7` is the median border tone across all three frames. Without it the
Mall's own neutral `#EDEFF0` — appreciably lighter, luminance ~238 against the
photographs' ~207–220 — would have drawn a bright rectangle around every image.

| Source image | SHA-256 of original |
|---|---|
| IMAGE 01 | `97597171d7edb62aa24e0b240e4952136f0ae7f503cd2bac881d23b0c83fa63f` |
| IMAGE 02 | `385fc75ff6d9591cd7e141cb0ff025ff1c09ca7df87267d53ac896ab7df10745` |
| IMAGE 03 | `1dd0b4d0daedad6aaf469e86f97067a9de7b4b240e713f6cd004c1056732b30a` |

| Live file | SHA-256 |
|---|---|
| `PM-032-main.webp` | `4db9ba476c6ac02382972b77462ea876651ef2cb6178615529f62fc33cd900d7` |
| `PM-032-02.webp` | `fa66c58c9fee14ed31d075c1327b4b08a5aa9d24b2431d712cfe32db64b300f2` |
| `PM-032-03.webp` | `07d1dc2c5cad68dfdc69b84c05c5d4f132ac947bad03c369e7d2d5929609a3d1` |

Originals are committed untouched in
`docs/pink-mall/media-acquisition/27733247/source/`. Regenerate from there;
never overwrite them.

## What this set lacks

**No side profile and no heel view.** PM-025 through PM-031 all lead with a
lateral shot; this set has none, so MAIN is the three-quarter pair — the only
frame showing the whole shoe near profile. Three images is also the media
policy's minimum, so no frame can be dropped without falling below it.

## Identity — what is and is not established

**Brand is confirmed from the product itself.** The tongue patch reads
`SCOTCH & SODA` and the insole carries the circular `SCOTCH & SODA AMSTERDAM`
monogram, both legible under magnification.

**The model name is not.** "Celest" comes from the owner, who knows their own
stock, and nothing reached in five passes names this article. Two facts point
mildly the other way and are recorded so nobody later mistakes the name for
sourced truth:

- The supplier titles this article only "Спортни обувки с велур", with no
  model, while naming models for other Scotch & Soda shoes it lists
  (`Кецове Sylvie`, `Спортни обувки Vivi`).
- Every Celest listing found is multicolour — Candy Pink Multi, Camel/Black,
  Cream/Yellow, Coral Multi, Off-White Multi — whereas this shoe is monochrome
  pale pink.

**The colour codes disagree**: the brief says `34A`, the supplier URL says
`S059`. Both agree the shoe is pink and the article number anchors it. The code
is internal; the public colour reads `Pink`.

## Not published on this product

- **Material / composition** — omitted. The supplier's URL slug says "велур"
  and the brand describes this line as cow suede with nylon panels, but no
  composition string was read from a page, and suede versus synthetic suede is
  not something a photograph settles. Unlike PM-031, where "гумени" described
  an unmistakable moulded rubber boot, the material word was kept out of the
  alt text too.
- **Size 41** — the owner holds it and it is real for this model, but the
  Mall's public ladder stops at EU 40 and the owner chose to keep that cap, so
  the size is not offered.
