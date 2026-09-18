# PINK MALL — Social Intelligence Contract

`PINK_MALL_SOCIAL_INTELLIGENCE_CONTRACT` · version `1.0.0` · status `CANDIDATE` ·
contract `04` · parent `PINK_MALL_SYSTEM_AUTHORITY_CONTRACT`

Status is provenance. Canonicality is decided by the parent's four conditions,
never by this string and never by the fact that these files exist.

## 1. What this contract is for

Social evidence arrives as numbers. Numbers are persuasive, and a number that
nobody labelled will be read as a conclusion by whoever needs a conclusion. Once
that happens the argument is no longer about what the audience did — it is about
a recommendation somebody is already acting on.

This contract settles the labelling in advance, while nothing is at stake. It
defines how social evidence becomes interpretation and recommendation, and where
that chain is required to stop.

**This contract implements nothing.** It builds no engine, connects no social
platform, ingests no metric and stores no history. Whether a Social Intelligence
Engine or a platform connector has been built is read from contract 00's source
registry, never from this document.

## 2. The core separation

> **RAW SOCIAL METRIC ≠ DERIVED METRIC ≠ SOCIAL INTERPRETATION ≠ RECOMMENDATION
> ≠ APPROVAL ≠ STORY CANON ≠ PUBLICATION**

| Layer | Truth class | Authority | Owned here |
|---|---|---|---|
| `RAW_SOCIAL_METRIC` | `FACT` | `SOCIAL_PLATFORM_API` | no |
| `DERIVED_METRIC` | `DERIVED_FACT` | `SOCIAL_PLATFORM_API` | no |
| `SOCIAL_INTERPRETATION` | `INTERPRETATION` | `SOCIAL_INTELLIGENCE_ENGINE` | no |
| `RECOMMENDATION` | `PROPOSAL` | `SOCIAL_INTELLIGENCE_ENGINE` | no |
| `APPROVAL` | `APPROVAL` | `OWNER` | no |
| `STORY_CANON` | `FACT` | `STORY_STATE_ENGINE` | no |
| `PUBLICATION` | `APPROVAL` | `OWNER` | no |

Every boundary in that row is a decision someone must make, not a step that
happens on its own. **Raw evidence is not a conclusion. Interpretation is not a
fact about Product Truth or Human Identity. Recommendation is not approval.
Audience response is not publication authority. High engagement does not become
canon because it was high.**

## 3. Authority, inherited exactly

Contract 00 already settled both domains. This contract inherits them verbatim
and redefines neither.

**`SOCIAL_RAW_METRICS`** — primary authority `SOCIAL_PLATFORM_API`, secondary
evidence `CANONICAL_REPOSITORY`. Measured platform metrics are evidence.
`SOCIAL_INTELLIGENCE_ENGINE`, `SUPER_BRAIN` and `CHAT_HISTORY` are **not**
raw-metric authority, and none of them may overwrite a raw metric fact.

Letting the interpreter also own the measurement would remove the only
independent check on its own conclusions.

**`SOCIAL_INTERPRETATION`** — primary authority `SOCIAL_INTELLIGENCE_ENGINE`,
secondary evidence `SUPER_BRAIN`. Resonance, fatigue, winner readings and
recommendations are interpretation.

Being the authority for interpretation grants **nothing** outside that domain:
not Product Truth, not Human Identity, not Story State, not approval, not
publication, not spend, not canonical repository state.

## 4. Three statements that must never share a field

| Statement | Kind | Truth class |
|---|---|---|
| *"shares increased"* | raw social metric | `FACT` |
| *"this mechanism resonates"* | social interpretation | `INTERPRETATION` |
| *"continue this arc"* | recommendation | `PROPOSAL` |

The runtime snapshot therefore keeps `rawEvidence`, `interpretations` and
`recommendations` as separate structures. They may not be collapsed.

## 5. The response-priority hierarchy

The owner has locked a **qualitative** priority order. It is reproduced here
exactly, and deliberately without arithmetic.

| Tier | Priority | Signals |
|---|---|---|
| `TIER_PRIMARY` | PRIMARY | `SHARES` · `DM_SENDS` |
| `TIER_NEXT` | NEXT | `COMMENTS` · `DMS` · `FOLLOWER_GROWTH` · `SAVES` · `PROFILE_INTEREST` |
| `TIER_CONTEXTUAL` | LOWER-SIGNAL / CONTEXTUAL | `LIKES` · `VIEWS` |

Tier 1 is an act of passing something on. Tier 2 is deliberate engagement that
costs the audience something, short of passing it on. Tier 3 is cheap or
passive, read as context and never as a conclusion on its own.

**No number appears in this hierarchy.** Not a weight, not a score, not a ratio,
not points. Turning it into `share = 10, like = 1` is a numeric weighting
decision, and **no numeric weighting is authorised**.

The distinction is the whole point:

- **qualitative priority** — `LOCKED`
- **numeric weight** — `OPEN`

## 6. Two metric vocabularies

`prioritySignalId` is the closed set of nine signals the owner ranked, so a tier
claim about one of them is checkable.

`sourceNativeMetricId` is open, because a provider may report anything and
refusing to record an unrecognised metric would lose evidence.

**An open provider metric MUST NOT be placed in a priority tier** without a
published mapping rule. Until one exists it is recorded under its native name
with no tier. An unrecorded metric is invisible; an untiered one is merely
unranked, and that is the smaller loss.

## 7. Winning creative mechanisms

A winning mechanism **may be exploited temporarily**. That is a locked owner
decision and this contract preserves it.

What a strong result may **not** do is become permanent. A winner reading is a
reading of evidence, so it is `INTERPRETATION`. It is **not** a permanent brand
rule, **not** Product Truth, **not** Human Identity truth, and it does **not**
alter Story State by itself.

No numeric winner score is required, and none is defined.

## 8. Creative fatigue

**Fatigue MUST be considered before repetitive continuation.** That requirement
is locked. Its measurement is not.

Fatigue is an `INTERPRETATION`, not a raw metric. No post count, no day count
and no percentage drop is defined here. No closed fatigue taxonomy is invented
for schema convenience either, because the only locked decision is that fatigue
is tracked — inventing a vocabulary would read as a methodology nobody agreed to.

A snapshot must be able to show that fatigue was considered, which evidence was
used, what was concluded and how uncertain that is. Where continued exploitation
of a winning mechanism is recommended, the fatigue assessment **must** reference
evidence.

## 9. Recommending a story action

Contract 03 owns the meaning of `CONTINUE`, `EVOLVE`, `PAUSE`, `CLOSE` and
`REVIVE`. Contract 04 may use evidence to **recommend** one of them.

It **MUST NOT** redefine their narrative meaning, and it **MUST NOT** mutate
Story State. A story recommendation is a `PROPOSAL`.

Until a later canonical contract defines autonomous transition authority,
**recommendation does not equal transition.** No story-transition authority is
granted here.

## 10. Audience evidence and canon

Contract 03 already settled this, and contract 04 works inside that settlement.

Contract 04 **may** collect evidence, interpret it, identify support for a
possible story development, recommend a story action and support a `PROPOSAL`.

Contract 04 **may not** rewrite Story State, declare audience voting
automatically binding, invent a threshold that promotes a proposal to canon, or
treat engagement as approval.

## 11. Missing data is not zero

Social data is incomplete, and the tempting repair is the destructive one.

| State | Meaning |
|---|---|
| `AVAILABLE` | the source reported a value, and it is recorded |
| `UNKNOWN` | the value may exist but was not obtained |
| `UNAVAILABLE` | the source does not provide it, or could not be reached |
| `NOT_APPLICABLE` | the metric has no meaning for this subject |
| `NOT_MEASURED` | it applies and could have been collected, but was not |

**Zero is a measurement.** The other four are not, and converting any of them to
zero invents evidence. An observed value is therefore permitted **only** when
availability is `AVAILABLE`, and is structurally forbidden otherwise — so a
missing metric cannot be laundered into a number a later interpretation treats
as real.

## 12. Normalisation

Exact cross-platform normalisation is **open**. A share on one platform is not
declared equal to a send on another, because no rule says so.

Source-native metrics are recorded with their provenance. A normalised figure
may be classed `DERIVED_FACT` only where a **published deterministic rule**
produces it reproducibly; the schema requires that rule to be referenced.
Otherwise it is interpretation wearing a number's clothes.

## 13. Priority does not authorise action

The hierarchy informs how evidence is read. It authorises nothing: no automatic
story change, campaign selection, publication, spend, retry or budget
escalation. Contract 06 owns approval, spend, publication and every
earned-autonomy grant.

## 14. Interfaces

**Campaign Context (01).** Contract 04 may produce structured social
intelligence for a future Campaign Context Builder. Contract 01 already classes
such signals as evidence that must not override Product Truth, Human Truth,
heritage or an approval, and the handoff inherits those rules unchanged. Nothing
here modifies contract 01.

**Super Brain (07).** Super Brain may provide secondary evidence to social
interpretation, and social intelligence may later feed semantic learning. Memory
schema, write policy, staleness and preference drift belong to contract 07 and
are not defined here. Super Brain must never overwrite a raw metric fact.

## 15. Provenance

Every raw metric retains which authority produced it, which subject it refers
to, which metric it represents and which observation window it belongs to.

Every interpretation references the evidence it used. Every recommendation
references the interpretations or evidence supporting it. **A recommendation
with no supporting reference MUST NOT be recorded.**

A reference is a pointer. A pointer is not a grant of authority.

### 15.1 References must resolve, and identifiers must be unambiguous

**A non-empty string is not evidence.** Every reference MUST resolve to exactly
one record present in the same snapshot; an unresolved reference is no
provenance at all.

That requires unambiguous identifiers, so `evidenceRef`, `interpretationRef`,
`assessmentRef` and `recommendationRef` share **one identifier space per
snapshot**. Uniqueness is enforced across the whole snapshot rather than per
collection: an interpretation named after a piece of evidence makes every
reference to that name ambiguous, and the ambiguity is silent because both
readings look valid.

Identifiers stay **opaque**. No format is defined and none is needed —
uniqueness is a property of one snapshot, not a global ID scheme.

Each kind may rest only on what sits beneath it:

| Referring record | May reference |
|---|---|
| interpretation | raw evidence |
| creative mechanism assessment | raw evidence · interpretation |
| fatigue assessment | raw evidence · interpretation |
| recommendation | raw evidence · interpretation |

An interpretation is drawn **from** measurement, so it may not cite another
conclusion — that would let a reading rest on a reading with no evidence
underneath. **Nothing may cite a recommendation:** a proposal is not support.
Nothing may cite a creative mechanism assessment either.

Where a conclusion *is* cited, it must itself be grounded: **a cited
interpretation MUST rest on at least one resolvable raw evidence record.**
Otherwise an unsupported reading launders into support for something else one
hop away.

These target sets are **unchanged from the reviewed base.** This correction adds
the requirement that a reference *resolves*; it does not widen what may be
cited.

### 15.2 What each validation layer actually proves

A snapshot is accepted only when **both** layers pass.

| Layer | Proves |
|---|---|
| JSON Schema (Draft 2020-12) | the shape of each record — required fields, closed vocabularies, closed objects, and the availability-to-value binding that keeps a missing metric from becoming a zero |
| semantic reference-integrity validation | that every reference resolves to exactly one present record of a permitted kind, and that no two records share an identifier |

**JSON Schema alone does not enforce cross-record resolution or uniqueness by an
arbitrary identifier property.** Draft 2020-12 has no keyword for either;
`uniqueItems` compares whole items, so two records differing in any other field
satisfy it while sharing an id. Claiming schema conformance alone would misstate
what has been checked.

## 16. The Social Intelligence Snapshot

`04_SOCIAL_INTELLIGENCE_OBJECT.schema.json` describes future runtime structure
only — the snapshot a Social Intelligence Engine would emit. **A schema is not
an engine.**

It carries `schemaVersion`, an opaque `snapshotRef`, an opaque `subjectRef` and
`subjectType`, an opaque `observationWindowRef`, then `rawEvidence`,
`interpretations`, `creativeMechanismAssessments`, `fatigueAssessment`,
`recommendations`, `knownLimitations` and `provenance`.

References are opaque. **No persistent ID format is defined**, and no ingestion
infrastructure is described — but within a single snapshot every identifier is
unique and every reference resolves, per §15.1.

`assertionsOutsideAuthority` is structurally empty: a snapshot asserts no
product truth, no human identity, no approval, no publication and no Story State
transition, and the array exists so that emptiness is explicit rather than
merely absent.

## 17. Hard failures

| Failure | Severity |
|---|---|
| `RAW_METRIC_AUTHORITY_CLAIMED_BY_INTERPRETER` | HARD_FAIL |
| `INTERPRETATION_RECORDED_AS_FACT` | HARD_FAIL |
| `RECOMMENDATION_RECORDED_AS_APPROVAL` | HARD_FAIL |
| `MISSING_METRIC_RECORDED_AS_ZERO` | HARD_FAIL |
| `UNSUPPORTED_RECOMMENDATION` | HARD_FAIL |
| `NUMERIC_WEIGHT_ATTACHED_TO_PRIORITY_SIGNAL` | HARD_FAIL |
| `UNKNOWN_METRIC_SILENTLY_TIERED` | HARD_FAIL |
| `STORY_STATE_MUTATED_BY_SOCIAL_EVIDENCE` | HARD_FAIL |
| `UNKNOWN_STORY_ACTION_RECOMMENDED` | HARD_FAIL |
| `FATIGUE_BYPASSED_ON_REPETITIVE_EXPLOITATION` | HARD_FAIL |
| `INVENTED_NUMERIC_THRESHOLD` | HARD_FAIL |
| `PRODUCT_TRUTH_OVERRIDDEN_BY_SOCIAL_INTERPRETATION` | HARD_FAIL |
| `HUMAN_IDENTITY_CHANGED_BY_SOCIAL_EVIDENCE` | HARD_FAIL |
| `WINNER_TREATED_AS_PERMANENT_RULE` | HARD_FAIL |
| `PRIVATE_PERFORMANCE_DATA_IN_PUBLIC_STATE` | HARD_FAIL |
| `ENGAGEMENT_TREATED_AS_APPROVAL` | HARD_FAIL |
| `UNRESOLVED_EVIDENCE_REFERENCE` | HARD_FAIL |
| `AMBIGUOUS_RECORD_IDENTIFIER` | HARD_FAIL |
| `REFERENCE_TO_INAPPROPRIATE_RECORD_KIND` | HARD_FAIL |
| `UNGROUNDED_INTERPRETATION_CITED_AS_SUPPORT` | HARD_FAIL |

## 18. Authority this contract does not grant

**No** product-truth write authority · **no** human-identity write authority ·
**no** story-transition authority · **no** story-canon write authority · **no**
approval authority · **no** publication authority · **no** spend authority ·
**no** autonomous-action authority · **no** canonical-repository write authority.

## 19. Deferred boundaries

| Contract | What belongs there |
|---|---|
| 05 Workstation Operating | node architecture, workflow graph, run model, job scheduling |
| 06 Automation & Approval | approval flow, budget modes, spend ceilings, publication, autonomy grants |
| 07 Super Brain Memory | memory schema, write rules, staleness, preference drift |
| 08 PINK MALL HQ | how social intelligence is reported and surfaced to an operator |

This contract records **which responsibilities are deferred, never whether the
receiving contract exists.** Live existence is read from
`SYSTEM_CONTRACT_INDEX.md`. **Authoring contract 05, 06, 07 or 08 later must not
require editing this contract** — the boundary does not change when the other
side of it comes into being.

## 20. Public / private boundary

`PIERCIINA-PROJECT` is a **PUBLIC** repository.

Public-safe and living here: this contract, its schemas, stable vocabularies,
validation rules and synthetic fixtures.

**MUST NOT** be committed: real social account metrics · real campaign
performance history · private audience history · direct message contents ·
customer or user identities · private strategy · private competitor analysis ·
any real Social Intelligence Snapshot. Social and provider credentials, API
tokens and secrets **MUST NOT** be committed to any repository.

Where a private field is structurally required, only the **schema or reference
shape** is defined; the content belongs to the private ops layer, which lives
outside this public repository. **This contract does not create that layer and
does not record its lifecycle state** — contract 00's source registry owns it,
and building the layer later does not make this contract stale.

## 21. Open items

Genuinely undecided. They **MUST NOT** be answered by invention:

exact numeric metric weights · exact winner score or formula · exact fatigue
threshold · exact cooldown duration · exact exploration/exploitation ratio ·
exact observation windows and freshness rules · exact API, provider and
ingestion implementation · exact account and platform connectors · exact
cross-platform normalisation · exact autonomous campaign-selection threshold ·
exact autonomous story-transition threshold · exact publication rule · persistent
snapshot ID format · private performance-history storage · qualitative
confidence vocabulary, which no owner decision has locked.

The **RESPONSE-PRIORITY HIERARCHY is deliberately NOT among them.** It is locked
as a qualitative order; only its conversion into numbers remains open. Recording
a plausible number here would erase the difference between a decision the owner
made and a default a system chose.

## 22. Change control

Durable change follows the parent's protocol: classify, update the candidate,
validate, independent review, then promote to canonical development.
