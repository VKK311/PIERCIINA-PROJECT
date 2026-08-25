# PM-028 — live product media

adidas Gazelle Bold Shoes · JR5952 (Almost Pink / Court Green / Gold Metallic) ·
published 2026-08-25

| File | Slot | Source image | View | Native size |
|---|---|---|---|---|
| `PM-028-main.webp` | `media.image` | IMAGE 02 | pair, three-quarter front | 560×746 |
| `PM-028-02.webp` | `gallery[0]` | IMAGE 01 | pair, lateral and heel-on | 560×746 |
| `PM-028-03.webp` | `gallery[1]` | IMAGE 05 | pair, top-down | 560×746 |
| `PM-028-04.webp` | `gallery[2]` | IMAGE 04 | upper detail — stripes and platform | 560×746 |
| `PM-028-05.webp` | `gallery[3]` | IMAGE 03 | outsole, gum rubber | 560×746 |

Filenames are **positional**, not source-numbered: `-02` is gallery position 0.
The approved order is MAIN 02 → 01 → 05 → 04 → 03, and the mapping above is the
whole of that translation.

MAIN is IMAGE 02, not the automation's proposal. The pipeline picks a proposed
MAIN by filename order and offered IMAGE 01; on visual review IMAGE 02 is the
stronger card image — both shoes complete, three-quarter front, silhouette and
stripe placement legible at thumbnail size. IMAGE 04 is a cropped upper detail
and is placed late for that reason.

Format conversion only — JPEG → WebP quality 88 at the **native** 560×746 of
each acquired original. No resize, no crop, no canvas, no upscaling. All five
are below the 1000 px preference; the approval package flags that and it was
accepted knowingly. These are portrait frames, not squares, and nothing was
padded to make them square.

`media.fit: 'contain'` with `media.surface: '#FFFFFF'` — the backdrop the
acquisition pipeline detected from the photographs themselves. The storefront
fits the image; the image was not prepared to fit the storefront.

## Provenance — trusted retailer, not manufacturer-official

**These are tier-5 trusted-retailer assets. They are not official adidas
manufacturer media and must not be described as such.**

Every official route failed for this SKU: adidas product pages and both API
regions returned `403` or timed out across five attempts, and
`assets.adidas.com` is not addressable by style code because adidas hashes its
asset paths. Media was acquired from `img.eobuwie.cloud`, with SKU evidence
carried by the source page's JSON-LD declaration rather than by the asset URLs
themselves. There is **no official image anchor** for this product — variant
confidence rests on exact-SKU evidence plus agreement with the official colour
text, which is materially weaker than PM-026's manufacturer-CDN media.

Marketplaces carrying the same SKU (Allegro, ERLI) were excluded as primary
media per the source hierarchy.

Variant state at acquisition: `VARIANT_CONFIDENCE_PASS` — exact-SKU evidence on
every image, and all three official colour terms (`pink`, `green`, `gold`)
detected in frame.

Full per-image provenance — source URL, discovery method, dimensions, MIME,
SHA-256, dHash, and the complete discovery ledger — is in
`docs/pink-mall/media-acquisition/JR5952/result.json`. The untouched originals
are committed beside it in `source/`.

| Source image | SHA-256 of original |
|---|---|
| IMAGE 01 | `0cab3a34b5f9a5b50f8149f95b3e29ba531b5117f4f8addaf0e123401d74ad68` |
| IMAGE 02 | `c5df8c2eaa320046a6510603be2e44986788a1d8b71d0ef909c5d45c770405c9` |
| IMAGE 03 | `0e964d27e5d27cf88aa70cdb0f9a6ece01651f8f1e361ef17718a45682b72d63` |
| IMAGE 04 | `d011be115e80fc4b317861c44459bca594cb142976f8b54512b414fafc2a5bca` |
| IMAGE 05 | `d4e22ea87c8ed1de787de54058f9f9308fdfa215114415c15a2a4c69de495c50` |

| Live file | SHA-256 |
|---|---|
| `PM-028-main.webp` | `c3a88ec0f501922137b70c01abbfc9c8f99f47a2f6f37931d635e27c89a5ac37` |
| `PM-028-02.webp` | `842caa475e66008fd2b098dd304fd705fbddf98862d13692c775ac10375e50d8` |
| `PM-028-03.webp` | `c16b338a400cd227ce8a260bd9c018a3cd0d17402aaffd91d67d1591c1c6d0d4` |
| `PM-028-04.webp` | `d09d69cb362b563722976e96707a65ab4b4c10d34cc8d90888a50dfec12156a7` |
| `PM-028-05.webp` | `ce022c37875f9491ed83f85c74e9a8fa9fe26e2ab5ff5338abb1dd132de61c5d` |

Regenerate from `source/`; never overwrite the originals.

## A correction this product records

An earlier pass rejected exactly this media as "a white-and-green Gazelle Bold,
not the pink JR5952". That rejection was wrong. `Almost Pink` is a very pale
tint and `Court Green` is part of the official colourway, so the imagery matched
the official variant precisely — correct media was discarded on a subjective
read of colour. The variant gate now reaches its conclusion from evidence rather
than impression, and the case is a permanent regression fixture in
`tools/media_acquisition/selftest.py`.

## Not published on this product

- **Material / composition** — omitted; never established by this pipeline.
- **Manufacturer juniors-series classification** — internal only; it appears
  nowhere in the storefront, the alt text, the tags, or the copy.
