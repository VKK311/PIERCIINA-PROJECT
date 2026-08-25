# PM-027 — live product media

Converse Chuck Taylor All Star Move · A08745C (Pink) · published 2026-08-25

| File | Slot | Source image | View | Native size |
|---|---|---|---|---|
| `PM-027-main.webp` | `media.image` | IMAGE 01 | lateral side profile, single shoe | 1500×1500 |
| `PM-027-02.webp` | `gallery[0]` | IMAGE 05 | pair, three-quarter front | 670×670 |
| `PM-027-03.webp` | `gallery[1]` | IMAGE 02 | pair, angled | 670×670 |
| `PM-027-04.webp` | `gallery[2]` | IMAGE 04 | medial side profile, single shoe | 670×670 |
| `PM-027-05.webp` | `gallery[3]` | IMAGE 03 | pair, flat and top-down | 670×670 |

Filenames are **positional**, not source-numbered: `-02` is gallery position 0.
The approved order is MAIN 01 → 05 → 02 → 04 → 03, and the mapping above is the
whole of that translation.

Format conversion only — JPEG → WebP quality 88 at the **native** pixel
dimensions of each acquired original. No resize, no crop, no canvas, no
upscaling. The four 670×670 gallery images are published at 670×670; the
approval package flags that resolution and it was accepted knowingly.

`media.fit: 'contain'` with `media.surface: '#FFFFFF'` — the backdrop the
acquisition pipeline detected from the photographs themselves. The storefront
fits the image; the image was not prepared to fit the storefront.

## Provenance — trusted retailer, not manufacturer-official

**These are tier-5 trusted-retailer assets. They are not official Converse
manufacturer media and must not be described as such.**

Every official route failed for this SKU: `converse.com` returned `403` on four
attempts, the reachable regional category pages carried no A08745C link to
follow, and one-hop link following reached no official target. Media was
acquired from `akn-spx.a-cdn.akinoncdn.com` via the spx.com.tr product page,
with SKU evidence carried by that page's `og:image` and JSON-LD declarations
rather than by the asset URLs themselves. There is **no official image anchor**
for this product.

Variant state at acquisition: `VARIANT_CONFIDENCE_PASS` — exact-SKU evidence on
every image, official colour term `pink` detected in frame.

Full per-image provenance — source URL, discovery method, dimensions, MIME,
SHA-256, dHash, and the complete discovery ledger — is in
`docs/pink-mall/media-acquisition/A08745C/result.json`. The untouched originals
are committed beside it in `source/`.

| Source image | SHA-256 of original |
|---|---|
| IMAGE 01 | `231e637a1117092ba8a436e8d723c33964063100f1fce008827ae37dc41067f2` |
| IMAGE 02 | `a5be621bd2b3abd96e7e3d47190fd22d7228c78467a32de516bc46b46be7dca3` |
| IMAGE 03 | `91628dbf5104a03d8974836d6f378f7126af34148c7ccc589afe38d749b2eba1` |
| IMAGE 04 | `fd5a1a2f274ba1670374cf0005624dad53f71eb03e72917cdfb1d4f4ba5f8c04` |
| IMAGE 05 | `8b96c65f238d57f0dd8ff4d727341668c2bb803875c375dd1cc3499c111975d3` |

| Live file | SHA-256 |
|---|---|
| `PM-027-main.webp` | `653963958397eccbfa14681742077bfe7ba45f8102e14a24494c09b45f67319a` |
| `PM-027-02.webp` | `96a41e90403b40a4d0f16c367035278c817aa5da9056643beefb0ca8deaa2c64` |
| `PM-027-03.webp` | `b25dba93fd6397454d0cfa96000dc8737768641123e229c44eca507bfa6a7ada` |
| `PM-027-04.webp` | `ee5359f11de2ae94c36a221073bf1def9c27d84fc35a71e5ec8eac97ea7cb847` |
| `PM-027-05.webp` | `a8b911b19456ffac26288aa840e151224e484652f21cd3b66197897009bc3d7f` |

Regenerate from `source/`; never overwrite the originals.

## Not published on this product

- **Material / composition** — omitted. See §7 of the approval package.
- **Manufacturer youth-series classification** — internal only; it appears
  nowhere in the storefront, the alt text, the tags, or the copy.
