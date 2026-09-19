# PINK MALL — Super Brain Memory Contract

| | |
|---|---|
| Contract ID | PINK_MALL_SUPER_BRAIN_MEMORY_CONTRACT |
| Version | 1.0.0 |
| Status | CANDIDATE |
| Machine-readable form | 07_SUPER_BRAIN_MEMORY_CONTRACT.json |
| Schema | 07_SUPER_BRAIN_MEMORY_CONTRACT.schema.json |
| Validator | tools/regression/super_brain_memory_contract.py |

## 1. Purpose

This contract defines the public-safe semantic-memory boundary for the planned PINK MALL Super Brain.
It preserves the locked owner decisions for structured memory, campaign memory, durable learning, preference drift and memory maintenance without inventing the private storage technology, API bridge or private memory content.

The Super Brain is PLANNED. This contract does not create a memory runtime, private ops store, graph database, API bridge, real-time knowledge service or learning engine.

## 2. Canonicality and inheritance

This contract inherits the System Authority Contract in full. Its status is provenance, not canonicality. Canonicality is decided only by Contract 00's four conditions.
GitHub remains the factual project authority. A semantic-memory assertion that exists only in model context, chat history or an ephemeral execution environment is not canonical project state.

## 3. Scope

### Covers
- conceptual Super Brain memory architecture;
- structured memory clusters plus free graph relationships;
- post-campaign Campaign Memory;
- durable-learning write rules;
- preference-drift states;
- provenance and evidence separation;
- periodic memory maintenance and cleanup;
- staleness and conflict handling;
- boundary between semantic memory and factual/operational authorities;
- public/private boundary;
- target of autonomous real-time knowledge.

### Does not cover
- exact persistent storage schema;
- exact graph implementation;
- exact API or bridge;
- private memory content;
- private strategy storage;
- social-platform ingestion;
- Story State authority or transition;
- Product Truth or Product Identity;
- approval, spend or publication;
- Workstation node architecture;
- PINK MALL HQ implementation.

## 4. Architecture

The locked architecture is:
1. Structured clusters — memory is organised into structured semantic groupings rather than one undifferentiated text store.
2. Free graph relationships — memory items may relate across clusters through relationships that are not restricted to a single hierarchy.

This contract does not freeze a private cluster taxonomy, graph database, edge vocabulary, storage engine or API.

## 5. Memory classes

| Class | Meaning | Authority |
|---|---|---|
| CAMPAIGN_MEMORY | Semantic memory written after a campaign about what was learned, observed or interpreted from that campaign. | SUPER_BRAIN |
| LEARNING_CANDIDATE | A possible durable learning not yet entitled to persist as a durable rule. | SUPER_BRAIN |
| DURABLE_LEARNING | A semantic learning that satisfied the locked durability rule. | SUPER_BRAIN |
| PREFERENCE_DRIFT | A pattern describing movement in a preference over time. | SUPER_BRAIN |
| MEMORY_MAINTENANCE_RECORD | A record of review, cleanup, contradiction handling or retirement. | SUPER_BRAIN |

These classes are semantic-memory records. They are not Product Truth, approval records, campaign operational state, raw social metrics or Story State.

## 6. Campaign Memory

Campaign Memory is written after campaigns.
A campaign-memory entry may preserve semantic evidence such as a mechanism, creative observation, audience interpretation, useful context or lesson from the completed campaign.
A campaign-memory entry MUST retain enough provenance to distinguish what was observed from what was interpreted or learned.

A campaign-memory entry MUST NOT fabricate campaign execution status, publication status, approval state, spend, Product Truth, Human Identity, Story State or raw social metrics.

The existence of a memory contract does not establish that a campaign occurred.

## 7. Durable Learning

Durable Learning is intentionally harder to earn than a one-off observation.
A semantic learning may become DURABLE_LEARNING only when at least one of the following is established:
- repeated evidence supports the pattern;
- sufficient signal supports the pattern;
- the owner explicitly confirms the learning.

The contract does not define a numeric threshold for sufficient signal.
A future implementation MUST preserve which basis justified durability and must not replace an open threshold with a guessed number.

### 7.1 One result is not permanent truth

One viral result must not become permanent truth automatically.
A highly successful single campaign, post, mechanism or signal may create a LEARNING_CANDIDATE, but it does not by itself become durable unless it also satisfies the durability rule above or receives explicit owner confirmation.

### 7.2 Evidence and interpretation remain separate

The Super Brain may store semantic interpretation, but it must preserve the distinction between observed fact/evidence, interpretation, learning candidate, durable learning, recommendation and approval.

## 8. Preference drift

Preference drift is a temporal semantic pattern, not a replacement for Product Truth or Human Truth.
The locked preference-drift states are STABLE, EMERGING, DECLINING and RETIRED.
A drift state describes the status of a semantic preference pattern over time. It does not assert that a product, price, size, availability, identity or approval state changed.
A future implementation MUST retain the evidence or memory lineage supporting a drift-state change.
No numeric drift threshold, time window or decay formula is defined here.

## 9. Memory maintenance and cleanup

Periodic memory maintenance and cleanup is required.
Maintenance must be able to identify and handle stale memory, contradictory memory, superseded memory, retired preference patterns, unsupported learning candidates and duplicate or redundant semantic records.
Cleanup MUST NOT silently convert uncertainty into fact.
Retirement or cleanup of semantic memory does not rewrite Product Truth, approval state, publication state or any other external authority.
The exact cadence, retention policy, conflict-resolution algorithm and storage mechanics are open.

## 10. Staleness and current-state use

Semantic memory is not automatically current fact.
When a memory entry concerns something that can change operationally — such as product availability, price, approval, publication, branch state or campaign execution — the implementation MUST consult the authoritative source rather than treating memory as current truth.
A stale or conflicting memory record may remain useful as historical context, but it MUST be labelled or handled as historical/uncertain rather than silently used as current factual state.
Memory is evidence or semantic context; it is not a shortcut around authority.

## 11. Authority boundaries

GitHub / the canonical project repository remains the factual authority for repository-backed project state.
Super Brain is explicitly non-authoritative for PM IDs, prices, sizes, availability, canonical product identity, approval state, branch or commit hash, campaign spend and publication state.
Super Brain also has no authority to rewrite Product Truth, Human Identity, Story State, raw social metrics or Campaign Registry operational state.
Where semantic memory conflicts with one of these authorities, the authoritative source wins and the memory is treated as stale, mistaken or interpretive.

## 12. Social Intelligence boundary

Contract 04 defines Super Brain as secondary evidence for social interpretation, not raw-metric authority.
The Super Brain MUST NOT overwrite a raw social metric, invent a missing metric, turn an interpretation into a raw fact, turn a recommendation into approval or turn audience engagement into publication authority.
Social evidence may contribute to semantic learning when the learning rules in this contract are satisfied, but source evidence and interpretation must remain distinguishable.

## 13. Story State boundary

Contract 03 owns Story State and narrative continuity.
Super Brain may preserve semantic context about story, audience or creative patterns, but it MUST NOT silently mutate Story State, declare canon or execute a story transition.
A memory of a previous story state is historical context, not authority for the current state.

## 14. Product and Human Truth boundary

Product Truth and Human Truth remain fixed.
Super Brain may remember semantic observations about creative work, products or characters, but it MUST NOT infer or overwrite canonical product identity, manufacturer item number, price, size, availability, canonical commerce media or Human Identity.
Generated output, memory confidence or semantic similarity is never a substitute for the authoritative product or identity source.

## 15. Provenance requirements

A future memory implementation MUST preserve provenance sufficient to answer: what the memory refers to; when or in which campaign/context it arose; what evidence or prior memory supports it; whether the entry is observation, interpretation, learning candidate, durable learning or preference drift; why durable learning was allowed when applicable; and whether the entry has been maintained, superseded or retired.
Opaque identifiers are preferred. No persistent ID format is defined here.
Private prompts, credentials, raw customer data, private performance history and confidential strategy MUST NOT be committed to this public repository.

## 16. Autonomous real-time knowledge target

Autonomous real-time knowledge is a target, not a current capability.
The target means a future Super Brain could continuously or automatically incorporate relevant current knowledge while respecting source authority, provenance, privacy and durability rules.
This contract does not assert that such real-time ingestion, retrieval or autonomous learning currently exists. No current runtime, connector, polling schedule, provider or API is implied.

## 17. Public/private boundary

PIERCIINA-PROJECT is a public repository.
Safe here: this contract, schemas describing the contract itself, validators, synthetic fixtures, stable public-safe vocabularies and authority boundaries.
MUST NOT be committed here: real private memory contents, private campaign strategy, real social performance history, private audience history, direct messages, customer or user identities, private prompts or source photographs, credentials, API tokens or secrets.
Where a private memory field is structurally required, only its public-safe shape or existence may be defined. The content belongs to a future private ops layer and must not be invented here.

## 18. Runtime existence boundary

This contract is a specification only.
It does not assert the existence of a Super Brain runtime, memory database, graph database, private ops store, API bridge, real-time knowledge ingestion, autonomous learning or live Campaign Memory store.
Current lifecycle state for named systems is owned by Contract 00's source registry and must be read there.

## 19. Open decisions

Exact private storage schema; exact graph/cluster implementation; exact API bridge; private memory content; exact cluster taxonomy; exact relationship/edge vocabulary; exact sufficient-signal threshold; exact repeated-evidence rule and counting window; exact preference-drift observation window; exact maintenance cadence; exact retention/decay policy; exact contradiction-resolution algorithm; exact real-time ingestion providers and refresh mechanics; exact confidence vocabulary; exact persistent memory ID format.

## 20. Hard failures

| Failure ID | Meaning | Severity |
|---|---|---|
| MEMORY_AS_PRODUCT_TRUTH | Semantic memory is treated as authority for product facts. | STOP |
| MEMORY_AS_APPROVAL | Memory is treated as approval. | STOP |
| MEMORY_AS_OPERATIONAL_STATE | Memory is treated as current campaign execution or operational state. | STOP |
| VIRAL_RESULT_AS_PERMANENT_TRUTH | One strong result is automatically promoted to durable truth. | HARD_FAIL |
| UNSUPPORTED_DURABLE_LEARNING | Durable learning is stored without an allowed durability basis. | HARD_FAIL |
| RAW_METRIC_OVERWRITE | Memory overwrites or replaces raw social evidence. | STOP |
| STORY_STATE_MUTATION | Memory directly mutates Story State or canon. | STOP |
| DRIFT_STATE_AS_PRODUCT_FACT | Preference drift is represented as a product or identity fact. | HARD_FAIL |
| STALE_MEMORY_USED_AS_CURRENT_FACT | Stale or conflicting memory is used as current operational truth without authority refresh. | HARD_FAIL |
| UNRESOLVED_MEMORY_PROVENANCE | A durable memory has no supporting provenance. | HARD_FAIL |
| PUBLIC_PRIVATE_MEMORY_LEAK | Private memory content or strategy is committed to the public repository. | STOP |
| RUNTIME_EXISTENCE_FABRICATION | A contract or schema is cited as proof that a Super Brain runtime exists. | STOP |
| UNKNOWN_DRIFT_STATE | A preference drift record uses a state outside the locked vocabulary. | HARD_FAIL |
| MEMORY_SILENTLY_ERASES_HISTORY | Cleanup destroys historical meaning or provenance without an explicit maintenance record. | HARD_FAIL |
| AUTHORITY_BYPASS | Memory is used to bypass a higher-authority source. | STOP |

## 21. Authority grants

This contract grants semantic-memory ownership to the future Super Brain domain only. It grants no Product Truth authority, Human Identity authority, Story State transition authority, approval authority, publication authority, spend authority, raw social metric authority, Campaign Registry operational-state authority or canonical-repository write authority.

## 22. Relationship to adjacent contracts

Contract 00 owns system authority, truth classes, source registry and canonical project state.
Contract 03 owns Story State and narrative continuity.
Contract 04 owns Social Intelligence interpretation and recommendation; Super Brain is secondary evidence there.
Contract 05 owns Workstation execution structure.
Contract 06 owns approval, spend and autonomy.
Contract 08 will own the HQ operating surface and visibility.
Authoring later contracts MUST NOT require this contract to cache their runtime existence.

## 23. Summary rule

> Super Brain may remember and learn semantically, but it may never become the source of factual or operational truth. Durable learning must be earned, one viral result is not permanent truth by itself, preference drift is temporal context, and maintenance keeps memory honest.