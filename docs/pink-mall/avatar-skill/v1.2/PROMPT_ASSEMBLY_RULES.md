# PINK MALL Prompt Assembly Rules v1.2

## Purpose

Convert a visual brief into a compact, evidence-grounded runtime pack plus a
consistent creative brief.

## Mandatory assembly sequence

### 1. SUBJECT
Determine `INA`, `SIS`, or `DUO`.

### 2. IDENTITY PACK
Select identity anchors **by role** from the candidate pools in
`CANONICAL_PACKS.json`. Pools are not packs — never emit a whole pool. Identity
selection always happens before styling.

If the task needs a SIS identity detail, stop: `SIS.IDENTITY_DETAILS.state` is
`notCaptured`. Set `identityConfidence: LOW`, warn, and do not substitute INA's
frames.

### 3. CAMPAIGN PRESET
Choose the closest preset in `CAMPAIGN_STYLE_PRESETS.json` and read its
`compositionSafety` block. If no preset fits, create a task-local preset without
editing the canonical file.

### 4. BRAND + SISTER STYLE
Apply `BRAND_DNA.json` and the relevant `SISTER_STYLE_PROFILES.json` entry.
Treat sister style profiles as creative defaults. Do not convert them into
biometric or personal claims.

### 5. TASK-SPECIFIC REFERENCES
Add only references with distinct jobs. Follow `REFERENCE_SELECTION_RULES.md`.
Prefer `FASHION_POSE.preferred` before reaching into `.secondary`.

### 6. PRODUCT — two separate fields

| Field | What it is | Where it comes from |
|---|---|---|
| `productGeometrySource` | authoritative shape, colour, logo, hardware, proportions | the PINK MALL catalogue image for the actual SKU |
| `productWearReference` | wear position, angle, attitude, how it sits on a body | `EYEWEAR` / `HEADWEAR` candidate pools |

A full-body eyewear or headwear frame teaches wear position. It is **never**
authoritative for product geometry — the item occupies roughly 2% of frame
height and no logo, temple or hardware is readable. Both pools are marked
`productAuthority: WEAR_REFERENCE_ONLY`.

Product-led task with no `productGeometrySource` → `productConfidence: LOW`
plus a warning. Never fill the gap from an avatar frame.

### 7. GUARDRAILS
Apply `CREATIVE_GUARDRAILS.md`. Resolve conflicts in this order:

`identity > product > campaign clarity > brand > creative flourish`

### 8. CONFIDENCE
Grade all three independently, then apply the mandatory downgrades in
`SKILL.md`. `compositionConfidence` cannot exceed MEDIUM for a landscape, 9:16,
text-safe or non-native-environment request, because
`CANONICAL_PACKS.json → knownLibraryLimits` records that no such reference
exists. Never report a single blended confidence.

### 9. OUTPUT THE GENERATION HANDOFF

```json
{
  "task": "...",
  "subjects": ["INA"],
  "campaignPreset": "hero_banner",
  "selectedReferences": [
    { "path": "INA/IMG_3854.JPEG", "role": "FACE_FRONT identity anchor", "priority": 1 }
  ],
  "identityLocks": [],
  "productGeometrySource": null,
  "productWearReference": null,
  "productLocks": [],
  "brandDirectives": [],
  "sisterStyleDirectives": [],
  "compositionDirectives": [],
  "compositionSafety": { "aspectRatio": null, "textSafeRegion": null, "edgeMargin": null },
  "negativeSpaceRequirement": "...",
  "format": "...",
  "warnings": [],
  "identityConfidence": "HIGH",
  "compositionConfidence": "MEDIUM",
  "productConfidence": null
}
```

Copy `compositionSafety` from the chosen preset so the evaluator can check
`compositionUsable` against the same numbers the brief was built from.

Then write the final image-generation brief using the same facts. Do not add
unsupported identity details while translating the handoff into prose.

## Runtime pack sizes

- Single sister: 4–6 references.
- DUO: 6–8 total.
- 8–10 only when every reference contributes unique information.

Stop adding images when every requirement has an evidence source.
