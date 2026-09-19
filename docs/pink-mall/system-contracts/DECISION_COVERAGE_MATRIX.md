# PINK MALL — Decision Coverage Matrix

Eight owner interviews produced locked decisions across the campaign, creative,
story, social, operating, approval, memory and HQ domains. Their detailed
contracts are being authored **incrementally**, one domain at a time, rather
than all at once.

Contracts **01 — Campaign Context**, **02 — Product Creative** and
**03 — Character & Story** have been authored: their files exist in this
lineage. Domains **05–08** are still awaiting their detailed contracts. File existence does **not** by itself
establish canonicality — that is decided only by the four conditions in
`00_SYSTEM_AUTHORITY_CONTRACT`.

This matrix exists so that a decision already taken is not lost merely because
its contract has not been written. It records **that** a decision exists, its
public-safe structural content, where its detail belongs, and whether that
detail is safe for a public repository.

## Three states, deliberately kept apart

| State | Meaning |
|---|---|
| **LOCKED DECISION EXISTS** | The owner has decided. The decision is authoritative input and MUST be preserved. |
| **DETAILED CANONICAL CONTRACT CREATED** | A reviewed, validated, committed contract carries the detail. |
| **GENUINELY OPEN** | No decision has been taken. Nothing to preserve yet. |

A locked decision is **not** a canonical contract — and it is **not** an open
question either. Writing "undefined" over a decision the owner has already made
would erase it, which is the exact failure this matrix exists to prevent. Where
a decision is locked but its contract is unwritten, the row says
**LOCKED — AWAITING CANONICAL CONTRACT**, never "undefined".

## Privacy note

This file is in a **PUBLIC** repository. Confidential creative and operating
strategy is **not** reproduced here. Where the owner has decided but the detail
is sensitive, the row says
`LOCKED — PRIVATE DETAIL DEFERRED TO PRIVATE OPS LAYER`.
That phrasing preserves the decision while withholding the content. It is never
used to mean "undecided".

## Matrix

### 1. Campaign Context / Purpose

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed contract authored** | YES — `01_CAMPAIGN_CONTEXT_CONTRACT` files **EXIST in this lineage**. Canonicality is decided solely by the four conditions in contract 00, not by this row and not by file existence. |
| **Target contract** | 01 — Campaign Context |
| **Private detail required** | PARTIAL |

Contract 01 is **authoring only**: it defines the rules and the package shape. No
Campaign Context Builder exists, and this row records no implementation.

**Locked, public-safe structure**

- Campaign Context is **idea-first, not product-first**.
- Context is assembled from: current world/story state; cultural and social
  signals; PINK MALL DNA; INA/SIS context; current products; target format.
- The initial operating mode produces **three competing campaign/story ideas**
  for owner selection.
- Product use is **contextual** — a campaign is not required to begin from a SKU.
- Detailed unpublished campaign concepts: `LOCKED — PRIVATE DETAIL DEFERRED TO
  PRIVATE OPS LAYER`.

**Genuinely open**

- external trend/social ingestion implementation — exact providers, API work,
  signal freshness windows and numeric weighting;
- later autonomous idea-selection policy, including any selection threshold or
  scoring formula;
- persistent Campaign Context ID format;
- private campaign-strategy storage implementation.

The serialized package **shape** is no longer open — it is defined by
`01_CAMPAIGN_CONTEXT_OBJECT.schema.json`. What a persistent campaign identifier
looks like across contexts remains open, and belongs to a future operational
system rather than to contract 01.

### 2. Product Creative / Product Truth

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed contract authored** | YES — `02_PRODUCT_CREATIVE_CONTRACT` files **EXIST in this lineage**. Canonicality is decided solely by the four conditions in contract 00, not by this row and not by file existence. The governing authority rule was **already canonical** via the product-onboarding system and is unchanged. |
| **Target contract** | 02 — Product Creative |
| **Private detail required** | NO |

Contract 02 is **authoring only**: it defines product-fidelity rules, the Product
Lock model and the package shape. **No Product Creative Engine exists**, and this
row records no implementation. Product onboarding authority is untouched.

**Locked, public-safe structure**

- **Product Truth is fixed.** **Human Truth is fixed.** The creative world may
  transform around them.
- Canonical commerce media is a separate class from campaign media and is never
  generatively altered.
- Product geometry and intrinsic construction **must not drift**.
- Product identity, price, availability and canonical media authority are ACTIVE
  and unchanged by this contract.
- A generator receives **no authority to redesign** a product: 1:1 product
  fidelity means the same exact SKU, variant, silhouette, geometry, construction,
  proportions, branding and distinctive details, not a pixel-identical copy.
- `productGeometrySource` and `productWearReference` are distinct; an avatar
  frame, generic imagery, a similar SKU or a different colourway is **never**
  product-geometry authority.
- **Clothing worn on a body is a HIGH-RISK** product-fidelity case, because
  colour can be preserved while cut, length, drape and construction change.
- Human identity lock and product lock operate **simultaneously**; if both cannot
  be satisfied the candidate is rejected rather than either being edited.
- Generated output starts as `GENERATED_OUTPUT` / `CANDIDATE` and never becomes
  canonical commerce media, an approval or a publication by succeeding.
- A failed generation is evidence about the attempt, **never** permission to
  rewrite Product Truth or weaken a lock.

**Genuinely open**

- product-lock **enforcement mechanics** — the lock vocabulary is now defined by
  contract 02, but nothing enforces it;
- exact computer-vision QA method, and every numeric geometry, colour and logo
  similarity tolerance;
- per-category creative rules and per-category risk taxonomy beyond the locked
  clothing risk;
- exact Clothing Fit implementation and external fit-evidence source strategy;
- automatic retry policy;
- execution-provider API and node mechanics.

The **QA criteria** are no longer wholly open: contract 02 defines ten structural
gates with a `PASS` / `FAIL` / `UNRESOLVED` vocabulary. What remains open is how
any of them is measured — deliberately, since inventing a tolerance would be
inventing a fact.

### 3. INA / SIS Character & Story

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed contract authored** | YES — `03_CHARACTER_STORY_CONTRACT` files **EXIST in this lineage**. Canonicality is decided solely by the four conditions in contract 00, not by this row and not by file existence. |
| **Target contract** | 03 — Character & Story |
| **Private detail required** | YES |

Contract 03 is **authoring only**: it defines the identity/role/relationship/canon
separation, the narrative-continuity requirement and the Story State snapshot
shape. **No Story State Engine exists**, no Story State instance exists, and this
row records no implementation. Human Identity remains owned by the Avatar Skill.

**Locked, public-safe structure**

- **Identity is persistent.** Personality role is **dynamic**. Relationship
  state is **dynamic**.
- **Narrative continuity is required.**
- **TEAM INA vs TEAM SIS** exists as an engagement and story mechanic.
- Audience input **may sometimes affect later canon**.
- **Story State must carry structured continuity** rather than relying on model
  memory.
- Identity truth belongs to the Avatar Skill; one sister is never substituted for
  the other; identity is never inferred from generated output.
- **Commercial generated-likeness publication remains BLOCKED** behind the
  Consent Gate — `CONSENT_AND_PROVENANCE.json` records
  `OWNER_CONFIRMATION_REQUIRED` for every subject and every allowed use.
- Character biography, personal material and Creative Director detail:
  `LOCKED — PRIVATE DETAIL DEFERRED TO PRIVATE OPS LAYER`.

**Genuinely open**

- exact audience-to-canon decision rules;
- exact Story State implementation mechanics;
- persistent Story State ID format;
- private character-material storage implementation.
- *(Consent resolution is an owner action, not a contract action.)*

The Story State **object shape** is no longer open — it is defined by
`03_STORY_STATE_OBJECT.schema.json`. What remains open is how a Story State
Engine implements it, and how audience evidence may ever become canon.

### 4. Story Engine + Social Intelligence

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed contract authored** | **AUTHORED** — this domain targets **two** contracts, and `03_CHARACTER_STORY_CONTRACT` and `04_SOCIAL_INTELLIGENCE_CONTRACT` files both exist in this lineage. Authored is a bookkeeping state, not canonicality. |
| **Target contract** | 03 — Character & Story, and 04 — Social Intelligence |
| **Private detail required** | YES |

The split is deliberate. Contract 03 carries the **story and narrative lifecycle
structure** — what `CONTINUE` / `EVOLVE` / `PAUSE` / `CLOSE` / `REVIVE` *mean* for
continuity. Contract 04 carries the **Social Intelligence** half — the evidence for
*choosing* between them. Contract 03 deliberately defines no metric weight,
threshold, cooldown or ratio, and contract 04 deliberately defines none either:
it preserves the hierarchy as a **qualitative** order and leaves every number
open.

**Locked, public-safe structure**

- Raw metrics and interpretation **remain separate** — evidence is not a
  conclusion.
- A **response-priority hierarchy exists**.
- Story arcs may **CONTINUE / EVOLVE / PAUSE / CLOSE / REVIVE** according to
  evidence.
- Winning creative mechanisms **may be exploited temporarily**.
- **Fatigue must be tracked** before repetitive continuation.
- Private performance history: `LOCKED — PRIVATE DETAIL DEFERRED TO PRIVATE OPS
  LAYER`.

**Genuinely open**

- exact metric weights (explicitly **not** yet locked);
- fatigue thresholds and cooldown durations;
- exploration/exploitation ratio;
- API and data-ingestion implementation;
- later autonomous selection and publication rules.

### 5. Workstation Operating Model

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed contract authored** | YES — `05_WORKSTATION_OPERATING_CONTRACT` files now exist in this lineage; canonicality is still decided solely by the four conditions in contract 00 |
| **Target contract** | 05 — Workstation Operating |
| **Private detail required** | NO |

**Locked, public-safe structure**

- **PINK MALL HQ / Master Station**, plus a **separate station per campaign**.
- Once an idea is approved, **campaign-station construction may begin without a
  further architecture approval**.
- Checkpoints are **CONCEPT → IMAGES → VIDEO (if applicable) → FINAL**.
- The initial image phase normally explores **2–3 meaningfully different
  variants**.
- **Claude selects the generation model.**
- **ECONOMY / STANDARD / PREMIUM** budget modes exist conceptually. *(Ceilings
  are not defined — see domain 6.)*
- Output quantity is **campaign-dependent**, not a fixed template.
- The Workstation is PLANNED and does not exist; generated output is a candidate
  until QA and approval.

**Genuinely open / implementation-dependent**

- exact CyberNinjas node implementation;
- whether the available CyberNinjas control surface can manipulate all required
  Workstation nodes programmatically;
- final reusable station-template serialization.

### 6. Approval / Automation

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed canonical contract created** | NO — LOCKED, AWAITING CANONICAL CONTRACT |
| **Target contract** | 06 — Automation & Approval |
| **Private detail required** | NO |

**Locked, public-safe structure**

- The owner approves **campaign idea + budget mode**.
- That approval **may authorise planned first-batch spend** within the future
  mode ceiling.
- **Extra correction spend after a failed QA batch requires owner review.**
- **Human approval remains the current default** for commercial publication.
- **Auto-publish is NOT authorised.**
- **Autonomy is capability-specific and earned**, never a global flag.
- Contract 06 also owns budget modes, ceilings, credit limits and correction-spend
  rules. There is no separate numbered "Campaign Execution" contract.

**Genuinely open**

- exact credit ceilings;
- numeric autonomy thresholds;
- future autonomous publication criteria.

### 7. Super Brain Memory

| | |
|---|---|
| **Locked decision exists** | YES |
| **Detailed canonical contract created** | NO — LOCKED, AWAITING CANONICAL CONTRACT |
| **Target contract** | 07 — Super Brain Memory |
| **Private detail required** | YES |

**Locked, public-safe structure**

- Architecture is **structured clusters + free graph relationships**.
- **Campaign Memory is written after campaigns.**
- **Durable Learning requires** repeated evidence, sufficient signal, or explicit
  owner confirmation.
- **One viral result must not become permanent truth automatically.**
- Preference drift must distinguish **stable / emerging / declining / retired**
  patterns.
- **Periodic memory maintenance and cleanup is required.**
- **GitHub remains factual authority.** Super Brain is non-authoritative for PM
  IDs, prices, sizes, availability, canonical product identity, approval state,
  branch or hash, campaign spend and publication state.
- Autonomous real-time knowledge is a **target**, not a current capability.
- Memory content and private strategy exports: `LOCKED — PRIVATE DETAIL DEFERRED
  TO PRIVATE OPS LAYER`.

**Genuinely open**

- exact storage schema;
- exact implementation and API bridge;
- the private memory content itself.

### 8. PINK MALL HQ Blueprint

| | |
|---|---|
| **Locked decision exists** | YES — **a blueprint already exists** |
| **Detailed canonical contract created** | NO — LOCKED, AWAITING CANONICAL CONTRACT |
| **Target contract** | 08 — PINK MALL HQ |
| **Private detail required** | PARTIAL |

**Locked, public-safe structural elements**

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
- a **hybrid surface**: simple creative overview, with expandable
  technical/audit detail
- HQ is PLANNED and does not exist.
- Detailed private commercial metrics and sensitive strategy:
  `LOCKED — PRIVATE DETAIL DEFERRED TO PRIVATE OPS LAYER`.

**Genuinely open**

- exact UI implementation;
- exact Workstation node layout;
- data connectors;
- production visualization technology.

## Summary

| # | Domain | Locked | Contract created | Target | Private detail |
|---|---|---|---|---|---|
| 1 | Campaign Context / Purpose | YES | AUTHORED — files exist in this lineage | 01 | PARTIAL |
| 2 | Product Creative / Product Truth | YES | AUTHORED — files exist in this lineage | 02 | NO |
| 3 | INA/SIS Character & Story | YES | AUTHORED — files exist in this lineage | 03 | YES |
| 4 | Story Engine + Social Intelligence | YES | AUTHORED — files exist in this lineage | 03, 04 | YES |
| 5 | Workstation Operating Model | YES | YES — authored candidate; validator-checked | 05 | NO |
| 6 | Approval / Automation | YES | NO — awaiting | 06 | NO |
| 7 | Super Brain Memory | YES | NO — awaiting | 07 | YES |
| 8 | PINK MALL HQ Blueprint | YES | NO — awaiting | 08 | PARTIAL |

Eight domains, eight sets of locked structural decisions preserved above. Domain
contracts **01**, **02**, **03** and **04** have been authored; domains 05–08
still await theirs. Domain 4 targets both 03 and 04, and both now exist, so it is
fully authored in the bookkeeping sense — which is not the same as canonical.
Closing that
gap is the Phase 1 work that continues — and it starts from these decisions, not
from a blank page.

"Authored" in the table above means the files exist in this lineage. Whether any
of them is **canonical** is decided only by the four conditions in
`00_SYSTEM_AUTHORITY_CONTRACT` — current review, presence on
`claude/pink-mall-development`, a passing validator, and a status that is not
`SUPERSEDED`. This matrix is bookkeeping; it is not a canonicality test.
