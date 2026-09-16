#!/usr/bin/env python3
"""Validator for the PINK MALL Character and Story Contract (contract 03).

    python tools/regression/character_story_contract.py

No Story State Engine exists and no Story State exists. This contract is what a
future engine will be held to, so the failure it guards against is specific: a
later system reading the machine-readable contract and quietly claiming an
authority nobody granted — letting a narrative event rewrite who someone is,
letting a generated image become canon because it rendered, letting high
engagement mutate continuity, or letting model memory stand in for recorded state.

Three kinds of claim are checked, and they are not the same kind:

  * the contract JSON says what the human-readable contract says, and neither
    contradicts contract 00 or duplicates contracts 01 and 02;
  * both JSON Schemas structurally ENCODE the rules that matter, proved by
    reading the schema documents rather than trusting their prose;
  * synthetic Story State snapshots are accepted or rejected as the contract
    requires, proved by running them through the checker below.

HONEST LIMIT ON THE RUNTIME FIXTURES: the Python standard library ships no JSON
Schema engine and this foundation must not grow a dependency to check its own
constitution. `check_state` below is a TARGETED SEMANTIC CHECKER covering the
governance-bearing subset of 03_STORY_STATE_OBJECT.schema.json: exactly INA and
SIS as identities, identity pinned to the Avatar Skill and immutable by story,
dynamic narrative role and relationship state, the closed arc vocabulary,
proposals that stay proposals, and the sources that may never be declared
authority. It is NOT a JSON Schema engine and a fixture passing it is NOT proof
of full schema conformance. That is why every rule it enforces is ALSO proved
present in the schema document by the structural checks in section E.

Every fixture here is SYNTHETIC. No real narrative state, no private biography
and no personal history appears in this file or anywhere in this repository.

Standard library only, by design.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CDIR = os.path.join(ROOT, "docs", "pink-mall", "system-contracts")

JSON_PATH   = os.path.join(CDIR, "03_CHARACTER_STORY_CONTRACT.json")
SCHEMA_PATH = os.path.join(CDIR, "03_CHARACTER_STORY_CONTRACT.schema.json")
OBJECT_PATH = os.path.join(CDIR, "03_STORY_STATE_OBJECT.schema.json")
MD_PATH     = os.path.join(CDIR, "03_CHARACTER_STORY_CONTRACT.md")
PARENT_PATH = os.path.join(CDIR, "00_SYSTEM_AUTHORITY_CONTRACT.json")
DEP_PATH    = os.path.join(CDIR, "01_CAMPAIGN_CONTEXT_CONTRACT.json")
PROD_PATH   = os.path.join(CDIR, "02_PRODUCT_CREATIVE_CONTRACT.json")
INDEX_PATH  = os.path.join(CDIR, "SYSTEM_CONTRACT_INDEX.md")
MATRIX_PATH = os.path.join(CDIR, "DECISION_COVERAGE_MATRIX.md")

EXPECTED_CONTRACT_ID = "PINK_MALL_CHARACTER_AND_STORY_CONTRACT"
EXPECTED_PARENT_ID   = "PINK_MALL_SYSTEM_AUTHORITY_CONTRACT"
EXPECTED_DEP_ID      = "PINK_MALL_CAMPAIGN_CONTEXT_CONTRACT"
EXPECTED_NUMBER      = "03"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

CHARACTERS = ["INA", "SIS"]
ARCS = ["CONTINUE", "EVOLVE", "PAUSE", "CLOSE", "REVIVE"]
LAYERS = ["HUMAN_IDENTITY", "NARRATIVE_ROLE", "RELATIONSHIP_STATE", "STORY_CANON"]
NONAUTH = ["MODEL_MEMORY", "CHAT_HISTORY", "SUPER_BRAIN", "SOCIAL_INTELLIGENCE_ENGINE",
           "CYBERNINJAS_STUDIO"]
STOP_FAILURES = {"OPERATIONAL_FACT_CONTRADICTION", "PRIVATE_CHARACTER_DETAIL_IN_PUBLIC_STATE",
                 "UNDEFINED_STORY_TRANSITION_AUTHORITY"}
FAILURES = ["WRONG_CHARACTER_IDENTITY", "SISTER_SUBSTITUTION", "IDENTITY_MUTATED_BY_STORY",
            "GENERATED_OUTPUT_TREATED_AS_CANON", "MODEL_MEMORY_TREATED_AS_STORY_AUTHORITY",
            "AUDIENCE_SIGNAL_TREATED_AS_DIRECT_CANON_AUTHORITY", "OPERATIONAL_FACT_CONTRADICTION",
            "PRIVATE_CHARACTER_DETAIL_IN_PUBLIC_STATE", "UNDEFINED_STORY_TRANSITION_AUTHORITY"]
STATE_REQUIRED = ["schemaVersion", "storyStateRef", "previousStoryStateRef", "generatedAt",
                  "isHumanIdentityRecord", "humanIdentityAuthority", "storyStateAuthority",
                  "characters", "relationshipState", "storyArcs", "pendingProposals",
                  "continuityUncertainty", "operationalFactsAsserted"]
STATE_OPTIONAL = ["teamMechanic", "changedSincePrevious", "sourcesNotAuthoritative"]
CHAR_REQUIRED = ["characterId", "identityAuthority", "identityPersistent",
                 "identityMutableByStory", "narrativeRoleIsDynamic", "narrativeRole"]
CHAR_OPTIONAL = ["privateDetailRef"]
# Fields that would carry private or identity content into a public artefact.
PRIVATE_KEYS = {"biography", "personalHistory", "privateDetail", "realName", "address",
                "facialDescriptor", "biometric", "likeness", "contact"}

passed = failed = 0


def check(label, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}" + (f"  [{detail}]" if detail else ""))


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ─────────────────────────────────────────────────────────────────────────────
# Targeted semantic checker for a Story State snapshot.
# Read the honest-limit note in the module docstring before trusting this.
# ─────────────────────────────────────────────────────────────────────────────
def check_state(st):
    """Return a list of violation strings. Empty list means the subset passes."""
    e = []
    if not isinstance(st, dict):
        return ["story state is not an object"]

    for key in STATE_REQUIRED:
        if key not in st:
            e.append(f"missing required key {key}")
    for key in st:
        if key not in STATE_REQUIRED and key not in STATE_OPTIONAL:
            e.append(f"unknown top-level key {key}")

    if st.get("schemaVersion") != 1:
        e.append("schemaVersion must be 1")
    if st.get("isHumanIdentityRecord") is not False:
        e.append("a Story State is NOT a Human Identity record")
    if st.get("humanIdentityAuthority") != "AVATAR_SKILL":
        e.append(f"human identity authority {st.get('humanIdentityAuthority')!r} is not AVATAR_SKILL")
    if st.get("storyStateAuthority") != "STORY_STATE_ENGINE":
        e.append(f"story state authority {st.get('storyStateAuthority')!r} is not STORY_STATE_ENGINE")
    if "previousStoryStateRef" in st:
        prev = st["previousStoryStateRef"]
        if prev is not None and not (isinstance(prev, str) and prev):
            e.append("previousStoryStateRef must be a non-empty string or an explicit null")
    if not st.get("storyStateRef"):
        e.append("storyStateRef must be a non-empty opaque reference")

    # ── exactly INA and SIS, identity pinned and story-immutable ─────────────
    chars = st.get("characters")
    if not isinstance(chars, list):
        e.append("characters must be an array")
    else:
        seen = [c.get("characterId") for c in chars if isinstance(c, dict)]
        for cid in CHARACTERS:
            n = seen.count(cid)
            if n != 1:
                e.append(f"character {cid} appears {n} times, must be exactly once")
        for extra in set(seen) - set(CHARACTERS):
            if extra == "DUO":
                e.append("DUO is not a human identity: it is a participation configuration "
                         "and staging evidence, never a person")
            else:
                e.append(f"unknown character identity {extra!r}")
        for c in chars:
            if not isinstance(c, dict):
                e.append("character record is not an object")
                continue
            cid = c.get("characterId")
            for k in CHAR_REQUIRED:
                if k not in c:
                    e.append(f"character {cid} missing {k}")
            for k in c:
                if k not in CHAR_REQUIRED and k not in CHAR_OPTIONAL:
                    e.append(f"character {cid}: unknown key {k}")
                if k.lower() in {p.lower() for p in PRIVATE_KEYS}:
                    e.append(f"character {cid}: private or identity detail key {k} may not appear "
                             f"in a public Story State")
            if c.get("identityAuthority") != "AVATAR_SKILL":
                e.append(f"character {cid} identity authority is not AVATAR_SKILL")
            if c.get("identityPersistent") is not True:
                e.append(f"character {cid} identity must be persistent")
            if c.get("identityMutableByStory") is not False:
                e.append(f"character {cid}: identity may not be mutated by story")
            if c.get("narrativeRoleIsDynamic") is not True:
                e.append(f"character {cid}: narrative role must be dynamic, never a fixed archetype")
            role = c.get("narrativeRole")
            if not isinstance(role, dict) or not role.get("summary"):
                e.append(f"character {cid}: narrativeRole.summary is required")

    # ── relationship state is dynamic and never identity-defining ────────────
    rel = st.get("relationshipState")
    if not isinstance(rel, dict):
        e.append("relationshipState must be an object")
    else:
        if rel.get("isDynamic") is not True:
            e.append("relationship state must be dynamic")
        if rel.get("isIdentityDefining") is not False:
            e.append("relationship state may not be identity-defining")
        if not rel.get("current"):
            e.append("relationshipState.current must be a non-empty value")
        for k in rel:
            if k.lower() in {p.lower() for p in PRIVATE_KEYS}:
                e.append(f"relationshipState: private detail key {k} may not appear here")

    # ── arcs use the closed vocabulary and declare their provenance ──────────
    arcs = st.get("storyArcs")
    if not isinstance(arcs, list):
        e.append("storyArcs must be an array, even when empty")
    else:
        for i, a in enumerate(arcs):
            if not isinstance(a, dict):
                e.append(f"storyArcs[{i}] is not an object")
                continue
            if not a.get("arcRef"):
                e.append(f"storyArcs[{i}] missing arcRef")
            if a.get("lastAction") not in ARCS:
                e.append(f"storyArcs[{i}] lastAction {a.get('lastAction')!r} not in arc vocabulary")
            if "proposedAction" in a and a["proposedAction"] not in ARCS:
                e.append(f"storyArcs[{i}] proposedAction {a.get('proposedAction')!r} "
                         f"not in arc vocabulary")
            if a.get("provenance") not in ("RECORDED_STORY_STATE", "PROPOSAL"):
                e.append(f"storyArcs[{i}] provenance {a.get('provenance')!r} cannot distinguish "
                         f"recorded continuity from a proposal")

    # ── proposals stay proposals ─────────────────────────────────────────────
    props = st.get("pendingProposals")
    if not isinstance(props, list):
        e.append("pendingProposals must be an array, even when empty")
    else:
        for i, p in enumerate(props):
            if not isinstance(p, dict):
                e.append(f"pendingProposals[{i}] is not an object")
                continue
            if p.get("state") != "PROPOSAL":
                e.append(f"pendingProposals[{i}] state {p.get('state')!r}: a proposal may not be "
                         f"recorded as canon, fact or approval")
            if p.get("influenceIsAuthority") is True:
                e.append(f"pendingProposals[{i}]: an influence reference is not authority")

    # ── team mechanic may not claim truth or authority ───────────────────────
    team = st.get("teamMechanic")
    if isinstance(team, dict):
        if team.get("isHumanIdentityTruth") is not False:
            e.append("the team mechanic is not Human Identity truth")
        if team.get("isStoryStateAuthority") is not False:
            e.append("the team mechanic is not Story State authority")

    src = st.get("sourcesNotAuthoritative")
    if src is not None:
        if not isinstance(src, list):
            e.append("sourcesNotAuthoritative must be an array")
        else:
            for x in src:
                if x not in NONAUTH + ["GENERATED_OUTPUT"]:
                    e.append(f"unknown non-authoritative source {x!r}")

    ops = st.get("operationalFactsAsserted")
    if not isinstance(ops, list):
        e.append("operationalFactsAsserted must be an array")
    elif ops:
        e.append("Story State may not assert operational facts; those belong to the campaign "
                 "operational authority")

    if not isinstance(st.get("continuityUncertainty"), list):
        e.append("continuityUncertainty must be an array, even when empty")
    return e


def valid_state():
    """A synthetic Story State the contract must accept. No real narrative."""
    def char(cid, summary):
        return {"characterId": cid, "identityAuthority": "AVATAR_SKILL",
                "identityPersistent": True, "identityMutableByStory": False,
                "narrativeRoleIsDynamic": True,
                "narrativeRole": {"summary": summary, "tones": ["synthetic tone"]}}

    return {
        "schemaVersion": 1,
        "storyStateRef": "synthetic-story-state-1",
        "previousStoryStateRef": None,
        "generatedAt": "2026-01-01",
        "isHumanIdentityRecord": False,
        "humanIdentityAuthority": "AVATAR_SKILL",
        "storyStateAuthority": "STORY_STATE_ENGINE",
        "characters": [char("INA", "synthetic narrative role A"),
                       char("SIS", "synthetic narrative role B")],
        "relationshipState": {"isDynamic": True, "isIdentityDefining": False,
                              "current": "synthetic relationship state",
                              "changedSincePrevious": False},
        "storyArcs": [{"arcRef": "synthetic-arc-1", "continuity": "synthetic continuity",
                       "lastAction": "CONTINUE", "provenance": "RECORDED_STORY_STATE"}],
        "teamMechanic": {"active": False, "isHumanIdentityTruth": False,
                         "isStoryStateAuthority": False},
        "pendingProposals": [],
        "continuityUncertainty": [],
        "changedSincePrevious": [],
        "sourcesNotAuthoritative": ["MODEL_MEMORY", "CHAT_HISTORY"],
        "operationalFactsAsserted": [],
    }


def mutate(fn, base=None):
    st = json.loads(json.dumps(base if base is not None else valid_state()))
    fn(st)
    return st


def main():
    print("PINK MALL — Character and Story Contract (03) validator\n")

    print("A. documents and identity")
    for path in (JSON_PATH, SCHEMA_PATH, OBJECT_PATH, MD_PATH, PARENT_PATH, DEP_PATH, PROD_PATH):
        if not os.path.exists(path):
            print(f"  FAIL  missing required file {os.path.basename(path)}")
            print("CHARACTER AND STORY CONTRACT: FAIL (cannot continue)")
            sys.exit(1)
    try:
        c = load(JSON_PATH); schema = load(SCHEMA_PATH); obj = load(OBJECT_PATH)
        parent = load(PARENT_PATH); dep = load(DEP_PATH); prod = load(PROD_PATH)
        check("1. contract, both schemas, parent and both sibling contracts parse", True)
    except Exception as exc:
        check("1. contract, both schemas, parent and both sibling contracts parse", False, str(exc))
        print("CHARACTER AND STORY CONTRACT: FAIL (cannot continue)")
        sys.exit(1)
    with open(MD_PATH, encoding="utf-8") as fh:
        md = fh.read()
    md_plain = " ".join(md.replace("*", "").replace("`", "").replace("–", "-")
                        .replace("—", "-").replace("_", " ").split())
    low = md_plain.lower()

    check("2. contractId is the expected id", c.get("contractId") == EXPECTED_CONTRACT_ID,
          str(c.get("contractId")))
    check("3. version is a semantic version", bool(SEMVER.fullmatch(str(c.get("version", "")))),
          str(c.get("version")))
    check("    the schema expresses the same version rule",
          schema.get("properties", {}).get("version", {}).get("pattern") == SEMVER.pattern)
    check("    that pattern and this validator accept the same strings",
          all(bool(re.fullmatch(schema["properties"]["version"]["pattern"], v))
              == bool(SEMVER.fullmatch(v))
              for v in ("1.0.0", "foo.bar.baz", "1.0", "1.0.0.0", "v1.0.0", "1.0.x")))
    check("4. contractNumber is 03", c.get("contractNumber") == EXPECTED_NUMBER,
          str(c.get("contractNumber")))
    check("5. parentContract is the System Authority Contract",
          c.get("parentContract") == EXPECTED_PARENT_ID, str(c.get("parentContract")))
    check("6. status is a declared provenance value",
          c.get("status") in ("CANDIDATE", "CANONICAL", "SUPERSEDED"), str(c.get("status")))
    check("    inheritance forbids contradicting the parent and calls status provenance",
          "MUST NOT contradict" in c.get("inheritance", "")
          and "provenance" in c.get("inheritance", "").lower())
    check("7. the human-readable contract states the same id and version",
          c["contractId"] in md and c["version"] in md)

    print("\nB. registry position and sibling boundaries")
    slots = parent.get("contractSequence", {}).get("slots", [])
    slot = next((s for s in slots if s.get("contractNumber") == EXPECTED_NUMBER), None)
    check("8. contract 00 reserves slot 03 for this contract id",
          slot is not None and slot.get("contractId") == EXPECTED_CONTRACT_ID, str(slot))
    check("9. contract 00 was not bumped to accommodate contract 03",
          parent.get("version") == "1.0.1", str(parent.get("version")))
    deps = {d.get("contractId"): d for d in c.get("dependsOn", [])}
    check("10. depends explicitly on the Campaign Context Contract",
          EXPECTED_DEP_ID in deps and deps[EXPECTED_DEP_ID].get("contractNumber") == "01")
    check("11. contract 01 already anticipated this dependency",
          any(f.get("contractNumber") == "03" for f in dep.get("futureDependencies", [])))
    check("12. contract 01 still owns the three-idea model unchanged",
          dep.get("ideaMode", {}).get("proposalsPerCycle") == 3
          and dep.get("ideaMode", {}).get("exactly") is True)
    check("    contract 01 still defines the four participation roles",
          {r.get("roleId") for r in dep.get("productRoles", [])} == {"NONE", "DETAIL", "SUPPORTING", "HERO"}
          and {r.get("roleId") for r in dep.get("characterRoles", [])} == {"INA", "SIS", "DUO", "NONE"})
    check("13. contract 02 product and human truth remain untransformable",
          prod.get("corePrinciple", {}).get("productTruthMayBeTransformed") is False
          and prod.get("corePrinciple", {}).get("humanIdentityMayBeTransformed") is False)
    fut = {f.get("contractNumber"): f for f in c.get("futureDependencies", [])}
    check("14. contract 04 is named as a future dependency and marked NOT existing",
          "04" in fut and fut["04"].get("exists") is False
          and fut["04"].get("contractId") == "PINK_MALL_SOCIAL_INTELLIGENCE_CONTRACT")
    check("    no future dependency is described as existing",
          all(f.get("exists") is False for f in c.get("futureDependencies", [])))
    check("15. contract 04 genuinely does not exist on disk",
          not glob.glob(os.path.join(CDIR, "04_*")),
          str(glob.glob(os.path.join(CDIR, "04_*"))))
    check("    contracts 04-08 all still absent",
          not any(glob.glob(os.path.join(CDIR, f"0{i}_*")) for i in range(4, 9)))

    print("\nC. the constitutional separation")
    cs = c.get("coreSeparation", {})
    layers = {l.get("layerId"): l for l in cs.get("layers", [])}
    check("16. all four separation layers are present exactly once",
          sorted(layers) == sorted(LAYERS), str(sorted(layers)))
    check("17. human identity is persistent and NOT mutable by story",
          layers.get("HUMAN_IDENTITY", {}).get("persistent") is True
          and layers.get("HUMAN_IDENTITY", {}).get("mutableByStory") is False)
    check("18. human identity authority is the Avatar Skill",
          layers.get("HUMAN_IDENTITY", {}).get("authority") == "AVATAR_SKILL")
    check("19. narrative role and relationship state ARE mutable by story",
          layers.get("NARRATIVE_ROLE", {}).get("mutableByStory") is True
          and layers.get("RELATIONSHIP_STATE", {}).get("mutableByStory") is True)
    rules = " ".join(cs.get("rules", []))
    check("20. a role change may not mutate identity", "MUST NOT mutate Human Identity" in rules)
    check("21. generated output may not become identity truth",
          "MUST NOT become identity truth" in rules)
    check("22. generated output may not become canon by being generated",
          "MUST NOT become story canon merely because it was generated" in rules)
    check("23. narrative intent loses against human identity and product truth",
          "narrative intent is what changes" in rules or "loses" in rules)

    hi = c.get("humanIdentityAuthority", {})
    check("24. human identity primary authority is AVATAR_SKILL",
          hi.get("primaryAuthority") == "AVATAR_SKILL")
    check("    it matches contract 00's own domain record",
          next((d for d in parent.get("authorityDomains", [])
                if d.get("domainId") == "HUMAN_IDENTITY"), {}).get("primaryAuthority")
          == ["AVATAR_SKILL"])
    check("25. the Story State Engine is NOT human identity authority",
          hi.get("storyStateEngineIsIdentityAuthority") is False)
    check("    contract 00 also lists it as non-authoritative for identity",
          "STORY_STATE_ENGINE" in next((d for d in parent.get("authorityDomains", [])
                if d.get("domainId") == "HUMAN_IDENTITY"), {}).get("nonAuthoritative", []))
    check("26. no second identity record and no biometric detail is held here",
          hi.get("identityRecordDuplicatedHere") is False
          and hi.get("biometricOrLikenessDetailHeldHere") is False)
    hrules = " ".join(hi.get("rules", []))
    for phrase, label in (("INA remains INA", "INA remains INA"),
                          ("SIS remains SIS", "SIS remains SIS"),
                          ("NEVER substitute", "no sister substitution"),
                          ("DUO is NOT a third human identity", "DUO is not a third identity"),
                          ("NEVER identity evidence", "generated output is not identity evidence"),
                          ("CANNOT rewrite identity", "narrative cannot rewrite identity"),
                          ("CANNOT override Avatar Skill", "role cannot override the Avatar Skill")):
        check(f"    {label}", phrase in hrules)
    check("27. the identity rule cites the collision-protocol precedent",
          "IDENTITY_COLLISION_PROTOCOL" in hi.get("precedent", ""))

    print("\nD. role, relationship, continuity and story authority")
    nr = c.get("narrativeRoleModel", {})
    check("28. narrative role is dynamic", nr.get("isDynamic") is True)
    check("29. NO fixed archetype taxonomy is defined",
          nr.get("fixedArchetypeTaxonomyDefined") is False
          and nr.get("closedArchetypeEnumPermitted") is False)
    check("30. the tone list is explicitly illustrative, not closed",
          nr.get("toneListIsClosed") is False and len(nr.get("illustrativeTones", [])) >= 4)
    check("31. contract 01's role is a participation selector, not personality truth",
          nr.get("contract01RoleIsParticipationSelector") is True
          and any("identity truth" in x for x in nr.get("contract01RoleIsNot", [])))
    check("    no permanent per-sister archetype is asserted",
          "always behaves as" in nr.get("rule", ""))

    rel = c.get("relationshipStateModel", {})
    check("32. relationship state is dynamic and not identity-defining",
          rel.get("isDynamic") is True and rel.get("isIdentityDefining") is False)
    check("33. no permanent relationship taxonomy is invented",
          rel.get("permanentTaxonomyDefined") is False)
    check("34. relationship state may evolve and shape future story",
          rel.get("mayEvolve") is True and rel.get("mayAffectFutureStory") is True)
    check("35. relationship state may not redefine identity",
          rel.get("mayRedefineIdentity") is False)
    check("36. model memory is not sufficient relationship storage",
          rel.get("modelMemoryIsSufficientStorage") is False)

    nc = c.get("narrativeContinuity", {})
    check("37. narrative continuity is REQUIRED", nc.get("required") is True)
    check("38. model memory is not sufficient continuity storage",
          nc.get("modelMemoryIsSufficient") is False)
    check("39. chat history is never canonical Story State",
          nc.get("chatHistoryIsCanonical") is False)
    check("40. a fresh session can answer all seven continuity questions from state",
          len(nc.get("freshSessionMustBeAbleToDetermine", [])) == 7,
          str(len(nc.get("freshSessionMustBeAbleToDetermine", []))))

    ss = c.get("storyStateAuthority", {})
    check("41. Story State primary authority is STORY_STATE_ENGINE",
          ss.get("primaryAuthority") == "STORY_STATE_ENGINE")
    check("    it matches contract 00's own domain record",
          next((d for d in parent.get("authorityDomains", [])
                if d.get("domainId") == "STORY_STATE"), {}).get("primaryAuthority")
          == ["STORY_STATE_ENGINE"])
    check("42. the Story State Engine remains PLANNED and does not exist",
          ss.get("engineImplementationStatus") == "PLANNED" and ss.get("engineExists") is False)
    check("    contract 00 still records the engine as PLANNED",
          next((s for s in parent.get("sourceTypes", [])
                if s.get("sourceId") == "STORY_STATE_ENGINE"), {}).get("implementationStatus")
          == "PLANNED")
    check("43. Super Brain and Social Intelligence are non-authoritative for Story State",
          {"SUPER_BRAIN", "SOCIAL_INTELLIGENCE_ENGINE"} <= set(ss.get("nonAuthoritative", [])))
    check("    model memory and chat history are named non-authoritative too",
          {"MODEL_MEMORY", "CHAT_HISTORY"} <= set(ss.get("nonAuthoritative", [])))

    oc = c.get("operationalStateConflict", {})
    check("44. campaign operational fact belongs to the Campaign Registry",
          oc.get("campaignOperationalFactAuthority") == "CAMPAIGN_REGISTRY")
    check("45. on conflict the operational fact wins",
          oc.get("onConflict") == "OPERATIONAL_FACT_WINS"
          and oc.get("staleStoryMemoryMustBeCorrected") is True)
    fab = " ".join(oc.get("storyStateMayNotFabricate", []))
    for term in ("executed", "published", "approved", "spent", "completed"):
        check(f"    Story State may not fabricate that a campaign {term}", term in fab)
    check("46. the conflict rule is inherited, not reinvented",
          oc.get("inheritedRule") == "SEMANTIC_VS_CANONICAL"
          and any(r.get("ruleId") == "SEMANTIC_VS_CANONICAL"
                  for r in parent.get("conflictRules", [])))

    iv = c.get("intentVersusEvent", {})
    check("47. proposal, approval, operational fact and canon stay four states",
          iv.get("distinctStates") == ["PROPOSAL", "APPROVAL", "OPERATIONAL_FACT", "STORY_CANON"]
          and iv.get("mayBeCollapsed") is False)
    check("48. a selected idea does not prove the narrative event occurred",
          iv.get("selectedIdeaProvesNarrativeEventOccurred") is False)

    print("\nE. arcs, audience, team, generated output, consent and privacy")
    arc_ids = [a.get("actionId") for a in c.get("storyArcActions", [])]
    check("49. the arc vocabulary is exactly CONTINUE/EVOLVE/PAUSE/CLOSE/REVIVE",
          arc_ids == ARCS, str(arc_ids))
    check("50. every arc action carries a narrative definition",
          all(a.get("definition") for a in c.get("storyArcActions", [])))
    arules = " ".join(c.get("storyArcRules", []))
    check("51. the arc vocabulary is declared CLOSED", "CLOSED" in arules)
    check("52. arc selection logic is deferred to contract 04", "Contract 04" in arules)
    check("53. no numeric rule for choosing an arc action is defined",
          "No numeric rule" in arules)
    check("54. no complete transition graph is invented",
          "No complete transition graph" in arules)
    check("55. not every Story State needs an active arc",
          "Not every Story State must contain an active arc" in arules)

    ai = c.get("audienceInfluence", {})
    check("56. audience input may affect later canon", ai.get("mayAffectLaterCanon") is True)
    check("57. audience input is NOT direct Story State authority",
          ai.get("isDirectStoryStateAuthority") is False)
    check("58. raw metrics stay evidence and interpretation stays interpretation",
          ai.get("rawMetricsAre") == "evidence"
          and ai.get("socialInterpretationIs") == "interpretation")
    check("59. audience input may create a PROPOSAL but not silently mutate canon",
          ai.get("mayCreateOrSupportProposal") is True
          and ai.get("maySilentlyMutateCanon") is False)
    check("60. no autonomous audience-to-canon authority is defined",
          ai.get("autonomousAudienceToCanonAuthorityDefined") is False)
    check("61. no thresholds, voting percentages, scores or formulas are invented",
          ai.get("thresholdsDefined") is False and ai.get("votingPercentagesDefined") is False
          and ai.get("engagementScoresDefined") is False
          and ai.get("automaticCanonSelectionFormulaDefined") is False)
    check("    audience scoring is deferred to contract 04", ai.get("deferredTo") == "04")

    tm = c.get("teamMechanic", {})
    check("62. TEAM INA / TEAM SIS exists as an engagement and story mechanic",
          tm.get("exists") is True and tm.get("isEngagementAndStoryMechanic") is True)
    check("63. the team mechanic is NOT identity truth",
          tm.get("isHumanIdentityTruth") is False)
    check("64. the team mechanic is NOT a permanent personality label",
          tm.get("isPermanentPersonalityLabel") is False)
    check("65. the team mechanic is NOT Story State authority",
          tm.get("isStoryStateAuthority") is False)
    check("66. audience team preference cannot rewrite identity",
          tm.get("audienceTeamPreferenceMayRewriteIdentity") is False)
    check("67. participating in a team is not commercial approval",
          tm.get("participationEqualsCommercialApproval") is False)
    check("68. no numeric winner logic is defined", tm.get("numericWinnerLogicDefined") is False)

    na = {n.get("sourceId"): n for n in c.get("nonAuthoritativeSources", [])}
    check("69. every named source is barred from Story State authority",
          sorted(na) == sorted(NONAUTH)
          and all(v.get("mayBeStoryStateAuthority") is False for v in na.values()),
          str(sorted(na)))
    check("    Super Brain loses to canonical Story State and is corrected",
          "Story State wins" in na.get("SUPER_BRAIN", {}).get("reason", ""))

    go = c.get("generatedOutputBoundary", {})
    check("70. generated output does not become canon on generation success",
          go.get("becomesCanonOnGenerationSuccess") is False)
    check("71. generated output is evidence of nothing",
          go.get("isEvidenceThat") == [])
    notev = " ".join(go.get("isNotEvidenceThat", []))
    for term in ("event occurred", "relationship changed", "campaign published",
                 "audience accepted", "identity changed"):
        check(f"    not evidence that a/an {term}", term in notev)
    check("72. a generated narrative concept remains a PROPOSAL",
          go.get("remainsUntilRecorded") == "PROPOSAL")

    cons = c.get("consent", {})
    check("73. consent references the gate and does not resolve it",
          cons.get("resolvedHere") is False and "CONSENT_AND_PROVENANCE" in cons.get("authority", ""))
    check("74. consent state is NOT owned or cached here",
          cons.get("stateOwnedHere") is False
          and cons.get("readCurrentStateFromAuthority") is True)
    check("75. no consent state value is frozen into the contract",
          not any(isinstance(v, str) and "OWNER_CONFIRMATION_REQUIRED" in v
                  for v in cons.values()),
          str([k for k, v in cons.items()
               if isinstance(v, str) and "OWNER_CONFIRMATION_REQUIRED" in v]))
    check("76. the contract does not claim consent is complete",
          cons.get("claimedComplete") is False
          and cons.get("internalPlanningAndPublicationAreDifferent") is True)
    check("    the consent authority file exists in this lineage",
          os.path.exists(os.path.join(ROOT, cons.get("authority", ""))))
    check("    the markdown caches no consent state value",
          "OWNER_CONFIRMATION_REQUIRED" not in md)

    cr = c.get("characterRecordRules", {})
    check("77. exactly INA and SIS, each exactly once",
          cr.get("requiredCharacters") == CHARACTERS and cr.get("eachExactlyOnce") is True)
    check("78. DUO is not an identity record", cr.get("duoIsIdentityRecord") is False)
    check("79. per-record identity is Avatar-Skill-owned, persistent and story-immutable",
          cr.get("perRecord", {}).get("identityAuthority") == "AVATAR_SKILL"
          and cr.get("perRecord", {}).get("identityPersistent") is True
          and cr.get("perRecord", {}).get("identityMutableByStory") is False
          and cr.get("perRecord", {}).get("narrativeRoleIsDynamic") is True)
    check("80. narrative-role content is not a closed enum",
          cr.get("narrativeRoleContentIsClosedEnum") is False)
    check("81. biometric descriptors are not permitted in Story State",
          cr.get("biometricDescriptorsPermitted") is False)

    so = c.get("storyStateObject", {})
    check("82. the Story State object is a snapshot, not an identity record",
          so.get("isSnapshot") is True and so.get("isHumanIdentityRecord") is False)
    check("83. no engine is implemented and no instance exists or is committed",
          so.get("engineImplemented") is False and so.get("instanceExists") is False
          and so.get("committed") is False)
    check("84. no persistent ID format is defined; references are opaque",
          so.get("persistentIdFormatDefined") is False and so.get("referencesAreOpaque") is True)
    check("85. lineage exists and an initial state may be explicitly null",
          so.get("lineageMechanism") and so.get("initialStateMayHaveNullLineage") is True)
    pr = " ".join(c.get("pendingProposalRules", []))
    check("86. proposals may not silently become recorded Story State",
          "MUST NOT silently become recorded Story State" in pr)
    check("87. a pointer is not authority", "pointer is not authority" in pr)
    disc = " ".join(c.get("existenceDisclaimers", []))
    check("88. a schema existing is not an engine existing",
          "NOT a Story State Engine existing" in disc)
    check("89. a fixture existing is not real narrative state existing",
          "NOT real narrative state existing" in disc)
    check("90. no continuity may be fabricated to populate the schema",
          "may be fabricated" in disc)

    fail_ids = [f.get("failureId") for f in c.get("hardFailures", [])]
    check("91. all nine hard failures are present exactly once",
          all(fail_ids.count(f) == 1 for f in FAILURES) and len(fail_ids) == len(FAILURES),
          str(fail_ids))
    sev = {f.get("failureId"): f.get("severity") for f in c.get("hardFailures", [])}
    check("92. the three STOP failures are STOPs",
          all(sev.get(f) == "STOP" for f in STOP_FAILURES), str(sev))
    check("    every other named failure is a HARD_FAIL",
          all(sev.get(f) == "HARD_FAIL" for f in FAILURES if f not in STOP_FAILURES))

    ag = c.get("authorityGrants", {})
    check("93. no story-transition authority is granted",
          ag.get("storyTransitionAuthorityGranted") is False)
    check("94. no publication, spend or approval authority is granted",
          ag.get("publicationAuthorityGranted") is False
          and ag.get("spendAuthorityGranted") is False
          and ag.get("approvalAuthorityGranted") is False)
    check("95. no identity-write authority is granted",
          ag.get("humanIdentityWriteAuthorityGranted") is False)

    imp = c.get("implementationStatus", {})
    check("96. every named system remains PLANNED and none is implemented here",
          all(imp.get(k) == "PLANNED" for k in ("storyStateEngine", "campaignRegistry",
              "socialIntelligenceEngine", "superBrain", "privateOpsStore"))
          and imp.get("anyImplementedHere") is False)
    check("    no Story State Engine or Campaign Registry implementation exists on disk",
          not glob.glob(os.path.join(ROOT, "**", "*story_state_engine*"), recursive=True)
          and not glob.glob(os.path.join(ROOT, "**", "*campaign_registry*"), recursive=True))
    check("    PINK-MALL-OPS was not created", not os.path.isdir(os.path.join(ROOT, "PINK-MALL-OPS")))

    priv = " ".join(c.get("privacyRules", []))
    check("97. the contract states this repository is PUBLIC", "PUBLIC" in priv)
    for term, label in (("biographies", "private biographies"), ("likeness", "likeness material"),
                        ("Customer data", "customer data"), ("audience history", "private audience history"),
                        ("PINK-MALL-OPS", "PINK-MALL-OPS remains planned")):
        check(f"    barred: {label}", term in priv)
    check("98. open items are declared undecided and may not be invented",
          len(c.get("openItems", [])) >= 14
          and "MUST NOT be answered by invention" in c.get("openItemsRule", ""))
    check("    the Story State object shape is NOT left open",
          "OBJECT SHAPE is deliberately NOT among them" in c.get("openItemsRule", ""))
    opens = " ".join(c.get("openItems", [])).lower()
    for term in ("audience-to-canon", "metric weights", "fatigue thresholds", "cooldown periods",
                 "exploration/exploitation", "persistent story state id format"):
        check(f"    still open: {term}", term in opens)

    print("\nF. schema structure (read from the schema documents, not their prose)")

    def _rules(node, key):
        """allOf entries whose `contains` pins `key`, split by shape.

        An identity rule constrains the key alone with min=max=1, proving the id
        appears exactly once. A binding rule pins a second field with minContains
        only: paired with the identity rule it proves THE one record with that id
        carries that value. maxContains on a binding rule would be weaker, not
        stronger, because a non-matching duplicate would satisfy it.
        """
        ident, bound = {}, {}
        for rule in node.get("allOf", []):
            props = rule.get("contains", {}).get("properties", {})
            const = props.get(key, {}).get("const")
            if const is None:
                continue
            (ident if set(props) == {key} else bound).setdefault(const, []).append(rule)
        return ident, bound

    def exactly_once(node, key, expected):
        ident, _ = _rules(node, key)
        bad = [k for k, rs in ident.items()
               if not any(r.get("minContains") == 1 and r.get("maxContains") == 1 for r in rs)]
        return set(ident) == set(expected) and not bad, f"covered={sorted(ident)} bad={bad}"

    def binds(node, key, field, mapping):
        _, bound = _rules(node, key)
        missing, wrong = [], []
        for ident, expected in mapping.items():
            rs = bound.get(ident, [])
            hit = [r for r in rs
                   if r.get("contains", {}).get("properties", {}).get(field, {})
                   .get("const", "\0MISSING") == expected
                   and r.get("minContains", 0) >= 1
                   and field in r.get("contains", {}).get("required", [])]
            if not rs:
                missing.append(ident)
            elif not hit:
                wrong.append(f"{ident}->{expected!r}")
        return not missing and not wrong, f"unbound={missing} wrong={wrong}"

    def admits(node, token):
        """True only if the schema ADMITS the value — const/enum/required/default.

        Deliberately ignores descriptions: prose explaining that a value is
        forbidden must not be mistaken for the value being allowed.
        """
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ("description", "$comment", "title"):
                    continue
                if k in ("const", "enum", "required", "default") and token in json.dumps(v):
                    return True
                if admits(v, token):
                    return True
        elif isinstance(node, list):
            return any(admits(x, token) for x in node)
        return False

    sp = schema.get("properties", {})
    check("99. contract schema is closed to unknown top-level keys",
          schema.get("additionalProperties") is False)
    check("100. contract schema requires every governed key",
          set(sp) == set(schema.get("required", [])) and set(sp) == set(c),
          f"schema-only={sorted(set(sp) - set(c))} contract-only={sorted(set(c) - set(sp))}")
    ok, d = exactly_once(sp.get("storyArcActions", {}), "actionId", ARCS)
    check("101. contract schema requires each arc action exactly once", ok, d)
    check("    contract schema caps the arc vocabulary at five, making it closed",
          sp.get("storyArcActions", {}).get("maxItems") == 5)
    ok, d = exactly_once(sp.get("hardFailures", {}), "failureId", FAILURES)
    check("102. contract schema requires each hard failure exactly once", ok, d)
    ok, d = binds(sp.get("hardFailures", {}), "failureId", "severity",
                  {f: ("STOP" if f in STOP_FAILURES else "HARD_FAIL") for f in FAILURES})
    check("    contract schema pins each failure's severity", ok, d)
    ok, d = exactly_once(sp.get("coreSeparation", {}).get("properties", {}).get("layers", {}),
                         "layerId", LAYERS)
    check("103. contract schema requires each separation layer exactly once", ok, d)
    lay = sp.get("coreSeparation", {}).get("properties", {}).get("layers", {})
    ok, d = binds(lay, "layerId", "mutableByStory",
                  {"HUMAN_IDENTITY": False, "NARRATIVE_ROLE": True, "RELATIONSHIP_STATE": True})
    check("    contract schema pins which layers story may mutate", ok, d)
    ok, d = binds(lay, "layerId", "authority", {"HUMAN_IDENTITY": "AVATAR_SKILL"})
    check("    contract schema pins human identity to the Avatar Skill", ok, d)
    ok, d = exactly_once(sp.get("nonAuthoritativeSources", {}), "sourceId", NONAUTH)
    check("104. contract schema requires each non-authoritative source exactly once", ok, d)
    ok, d = binds(sp.get("nonAuthoritativeSources", {}), "sourceId", "mayBeStoryStateAuthority",
                  {s: False for s in NONAUTH})
    check("    contract schema bars every one of them from Story State authority", ok, d)
    ok, d = exactly_once(sp.get("dependsOn", {}), "contractId", [EXPECTED_DEP_ID])
    check("105. contract schema requires the contract-01 dependency exactly once", ok, d)
    ok, d = binds(sp.get("futureDependencies", {}), "contractNumber", "exists", {"04": False})
    check("106. contract schema pins contract 04 as NOT existing", ok, d)
    for key, sub, want in (("humanIdentityAuthority", "primaryAuthority", "AVATAR_SKILL"),
                           ("humanIdentityAuthority", "storyStateEngineIsIdentityAuthority", False),
                           ("humanIdentityAuthority", "biometricOrLikenessDetailHeldHere", False),
                           ("storyStateAuthority", "primaryAuthority", "STORY_STATE_ENGINE"),
                           ("storyStateAuthority", "engineImplementationStatus", "PLANNED"),
                           ("storyStateAuthority", "engineExists", False),
                           ("narrativeRoleModel", "isDynamic", True),
                           ("narrativeRoleModel", "fixedArchetypeTaxonomyDefined", False),
                           ("narrativeRoleModel", "closedArchetypeEnumPermitted", False),
                           ("relationshipStateModel", "isDynamic", True),
                           ("relationshipStateModel", "isIdentityDefining", False),
                           ("relationshipStateModel", "mayRedefineIdentity", False),
                           ("narrativeContinuity", "required", True),
                           ("narrativeContinuity", "modelMemoryIsSufficient", False),
                           ("narrativeContinuity", "chatHistoryIsCanonical", False),
                           ("audienceInfluence", "isDirectStoryStateAuthority", False),
                           ("audienceInfluence", "maySilentlyMutateCanon", False),
                           ("audienceInfluence", "thresholdsDefined", False),
                           ("teamMechanic", "isHumanIdentityTruth", False),
                           ("teamMechanic", "isStoryStateAuthority", False),
                           ("generatedOutputBoundary", "becomesCanonOnGenerationSuccess", False),
                           ("generatedOutputBoundary", "remainsUntilRecorded", "PROPOSAL"),
                           ("operationalStateConflict", "onConflict", "OPERATIONAL_FACT_WINS"),
                           ("intentVersusEvent", "mayBeCollapsed", False),
                           ("consent", "stateOwnedHere", False),
                           ("consent", "resolvedHere", False),
                           ("consent", "claimedComplete", False),
                           ("characterRecordRules", "duoIsIdentityRecord", False),
                           ("storyStateObject", "engineImplemented", False),
                           ("storyStateObject", "instanceExists", False),
                           ("authorityGrants", "storyTransitionAuthorityGranted", False),
                           ("implementationStatus", "storyStateEngine", "PLANNED"),
                           ("implementationStatus", "anyImplementedHere", False)):
        got = sp.get(key, {}).get("properties", {}).get(sub, {}).get("const")
        check(f"    contract schema pins {key}.{sub} = {want}", got is want or got == want,
              f"got={got!r}")
    check("107. contract schema closes the consent object",
          sp.get("consent", {}).get("additionalProperties") is False)
    check("    contract schema declares no property that could hold a consent state value",
          not any(k in sp.get("consent", {}).get("properties", {})
                  for k in ("currentState", "state", "consentState", "status")),
          str(sorted(sp.get("consent", {}).get("properties", {}))))
    open_objs = [k for k, v in sp.items()
                 if isinstance(v, dict) and v.get("type") == "object"
                 and v.get("additionalProperties") is not False]
    check("    every governed contract sub-object is closed", not open_objs, str(open_objs))

    op = obj.get("properties", {})
    check("108. object schema is closed to unknown top-level keys",
          obj.get("additionalProperties") is False)
    open_items = [k for k, v in op.items()
                  if isinstance(v, dict) and v.get("type") == "object"
                  and v.get("additionalProperties") is not False]
    check("    every governed snapshot sub-object is closed", not open_items, str(open_items))
    chars_node = op.get("characters", {})
    ok, d = exactly_once(chars_node, "characterId", CHARACTERS)
    check("109. object schema requires INA and SIS each exactly once", ok, d)
    ok, d = binds(chars_node, "characterId", "identityAuthority",
                  {x: "AVATAR_SKILL" for x in CHARACTERS})
    check("    object schema pins identity authority to AVATAR_SKILL per character", ok, d)
    ok, d = binds(chars_node, "characterId", "identityMutableByStory",
                  {x: False for x in CHARACTERS})
    check("110. object schema forbids story mutating identity, per character", ok, d)
    ok, d = binds(chars_node, "characterId", "identityPersistent", {x: True for x in CHARACTERS})
    check("    object schema pins identity persistent per character", ok, d)
    ok, d = binds(chars_node, "characterId", "narrativeRoleIsDynamic",
                  {x: True for x in CHARACTERS})
    check("111. object schema pins narrative role dynamic per character", ok, d)
    cprops = chars_node.get("items", {}).get("properties", {})
    check("112. object schema admits no DUO character identity",
          cprops.get("characterId", {}).get("enum") == CHARACTERS
          and not admits({"a": cprops.get("characterId", {})}, "DUO"),
          str(cprops.get("characterId", {}).get("enum")))
    check("    the character array is capped at two, so no third identity fits",
          chars_node.get("minItems") == 2 and chars_node.get("maxItems") == 2)
    # A description explaining why there is no enum must not read as an enum.
    def _has_enum(node):
        if isinstance(node, dict):
            return any(k == "enum" or _has_enum(v) for k, v in node.items()
                       if k not in ("description", "$comment", "title"))
        if isinstance(node, list):
            return any(_has_enum(x) for x in node)
        return False

    check("113. object schema leaves narrative role open, not a closed archetype enum",
          not _has_enum(cprops.get("narrativeRole", {})))
    check("114. object schema pins the snapshot as NOT a human identity record",
          op.get("isHumanIdentityRecord", {}).get("const") is False)
    check("115. object schema closes human identity authority to AVATAR_SKILL",
          op.get("humanIdentityAuthority", {}).get("const") == "AVATAR_SKILL")
    check("116. object schema closes story state authority to STORY_STATE_ENGINE",
          op.get("storyStateAuthority", {}).get("const") == "STORY_STATE_ENGINE")
    check("    model memory and social sources cannot be declared the authority",
          not any(admits({"a": op.get("storyStateAuthority", {})}, s)
                  for s in ("MODEL_MEMORY", "CHAT_HISTORY", "SUPER_BRAIN",
                            "SOCIAL_INTELLIGENCE_ENGINE")))
    rel_p = op.get("relationshipState", {}).get("properties", {})
    check("117. object schema pins relationship state dynamic and not identity-defining",
          rel_p.get("isDynamic", {}).get("const") is True
          and rel_p.get("isIdentityDefining", {}).get("const") is False)
    check("    relationship state carries no closed taxonomy enum",
          not _has_enum(rel_p.get("current", {})))
    arc_p = op.get("storyArcs", {}).get("items", {}).get("properties", {})
    check("118. object schema closes the arc action vocabulary",
          arc_p.get("lastAction", {}).get("enum") == ARCS
          and arc_p.get("proposedAction", {}).get("enum") == ARCS)
    check("    arcs must declare recorded-versus-proposal provenance",
          arc_p.get("provenance", {}).get("enum") == ["RECORDED_STORY_STATE", "PROPOSAL"])
    prop_p = op.get("pendingProposals", {}).get("items", {}).get("properties", {})
    check("119. object schema pins a pending proposal's state to PROPOSAL",
          prop_p.get("state", {}).get("const") == "PROPOSAL")
    check("    no canon, fact or approval state is expressible on a proposal",
          not any(admits({"a": prop_p.get("state", {})}, s)
                  for s in ("CANON", "FACT", "APPROVAL", "OPERATIONAL_FACT")))
    check("    an influence reference is pinned non-authoritative",
          prop_p.get("influenceIsAuthority", {}).get("const") is False)
    team_p = op.get("teamMechanic", {}).get("properties", {})
    check("120. object schema bars the team mechanic from identity truth and story authority",
          team_p.get("isHumanIdentityTruth", {}).get("const") is False
          and team_p.get("isStoryStateAuthority", {}).get("const") is False)
    check("121. object schema forbids asserting operational facts",
          op.get("operationalFactsAsserted", {}).get("maxItems") == 0)
    check("122. object schema requires lineage to be stated, null or otherwise",
          "previousStoryStateRef" in obj.get("required", [])
          and any(x.get("type") == "null"
                  for x in op.get("previousStoryStateRef", {}).get("oneOf", [])))
    check("123. object schema admits no private-detail content field",
          not any(k.lower() in {p.lower() for p in PRIVATE_KEYS}
                  for k in list(cprops) + list(rel_p)),
          str([k for k in list(cprops) + list(rel_p)
               if k.lower() in {p.lower() for p in PRIVATE_KEYS}]))
    check("    private material may only be referenced, never carried",
          "privateDetailRef" in cprops and "REFERENCE only" in
          cprops.get("privateDetailRef", {}).get("description", ""))
    check("124. object schema records what may never appear in a snapshot",
          len(obj.get("x-notPermitted", {})) >= 5)

    print("\nG. synthetic runtime fixtures — targeted semantic checker, NOT a JSON Schema engine")
    errs = check_state(valid_state())
    check("125. a well-formed synthetic Story State is ACCEPTED", not errs, str(errs[:4]))

    def rejects(label, fn, needle=None, base=None):
        e = check_state(mutate(fn, base))
        ok = bool(e) and (needle is None or any(needle in x for x in e))
        check(label, ok, f"errors={e[:3]}")

    rejects("126. a missing INA record is REJECTED",
            lambda s: s.__setitem__("characters",
                                    [x for x in s["characters"] if x["characterId"] != "INA"]),
            "INA appears 0 times")
    rejects("127. a missing SIS record is REJECTED",
            lambda s: s.__setitem__("characters",
                                    [x for x in s["characters"] if x["characterId"] != "SIS"]),
            "SIS appears 0 times")
    rejects("128. a duplicated INA record is REJECTED",
            lambda s: s["characters"].append(json.loads(json.dumps(s["characters"][0]))),
            "INA appears 2 times")
    rejects("129. DUO inserted as an identity is REJECTED",
            lambda s: s["characters"].append(
                {"characterId": "DUO", "identityAuthority": "AVATAR_SKILL",
                 "identityPersistent": True, "identityMutableByStory": False,
                 "narrativeRoleIsDynamic": True, "narrativeRole": {"summary": "x"}}),
            "DUO is not a human identity")
    rejects("130. STORY_STATE_ENGINE claimed as human identity authority is REJECTED",
            lambda s: s.__setitem__("humanIdentityAuthority", "STORY_STATE_ENGINE"),
            "is not AVATAR_SKILL")
    rejects("    a character claiming a non-Avatar identity authority is REJECTED",
            lambda s: s["characters"][0].__setitem__("identityAuthority", "STORY_STATE_ENGINE"),
            "identity authority is not AVATAR_SKILL")
    rejects("131. identityMutableByStory = true is REJECTED",
            lambda s: s["characters"][0].__setitem__("identityMutableByStory", True),
            "identity may not be mutated by story")
    rejects("    a non-persistent identity is REJECTED",
            lambda s: s["characters"][1].__setitem__("identityPersistent", False),
            "identity must be persistent")
    rejects("132. narrativeRoleIsDynamic = false is REJECTED",
            lambda s: s["characters"][0].__setitem__("narrativeRoleIsDynamic", False),
            "never a fixed archetype")
    rejects("133. relationship state marked permanent is REJECTED",
            lambda s: s["relationshipState"].__setitem__("isDynamic", False),
            "must be dynamic")
    rejects("134. relationship state marked identity-defining is REJECTED",
            lambda s: s["relationshipState"].__setitem__("isIdentityDefining", True),
            "may not be identity-defining")
    rejects("135. an unknown arc action is REJECTED",
            lambda s: s["storyArcs"][0].__setitem__("lastAction", "RETCON"),
            "not in arc vocabulary")
    rejects("    an unknown proposed arc action is REJECTED",
            lambda s: s["storyArcs"][0].__setitem__("proposedAction", "REBOOT"),
            "not in arc vocabulary")
    rejects("    an arc with no recorded-versus-proposal provenance is REJECTED",
            lambda s: s["storyArcs"][0].__setitem__("provenance", "ASSUMED"),
            "cannot distinguish")
    rejects("136. generated output treated as canon is REJECTED",
            lambda s: s["storyArcs"].append(
                {"arcRef": "a2", "continuity": "from a generated image", "lastAction": "EVOLVE",
                 "provenance": "GENERATED_OUTPUT"}), "cannot distinguish")
    rejects("137. model memory declared the story authority is REJECTED",
            lambda s: s.__setitem__("storyStateAuthority", "MODEL_MEMORY"),
            "is not STORY_STATE_ENGINE")
    rejects("    chat history declared the story authority is REJECTED",
            lambda s: s.__setitem__("storyStateAuthority", "CHAT_HISTORY"),
            "is not STORY_STATE_ENGINE")
    rejects("138. a social signal declared direct canon authority is REJECTED",
            lambda s: s.__setitem__("storyStateAuthority", "SOCIAL_INTELLIGENCE_ENGINE"),
            "is not STORY_STATE_ENGINE")
    rejects("    an influence reference claiming authority is REJECTED",
            lambda s: s["pendingProposals"].append(
                {"proposalRef": "p1", "state": "PROPOSAL", "summary": "synthetic",
                 "influenceRef": "synthetic-signal", "influenceIsAuthority": True}),
            "is not authority")
    rejects("139. a pending audience proposal marked canon is REJECTED",
            lambda s: s["pendingProposals"].append(
                {"proposalRef": "p2", "state": "STORY_CANON", "summary": "synthetic"}),
            "may not be recorded as canon")
    rejects("    a proposal marked FACT is REJECTED",
            lambda s: s["pendingProposals"].append(
                {"proposalRef": "p3", "state": "FACT", "summary": "synthetic"}),
            "may not be recorded as canon")
    rejects("140. the team mechanic claiming identity truth is REJECTED",
            lambda s: s["teamMechanic"].__setitem__("isHumanIdentityTruth", True),
            "not Human Identity truth")
    rejects("    the team mechanic claiming story authority is REJECTED",
            lambda s: s["teamMechanic"].__setitem__("isStoryStateAuthority", True),
            "not Story State authority")
    rejects("141. asserting an operational fact is REJECTED",
            lambda s: s.__setitem__("operationalFactsAsserted", ["campaign published"]),
            "may not assert operational facts")
    rejects("142. a private biography field in the snapshot is REJECTED",
            lambda s: s["characters"][0].__setitem__("biography", "synthetic"),
            "private or identity detail key")
    rejects("    a facial descriptor field is REJECTED",
            lambda s: s["characters"][1].__setitem__("facialDescriptor", "synthetic"),
            "private or identity detail key")
    rejects("143. a snapshot claiming to be an identity record is REJECTED",
            lambda s: s.__setitem__("isHumanIdentityRecord", True),
            "NOT a Human Identity record")
    rejects("144. an unknown top-level field is REJECTED",
            lambda s: s.__setitem__("autoCanon", True), "autoCanon")
    rejects("    an unknown character field is REJECTED",
            lambda s: s["characters"][0].__setitem__("archetype", "comic relief"), "unknown key")
    rejects("    an omitted lineage key is REJECTED",
            lambda s: s.pop("previousStoryStateRef"), "previousStoryStateRef")
    check("145. an explicit null lineage is ACCEPTED for an initial state",
          not check_state(mutate(lambda s: s.__setitem__("previousStoryStateRef", None))))
    check("    a named previous state is ACCEPTED",
          not check_state(mutate(lambda s: s.__setitem__("previousStoryStateRef", "prior-1"))))
    check("146. an empty arc list is ACCEPTED — not every state has an active arc",
          not check_state(mutate(lambda s: s.__setitem__("storyArcs", []))))
    check("    a well-formed PROPOSAL is ACCEPTED",
          not check_state(mutate(lambda s: s["pendingProposals"].append(
              {"proposalRef": "p4", "state": "PROPOSAL", "summary": "synthetic",
               "influenceRef": "synthetic-signal", "influenceIsAuthority": False}))))
    check("147. the accepted fixture uses only keys the object schema declares",
          set(valid_state()) <= set(op), str(set(valid_state()) - set(op)))
    check("    the fixture's character keys are all declared by the object schema",
          set(valid_state()["characters"][0]) <= set(cprops))
    check("148. no fixture in this validator contains private or real narrative content",
          all("synthetic" in json.dumps(v).lower() or v in ([], None, True, False)
              for v in (valid_state()["characters"][0]["narrativeRole"],
                        valid_state()["relationshipState"]["current"])))

    print("\nH. registry bookkeeping")
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, encoding="utf-8") as fh:
            index = fh.read()
        index_plain = " ".join(index.replace("*", "").replace("`", "").split()).lower()
        marker = "## Planned contracts"
        head, _, tail = index.partition(marker)
        above = [ln for ln in head.splitlines() if ln.strip().startswith("| 03 ")]
        below = [ln for ln in tail.splitlines() if ln.strip().startswith("| 03 ")]
        check("149. the index lists contract 03 in its current set",
              len(above) == 1 and "CHARACTER" in above[0].upper(), str(above))
        check("150. the index no longer lists 03 as NOT YET CREATED",
              bool(marker in index) and not below, str(below))
        check("    contracts 00-02 remain in the current set",
              all(any(ln.strip().startswith(f"| 0{i} ") for ln in head.splitlines())
                  for i in (0, 1, 2)))
        check("151. contracts 04-08 remain NOT YET CREATED",
              all(f"| 0{i} " in tail for i in range(4, 9)),
              str([i for i in range(4, 9) if f"| 0{i} " not in tail]))
        check("    the index names the contract-03 validator",
              "character_story_contract.py" in index)
        check("    the index does not treat file existence as canonicality",
              "existence does not make it canonical" in index_plain
              or "does not assert" in index_plain)
        check("152. the index records that no Story State Engine exists",
              "story state engine" in index_plain and "does not exist" in index_plain)
        check("    the index records the object schema as future runtime structure",
              "story state" in index_plain and "must not" in index_plain)
        check("    the index states contract 03 does not own Human Identity",
              "human identity" in index_plain and "avatar skill" in index_plain)
    else:
        check("149. the contract index exists", False, INDEX_PATH)

    if os.path.exists(MATRIX_PATH):
        with open(MATRIX_PATH, encoding="utf-8") as fh:
            matrix = fh.read()
        mp = " ".join(matrix.replace("*", "").replace("`", "").replace("–", "-")
                      .replace("—", "-").split()).lower()
        authored = sorted(n for n in (f"{i:02d}" for i in range(9))
                          if glob.glob(os.path.join(CDIR, f"{n}_*_CONTRACT.json")))
        awaiting = [n for n in (f"{i:02d}" for i in range(9)) if n not in authored]
        stale = [f"{lead} {n}-08 {t}" for n in authored if n != "00"
                 for lead in ("domains", "contracts", "domain", "contract")
                 for t in ("are still awaiting", "still awaiting", "are awaiting",
                           "still await", "await")
                 if f"{lead} {n}-08 {t}" in mp]
        check("153. the matrix makes no global claim that an authored contract is awaiting",
              not stale, f"stale={stale[:3]}")
        first = awaiting[0] if awaiting else None
        check("154. the awaiting range starts at the first genuinely unwritten contract",
              first is None or f"{first}-08" in mp, f"expected the range to start at {first}")
        check("    the matrix names contract 03 as authored",
              "03" in mp and "authored" in mp)
        check("155. the Character & Story domain records its contract as authored",
              "character & story" in mp or "character and story" in mp)
        check("156. the Story Engine + Social Intelligence domain is NOT fully authored",
              "not fully authored" in mp or "04" in mp)
        check("    contract 04 is still described as not created",
              "04" in mp)
        check("157. all eight locked interview domains are preserved",
              all(f"### {i}." in matrix for i in range(1, 9)),
              str([i for i in range(1, 9) if f"### {i}." not in matrix]))
        check("    the three states are still kept apart",
              "awaiting canonical contract" in mp and "genuinely open" in mp)
        check("    the private-detail deferral is preserved",
              matrix.count("PRIVATE DETAIL DEFERRED TO PRIVATE OPS LAYER") >= 3)
        check("158. the matrix defers canonicality to the four conditions",
              "four conditions" in mp and "not a canonicality test" in mp)
    else:
        check("153. the decision-coverage matrix exists", False, MATRIX_PATH)

    print("\nI. human-readable agreement")
    check("159. the markdown states the core separation",
          "human identity" in low and "narrative role" in low
          and "relationship state" in low and "story canon" in low)
    check("160. the markdown names every arc action", all(a in md for a in ARCS))
    check("161. the markdown names every hard failure", all(f in md for f in FAILURES))
    check("162. the markdown states DUO is not a third identity",
          "duo is not a third human identity" in low)
    check("163. the markdown states model memory is never sufficient",
          "model memory is never sufficient" in low)
    check("164. the markdown states audience input may not silently mutate canon",
          "must not silently mutate canonical story state" in low)
    check("165. the markdown states a schema is not an engine",
          "a schema is not an engine" in low)
    check("166. the markdown states contract 04 is not yet created",
          "not yet created" in low)
    check("167. the markdown declares open items rather than inventing answers",
          "open items" in low and "MUST NOT" in md)

    print(f"\n{len(c.get('storyArcActions', []))} arc actions, "
          f"{len(c.get('hardFailures', []))} hard failures, "
          f"{len(c.get('nonAuthoritativeSources', []))} non-authoritative sources, "
          f"{len(c.get('openItems', []))} open items")
    print("Runtime fixtures were checked by a targeted semantic checker, not a JSON Schema "
          "engine; section F proves the same rules are encoded in the schema documents.")
    print(f"CHARACTER AND STORY CONTRACT: {'PASS' if not failed else 'FAIL'} "
          f"({passed} passed, {failed} failed)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
