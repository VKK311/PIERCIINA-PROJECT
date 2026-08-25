# adidas JR5952 — variant confidence resolved, ready for approval

**Supersedes the earlier `MEDIA DISCOVERY BLOCKED` record, which rested on a
rejection I got wrong.**

| | |
|---|---|
| Brand | adidas |
| Model | Gazelle Bold Shoes |
| Manufacturer item | JR5952 |
| Manufacturer colour | Almost Pink / Court Green / Gold Metallic |
| Sizes supplied | 36, 37 1/3, 38, 38 2/3 |
| Status | `PASS` · `VARIANT_CONFIDENCE_PASS` — **not published** |

## The correction

I previously rejected the acquired imagery as "a white-and-green Gazelle Bold,
not the pink JR5952". That was wrong. The official colourway is
**Almost Pink / Court Green / Gold Metallic**: a very pale upper with **green**
stripes and gold lettering. The images matched the official variant precisely.
"Not pink enough" was never a sound rejection, and it discarded correct media.

The variant-confidence gate now reaches the same conclusion from evidence
rather than impression — exact-SKU evidence on every image, plus `pink`,
`green` and `gold` all detected in frame, matching all three official colour
terms.

## Media — 5 images

Source: eobuwie / modivo / shooos, mainstream retailers carrying the exact SKU.
`TRUSTED_RETAILER_SEARCH`, tier 5. adidas direct routes returned 403 on all
five attempts, and adidas hashes its CDN paths so `assets.adidas.com` is not
addressable from the SKU alone.

| 01 | `0cab3a34b5f9a5b50f8149f95b3e29ba531b5117f4f8addaf0e123401d74ad68` |
| 02 | `c5df8c2eaa320046a6510603be2e44986788a1d8b71d0ef909c5d45c770405c9` |
| 03 | `0e964d27e5d27cf88aa70cdb0f9a6ece01651f8f1e361ef17718a45682b72d63` |
| 04 | `d011be115e80fc4b317861c44459bca594cb142976f8b54512b414fafc2a5bca` |
| 05 | `d4e22ea87c8ed1de787de54058f9f9308fdfa215114415c15a2a4c69de495c50` |

## Honest limit

No **official image anchor** exists for this SKU, so confidence rests on
exact-SKU evidence plus agreement with the official colour text. That is
materially weaker than PM-026, where the media came from the manufacturer's own
CDN. Anchor-backed certainty would need official asset URLs.

Resolution is 560x746 — below the 1000 px preference. Non-blocking; do not
upscale.
