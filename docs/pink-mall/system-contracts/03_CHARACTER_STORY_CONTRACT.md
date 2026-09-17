# PINK MALL — Character and Story Contract

| | |
|---|---|
| **Contract ID** | `PINK_MALL_CHARACTER_AND_STORY_CONTRACT` |
| **Number** | `03` |
| **Version** | `1.0.0` |
| **Status** | `CANDIDATE` — provenance only; canonicality follows contract 00's four conditions |
| **Parent** | `PINK_MALL_SYSTEM_AUTHORITY_CONTRACT` |
| **Depends on** | `PINK_MALL_CAMPAIGN_CONTEXT_CONTRACT` (contract 01) |
| **Machine-readable** | `03_CHARACTER_STORY_CONTRACT.json` |
| **Runtime snapshot** | `03_STORY_STATE_OBJECT.schema.json` |
| **Validator** | `tools/regression/character_story_contract.py` |

## 1. Purpose

Define the constitutional boundary between **human identity**, **narrative
role**, **relationship state**, **story canon**, **audience influence** and
**generated output** — before any runtime story system is built.

The order matters. Once a story engine is running and continuity is accumulating,
every argument about whether a narrative event "really happened" becomes an
argument about a specific record someone is already relying on. This settles it
while nothing is at stake.

**No Story State Engine exists. No Story State exists.** Nothing here is
implemented.

## 2. The core separation

> **HUMAN IDENTITY ≠ NARRATIVE ROLE ≠ RELATIONSHIP STATE ≠ STORY CANON**

| Layer | Persistent | Mutable by story | Authority |
|---|---|---|---|
| `HUMAN_IDENTITY` | **yes** | **NO** | Avatar Skill |
| `NARRATIVE_ROLE` | no | yes | Story State Engine |
| `RELATIONSHIP_STATE` | no | yes | Story State Engine |
| `STORY_CANON` | no | yes | Story State Engine |

- A change in narrative role **MUST NOT** mutate Human Identity.
- A change in relationship state **MUST NOT** mutate Human Identity.
- A generated depiction or text **MUST NOT** become identity truth.
- A generated depiction or text **MUST NOT** become story canon merely because
  it was generated.
- Narrative intent that conflicts with **Human Identity** or **Product Truth**
  loses. The narrative intent is what changes.

## 3. Human identity authority

Inherited from contract 00 and **not redefined**:

| | |
|---|---|
| Domain | `HUMAN_IDENTITY` |
| Primary authority | **`AVATAR_SKILL`** |
| Secondary evidence | `OWNER` |
| `STORY_STATE_ENGINE` | explicitly **NOT** identity authority |

- **INA remains INA. SIS remains SIS.**
- One sister may **NEVER** substitute for the other.
- **DUO is not a third human identity.**
- Generated output is **never** identity evidence.
- Narrative events **cannot** rewrite identity.
- Narrative role **cannot** override Avatar Skill truth.

This contract **references** human identity. It does not create a second
identity record, and **facial, biometric and likeness detail MUST NOT appear in
Story State**.

> Precedent, `IDENTITY_COLLISION_PROTOCOL.json`: INA references are authoritative
> only for INA, SIS references only for SIS, and **DUO references are staging
> evidence that is NEVER identity authority for either sister.**

## 4. Narrative role is dynamic — and has no fixed archetype

Contract 01's `characterRole` (`INA` / `SIS` / `DUO` / `NONE`) is a **campaign
participation selector**. That vocabulary is **not redefined here**.

It is **not**: personality truth · identity truth · a permanent archetype ·
Story State itself.

**No permanent archetype may be encoded.** No rule of the form *"INA always
behaves as X"* or *"SIS always behaves as Y"* may be invented here, and none may
be introduced unless separately established by an authorised source.

Comedy, seriousness, sensuality, absurdity, rivalry, tenderness and other tones
may all be campaign-dependent — that list is **illustrative, not closed**.
Creative variation may be broad.

**Human Identity stays fixed while narrative behaviour may change.**

## 5. Relationship state

Dynamic, and structurally distinct from Human Identity.

- may **evolve**;
- may **affect future story**;
- may **not** redefine either sister's identity;
- **must not** rely on model memory.

No permanent relationship taxonomy is locked, so the schema carries an
**extensible structured state or an opaque narrative value** rather than
pretending a fixed list is canonical.

## 6. Narrative continuity is required

A future Story State must carry enough structured information that a **fresh
session** can determine:

1. what narrative situation currently exists;
2. what arcs exist;
3. what relevant prior narrative events matter;
4. which character roles are currently in play;
5. the current relationship state;
6. what changed since the previous Story State;
7. whether a proposed development contradicts established continuity.

**Model memory is NEVER sufficient continuity storage. Chat history is NEVER
canonical Story State.**

## 7. Story State authority

Inherited from contract 00, unchanged:

| | |
|---|---|
| Domain | `STORY_STATE` |
| Primary | `STORY_STATE_ENGINE` |
| Secondary evidence | `CAMPAIGN_REGISTRY`, `OWNER` |
| Non-authoritative | `SUPER_BRAIN`, `SOCIAL_INTELLIGENCE_ENGINE`, model memory, chat history |

This contract defines **what authority** the Story State Engine holds — not
**whether it currently exists**. Implementation state is owned by contract 00's
source registry and must be read from there; caching it here would make this
contract stale the day the engine is built. Contract 03 neither implements nor
activates the engine, and provides no implementation at all.

*(Current repository state, reported rather than frozen into this contract:
contract 00 records `STORY_STATE_ENGINE` as `PLANNED`.)*

## 8. Story State versus campaign operational state

| Kind of fact | Authority |
|---|---|
| campaign operational fact | `CAMPAIGN_REGISTRY` |
| narrative continuity | `STORY_STATE` |

Where story or semantic memory contradicts an authoritative operational fact,
**the operational fact wins** and the story memory is corrected
(contract 00's `SEMANTIC_VS_CANONICAL`).

Story State **MUST NOT** fabricate that a campaign executed, published, was
approved, spent money or completed unless the operational authority records it.

## 9. Story intent is not a story event

`PROPOSAL` · `APPROVAL` · `OPERATIONAL_FACT` · `STORY_CANON` are four states and
**MUST NOT be collapsed into one.**

A proposal — or a Campaign Context idea the owner **selected** — does **not by
itself** prove the narrative event occurred. The parent's truth-class semantics
govern.

## 10. Story arc lifecycle

**Closed vocabulary:**

| Action | Narrative meaning |
|---|---|
| `CONTINUE` | the arc proceeds as established |
| `EVOLVE` | the arc develops into a materially new direction, still the same arc |
| `PAUSE` | the arc stops advancing without concluding; it may resume |
| `CLOSE` | the arc is concluded; continuity records it as ended |
| `REVIVE` | a paused or closed arc resumes, prior continuity acknowledged |

This contract owns the **narrative meaning** side. **Contract 04** will own the
social-intelligence evidence, weighting, fatigue and recommendation logic for
*choosing* between them.

**Not defined here:** metric thresholds · social weights · fatigue thresholds ·
cooldown durations · exploration/exploitation ratios · any numeric rule for
picking an action · a complete transition graph (repository evidence locks none).

Not every Story State must contain an active arc.

## 11. Audience influence

Audience input **may sometimes affect later canon** — that decision is locked.
What follows from it:

- audience evidence is eligible **INPUT** to a possible future story change;
- it is **NOT** Story State authority;
- raw social metrics remain **evidence**; social interpretation remains
  **interpretation**;
- neither may rewrite Story State **merely because engagement was high**.

Until a later canonical rule explicitly defines autonomous audience-to-canon
transition authority, audience influence **may create or support a `PROPOSAL`**
and **MUST NOT silently mutate canonical Story State.**

**Not invented here:** thresholds · voting percentages · engagement scores ·
automatic canon-selection formulas. **Contract 04 remains NOT YET CREATED.**

## 12. TEAM INA vs TEAM SIS

Exists as an **engagement and story mechanic**.

| It may | It is not |
|---|---|
| be used by campaigns and arcs | Human Identity truth |
| influence future story proposals | a permanent personality label |
| | Story State authority |

Audience team preference **cannot** rewrite identity. Participation is **not**
commercial approval. **No numeric winner logic is defined here.**

## 13. Sources that are never Story State authority

`MODEL_MEMORY` · `CHAT_HISTORY` · `SUPER_BRAIN` · `SOCIAL_INTELLIGENCE_ENGINE` ·
`CYBERNINJAS_STUDIO`

Super Brain may later hold semantic interpretation, campaign memory, creative
learning and preference drift. **Where it disagrees with canonical Story State,
Story State wins** and Super Brain is marked stale and corrected per contract 00.

## 14. Generated output

A generated image, video or text **may depict** a current story state, a proposed
development, or a narrative experiment.

It does **not** become canon because generation succeeded. It is **never**
evidence that an event occurred, a relationship changed, a campaign published,
audience accepted a development, or identity changed.

A generated narrative concept remains a **`PROPOSAL`** until the appropriate
future authority records the real Story State transition.

## 15. Consent

Commercial publication of a generated likeness remains governed by the
**Consent Gate** (`CONSENT_AND_PROVENANCE.json`).

This contract **references** that authority and **does not resolve** it.
**Current consent state is deliberately not recorded here** — caching mutable
authority state would make this contract stale the moment the owner resolves
consent. It must be read from the authority when it matters.

**Internal narrative planning and Story State design are distinct from
permission to publish a generated likeness commercially.** This contract makes
**no claim that consent is complete.**

## 16. Character records

The Story State represents exactly **INA** and **SIS**, each **exactly once**.

Per record: `identityAuthority: AVATAR_SKILL` · `identityPersistent: true` ·
`identityMutableByStory: false` · `narrativeRoleIsDynamic: true`.

**DUO must not become a third identity record.** Narrative-role content stays
flexible rather than a closed archetype enum. **No facial or biometric
descriptors.**

## 17. Pending proposals

A Story State may carry pending story or canon proposals. They remain explicitly
**`PROPOSAL`** and **MUST NOT silently become recorded Story State**.

Audience-influenced change lives here until a valid future transition rule
promotes it through the proper authority. A proposal may cite an influence
reference — **a pointer is not authority merely because it points somewhere.**

## 18. Lineage

Continuity must not depend on replacing the current state without trace, so the
snapshot carries `previousStoryStateRef` **and** `changedSincePrevious`.

Both are **required on every snapshot**. `changedSincePrevious` may be empty —
an empty array asserts nothing changed — but the key must be present, because an
absent key leaves *"no declared change information"* and *"nothing changed"*
indistinguishable, and §6 requires a fresh session to tell them apart. For an
initial state, `previousStoryStateRef` is `null` and `changedSincePrevious` is
`[]`.

An initial state may have `null` lineage, but the key is **required** so absence
is explicit rather than ambiguous. **No persistent ID format is defined**, and no
version-control infrastructure is built.

## 19. Hard failures

| Failure | Severity |
|---|---|
| `WRONG_CHARACTER_IDENTITY` | HARD_FAIL |
| `SISTER_SUBSTITUTION` | HARD_FAIL |
| `IDENTITY_MUTATED_BY_STORY` | HARD_FAIL |
| `GENERATED_OUTPUT_TREATED_AS_CANON` | HARD_FAIL |
| `MODEL_MEMORY_TREATED_AS_STORY_AUTHORITY` | HARD_FAIL |
| `AUDIENCE_SIGNAL_TREATED_AS_DIRECT_CANON_AUTHORITY` | HARD_FAIL |
| `OPERATIONAL_FACT_CONTRADICTION` | **STOP** |
| `PRIVATE_CHARACTER_DETAIL_IN_PUBLIC_STATE` | **STOP** |
| `UNDEFINED_STORY_TRANSITION_AUTHORITY` | **STOP** |

## 20. A schema is not an engine

- A Story State **schema** existing is **not** a Story State **Engine** existing.
- **Contract 03** existing is **not** a live Story State existing.
- A **synthetic fixture** existing is **not** real narrative state existing.

**No current story continuity may be fabricated merely to populate the schema.**

## 21. Interfaces with 01, 02 and 04

**Contract 01** remains authoritative for campaign-context idea generation, the
**exactly three** initial proposals, campaign character participation role and
owner selection. This contract changes **none** of it.

**Contract 02** remains authoritative for Product Truth, Product Locks and the
Human + Product dual lock. This contract weakens **neither** Human Truth nor
Product Truth.

**Contract 04** (`PINK_MALL_SOCIAL_INTELLIGENCE_CONTRACT`) is a **deferred
boundary**: metric weighting, scoring, social interpretation, creative fatigue
and evidence-driven story recommendations belong to it, and this contract
defines none of them. Contracts **06** (approval, spend, publication) and **07**
(semantic memory) are deferred the same way.

This contract records **which responsibilities are deferred, never whether the
receiving contract exists.** Live existence is read from
`SYSTEM_CONTRACT_INDEX.md`. **Authoring contract 04, 06 or 07 later must not
require editing this contract** — the boundary does not change when the other
side of it comes into being.

*(Current repository state, reported rather than frozen into this contract: no
contract 04 file exists.)*

## 22. Authority this contract does not grant

**No** story-transition authority · **no** publication authority · **no** spend
authority · **no** approval authority · **no** identity-write authority.

## 23. Public / private boundary

This repository is **PUBLIC**. Only public-safe **structure** lives here.

**MUST NOT** be committed: private biographies · personal history · private
interpersonal detail · private Creative Director detail · source likeness
material · unpublished real story plans · private campaign strategy · customer
data · private audience history · any real Story State instance.

Where a private field is structurally required, only the **schema or reference
shape** is defined; the content belongs to the future private ops layer.
**PINK-MALL-OPS remains PLANNED and MUST NOT be created.**

## 24. Open items

Genuinely undecided. They **MUST NOT** be answered by invention:

exact audience-to-canon decision rules · exact Story State implementation ·
exact private storage implementation · persistent Story State ID format · exact
audience thresholds · exact metric weights · exact social scoring · fatigue
thresholds · cooldown periods · exploration/exploitation ratio · Social
Intelligence API and data ingestion · automatic narrative-selection thresholds ·
exact Workstation integration · exact Super Brain bridge

The Story State **object shape** is deliberately **not** among them — this
contract formalises it.

## 25. STOP conditions

Stop rather than proceed when a canon transition has no defined authority; when
Story State would assert an operational fact its authority does not record; when
identity would be altered by a narrative event; when a generated output or model
memory is about to be treated as canon or authority; or when a question maps to
no rule here — that is a gap in the contract, not a licence to improvise.

## 26. Change control

Durable change follows the parent's change-control protocol: classify, update
the candidate, validate, independent review, then promote to canonical
development.
