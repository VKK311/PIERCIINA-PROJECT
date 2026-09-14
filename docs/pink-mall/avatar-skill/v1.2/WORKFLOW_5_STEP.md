# PINK MALL Avatar Skill — 5-Step Operational Workflow v1.2

This is the canonical operating sequence for test-phase campaign work.

## STEP 1 — Identity & Reference Selection

Use `SKILL.md`, `AVATAR_LIBRARY_MANIFEST.json`, `CANONICAL_PACKS.json`, both Avatar Bibles, `DUO_LIBRARY.json` and `REFERENCE_SELECTION_RULES.md`.

Output a compact reference pack. Do not style the task before the identity pack is stable.

## STEP 2 — Brand DNA

Load `BRAND_DNA.json`. Translate the task into PINK MALL visual language while keeping identity and product locks untouched.

## STEP 3 — Sister Creative Profile

Load the relevant entry from `SISTER_STYLE_PROFILES.json` (`INA`, `SIS`, or `DUO`). These are testable creative defaults, not personal/biometric facts.

## STEP 4 — Campaign Preset

Select a preset from `CAMPAIGN_STYLE_PRESETS.json` and add any product-specific constraints. If no preset fits, use a temporary task-local variant and report it for possible later promotion into the canonical preset file.

## STEP 5 — Guardrails, Prompt Assembly & Test Logging

Apply `CREATIVE_GUARDRAILS.md` and `PROMPT_ASSEMBLY_RULES.md`. Produce the structured generation handoff, then the final brief. After the generated result is reviewed, score it with `TEST_EVALUATION_RUBRIC.json` and record changes needed before editing canonical rules.

## Test-phase rule

Do not change identity packs, Brand DNA or sister creative profiles after a single weak output. Record at least one concrete failure mode and distinguish whether the cause is:

- wrong reference selection,
- insufficient identity evidence,
- model-generation drift,
- weak campaign preset,
- weak creative profile,
- product conflict,
- crop/layout failure,
- or an overly restrictive/ambiguous prompt.

## v1.2 additions to step 5

Step 5 now emits three confidences rather than one, keeps
`productGeometrySource` separate from `productWearReference`, and copies the
preset's `compositionSafety` block into the handoff so the evaluator checks
`compositionUsable` against the same geometry the brief was built from.

Step 1 selects by role from candidate pools. It never emits a whole pool.
