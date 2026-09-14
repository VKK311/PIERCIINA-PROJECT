# Changelog

## v1.3 — failure-learning patch

Response to T04 run 001, the first real generation, which failed with three
independent failure classes. Scope limited to the Avatar Skill package.

**No canonical identity reference, manifest record, hash, identity master or
privacy rule was changed.** The 190-record manifest, both bibles and the
storage policy are byte-identical to v1.2.

### New files
- `PIERCIINA_HERITAGE_DNA.json` — derived from the canonical `PINKMALL.html`:
  CSS tokens (magenta #C3537D / #8B3A5C / #5A2640, cream #FDF59A / #E8C547,
  gold #D4AF37), font stacks (Bungee, Bungee Shade, Lilita One, Playfair
  Display, Allura), motif classes (marquee, retro-sticker, pm-bg-sparkle,
  pm-neon), glyph counts (✦60, ★40, ♡♥21, ⚡5) and measured vocabulary weight
  (retro 66 vs Y2K 28). Not generic fashion assumptions.
- `IDENTITY_COLLISION_PROTOCOL.json` — authority rules, three labelled
  reference groups, detection booleans, LEVEL 1 / LEVEL 2 escalation.
- `WARDROBE_AUTHORITY.json` — `identityReference` vs `wardrobeAuthority`,
  `referencePhotoWardrobe = IGNORE_FOR_STYLING`, three-rank source priority.
- `CURRENT_PINK_MALL_FASHION_CONTEXT.schema.json` + `build_fashion_context.py` —
  runtime adapter; instances are deliberately not committed.
- `FAILURE_TAXONOMY.json` — F01–F08 plus the T04 run 001 record.

### Changed
- `SKILL.md`, `PROMPT_ASSEMBLY_RULES.md`, `REFERENCE_SELECTION_RULES.md`,
  `CREATIVE_GUARDRAILS.md`, `WORKFLOW_5_STEP.md` — new assembly order, labelled
  DUO groups, wardrobe layer, heritage layer, collision protocol, seven-level
  conflict priority, mandatory negative prompt.
- `TEST_EVALUATION_RUBRIC.json` — added `brandHeritageMatch` (0.08), funded by
  `brandFit` 0.12→0.06 and `creativeOriginality` 0.07→0.05; weights still sum to
  exactly 1. New gates: `sisterDistinctnessRequired`,
  `identityCollisionDetected=false`, `subjectRoleSwapDetected=false`,
  `wardrobeSourceValid=true`, `brandHeritageMatchMinimum=7`.
- `TEST_SCENARIOS.json` — wardrobe expectations, collision checks for DUO,
  T04 prior-run record, no-auto-retry policy.
- `CANONICAL_PACKS.json` — additive flags only: `referencePhotoWardrobe`,
  wardrobe and identity authority notes. Zero image references changed.
- `VALIDATE_SKILL.py` — 150 checks (was 86).

### Doctrine
One failed generation is evidence about the pipeline, not permission to rewrite
the identity system.

## v1.2 — hardening patch

Implements the required changes from the v1.1 read-only audit. Scope limited to
the Avatar Skill package. No image generation, no PINKMALL changes, no Avatar
Masterclass changes, no product or jewelry changes.

Source: the v1.1 package verified at SHA-256
`461490e032798eef5e7049277c28bfcdd82430d53291347143dbd29192987874`.
The truncated 7,529-byte archive in the audit branch was not used.

### Preserved
- 190 records — 77 INA, 76 SIS, 37 DUO.
- Zero INA/SIS cross-label mixing.
- `INA_v1.0` and `SIS_v1.0` masters untouched; both remain
  `CURATED_FOUNDATION_CANDIDATE`.
- All 83 canonical references and all 103 canonical/DUO resolutions retained.
- Rubric criteria weights unchanged, summing to exactly 1.

### AVATAR_LIBRARY_MANIFEST.json
- `sharpnessLaplacianVar` → `frameLaplacianVar` across all 190 records.
- Added `metrics.frameLaplacianVar` documenting full-frame scope, what it must
  not be used for, and why: background texture dominates the value, so the
  sharpest identity frames score lowest.
- Added `identityPolicy.metricPolicy` forbidding re-ranking from it.
- No record re-ranked or re-tiered.

### CANONICAL_PACKS.json
- Introduced `terminology` separating `candidatePool` from `runtimePack`.
- Added `runtimeSelection` with caps 4–6 single / 6–8 duo and a `roleOrder`.
- Every pool now carries an explicit `role`; no reference removed.
- `FASHION_POSE` split into `preferred` and `secondary` — ranking only.
- `SIS.IDENTITY_DETAILS` added with `state: notCaptured` and an explicit
  no-borrowing rule.
- `EYEWEAR` and `HEADWEAR` marked `productAuthority: WEAR_REFERENCE_ONLY`.
- `DUO.commercialDefault` set to `BLAZER_EDITORIAL`; `FOUNDATION_STORY` marked
  `notForHeroDefault` with its reason recorded.
- Added `knownLibraryLimits`.

### CAMPAIGN_STYLE_PRESETS.json
- Added `compositionSafety` to all six presets: aspect ratios, numeric
  `textSafeRegion`, `subjectZone`, `edgeMargin`, mobile-crop expectation.
- Flagged `TEST_DEFAULTS_NOT_PERMANENT_BRAND_TRUTH`.

### TEST_EVALUATION_RUBRIC.json
- Added `compositionUsableRequired` gate and a `compositionUsable` definition
  with explicit fail conditions.
- Gate rule now states score cannot override it.
- `compositionUsable` and `compositionFailReason` added to review fields.

### TEST_SCENARIOS.json
- Each scenario carries `expectedConfidence` across all three axes with a
  rationale, and `requiresCompositionUsableGate`.
- T02 carries `productGeometrySource` and `productWearReference`.

### CONSENT_AND_PROVENANCE.json — new
- Schema for ownership, authorisation, allowed use, expiry/review and
  revocation. Every human-authorisation field initialised to
  `OWNER_CONFIRMATION_REQUIRED`. No consent was inferred or invented.
- Records that the library contains sensitive personal imagery and that public
  repository exposure is prohibited.

### IMAGE_LIBRARY_INTEGRATION_POLICY.md
- Rewritten as a privacy policy. States the repository is public, prohibits
  committing source photographs or any derivative, withdraws Git LFS in a public
  repository as an option, and names the two acceptable storage architectures.

### SKILL.md / PROMPT_ASSEMBLY_RULES.md / REFERENCE_SELECTION_RULES.md / CREATIVE_GUARDRAILS.md / WORKFLOW_5_STEP.md
- Pools-versus-packs, three confidences with mandatory downgrades, product
  geometry versus wear reference, the SIS gap state, the DUO default, the
  metric prohibition and the consent gate propagated consistently.
- Handoff schema updated in both files that define it.

### VALIDATE_SKILL.py
- Rewritten: 86 checks covering the v1.1 baseline plus every v1.2 rule.
  Standard library only.

### Packaging
- Canonical source is now loose reviewable files under
  `docs/pink-mall/avatar-skill/v1.2/`. No binary archive is canonical.

## v1.1
Added creative context and test layers to the v1.0 identity evidence base.

## v1.0
Curated identity evidence: manifest, canonical packs, avatar bibles, DUO library.
