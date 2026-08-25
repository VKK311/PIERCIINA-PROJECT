# PM-025 — live product media

adidas VL Court Bold Shoes · JQ4556 · published 2026-08-25

| File | Slot | Source image | View |
|---|---|---|---|
| `PM-025-main.webp` | `media.image` | IMAGE 01 | lateral side profile |
| `PM-025-02.webp` | `gallery[0]` | IMAGE 04 | three-quarter front angle |
| `PM-025-03.webp` | `gallery[1]` | IMAGE 02 | top-down |
| `PM-025-04.webp` | `gallery[2]` | IMAGE 03 | outsole |

All four are 1440×1920 (3:4) WebP, quality 88.

## Why 3:4 and not the original square

The card is `aspect-ratio: 3/4` and the PDP is `4/5`, both with
`object-fit: cover`. Feeding a square 1880×1880 source into those containers
would crop 25% off each side of the card — cutting the toe and heel off the
lateral shot.

So each live file is the 1880×1880 original composited onto a 3:4 canvas at 96%
of frame width, on `rgb(234,238,239)` — the exact studio background of the
source images, so the extension is seamless. The card then crops nothing, and
the PDP crops 6.2% of height from a frame where the product occupies the middle
72%. The product is never cut.

This is the skill's "add breathing space rather than aggressive crop", applied
at asset-generation time so no site CSS had to change.

## Originals

Not duplicated here. The untouched 1880×1880 originals are preserved, committed
and hash-recorded in two places:

- `docs/pink-mall/approval-media/PM-025/source/` — the approved package
- `docs/pink-mall/media-acquisition/JQ4556/source/` — as acquired, with full
  provenance in the sibling `result.json`

| Source image | SHA-256 |
|---|---|
| IMAGE 01 | `cd35da4bc75864eb854c1735d69ef07c2fbf1a4d6335e975c3fef6be67fad7f4` |
| IMAGE 02 | `0a0270dc1c9f63a5526c16db855c8d99c52774ebd80092476cd88505ad5bc96d` |
| IMAGE 03 | `656cd37b2912f1a35136cc9c1dfa2685f9a9e3cba71ebf776052bba645be1bfb` |
| IMAGE 04 | `d7cb5f1b4a8eb723e937bf765a574e7c45c9f88340f6e65c07d8928f3b328f94` |

The skill's post-approval layout puts a `source/` copy beside the live files.
A third committed copy of the same bytes adds no protection here — both existing
copies are in git with hashes — so this README records the location instead.
Regenerate the live WebP from either path; never overwrite the originals.
