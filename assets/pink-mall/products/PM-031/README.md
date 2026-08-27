# PM-031 — live product media

Colors of California Glossy rainboot · HC.RBGLOW01, colour code **FUX**,
season code F24 · published 2026-08-27

| File | Slot | Source image | View | Native size |
|---|---|---|---|---|
| `PM-031-main.webp` | `media.image` | IMAGE 01 | lateral side profile | 1200×1200 |
| `PM-031-02.webp` | `gallery[0]` | IMAGE 02 | three-quarter front | 1200×1200 |
| `PM-031-03.webp` | `gallery[1]` | IMAGE 03 | inner side, lining visible | 1200×1200 |
| `PM-031-04.webp` | `gallery[2]` | IMAGE 05 | medial side | 1200×1200 |
| `PM-031-05.webp` | `gallery[3]` | IMAGE 04 | heel and back | 1200×1200 |

Filenames are **positional**, not source-numbered: `-02` is gallery position 0.
The approved order is MAIN 01 → 02 → 03 → 05 → 04, and the mapping above is the
whole of that translation. The straight-on back view sits last.

## Conversion

Format conversion only — JPEG → WebP quality 88 at each acquired original's
native 1200×1200. No resize, no crop, no canvas, no upscaling, no generative
edit. The conversion is deterministic: it was re-run from the committed
originals after the working container was recycled and reproduced all five
files byte-for-byte.

`media.fit: 'contain'`. `media.surface: '#FFFFFF'`, the backdrop the pipeline
detected by consensus across the set — these are photographs on white, not
transparent cut-outs, so unlike PM-030 a surface **is** declared.

## Provenance — OFFICIAL manufacturer media

**Source: `hub2.artcrafts.it`.** Fourth product in the catalogue with
manufacturer-tier imagery, after PM-026, PM-029 and PM-030. PM-025, PM-027 and
PM-028 rest on trusted-retailer media.

The tier is a verified claim, not an inference from the hostname. Colors of
California was founded in Florence in 1989 as the sportswear brand of
**Artcrafts International S.p.A.**, which owns and operates it, so this is the
brand owner's own media host — the same standing already accepted for
`images.pepejeans.com` and `nb.scene7.com`.

Asset paths are self-evidencing twice over:

    /_public/resized/1200x1200/HC/F24/FUX/HC.F24.RBGLOW01-FUX-<n>.jpg

Both the article code and the colour code appear in every path, so a candidate
could be neither another product nor the sibling `MUD` colourway.

The colour code resolved itself: fetching the bare product URL redirected to
`?color=FUX`, so the source selected the colourway rather than the pipeline
guessing at it.

| Source image | SHA-256 of original |
|---|---|
| IMAGE 01 | `e8b2cb59f77350535b4b9620a35bb5e1bfdba26836f773c4344ed435c3ee61fa` |
| IMAGE 02 | `039078f3e85d04f3f731055272032134eee801bb056f1087add103e53c5d8892` |
| IMAGE 03 | `83147aa9fd6e05f9b27bbc3ffc816ca0a5abc67207bbc7431bab03c6f7f47d3b` |
| IMAGE 04 | `92a03de1e9f2a90fafb87176467f5c034359aeb5dafd48dcfee384f68f4a1333` |
| IMAGE 05 | `2e7b67682f450e841b2d83064a35acdd67a5f0dbb4d5dca2e360316692533691` |

| Live file | SHA-256 |
|---|---|
| `PM-031-main.webp` | `2e60bf9339b48a3f44708c663422f5620dc4a4cb30eb2d4bc562e66490e8572e` |
| `PM-031-02.webp` | `e82431a409cb68d38005e6547063708705d1c027e67ce2e427233709a59e2082` |
| `PM-031-03.webp` | `21de22ebbe3f3b48ee21597188b09fe8f5bfdbeca4e0b97027450643c09876bc` |
| `PM-031-04.webp` | `d779a1ccc463f55d0432bbf1360d1efa62278b53f6addab67baa7688467eeebc` |
| `PM-031-05.webp` | `28b272be761589a31a58ac0f54272a2be27a09919fc36fdaff88a335cb2de8d9` |

The live hashes are also the identity the regression suite checks against, so a
frame that silently changed would fail the run rather than pass unnoticed.

Full per-image provenance is in
`docs/pink-mall/media-acquisition/HC.RBGLOW01/result.json`; the untouched
originals are committed beside it in `source/`.

Regenerate from `source/`; never overwrite the originals.

## Resolution

1200×1200 is above the project's 1000 px preference and below its 1600 px
ideal. That is what the source serves for this article — the page also declares
400×570 and 220×200, both smaller. Nothing was upscaled to close the gap.

## Not published on this product

- **Material / composition** — omitted. The boot is plainly a moulded
  rubber-type material and the brand's own category is "rain boots", but the
  pipeline never extracted a composition string from the page it read, so no
  material row is rendered. The word "гумени" in the alt text describes what is
  visible in the photograph; it is not a published composition claim.
- **Supplier stock state** — not used as PINK MALL availability. All five
  supplied sizes are listed available and no sold-out ladder is asserted,
  because the exact size run was never proven (`SIZE_SCALE_NOT_PROVEN`).
