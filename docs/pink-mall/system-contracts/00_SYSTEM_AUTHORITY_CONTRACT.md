# PINK MALL — System Authority Contract

| | |
|---|---|
| Contract ID | `PINK_MALL_SYSTEM_AUTHORITY_CONTRACT` |
| Version | `1.0.0` |
| Status | `CANDIDATE` |
| Machine-readable form | `00_SYSTEM_AUTHORITY_CONTRACT.json` |
| Schema | `00_SYSTEM_AUTHORITY_CONTRACT.schema.json` |
| Validator | `tools/regression/system_authority_contract.py` |

## 1. Purpose

This contract defines which system is authoritative for which domain of truth,
how sources are classified, what happens when they disagree, and which data may
exist in a public repository.

It exists because the systems now being planned — campaign, story, social
intelligence, semantic memory, execution and publication — will each hold some
state and each be capable of asserting something. Without a prior agreement
about who decides what, the first disagreement is resolved by whichever system
happens to be asked, which is not a decision procedure at all.

## 2. Scope

This contract is **constitutional**. It binds every PINK MALL / Pierciina
system, current and future.

It deliberately does **not** specify campaign scoring weights, story cadence,
creative-fatigue thresholds, prompt templates, Workstation node architecture,
budget ceilings, output quantities, semantic-memory content, or HQ layout.
Those belong to the domain contracts listed in §23. Where a decision on such a
matter is already locked, this contract records only its **authority
implication** and names the future contract that will carry the detail.

## 3. Canonicality

A contract is canonical only when **all four** conditions hold:

1. it has passed current owner or independent review;
2. it is committed to the canonical project branch `claude/pink-mall-development`;
3. its machine-readable form passes its validator;
4. **its status is not `SUPERSEDED`.**

**A file's existence MUST NOT be read as canonicality.** These same files exist
on a review candidate branch. A candidate branch is review material, not project
truth — but it is the *branch* that makes the difference, not a string inside
the file.

### Two kinds of status label

`status` carries two different kinds of value, and conflating them is what made
an earlier draft of this section incoherent.

| Value | Kind | Effect |
|---|---|---|
| `CANDIDATE` | lifecycle provenance | **Does not by itself deny canonicality.** |
| `CANONICAL` | lifecycle provenance | **Does not by itself grant canonicality.** |
| `SUPERSEDED` | **terminal tombstone** | **Disqualifies reliance**, by condition 4. |

`CANDIDATE` and `CANONICAL` are **location-neutral provenance**. Neither is a
canonicality test: conditions 1–3 decide, and a contract whose status still
reads `CANDIDATE` because it was promoted unchanged **is canonical** once they
hold. No text may call such a file "under review" or "not to be relied upon" on
the strength of the label alone.

`SUPERSEDED` is different in kind. It is a tombstone, and it disqualifies
reliance even while the file is still physically present on the canonical
branch — **because the contract was replaced, not because its historical review
somehow stopped having happened.** That is why retirement is condition 4 and not
a re-reading of condition 1.

**Exact-byte promotion remains the policy.** The reviewed bytes move to the
canonical branch unchanged, status string included. Rewriting a label at
promotion time would mean the promoted artefact is not the reviewed artefact, so
it is never required.

Underlying rule, inherited from `CLAUDE.md` and unchanged here: **GitHub is the
project state; model memory is not.** Work that exists only in an ephemeral
environment and is not committed MUST NOT be treated as canonical.

## 4. Authority domains

Authority is **domain-specific**. There is no single ranking in which one source
beats all others for every question.

The roles are distinct and MUST NOT be conflated:

- the **owner** authorises policy;
- the **canonical repository** persists policy and state;
- **domain authorities** determine facts within their domain;
- **execution systems** act and produce candidates;
- **semantic systems** interpret.

A system does not become a factual authority by having produced an asset, a
recommendation or a plausible sentence.

## 5. Source-of-truth matrix

| Domain | Status | Primary authority | Secondary evidence | Non-authoritative | On conflict |
|---|---|---|---|---|---|
| SYSTEM_GOVERNANCE | ACTIVE | Owner | Canonical repository | Super Brain, chat history, model memory, Workstation | STOP |
| CANONICAL_REPOSITORY_STATE | ACTIVE | Canonical repository | — | Model memory, chat history, Super Brain, Workstation, CyberNinjas | STOP |
| PRODUCT_IDENTITY | ACTIVE | Product onboarding system, canonical repository | Owner | Super Brain, CyberNinjas, Workstation, Social Intelligence | STOP |
| PRODUCT_PRICE | ACTIVE | Owner | Canonical repository | Super Brain, Social Intelligence, CyberNinjas, Workstation | STOP |
| PRODUCT_AVAILABILITY_AND_SIZES | ACTIVE | Owner | Canonical repository | Super Brain, Social Intelligence, CyberNinjas, Workstation | STOP |
| CANONICAL_PRODUCT_MEDIA | ACTIVE | Product onboarding system | Owner | CyberNinjas, Workstation, Super Brain | STOP |
| HUMAN_IDENTITY | ACTIVE | Avatar Skill | Owner | CyberNinjas, Workstation, Super Brain, Story State | STOP |
| AVATAR_CONSENT_STATUS | **BLOCKED** | Owner | Avatar Skill | Super Brain, CyberNinjas, Workstation, chat history | STOP |
| CAMPAIGN_OPERATIONAL_STATE | PLANNED | Campaign Registry | Canonical repository, owner | Super Brain, Story State, Workstation, chat history | STOP |
| STORY_STATE | PLANNED | Story State engine | Campaign Registry, owner | Super Brain, Social Intelligence | STOP |
| SOCIAL_RAW_METRICS | PLANNED | Social platform API | Canonical repository | Super Brain, Social Intelligence, chat history | STOP |
| SOCIAL_INTERPRETATION | PLANNED | Social Intelligence engine | Super Brain | Canonical repository | FLAG_STALE |
| SEMANTIC_CREATIVE_MEMORY | PLANNED | Super Brain | Social Intelligence, Story State | Canonical repository | FLAG_STALE |
| GENERATED_CAMPAIGN_MEDIA | PARTIAL | CyberNinjas Studio | Workstation, Claude orchestrator | Product onboarding system | REJECT_CANDIDATE |
| CAMPAIGN_APPROVAL | PLANNED | Owner | Campaign Registry | Super Brain, Workstation, CyberNinjas, Claude | STOP |
| PAID_GENERATION_AUTHORITY | PLANNED | Owner | Campaign Registry | Super Brain, Workstation, CyberNinjas | STOP |
| COMMERCIAL_PUBLICATION | ACTIVE | Owner | Product onboarding system, canonical repository | Super Brain, Workstation, CyberNinjas, Claude | STOP |
| PRIVATE_STRATEGIC_DATA | PLANNED | Private ops store *(does not exist)* | Owner | Canonical repository | STOP |

## 6. Truth taxonomy

| Class | Definition |
|---|---|
| **FACT** | Direct canonical or verified state, held by the authority for its domain. |
| **DERIVED_FACT** | Deterministic, reproducible result computed from facts by a specified rule. |
| **INTERPRETATION** | Semantic conclusion, hypothesis or learning. Not verifiable by inspecting canonical state. |
| **PROPOSAL** | A suggested future action or creative direction. Carries no authority. |
| **GENERATED_OUTPUT** | Model-created candidate asset or text. A candidate until it passes QA and approval. |
| **APPROVAL** | Explicit authorised acceptance, scoped and recorded. |

These classes **MUST NOT** be collapsed into one another.

- A `GENERATED_OUTPUT` **MUST NOT** become a `FACT` by virtue of having been produced.
- An `INTERPRETATION` **MUST NOT** overwrite a `FACT`.
- A `PROPOSAL` **MUST NOT** be executed as though it were an `APPROVAL`.
- **Silence is never an `APPROVAL`.**

A worked example already canonical in this repository: `newUntil` in the product
record is a `FACT`; membership of NEW IN computed from it by the storefront's
freshness rule is a `DERIVED_FACT`; "this product still feels fresh to the
audience" would be an `INTERPRETATION`.

## 7. Conflict-resolution rules

| Rule | Condition | Action | Auto-resolve |
|---|---|---|---|
| SAME_DOMAIN_CANONICAL_CONFLICT | Two canonical sources in one domain disagree | **STOP** | No |
| SEMANTIC_VS_CANONICAL | Semantic/generated state disagrees with canonical truth | CANONICAL_WINS | Yes — flag the stale state |
| GENERATED_VS_PRODUCT_TRUTH | Generated output contradicts product truth or identity | REJECT_CANDIDATE | Yes |
| OWNER_VS_DURABLE_CONTRACT | New owner instruction conflicts with a durable contract | CLASSIFY_OVERRIDE | No |
| CROSS_DOMAIN_PRECEDENCE | Sources in different domains appear to disagree | ROUTE_TO_DOMAIN_AUTHORITY | Yes |
| UNKNOWN_DOMAIN | Question maps to no defined domain | **STOP** | No |

An undefined domain is a gap in this contract, not a licence to improvise.

### Worked examples

**1 — Super Brain says PM-038 costs X; the canonical catalogue says Y.**
The canonical catalogue wins. `PRODUCT_PRICE` is owner-authored and
repository-persisted; Super Brain is explicitly non-authoritative for price. The
Super Brain memory is stale and MUST be flagged for correction.

**2 — Workstation generates a beautiful shoe with the wrong sole geometry.**
The output is rejected or sent to exception review. `GENERATED_CAMPAIGN_MEDIA`
never redefines `PRODUCT_IDENTITY`. A more attractive image is not a product
fact.

**3 — Story memory says INA appeared in the last campaign; the Campaign
Registry says SIS.** The Campaign Registry wins for operational fact; semantic
memory MUST be corrected. *(Both systems are PLANNED; this is the rule that will
apply when they exist.)*

**4 — The owner approves a one-time creative exception.** Only that campaign is
affected. The global contract does **not** silently change. PM-041's
owner-approved single-image publication is the existing precedent: the
three-image media contract remained in force for every other product.

**5 — Two canonical GitHub sources disagree on publication state.** **STOP** and
reconcile. Do not silently choose the more convenient one.

## 8. Owner authority

The owner is the ultimate business-policy approver. That authority is real and
this contract does not constrain it. What the contract constrains is how an
owner decision becomes **durable system policy**.

- Silence is never approval.
- Chat history is never sufficient evidence of a durable rule when a canonical
  contract says otherwise.
- The owner authorises policy; the repository persists it; domain authorities
  determine facts. These are different acts.

## 9. One-time exception vs durable policy change

Every owner instruction that conflicts with a durable contract MUST be
classified before it is acted on.

| | ONE_TIME_EXCEPTION | DURABLE_POLICY_CHANGE |
|---|---|---|
| Scope | A named product, campaign or action | How the system operates from now on |
| Mutates policy | **No** | **Yes** |
| Requirement | Recorded with its scope | MUST be reflected in the relevant canonical contract before any later system treats it as permanent |

Until a proposed durable change completes change control (§21) it is a
`PROPOSED_DURABLE_CHANGE`, not policy.

## 10. Product Truth

The existing product-onboarding system remains authoritative for product
publication workflow, unchanged by this contract.

Product truth includes manufacturer identity, PM ID, owner-authoritative price,
owner-authoritative available sizes, approved factual enrichment, canonical
product media and publication state.

- Product facts **MUST NEVER** be invented.
- Generated campaign media **MUST NEVER** become canonical commerce media.
- Canonical product photography and generated campaign photography are separate
  media classes (§16) and separate storage paths.

## 11. Human Truth

INA / SIS identity truth belongs to the validated Avatar system.

- Identity **MUST NOT** be inferred from generated output.
- One sister **MUST NEVER** be substituted for the other.
- Reference wardrobe is **not** automatically identity truth.

**Consent status.** `CONSENT_AND_PROVENANCE.json` currently records
`OWNER_CONFIRMATION_REQUIRED` for every subject and every allowed use —
including `commercialCampaign`, `aiGeneratedLikeness` and `socialDistribution` —
and records `library.publicRepositoryExposure: PROHIBITED`.

Commercial generated-likeness publication therefore remains **BLOCKED** behind
the Consent Gate. **This contract does not assert, and MUST NOT be read as
asserting, that commercial consent has been completed.**

## 12. Operational Truth

Campaign Registry, Story State, approval state, Campaign Execution Plan, current
campaign status and creative-fatigue state are **PLANNED**. They do not exist
canonically.

Authority is reserved for them here so that later contracts inherit a defined
position. Until they exist:

- operational state **MUST NOT** be fabricated;
- no system may claim campaign operational fact;
- absence of a registry is not a reason to treat semantic memory as one.

## 13. Social Data Truth

Raw platform metrics are **evidence** (`FACT` within `SOCIAL_RAW_METRICS`).

Conclusions drawn from them — "this concept is strong", "the audience is
fatigued", "TEAM SIS is resonating" — are **INTERPRETATION**.

This contract defines only that distinction. Weighting, scoring and thresholds
belong to the future Social Intelligence contract (04).

## 14. Semantic Memory

Super Brain is intended to hold interpretation, learning, campaign memory,
creative patterns, audience interpretation, preference drift and useful semantic
relationships.

Super Brain is **NOT** authoritative for: PM IDs; prices; sizes; stock and
availability; canonical product identity; approval state; exact current branch
or hash; exact campaign spend; exact publication state.

> **GitHub wins for factual and canonical truth. Super Brain may govern
> interpretation, not canonical facts.**

**Autonomy is a target state, not a current capability.** The intended
architecture — social data plus trend data plus campaign history plus PINK MALL
context, producing content intelligence and eventually earned autonomy — is
design, not implementation. An aspirational capability **MUST NEVER** be
documented as an implemented feature.

## 15. Execution-layer authority

Claude is the intended architect, orchestrator and QA operator. CyberNinjas
Studio and other model providers are execution and generation systems. The
Workstation is the intended persistent visual workflow graph (PLANNED).

These systems **MAY** generate, transform, propose, render, compare and
organise. They **MUST NOT** become canonical factual authority merely because
they produced an asset or a recommendation.

**Generated output is a candidate until it passes required QA and approval.**

## 16. Media classes

| Class | What it is | Generative alteration | Rule |
|---|---|---|---|
| **CANONICAL_COMMERCE_MEDIA** | Exact approved product media used for product and storefront truth | **Never** | MUST NOT be generatively altered or replaced by other classes |
| **CAMPAIGN_MEDIA** | Generated or campaign-directed creative media that may place real products and INA/SIS inside a campaign world | Allowed | MUST remain product-locked and identity-locked |
| **DERIVATIVE_MEDIA** | Crops, story adaptations, reels, overlays, captions, derivative formats | Allowed | Inherits its source's constraints |

Campaign and derivative media **MUST NEVER** silently replace canonical commerce
media. An asset of unknown class MUST be treated as `GENERATED_OUTPUT` and MUST
NOT be published.

## 17. Approval and publication authority

Human approval remains the **current default** for commercial publication. No
system holds autonomous publishing authority under this contract.

**Paid generation — authority implication only.** The locked principle is that
once the owner approves a campaign idea *and* selects a budget mode, planned
paid generation may proceed within that approved ceiling; if the first planned
batch fails QA and correction spend is needed, owner review is required before
that additional spend. This contract records the authority shape and nothing
else. Budget modes, ceilings and credit limits are **not defined here** and
belong to **contract 06 — Automation & Approval**.

A *Campaign Execution Plan* may be a structured object that a future domain
contract defines or references. It is **not** a separate numbered contract in
the 00–08 sequence, and it MUST NOT be cited as one unless the owner creates it
through durable change control.

## 18. Earned autonomy

Autonomy is **capability-specific**, not one global on/off flag. Candidate
capability domains include concept selection, image generation, identity QA,
product QA, video, copy and publication.

A system MAY earn autonomy in one domain while remaining manual in another. Any
grant MUST be made explicitly by a later contract change, based on proven
history. **No confidence thresholds are defined by this contract, and no
autonomous authority is granted by it.**

## 19. Public / private data boundary

`PIERCIINA-PROJECT` is a **PUBLIC** repository.

**PUBLIC_SAFE** — MAY live here: software; schemas; public-safe contracts;
validation rules; generic campaign architecture; non-private manifests; public
product truth; storefront assets already approved for publication.

**PRIVATE_OPS_REQUIRED** — MUST NOT live here: private INA/SIS/DUO source
photographs; SAFE20 source photographs; private contact sheets; private
generated likeness tests; raw private customer data; detailed Creative Director
personal profile; private performance history not intentionally public; Super
Brain exports containing private strategy or history; unpublished confidential
campaign strategy; sensitive internal commercial analysis; private likeness
provenance where required.

**NEVER_PERSIST_IN_ANY_REPOSITORY**: credentials, API tokens, social account
credentials, private keys.

Git LFS does not make public material private.

The intended private store is named **PINK-MALL-OPS**. It is **PLANNED**. It
does not exist, MUST NOT be described as existing, and MUST NOT be created
without a separate explicit authorisation. Until it exists, PRIVATE_OPS_REQUIRED
material is held outside version control.

## 20. Current vs target architecture

| State | Systems |
|---|---|
| **ACTIVE** | canonical GitHub project state; PINKMALL storefront; product onboarding; media acquisition; publication regression; viewport smoke; fashion-context contract; Avatar Skill architecture (v1.2, v1.3); Studio Jewelry canonical mapping (documentation); Avatar Masterclass (instructional) |
| **PARTIAL** | Avatar generation capability via CyberNinjas Studio — connected and exercised, not cleared for commercial likeness publication |
| **BLOCKED** | commercial generated-likeness publication — consent gate unresolved |
| **PLANNED** | Campaign Context Builder; Campaign Registry; Story State engine; Social Intelligence engine; Creative Fatigue engine; PINK MALL HQ; campaign Workstation automation; Super Brain data bridge; automated social publishing; analytics feedback loop; PINK-MALL-OPS private store |
| **HISTORICAL** | `claude/pink-mall-hero-carousel-jvhdb8` — preserved, superseded, not merged |

Current autonomy **MUST NOT** be overclaimed. Every system referenced anywhere
in this contract carries an implementation status.

## 21. Change-control protocol

```
NEW OWNER DECISION
      ↓
CLASSIFY — one-time exception, or durable policy change
      ↓  (durable only)
UPDATE CONTRACT CANDIDATE
      ↓
VALIDATE
      ↓
INDEPENDENT REVIEW
      ↓
PROMOTE TO CANONICAL DEVELOPMENT
      ↓
later systems may rely on it
```

**Chat memory alone MUST NOT become permanent policy.**

## 22. Failure and STOP conditions

Work MUST stop, and the condition MUST be reported rather than worked around,
when any of these holds:

| Stop | Condition |
|---|---|
| SAME_DOMAIN_CANONICAL_CONFLICT | Two canonical sources in one domain disagree |
| UNDEFINED_AUTHORITY_DOMAIN | A question maps to no defined domain |
| CONSENT_GATE_UNRESOLVED | Commercial generated-likeness publication attempted while consent is unresolved |
| PRIVATE_MATERIAL_IN_PUBLIC_DIFF | Private or never-persist material appears in a public-repository change |
| GENERATED_OUTPUT_AS_CANONICAL | Generated media or text is about to be written into a canonical factual path |
| UNAPPROVED_PUBLICATION | Commercial publication attempted without explicit recorded approval |
| UNCOMMITTED_STATE_TREATED_AS_CANONICAL | Ephemeral work is about to be treated as project truth |
| POLICY_MUTATION_WITHOUT_CHANGE_CONTROL | A durable rule is about to change without change control |

## 23. Relationship to future domain contracts

This contract is constitutional. Domain contracts inherit from it and MUST NOT
contradict it; where one needs to, that is a durable policy change and goes
through §21.

| # | Contract | Status |
|---|---|---|
| 00 | System Authority | **this document** — CANDIDATE |
| 01 | Campaign Context | NOT YET CREATED |
| 02 | Product Creative | NOT YET CREATED |
| 03 | Character & Story | NOT YET CREATED |
| 04 | Social Intelligence | NOT YET CREATED |
| 05 | Workstation Operating | NOT YET CREATED |
| 06 | Automation & Approval | NOT YET CREATED |
| 07 | Super Brain Memory | NOT YET CREATED |
| 08 | PINK MALL HQ | NOT YET CREATED |

Locked decisions that belong to those contracts are recorded in
`DECISION_COVERAGE_MATRIX.md` so that a decision already taken is not lost
merely because its detailed contract has not been written yet.

## Creative freedom — governing principle

> **World physics may break. Product truth may not. Human identity may not.**

Creative systems MAY transform environment, scale, story, absurdity, atmosphere,
composition, narrative and visual genre. They MUST NOT silently transform
intrinsic product truth or human identity.
