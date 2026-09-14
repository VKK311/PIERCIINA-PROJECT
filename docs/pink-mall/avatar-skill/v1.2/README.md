# PINK MALL Avatar Reference + Creative Orchestrator — v1.2

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
| `VALIDATE_SKILL.py` | 86 structural and semantic checks |

```bash
cd docs/pink-mall/avatar-skill/v1.2
python VALIDATE_SKILL.py
```

## The library is private and is not here

190 photographs — 77 INA, 76 SIS, 37 DUO — of two identifiable real people.
**They are not in this repository and must never be.** `PIERCIINA-PROJECT` is
public; Git LFS would not change that.

The manifest carries paths and SHA-256 hashes only. Paths are relative
(`INA/IMG_3854.JPEG`) and resolve against whatever private root the operator
mounts at runtime. Read `IMAGE_LIBRARY_INTEGRATION_POLICY.md` before touching
any image file.

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

Ready for controlled internal testing. Commercial publication of a generated
likeness is gated on `CONSENT_AND_PROVENANCE.json`.
