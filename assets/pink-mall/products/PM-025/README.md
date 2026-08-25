# PM-025 — live product media

adidas VL Court Bold Shoes · JQ4556 · published 2026-08-25

| File | Slot | Source image | View |
|---|---|---|---|
| `PM-025-main.webp` | `media.image` | IMAGE 01 | lateral side profile |
| `PM-025-02.webp` | `gallery[0]` | IMAGE 04 | three-quarter front angle |
| `PM-025-03.webp` | `gallery[1]` | IMAGE 02 | top-down |
| `PM-025-04.webp` | `gallery[2]` | IMAGE 03 | outsole |

All four are 1880×1880 WebP, quality 88 — the official originals at their
native aspect ratio, format-converted only. No resize, no crop, no canvas.

## Fitting is the storefront's job, not the asset's

An earlier revision pre-composited these onto 3:4 canvases to compensate for
`object-fit: cover` on the card and PDP. It worked, but it baked one
storefront's CSS into the product record, and every future SKU would have needed
the same manual preparation.

The product object now declares its presentation policy instead:

```js
media: { fit: 'contain', surface: '#EAEEEF', … }
```

`contain` guarantees the whole product is visible in both the 3:4 card and the
4:5 PDP. `surface` is the studio backdrop of these photographs — detected
automatically during acquisition and reported as `dominantBackdrop` — so the
field behind a contained image matches the photo and shows no seam.

Side by side, the native-source route also displays the product noticeably
larger on the PDP than the pre-framed route did, because no canvas margin is
being carried inside the image.

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
