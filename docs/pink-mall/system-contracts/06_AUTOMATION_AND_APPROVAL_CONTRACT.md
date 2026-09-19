# PINK MALL — Automation & Approval Contract

| | |
|---|---|
| Contract ID | `PINK_MALL_AUTOMATION_AND_APPROVAL_CONTRACT` |
| Version | `1.0.0` |
| Status | `CANDIDATE` |
| Machine-readable form | `06_AUTOMATION_AND_APPROVAL_CONTRACT.json` |
| Schema | `06_AUTOMATION_AND_APPROVAL_CONTRACT.schema.json` |
| Validator | `tools/regression/automation_approval_contract.py` |

## 1. Purpose

This contract defines the approval, spend and autonomy boundary for PINK MALL
campaign execution.

It preserves the locked owner decisions that belong to this domain while
deliberately leaving the exact numeric ceilings, autonomy thresholds and future
autonomous-publication criteria open.

**This contract is a specification only. It does not create a Campaign Registry,
approval service, budget ledger, autonomous publisher or paid-generation runner.**

## 2. Canonicality and inheritance

This contract inherits the System Authority Contract in full. Its status is
lifecycle provenance, not a substitute for canonicality. Canonicality follows
the four conditions defined by Contract 00.

GitHub is project state. Approval or spend claims that exist only in model
memory, chat history or an ephemeral execution environment are not canonical.

## 3. Locked operating model

The approval model has four explicit boundaries:

1. **Campaign idea approval** — the owner approves the campaign idea and selects
   a budget mode.
2. **Planned first-batch spend** — that approval may authorise the planned first
   paid generation batch, but only within the numeric ceiling eventually defined
   by this contract.
3. **Correction spend** — additional paid correction spend after a failed QA
   batch requires owner review.
4. **Commercial publication** — human approval remains the current default.
   Auto-publish is **NOT authorised** by this contract.

These are separate acts. Generation, QA pass, campaign-station completion or
social recommendation do not silently become approval.

## 4. Approval object

A future implementation MUST preserve approval as an explicit, scoped act.

The public-safe approval record is conceptually:

| Field | Meaning |
|---|---|
| `approvalRef` | Unique approval record reference |
| `campaignRef` | Campaign to which approval applies |
| `scope` | What the approval authorises |
| `budgetMode` | ECONOMY / STANDARD / PREMIUM |
| `approvedBy` | Owner or a future explicitly delegated authority |
| `approvedAt` | Time of approval |
| `status` | Current approval disposition |
| `sourceEvidence` | Reference to the canonical approval record |

The exact persistent storage, identifier format and interface are open
implementation questions.

An approval MUST be scoped. Approval of one campaign, batch or use MUST NOT be
silently reused as approval for a different campaign, spend class or publication
use.

## 5. Approval states

The contract uses a deliberately small public-safe vocabulary:

- `PENDING`
- `APPROVED`
- `REVOKED`
- `EXPIRED`

`APPROVED` means an explicit authorised act exists for the stated scope.

`PENDING`, `REVOKED` and `EXPIRED` MUST NOT be treated as permission to
execute the approved action.

**Silence is never approval.**

The contract does not define automatic expiry duration; that remains an
implementation/owner decision.

## 6. Budget modes

The locked budget-mode vocabulary is:

- `ECONOMY`
- `STANDARD`
- `PREMIUM`

The modes are semantic operating choices, not numeric values.

This contract intentionally does **not** define:

- credit ceilings;
- currency ceilings;
- per-batch generation limits;
- provider prices;
- correction-spend amounts;
- numeric autonomy thresholds.

Until those values are explicitly defined, an implementation MUST NOT infer them
from the mode name.

## 7. First-batch spend

Owner approval of a campaign idea plus a budget mode MAY authorise planned
first-batch paid generation.

The authorisation is bounded by the future budget ceiling for that mode.

A Workstation or generation provider MUST NOT interpret campaign approval as an
unbounded spend grant.

If no applicable numeric ceiling exists, the system MUST NOT invent one.

## 8. Failed QA and correction spend

If a first paid batch fails QA, additional paid correction spend requires
owner review.

A correction attempt may be technically prepared or proposed without becoming
authorised spend.

The system MUST distinguish:

- correction proposal;
- owner review;
- approved correction spend;
- executed correction spend.

A failed batch does not create permission for unlimited retries.

## 9. Commercial publication

**Human approval remains the current default for commercial publication.**

Auto-publish is **NOT authorised** by this contract.

A candidate reaching FINAL, passing QA, receiving a social recommendation, or
being marked as a winning mechanism MUST NOT be treated as publication authority.

Commercial publication remains subject to the authority domain
`COMMERCIAL_PUBLICATION` from Contract 00.

The contract deliberately does not define a future autonomous-publication policy.
That is one of the explicitly open owner decisions.

## 10. Autonomy model

Autonomy is **capability-specific and earned**.

It is not a global flag such as `autonomous=true`.

A future autonomy grant MUST identify the exact capability it permits. Examples
of distinct capabilities include:

- generating a first batch within an approved ceiling;
- preparing a correction proposal;
- executing an already-authorised non-publication workflow step;
- preparing a publication package.

These examples are illustrative capability classes, not additional permissions.

No capability is granted merely because another capability was earned.

## 11. Autonomy grant structure

A future autonomy record should be able to establish:

- `grantRef`
- `capability`
- `scope`
- `grantAuthority`
- `grantedAt`
- `status`
- `conditions`
- `evidenceRefs`

The exact capability catalogue, numeric thresholds, evaluation window,
revocation rules and persistent storage remain open.

An autonomy grant MUST NOT override Product Truth, Human Identity, approval,
publication, privacy or other higher-authority boundaries.

## 12. Approval versus autonomy

Approval and autonomy are different concepts.

- **Approval** authorises a specific scoped act.
- **Autonomy** is a capability-specific permission to execute a class of acts
  under explicit conditions.

An autonomy grant MUST NOT be interpreted as blanket approval for every future
campaign.

Likewise, one approval MUST NOT be converted into a permanent autonomy grant
unless a later canonical rule explicitly authorises that capability.

## 13. Campaign operational state

Campaign execution and approval state belong to the future Campaign Registry
authority.

This contract may define the shape and rules of approval records, but it does
not claim that the Campaign Registry exists.

Operational facts such as:

- campaign approved;
- batch authorised;
- spend executed;
- correction executed;
- publication authorised;
- publication executed

MUST NOT be fabricated from chat history, model memory, Workstation state,
Social Intelligence output or generation-provider output.

## 14. Authority boundaries

This contract grants:

- approval authority: **OWNER**, within the explicit scope recorded;
- paid-generation authority: reserved to the owner under the approved budget
  model;
- publication authority: **OWNER** under the current default;
- autonomous authority: **NONE by default**.

The contract does not grant authority to:

- Workstation;
- CyberNinjas Studio;
- Claude Orchestrator;
- Super Brain;
- Social Intelligence Engine.

Those systems may execute, interpret, prepare or recommend only within the
authority assigned to them elsewhere.

## 15. Delegation

A future delegated approver is possible only if a canonical rule explicitly
names the delegation and its scope.

Until then, owner approval remains the default approval authority.

A system MUST NOT infer delegation from a user's role, prior approval, frequent
interaction or absence of objection.

## 16. Revocation and expiry

An explicit approval or autonomy grant may be revoked by its authorised
authority when the future implementation supports revocation.

Revocation MUST prevent further execution under that grant unless another valid
authorisation exists.

Expiry, where implemented, MUST be explicit and must not be inferred from
silence.

No universal expiry duration is locked here.

## 17. Public / private boundary

The repository is public.

Safe here:

- approval vocabulary;
- public-safe schemas;
- authority boundaries;
- budget-mode names;
- synthetic validation fixtures;
- rules for separating approval from execution.

Not safe here:

- real campaign spend;
- real credit balances;
- private approval records;
- provider credentials;
- private campaign strategy;
- customer data;
- private performance history.

The intended private operational store remains governed by Contract 00 and is
not created by this contract.

## 18. Relationship to adjacent contracts

- **Contract 00** owns constitutional authority and the current lifecycle state
  of Campaign Registry, Workstation, paid-generation authority and publication.
- **Contract 02** owns product-fidelity rules.
- **Contract 03** owns Story State and narrative continuity.
- **Contract 04** owns social evidence, interpretation and recommendation.
- **Contract 05** owns Workstation execution structure and candidate boundaries.
- **Contract 07** will own Super Brain memory and durable learning.
- **Contract 08** will own the HQ operating surface.

This contract MUST NOT duplicate or rewrite those domains.

## 19. Explicit open decisions

The following remain genuinely open and are intentionally absent as numeric
rules:

1. exact credit ceilings;
2. exact currency/spend ceilings by budget mode;
3. exact numeric autonomy thresholds;
4. future autonomous-publication criteria;
5. exact capability catalogue for earned autonomy;
6. evaluation windows and evidence requirements for earning autonomy;
7. exact revocation/expiry implementation;
8. persistent approval and autonomy record storage;
9. exact delegation mechanism, if delegation is later authorised.

An implementation may not silently convert any of these into a permanent policy.

## 20. Hard failures

| Failure ID | Meaning | Severity |
|---|---|---|
| `SILENCE_AS_APPROVAL` | No explicit approval exists, but execution treats silence as permission. | STOP |
| `UNSCOPED_APPROVAL` | Approval is reused outside its recorded scope. | HARD_FAIL |
| `NUMERIC_BUDGET_INVENTION` | A mode is assigned an unauthorised ceiling or spend amount. | STOP |
| `UNBOUNDED_FIRST_BATCH` | First-batch approval is treated as unlimited spend. | STOP |
| `CORRECTION_SPEND_WITHOUT_REVIEW` | Extra paid correction spend follows failed QA without owner review. | STOP |
| `AUTO_PUBLISH` | A system publishes commercially without the current required human approval. | STOP |
| `GENERATION_AS_APPROVAL` | Generation success is treated as approval. | HARD_FAIL |
| `QA_AS_APPROVAL` | QA pass is treated as commercial approval. | HARD_FAIL |
| `RECOMMENDATION_AS_APPROVAL` | Social recommendation is treated as approval. | HARD_FAIL |
| `GLOBAL_AUTONOMY_FLAG` | One autonomy grant is interpreted as permission for unrelated capabilities. | HARD_FAIL |
| `AUTONOMY_OVERRIDES_AUTHORITY` | Autonomy is used to bypass Product Truth, Human Identity, approval or publication authority. | STOP |
| `OPERATIONAL_STATE_FABRICATION` | Approval/spend/publication facts are asserted without the authoritative operational record. | STOP |
| `PRIVATE_APPROVAL_DATA_PUBLIC` | Real private approval/spend data is persisted in the public repo. | STOP |
| `REVOKED_GRANT_EXECUTED` | Execution proceeds under a revoked approval or autonomy grant. | STOP |
| `EXPIRED_GRANT_EXECUTED` | Execution proceeds under an expired grant without a new valid authorisation. | STOP |

## 21. Summary rule

> **Approval is explicit and scoped. Budget modes are not numbers until their
> authority defines the numbers. Failed QA does not buy unlimited retries.
> Human publication approval remains the default. Autonomy is earned per
> capability, never granted globally.**
