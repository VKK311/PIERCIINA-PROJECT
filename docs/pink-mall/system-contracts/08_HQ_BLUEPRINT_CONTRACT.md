# PINK MALL — HQ Blueprint Contract

| | |
|---|---|
| Contract ID | PINK_MALL_HQ_BLUEPRINT_CONTRACT |
| Version | 1.0.0 |
| Status | CANDIDATE |
| Machine-readable form | 08_HQ_BLUEPRINT_CONTRACT.json |
| Schema | 08_HQ_BLUEPRINT_CONTRACT.schema.json |
| Validator | tools/regression/hq_blueprint_contract.py |

## 1. Purpose

This contract defines the public-safe blueprint and authority boundary for the planned **PINK MALL HQ / Master Station**.

HQ is the operating surface that brings together campaign, story, approval, learning and creative-work visibility. It is a surface over authoritative systems; it is not a new source of truth.

**HQ is PLANNED. This contract does not create an HQ runtime, dashboard, Campaign Registry, Workstation runtime, Super Brain runtime, private ops store, social connector or autonomous execution service.**

## 2. Canonicality and inheritance

This contract inherits Contract 00 in full. Its lifecycle status is provenance, not canonicality. Canonicality is determined only by Contract 00's four conditions.

The HQ MUST read current state from the authority that owns that state. It MUST NOT reconstruct current operational truth from stale UI state, model memory, chat history or semantic memory.

## 3. Locked HQ surface

The locked public-safe HQ blueprint contains:

- **CURRENT STORY**
- **ACTIVE CAMPAIGNS**
- **WAITING FOR APPROVAL**
- recent winner / social signals
- **creative-fatigue visibility**
- **NEXT 3 IDEAS**
- credit and cost visibility
- **EXPERIMENT LAB**
- **WORLD / STORY MAP**
- a separate **REJECTS & LEARNINGS** area within campaign stations
- a **hybrid surface**: simple creative overview with expandable technical/audit detail

These are surface requirements, not claims that the underlying systems currently exist or that the values shown are currently available.

## 4. HQ role

HQ is a **read/coordinate/visibility surface**, not a replacement authority.

It may present current authoritative state, surface approved or pending work according to the owning authority, expose links or drill-downs to underlying campaign/workstation records, expose technical/audit detail when available, make approved workflow state understandable to the owner, expose semantic learning and social signals with provenance and status, and show cost/credit information only when an authoritative operational source provides it.

HQ MUST NOT invent campaign status, invent approval, invent spend or credit balances, promote a recommendation into approval, promote a generated candidate into publication, rewrite Product Truth, rewrite Human Identity, rewrite Story State, overwrite raw social metrics, or convert Super Brain memory into operational truth.

## 5. Authority map

| HQ surface | Authority / source | HQ authority |
|---|---|---|
| CURRENT STORY | STORY_STATE_ENGINE | NONE — read/visualise |
| ACTIVE CAMPAIGNS | CAMPAIGN_REGISTRY | NONE — read/visualise |
| WAITING FOR APPROVAL | CAMPAIGN_APPROVAL / CAMPAIGN_REGISTRY | NONE — read/visualise |
| recent winner / social signals | SOCIAL_PLATFORM_API + SOCIAL_INTELLIGENCE_ENGINE, with Super Brain as secondary semantic evidence | NONE — read/visualise |
| creative-fatigue visibility | SOCIAL_INTELLIGENCE_ENGINE / future fatigue evidence | NONE — read/visualise |
| NEXT 3 IDEAS | future Campaign Context / owner selection workflow | NONE — proposal/visibility only |
| credit and cost visibility | authoritative budget/operational layer | NONE — read/visualise |
| EXPERIMENT LAB | Workstation / campaign workflow | NONE — organise/visualise |
| WORLD / STORY MAP | STORY_STATE_ENGINE + semantic context | NONE — read/visualise |
| REJECTS & LEARNINGS | Workstation + Super Brain semantic memory | NONE — read/visualise |

Where a named authority is still PLANNED, HQ MUST show absence/unavailable state rather than fabricate a value.

## 6. CURRENT STORY

CURRENT STORY is a view of the authoritative Story State.

It may show narrative continuity, current arc/context and related approved creative context when the Story State Engine provides them.

It MUST NOT infer the current story from model memory, mutate Story State, declare canon, or treat a Super Brain memory as current Story State.

Story State remains owned by Contract 03 / STORY_STATE_ENGINE.

## 7. ACTIVE CAMPAIGNS

ACTIVE CAMPAIGNS is a view of campaign operational state.

The Campaign Registry is the reserved authority. Because that system is currently PLANNED, the contract does not create or imply live campaign records.

HQ MUST distinguish between no authoritative data available, authoritative active campaign data, and historical campaign context.

A campaign appearing in a semantic memory record does not make it an active campaign.

## 8. WAITING FOR APPROVAL

WAITING FOR APPROVAL is a visibility surface for explicit pending approvals.

Silence is not approval.

HQ MUST source approval state from the future approval/Campaign Registry authority and MUST NOT infer it from generation completion, QA PASS, Workstation state, Social Intelligence recommendation, Super Brain learning, previous owner behaviour, or chat history.

HQ may provide an owner-facing path to review an approval, but this contract does not create the approval action itself.

## 9. Recent winner / social signals

This surface may display recent social evidence and derived interpretation when authoritative sources provide them.

The implementation MUST preserve the distinction between raw platform metric, derived metric, interpretation, recommendation, campaign/story consequence, and approval.

A "winner" label is a presentation of an already-established result or interpretation. HQ MUST NOT create a winner merely because a result looks strong.

One viral result must not be silently promoted to permanent Super Brain truth.

## 10. Creative-fatigue visibility

HQ may expose fatigue information when the Social Intelligence / campaign system has an authoritative or explicitly derived fatigue state.

Fatigue visibility is informational. It does not itself pause a campaign, close an arc, approve a new campaign, authorise spend, or publish content.

Any operational action remains with the authority defined by Contracts 03, 05 and 06 and the future Campaign Registry.

## 11. NEXT 3 IDEAS

NEXT 3 IDEAS is a planning surface.

Contract 01 establishes the initial idea-first operating mode in which three competing campaign/story ideas are produced for owner selection.

HQ may present those ideas, their provenance and their current proposal status. Presentation is not approval.

The exact autonomous selection rule, scoring formula and later idea-selection policy remain open.

## 12. Credit and cost visibility

Credit and cost visibility MUST be read from the future authoritative budget/operational layer.

This contract defines **no numeric credit ceiling, currency ceiling, provider price, spend threshold or cost estimate**.

HQ MUST NOT calculate or invent an authoritative balance from incomplete evidence, infer remaining credit from generation history, treat a budget mode name as a numeric budget, or treat an approval as proof that spend occurred.

Contract 06 owns approval/budget/autonomy rules. Actual operational spend remains a future authoritative record.

## 13. EXPERIMENT LAB

EXPERIMENT LAB is a visibility and organisation surface for experimentation.

It may expose experiment proposals, candidate variants, QA outcomes, learning candidates, rejected outputs, provenance and audit detail.

It MUST preserve the distinction between proposal, generated output, candidate, QA result, approval and publication.

The lab does not grant authority to spend, publish, alter Product Truth or alter Human Identity.

## 14. WORLD / STORY MAP

WORLD / STORY MAP is a visual/contextual representation of story and semantic relationships.

It may combine authoritative Story State, approved narrative context, Super Brain semantic memory and relevant campaign relationships.

It MUST clearly distinguish current authoritative state from historical or semantic context.

A graph visualisation is not itself authority.

## 15. REJECTS & LEARNINGS

Each campaign station has a separate **REJECTS & LEARNINGS** area.

This area may retain rejected candidates, QA failure reasons, useful negative evidence, learning candidates, and durable learnings when the Contract 07 durability rule is satisfied.

Rejected output MUST NOT silently become approved output.

A learning entry MUST retain its provenance and durability basis.

Private performance history and private strategy remain outside the public repository.

## 16. Hybrid surface

The locked presentation model is hybrid:

- a **simple creative overview** for fast owner comprehension;
- **expandable technical/audit detail** for verification, debugging and governance.

The exact UI framework, node layout, visual language, database, connector set, rendering technology and interaction mechanics remain open.

The technical/audit layer MUST NOT expose private secrets merely because it is expandable.

## 17. HQ and Workstation relationship

PINK MALL HQ / Master Station is distinct from the individual campaign stations.

The Workstation contract requires:

- one HQ / Master Station;
- a separate station per campaign;
- checkpoints CONCEPT → IMAGES → optional VIDEO → FINAL;
- initial image exploration normally 2–3 meaningfully different variants.

HQ may navigate into campaign stations and summarise their state, but it MUST NOT collapse station-level candidate/QA/approval state into a single misleading "done" flag.

The exact CyberNinjas implementation and programmatic control surface remain open.

## 18. Authority boundaries

HQ has **no independent authority** over Product Truth, Human Identity, Story State, campaign operational state, approval, paid-generation spend, publication, raw social metrics or Super Brain durable learning.

HQ is an observability and coordination surface. When two underlying authorities disagree, HQ MUST expose the conflict rather than choose a winner.

## 19. Public / private boundary

PIERCIINA-PROJECT is public.

Safe here: this blueprint, public-safe schemas, validators, authority maps, synthetic fixtures and non-sensitive UI structure.

MUST NOT be committed here: private campaign strategy, real private performance history, real credit balances or spend records, customer data, private audience history, private likeness material, credentials, API tokens or secrets.

Detailed private HQ content and operational records belong to the future private ops layer.

## 20. Runtime existence boundary

This contract is specification only.

It does not create or assert the existence of PINK MALL HQ runtime, Campaign Registry, approval service, budget ledger, Workstation runtime, Super Brain runtime, Story State Engine, Social Intelligence Engine, private ops store, live social connectors or autonomous execution.

Current lifecycle state remains owned by Contract 00.

## 21. Open implementation decisions

The following remain open and must not be invented:

1. exact HQ UI implementation;
2. exact node layout;
3. exact data connectors;
4. exact production visualization technology;
5. exact private operational storage;
6. exact live Campaign Registry integration;
7. exact approval-service integration;
8. exact budget/credit data integration;
9. exact Social Intelligence integration;
10. exact Super Brain integration;
11. exact Story State integration;
12. exact Workstation station-navigation mechanics;
13. exact CyberNinjas programmatic control coverage;
14. exact interaction/permission model;
15. exact audit-log implementation.

## 22. Hard failures

| Failure ID | Meaning | Severity |
|---|---|---|
| HQ_AS_SOURCE_OF_TRUTH | HQ is treated as the authority for a domain owned elsewhere. | STOP |
| FABRICATED_OPERATIONAL_STATE | HQ displays invented campaign, approval, spend or publication state. | STOP |
| SILENCE_AS_APPROVAL | Absence of approval is displayed or interpreted as approval. | STOP |
| RECOMMENDATION_AS_APPROVAL | Recommendation is shown or acted on as approval. | HARD_FAIL |
| QA_AS_APPROVAL | QA PASS is treated as commercial approval. | HARD_FAIL |
| GENERATION_AS_APPROVAL | Generation completion is treated as approval. | HARD_FAIL |
| PRIVATE_DATA_PUBLIC | Private operational data is persisted to the public repository. | STOP |
| RAW_METRIC_OVERWRITE | HQ changes or replaces raw social evidence. | STOP |
| STORY_STATE_MUTATION | HQ directly mutates Story State without the owning authority. | STOP |
| PRODUCT_TRUTH_MUTATION | HQ changes Product Truth. | STOP |
| HUMAN_IDENTITY_MUTATION | HQ changes Human Identity. | STOP |
| MEMORY_AS_CURRENT_FACT | Semantic memory is presented as current operational truth without authority refresh. | HARD_FAIL |
| VIRAL_RESULT_AS_PERMANENT_TRUTH | A single strong result is automatically made durable learning. | HARD_FAIL |
| COST_INVENTION | HQ invents a balance, ceiling, spend or provider cost. | STOP |
| RUNTIME_EXISTENCE_FABRICATION | Blueprint files are cited as proof that HQ or its dependencies exist. | STOP |
| CONFLICT_HIDDEN | HQ silently selects one conflicting authority instead of exposing the conflict. | HARD_FAIL |
| REJECT_PROMOTION | Rejected candidate is silently promoted to approved/published state. | HARD_FAIL |
| GLOBAL_EXECUTION_AUTHORITY | HQ gains a blanket right to execute unrelated capabilities. | STOP |

## 23. Authority grants

This contract grants HQ only presentation of authoritative state, cross-system navigation, owner-facing visibility, technical/audit inspection of data the viewer is authorised to see, and organisation of campaign/workstation information.

It grants **no** Product Truth, Human Identity, Story State, approval, spend, publication, raw-metric, semantic-memory or autonomous execution authority.

## 24. Relationship to adjacent contracts

- **Contract 00** owns constitutional authority and lifecycle truth.
- **Contract 01** owns Campaign Context structure.
- **Contract 03** owns Story State and narrative continuity.
- **Contract 04** owns Social Intelligence interpretation/recommendation.
- **Contract 05** owns Workstation execution structure.
- **Contract 06** owns approval, budget and earned autonomy.
- **Contract 07** owns Super Brain semantic memory and durable learning.
- **Contract 08** owns the HQ operating-surface blueprint.

## 25. Summary rule

> **HQ is the window, not the authority. It shows the state owned by other systems, exposes conflicts instead of hiding them, keeps private operational data private, and never turns visibility into permission.**
