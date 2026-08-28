# PM-037 — live product media

VEE Collective 134-200-409 · Porter Messenger Mini · Seashell Pink
published 2026-08-28

| File | Slot | Source | View | Native size |
|---|---|---|---|---|
| `PM-037-main.webp` | `media.image` | SUPPLIED 02 | front, whole bag and knotted straps | 1200×1500 |
| `PM-037-02.webp` | `gallery[0]` | SUPPLIED 03 | side profile with strap | 1200×1500 |
| `PM-037-03.webp` | `gallery[1]` | SUPPLIED 01 | open top, zip and lining | 1200×1500 |

Filenames are **positional**. MAIN is the clean front shot — the only frame
showing the whole bag square-on, and the closest match to the retailer's own
catalogue image.

## This product was BLOCKED, and what unblocked it

`134-200-409` stood as **BLOCKED — PHOTO SET INCOMPLETE** with a single unique
exact-SKU image from `tootsies.com`. The media policy needs three. The owner
supplied three photographs, which close the gap.

**Exact-product consistency was checked, not assumed.** All three were compared
against the previously evidenced image: same quilted puffer body, same knotted
padded straps, same pale pink. Perceptual hashing put every pair well apart —
the closest was 57, where a duplicate scores 4 or below — so the set is three
genuinely different views and nothing collapsed on dedupe. Aspect 1.25, inside
the 2.2 shape limit, product-only, no people, no cut-out alpha.

**The evidenced tootsies image is deliberately NOT in the gallery.** It is
1600×1600 (1:1) where the supplied frames are 1200×1500 (4:5), and one gallery
should not mix aspect ratios. It remains on record in
`docs/pink-mall/media-acquisition/134-200-409/`.

## Provenance — identity and media come from different places

| | |
|---|---|
| **Identity** | TRUSTED_RETAILER — `tootsies.com`, exact SKU in the document body, `VARIANT_CONFIDENCE_PASS` |
| **Media** | **USER_SUPPLIED** — the three photographs, no source URL |

The record says so rather than letting the media inherit the retailer tier it
did not come from. Identity established the brand, the model name
`Porter Messenger Mini`, the `Seashell Pink` variant and the `O/S` size scale;
the photographs establish nothing but themselves.

| Live file | SHA-256 |
|---|---|
| `PM-037-main.webp` | `ba3f70df3d152ee9bf6ff3de826fdac61e29678bb4dd108c350ad011de33d972` |
| `PM-037-02.webp` | `0d45f15bf376616f1738075dea8b9d5049de64ef5403aa3b84dfbdcba4c19b1c` |
| `PM-037-03.webp` | `2f383b4b1d05f80d4d51b5df25dc8d77e857b34c7c1f655bab9d848cbeeb51d4` |

Originals are kept untouched in
`docs/pink-mall/media-acquisition/134-200-409/user-supplied/`.

## Conversion — none needed

The supplied files are **already WebP**, so the bytes were copied rather than
re-encoded: a second WebP pass would only have cost quality. No resize, no
crop, no canvas, no upscaling, no generative edit. The live file hashes above
are therefore identical to the originals'.

`media.fit: 'contain'`. `media.surface: '#E8E8E8'`, the measured median border
tone across the three frames. The studio backdrop is a soft gradient rather
than a flat colour, which is why `backdrop()` derived nothing; the measured
median keeps the letterboxed area close to the photograph instead of showing a
lighter band around it.

## Not published on this product

- **Composition** — omitted. No exact-product source states one, the same
  standard applied since PM-026.
- **Dimensions** — omitted, not established.
- **Retailer stock state** — not imported. `ONE SIZE — available` is the whole
  availability truth, and the source's own `O/S` scale agrees there is one size
  to have.
