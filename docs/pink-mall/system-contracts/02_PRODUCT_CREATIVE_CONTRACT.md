# PINK MALL — Product Creative Contract

| | |
|---|---|
| **Contract ID** | `PINK_MALL_PRODUCT_CREATIVE_CONTRACT` |
| **Number** | `02` |
| **Version** | `1.0.0` |
| **Status** | `CANDIDATE` — provenance only; canonicality follows contract 00's four conditions |
| **Parent** | `PINK_MALL_SYSTEM_AUTHORITY_CONTRACT` |
| **Depends on** | `PINK_MALL_CAMPAIGN_CONTEXT_CONTRACT` (contract 01) |
| **Machine-readable** | `02_PRODUCT_CREATIVE_CONTRACT.json` |
| **Runtime package** | `02_PRODUCT_CREATIVE_OBJECT.schema.json` |
| **Validator** | `tools/regression/product_creative_contract.py` |

## 1. Purpose

Define the product-fidelity constitution that governs creative work depicting a
real PINK MALL product — **before** paid generation infrastructure is activated.

The order matters. Once a generator is running and producing plausible images,
every argument about what it may change becomes an argument about a specific
picture someone already likes. This contract settles the question while nothing
is at stake.

**No Product Creative Engine exists.** Nothing here is implemented.

## 2. Core principle

> **World physics may break.
> Product truth may not.
> Human identity may not.**

Inherited verbatim from the parent's `creativeFreedomPrinciple`.

The creative world may transform around a real product. The product itself may
not be redesigned.

## 3. What 1:1 product fidelity actually means

The creative target for a real SKU is **1:1 product fidelity**. Stated honestly:

**It does NOT mean** a generated image is a pixel-identical copy of a catalogue
photograph. That would make campaign work impossible and is not the goal.

**It means the generator receives NO authority to redesign the product.**

The depiction must remain recognisable as the **same exact**:

- product identity;
- manufacturer item number / SKU;
- variant / colourway;
- silhouette;
- intrinsic geometry;
- construction;
- proportions between product components;
- distinctive product features;
- logos, wordmarks and graphics where visible;
- hardware, closures, handles, straps, soles, lenses, frames, stitching and
  pattern placement where applicable and established.

**Factual attributes Product Truth has not established MUST NOT be invented** to
fill a gap in the depiction.

### This is not a new standard

`references/03-media-policy.md` in the product-onboarding skill already forbids,
for canonical ecommerce images: recolour, reshape, logo change, print change,
sole change, hardware addition or removal, stitching change, proportion change,
hallucinated angles, and feature addition or removal. This contract carries that
same discipline into **generated campaign media** rather than inventing a second
standard.

## 4. Product Truth authority

**This contract MUST NOT become a second product database.**

| Fact | Domain | Authority |
|---|---|---|
| exact SKU / product identity | `PRODUCT_IDENTITY` | Product Onboarding system |
| price | `PRODUCT_PRICE` | **OWNER** |
| available sizes | `PRODUCT_AVAILABILITY_AND_SIZES` | **OWNER** |
| variant / colourway | `PRODUCT_IDENTITY` | Product Onboarding system |
| canonical product media | `CANONICAL_PRODUCT_MEDIA` | Product Onboarding system |

- A creative system **MAY READ** Product Truth.
- A creative system **MUST NOT WRITE** Product Truth.
- **A generated image is never evidence that Product Truth changed.**
- A depiction that disagrees with Product Truth is a defect in the depiction,
  never a correction to the product.

## 5. Product geometry is not a wear reference

Two distinct things, never merged. Inherited from Avatar Skill v1.3.

| Role | Authoritative for geometry | Must derive from the exact product |
|---|---|---|
| `productGeometrySource` | **YES** | **YES** |
| `productWearReference` | **NO** | no |

**`productGeometrySource`** is authoritative visual evidence for shape, colour,
logo and markings, hardware, construction and product proportions. For a real
SKU it **MUST** derive from the actual verified product.

**`productWearReference`** describes only how an item sits, how it is worn, how
it is held, and its approximate interaction with a human body. It **MAY** inform
placement. It **MUST NOT** override product geometry.

### Never product-geometry authority

- avatar photographs and any avatar frame;
- generic category imagery;
- a visually similar SKU;
- a different colourway of the same model;
- avatar calibration-photograph wardrobe;
- a generated image, including one this system produced.

**Do not convert an Avatar reference into Product Truth.**

## 6. The Product Lock model

Nine core locks. Every one applies whenever a real product appears at role
`DETAIL`, `SUPPORTING` or `HERO`.

| Lock | Guards against |
|---|---|
| `IDENTITY` | wrong model, substituted similar SKU, generic stand-in |
| `VARIANT` | different colourway, different print run, different finish |
| `SILHOUETTE` | reshaped body, altered outline, changed volume |
| `GEOMETRY` | hallucinated angle, invented facet, reflowed form |
| `CONSTRUCTION` | changed seams, stitching, sole construction, added panel |
| `PROPORTIONS` | resized heel, lengthened strap, rescaled hardware |
| `COLOUR` | recolour, moved colour block, invented gradient |
| `BRANDING_MARKINGS` | altered logo, invented wordmark, restyled brand mark |
| `DISTINCTIVE_DETAILS` | removed signature detail, added hardware, simplification |

A later contract **MAY** add category-specific locks. It **MUST NOT** silently
weaken a core lock.

**A lock is not a numeric tolerance.** Exact computer-vision thresholds are OPEN
and are deliberately not set here.

## 7. The creative envelope

> **CREATIVE FREEDOM applies to the WORLD.
> PRODUCT LOCK applies to the PRODUCT.**

Creative systems **MAY** alter, subject to other contracts: environment,
lighting, atmosphere, narrative situation, surrounding objects, visual genre,
camera language, surrealism, world physics, composition.

They **MUST NOT** intentionally redesign the product itself.

This contract constrains **product fidelity only**. It does not narrow PINK MALL
into a single visual style — heritage and brand-fit belong to the Avatar
heritage authority and contract 01.

## 8. Commerce media versus campaign media

The media taxonomy belongs to contract 00 and is **not redefined here**.

| Class | Generative alteration | Boundary |
|---|---|---|
| `CANONICAL_COMMERCE_MEDIA` | **forbidden** | belongs to Product Truth; acquired and approved through onboarding |
| `CAMPAIGN_MEDIA` | allowed | may place the real product in an imaginative world; **never** canonical commerce photography |
| `DERIVATIVE_MEDIA` | allowed | inherits its source's constraints |

- Campaign media **MUST NOT** silently replace canonical commerce media.
- Campaign media **MUST NOT** be promoted into Product Truth **merely because it
  looks convincing**.

## 9. Product role — the dependency on contract 01

Contract 01 decides whether a product is `NONE`, `DETAIL`, `SUPPORTING` or
`HERO`. This contract does not duplicate that.

- **`HERO` is never globally required.** Not every campaign is product-led.
- **`NONE` remains valid.** When the role is `NONE` there is no real product to
  lock and this contract imposes nothing.
- When the role is `DETAIL`, `SUPPORTING` or `HERO`, **every rule here applies in
  full** — a product shown as a detail is still the real product.

## 10. Product confidence

States: `HIGH` · `MEDIUM` · `LOW`. Compatible with Avatar Skill v1.3's
`productConfidence`. **No numeric scoring is defined.**

**A product-led task without an adequate `productGeometrySource` cannot claim
high product confidence.**

| Condition | Result |
|---|---|
| no `productGeometrySource` for a product-led task | `LOW` |
| geometry evidence is a *similar* SKU | **STOP** |
| geometry evidence is a *different colourway* | **STOP** |
| evidence omits a lock category visible in the depiction | `MEDIUM` |
| body-worn clothing without sufficient garment geometry evidence | **STOP** |

An uncertain product **MUST NOT** be reported as fully grounded. Declare the
uncertainty instead.

### Confidence is not permission to generate

Product confidence and **generation readiness** are different judgements, and
collapsing them is how an ungrounded task gets generated anyway.

| | |
|---|---|
| `productConfidence` | **a statement** about how well grounded the task is |
| generation readiness | **a gate**: `READY` or `BLOCKED` |

`LOW` confidence is a confidence statement. **It is not permission to generate.**

Readiness is `BLOCKED` when there is no adequate exact-product
`productGeometrySource`, when the only geometry evidence is a similar SKU or a
different colourway, or when a body-worn clothing depiction lacks
garment-geometry evidence.

**No Product Reference Package may be emitted for generation while readiness is
`BLOCKED`** — which is why the package schema requires at least one exact-product
geometry source. A package that cannot name the product's geometry evidence
cannot be assembled at all.

Avatar Skill v1.3's mapping — no `productGeometrySource` on a product-led task
sets `productConfidence: LOW` — is **preserved verbatim**. The readiness gate is
added alongside it, not in place of it.

## 11. Clothing worn on a body is a high-risk class

Garment geometry and human-body geometry interact. A generator can preserve the
apparent **colour** of a garment while still changing:

cut · length · neckline · sleeve geometry · waist position · drape · volume ·
seams · openings · closures · fit · distinctive construction

**Preserved colour is not evidence of preserved garment geometry.**

Therefore: **CLOTHING WORN ON BODY = HIGH-RISK PRODUCT-FIDELITY CASE.**

A complete per-category risk taxonomy is **not** invented here. Other categories
remain OPEN unless repository evidence already locks them.

## 12. Clothing Fit Protocol

Contract-level. **No implementation yet.**

| Evidence kind | Authoritative for the garment | From the exact product |
|---|---|---|
| `GARMENT_GEOMETRY_EVIDENCE` | **YES** | **YES** |
| `WEAR_FIT_EVIDENCE` | **NO** | no |

Rules:

- garment geometry still comes from **exact-product** evidence;
- body and avatar references are **never** garment-geometry authority;
- calibration-photograph wardrobe is **never** styling authority
  (`referencePhotoWardrobe = IGNORE_FOR_STYLING`);
- a **similar garment is not evidence** for the real SKU;
- fit evidence **may** inform how the exact garment interacts with a body;
- fit evidence **may not** redesign the garment;
- if critical fit evidence is absent, the uncertainty **MUST be declared rather
  than invented**.

Outcomes: `PASS` · `FAIL` · `UNRESOLVED`.

**`UNRESOLVED` is a real, blocking outcome** — never a silent `PASS`. No numeric
computer-vision thresholds are defined.

### Evidence readiness before generation is not a fit result after it

These outcomes describe an **actual generated depiction**. A depiction that does
not exist yet cannot have passed or failed anything.

So the pre-generation Product Reference Package carries `clothingFitEvidence` —
`garmentGeometryEvidencePresent`, `wearFitEvidencePresent`,
`avatarWardrobeUsedAsGarmentAuthority` — and **never** a `fitStatus`. The
`PASS` / `FAIL` / `UNRESOLVED` vocabulary stays here, in the normative protocol,
for evaluating a real depiction later.

For a **generation-ready** package where `clothingWornOnBody` is true, the schema
structurally requires `riskLevel: HIGH`, the presence of `clothingFitEvidence`,
`garmentGeometryEvidencePresent: true`, and
`avatarWardrobeUsedAsGarmentAuthority: false`. Missing optional wear/fit evidence
is **declared in `knownUncertainties`**, never invented.

## 13. Human + product: two locks at once

When a campaign contains INA, SIS or DUO **together with** a product, two
independent locks operate simultaneously:

**HUMAN IDENTITY LOCK** and **PRODUCT LOCK**.

**Neither may be sacrificed to preserve the other.**

If the generator cannot satisfy both → **REJECT THE CANDIDATE.**

Forbidden ways to "resolve" the conflict: changing the sister, changing the
product, changing the SKU, changing the colourway, silently simplifying a
distinctive product feature.

## 14. Consent

Commercial publication of a generated likeness remains governed by the existing
**Consent Gate** (`CONSENT_AND_PROVENANCE.json`).

This contract **references** that authority. It **does not resolve** it.

**Current consent state is deliberately not recorded here.** Consent state is
mutable authority state owned by the Consent Gate; caching a copy in this
contract would make it stale — and contradict its own authority — the moment the
owner resolves consent. It **MUST be read from the authority** at the time it
matters.

**Controlled internal validation and commercial publication are different
operations** and are not interchangeable.

## 15. Generated output status

Once a generated depiction **exists**, it begins as **`GENERATED_OUTPUT` /
`CANDIDATE`**.

This is a statement about an **output**, not about the input package. The
pre-generation Product Reference Package carries **no** `outputStatus` at all:
there is no output yet to have a status.

It is **not** `FACT`, `CANONICAL_PRODUCT_MEDIA`, `APPROVAL` or `PUBLISHED`
simply because generation succeeded.

**Generation success is not validation success.**

States this contract may express: `CANDIDATE`, `QA_PASSED`, `QA_FAILED`,
`QA_UNRESOLVED`. States it may **not** express — `APPROVED`, `APPROVED_SPEND`,
`PUBLISHED`, `SCHEDULED`, `EXECUTING` — belong to **contract 06**.

## 16. QA gates

Ten structural gates. Each returns `PASS`, `FAIL` or `UNRESOLVED`.

1. exact product identity
2. exact variant / colourway
3. silhouette
4. geometry / construction
5. relative proportions
6. distinctive details
7. branding / markings when visible
8. hardware / closures where applicable
9. clothing fit integrity when applicable
10. Human Truth integrity when a person is present

### Applicability and result are two dimensions, not one vocabulary

| Dimension | Values |
|---|---|
| **Result**, when a gate *applies* | `PASS` · `FAIL` · `UNRESOLVED` |
| **Applicability marker** | `NOT_APPLICABLE` |

`NOT_APPLICABLE` is **not a fourth evaluation result**. It means the gate does
not apply to that depiction at all, and it asserts nothing about quality.

- `UNRESOLVED` **MUST NOT** be recorded as `PASS`.
- A gate that **applies MUST NOT** be marked `NOT_APPLICABLE` in order to bypass
  it. Doing so is a governance defect, not a result.

These gates evaluate a **generated depiction, after generation**.

**No numeric pass percentage, tolerance or similarity threshold is defined by
this contract.** Avatar Skill v1.3 carries its own test-phase gate
(`productFidelity >= 8`, F04). That number belongs to that skill's test rubric —
which its own SKILL.md calls a test default rather than immutable truth — and is
deliberately **not** promoted into this contract as a constitutional threshold.

## 17. Hard failures

| Failure | Severity |
|---|---|
| `WRONG_PRODUCT` | HARD_FAIL |
| `WRONG_VARIANT` | HARD_FAIL |
| `PRODUCT_GEOMETRY_DRIFT` | HARD_FAIL |
| `PRODUCT_CONSTRUCTION_DRIFT` | HARD_FAIL |
| `DISTINCTIVE_DETAIL_DRIFT` | HARD_FAIL |
| `PRODUCT_TRUTH_CONTRADICTION` | HARD_FAIL |
| `HUMAN_IDENTITY_CONTRADICTION` | HARD_FAIL |
| `CLOTHING_FIT_UNRESOLVED` | **STOP** |
| `UNSUPPORTED_EVIDENCE_TREATED_AS_EXACT` | HARD_FAIL |
| `GENERATOR_CLAIMED_AUTHORITY` | **STOP** |

Related precedent: `FAILURE_TAXONOMY.json → F04_PRODUCT_GEOMETRY_DRIFT`.

## 18. Retry and correction semantics

A failed generation is **evidence about the generation attempt**.

It is **NOT**:

- permission to rewrite Product Truth;
- permission to weaken Product Locks;
- proof that the canonical product reference is wrong.

Any retry **MUST preserve the same underlying Product Truth** unless that truth
is separately corrected through its own authority system.

Spend and correction-credit approval belong to **contract 06**. **No credit
ceiling is defined here.**

> Precedent, Avatar Skill v1.3: *"One failed generation is evidence about the
> pipeline, not permission to rewrite the identity system."*

## 19. The execution layer

CyberNinjas / Studio is an **EXECUTION / GENERATION** layer.

It **may receive** approved context, product references, Product Locks and
creative directives. It **may produce** `GENERATED_OUTPUT`.

It does **NOT** become authority for product identity, product geometry, Product
Truth, Human Truth, approvals or publication.

**An execution layer executes. It does not become an authority by producing
output.**

This contract's validity **does not depend on a provider**: it assumes no
activated subscription and no specific API implementation, and the authority
boundary holds whether or not a provider is connected.

Facts about what happened during one authoring session — whether a provider was
called, whether credits were spent — describe an **operation**, not policy. They
belong in that phase's report, not in a normative contract, and are deliberately
absent here.

## 20. The Product Reference Package

The structure a future Product Creative system assembles **before** generation:

product identity reference · `productGeometrySource` references · optional
`productWearReference` · Product Locks · campaign product role · creative
freedoms · known uncertainties · product confidence · risk classification · QA
requirements · `clothingFitEvidence` when body-worn

**The package is a GENERATION INPUT. It is not a new Product Truth record.**

Because it is assembled **before** generation, it carries only what can
truthfully exist at that moment. It therefore has **no `outputStatus`** and **no
`fitStatus`** — both describe an output that does not exist yet. The schema is
closed (`additionalProperties: false`), which is what keeps them out.

Its builder is **not implemented** in this phase. Instances are snapshots and
**MUST NOT** be committed to this public repository.

## 21. Authority this contract does not grant

Contract 02 grants **no** publication authority, **no** spend authority, **no**
approval authority and **no** Product-Truth write authority.

## 22. Public / private boundary

This repository is **PUBLIC**.

Public-safe and held here: contract, schemas, stable vocabularies, validation
rules, generic QA logic, synthetic fixtures.

**MUST NOT** be committed: unpublished real campaign creative, private campaign
strategy, private character material, private generated likeness output,
credentials and API keys, execution-provider tokens, private customer and
performance data, runtime package instances.

**PINK-MALL-OPS remains PLANNED and MUST NOT be created.**

## 23. Open items

Genuinely undecided. They **MUST NOT** be answered by invention, and a later
system **MUST NOT** assume a default:

exact product-lock enforcement implementation · exact computer-vision QA method ·
numeric geometry tolerances · numeric colour tolerances · numeric logo
similarity thresholds · per-category creative rule set · per-category risk
taxonomy beyond the locked clothing risk · exact Clothing Fit implementation ·
exact external fit-evidence source strategy · automatic retry policy ·
model-specific prompt syntax · model-specific reference limits ·
execution-provider API and node mechanics

## 24. STOP conditions

Stop rather than proceed when:

- a product-led task has no exact-product `productGeometrySource`;
- the only geometry evidence is a similar SKU or a different colourway;
- body-worn clothing lacks sufficient garment-geometry evidence
  (`CLOTHING_FIT_UNRESOLVED`);
- human and product locks cannot both be satisfied;
- an execution layer is being treated as an authority;
- a question maps to no rule here — that is a gap in the contract, not a licence
  to improvise.

## 25. Change control

Durable change follows the parent's change-control protocol: classify, update
the candidate, validate, independent review, then promote to canonical
development.
