# PM-030 — live product media

Puma Palermo Moda · 398855, colour suffix **-11** (`Poised Pink / Aqua`) ·
published 2026-08-26

| File | Slot | Source image | View | Native size |
|---|---|---|---|---|
| `PM-030-main.webp` | `media.image` | IMAGE 01 | lateral side profile, single shoe | 2000×2000 |
| `PM-030-02.webp` | `gallery[0]` | IMAGE 05 | pair, three-quarter | 2000×2000 |
| `PM-030-03.webp` | `gallery[1]` | IMAGE 03 | medial side profile | 2000×2000 |
| `PM-030-04.webp` | `gallery[2]` | IMAGE 04 | heel and platform detail | 2000×2000 |
| `PM-030-05.webp` | `gallery[3]` | IMAGE 02 | top-down and outsole | 2000×2000 |

Filenames are **positional**, not source-numbered: `-02` is gallery position 0.
The approved order is MAIN 01 → 05 → 03 → 04 → 02, and the mapping above is the
whole of that translation. The combined top-down and outsole frame sits last,
as the outsole does on PM-025 through PM-029.

## Transparency is the point

These are **transparent cut-outs**, not photographs on a backdrop — between 54%
and 79% of each frame is fully clear. The conversion is PNG → WebP quality 88
at native 2000×2000 **with the alpha channel preserved**. No resize, no crop,
no canvas, no upscaling, and no flattening.

`media.surface` is **deliberately omitted** so the storefront's own neutral
field (`#EDEFF0`) shows through. That is not an oversight: the acquisition
pipeline originally derived a backdrop of `#47704C` — a dark green produced by
flattening a transparent PNG to RGB — which would have painted a green field
behind the product in a pink store. `backdrop()` now checks the cut-out flag
recorded at validation time, and returns nothing for a cut-out.

`media.fit: 'contain'`.

## Provenance — OFFICIAL manufacturer media

**Source: `images.puma.com`.** Third product in the catalogue with
manufacturer-tier imagery, after PM-026 and PM-029. PM-025, PM-027 and PM-028
rest on trusted-retailer media.

Discovery was by **CDN probe**, not archive lookup. A probe is a lead and never
evidence: it becomes a candidate only if it downloads, decodes and carries the
exact article number in its own path. Here **both** the article number and the
colour suffix appear in every path, so a probe could reach neither another
product nor another colourway.

| Source image | SHA-256 of original |
|---|---|
| IMAGE 01 | `9bcd9f343aa9469f31601ab9664240cbe7d1ef2c6da52fa8f50eaceeed7bc7c3` |
| IMAGE 02 | `07ea5ddb917150518fe387e75794ba8361cf7b0ce7bfe365fa2186f462c5ab08` |
| IMAGE 03 | `97edeb05484454dbdfef833977fb4bcdaf0ba6abc1016d80f3e8c0f9caeb3cf0` |
| IMAGE 04 | `120bebe751c510bd29856336d9614306277753f55eda19227ef3f7d7e048b5f0` |
| IMAGE 05 | `1b488470747571cc0a49581084215639fc29bcb39c0f49cc2336cbf53e570582` |

| Live file | SHA-256 |
|---|---|
| `PM-030-main.webp` | `5a8d4ea023cbc074be4987ec56acc9b4501c5918acbf90594075e426e4a5ca06` |
| `PM-030-02.webp` | `b2c67fbbbd24c9bbdfc3200a740f760f5e97e53b5b54ac4995ffeda10114d5aa` |
| `PM-030-03.webp` | `d846616dfc2b088c513475fc7ed02c3313547dbc2d0685112762f66315e7888f` |
| `PM-030-04.webp` | `a1c5109834e1d2baea86fc189ad36404a62364e9e12d38e2fbd33c1f35a7ad93` |
| `PM-030-05.webp` | `97ca48f6552a2376d523d56e3f2d9ee7905d4299f8a64a340ccc196874148e79` |

Full per-image provenance is in
`docs/pink-mall/media-acquisition/398855/result.json`; the untouched originals
are committed beside it in `source/`.

Regenerate from `source/`; never overwrite the originals.

## How the colourway was resolved

Article 398855 ships **eleven** colourways and the Puma colour suffix was
evidenced nowhere reachable. A first pass selected five views of `398855-01`,
Puma White / Puma Black, because the official product page serves the *default*
colourway and its images outranked everything else.

A reconnaissance sweep then fetched one hero view per colour code and put all
eleven on a contact sheet, which made `-11` unambiguous. The decoys were
visible in the same sheet and are worth naming, because each would have
satisfied a check that verified only the article number:

| Code | Colourway |
|---|---|
| 01 | white, black formstripe |
| 03 | mint, mauve formstripe |
| 07 | coral, pink formstripe |
| 10 | cream, **pale pink** formstripe |
| **11** | **pink, aqua formstripe** ← this product |

Before that, an earlier attempt targeted the wrong article entirely: `401489`
Club II Era, whose pink-bearing colourway `-04` turned out to be an
aquatic-primary shoe with a pink formstripe.

## Not published on this product

- **Material / composition** — omitted. The official page describes a suede
  upper with synthetic overlays, but that reached the project through a search
  summary of the page rather than the pipeline reading it.
- **Junior-series classification** — internal only. The manufacturer lists this
  as a big-kids item and the supplied model name carried "Jr"; neither appears
  in the storefront, the alt text, the tags or the copy.
- **The word "pink" alone** — the public colour is `Pink / Aqua`. The aqua
  formstripe is prominent and is not flattened away because the store is
  pink-themed.
