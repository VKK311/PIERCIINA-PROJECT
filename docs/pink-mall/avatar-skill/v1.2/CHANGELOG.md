# Changelog

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
