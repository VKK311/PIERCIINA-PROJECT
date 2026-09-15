# PINK MALL Avatar Reference + Creative Orchestrator — v1.3

Reference-selection, identity-consistency and creative-context layer for PINK
MALL avatar work involving INA, SIS or both.

**This directory is the canonical source.** The files are loose JSON, Markdown
and Python so every change is reviewable in a Git diff. There is no binary
archive to trust or re-hash.

## Start here

| File | Role |
|---|---|
| `SKILL.md` | the behaviour contract |
| `WORKFLOW_5_STEP.md` | the operating sequence |
| `CANONICAL_PACKS.json` | candidate pools + runtime selection caps |
| `AVATAR_LIBRARY_MANIFEST.json` | 190 records: paths, hashes, classifications |
| `CONSENT_AND_PROVENANCE.json` | authorisation state — currently unset |
| `IMAGE_LIBRARY_INTEGRATION_POLICY.md` | privacy policy for the photographs |
| `PIERCIINA_HERITAGE_DNA.json` | the retro lineage, derived from the canonical site |
| `IDENTITY_COLLISION_PROTOCOL.json` | keeping two sisters two people |
| `WARDROBE_AUTHORITY.json` | what may and may not dictate styling |
| `FAILURE_TAXONOMY.json` | F01–F08 codes and the run log |
| `build_fashion_context.py` | runtime wardrobe authority generator |
| `VALIDATE_SKILL.py` | 150 structural and semantic checks |

```bash
cd docs/pink-mall/avatar-skill/v1.3
python VALIDATE_SKILL.py

# resolve the current wardrobe authority before any fashion-led task
python build_fashion_context.py --catalogue ../../../../PINKMALL.html \
                                --out /tmp/fashion_context.json
# optional: pin the freshness date (defaults to today)
#                               --as-of 2026-09-15

# prove the catalogue seam still holds
cd "$(git rev-parse --show-toplevel)"
python tools/regression/fashion_context_contract.py PINKMALL.html
```

## The library is private and is not here

190 photographs — 77 INA, 76 SIS, 37 DUO — of two identifiable real people.
**They are not in this repository and must never be.** `PIERCIINA-PROJECT` is
public; Git LFS would not change that.

The manifest carries paths and SHA-256 hashes only. Paths are relative
(`INA/IMG_3854.JPEG`) and resolve against whatever private root the operator
mounts at runtime. Read `IMAGE_LIBRARY_INTEGRATION_POLICY.md` before touching
any image file.

## What changed in v1.3

T04 run 001 was generated and failed three independent ways. v1.3 is the
failure-learning patch. **No canonical identity reference was changed** — the
failures were pipeline defects, not evidence against the identity pools.

| Code | Failure | Fix |
|---|---|---|
| F01 | both women converged toward INA | three labelled reference groups + collision gates + LEVEL 2 sequential identity lock |
| F02 | calibration clothing copied as fashion | `identityReference` vs `wardrobeAuthority`; `referencePhotoWardrobe = IGNORE_FOR_STYLING` |
| F03 | generic glossy pink mall, no Pierciina | `PIERCIINA_HERITAGE_DNA.json` derived from the canonical site, scored and gated |

Assembly order changed from `identity → generic Brand DNA → campaign preset` to:

```
identity → current wardrobe authority → Pierciina heritage
        → PINK MALL campaign layer → composition → creative flourish
```

Wardrobe resolves before any styling language exists; heritage applies before
the campaign layer. New hard gates: `sisterDistinctnessRequired`,
`identityCollisionDetected=false`, `subjectRoleSwapDetected=false`,
`wardrobeSourceValid=true` for fashion-led work, and
`brandHeritageMatchMinimum`. Fashion direction is **not** frozen into the skill
— `build_fashion_context.py` reads the live catalogue at task time.

### `newIn` follows the storefront, not the raw flag

`build_fashion_context.py` decides freshness the way `PINKMALL.html` does: a
parseable `newUntil` wins outright and is **inclusive** through the end of that
day, and the raw `isNew` flag is only the fallback when `newUntil` is absent or
unreadable. Both values stay in `assortment` for provenance, but `newIn` is the
date-gated set.

This matters because the two disagree in practice. Every published product
(PM-025 onward) carries `isNew: false` with a fourteen-day `newUntil` window,
so during that window the Mall shows it as NEW while the raw flag says it is
not. On 2026-09-14 that was five products — PM-042 through PM-046 — live in
NEW IN and invisible to a flag-reading builder. The divergence runs the other
way too: a product keeping `isNew: true` past its `newUntil` would be reported
as NEW after the Mall had stopped showing it.

Dates are exactly `YYYY-MM-DD`. A `newUntil` in any other shape is treated as
unparseable and falls back to the raw flag, matching the storefront. Each
product is parsed only from inside its own record, so a missing field can never
be borrowed from the next product.

`--as-of YYYY-MM-DD` pins the evaluation date for reproducible runs and
defaults to today; the emitted context records it as `asOfDate`.
`tools/regression/fashion_context_contract.py` holds this seam, including the
boundary day, and fails loudly on structural drift in the catalogue.

## What changed in v1.2

v1.2 is a hardening patch from the v1.1 read-only audit. No identity master was
altered, no evidence deleted, no count changed: 190 / 77 / 76 / 37 with zero
cross-label mixing, verified by the validator.

- **Pools are not packs.** `CANONICAL_PACKS.json` holds candidate pools; a
  runtime pack is 4–6 images (6–8 for DUO) selected by role.
- **`frameLaplacianVar`** replaces `sharpnessLaplacianVar` and is documented as
  full-frame and not comparable across capture types. It must never rank
  identity masters.
- **Three confidences** — identity, composition, product — replace one blended
  value, with mandatory downgrades where the library has no evidence.
- **Product geometry is separate from wear reference.** No avatar frame is
  authoritative for a product's shape, logo or hardware.
- **Measurable composition safety** per preset, and `compositionUsable` is a
  hard gate: an unusable banner fails regardless of score.
- **`SIS.IDENTITY_DETAILS` is `notCaptured`** — a declared gap, not a borrowed
  reference.
- **`BLAZER_EDITORIAL`** is the commercial DUO default; `FOUNDATION_STORY` is
  not a hero default.
- **Consent is a schema, not a claim.** Every human-authorisation field is
  `OWNER_CONFIRMATION_REQUIRED`.

## Known library limits

Recorded in `CANONICAL_PACKS.json → knownLibraryLimits` and enforced through
confidence downgrades:

- all 190 frames are portrait 1536×2048 — no landscape, no 9:16;
- one location, flat daylight, no environmental variety;
- subjects centred and filling frame — no offset-subject copy space;
- no PINK MALL catalogue SKU appears in any frame.

These constrain composition and product confidence. They do **not** constrain
identity confidence, which the audit found well-supported.

## Status

v1.3 is ready for a T04 retry under a new controlled prompt, after independent
review. Do not auto-retry. Commercial publication of a generated
likeness is gated on `CONSENT_AND_PROVENANCE.json`.
