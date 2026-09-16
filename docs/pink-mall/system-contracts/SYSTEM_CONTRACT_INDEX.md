# PINK MALL — System Contracts

Entry point for every PINK MALL / Pierciina system contract. Read this before
any task involving campaign systems, Story State, Social Intelligence, Super
Brain, the Workstation, generated campaign media, or system governance.

## Why these exist

The systems being planned each hold some state and each can assert something.
Without a prior agreement about who decides what, the first disagreement is
settled by whichever system happens to be asked — which is not a decision
procedure. System contracts fix that in advance, in a form software can read.

They are **not** implementation plans. A contract says who is authoritative and
what happens on conflict; the implementation is separate work.

## Canonicality

A contract is canonical only when **all four** hold:

1. it has passed current owner or independent review;
2. it is committed to `claude/pink-mall-development`;
3. its machine-readable form passes its validator;
4. its status is not `SUPERSEDED`.

**A file's existence does not make it canonical.** These files also exist on
review candidate branches, and a candidate branch is review material rather than
project truth.

`CANDIDATE` and `CANONICAL` are **lifecycle provenance and location-neutral**.
Neither is a canonicality test: a contract whose status still reads `CANDIDATE`
because it was promoted unchanged *is* canonical once conditions 1–3 hold. That
is what lets the exact reviewed bytes be promoted without rewriting them.

`SUPERSEDED` is a different kind of value — a **terminal tombstone** that
disqualifies reliance by condition 4, wherever the file sits. It is disqualified
because it was replaced, not because its historical review stopped counting.

## Reading order

1. **`00_SYSTEM_AUTHORITY_CONTRACT.md`** — constitutional layer. Read first;
   everything else inherits from it.
2. `00_SYSTEM_AUTHORITY_CONTRACT.json` — the same model, machine-readable.
3. `DECISION_COVERAGE_MATRIX.md` — which owner decisions are locked, and which
   still lack a detailed contract.
4. `01_CAMPAIGN_CONTEXT_CONTRACT.md` — how a campaign context is assembled,
   what may influence it and what may not.
5. The domain contract for the work in hand, once it exists.

## Current contract set

| # | Contract | Files | Status |
|---|---|---|---|
| 00 | **System Authority** | `00_SYSTEM_AUTHORITY_CONTRACT.md` / `.json` / `.schema.json` | status `CANDIDATE` — canonicality follows the rule above, not this string |
| 01 | **Campaign Context** | `01_CAMPAIGN_CONTEXT_CONTRACT.md` / `.json` / `.schema.json`, plus `01_CAMPAIGN_CONTEXT_OBJECT.schema.json` | status `CANDIDATE` — canonicality follows the rule above, not this string |

Validators, standard library only:

- `tools/regression/system_authority_contract.py`
- `tools/regression/campaign_context_contract.py`

This table records that the files **exist in this lineage**. It does not assert
canonicality, which is decided only by the four conditions above.

Contract 01 is **authoring only**. The Campaign Context Builder it describes
**does not exist**, and `01_CAMPAIGN_CONTEXT_OBJECT.schema.json` describes the
shape a future builder must emit. Context instances are snapshots and **MUST
NOT** be committed to this public repository.

## Planned contracts — NOT YET CREATED

The detailed contracts below **do not yet exist** and **MUST NOT** be cited as
canonical domain contracts.

Their *domains*, however, may already contain **locked owner decisions**,
recorded in `DECISION_COVERAGE_MATRIX.md`. Those locked decisions are valid
owner-authorised input and **MUST be preserved**. Only questions the matrix does
**not** record as locked remain open.

No later phase starts from a blank page.

| # | Contract | Covers | Status |
|---|---|---|---|
| 02 | Product Creative | product-led creative rules, product-lock enforcement | NOT YET CREATED |
| 03 | Character & Story | INA/SIS character canon, story continuity | NOT YET CREATED |
| 04 | Social Intelligence | metric weighting, scoring, creative fatigue | NOT YET CREATED |
| 05 | Workstation Operating | node architecture, workflow graph, run model | NOT YET CREATED |
| 06 | Automation & Approval | approval flow, budget modes, earned autonomy grants | NOT YET CREATED |
| 07 | Super Brain Memory | memory schema, write rules, staleness handling | NOT YET CREATED |
| 08 | PINK MALL HQ | HQ blueprint and operating surface | NOT YET CREATED |

`DECISION_COVERAGE_MATRIX.md` is the register of what has already been decided
in each of those domains, so that a decision already taken is not lost merely
because its contract has not been written. Read it before treating any of the
subject matter above as an open question.

**A locked decision is not a canonical contract — and it is not an open question
either.** The matrix keeps all three states apart: locked and awaiting a
contract, carried by a canonical contract, or genuinely open.

## Public / private boundary

`PIERCIINA-PROJECT` is a **PUBLIC** repository.

Contracts, schemas and validation rules are public-safe and live here. Private
strategy, private performance history, private likeness material and anything
carrying credentials do **not** — see §19 of the authority contract.

The intended private store, **PINK-MALL-OPS**, is **PLANNED**. It does not
exist and MUST NOT be described as existing.

## Conflict rule

Authority is domain-specific. There is no global ranking in which one source
beats all others for every question.

- Two canonical sources in the **same** domain disagree → **STOP** and reconcile.
- Semantic or generated state disagrees with canonical truth → **canonical
  wins**, flag the stale state.
- A question maps to **no** defined domain → **STOP**. That is a gap in the
  contract, not a licence to improvise.

Full rules and worked examples: §7 of the authority contract.

## Changing a contract

```
NEW OWNER DECISION → CLASSIFY (one-time exception | durable policy change)
   → UPDATE CANDIDATE → VALIDATE → INDEPENDENT REVIEW
   → PROMOTE TO CANONICAL DEVELOPMENT
```

Chat memory alone MUST NOT become permanent policy.
