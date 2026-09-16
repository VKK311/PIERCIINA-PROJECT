#!/usr/bin/env python3
"""Validator for the PINK MALL System Authority Contract.

    python tools/regression/system_authority_contract.py

The authority contract is the constitutional layer beneath every later campaign,
story, social-intelligence, memory and publication system. Those systems will
read the machine-readable form and act on it, so a silently dropped domain, a
stale status flag or a human/JSON disagreement is not a documentation defect —
it is a governance defect that would let a later system claim an authority the
owner never granted.

This checks structure, vocabulary and the specific rules that must not be lost:
no planned system marked ACTIVE, semantic memory never authoritative for product
facts, generated media never authoritative for canonical commerce media, the
private ops store still PLANNED, and the human-readable contract agreeing with
the JSON on identity and version.

Standard library only, by design: the foundation must not grow a dependency to
check its own constitution.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CDIR = os.path.join(ROOT, "docs", "pink-mall", "system-contracts")
JSON_PATH   = os.path.join(CDIR, "00_SYSTEM_AUTHORITY_CONTRACT.json")
SCHEMA_PATH = os.path.join(CDIR, "00_SYSTEM_AUTHORITY_CONTRACT.schema.json")
MD_PATH     = os.path.join(CDIR, "00_SYSTEM_AUTHORITY_CONTRACT.md")
INDEX_PATH  = os.path.join(CDIR, "SYSTEM_CONTRACT_INDEX.md")
MATRIX_PATH = os.path.join(CDIR, "DECISION_COVERAGE_MATRIX.md")

EXPECTED_CONTRACT_ID = "PINK_MALL_SYSTEM_AUTHORITY_CONTRACT"

REQUIRED_DOMAINS = {
    "SYSTEM_GOVERNANCE", "CANONICAL_REPOSITORY_STATE", "PRODUCT_IDENTITY", "PRODUCT_PRICE",
    "PRODUCT_AVAILABILITY_AND_SIZES", "CANONICAL_PRODUCT_MEDIA", "HUMAN_IDENTITY",
    "AVATAR_CONSENT_STATUS", "CAMPAIGN_OPERATIONAL_STATE", "STORY_STATE", "SOCIAL_RAW_METRICS",
    "SOCIAL_INTERPRETATION", "SEMANTIC_CREATIVE_MEMORY", "GENERATED_CAMPAIGN_MEDIA",
    "CAMPAIGN_APPROVAL", "PAID_GENERATION_AUTHORITY", "COMMERCIAL_PUBLICATION",
    "PRIVATE_STRATEGIC_DATA",
}
REQUIRED_SOURCES = {
    "OWNER", "CANONICAL_REPOSITORY", "PRODUCT_ONBOARDING_SYSTEM", "AVATAR_SKILL",
    "FASHION_CONTEXT_BUILDER", "CAMPAIGN_REGISTRY", "STORY_STATE_ENGINE", "SOCIAL_PLATFORM_API",
    "SOCIAL_INTELLIGENCE_ENGINE", "SUPER_BRAIN", "CYBERNINJAS_STUDIO", "WORKSTATION",
    "CLAUDE_ORCHESTRATOR", "MODEL_MEMORY", "CHAT_HISTORY", "PRIVATE_OPS_STORE",
}
VALID_STATES = {"ACTIVE", "PARTIAL", "PLANNED", "BLOCKED", "HISTORICAL"}
REQUIRED_TRUTH_CLASSES = {"FACT", "DERIVED_FACT", "INTERPRETATION", "PROPOSAL",
                          "GENERATED_OUTPUT", "APPROVAL"}
REQUIRED_MEDIA_CLASSES = {"CANONICAL_COMMERCE_MEDIA", "CAMPAIGN_MEDIA", "DERIVATIVE_MEDIA"}
REQUIRED_OVERRIDES = {"ONE_TIME_EXCEPTION", "DURABLE_POLICY_CHANGE"}
REQUIRED_PRIVACY_CLASSES = {"PUBLIC_SAFE", "PRIVATE_OPS_REQUIRED", "NEVER_PERSIST_IN_ANY_REPOSITORY"}
# Systems that do not exist. None may be described as ACTIVE.
PLANNED_SOURCES = {"CAMPAIGN_REGISTRY", "STORY_STATE_ENGINE", "SOCIAL_PLATFORM_API",
                   "SOCIAL_INTELLIGENCE_ENGINE", "SUPER_BRAIN", "WORKSTATION", "PRIVATE_OPS_STORE"}
# Facts Super Brain must never own, phrased as the contract phrases them.
SEMANTIC_FORBIDDEN = ["PM IDs", "prices", "sizes", "canonical product identity",
                      "approval state", "exact publication state"]
EIGHT_INTERVIEWS = [
    "Campaign Context", "Product Creative", "Character & Story",
    "Social Intelligence", "Workstation Operating", "Automation & Approval",
    "Super Brain Memory", "PINK MALL HQ",
]

# Spelled-out and numeric forms of a count, for prose that states how many
# canonicality conditions there are. Checking meaning rather than punctuation.
NUMBER_WORDS = {1: ("one", "1"), 2: ("two", "2"), 3: ("three", "3"),
                4: ("four", "4"), 5: ("five", "5"), 6: ("six", "6")}


def _states_count(text, n):
    """True if text asserts n conditions, in words or digits."""
    low = text.lower()
    return any(f"{w} condition" in low or f"{w}** condition" in low or
               f"all {w}" in low or f"all **{w}**" in low
               for w in NUMBER_WORDS[n])


passed, failed = 0, 0


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS  {name}" + (f"  — {detail}" if detail else ""))
    else:
        failed += 1
        print(f"  FAIL  {name}" + (f"  — {detail}" if detail else ""))
    return bool(cond)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main():
    print("== PINK MALL system authority contract ==")

    for p in (JSON_PATH, SCHEMA_PATH, MD_PATH, INDEX_PATH, MATRIX_PATH):
        if not os.path.exists(p):
            check(f"required file present: {os.path.basename(p)}", False, "missing")
            print("\nSYSTEM AUTHORITY CONTRACT: FAIL (cannot continue)")
            sys.exit(1)

    # 1 — JSON parses
    try:
        c = json.loads(read(JSON_PATH))
        check("1. contract JSON parses", True)
    except Exception as e:                                        # noqa: BLE001
        check("1. contract JSON parses", False, str(e)[:90])
        print("\nSYSTEM AUTHORITY CONTRACT: FAIL (cannot continue)")
        sys.exit(1)
    try:
        schema = json.loads(read(SCHEMA_PATH))
        check("   schema JSON parses", True)
    except Exception as e:                                        # noqa: BLE001
        check("   schema JSON parses", False, str(e)[:90])
        print("\nSYSTEM AUTHORITY CONTRACT: FAIL (cannot continue)")
        sys.exit(1)

    # 2 / 3 — identity and version
    check("2. contractId is exactly the expected value",
          c.get("contractId") == EXPECTED_CONTRACT_ID, str(c.get("contractId")))
    ver = c.get("version", "")
    check("3. version is semantic (MAJOR.MINOR.PATCH)",
          bool(re.fullmatch(r"\d+\.\d+\.\d+", str(ver))), str(ver))
    check("   status is a known lifecycle value",
          c.get("status") in {"CANDIDATE", "CANONICAL", "SUPERSEDED"}, str(c.get("status")))

    # 4 — canonicality rule: four conditions, retirement among them
    cr = c.get("canonicalityRule") or {}
    conds = cr.get("conditions", [])
    check("4. canonicalityRule exists with all four conditions",
          bool(cr) and len(conds) >= 4, f"{len(conds)} conditions")
    joined = " ".join(conds).lower()
    for label, needle in (("review", "review"),
                          ("canonical branch", "claude/pink-mall-development"),
                          ("validator", "validator"),
                          ("not superseded", "superseded")):
        check(f"   condition present: {label}", needle in joined)
    # The prose statement and the conditions array are two representations of
    # one fact, and they drifted apart once: conditions grew to four while the
    # statement still said three. Agreement is asserted by meaning rather than
    # by exact sentence, so rewording stays allowed and miscounting does not.
    stmt = cr.get("statement", "")
    n = len(conds)
    check("   canonicalityRule.statement agrees with the conditions array",
          _states_count(stmt, n), f"{n} conditions, statement says: {stmt!r}")
    check("   statement does not claim three conditions",
          not _states_count(stmt, 3) or n == 3, f"statement={stmt!r}")
    check("   file existence alone is NOT canonicality",
          cr.get("fileExistenceImpliesCanonicality") is False)
    check("   candidate branch is declared review material",
          cr.get("candidateBranchIsReviewMaterial") is True)

    # 5 / 6 — domains
    domains = c.get("authorityDomains", [])
    ids = [d.get("domainId") for d in domains]
    missing = REQUIRED_DOMAINS - set(ids)
    check("5. all required authority domains are present",
          not missing, f"{len(ids)} present; missing={sorted(missing)}")
    check("6. authority-domain ids are unique",
          len(ids) == len(set(ids)), f"{len(ids) - len(set(ids))} duplicates")
    check("   every domain names at least one primary authority",
          all(d.get("primaryAuthority") for d in domains),
          str([d["domainId"] for d in domains if not d.get("primaryAuthority")]))
    check("   every domain states a conflict action",
          all(d.get("conflictAction") for d in domains))
    check("   no domain lists the same source as primary and non-authoritative",
          all(not (set(d.get("primaryAuthority", [])) & set(d.get("nonAuthoritative", [])))
              for d in domains),
          str([d["domainId"] for d in domains
               if set(d.get("primaryAuthority", [])) & set(d.get("nonAuthoritative", []))]))

    # 7 / 8 — truth and media classes
    tids = [t.get("classId") for t in c.get("truthClasses", [])]
    check("7. truth-class ids are unique and complete",
          len(tids) == len(set(tids)) and REQUIRED_TRUTH_CLASSES <= set(tids),
          f"{sorted(set(tids))}")
    mids = [m.get("classId") for m in c.get("mediaClasses", [])]
    check("8. media-class ids are unique and complete",
          len(mids) == len(set(mids)) and REQUIRED_MEDIA_CLASSES <= set(mids),
          f"{sorted(set(mids))}")
    canon_media = next((m for m in c.get("mediaClasses", [])
                        if m.get("classId") == "CANONICAL_COMMERCE_MEDIA"), {})
    check("   canonical commerce media forbids generative alteration",
          canon_media.get("generativeAlterationAllowed") is False)

    # 9 — implementation-state vocabulary
    declared = set(c.get("implementationStates", {}))
    check("9. implementation-state vocabulary is exactly the valid set",
          declared == VALID_STATES, f"declared={sorted(declared)}")
    bad_state = [d["domainId"] for d in domains if d.get("implementationStatus") not in VALID_STATES]
    check("   every domain uses a valid implementation state", not bad_state, str(bad_state))
    bad_src = [s["sourceId"] for s in c.get("sourceTypes", [])
               if s.get("implementationStatus") not in VALID_STATES]
    check("   every source uses a valid implementation state", not bad_src, str(bad_src))

    # 10 — owner override types
    over = {o.get("typeId") for o in c.get("ownerOverrideTypes", [])}
    check("10. owner override types include both required kinds",
          REQUIRED_OVERRIDES <= over, str(sorted(over)))
    onetime = next((o for o in c.get("ownerOverrideTypes", [])
                    if o.get("typeId") == "ONE_TIME_EXCEPTION"), {})
    durable = next((o for o in c.get("ownerOverrideTypes", [])
                    if o.get("typeId") == "DURABLE_POLICY_CHANGE"), {})
    check("    a one-time exception does not mutate policy",
          onetime.get("mutatesPolicy") is False)
    check("    a durable policy change does mutate policy",
          durable.get("mutatesPolicy") is True)

    # 11 — conflict handling
    rules = c.get("conflictRules", [])
    same = next((r for r in rules if r.get("ruleId") == "SAME_DOMAIN_CANONICAL_CONFLICT"), None)
    check("11. same-domain canonical conflict STOPs and never auto-resolves",
          same is not None and same.get("action") == "STOP" and same.get("mayAutoResolve") is False,
          str(same.get("action") if same else "rule absent"))
    check("    an undefined domain also STOPs",
          any(r.get("ruleId") == "UNKNOWN_DOMAIN" and r.get("action") == "STOP" for r in rules))
    check("    semantic state never overrides canonical truth",
          any(r.get("ruleId") == "SEMANTIC_VS_CANONICAL" and r.get("action") == "CANONICAL_WINS"
              for r in rules))

    # 12 — semantic memory is not authoritative for product facts
    sem = next((n for n in c.get("nonAuthoritativeAssertions", [])
                if n.get("sourceId") == "SUPER_BRAIN"), {})
    forbidden = [f.lower() for f in sem.get("mustNotBeAuthoritativeFor", [])]
    gaps = [f for f in SEMANTIC_FORBIDDEN if f.lower() not in forbidden]
    check("12. semantic memory is explicitly non-authoritative for product/catalogue facts",
          not gaps, f"unlisted={gaps}")
    sem_dom = next((d for d in domains if d["domainId"] == "SEMANTIC_CREATIVE_MEMORY"), {})
    check("    semantic memory never claims the canonical repository",
          "CANONICAL_REPOSITORY" in sem_dom.get("nonAuthoritative", []))
    for pd in ("PRODUCT_PRICE", "PRODUCT_IDENTITY", "PRODUCT_AVAILABILITY_AND_SIZES"):
        d = next((x for x in domains if x["domainId"] == pd), {})
        check(f"    SUPER_BRAIN is non-authoritative for {pd}",
              "SUPER_BRAIN" in d.get("nonAuthoritative", []))

    # 13 — generated media is not canonical commerce media
    gen = next((d for d in domains if d["domainId"] == "GENERATED_CAMPAIGN_MEDIA"), {})
    check("13. generated campaign media never holds canonical commerce media authority",
          "PRODUCT_ONBOARDING_SYSTEM" in gen.get("nonAuthoritative", [])
          and gen.get("conflictAction") == "REJECT_CANDIDATE",
          f"conflictAction={gen.get('conflictAction')}")
    cpm = next((d for d in domains if d["domainId"] == "CANONICAL_PRODUCT_MEDIA"), {})
    check("    canonical product media excludes the generation systems",
          {"CYBERNINJAS_STUDIO", "WORKSTATION"} <= set(cpm.get("nonAuthoritative", [])))
    check("    media rules forbid silent replacement of commerce media",
          any("never" in r.lower() and "replace" in r.lower() for r in c.get("mediaClassRules", [])))

    # 14 — planned systems are not ACTIVE
    active_planned = [s["sourceId"] for s in c.get("sourceTypes", [])
                      if s["sourceId"] in PLANNED_SOURCES and s.get("implementationStatus") == "ACTIVE"]
    check("14. no planned system is marked ACTIVE", not active_planned, str(active_planned))
    planned_names = set(c.get("currentSystemStatus", {}).get("PLANNED", []))
    active_names = set(c.get("currentSystemStatus", {}).get("ACTIVE", []))
    check("    the status inventory does not list a system as both ACTIVE and PLANNED",
          not (planned_names & active_names), str(sorted(planned_names & active_names)))
    check("    no autonomous authority is granted",
          c.get("earnedAutonomy", {}).get("currentGrants") == [])

    # 15 / 16 — privacy classes and the private store
    pcls = {p.get("classId") for p in c.get("privacyClasses", [])}
    check("15. public/private classes are present", REQUIRED_PRIVACY_CLASSES <= pcls, str(sorted(pcls)))
    ops = next((s for s in c.get("sourceTypes", []) if s["sourceId"] == "PRIVATE_OPS_STORE"), {})
    check("16. PINK-MALL-OPS is PLANNED, not existing or active",
          ops.get("implementationStatus") == "PLANNED", str(ops.get("implementationStatus")))
    check("    a privacy rule states the private store must not be described as existing",
          any("must not be described as existing" in r.lower() for r in c.get("privacyRules", [])))
    private_cls = next((p for p in c.get("privacyClasses", [])
                        if p.get("classId") == "PRIVATE_OPS_REQUIRED"), {})
    inc = " ".join(private_cls.get("includes", [])).lower()
    check("    private class covers source photographs and private strategy",
          "photograph" in inc and "strategy" in inc)

    # consent must not be overclaimed — the repository says it is unresolved
    consent = next((d for d in domains if d["domainId"] == "AVATAR_CONSENT_STATUS"), {})
    check("    avatar consent is not represented as resolved",
          consent.get("implementationStatus") == "BLOCKED",
          str(consent.get("implementationStatus")))
    check("    commercial generated-likeness publication is a hard stop",
          any(h.get("stopId") == "CONSENT_GATE_UNRESOLVED" for h in c.get("hardStops", [])))

    # 17 — planned contract ids unique
    pc = c.get("plannedContracts", [])
    pcids = [p.get("contractId") for p in pc]
    pcnums = [p.get("contractNumber") for p in pc]
    check("17. planned contract ids are unique",
          len(pcids) == len(set(pcids)), f"{len(pcids) - len(set(pcids))} duplicates")
    check("    planned contract numbers are unique and cover 00-08",
          len(pcnums) == len(set(pcnums)) and {f"{i:02d}" for i in range(9)} <= set(pcnums),
          str(sorted(pcnums)))
    check("    only contract 00 is marked created",
          [p["contractNumber"] for p in pc if p.get("created")] == ["00"],
          str([p["contractNumber"] for p in pc if p.get("created")]))

    # 18 — human-readable and JSON agree
    md = read(MD_PATH)
    check("18. markdown contract states the same contract id",
          EXPECTED_CONTRACT_ID in md)
    check("    markdown contract states the same version",
          f"`{ver}`" in md or f" {ver}" in md, str(ver))
    check("    markdown contract states the same status",
          str(c.get("status")) in md)
    md_domains = [d for d in sorted(REQUIRED_DOMAINS) if d not in md]
    check("    markdown documents every authority domain", not md_domains, str(md_domains))

    # 19 — index references the authority contract
    idx = read(INDEX_PATH)
    check("19. SYSTEM_CONTRACT_INDEX references the authority contract",
          "00_SYSTEM_AUTHORITY_CONTRACT" in idx)
    check("    index states the canonicality rule",
          "canonical" in idx.lower() and "candidate branch" in idx.lower())
    # Condition-count agreement across all three representations. Scoped to the
    # canonicality passage, because 'all three states' elsewhere in the index
    # describes decision states and is not a condition count.
    for label, text in (("markdown", md), ("index", idx)):
        low = text.lower()
        at = low.find("canonical only when")
        window = low[at:at + 240] if at >= 0 else ""
        check(f"    {label} states the canonicality condition count as {len(conds)}",
              bool(window) and _states_count(window, len(conds)),
              f"window={window[:70]!r}")
        check(f"    {label} canonicality passage does not say three",
              not (window and len(conds) != 3 and _states_count(window, 3)))

    check("    index marks the eight future contracts as not yet created",
          idx.upper().count("NOT YET CREATED") >= 8,
          f"{idx.upper().count('NOT YET CREATED')} occurrences")

    # 20 — decision coverage matrix
    matrix = read(MATRIX_PATH)
    absent = [d for d in EIGHT_INTERVIEWS if d.lower() not in matrix.lower()]
    check("20. DECISION_COVERAGE_MATRIX contains all eight interview domains",
          not absent, f"absent={absent}")
    check("    matrix separates 'locked decision' from 'contract created'",
          "LOCKED DECISION EXISTS" in matrix.upper()
          and "DETAILED CANONICAL CONTRACT CREATED" in matrix.upper())
    check("    matrix defers private strategy rather than publishing it",
          "PRIVATE DETAIL REQUIRED" in matrix.upper())

    # schema sanity — it must actually constrain
    props = schema.get("properties", {})
    check("    schema requires the contract id as a constant",
          props.get("contractId", {}).get("const") == EXPECTED_CONTRACT_ID)
    check("    schema closes the authority-domain vocabulary",
          REQUIRED_DOMAINS <= set(props.get("authorityDomains", {})
                                  .get("items", {}).get("properties", {})
                                  .get("domainId", {}).get("enum", [])))
    # minItems + uniqueItems does NOT prove completeness: uniqueItems compares
    # whole objects, so two records could share a domainId while differing in
    # another field, satisfying the array constraints while a required domain is
    # absent. Exactly-once coverage has to be asserted per domain id.
    ad = props.get("authorityDomains", {})
    check("    schema declares minItems matching the required domain count",
          ad.get("minItems") == len(REQUIRED_DOMAINS), str(ad.get("minItems")))
    allof = ad.get("allOf", [])
    covered, malformed = set(), []
    for rule in allof:
        con = rule.get("contains", {})
        const = con.get("properties", {}).get("domainId", {}).get("const")
        if const is None:
            malformed.append(rule)
            continue
        covered.add(const)
        if rule.get("minContains") != 1 or rule.get("maxContains") != 1:
            malformed.append(const)
    check("    schema requires EACH domain exactly once via allOf/contains",
          covered == REQUIRED_DOMAINS and not malformed,
          f"covered={len(covered)}/{len(REQUIRED_DOMAINS)} "
          f"missing={sorted(REQUIRED_DOMAINS - covered)} malformed={malformed}")
    check("    every contains rule is minContains=maxContains=1",
          all(r.get("minContains") == 1 and r.get("maxContains") == 1 for r in allof),
          f"{len(allof)} rules")
    check("    schema does not rely on uniqueItems alone for completeness",
          bool(allof), "allOf/contains rules absent" if not allof else "")
    check("    schema rejects unknown top-level properties",
          schema.get("additionalProperties") is False)
    check("    schema's required list covers every property it defines",
          set(schema.get("required", [])) >= set(props) - {"supersedes"},
          str(sorted(set(props) - {"supersedes"} - set(schema.get("required", [])))))

    # ── status: two kinds of label, not one informational blanket ─────────
    print("  -- status model --")
    ss = cr.get("statusSemantics") or {}
    check("21. status semantics distinguish provenance labels from a tombstone",
          set(ss.get("canonicalityLabels", [])) == {"CANDIDATE", "CANONICAL"}
          and ss.get("tombstoneLabels") == ["SUPERSEDED"],
          f"labels={ss.get('canonicalityLabels')} tombstone={ss.get('tombstoneLabels')}")
    check("    CANDIDATE alone does not deny canonicality",
          ss.get("candidateAloneDeniesCanonicality") is False)
    check("    CANONICAL alone does not grant canonicality",
          ss.get("canonicalAloneGrantsCanonicality") is False)
    check("    SUPERSEDED explicitly disqualifies reliance",
          ss.get("supersededDisqualifiesReliance") is True)
    check("    exact-byte candidate promotion remains permitted",
          ss.get("exactByteCandidatePromotionPermitted") is True)
    check("    no field claims every status value is purely informational",
          "statusIsInformationalOnly" not in cr,
          "legacy blanket field still present" if "statusIsInformationalOnly" in cr else "")
    # the contract must not resurrect the fiction that a superseded contract
    # retroactively fails its historical review
    rule_text = (ss.get("rule", "") + " " + cr.get("statusRule", "")).lower()
    check("    superseded is disqualified by replacement, not by failed review",
          "replaced" in rule_text and "historical review" in rule_text)
    sem = {str(k).upper(): str(v).lower()
           for k, v in (cr.get("statusFieldSemantics") or {}).items()}
    check("    all three status values are defined",
          {"CANDIDATE", "CANONICAL", "SUPERSEDED"} <= set(sem), str(sorted(sem)))
    check("    CANDIDATE is not described as unreliable by status alone",
          "must not be relied upon" not in sem.get("CANDIDATE", ""),
          str(sem.get("CANDIDATE", "<absent>"))[:70])
    check("    SUPERSEDED is described as disqualifying",
          "disqualif" in sem.get("SUPERSEDED", ""))
    for label, text in (("markdown", md), ("index", idx)):
        low = text.lower()
        check(f"    {label} states all four canonicality conditions",
              "all **four**" in low or "four** conditions" in low or "all four" in low)
        check(f"    {label} does not claim superseded fails its historical review",
              not ("superseded" in low and "fails condition 1" in low))
    check("    markdown keeps status location-neutral for the provenance labels",
          "location-neutral" in md.lower())
    check("    index keeps status location-neutral for the provenance labels",
          "location-neutral" in idx.lower())
    check("    markdown names SUPERSEDED a tombstone",
          "tombstone" in md.lower())

    # ── the index must not erase locked decisions ─────────────────────────
    print("  -- index preserves locked decisions --")
    ilow = idx.lower()
    check("22. index does not claim future subject matter is undecided",
          "assumed decided" not in ilow)
    check("    index states the future contracts do not yet exist",
          "not yet created" in ilow or "do not yet exist" in ilow)
    check("    index points at the decision coverage matrix",
          "decision_coverage_matrix" in ilow)
    check("    index requires locked decisions to be preserved",
          "locked" in ilow and "preserved" in ilow)
    check("    index states only unrecorded questions remain open",
          "remain open" in ilow or "remains open" in ilow)

    # ── no orphan contract outside the 00-08 sequence ─────────────────────
    print("  -- spend authority routes to a real contract --")
    blob = json.dumps(c, ensure_ascii=False) + md + idx + matrix
    check("23. no reference to an undefined 'Campaign Execution contract' remains",
          "campaign execution contract" not in blob.lower())
    spend = c.get("spendAuthorityOwner", {})
    check("    spend authority is owned by contract 06",
          spend.get("targetContract") == "06" and
          spend.get("targetContractId") == "PINK_MALL_AUTOMATION_AND_APPROVAL_CONTRACT",
          str(spend.get("targetContract")))
    check("    contract 06 exists in the planned sequence",
          any(p.get("contractNumber") == "06" and
              p.get("contractId") == "PINK_MALL_AUTOMATION_AND_APPROVAL_CONTRACT"
              for p in pc))
    paid = next((d for d in domains if d["domainId"] == "PAID_GENERATION_AUTHORITY"), {})
    check("    the paid-generation domain points at contract 06",
          "06" in paid.get("note", "") and "Automation" in paid.get("note", ""))

    # ── locked interview decisions must survive in the matrix ─────────────
    # Wording-tolerant: each anchor is a set of alternative phrasings, and the
    # check passes if any one of them appears. The point is that the decision
    # was preserved, not that a particular sentence was.
    print("  -- locked decisions preserved in the coverage matrix --")
    mlow = matrix.lower()
    ANCHORS = [
        ("three competing ideas",      ["three competing", "3 competing", "next 3 ideas"]),
        ("idea-first campaign context",["idea-first", "idea first", "not product-first"]),
        ("TEAM INA / TEAM SIS",        ["team ina", "team sis"]),
        ("arc lifecycle verbs",        ["continue / evolve / pause / close / revive",
                                        "continue/evolve/pause/close/revive"]),
        ("master station / campaign station", ["master station", "campaign station",
                                               "station per campaign"]),
        ("checkpoint sequence",        ["concept → images", "concept -> images",
                                        "concept / images / video / final"]),
        ("capability-specific autonomy",["capability-specific", "capability specific"]),
        ("campaign memory",            ["campaign memory"]),
        ("durable learning",           ["durable learning"]),
        ("next 3 ideas",               ["next 3 ideas", "next three ideas"]),
        ("experiment lab",             ["experiment lab"]),
        ("world / story map",          ["world / story map", "world/story map", "story map"]),
        ("creative fatigue tracking",  ["fatigue"]),
        ("structured story continuity",["story state", "narrative continuity"]),
        ("budget modes",               ["economy", "standard", "premium"]),
    ]
    missing_anchors = [name for name, alts in ANCHORS if not any(a in mlow for a in alts)]
    check("24. matrix preserves the locked structural decisions",
          not missing_anchors, f"absent={missing_anchors}")
    check("    matrix distinguishes locked-but-uncanonicalized from genuinely open",
          "awaiting canonical contract" in mlow and "genuinely open" in mlow)
    check("    matrix never writes 'undefined' over a locked decision",
          mlow.count("undefined") <= 2 and "never \"undefined\"" in mlow,
          f"{mlow.count('undefined')} occurrences, all in the rule that forbids it")
    check("    matrix defers private detail with the locked phrasing",
          "private detail deferred to private ops layer" in mlow)
    check("    matrix still records zero detailed contracts created",
          "zero" in mlow and "detailed canonical contract" in mlow)

    # ── source registry: complete, exactly-once, and referentially sound ──
    # Authority domains address sources by id, so a missing or duplicated
    # registry entry leaves a domain pointing at nothing, or at two different
    # descriptions of the same system.
    print("  -- source registry --")
    sids = [x.get("sourceId") for x in c.get("sourceTypes", [])]
    reg = c.get("requiredSourceRegistry", {})
    check("26. all required source ids are present",
          REQUIRED_SOURCES <= set(sids), f"missing={sorted(REQUIRED_SOURCES - set(sids))}")
    dup_src = [x for x in REQUIRED_SOURCES if sids.count(x) != 1]
    check("    every required source appears exactly once", not dup_src, f"wrong-count={sorted(dup_src)}")
    check("    no unknown source id appears",
          not (set(sids) - REQUIRED_SOURCES), f"unknown={sorted(set(sids) - REQUIRED_SOURCES)}")
    check("    the contract declares its required source registry",
          set(reg.get("sourceIds", [])) == REQUIRED_SOURCES,
          f"declared={len(reg.get('sourceIds', []))}")

    declared = set(sids)
    dangling = []
    for d in domains:
        for field in ("primaryAuthority", "secondaryEvidence", "nonAuthoritative"):
            for ref in d.get(field, []):
                if ref not in declared:
                    dangling.append(f"{d['domainId']}.{field}->{ref}")
    check("27. every authority-domain source reference is declared",
          not dangling, str(dangling[:6]))
    wdangling = [f"{w.get('target')}->{r}" for w in c.get("writeAuthorities", [])
                 for r in w.get("mayWrite", []) if r not in declared]
    check("    every writeAuthorities.mayWrite source is declared", not wdangling, str(wdangling))
    ndangling = [n.get("sourceId") for n in c.get("nonAuthoritativeAssertions", [])
                 if n.get("sourceId") not in declared]
    check("    every nonAuthoritativeAssertions source is declared", not ndangling, str(ndangling))

    st_schema = props.get("sourceTypes", {})
    st_allof = st_schema.get("allOf", [])
    st_cov, st_bad = set(), []
    for rule in st_allof:
        const = rule.get("contains", {}).get("properties", {}).get("sourceId", {}).get("const")
        if const is None:
            st_bad.append(rule)
            continue
        st_cov.add(const)
        if rule.get("minContains") != 1 or rule.get("maxContains") != 1:
            st_bad.append(const)
    check("28. schema requires EACH source id exactly once via allOf/contains",
          st_cov == REQUIRED_SOURCES and not st_bad,
          f"covered={len(st_cov)}/{len(REQUIRED_SOURCES)} "
          f"missing={sorted(REQUIRED_SOURCES - st_cov)} malformed={st_bad}")
    check("    schema does not rely on uniqueItems alone for sources", bool(st_allof))
    check("    schema constrains the status-semantics object",
          bool(props.get("canonicalityRule", {}).get("properties", {})
               .get("statusSemantics", {}).get("required")))
    check("    schema requires all three status definitions",
          {"CANDIDATE", "CANONICAL", "SUPERSEDED"} <= set(
              props.get("canonicalityRule", {}).get("properties", {})
              .get("statusFieldSemantics", {}).get("required", [])))
    check("    schema rejects unknown status values",
          props.get("canonicalityRule", {}).get("properties", {})
          .get("statusFieldSemantics", {}).get("additionalProperties") is False)
    check("    schema requires at least four canonicality conditions",
          props.get("canonicalityRule", {}).get("properties", {})
          .get("conditions", {}).get("minItems") == 4)

    # ── the contract itself must contain each domain exactly once ─────────
    once = [d for d in REQUIRED_DOMAINS if ids.count(d) != 1]
    check("25. every required domain appears exactly once in the contract",
          not once, f"wrong-count={sorted(once)}")

    print(f"\n{len(domains)} authority domains, {len(c.get('sourceTypes', []))} source types, "
          f"{len(c.get('hardStops', []))} hard stops")
    print(f"SYSTEM AUTHORITY CONTRACT: {'PASS' if not failed else 'FAIL'} "
          f"({passed} passed, {failed} failed)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
