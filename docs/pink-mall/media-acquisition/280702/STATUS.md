# Ted Baker 280702 — SLIDDS slider keyring, PINK — identity evidenced, media not acquired

Brief of 2026-08-31: *Ted Baker / 280702 / €49 / one size / Colour: Pink*, with
three owner photographs. **Not published. No `PM-###` allocated.**

## Identity — settled

| | |
|---|---|
| Brand | Ted Baker |
| Model | SLIDDS ("Club Ted" slider keyring) — a key case shaped like a slider |
| Model number | `280702` — a **style root**; colour is carried by suffix (`280702-green` observed) |
| Material | 100% polyurethane |
| Size | approx. 12 × 5 × 2.5 cm, ships with key ring and carabiner |
| Pink colourway | exists — Zalando article `TE451F0H6-J11`; the green sibling is `TE451F0H6-M11` |

The exact-product document at modeherz anchors `280702` to the SLIDDS slider key
case. The run reached it and recorded it under `exactProductDocuments`, so
identity is evidenced. Status is therefore
`MEDIA_NOT_ACQUIRED_IDENTITY_EVIDENCED`, never "product not found".

## The variant conflict this item has carried since 2026-08-28 — now resolved

`docs/pink-mall/media-requests/280702-green.request.json` recorded, on
2026-08-28:

> *"This conflicts with the user's short descriptor pink; preserve the conflict
> for visual approval and never silently remap it."*
> *"Variant gate: exact-SKU evidence supports green/dark green/rose rather than a
> pink-only variant."*
> *"human variant confirmation remains mandatory."*

That run acquired three frames of the **GREEN** colourway
(`docs/pink-mall/media-acquisition/280702-green/`, status PASS) and the article
was left unpublished pending confirmation of which colourway the owner holds.

The owner's photographs of 2026-08-31 answer it: the article is the **pink**
exterior with a green lining and `TED BAKER LONDON` embossed on the strap — the
pink colourway, not the green one. The conflict is resolved in favour of pink.

**The green frames must not be used for this product.** They are a different
colourway and would misrepresent the article to a customer.

## Why media was not acquired

Every available route was attempted. The blocking fact is a single line in the
discovery ledger:

```
DIRECT_OFFICIAL_PAGE  https://www.zalando.co.uk/ted-baker-slidds-keyring-pink-te451f0h6-j11.html
                      HTTPError: HTTP Error 403: Forbidden
```

The retailer holding the pink gallery declines the runner outright. Because the
page never returns 2xx, the bounded SPA render route cannot fire either — a 2xx
response is one of its preconditions — which is why `JS_RENDERED_PAGE` is listed
as not attempted rather than as failed. Getting past a 403 would require
user-agent spoofing or fingerprint masking, which this project has refused at
eMAG HTTP 511, at Giglio and at jimmychoo.com, and refuses here.

The green colourway is present in this repo only because a previous session's
reviewer live-verified three exact `img01.ztat.net` asset URLs and seeded them
into the request as `candidateMedia`. No equivalent verified URL set exists for
the pink colourway, and constructing one by extrapolating from the green asset
paths is guessing, not evidence.

## Why the owner's photographs were not used

They never reached the working container. Attachments earlier in the session did
land on disk; the uploads directory was lost when the container recycled at
11:41 on 2026-08-31 and is not being recreated for later attachments. The images
are visible in the conversation and absent from the filesystem, so they cannot
be hashed, converted, committed, or checked by the publication regression.

Media is never reconstructed from a rendered image.

## What unblocks it

Either:

1. **The owner's three photographs reaching the container** — committed to this
   branch, or fetchable from a URL. This is the better route: it is the pink
   article itself, and it publishes as `USER_SUPPLIED` at the owner's own
   authority. Or:
2. **Verified exact asset URLs for the pink colourway**, observed in a live
   product document rather than constructed, seeded into
   `280702.request.json` as `candidateMedia` — the same route that worked for
   the green colourway.

## Staged, pending only media

| Field | Value |
|---|---|
| brand | `Ted Baker` |
| manufacturerItemNo | `280702` |
| variant | `Pink` (carried separately; `280702` is a style root) |
| name | `SLIDDS Slider Keyring` |
| category | `accessories` |
| color | `Pink` |
| composition | `100% полиуретан` |
| priceEUR | `49` |
| availability | `{"ONE SIZE": "available"}` |

Owner source of truth: €49, ONE SIZE. Retailer price, stock and measurements are
not imported.
