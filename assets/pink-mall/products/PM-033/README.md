# PM-033 — live product media

Stella McCartney TU0A28Z0699 · Pineapple Bucket Bag · published 2026-08-27

| File | Slot | Source image | View | Native size |
|---|---|---|---|---|
| `PM-033-main.webp` | `media.image` | IMAGE 01 | front, whole bag, strap tucked | 1125×1500 |
| `PM-033-02.webp` | `gallery[0]` | IMAGE 02 | side profile, full crossbody strap | 1125×1500 |
| `PM-033-03.webp` | `gallery[1]` | IMAGE 04 | open top, green pineapple leaves | 1125×1500 |
| `PM-033-04.webp` | `gallery[2]` | IMAGE 03 | print and strap-attachment detail | 1125×1500 |

Filenames are **positional**, not source-numbered: `-02` is gallery position 0.
The approved order is MAIN 01 → 02 → 04 → 03, and the mapping above is the
whole of that translation. The tight print crop sits last so the gallery does
not open on a detail.

## Provenance — TRUSTED_RETAILER, and why the label is reliable

**Source: `img.giglio.com`**, the image CDN of Giglio, an established Italian
retailer. **This is not manufacturer media and is not presented as such.**

The four URLs are **exact observed link targets** from a product document read
directly by an independent reviewer transport. They were not constructed, not
guessed, and no template was extrapolated from them. Reviewer verification was
not treated as byte validation: every URL went through host check, fetch, MIME,
dimensions, non-product guards, identity, hash, dedupe, perceptual uniqueness,
variant confidence and backdrop detection.

Identity holds on the **asset URL itself**, via the colour-scoped alias
`401012.003`. Giglio paths carry its own product code rather than the designer
code, so the alias is what lets the gate recognise the retailer's own images.
Bare `401012` is deliberately unused: `.003` is the colour variant, and
dropping it would let a sibling colourway through.

`VARIANT_CONFIDENCE_PASS`, with the official colour term found in the frames.

This tier is only trustworthy because of a fix made for this product.
`_authority_tier` had been seeding OFFICIAL from `allowed_hosts` — the *network
permission* list — so every trusted retailer in a brand's registry read as
manufacturer media. That went beyond mislabelling: the same function decides
whether to keep hunting for official media, so a retailer answering "yes, I am
official" silently switched official discovery off. Manufacturer authority is
now declared explicitly via `official_hosts` and nowhere else.

| Source image | SHA-256 of original |
|---|---|
| IMAGE 01 | `2bf52fedd7f50dbdefae063016b78599…` |
| IMAGE 02 | `93c8283988f0f92d2220ef0ca0da7012…` |
| IMAGE 03 | `3394eafdf694c5b6ca29da706bfd3fa8…` |
| IMAGE 04 | `5d820a1b62677982246789fe47bc3aac…` |

| Live file | SHA-256 |
|---|---|
| `PM-033-main.webp` | `cc6227c36e54907ecef7d8f8f4ab2779a47fcad1a040a51366d7d5675d67407d` |
| `PM-033-02.webp` | `3a4a30376af5d1d65bb41447670107fa7168fb54be959c993b1edd5b407de18c` |
| `PM-033-03.webp` | `451dc64913ab74f04fb916f1498d7c954059bfafcc8c9d9e832c323b35a0ff8f` |
| `PM-033-04.webp` | `ee9349e3398194480bca0de67e8760f811f30e62eabe54dfa8a752e89698e6cd` |

Originals are committed untouched in
`docs/pink-mall/media-acquisition/TU0A28Z0699/source/`. Regenerate from there;
never overwrite them.

## Conversion

Format conversion only — JPEG → WebP quality 88 at each original's native
1125×1500 (3:4). No resize, no crop, no canvas, no upscaling.

`media.fit: 'contain'`. **`media.surface` is omitted, not chosen.** Images 01,
02 and 04 sit on a studio white of about `#ECECEC`; image 03 is a tight crop
with no backdrop at all, so no consensus backdrop could be derived and
`dominantBackdrop` correctly came back null. The Mall's own neutral `#EDEFF0`
is within three levels of that white, so the letterboxed area matches without
asserting a colour the set does not agree on.

One warning, non-blocking: **1500 px longest edge** — above the 1000 px
preference, below the 1600 px ideal.

## First product to publish a composition

`composition: '100% Polyurethane'` is rendered on the PDP. PM-026 through
PM-032 all omitted composition because no exact-product source ever stated one;
here the exact-SKU document does, so the material row appears.

**Dimensions are still NOT published.** The widely repeated `14 × 17 × 11 cm`
appears only in search-engine paraphrase and on a Smallable page that does not
name the article (measured: `page_has_sku` False).

## Colour — recorded honestly

Published as `Yellow`, per the brief and the approval.

The frames show yellow **printed with pink scalloped waves**, a green
drawstring top gathered into pineapple leaves, and a lilac strap. Pink is
roughly half the visible surface. `Yellow / Pink` would be the more accurate
public colour; that was put to the user in the approval package rather than
changed unilaterally, and the alt text describes all four colours so nothing is
hidden from a customer.

An earlier claim of mine that this product was "yellow, not pink" was wrong and
came from retailer text rather than the photographs. An early search summary
describing a "purple waves print" was also wrong: the waves are pink and the
strap is lilac.

## Not published on this product

- **Dimensions** — see above.
- **Retailer stock state** — not imported. `ONE SIZE` is the whole availability
  truth, verified against the live engine: availability mode yields stock state
  `ok`, is orderable at ONE SIZE, and refuses any other size.
- **Age-series classification** — internal only. It appears in no public name,
  copy, category, tag or alt text, and the opposite claim is not made either.
