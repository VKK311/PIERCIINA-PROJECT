# PINK MALL — Workstation Operating Contract

| | |
|---|---|
| Contract ID | `PINK_MALL_WORKSTATION_OPERATING_CONTRACT` |
| Version | `1.0.0` |
| Status | `CANDIDATE` |
| Machine-readable form | `05_WORKSTATION_OPERATING_CONTRACT.json` |
| Schema | `05_WORKSTATION_OPERATING_CONTRACT.schema.json` |
| Validator | `tools/regression/workstation_operating_contract.py` |

## 1. Purpose

This contract defines the public-safe operating boundary for the planned PINK
MALL Workstation: the persistent visual workflow model in which campaign work
moves from an approved idea through creative checkpoints to a final candidate.

It exists to preserve the locked owner decisions for the Workstation domain
without inventing implementation details that remain open.

**The Workstation is PLANNED. This contract does not create a Workstation
runtime, a CyberNinjas node graph, a campaign station instance, or a paid
generation run.**

## 2. Canonicality and inheritance

This contract inherits the System Authority Contract in full. Its file status is
provenance, not canonicality. Canonicality is decided only by the four
conditions in Contract 00.

GitHub is the project state. A workstation artefact that exists only in a chat,
model context or ephemeral execution environment is not canonical project
state.

## 3. Scope

### Covers

- the PINK MALL HQ / Master Station and per-campaign station model;
- the lifecycle of a campaign station from approved idea to final candidate;
- the locked creative checkpoints;
- candidate/output state separation;
- provenance and lineage requirements for generated work;
- the normal initial image exploration pattern;
- the conceptual ECONOMY / STANDARD / PREMIUM budget-mode interface;
- the boundary between Workstation execution, QA, approval and publication;
- failure, rejection and rework semantics.

### Does not cover

- exact CyberNinjas node types or node wiring;
- whether the current CyberNinjas control surface can manipulate every required node;
- final serialized station-template implementation;
- budget ceilings, credit limits or correction-spend amounts;
- approval authority or autonomous publication;
- social metrics or interpretation;
- Super Brain memory storage;
- PINK MALL HQ UI implementation.

Those questions remain with the owner or Contracts 06–08 as recorded in the
Decision Coverage Matrix.

## 4. Operating model

The Workstation has two structural levels:

1. **PINK MALL HQ / Master Station** — the top-level operating surface for
   campaign work.
2. **One separate station per campaign** — an isolated execution workspace for
   the approved campaign idea.

Once an idea has been approved by the owner, construction of that campaign's
station may begin **without another architecture approval**.

This permission is about station construction only. It does not grant approval
to publish, spend beyond the authorised budget mode, alter Product Truth,
alter Human Identity, or skip QA.

## 5. Campaign station lifecycle

The locked checkpoint sequence is:

`CONCEPT → IMAGES → VIDEO (if applicable) → FINAL`

These are **workflow checkpoints**, not proof of approval or publication.

| Checkpoint | Meaning | Required boundary |
|---|---|---|
| CONCEPT | The approved campaign idea is represented as an executable creative brief. | Owner approval of the idea is already recorded before campaign-station construction. |
| IMAGES | Candidate image directions are generated and evaluated. | Initial exploration normally contains 2–3 meaningfully different variants. |
| VIDEO | Optional candidate video work derived from an approved campaign direction. | Only applicable when the campaign requires video. |
| FINAL | Candidate package assembled for final QA and approval. | FINAL is not publication authority. |

A checkpoint MUST NOT silently promote a proposal to approval, a generated output
to Product Truth, or a candidate to publication.

## 6. Initial image exploration

The normal image phase explores **2–3 meaningfully different variants**.

"Meaningfully different" refers to creative direction, composition, treatment,
or other intentional visual approach. It does not authorise product drift or
identity substitution.

The quantity is a normal operating pattern, not a universal fixed output
quota. A campaign may require a different quantity when its approved scope
requires it.

A single generated result MUST NOT be treated as evidence that a permanent
creative rule has been established.

## 7. Model selection

**Claude selects the generation model.**

Model selection is an execution decision. It does not transfer authority for
Product Truth, Human Identity, approval, publication or spend.

The Workstation contract intentionally does not freeze a provider, model name,
node implementation, prompt template or routing algorithm. Those are
implementation details and may change without changing the operating contract.

## 8. Budget modes

The Workstation exposes three conceptual budget modes:

- **ECONOMY**
- **STANDARD**
- **PREMIUM**

These are mode names, not numeric ceilings.

This contract does **not** define:

- credits;
- currency ceilings;
- per-run spend;
- correction-spend allowance;
- provider-specific prices;
- autonomous-spend thresholds.

Those values belong to Contract 06. A Workstation run MUST NOT infer a numeric
ceiling from the mode name alone.

Owner approval of a campaign idea plus budget mode may authorise planned
first-batch spend only within the future rules and ceiling established by
Contract 06.

## 9. Output and candidate states

The Workstation distinguishes execution output from accepted business state.

Minimum public-safe state vocabulary:

| State | Meaning |
|---|---|
| `PROPOSAL` | Suggested creative direction, not yet an executed output. |
| `GENERATED_OUTPUT` | Output produced by an execution step. |
| `CANDIDATE` | Generated output currently under QA or approval consideration. |
| `REJECTED` | Candidate failed a required gate or was not accepted. |
| `APPROVED` | Explicit owner approval exists for the scoped use. |
| `PUBLISHED` | Publication authority has executed publication. |

A generated output starts as `GENERATED_OUTPUT` and remains a candidate until
the required QA and approval boundaries are satisfied.

The Workstation MUST NOT manufacture `APPROVED` or `PUBLISHED` state from
generation success, checkpoint completion, model confidence, or operator
silence.

## 10. Provenance and lineage

Every executable output MUST be traceable to its originating station, campaign
and workflow checkpoint.

Public-safe provenance must be sufficient to answer:

- which campaign station produced the output;
- which checkpoint produced it;
- which parent output or input it derives from, when applicable;
- which execution model/provider was selected;
- whether the output is original generation or derivative work;
- which QA disposition currently applies.

Opaque identifiers are preferred for runtime objects. This contract does not
define a persistent campaign ID format.

Private prompts, private source photographs, credentials, raw customer data and
private performance history MUST NOT be embedded in public repository
provenance.

## 11. Product and Human Truth boundaries

The Workstation is an execution layer, not a factual authority.

It MUST inherit Contract 00 and Contract 02:

- Product Identity, price, availability, sizes and canonical commerce media
  remain authoritative elsewhere.
- Campaign media MUST NOT silently replace canonical commerce media.
- Human Identity remains authoritative with the Avatar Skill.
- One sister MUST NOT be substituted for the other.
- Generated likeness MUST NOT be treated as identity evidence.
- A visually successful output with wrong product geometry or wrong identity is
  still a failed candidate.

The Workstation may transform the world around Product Truth and Human Truth.
It may not rewrite either.

## 12. QA boundary

The Workstation produces candidates. QA decides whether a candidate is fit to
advance.

At minimum, the Workstation lifecycle must support a disposition of:

- `PASS`
- `FAIL`
- `UNRESOLVED`

A failed or unresolved candidate MUST NOT be silently promoted.

A rework loop may return a candidate to an earlier checkpoint. Rework does not
erase the failed attempt; provenance should preserve the lineage.

The Workstation itself does not define numeric similarity tolerances, fatigue
thresholds, approval thresholds or publication rules. Those belong to their
own authorities.

## 13. Rejection and rework

A rejection is a disposition on a candidate, not permission to weaken a lock.

Typical classes include:

- product-fidelity failure;
- human-identity failure;
- missing required evidence;
- technical generation failure;
- QA failure;
- approval refusal.

The Workstation MAY generate a replacement candidate after failure when the
applicable execution/approval rules permit it.

**Additional paid correction spend after a failed QA batch requires owner review**
under the locked approval model; the numeric spend rules belong to Contract 06.

## 14. Final checkpoint

`FINAL` means the campaign station has assembled the candidate package needed
for final review.

It does not mean:

- owner approval happened;
- commercial publication is authorised;
- a social platform accepted the content;
- a story transition occurred;
- Product Truth changed.

Final approval and publication remain outside this contract.

## 15. Runtime existence boundary

This contract is a specification only.

It does not assert that any of the following currently exists:

- a Workstation runtime;
- a reusable campaign-station template;
- a CyberNinjas node graph implementing this contract;
- an automated paid-generation runner;
- a campaign execution instance.

Current lifecycle values for named systems are owned by Contract 00's source
registry and MUST be read there.

## 16. Deferred implementation decisions

The following are deliberately open:

1. exact CyberNinjas node implementation;
2. programmatic control coverage of the required nodes;
3. final station-template serialization;
4. exact runtime persistence technology;
5. exact provider/model routing mechanics;
6. exact observability and retry implementation.

An implementation may choose among these without changing the locked operating
model, provided it does not contradict a canonical contract.

## 17. Hard failures

| Failure ID | Meaning | Severity |
|---|---|---|
| `UNAUTHORISED_STATION_CONSTRUCTION` | A campaign station is constructed as though an unapproved idea were approved. | STOP |
| `CHECKPOINT_ORDER_BYPASS` | Required checkpoints are silently skipped or represented as completed without their work. | HARD_FAIL |
| `GENERATED_AS_APPROVED` | Generation success is treated as owner approval. | HARD_FAIL |
| `GENERATED_AS_PUBLISHED` | Generation or FINAL state is treated as publication. | STOP |
| `PRODUCT_TRUTH_MUTATION` | Workstation output attempts to rewrite Product Truth. | STOP |
| `HUMAN_TRUTH_MUTATION` | Workstation output attempts to rewrite Human Identity. | STOP |
| `NUMERIC_BUDGET_INVENTION` | A budget mode is given a ceiling not supplied by its authority. | HARD_FAIL |
| `PRIVATE_DATA_IN_PUBLIC_PROVENANCE` | Private operational or likeness material is persisted in the public repo. | STOP |
| `FAILED_CANDIDATE_PROMOTED` | FAIL/UNRESOLVED candidate is advanced without the required gate. | HARD_FAIL |
| `RUNTIME_EXISTENCE_FABRICATION` | A contract or schema is cited as proof that the Workstation runtime exists. | STOP |

## 18. Authority grants

This contract grants:

- no Product Truth authority;
- no Human Identity authority;
- no Story State transition authority;
- no approval authority;
- no publication authority;
- no spend authority;
- no autonomous authority.

The Workstation is an execution and organisation layer.

## 19. Public/private boundary

This repository is public.

Safe here:

- this contract;
- schemas;
- validators;
- public-safe station architecture;
- synthetic fixtures.

Not safe here:

- private source photographs;
- private likeness tests;
- private campaign strategy;
- raw social performance history;
- credentials or tokens;
- private customer data;
- confidential spend records.

The intended private ops store remains governed by Contract 00 and does not become
real merely because this contract references the boundary.

## 20. Relationship to later contracts

- **Contract 06** owns approval flow, budget ceilings, credit limits,
  correction-spend rules and earned autonomy.
- **Contract 07** owns Super Brain memory and durable-learning rules.
- **Contract 08** owns HQ operating surface and visibility.
- **Contract 02** owns Product Creative / Product Lock rules.
- **Contract 03** owns Character & Story / Story State rules.
- **Contract 04** owns Social Intelligence interpretation and recommendation.

Authoring those later contracts MUST NOT require this contract to cache their
runtime existence.

## 21. Summary rule

> **The Workstation executes approved creative work through explicit checkpoints;
> it produces candidates, preserves provenance, and stops at QA/approval
> boundaries. It may make the world around Product Truth and Human Truth
> flexible, but it may never make those truths flexible.**
