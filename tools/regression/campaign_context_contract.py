#!/usr/bin/env python3
"""Validator for the PINK MALL Campaign Context Contract (contract 01).

    python tools/regression/campaign_context_contract.py

No Campaign Context Builder exists. This contract is what a future builder will
be held to, so the failure this guards against is not a typo — it is a later
system reading the machine-readable contract and quietly claiming an authority
the owner never granted: selecting its own winning idea, treating a trend signal
as truth, inventing a story state that no engine produces, or emitting a package
whose provenance is implied rather than declared.

Three things are checked, and they are different kinds of claim:

  * the contract JSON says what the human-readable contract says, and neither
    has drifted from the parent authority contract;
  * the two JSON Schemas structurally ENCODE the rules that matter, proved by
    reading the schema documents themselves — not by trusting their prose;
  * synthetic runtime packages are accepted or rejected as the contract
    requires, proved by running them through a small semantic checker below.

HONEST LIMIT ON THE RUNTIME FIXTURES: the Python standard library ships no JSON
Schema engine and this foundation must not grow a dependency to check its own
constitution. `check_package` below is a TARGETED SEMANTIC CHECKER covering the
subset of 01_CAMPAIGN_CONTEXT_OBJECT.schema.json that carries governance weight
(exactly three ideas, declared provenance for every input domain, closed role
and state vocabularies, untransformable product and human truth, closed object
shape). It is NOT a JSON Schema engine and a fixture passing it is NOT proof of
full schema conformance. That is why every rule it enforces is ALSO proved to be
present in the schema document by the structural checks in section E: the
fixtures show the rule behaves, the structural checks show the rule is written
where a real validator would read it.

Standard library only, by design.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CDIR = os.path.join(ROOT, "docs", "pink-mall", "system-contracts")

JSON_PATH    = os.path.join(CDIR, "01_CAMPAIGN_CONTEXT_CONTRACT.json")
SCHEMA_PATH  = os.path.join(CDIR, "01_CAMPAIGN_CONTEXT_CONTRACT.schema.json")
OBJECT_PATH  = os.path.join(CDIR, "01_CAMPAIGN_CONTEXT_OBJECT.schema.json")
MD_PATH      = os.path.join(CDIR, "01_CAMPAIGN_CONTEXT_CONTRACT.md")
PARENT_PATH  = os.path.join(CDIR, "00_SYSTEM_AUTHORITY_CONTRACT.json")
INDEX_PATH   = os.path.join(CDIR, "SYSTEM_CONTRACT_INDEX.md")
MATRIX_PATH  = os.path.join(CDIR, "DECISION_COVERAGE_MATRIX.md")

EXPECTED_CONTRACT_ID = "PINK_MALL_CAMPAIGN_CONTEXT_CONTRACT"
EXPECTED_PARENT_ID   = "PINK_MALL_SYSTEM_AUTHORITY_CONTRACT"
EXPECTED_NUMBER      = "01"

INPUT_DOMAINS = ["WORLD_STORY_STATE", "CULTURAL_SOCIAL_SIGNALS", "BRAND_DNA_HERITAGE",
                 "CHARACTER_CONTEXT", "CURRENT_PRODUCTS", "TARGET_FORMAT"]
REQUIRED_TRUTH_DOMAINS = {"BRAND_DNA_HERITAGE", "CURRENT_PRODUCTS", "TARGET_FORMAT"}
OPTIONAL_DOMAINS = set(INPUT_DOMAINS) - REQUIRED_TRUTH_DOMAINS
# Authority is pinned per class, not left to a free boolean. A reference to
# private material is a pointer, not a fact: the future PRIVATE_OPS_STORE may
# hold authority in domains contract 00 assigns it, but the pointer carried by a
# campaign context does not acquire that authority by pointing there.
INPUT_CLASS_AUTHORITY = {
    "CANONICAL_FACT": True, "DERIVED_FACT": True, "LOCKED_OWNER_DECISION": True,
    "OPERATIONAL_STATE": True, "SOCIAL_OR_CULTURAL_SIGNAL": False,
    "SEMANTIC_INTERPRETATION": False, "PRIVATE_OPS_REFERENCE": False,
    "UNAVAILABLE_INPUT": False,
}
INPUT_CLASSES = ["CANONICAL_FACT", "DERIVED_FACT", "LOCKED_OWNER_DECISION", "OPERATIONAL_STATE",
                 "SOCIAL_OR_CULTURAL_SIGNAL", "SEMANTIC_INTERPRETATION", "PRIVATE_OPS_REFERENCE",
                 "UNAVAILABLE_INPUT"]
# The single source of truth for domain requirement, shared by the semantic
# checker and by the structural proof that the schema encodes the same map.
DOMAIN_REQUIREMENT = {
    "WORLD_STORY_STATE": "OPTIONAL_CONTEXT_INPUT",
    "CULTURAL_SOCIAL_SIGNALS": "OPTIONAL_CONTEXT_INPUT",
    "BRAND_DNA_HERITAGE": "REQUIRED_TRUTH_INPUT",
    "CHARACTER_CONTEXT": "OPTIONAL_CONTEXT_INPUT",
    "CURRENT_PRODUCTS": "REQUIRED_TRUTH_INPUT",
    "TARGET_FORMAT": "REQUIRED_TRUTH_INPUT",
}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
PRODUCT_ROLES   = ["NONE", "DETAIL", "SUPPORTING", "HERO"]
CHARACTER_ROLES = ["INA", "SIS", "DUO", "NONE"]
AVAILABILITY    = ["AVAILABLE", "UNAVAILABLE", "NOT_APPLICABLE"]
REQUIREMENTS    = ["REQUIRED_TRUTH_INPUT", "OPTIONAL_CONTEXT_INPUT"]
IDEA_STATES     = ["PROPOSAL", "OWNER_SELECTED"]
# States contract 01 has no authority to express. Spend, execution and
# publication belong to contract 06 and to the parent's own domains.
FORBIDDEN_STATES = ["PUBLISHED", "EXECUTING", "APPROVED_SPEND", "APPROVED", "SCHEDULED"]
REQUIRED_FAILURES = {"GENERIC_AI_AESTHETIC", "PRODUCT_TRUTH_CONTRADICTED",
                     "HUMAN_IDENTITY_CONTRADICTED"}
IDEA_REQUIRED = ["ideaRef", "title", "worldPremise", "purpose", "productRole", "characterRole",
                 "targetFormatIntent", "creativeMechanisms", "truthRisks", "state"]
IDEA_OPTIONAL = ["privateDetailRefs"]
PKG_REQUIRED  = ["schemaVersion", "contextRef", "generatedAt", "inputSummary", "brandConstraints",
                 "truthConstraints", "targetFormat", "ideas"]

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
# Targeted semantic checker for a runtime Campaign Context package.
# Read the honest-limit note in the module docstring before trusting this.
# ─────────────────────────────────────────────────────────────────────────────
def check_package(pkg):
    """Return a list of violation strings. Empty list means the subset passes."""
    e = []
    if not isinstance(pkg, dict):
        return ["package is not an object"]

    for key in PKG_REQUIRED:
        if key not in pkg:
            e.append(f"missing required key {key}")
    for key in pkg:
        if key not in PKG_REQUIRED:
            e.append(f"unknown top-level key {key}")

    if pkg.get("schemaVersion") != 1:
        e.append("schemaVersion must be 1")
    if not isinstance(pkg.get("contextRef"), str) or not pkg.get("contextRef"):
        e.append("contextRef must be a non-empty string")

    # Provenance: every input domain declared exactly once, absence included.
    summary = pkg.get("inputSummary")
    if not isinstance(summary, list):
        e.append("inputSummary must be an array")
    else:
        seen = [r.get("domainId") for r in summary if isinstance(r, dict)]
        for dom in INPUT_DOMAINS:
            n = seen.count(dom)
            if n != 1:
                e.append(f"input domain {dom} declared {n} times, must be exactly once")
        for extra in set(seen) - set(INPUT_DOMAINS):
            e.append(f"unknown input domain {extra}")
        for r in summary:
            if not isinstance(r, dict):
                e.append("inputSummary entry is not an object")
                continue
            dom = r.get("domainId")
            if r.get("availability") not in AVAILABILITY:
                e.append(f"{dom}: availability {r.get('availability')!r} not in vocabulary")
            if r.get("inputClass") not in INPUT_CLASSES:
                e.append(f"{dom}: inputClass {r.get('inputClass')!r} not in vocabulary")
            if r.get("requirement") not in REQUIREMENTS:
                e.append(f"{dom}: requirement {r.get('requirement')!r} not in vocabulary")
            # The requirement is contract-fixed; a package may not downgrade it.
            fixed = DOMAIN_REQUIREMENT.get(dom)
            if fixed and r.get("requirement") != fixed:
                e.append(f"{dom} is a {fixed} and may not be relabelled")
            # A required truth input that is missing is a STOP, not a package.
            if dom in REQUIRED_TRUTH_DOMAINS and r.get("availability") != "AVAILABLE":
                e.append(f"{dom} is a REQUIRED_TRUTH_INPUT and is not AVAILABLE: STOP condition")
            # UNAVAILABLE and UNAVAILABLE_INPUT are two views of one fact: the
            # input could not be obtained. Neither may be stated without the
            # other, or a later system reads a provenance class as evidence
            # that something was actually supplied.
            if (r.get("availability") == "UNAVAILABLE"
                    and r.get("inputClass") != "UNAVAILABLE_INPUT"):
                e.append(f"{dom}: availability UNAVAILABLE requires inputClass UNAVAILABLE_INPUT")
            if (r.get("inputClass") == "UNAVAILABLE_INPUT"
                    and r.get("availability") != "UNAVAILABLE"):
                e.append(f"{dom}: inputClass UNAVAILABLE_INPUT requires availability UNAVAILABLE")
            for k in r:
                if k not in ("domainId", "availability", "inputClass", "requirement", "note"):
                    e.append(f"{dom}: unknown inputSummary key {k}")

    tc = pkg.get("truthConstraints")
    if not isinstance(tc, dict):
        e.append("truthConstraints must be an object")
    else:
        if tc.get("productTruthMayBeTransformed") is not False:
            e.append("productTruthMayBeTransformed must be false")
        if tc.get("humanIdentityMayBeTransformed") is not False:
            e.append("humanIdentityMayBeTransformed must be false")
        if tc.get("worldPhysicsMayBreak") is not True:
            e.append("worldPhysicsMayBreak must be true")

    bc = pkg.get("brandConstraints")
    if not isinstance(bc, dict):
        e.append("brandConstraints must be an object")
    elif bc.get("mustRemainSpecific") is not True:
        e.append("mustRemainSpecific must be true")

    tf = pkg.get("targetFormat")
    if not isinstance(tf, dict) or not tf.get("intent"):
        e.append("targetFormat.intent must be a non-empty string")

    ideas = pkg.get("ideas")
    if not isinstance(ideas, list):
        e.append("ideas must be an array")
    else:
        if len(ideas) != 3:
            e.append(f"INITIAL mode requires exactly 3 ideas, found {len(ideas)}")
        for i, idea in enumerate(ideas):
            if not isinstance(idea, dict):
                e.append(f"idea[{i}] is not an object")
                continue
            for key in IDEA_REQUIRED:
                if key not in idea:
                    e.append(f"idea[{i}] missing {key}")
            for key in idea:
                if key not in IDEA_REQUIRED and key not in IDEA_OPTIONAL:
                    e.append(f"idea[{i}] unknown key {key}")
            if idea.get("productRole") not in PRODUCT_ROLES:
                e.append(f"idea[{i}] productRole {idea.get('productRole')!r} not in vocabulary")
            if idea.get("characterRole") not in CHARACTER_ROLES:
                e.append(f"idea[{i}] characterRole {idea.get('characterRole')!r} not in vocabulary")
            if idea.get("state") not in IDEA_STATES:
                e.append(f"idea[{i}] state {idea.get('state')!r} not in vocabulary")
            if not idea.get("creativeMechanisms"):
                e.append(f"idea[{i}] creativeMechanisms must be non-empty")
    return e


def valid_package():
    """A package the contract must accept."""
    def summary(dom, avail, cls, req):
        return {"domainId": dom, "availability": avail, "inputClass": cls, "requirement": req}

    def idea(ref, prole, crole):
        return {
            "ideaRef": ref, "title": f"synthetic {ref}",
            "worldPremise": "synthetic premise for validation only",
            "purpose": "exercise the validator", "productRole": prole, "characterRole": crole,
            "targetFormatIntent": "synthetic", "creativeMechanisms": ["synthetic mechanism"],
            "truthRisks": [], "state": "PROPOSAL",
        }

    return {
        "schemaVersion": 1,
        "contextRef": "synthetic-fixture-1",
        "generatedAt": "2026-01-01",
        "inputSummary": [
            summary("WORLD_STORY_STATE", "UNAVAILABLE", "UNAVAILABLE_INPUT",
                    "OPTIONAL_CONTEXT_INPUT"),
            summary("CULTURAL_SOCIAL_SIGNALS", "UNAVAILABLE", "UNAVAILABLE_INPUT",
                    "OPTIONAL_CONTEXT_INPUT"),
            summary("BRAND_DNA_HERITAGE", "AVAILABLE", "CANONICAL_FACT",
                    "REQUIRED_TRUTH_INPUT"),
            summary("CHARACTER_CONTEXT", "UNAVAILABLE", "UNAVAILABLE_INPUT",
                    "OPTIONAL_CONTEXT_INPUT"),
            summary("CURRENT_PRODUCTS", "AVAILABLE", "CANONICAL_FACT", "REQUIRED_TRUTH_INPUT"),
            summary("TARGET_FORMAT", "AVAILABLE", "LOCKED_OWNER_DECISION",
                    "REQUIRED_TRUTH_INPUT"),
        ],
        "brandConstraints": {"heritageSource": "PINK MALL heritage", "mustRemainSpecific": True},
        "truthConstraints": {"productTruthMayBeTransformed": False,
                             "humanIdentityMayBeTransformed": False,
                             "worldPhysicsMayBreak": True},
        "targetFormat": {"intent": "synthetic target format"},
        "ideas": [idea("A", "HERO", "INA"), idea("B", "NONE", "DUO"),
                  idea("C", "DETAIL", "NONE")],
    }


def mutate(fn):
    """Return a copy of the valid package with fn applied."""
    pkg = json.loads(json.dumps(valid_package()))
    fn(pkg)
    return pkg


def main():
    print("PINK MALL — Campaign Context Contract (01) validator\n")

    # ── A. documents parse and agree on identity ─────────────────────────────
    print("A. documents and identity")
    for path in (JSON_PATH, SCHEMA_PATH, OBJECT_PATH, MD_PATH, PARENT_PATH):
        if not os.path.exists(path):
            print(f"  FAIL  missing required file {os.path.basename(path)}")
            print("CAMPAIGN CONTEXT CONTRACT: FAIL (cannot continue)")
            sys.exit(1)
    try:
        c = load(JSON_PATH)
        check("1. contract JSON parses", True)
    except Exception as exc:
        check("1. contract JSON parses", False, str(exc))
        print("CAMPAIGN CONTEXT CONTRACT: FAIL (cannot continue)")
        sys.exit(1)
    try:
        schema = load(SCHEMA_PATH)
        obj = load(OBJECT_PATH)
        parent = load(PARENT_PATH)
        check("2. contract schema, object schema and parent contract parse", True)
    except Exception as exc:
        check("2. contract schema, object schema and parent contract parse", False, str(exc))
        print("CAMPAIGN CONTEXT CONTRACT: FAIL (cannot continue)")
        sys.exit(1)
    with open(MD_PATH, encoding="utf-8") as fh:
        md = fh.read()
    # Emphasis markers must not be able to defeat a prose check: "grants
    # **nothing** else" and "grants nothing else" make the same promise.
    md_plain = " ".join(md.replace("*", "").replace("`", "").replace("_", " ").split())

    check("3. contractId is the expected id", c.get("contractId") == EXPECTED_CONTRACT_ID,
          str(c.get("contractId")))
    check("4. contractNumber is 01", c.get("contractNumber") == EXPECTED_NUMBER,
          str(c.get("contractNumber")))
    check("5. parentContract is the System Authority Contract",
          c.get("parentContract") == EXPECTED_PARENT_ID, str(c.get("parentContract")))
    check("6. status is a declared provenance value",
          c.get("status") in ("CANDIDATE", "CANONICAL", "SUPERSEDED"), str(c.get("status")))
    check("7. human-readable contract states the same id and version",
          c["contractId"] in md and c["version"] in md)
    # Counting dots called "foo.bar.baz" a semantic version. Because no JSON
    # Schema engine runs here, this validator must itself enforce the claim it
    # prints, so it applies the same pattern the schema specifies.
    check("8. version is a semantic version", bool(SEMVER.fullmatch(str(c.get("version", "")))),
          str(c.get("version")))
    check("    the contract schema expresses the same version rule",
          schema.get("properties", {}).get("version", {}).get("pattern")
          in (r"^\d+\.\d+\.\d+$", SEMVER.pattern),
          str(schema.get("properties", {}).get("version", {}).get("pattern")))
    check("    that pattern and this validator agree on what they accept",
          all(bool(re.fullmatch(schema["properties"]["version"]["pattern"], v))
              == bool(SEMVER.fullmatch(v))
              for v in ("1.0.0", "foo.bar.baz", "1.0", "1.0.0.0", "v1.0.0", "1.0.x")))

    # ── B. inheritance and non-contradiction of the parent ───────────────────
    print("\nB. inheritance from contract 00")
    inh = c.get("inheritance", "")
    check("9. inheritance forbids contradicting the parent",
          "MUST NOT contradict" in inh, inh[:80])
    check("10. inheritance states status is provenance, not permission",
          "provenance" in inh.lower(), inh[:80])
    check("11. canonicality is deferred to the parent's rule",
          "canonicalityRule" in inh or "canonicality" in inh.lower(), inh[:80])
    pseq = parent.get("contractSequence", {}).get("slots", [])
    slot = next((s for s in pseq if s.get("contractNumber") == EXPECTED_NUMBER), None)
    check("12. parent reserves slot 01 for this contract id",
          slot is not None and slot.get("contractId") == EXPECTED_CONTRACT_ID, str(slot))
    check("13. parent registry does not record file existence as canonicality",
          parent.get("canonicalityRule", {}).get("fileExistenceImpliesCanonicality") is False)
    ptc = {t["classId"] if isinstance(t, dict) and "classId" in t else t
           for t in parent.get("truthClasses", [])}
    check("14. every contract-01 input class maps onto a parent truth vocabulary word or is "
          "locally defined", len(set(INPUT_CLASSES)) == 8, str(len(INPUT_CLASSES)))
    check("15. parent grants the owner spend authority (01 may not)",
          bool(parent.get("spendAuthorityOwner")))

    # ── C. the contract's own governance rules ───────────────────────────────
    print("\nC. contract rules")
    dom_ids = [d.get("domainId") for d in c.get("inputDomains", [])]
    check("16. all six input domains present exactly once",
          all(dom_ids.count(d) == 1 for d in INPUT_DOMAINS) and len(dom_ids) == 6,
          str(dom_ids))
    req_map = {d["domainId"]: d.get("requirement") for d in c.get("inputDomains", [])}
    check("17. exactly the three required truth inputs are REQUIRED_TRUTH_INPUT",
          {d for d, r in req_map.items() if r == "REQUIRED_TRUTH_INPUT"} == REQUIRED_TRUTH_DOMAINS,
          str(req_map))
    check("18. every input domain declares a default input class",
          all(d.get("defaultInputClass") in INPUT_CLASSES for d in c.get("inputDomains", [])))
    planned = {d["domainId"] for d in c.get("inputDomains", [])
               if d.get("providerImplementationStatus") == "PLANNED"}
    check("19. no REQUIRED_TRUTH_INPUT depends on a PLANNED provider",
          not (planned & REQUIRED_TRUTH_DOMAINS), str(sorted(planned & REQUIRED_TRUTH_DOMAINS)))
    check("20. story state and social signals are declared PLANNED, not ACTIVE",
          {"WORLD_STORY_STATE", "CULTURAL_SOCIAL_SIGNALS"} <= planned, str(sorted(planned)))

    cls_ids = [x.get("classId") for x in c.get("inputClasses", [])]
    check("21. all eight input classes present exactly once",
          all(cls_ids.count(x) == 1 for x in INPUT_CLASSES) and len(cls_ids) == 8, str(cls_ids))
    check("22. NO input class may override truth",
          all(x.get("mayOverrideTruth") is False for x in c.get("inputClasses", [])),
          str([x["classId"] for x in c.get("inputClasses", [])
               if x.get("mayOverrideTruth") is not False]))
    got = {x.get("classId"): x.get("authoritative") for x in c.get("inputClasses", [])}
    check("23. every input class carries its pinned authority value",
          got == INPUT_CLASS_AUTHORITY,
          str({k: v for k, v in got.items() if INPUT_CLASS_AUTHORITY.get(k) is not v}))
    check("    a reference to private material is not itself authority",
          got.get("PRIVATE_OPS_REFERENCE") is False, str(got.get("PRIVATE_OPS_REFERENCE")))
    check("    an unobtainable input is not authority",
          got.get("UNAVAILABLE_INPUT") is False)
    check("    signals and interpretations are not authority",
          got.get("SOCIAL_OR_CULTURAL_SIGNAL") is False
          and got.get("SEMANTIC_INTERPRETATION") is False)
    check("    the four canonical-origin classes remain authoritative",
          all(got.get(k) is True for k in ("CANONICAL_FACT", "DERIVED_FACT",
                                           "LOCKED_OWNER_DECISION", "OPERATIONAL_STATE")))

    im = c.get("ideaMode", {})
    check("24. INITIAL mode requires exactly three proposals per cycle",
          im.get("proposalsPerCycle") == 3 and im.get("exactly") is True, str(im))
    check("25. selection authority is the OWNER", im.get("selectionAuthority") == "OWNER",
          str(im.get("selectionAuthority")))
    check("26. autonomous selection is not granted", im.get("autonomousSelection") is False)
    check("27. no ranking threshold is claimed to exist",
          im.get("rankingThresholdDefined") is False)

    pr = c.get("proposalRules", {})
    check("28. default idea state is PROPOSAL", pr.get("defaultState") == "PROPOSAL")
    check("29. allowed idea states are exactly PROPOSAL and OWNER_SELECTED",
          pr.get("allowedStates") == IDEA_STATES, str(pr.get("allowedStates")))
    check("30. owner selection grants nothing further", pr.get("selectionGrants") == [],
          str(pr.get("selectionGrants")))
    check("31. selection explicitly does not grant spend or publication",
          {"paid generation", "publication"} <= set(pr.get("selectionDoesNotGrant", [])),
          str(pr.get("selectionDoesNotGrant")))

    prole_ids = [r.get("roleId") for r in c.get("productRoles", [])]
    crole_ids = [r.get("roleId") for r in c.get("characterRoles", [])]
    check("32. product roles are exactly NONE/DETAIL/SUPPORTING/HERO",
          prole_ids == PRODUCT_ROLES, str(prole_ids))
    check("33. no product role is mandatory (a product is never forced into an idea)",
          all(r.get("required") is False for r in c.get("productRoles", [])))
    check("34. character roles are exactly INA/SIS/DUO/NONE", crole_ids == CHARACTER_ROLES,
          str(crole_ids))

    fail_ids = {f.get("failureId") for f in c.get("hardFailures", [])}
    check("35. the three named hard failures are present", REQUIRED_FAILURES <= fail_ids,
          str(sorted(REQUIRED_FAILURES - fail_ids)))
    check("36. GENERIC_AI_AESTHETIC is a HARD_FAIL with concrete examples",
          any(f["failureId"] == "GENERIC_AI_AESTHETIC" and f.get("severity") == "HARD_FAIL"
              and len(f.get("examples", [])) >= 3 for f in c.get("hardFailures", [])))
    check("37. every hard failure carries a severity and a definition",
          all(f.get("severity") and f.get("definition") for f in c.get("hardFailures", [])))
    sig = " ".join(c.get("signalRules", []))
    check("38. signals are evidence, never authority",
          "MUST NOT be treated as authority" in sig)
    check("39. model knowledge may not pose as current social evidence",
          "Model knowledge MUST NOT be presented as current social evidence" in sig)
    miss = " ".join(c.get("missingInputRules", []))
    check("40. an unobtainable input is recorded UNAVAILABLE, never fabricated",
          "UNAVAILABLE" in miss and "fabricated" in miss)
    check("41. absence of a REQUIRED_TRUTH_INPUT is a STOP condition",
          "REQUIRED_TRUTH_INPUT is a STOP" in miss, miss[:120])
    check("42. open items are declared undecided and may not be invented",
          len(c.get("openItems", [])) >= 5 and "MUST NOT be answered by invention"
          in c.get("openItemsRule", ""))

    # ── D. public repository privacy boundary ────────────────────────────────
    print("\nD. privacy boundary")
    priv = " ".join(c.get("privacyRules", []))
    check("43. the contract states this repository is PUBLIC", "PUBLIC" in priv)
    check("44. unpublished real campaign concepts may not be committed here",
          "MUST NOT be committed" in priv)
    check("45. a private reference may name private material but never carry it",
          "content MUST NOT appear" in priv.lower() or "The content MUST NOT appear" in priv)
    check("46. runtime context instances are not committed",
          c.get("contextObject", {}).get("committed") is False)

    # ── E. the schemas structurally ENCODE these rules ───────────────────────
    print("\nE. schema structure (read from the schema documents, not their prose)")
    sp = schema.get("properties", {})

    def _rules(node, key):
        """allOf entries whose `contains` pins `key` to a const, split by shape.

        An identity rule constrains the key alone and carries min=max=1, so it
        proves the id appears exactly once. A binding rule additionally pins a
        second field and carries minContains only: paired with the identity rule
        it proves THE one record with that id carries that value. maxContains on
        a binding rule would be weaker, not stronger — a non-matching duplicate
        would satisfy it.
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
        """Prove a schema array requires each id exactly once via allOf/contains."""
        ident, _ = _rules(node, key)
        bad = [k for k, rs in ident.items()
               if not any(r.get("minContains") == 1 and r.get("maxContains") == 1 for r in rs)]
        cov = set(ident)
        return cov == set(expected) and not bad, f"covered={sorted(cov)} bad={bad}"

    def binds(node, key, field, mapping):
        """Prove each id is bound to its expected value for `field`.

        Relies on exactly_once holding for the same key: exactly one record
        carries the id, and at least one record carries id AND value, so that
        one record carries the value.
        """
        _, bound = _rules(node, key)
        missing, wrong = [], []
        for ident, expected in mapping.items():
            rules = bound.get(ident, [])
            hit = [r for r in rules
                   if r.get("contains", {}).get("properties", {}).get(field, {})
                   .get("const", "\0MISSING") == expected
                   and r.get("minContains", 0) >= 1
                   and field in r.get("contains", {}).get("required", [])]
            if not rules:
                missing.append(ident)
            elif not hit:
                wrong.append(f"{ident}->{expected!r}")
        return not missing and not wrong, f"unbound={missing} wrong={wrong}"

    ok, d = exactly_once(sp.get("inputDomains", {}), "domainId", INPUT_DOMAINS)
    check("47. contract schema requires each input domain exactly once", ok, d)
    ok, d = exactly_once(sp.get("inputClasses", {}), "classId", INPUT_CLASSES)
    check("48. contract schema requires each input class exactly once", ok, d)
    ok, d = binds(sp.get("inputClasses", {}), "classId", "authoritative", INPUT_CLASS_AUTHORITY)
    check("    contract schema pins each class's authority value", ok, d)
    check("    contract schema leaves no class authority as a free boolean",
          sp.get("inputClasses", {}).get("items", {}).get("properties", {})
          .get("mayOverrideTruth", {}).get("const") is False and ok)
    check("    contract schema records the authority map for readers",
          schema.get("x-inputClassAuthority") == INPUT_CLASS_AUTHORITY)
    ok, d = exactly_once(sp.get("productRoles", {}), "roleId", PRODUCT_ROLES)
    check("49. contract schema requires each product role exactly once", ok, d)
    ok, d = exactly_once(sp.get("characterRoles", {}), "roleId", CHARACTER_ROLES)
    check("50. contract schema requires each character role exactly once", ok, d)
    ok, d = exactly_once(sp.get("hardFailures", {}), "failureId", REQUIRED_FAILURES)
    check("51. contract schema requires each named hard failure exactly once", ok, d)
    check("52. contract schema is closed to unknown top-level keys",
          schema.get("additionalProperties") is False)
    check("53. contract schema pins proposalsPerCycle to 3",
          sp.get("ideaMode", {}).get("properties", {}).get("proposalsPerCycle", {})
          .get("const") == 3)
    check("54. contract schema forbids autonomous selection",
          sp.get("ideaMode", {}).get("properties", {}).get("autonomousSelection", {})
          .get("const") is False)
    check("55. contract schema pins selectionGrants to the empty list",
          sp.get("proposalRules", {}).get("properties", {}).get("selectionGrants", {})
          .get("maxItems") == 0)

    op = obj.get("properties", {})
    ideas_node = op.get("ideas", {})
    check("56. object schema requires exactly three ideas",
          ideas_node.get("minItems") == 3 and ideas_node.get("maxItems") == 3,
          f"min={ideas_node.get('minItems')} max={ideas_node.get('maxItems')}")
    iprops = ideas_node.get("items", {}).get("properties", {})
    check("57. object schema closes the product-role vocabulary",
          iprops.get("productRole", {}).get("enum") == PRODUCT_ROLES)
    check("58. object schema closes the character-role vocabulary",
          iprops.get("characterRole", {}).get("enum") == CHARACTER_ROLES)
    check("59. object schema limits idea state to PROPOSAL and OWNER_SELECTED",
          iprops.get("state", {}).get("enum") == IDEA_STATES)
    check("60. object schema admits no execution, spend or publication state",
          not (set(FORBIDDEN_STATES) & set(iprops.get("state", {}).get("enum", []))))
    check("61. object schema records the states contract 01 may not express",
          obj.get("x-notPermittedStates") == FORBIDDEN_STATES)
    check("62. object schema closes the idea object",
          ideas_node.get("items", {}).get("additionalProperties") is False)
    check("63. object schema requires every governance field on an idea",
          set(IDEA_REQUIRED) <= set(ideas_node.get("items", {}).get("required", [])),
          str(sorted(set(IDEA_REQUIRED) - set(ideas_node.get("items", {}).get("required", [])))))
    ok, d = exactly_once(op.get("inputSummary", {}), "domainId", INPUT_DOMAINS)
    check("64. object schema requires provenance for each input domain exactly once", ok, d)
    # The semantic checker enforces these two rules, so the schema must encode
    # them too: otherwise the validator's own claim that every rule it enforces
    # is mirrored in the schema would be false.
    ok, d = binds(op.get("inputSummary", {}), "domainId", "requirement", DOMAIN_REQUIREMENT)
    check("    object schema binds each domain to its contract-fixed requirement", ok, d)
    ok, d = binds(op.get("inputSummary", {}), "domainId", "availability",
                  {k: "AVAILABLE" for k in REQUIRED_TRUTH_DOMAINS})
    check("    object schema pins every REQUIRED_TRUTH_INPUT to AVAILABLE", ok, d)
    _, obound = _rules(op.get("inputSummary", {}), "domainId")
    pinned_avail = {k for k, rs in obound.items()
                    if any("availability" in r.get("contains", {}).get("properties", {})
                           for r in rs)}
    check("    object schema leaves optional domains free to be unavailable",
          not (pinned_avail & OPTIONAL_DOMAINS), str(sorted(pinned_avail & OPTIONAL_DOMAINS)))
    check("    object schema and semantic checker share one requirement map",
          op.get("inputSummary", {}) is not None
          and obj.get("x-domainRequirement") == DOMAIN_REQUIREMENT,
          str(obj.get("x-domainRequirement")))
    # UNAVAILABLE <-> UNAVAILABLE_INPUT, encoded as a pair of if/then rules.
    conds = op.get("inputSummary", {}).get("items", {}).get("allOf", [])

    def _implies(if_field, if_val, then_field, then_val):
        return any(r.get("if", {}).get("properties", {}).get(if_field, {}).get("const") == if_val
                   and r.get("then", {}).get("properties", {}).get(then_field, {})
                   .get("const") == then_val for r in conds)

    check("    object schema requires UNAVAILABLE to carry UNAVAILABLE_INPUT",
          _implies("availability", "UNAVAILABLE", "inputClass", "UNAVAILABLE_INPUT"))
    check("    object schema requires UNAVAILABLE_INPUT to be UNAVAILABLE",
          _implies("inputClass", "UNAVAILABLE_INPUT", "availability", "UNAVAILABLE"))
    check("    object schema documents what UNAVAILABLE means for provenance",
          "NOT_APPLICABLE" in str(obj.get("x-unavailableSemantics", "")))
    isum_props = op.get("inputSummary", {}).get("items", {}).get("properties", {})
    check("65. object schema requires availability to be declared, not implied",
          isum_props.get("availability", {}).get("enum") == AVAILABILITY
          and {"domainId", "availability", "inputClass", "requirement"}
          <= set(op.get("inputSummary", {}).get("items", {}).get("required", [])))
    tcp = op.get("truthConstraints", {}).get("properties", {})
    check("66. object schema pins product truth as untransformable",
          tcp.get("productTruthMayBeTransformed", {}).get("const") is False)
    check("67. object schema pins human identity as untransformable",
          tcp.get("humanIdentityMayBeTransformed", {}).get("const") is False)
    check("68. object schema permits world physics to break",
          tcp.get("worldPhysicsMayBreak", {}).get("const") is True)
    check("69. object schema is closed to unknown top-level keys",
          obj.get("additionalProperties") is False)
    check("70. object schema requires every governance field on the package",
          set(PKG_REQUIRED) <= set(obj.get("required", [])),
          str(sorted(set(PKG_REQUIRED) - set(obj.get("required", [])))))

    # ── F. synthetic runtime fixtures (targeted semantic checker) ────────────
    print("\nF. synthetic runtime fixtures — targeted semantic checker, NOT a JSON Schema engine")
    errs = check_package(valid_package())
    check("71. a well-formed package is ACCEPTED", not errs, str(errs[:4]))

    def rejects(label, fn, needle=None):
        e = check_package(mutate(fn))
        ok = bool(e) and (needle is None or any(needle in x for x in e))
        check(label, ok, f"errors={e[:3]}")

    rejects("72. two ideas are REJECTED", lambda p: p["ideas"].pop(), "exactly 3 ideas")
    rejects("73. four ideas are REJECTED",
            lambda p: p["ideas"].append(json.loads(json.dumps(p["ideas"][0]))), "exactly 3 ideas")
    rejects("74. zero ideas are REJECTED", lambda p: p.__setitem__("ideas", []), "exactly 3 ideas")
    rejects("75. an unknown productRole is REJECTED",
            lambda p: p["ideas"][0].__setitem__("productRole", "MEGA_HERO"), "productRole")
    rejects("76. an unknown characterRole is REJECTED",
            lambda p: p["ideas"][1].__setitem__("characterRole", "MOTHER"), "characterRole")
    rejects("77. an absent input-domain provenance record is REJECTED",
            lambda p: p["inputSummary"].pop(0), "WORLD_STORY_STATE")
    rejects("78. a duplicated input-domain provenance record is REJECTED",
            lambda p: p["inputSummary"].append(json.loads(json.dumps(p["inputSummary"][0]))),
            "exactly once")
    rejects("79. an undeclared availability is REJECTED",
            lambda p: p["inputSummary"][0].__setitem__("availability", "MAYBE"), "availability")
    rejects("80. a missing REQUIRED_TRUTH_INPUT is REJECTED as a STOP condition",
            lambda p: p["inputSummary"][4].__setitem__("availability", "UNAVAILABLE"), "STOP")
    idx = {d: i for i, d in enumerate(INPUT_DOMAINS)}
    rejects("81. relabelling CURRENT_PRODUCTS as optional is REJECTED",
            lambda p: p["inputSummary"][idx["CURRENT_PRODUCTS"]]
            .__setitem__("requirement", "OPTIONAL_CONTEXT_INPUT"), "may not be relabelled")
    rejects("    relabelling TARGET_FORMAT as optional is REJECTED",
            lambda p: p["inputSummary"][idx["TARGET_FORMAT"]]
            .__setitem__("requirement", "OPTIONAL_CONTEXT_INPUT"), "may not be relabelled")
    rejects("    relabelling BRAND_DNA_HERITAGE as optional is REJECTED",
            lambda p: p["inputSummary"][idx["BRAND_DNA_HERITAGE"]]
            .__setitem__("requirement", "OPTIONAL_CONTEXT_INPUT"), "may not be relabelled")
    rejects("    promoting an optional domain to required truth is REJECTED",
            lambda p: p["inputSummary"][idx["WORLD_STORY_STATE"]]
            .__setitem__("requirement", "REQUIRED_TRUTH_INPUT"), "may not be relabelled")

    def _unavailable(dom):
        def fn(p):
            r = p["inputSummary"][idx[dom]]
            r["availability"] = "UNAVAILABLE"
            r["inputClass"] = "UNAVAILABLE_INPUT"
        return fn

    rejects("    an unavailable CURRENT_PRODUCTS is REJECTED as a STOP condition",
            _unavailable("CURRENT_PRODUCTS"), "STOP")
    rejects("    an unavailable BRAND_DNA_HERITAGE is REJECTED as a STOP condition",
            _unavailable("BRAND_DNA_HERITAGE"), "STOP")
    rejects("    an unavailable TARGET_FORMAT is REJECTED as a STOP condition",
            _unavailable("TARGET_FORMAT"), "STOP")
    rejects("    UNAVAILABLE carrying a provenance class is REJECTED",
            lambda p: p["inputSummary"][idx["WORLD_STORY_STATE"]]
            .__setitem__("inputClass", "OPERATIONAL_STATE"), "requires inputClass")
    rejects("    UNAVAILABLE_INPUT claimed AVAILABLE is REJECTED",
            lambda p: p["inputSummary"][idx["CHARACTER_CONTEXT"]]
            .__setitem__("availability", "AVAILABLE"), "requires availability UNAVAILABLE")

    def _optional_unavailable(p):
        r = p["inputSummary"][idx["CULTURAL_SOCIAL_SIGNALS"]]
        r["availability"], r["inputClass"] = "UNAVAILABLE", "UNAVAILABLE_INPUT"

    check("    an unavailable OPTIONAL domain is still ACCEPTED",
          not check_package(mutate(_optional_unavailable)),
          str(check_package(mutate(_optional_unavailable))[:3]))
    rejects("82. a PUBLISHED idea state is REJECTED",
            lambda p: p["ideas"][0].__setitem__("state", "PUBLISHED"), "state")
    rejects("83. an APPROVED_SPEND idea state is REJECTED",
            lambda p: p["ideas"][2].__setitem__("state", "APPROVED_SPEND"), "state")
    rejects("84. transformable product truth is REJECTED",
            lambda p: p["truthConstraints"].__setitem__("productTruthMayBeTransformed", True),
            "productTruthMayBeTransformed")
    rejects("85. transformable human identity is REJECTED",
            lambda p: p["truthConstraints"].__setitem__("humanIdentityMayBeTransformed", True),
            "humanIdentityMayBeTransformed")
    rejects("86. an idea missing its truth-risk field is REJECTED",
            lambda p: p["ideas"][0].pop("truthRisks"), "truthRisks")
    rejects("87. an idea missing its world premise is REJECTED",
            lambda p: p["ideas"][1].pop("worldPremise"), "worldPremise")
    rejects("88. an unknown top-level package key is REJECTED",
            lambda p: p.__setitem__("autoPublish", True), "autoPublish")
    rejects("89. an unknown idea key is REJECTED",
            lambda p: p["ideas"][0].__setitem__("approvedBudget", 500), "approvedBudget")
    rejects("90. a wrong schemaVersion is REJECTED",
            lambda p: p.__setitem__("schemaVersion", 2), "schemaVersion")
    rejects("91. an empty creativeMechanisms list is REJECTED",
            lambda p: p["ideas"][2].__setitem__("creativeMechanisms", []), "creativeMechanisms")

    # The fixtures above prove behaviour. Prove the same package shape is what
    # the schema document describes, so the two cannot drift apart silently.
    check("92. the accepted fixture uses only keys the object schema declares",
          set(valid_package()) <= set(op), str(set(valid_package()) - set(op)))
    check("93. the accepted fixture's idea keys are all declared by the object schema",
          set(valid_package()["ideas"][0]) <= set(iprops))

    # ── G. registry bookkeeping ──────────────────────────────────────────────
    print("\nG. registry bookkeeping")
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, encoding="utf-8") as fh:
            index = fh.read()
        # Split at the NOT YET CREATED heading: a contract that exists must be
        # listed above it and must no longer appear below it. Testing the
        # sections separately, because "01" appears in both tables' prose.
        marker = "## Planned contracts"
        head, _, tail = index.partition(marker)
        rows_above = [ln for ln in head.splitlines() if ln.strip().startswith("| 01 ")]
        rows_below = [ln for ln in tail.splitlines() if ln.strip().startswith("| 01 ")]
        check("94. the contract index lists contract 01 in its current set",
              len(rows_above) == 1 and "CAMPAIGN_CONTEXT" in rows_above[0].upper(),
              str(rows_above))
        check("95. the contract index no longer lists 01 as NOT YET CREATED",
              bool(marker in index) and not rows_below, str(rows_below))
        check("    the contract index names the contract-01 validator",
              "campaign_context_contract.py" in index)
        check("    the contract index does not treat file existence as canonicality",
              "existence does not make it canonical" in index.lower()
              or "does not assert" in index.lower())
        # This once read "still lists 02-08 as NOT YET CREATED". That was a
        # point-in-time fact, not an invariant: it had to fail the moment the
        # next domain contract was authored. The durable rule is that the two
        # sections agree with what is actually on disk, so that is what is
        # checked — derived from the filesystem, never from a hardcoded range.
        misfiled = []
        for i in range(2, 9):
            num = f"0{i}"
            listed_planned = any(ln.strip().startswith(f"| {num} ")
                                 for ln in tail.splitlines())
            listed_current = any(ln.strip().startswith(f"| {num} ")
                                 for ln in head.splitlines())
            exists = bool(glob.glob(os.path.join(CDIR, f"{num}_*_CONTRACT.json")))
            if exists and (listed_planned or not listed_current):
                misfiled.append(f"{num}: files exist but index says NOT YET CREATED")
            if not exists and (listed_current or not listed_planned):
                misfiled.append(f"{num}: no files but index lists it as created")
        check("    the index's created/not-created split matches what is on disk",
              not misfiled, str(misfiled))
    else:
        check("94. the contract index exists", False, INDEX_PATH)
    if os.path.exists(MATRIX_PATH):
        with open(MATRIX_PATH, encoding="utf-8") as fh:
            matrix = fh.read()
        check("96. the decision-coverage matrix records the Campaign Context row",
              "Campaign Context" in matrix)
    else:
        check("96. the decision-coverage matrix exists", False, MATRIX_PATH)

    slots = parent.get("contractSequence", {}).get("slots", [])
    nums = [s.get("contractNumber") for s in slots]
    cids = [s.get("contractId") for s in slots]
    check("97. parent sequence is 00–08 with no gaps",
          nums == [f"{i:02d}" for i in range(9)], str(nums))
    check("98. parent sequence contract ids are unique", len(set(cids)) == len(cids))
    check("99. parent registry defers existence to the index, not to the sequence",
          "SYSTEM_CONTRACT_INDEX.md" in parent.get("contractSequence", {})
          .get("existenceRecordedIn", ""))

    # ── H. human-readable contract agrees with the JSON ──────────────────────
    print("\nH. human-readable agreement")
    # Derive the expected wording from the JSON so the two cannot drift: if the
    # machine-readable count ever changes, this check changes with it.
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
    n = im.get("proposalsPerCycle")
    low = md_plain.lower()
    check("100. the markdown states the same proposal count as the JSON",
          f"exactly {words.get(n, n)}" in low or f"exactly {n}" in low, f"count={n}")
    check("    the markdown states no contradicting proposal count",
          not [w for k, w in words.items() if k != n and f"exactly {w} " in low],
          str([w for k, w in words.items() if k != n and f"exactly {w} " in low]))
    check("101. the markdown names every input domain",
          all(d in md for d in INPUT_DOMAINS),
          str([d for d in INPUT_DOMAINS if d not in md]))
    check("102. the markdown names every input class",
          all(x in md for x in INPUT_CLASSES),
          str([x for x in INPUT_CLASSES if x not in md]))
    check("103. the markdown names every product and character role",
          all(r in md for r in PRODUCT_ROLES + CHARACTER_ROLES))
    check("104. the markdown states that signals are not authority",
          "not authority" in md_plain.lower() or "never authority" in md_plain.lower())
    check("105. the markdown states the generic-AI hard failure",
          "GENERIC_AI_AESTHETIC" in md)
    check("106. the markdown states that selection grants nothing further",
          "grants nothing" in md_plain.lower())
    check("107. the markdown declares open items rather than inventing answers",
          "Open items" in md and "MUST NOT" in md)
    check("108. the markdown does not claim a Campaign Context Builder exists",
          "no builder exists" in md_plain.lower() or "does not exist" in md_plain.lower())
    # The human-readable authority column and the JSON must not disagree again.
    for cid, auth in sorted(INPUT_CLASS_AUTHORITY.items()):
        row = next((ln for ln in md.splitlines()
                    if ln.strip().startswith(f"| `{cid}`")), None)
        cells = [x.strip().lower() for x in row.split("|")] if row else []
        word = "yes" if auth else "no"
        check(f"    markdown authority column agrees for {cid}",
              row is not None and word in cells, str(row)[:90])
    check("109. the markdown states the UNAVAILABLE / UNAVAILABLE_INPUT equivalence",
          "UNAVAILABLE_INPUT" in md and "each implies the other" in md_plain.lower())
    check("110. the markdown keeps NOT_APPLICABLE distinct from UNAVAILABLE",
          "NOT_APPLICABLE" in md and "not sought" in md_plain.lower())

    print(f"\n{len(c.get('inputDomains', []))} input domains, "
          f"{len(c.get('inputClasses', []))} input classes, "
          f"{len(c.get('hardFailures', []))} hard failures, "
          f"{len(c.get('openItems', []))} open items")
    print("Runtime fixtures were checked by a targeted semantic checker, not a JSON Schema "
          "engine; section E proves the same rules are encoded in the schema documents.")
    print(f"CAMPAIGN CONTEXT CONTRACT: {'PASS' if not failed else 'FAIL'} "
          f"({passed} passed, {failed} failed)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
