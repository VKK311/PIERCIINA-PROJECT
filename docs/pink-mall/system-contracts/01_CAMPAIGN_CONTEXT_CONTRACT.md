# PINK MALL — Campaign Context Contract

| | |
|---|---|
| Contract ID | `PINK_MALL_CAMPAIGN_CONTEXT_CONTRACT` |
| Contract number | `01` |
| Version | `1.0.0` |
| Status | `CANDIDATE` *(provenance only — canonicality follows Contract 00 §3)* |
| Parent | `PINK_MALL_SYSTEM_AUTHORITY_CONTRACT` |
| Machine-readable | `01_CAMPAIGN_CONTEXT_CONTRACT.json` |
| Schemas | `01_CAMPAIGN_CONTEXT_CONTRACT.schema.json`, `01_CAMPAIGN_CONTEXT_OBJECT.schema.json` |
| Validator | `tools/regression/campaign_context_contract.py` |

## 1. Purpose

Define how a campaign context is assembled, what may influence it, what may not,
and what a Campaign Context package contains — so that ideation starts from a
creative premise rather than a SKU, and so that no later system can quietly
promote a trend signal into a fact.

## 2. Scope

**Covers:** idea-first context assembly; input domains and their provenance; the
authority of cultural and social signals; product and character role
vocabularies; creative freedom and brand specificity; the three-idea proposal
rule; the Campaign Context package shape; behaviour when an optional input does
not exist.

**Does not cover:** product-lock enforcement mechanics (02); character canon and
story continuity (03); metric weighting, scoring and fatigue thresholds (04);
workflow graph and run model (05); approval flow, budget modes and spend
ceilings (06); semantic memory schema (07); HQ surface (08).

**Implementation status: `PLANNED`.** No Campaign Context Builder exists. This
contract defines the shape and rules a future builder MUST satisfy. It does not
create one.

## 3. Parent authority and inheritance

This contract inherits every rule of the System Authority Contract and **MUST
NOT** contradict it. Where the two disagree, the parent governs and the
disagreement is a defect in this contract.

Its `status` is provenance only. Canonicality is decided by the parent's four
conditions: current review, canonical branch, passing validator, not
`SUPERSEDED`. Files existing on a candidate branch are review material.

## 4. Idea-first principle

Campaign Context is **IDEA-FIRST**, not product-first by default.

It starts from *"what world, story, cultural moment or creative premise should
PINK MALL enter?"* — **not** from *"which SKU should we advertise?"*

A product MAY be central, supporting, a detail, or absent. A campaign **MUST
NOT** be required to originate from a product. When a real product is used,
every factual attribute **MUST** come from Product Truth, without exception.

## 5. Input domains

| Domain | Requirement | Default class | Provider status |
|---|---|---|---|
| `WORLD_STORY_STATE` | optional | operational state | **PLANNED** |
| `CULTURAL_SOCIAL_SIGNALS` | optional | social/cultural signal | **PLANNED** |
| `BRAND_DNA_HERITAGE` | **required truth** | canonical fact | ACTIVE |
| `CHARACTER_CONTEXT` | optional | canonical fact | ACTIVE |
| `CURRENT_PRODUCTS` | **required truth** | canonical fact | ACTIVE |
| `TARGET_FORMAT` | **required truth** | locked owner decision | ACTIVE |

`TARGET_FORMAT` is the intended communication surface or output family. It is
deliberately **concept-level**: campaign image, social series, reel or video
concept, editorial, activation and other future formats are examples, **not** a
closed enum. No exhaustive creative-format vocabulary is locked.

## 6. Input availability and provenance

| Requirement class | Absence behaviour |
|---|---|
| `REQUIRED_TRUTH_INPUT` | **STOP.** Ideation MUST NOT proceed. |
| `OPTIONAL_CONTEXT_INPUT` | Recorded as absent. Ideation MAY proceed from available canonical inputs. |

Every input carries an explicit availability: `AVAILABLE`, `UNAVAILABLE` or
`NOT_APPLICABLE`. **Absence MUST be declared, never implied.**

Every input also carries an explicit provenance class. The vocabulary is closed:

| Input class | Authoritative | Meaning |
|---|---|---|
| `CANONICAL_FACT` | yes | Canonical state from the domain's authority under contract 00. |
| `DERIVED_FACT` | yes | Deterministic result computed from canonical facts by a published rule. |
| `LOCKED_OWNER_DECISION` | yes | A decision the owner has locked. |
| `OPERATIONAL_STATE` | yes | Recorded state of a running system. |
| `SOCIAL_OR_CULTURAL_SIGNAL` | no | External evidence. Inspiration only. |
| `SEMANTIC_INTERPRETATION` | no | A reading, not a fact. |
| `PRIVATE_OPS_REFERENCE` | no | A pointer to private material held outside this repository. |
| `UNAVAILABLE_INPUT` | no | The input could not be obtained. |

**No input class may override truth.** Authority to *inform* is not authority to
*overwrite*: even a `CANONICAL_FACT` enters the context as an input, and the
domain authorities in contract 00 remain the only source that may change it.

Story State, the social bridge and semantic memory are `PLANNED`. Their inputs
are expected to read `UNAVAILABLE` today, and that is a **correct result**, not
a failure.

## 7. Trend and social signal authority

Cultural and social signals are **EVIDENCE**. They are not authority.

They **MUST NOT** override Product Truth, Human Truth, PINK MALL heritage, or
any approval. Model knowledge **MUST NOT** be presented as current social
evidence. A signal whose feed does not exist is recorded `UNAVAILABLE` and
**MUST NOT** be reconstructed from memory. An interpretation **MUST NOT** be
recorded as a fact.

Signals may inspire. They may not overwrite truth.

## 8. PINK MALL heritage constraint

Campaign context **MUST** remain recognisably from the PINK MALL / Pierciina
world. Heritage comes from the existing canonical Avatar Skill v1.3 brand and
heritage documents. This contract **MUST NOT** define a second brand-DNA
authority.

## 9. Product-role model

| Role | Meaning |
|---|---|
| `NONE` | No specific product is required in the concept. |
| `DETAIL` | A product appears as a meaningful detail. |
| `SUPPORTING` | A product contributes materially but is not the whole idea. |
| `HERO` | A specific product is deliberately central. |

`HERO` **MUST NOT** be required. `NONE` is always permitted. Whenever a real
product is named at any role, every factual attribute **MUST** come from Product
Truth. Additional constraints on product-led contexts belong to **contract 02**
and **MUST NOT** be duplicated here.

## 10. Character-role model

`INA` · `SIS` · `DUO` · `NONE`.

This is a **campaign role selector, not identity truth**. Human identity remains
governed by the Avatar Skill and **MUST NOT** be redefined here. Personality and
relationship roles are **dynamic**: no fixed permanent archetype may be encoded —
not "INA always X, SIS always Y". Character canon and story continuity belong to
**contract 03**. Commercial generated-likeness publication remains gated by the
parent's consent stop.

## 11. Creative freedom

World-building is primary. A campaign world MAY be surreal, absurd, cinematic,
funny, glamorous, ugly-on-purpose, nostalgic, editorial, chaotic, quiet,
dramatic, documentary-like, fantastical — or any other idea-serving direction.

**That list is illustrative, not a closed enum.** PINK MALL **MUST NOT** be
narrowed into one permanent visual genre.

> **World physics may break. Product truth may not. Human identity may not.**

## 12. Generic-AI hard failure

An idea that could belong to any generic AI fashion, pink or luxury brand is a
**failure**, not a weak result.

`GENERIC_AI_AESTHETIC = HARD_FAIL`

Named failure modes: generic futuristic pink mall; generic luxury campaign;
generic Barbie-like pink world; generic chrome AI aesthetic; generic anonymous
fashion editorial.

Brand specificity is judged against the existing canonical heritage definitions,
not against a second authority invented here.

## 13. Three-idea proposal rule

In `INITIAL` mode an ideation cycle **MUST** produce **exactly three** competing
campaign/story ideas. Fewer or more is a STOP condition.

Selection authority is the **OWNER**. No autonomous winner exists. No ranking
threshold or scoring formula is defined, and none may be assumed.

## 14. Proposal versus approval

Every idea is a `PROPOSAL` until explicitly selected.

```
PROPOSAL --(OWNER)--> OWNER_SELECTED
```

Owner selection grants **nothing else**. It does **not** authorise paid
generation, publication, auto-publishing, additional spend or autonomous
execution. Those belong to **contract 06** and to the parent's
`COMMERCIAL_PUBLICATION` and `PAID_GENERATION_AUTHORITY` domains.

## 15. Campaign Context object model

Defined by `01_CAMPAIGN_CONTEXT_OBJECT.schema.json`. A package carries
`schemaVersion`, `contextRef`, `generatedAt`, `inputSummary`,
`brandConstraints`, `truthConstraints`, `targetFormat` and exactly three
`ideas`.

Each idea carries `ideaRef`, `title`, `worldPremise`, `purpose`, `productRole`,
`characterRole`, `targetFormatIntent`, `creativeMechanisms`, `truthRisks`,
optional `privateDetailRefs`, and `state`.

`contextRef` and `ideaRef` are **opaque within one package**. No persistent
campaign ID format is defined here; that belongs to a future operational system.

**Instances MUST NOT be committed** to this public repository — a stale snapshot
silently becomes wrong, and a real campaign context is unpublished strategy.

## 16. Missing-input behaviour

An input that cannot be obtained **MUST** be recorded `UNAVAILABLE` and **MUST
NOT** be replaced with fabricated state. Absence of an optional input **MUST
NOT** stop ideation. Absence of a required truth input **is** a STOP condition.

## 17. Public / private boundary

Public-safe and belonging here: this contract, its schemas, vocabularies,
validation rules, synthetic fixtures and generic architecture.

`PRIVATE_OPS_REQUIRED` and **MUST NOT** appear here: unpublished real campaign
concepts; owner private creative strategy; sensitive audience or performance
interpretation; private competitor analysis; private character material;
Creative Director preference history; private semantic memory; private
social-account data.

A `PRIVATE_OPS_REFERENCE` may record **that** such material exists. Its
**content MUST NOT** appear.

## 18. Dependencies on future contracts

| Contract | Dependency |
|---|---|
| 02 Product Creative | product-led creative constraints and product-lock enforcement |
| 03 Character & Story | character canon, story continuity, narrative state |
| 04 Social Intelligence | signal weighting, scoring, creative fatigue |
| 06 Automation & Approval | approval flow, budget modes, spend ceilings, earned autonomy over selection |
| 07 Super Brain Memory | semantic memory that may inform, never authorise, an idea |

None of these exists. They **MUST NOT** be cited as authority.

## 19. Open items

Genuinely undecided, and **MUST NOT** be answered by invention or assumed by
default: exact external trend and social providers; ingestion and API
implementation; signal freshness windows; numeric signal weighting; autonomous
idea-selection threshold; autonomous idea-selection policy; persistent Campaign
Context ID format; exact scoring formula; private campaign-strategy storage
implementation.

## 20. STOP and rejection conditions

| Condition | Severity |
|---|---|
| Canonical Product Truth contradicted | HARD_FAIL |
| Human identity contradicted, including sister substitution | HARD_FAIL |
| Idea collapses into generic AI aesthetic with no PINK MALL specificity | HARD_FAIL |
| A required truth input is missing | STOP |
| A supposedly current signal is fabricated | STOP |
| A signal or interpretation is used as canonical authority | STOP |
| Other than exactly three proposals in INITIAL mode | STOP |
| An idea is treated as approved without owner selection | STOP |
| Private material would be written into the public repository | STOP |

No numeric thresholds are defined by this contract.

## 21. Change control

Durable change follows the parent's protocol: classify as one-time exception or
durable policy change; update the candidate; validate; independent review;
promote. **Chat memory alone MUST NOT become permanent policy.**
