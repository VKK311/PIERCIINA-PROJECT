# PM-045 — live product media

Minions `A2245` · Spread Happiness Strawberry Candle · published 2026-08-31

| Live file | Slot | Owner original | View | Native size |
|---|---|---|---|---|
| `PM-045-main.webp` | `media.image` | `source/PM-045-owner-01.jpg` | front, label legible | 970×1182 |
| `PM-045-02.webp` | `gallery[0]` | `source/PM-045-owner-02.jpg` | label detail, Minions artwork | 970×1182 |
| `PM-045-03.webp` | `gallery[1]` | `source/PM-045-owner-03.jpg` | candle lit, both wicks burning | 970×1182 |

## Provenance

- Media source: **USER_SUPPLIED**, owner-approved. Identity tier
  **TRUSTED_RETAILER**.
- The owner originals are JPEG; the live frames are WebP q88 at native size.
  No crop, no resize or upscale, no recolouring, no generative edit, no object
  removal or addition. Originals are preserved unchanged under `source/`.
- Identity: independent retailers list article `A2245` as the Minions
  *Spread Happiness* Strawberry large jar candle, 510 g. The jar label in the
  supplied photographs reads `Spread Happiness / SCENTED CANDLE · BOUGIE
  PARFUMÉE / Strawberry · Fraise` and carries the Minions artwork, so the
  photographed article and the article number agree.

| Live file | Owner original SHA-256 | Live WebP SHA-256 |
|---|---|---|
| `PM-045-main.webp` | `f35d32c4f0a286a1a91f546da9d6716ccb2d51d5390499e6ea57f98aa562d626` | `537ae40ff658…` |
| `PM-045-02.webp` | `76a3e722ca8700cc0a4350c9abd81a7297c3de12fc543e88c722f810e37fab0f` | `7f2be487a60b…` |
| `PM-045-03.webp` | `18b32c7773d84e307ef71e1b1d45ac42d67cee5e155cab3079da2729a539c724` | `8f5080d52293…` |

Full live hashes are recorded in `tools/regression/expect/PM-045.json`, which
the publication regression checks byte-for-byte.

`media.surface` is `#F1F1F1`, measured from the first two frames. The third is
a lifestyle frame with its own soft environment and no flat backdrop; it is a
gallery frame only and never the card image. Availability is
`ONE SIZE — available`. Composition is omitted: the wax type is not
independently established. The 510 g weight and the burn time appear in
retailer listings but are not published as product fields.
