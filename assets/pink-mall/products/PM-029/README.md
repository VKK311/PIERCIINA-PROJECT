# PM-029 — live product media

Pepe Jeans Ben Band · PGS30614 (full article PGS30614327, `factory pink`) ·
published 2026-08-26

| File | Slot | Source image | View | Native size |
|---|---|---|---|---|
| `PM-029-main.webp` | `media.image` | IMAGE 01 | lateral side profile, single shoe | 1920×2652 |
| `PM-029-02.webp` | `gallery[0]` | IMAGE 02 | pair, top-down | 1600×2210 |
| `PM-029-03.webp` | `gallery[1]` | IMAGE 04 | three-quarter, platform and midsole logo | 1200×1658 |
| `PM-029-04.webp` | `gallery[2]` | IMAGE 05 | heel and back quarter | 1200×1658 |
| `PM-029-05.webp` | `gallery[3]` | IMAGE 03 | outsole | 1600×2210 |

Filenames are **positional**, not source-numbered: `-02` is gallery position 0.
The approved order is MAIN 01 → 02 → 04 → 05 → 03, and the mapping above is the
whole of that translation. Outsole sits last, as on PM-025, PM-026 and PM-028.

Format conversion only — JPEG → WebP quality 88 at each acquired original's
**native** pixel dimensions. No resize, no crop, no canvas, no upscaling.

`media.fit: 'contain'` with `media.surface: '#DDDCD8'` — the studio backdrop the
acquisition pipeline detected from the photographs themselves. The storefront
fits the image; the image was not prepared to fit the storefront.

## Provenance — OFFICIAL manufacturer media

**Source: `images.pepejeans.com`, Pepe Jeans' own Salesforce Commerce Cloud
CDN.** This is the second product in the catalogue with manufacturer-tier
imagery; PM-026 was the first. PM-025, PM-027 and PM-028 all rest on
trusted-retailer media.

Every original filename carries the full article code
`PGS30614_327_<view>_FL.jpg`, so each asset is self-evidencing on its own URL —
the strongest identity class this pipeline recognises.

Resolution was raised by rewriting only the CDN's own sizing query
(`?sw=950` → `?sw=1600` or `?sw=1200`). The asset path is never touched, so the
bytes are the same photograph at a larger size. Nothing was upscaled.

| Source image | SHA-256 of original |
|---|---|
| IMAGE 01 | `08748a215fc7f5b4df43c1740dcb4f84ee186be870ce9fc9fa37186c5789ae52` |
| IMAGE 02 | `49e789f52fabac596f06dadfc4fac5197b07423fa93c063f99e60ed16ab30644` |
| IMAGE 03 | `36895cb0a3aaee9d75726bd4dc405ea757fdcabcb267eda3e49406fd7eb5095f` |
| IMAGE 04 | `632ed69341838688fecd259bd4e40a2591e7f594f95a49f60051b9cc235bb8d8` |
| IMAGE 05 | `be25d57b61bc5675bc838751353275bc9978827a93338760ca47c183b926fabc` |

| Live file | SHA-256 |
|---|---|
| `PM-029-main.webp` | `d27b7ad06138ea14adddba89a96680e0bd1438d035f556f9c7e7cb4f265ec77e` |
| `PM-029-02.webp` | `48a05fd583cc8a5b4981f4e7c794ed346b5b485bcc5223a88e32faae5e004792` |
| `PM-029-03.webp` | `8a5f9d39ff46319d7839421dbb1f75164c3d71de965ba2b2dda847c3a63ac1a7` |
| `PM-029-04.webp` | `0691e77ff02638c343a5ca520239d2bd82f53f254168cef944959c810fcd6d28` |
| `PM-029-05.webp` | `131adbc10fb06cca9e0a219512b4f00fc19bb0fe752f2aa868d9145953758640` |

Full per-image provenance — source URL, discovery method, dimensions, MIME,
SHA-256, dHash and the complete discovery ledger — is in
`docs/pink-mall/media-acquisition/PGS30614/result.json`. The untouched
originals are committed beside it in `source/`.

Regenerate from `source/`; never overwrite the originals.

## How this SKU was identified

Two independent provenance classes agreed, and neither was taken on assertion:

- **Claude's own research** across three official Pepe Jeans locale URLs and
  two retailers established `PGS30614` + colour `327`, the model name
  **Ben Band**, and the manufacturer colour name `factory pink`.
- **A reviewer-verified read** of the live Deporvillage product document
  supplied the exact retailer reference `PPJ-PGS30614-327` and the full
  **32–40** size ladder that confirms size 39 exists for this article.

The archive route that originally located the official CDN assets is
rate-limited and non-deterministic — the same manifest returned seven official
candidates on one run and none on the next. The media is therefore seeded from
bytes this pipeline had already fetched and hash-recorded, which is stronger
evidence than an archive lookup and makes acquisition reproducible.

## Not published on this product

- **Material / composition** — omitted. Retailers repeat a "70% sustainable
  cotton" line, which is a sustainability claim rather than a composition, and
  all three official locale URLs return 404, so this pipeline never read one.
- **Manufacturer junior-series classification** — internal only; it appears
  nowhere in the storefront, the alt text, the tags or the copy.
- **Manufacturer view 03** was not recovered. Its opaque `dw<hash>` path
  segment cannot be derived from the others and was not guessed.
