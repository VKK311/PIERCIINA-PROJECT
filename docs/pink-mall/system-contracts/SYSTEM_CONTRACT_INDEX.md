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

A contract is canonical only when **all three** hold:

1. it has passed owner or independent review;
2. it is committed to `claude/pink-mall-development`;
3. its machine-readable form passes its validator.

**A file's existence does not make it canonical.** These files also exist on
review candidate branches, and a candidate branch is review material rather than
project truth.

The `status` field is **lifecycle provenance and is location-neutral**. It is not
a second source of canonicality truth: a contract whose status still reads
`CANDIDATE` because it was promoted unchanged *is* canonical once the three
conditions hold. That is what lets the exact reviewed bytes be promoted without
rewriting them. `SUPERSEDED` is the one status that independently disqualifies
reliance, because it fails condition 1 wherever it sits.

## Reading order

1. **`00_SYSTEM_AUTHORITY_CONTRACT.md`** — constitutional layer. Read first;
   everything else inherits from it.
2. `00_SYSTEM_AUTHORITY_CONTRACT.json` — the same model, machine-readable.
3. `DECISION_COVERAGE_MATRIX.md` — which owner decisions are locked, and which
   still lack a detailed contract.
4. The domain contract for the work in hand, once it exists.

## Current contract set

| # | Contract | Files | Status |
|---|---|---|---|
| 00 | **System Authority** | `00_SYSTEM_AUTHORITY_CONTRACT.md` / `.json` / `.schema.json` | status `CANDIDATE` — canonicality follows the rule above, not this string |

Validator: `tools/regression/system_authority_contract.py` (standard library only).

## Planned contracts — NOT YET CREATED

None of the following exist. They **MUST NOT** be cited as authority, and their
subject matter **MUST NOT** be assumed decided.

| # | Contract | Covers | Status |
|---|---|---|---|
| 01 | Campaign Context | campaign purpose, context assembly, campaign taxonomy | NOT YET CREATED |
| 02 | Product Creative | product-led creative rules, product-lock enforcement | NOT YET CREATED |
| 03 | Character & Story | INA/SIS character canon, story continuity | NOT YET CREATED |
| 04 | Social Intelligence | metric weighting, scoring, creative fatigue | NOT YET CREATED |
| 05 | Workstation Operating | node architecture, workflow graph, run model | NOT YET CREATED |
| 06 | Automation & Approval | approval flow, budget modes, earned autonomy grants | NOT YET CREATED |
| 07 | Super Brain Memory | memory schema, write rules, staleness handling | NOT YET CREATED |
| 08 | PINK MALL HQ | HQ blueprint and operating surface | NOT YET CREATED |

Where a decision on one of these has already been locked by the owner, it is
recorded in `DECISION_COVERAGE_MATRIX.md` — so that a decision already taken is
not lost merely because its contract has not been written.

**A locked decision is not a canonical contract.** Those are different states
and the matrix keeps them apart.

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
