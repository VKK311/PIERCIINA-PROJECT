# PINK MALL — Decision Coverage Matrix

Eight owner interviews produced locked decisions across the campaign, creative,
story, social, operating, approval, memory and HQ domains. Their detailed
contracts are **not** being authored yet.

This matrix exists so that a decision already taken is not lost merely because
its contract has not been written. It records **that** a decision exists, where
its detail belongs, and whether that detail is safe for a public repository.

## Two states that are not the same

| State | Meaning |
|---|---|
| **LOCKED DECISION EXISTS** | The owner has decided. The decision is authoritative input. |
| **DETAILED CANONICAL CONTRACT CREATED** | A reviewed, validated, committed contract carries the detail. |

A locked decision is **not** a canonical contract. Only the System Authority
Contract (00) has reached candidate contract status; every domain contract below
is **NOT YET CREATED**.

## Privacy note

This file is in a **PUBLIC** repository. Confidential creative and operating
strategy is **not** reproduced here. Where detail is sensitive, the row says
`PRIVATE DETAIL REQUIRED — MOVE TO PRIVATE OPS CONTRACT LAYER` and stops there.
That is deliberate, not an omission.

## Matrix

### 1. Campaign Context / Purpose

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed canonical contract created** | NO |
| **Target contract** | 01 — Campaign Context |
| **Private detail required** | PARTIAL |
| **Public-safe summary** | Campaigns are purpose-driven and context-assembled rather than ad-hoc. Campaign operational state will be owned by a Campaign Registry, which is PLANNED and does not exist. Authority is reserved in contract 00 under `CAMPAIGN_OPERATIONAL_STATE`. |
| **Open items** | Campaign taxonomy, context-assembly inputs and registry schema are undefined. Unpublished campaign concepts: PRIVATE DETAIL REQUIRED — MOVE TO PRIVATE OPS CONTRACT LAYER. |

### 2. Product Creative / Product Truth

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed canonical contract created** | NO — but the governing authority rule **is** canonical via the existing product-onboarding system |
| **Target contract** | 02 — Product Creative |
| **Private detail required** | NO |
| **Public-safe summary** | Product truth may not be transformed by creative work. Generated campaign media never becomes canonical commerce media. The three media classes are defined in contract 00 §16. Product identity, price, availability and canonical media authority are already ACTIVE and unchanged. |
| **Open items** | Product-lock enforcement mechanics, per-category creative rules and QA criteria for product geometry in generated media. |

### 3. INA / SIS Character & Story

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed canonical contract created** | NO |
| **Target contract** | 03 — Character & Story |
| **Private detail required** | YES |
| **Public-safe summary** | Human identity truth belongs to the Avatar Skill. One sister is never substituted for the other; identity is never inferred from generated output. **Commercial generated-likeness publication remains BLOCKED** behind the Consent Gate — `CONSENT_AND_PROVENANCE.json` records `OWNER_CONFIRMATION_REQUIRED` for every subject and every allowed use. |
| **Open items** | Character canon and story continuity rules undefined. Consent resolution is an owner action, not a contract action. Character backstory and personal profile detail: PRIVATE DETAIL REQUIRED — MOVE TO PRIVATE OPS CONTRACT LAYER. |

### 4. Story Engine + Social Intelligence

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed canonical contract created** | NO |
| **Target contract** | 03 — Character & Story, and 04 — Social Intelligence |
| **Private detail required** | YES |
| **Public-safe summary** | Raw platform metrics are evidence; conclusions drawn from them are interpretation. Contract 00 defines that distinction (`SOCIAL_RAW_METRICS` vs `SOCIAL_INTERPRETATION`) and nothing further. Story State and the Social Intelligence engine are PLANNED. |
| **Open items** | Metric weighting, scoring, creative-fatigue thresholds and story cadence are all undefined. Audience-performance history and private account data: PRIVATE DETAIL REQUIRED — MOVE TO PRIVATE OPS CONTRACT LAYER. |

### 5. Workstation Operating Model

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed canonical contract created** | NO |
| **Target contract** | 05 — Workstation Operating |
| **Private detail required** | NO |
| **Public-safe summary** | The Workstation is the intended persistent visual workflow graph. It is PLANNED and does not exist. It may generate, transform, propose, render, compare and organise; it never becomes factual authority by producing an asset. Generated output is a candidate until QA and approval. |
| **Open items** | Node architecture, run model and graph persistence undefined. Whether the CyberNinjas platform can host it is a capability question already audited and unresolved. |

### 6. Approval / Automation

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed canonical contract created** | NO |
| **Target contract** | 06 — Automation & Approval |
| **Private detail required** | NO |
| **Public-safe summary** | Human approval is the current default for commercial publication; no system holds autonomous publishing authority. Autonomy is capability-specific, never a global flag. Paid-generation authority shape is recorded in contract 00 §17: owner approves idea plus budget mode, planned spend may proceed within the approved ceiling, correction spend after a failed QA batch requires owner review. |
| **Open items** | Budget modes, ceilings and credit limits are **deliberately not defined**. Earned-autonomy grants and confidence thresholds are undefined. |

### 7. Super Brain Memory

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed canonical contract created** | NO |
| **Target contract** | 07 — Super Brain Memory |
| **Private detail required** | YES |
| **Public-safe summary** | Super Brain may govern interpretation, learning and creative memory. It is explicitly **non-authoritative** for PM IDs, prices, sizes, availability, canonical product identity, approval state, branch or hash, campaign spend and publication state. GitHub wins for factual truth. Autonomous real-time knowledge is a **target**, not a current capability. |
| **Open items** | Memory schema, write rules and staleness handling undefined. Memory content and private strategy exports: PRIVATE DETAIL REQUIRED — MOVE TO PRIVATE OPS CONTRACT LAYER. |

### 8. PINK MALL HQ Blueprint

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed canonical contract created** | NO |
| **Target contract** | 08 — PINK MALL HQ |
| **Private detail required** | PARTIAL |
| **Public-safe summary** | HQ is the intended operating surface over the campaign, story, social and memory systems. It is PLANNED and does not exist. |
| **Open items** | Blueprint, layout and surface scope undefined. Depends on contracts 01–07. Internal commercial analysis surfaced by HQ: PRIVATE DETAIL REQUIRED — MOVE TO PRIVATE OPS CONTRACT LAYER. |

## Summary

| # | Domain | Locked | Contract created | Target | Private detail |
|---|---|---|---|---|---|
| 1 | Campaign Context / Purpose | YES | NO | 01 | PARTIAL |
| 2 | Product Creative / Product Truth | YES | NO | 02 | NO |
| 3 | INA/SIS Character & Story | YES | NO | 03 | YES |
| 4 | Story Engine + Social Intelligence | YES | NO | 03, 04 | YES |
| 5 | Workstation Operating Model | YES | NO | 05 | NO |
| 6 | Approval / Automation | YES | NO | 06 | NO |
| 7 | Super Brain Memory | YES | NO | 07 | YES |
| 8 | PINK MALL HQ Blueprint | YES | NO | 08 | PARTIAL |

Eight domains, eight locked decisions, **zero** detailed canonical contracts.
That gap is the Phase 1 work that follows.
