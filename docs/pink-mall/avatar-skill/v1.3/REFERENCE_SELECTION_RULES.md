# PINK MALL Avatar Reference Selection Rules v1.3

## Purpose

This library is a retrieval system, not a dump of every available photograph into every image-generation request. The goal is to select the smallest set of references that provides independent, non-conflicting information about identity, angle, body geometry, expression, pose, product interaction and duo composition.

## Mandatory selection order

1. Identify the subject: `INA`, `SIS`, or `DUO`.
2. Start with identity anchors. For one sister, normally use `FACE_FRONT` plus the face angle nearest the requested view. For full-body work add `BODY_FRONT` plus the matching body angle.
3. Add exactly one task-specific pose reference when a pose is important.
4. Add a product-specific reference for eyewear/headwear/accessory tasks.
5. Add an expression reference only when the requested expression is materially different from neutral.
6. For duo work, select identity anchors for both sisters first, then add one or two DUO composition references.
7. Stop adding references when every image has a distinct job. Redundant references increase ambiguity.

## Candidate pools versus runtime packs

`CANONICAL_PACKS.json` holds **candidate pools** — the full approved evidence
set per role. A pool is never sent to a generator. A **runtime pack** is the
subset you select for one task.

Single subject: 4–6 reference images.
Two sisters: 6–8 total reference images.
Use 8–10 only when each image contributes unique information.

Each sister's CORE_FACE (5) plus CORE_BODY (6) is already 11 candidates — larger
than any pack. Select by role, never by pool.

## Identity separation

Never allow INA and SIS references to become an unlabeled mixed pool. Every selected image must keep its subject label.

For DUO tasks this is structural, not advisory: emit three labelled groups —
`GROUP_INA_IDENTITY`, `GROUP_SIS_IDENTITY`, `GROUP_DUO_STAGING`. A flat list is
what produced F01_IDENTITY_COLLISION in T04 run 001, where both generated women
converged toward INA.

INA references are authoritative only for INA. SIS references only for SIS. DUO
references never carry identity for either.

DUO photographs teach composition and interpersonal geometry. They do not replace clean single-subject face and body anchors.

## Reference priority

`CORE_IDENTITY` > `POSE_MASTER` / `DUO_MASTER` > `EXTENDED_REFERENCE` > `SELECT` > `ARCHIVE`.

If a higher-priority image conflicts with a lower-priority image, preserve the higher-priority identity geometry and use the lower-priority image only for pose/styling.

## Task recipes

### Portrait
FACE_FRONT + requested FACE_45/PROFILE + expression reference if needed.

### Full-body fashion
FACE_FRONT + BODY_FRONT + requested BODY_ANGLE + one POSE_MASTER.

### Eyewear
FACE_FRONT + relevant FACE_45 + one EYEWEAR **wear reference** + the catalogue
`productGeometrySource`. The EYEWEAR frame teaches wear position only.

### Headwear
FACE_FRONT + relevant FACE_45 + one HEADWEAR **wear reference** + the catalogue
`productGeometrySource`. The HEADWEAR frame teaches wear position only.

### Motion
FACE_FRONT + BODY_FRONT + one body angle + one MOTION reference.

### Duo hero/banner
INA FACE + INA BODY + SIS FACE + SIS BODY + one primary DUO composition from
`BLAZER_EDITORIAL` (the commercial default) + optionally one alternate.
`FOUNDATION_STORY` is not a hero default.

## Ranking and metrics

Prefer `FASHION_POSE.preferred` before `.secondary`. Both are retained evidence;
ranking only changes reach order.

Never rank or filter candidates by `frameLaplacianVar`. It is a full-frame
measurement dominated by background texture, and it scores the sharpest identity
frames lowest.

## Wardrobe is not selectable from this library

Every frame in every pool is an `identityReference`. None is a
`wardrobeAuthority`. `referencePhotoWardrobe = IGNORE_FOR_STYLING`. Never select
a reference because of what the subject is wearing, and never let selected
clothing become styling direction. See `WARDROBE_AUTHORITY.json`.

## Gap states

`SIS.IDENTITY_DETAILS.state` is `notCaptured`. Do not borrow INA's frames and do
not infer the missing detail. Lower `identityConfidence` and warn.

## Failure conditions

Do not claim a strong identity lock when the needed angle/detail is absent.
Do not invent permanent piercings, tattoos, hair changes or facial characteristics.
Do not use a DUO frame to decide which face belongs to which sister when clean solo references exist.
Do not select the full archive by default.
Do not emit a candidate pool as if it were a runtime pack.
Do not treat a full-body product frame as authoritative product geometry.
Do not emit a flat reference list for a DUO task.
Do not let calibration clothing become fashion direction.
