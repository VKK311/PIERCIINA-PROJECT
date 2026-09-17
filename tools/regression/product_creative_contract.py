#!/usr/bin/env python3
"""Validator for the PINK MALL Product Creative Contract (contract 02).

    python tools/regression/product_creative_contract.py

This contract exists to settle what a generator may and may not change BEFORE
paid generation is switched on. That makes the failure it guards against a
specific one: a later system reading the machine-readable contract and quietly
claiming an authority nobody granted — redesigning a product it was only asked
to depict, treating an avatar photograph as evidence of a garment's cut, or
promoting a convincing generated image into canonical commerce media.

Three kinds of claim are checked, and they are not the same kind:

  * the contract JSON says what the human-readable contract says, and neither
    contradicts contract 00 or duplicates contract 01;
  * both JSON Schemas structurally ENCODE the rules that matter, proved by
    reading the schema documents rather than trusting their prose;
  * synthetic Product Reference Packages are accepted or rejected as the
    contract requires, proved by running them through the checker below.

HONEST LIMIT ON THE RUNTIME FIXTURES: the Python standard library ships no JSON
Schema engine and this foundation must not grow a dependency to check its own
constitution. `check_package` below is a TARGETED SEMANTIC CHECKER covering the
governance-bearing PRE-GENERATION subset of 02_PRODUCT_CREATIVE_OBJECT.schema.json:
exact identity and variant, exact-product geometry evidence, all nine Product
Locks engaged, clothing evidence READINESS for body-worn cases, the QA gate
obligations, the product and human truth constraints, the non-authoritative
execution layer, and the absence of any post-generation state. It is NOT a JSON
Schema engine and a fixture passing it is NOT proof of full schema conformance.

It does NOT check a post-generation result schema. No such schema exists: the
package describes inputs assembled before generation, so it carries no output
status and no QA result, only the obligation that each gate be evaluated if it
applies.
That is why every rule it enforces is ALSO proved present in the schema document
by the structural checks in section E: the fixtures show the rule behaves, the
structural checks show the rule is written where a real validator would read it.

Standard library only, by design.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CDIR = os.path.join(ROOT, "docs", "pink-mall", "system-contracts")

JSON_PATH   = os.path.join(CDIR, "02_PRODUCT_CREATIVE_CONTRACT.json")
SCHEMA_PATH = os.path.join(CDIR, "02_PRODUCT_CREATIVE_CONTRACT.schema.json")
OBJECT_PATH = os.path.join(CDIR, "02_PRODUCT_CREATIVE_OBJECT.schema.json")
MD_PATH     = os.path.join(CDIR, "02_PRODUCT_CREATIVE_CONTRACT.md")
PARENT_PATH = os.path.join(CDIR, "00_SYSTEM_AUTHORITY_CONTRACT.json")
DEP_PATH    = os.path.join(CDIR, "01_CAMPAIGN_CONTEXT_CONTRACT.json")
INDEX_PATH  = os.path.join(CDIR, "SYSTEM_CONTRACT_INDEX.md")
MATRIX_PATH = os.path.join(CDIR, "DECISION_COVERAGE_MATRIX.md")

EXPECTED_CONTRACT_ID = "PINK_MALL_PRODUCT_CREATIVE_CONTRACT"
EXPECTED_PARENT_ID   = "PINK_MALL_SYSTEM_AUTHORITY_CONTRACT"
EXPECTED_DEP_ID      = "PINK_MALL_CAMPAIGN_CONTEXT_CONTRACT"
EXPECTED_NUMBER      = "02"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

LOCKS = ["IDENTITY", "VARIANT", "SILHOUETTE", "GEOMETRY", "CONSTRUCTION", "PROPORTIONS",
         "COLOUR", "BRANDING_MARKINGS", "DISTINCTIVE_DETAILS"]
GATES = ["PRODUCT_IDENTITY", "PRODUCT_VARIANT", "SILHOUETTE", "GEOMETRY_CONSTRUCTION",
         "RELATIVE_PROPORTIONS", "DISTINCTIVE_DETAILS", "BRANDING_MARKINGS", "HARDWARE_CLOSURES",
         "CLOTHING_FIT_INTEGRITY", "HUMAN_TRUTH_INTEGRITY"]
STOP_FAILURES = {"CLOTHING_FIT_UNRESOLVED", "GENERATOR_CLAIMED_AUTHORITY"}
FAILURES = ["WRONG_PRODUCT", "WRONG_VARIANT", "PRODUCT_GEOMETRY_DRIFT",
            "PRODUCT_CONSTRUCTION_DRIFT", "DISTINCTIVE_DETAIL_DRIFT", "PRODUCT_TRUTH_CONTRADICTION",
            "HUMAN_IDENTITY_CONTRADICTION", "CLOTHING_FIT_UNRESOLVED",
            "UNSUPPORTED_EVIDENCE_TREATED_AS_EXACT", "GENERATOR_CLAIMED_AUTHORITY"]
PRODUCT_ROLES_HERE = ["DETAIL", "SUPPORTING", "HERO"]   # NONE means no package at all
FIT_OUTCOMES = ["PASS", "FAIL", "UNRESOLVED"]
OUTPUT_STATES = ["CANDIDATE", "QA_PASSED", "QA_FAILED", "QA_UNRESOLVED"]
FORBIDDEN_STATES = ["APPROVED", "APPROVED_SPEND", "PUBLISHED", "SCHEDULED", "EXECUTING"]
SUBJECTS = ["INA", "SIS", "DUO"]
# The package is assembled BEFORE generation, so it carries only what can
# truthfully exist before an output does: no generated-output status, and
# clothing-fit EVIDENCE rather than a clothing-fit RESULT.
PKG_REQUIRED = ["schemaVersion", "packageRef", "generatedAt", "isProductTruthRecord",
                "productIdentity", "productRole", "productGeometrySources", "productLocks",
                "creativeFreedoms", "riskClassification", "productConfidence",
                "knownUncertainties", "qaRequirements", "humanSubjects", "truthConstraints",
                "executionLayer"]
PKG_OPTIONAL = ["productWearReference", "clothingFitEvidence"]
# Post-generation vocabulary that must never appear in a pre-generation package.
POST_GENERATION_KEYS = ["outputStatus", "clothingFit", "fitStatus", "qaResults"]
NOT_APPLICABLE = "NOT_APPLICABLE"
PM_ID = re.compile(r"^PM-\d{3}$")

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
# Targeted semantic checker for a Product Reference Package.
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
        if key not in PKG_REQUIRED and key not in PKG_OPTIONAL:
            e.append(f"unknown top-level key {key}")

    if pkg.get("schemaVersion") != 1:
        e.append("schemaVersion must be 1")
    if pkg.get("isProductTruthRecord") is not False:
        e.append("isProductTruthRecord must be false: a package is a generation input")

    # ── exact product identity ───────────────────────────────────────────────
    pid = pkg.get("productIdentity")
    if not isinstance(pid, dict):
        e.append("productIdentity must be an object")
    else:
        if not PM_ID.match(str(pid.get("pmId", ""))):
            e.append(f"pmId {pid.get('pmId')!r} is not a PM-NNN identifier")
        if not pid.get("manufacturerItemNumber"):
            e.append("manufacturerItemNumber is required: an unnamed SKU cannot be locked")
        if not pid.get("variant"):
            e.append("variant is required: an unnamed variant cannot be locked")
        if pid.get("truthSource") not in ("PRODUCT_ONBOARDING_SYSTEM", "CANONICAL_REPOSITORY"):
            e.append(f"truthSource {pid.get('truthSource')!r} is not a Product Truth authority")
        if pid.get("mayBeWrittenByCreativeSystem") is not False:
            e.append("a creative system may never write Product Truth")
        if pid.get("similarSkuSubstituted") is True:
            e.append("a similar SKU was substituted: WRONG_PRODUCT")

    if pkg.get("productRole") not in PRODUCT_ROLES_HERE:
        e.append(f"productRole {pkg.get('productRole')!r} not in vocabulary "
                 f"(role NONE assembles no package at all)")

    # ── geometry evidence must be the exact product ──────────────────────────
    srcs = pkg.get("productGeometrySources")
    if not isinstance(srcs, list) or not srcs:
        e.append("productGeometrySources must contain at least one exact-product source")
    else:
        for i, s in enumerate(srcs):
            if not isinstance(s, dict):
                e.append(f"productGeometrySources[{i}] is not an object")
                continue
            if s.get("derivesFromExactProduct") is not True:
                e.append(f"geometry source {i} does not derive from the exact product")
            if s.get("isAvatarFrame") is True:
                e.append("an avatar frame is never product-geometry authority")
            if s.get("isGenericCategoryImagery") is True:
                e.append("generic category imagery is never product-geometry authority")
            if s.get("isDifferentColourway") is True:
                e.append("a different colourway is never product-geometry authority")
            for k in s:
                if k not in ("sourceRef", "derivesFromExactProduct", "isAvatarFrame",
                             "isGenericCategoryImagery", "isDifferentColourway",
                             "coversLockCategories"):
                    e.append(f"geometry source {i}: unknown key {k}")

    wear = pkg.get("productWearReference")
    if isinstance(wear, dict) and wear.get("authoritativeForGeometry") is not False:
        e.append("a wear reference is never authoritative for geometry")

    # ── every core lock present and engaged ──────────────────────────────────
    locks = pkg.get("productLocks")
    if not isinstance(locks, list):
        e.append("productLocks must be an array")
    else:
        seen = [l.get("lockId") for l in locks if isinstance(l, dict)]
        for lock in LOCKS:
            n = seen.count(lock)
            if n == 0:
                e.append(f"product lock {lock} is omitted")
            elif n > 1:
                e.append(f"product lock {lock} appears {n} times")
        for extra in set(seen) - set(LOCKS):
            e.append(f"unknown product lock {extra}")
        for l in locks:
            if isinstance(l, dict) and l.get("engaged") is not True:
                e.append(f"product lock {l.get('lockId')} is not engaged")

    # ── clothing risk and fit ────────────────────────────────────────────────
    risk = pkg.get("riskClassification")
    body_worn = isinstance(risk, dict) and risk.get("clothingWornOnBody") is True
    if isinstance(risk, dict):
        if risk.get("riskLevel") not in ("HIGH", "MEDIUM", "LOW"):
            e.append(f"riskLevel {risk.get('riskLevel')!r} not in vocabulary")
        if body_worn and risk.get("riskLevel") != "HIGH":
            e.append("clothing worn on a body is a HIGH-risk product-fidelity case")
    fit = pkg.get("clothingFitEvidence")
    if body_worn:
        if not isinstance(fit, dict):
            e.append("body-worn clothing requires clothingFitEvidence")
        else:
            # Readiness, not a verdict: a depiction that does not exist yet
            # cannot have passed or failed anything.
            if fit.get("garmentGeometryEvidencePresent") is not True:
                e.append("body-worn clothing requires garment geometry evidence; "
                         "generation readiness is BLOCKED without it")
            if fit.get("avatarWardrobeUsedAsGarmentAuthority") is not False:
                e.append("avatar wardrobe is never garment-geometry authority")
            if not isinstance(fit.get("wearFitEvidencePresent"), bool):
                e.append("wearFitEvidencePresent must be stated as a boolean, "
                         "and absent fit evidence declared in knownUncertainties")
            for k in fit:
                if k not in ("garmentGeometryEvidencePresent", "wearFitEvidencePresent",
                             "avatarWardrobeUsedAsGarmentAuthority", "note"):
                    e.append(f"clothingFitEvidence: unknown key {k}")
    elif isinstance(fit, dict):
        e.append("clothingFitEvidence is only meaningful for body-worn clothing")

    # ── product confidence honesty ───────────────────────────────────────────
    if pkg.get("productConfidence") not in ("HIGH", "MEDIUM", "LOW"):
        e.append(f"productConfidence {pkg.get('productConfidence')!r} not in vocabulary")
    if isinstance(pkg.get("knownUncertainties"), list) is False:
        e.append("knownUncertainties must be an array, even when empty")

    # ── QA requirements: all gates, no invented numbers ──────────────────────
    qa = pkg.get("qaRequirements")
    if not isinstance(qa, list):
        e.append("qaRequirements must be an array")
    else:
        seen = [q.get("gateId") for q in qa if isinstance(q, dict)]
        for g in GATES:
            if seen.count(g) != 1:
                e.append(f"QA gate {g} appears {seen.count(g)} times, must be exactly once")
        for extra in set(seen) - set(GATES):
            e.append(f"unknown QA gate {extra}")
        for q in qa:
            if not isinstance(q, dict):
                e.append("qaRequirements entry is not an object")
                continue
            gid = q.get("gateId")
            # An obligation, not an applicability result. A package that can set
            # this false can waive a constitutionally mandatory gate.
            if "mustEvaluateIfApplicable" not in q:
                e.append(f"QA gate {gid} does not register the obligation "
                         f"mustEvaluateIfApplicable")
            elif q.get("mustEvaluateIfApplicable") is not True:
                e.append(f"QA gate {gid} sets mustEvaluateIfApplicable "
                         f"{q.get('mustEvaluateIfApplicable')!r}; a package may not waive a gate")
            if "required" in q:
                e.append(f"QA gate {gid} carries the removed `required` field; a package may not "
                         f"decide that a gate does not apply")
            if q.get("numericThreshold") is not None:
                e.append(f"QA gate {gid} carries an invented numeric threshold "
                         f"{q.get('numericThreshold')!r}; contract 02 defines none")
            if NOT_APPLICABLE in str(q.values()):
                e.append(f"QA gate {gid} resolves applicability; NOT_APPLICABLE is decided after "
                         f"generation, not in the input package")
            for k in q:
                if k not in ("gateId", "mustEvaluateIfApplicable", "numericThreshold"):
                    e.append(f"QA gate {gid}: unknown key {k}")

    # ── truth constraints ────────────────────────────────────────────────────
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

    subs = pkg.get("humanSubjects")
    if not isinstance(subs, list):
        e.append("humanSubjects must be an array, even when empty")
    else:
        for s in subs:
            if s not in SUBJECTS:
                e.append(f"unknown human subject {s!r}")

    # ── execution layer is not an authority ──────────────────────────────────
    ex = pkg.get("executionLayer")
    if not isinstance(ex, dict):
        e.append("executionLayer must be an object")
    else:
        if ex.get("isAuthoritative") is not False:
            e.append("the execution layer is never authoritative")
        if "mayProduce" in ex and ex["mayProduce"] != ["GENERATED_OUTPUT"]:
            e.append("the execution layer may produce GENERATED_OUTPUT and nothing else")

    # ── nothing post-generation may appear in a pre-generation package ───────
    # The unknown-key sweep above already rejects these; naming them gives the
    # failure a reason rather than a shrug.
    for k in POST_GENERATION_KEYS:
        if k in pkg:
            e.append(f"{k} is post-generation state and cannot appear in a package assembled "
                     f"before generation")
    return e


def valid_package():
    """A package the contract must accept."""
    return {
        "schemaVersion": 1,
        "packageRef": "synthetic-fixture-1",
        "generatedAt": "2026-01-01",
        "isProductTruthRecord": False,
        "productIdentity": {
            "pmId": "PM-001", "manufacturerItemNumber": "SYNTHETIC-0001",
            "variant": "synthetic variant", "truthSource": "PRODUCT_ONBOARDING_SYSTEM",
            "mayBeWrittenByCreativeSystem": False, "similarSkuSubstituted": False,
        },
        "productRole": "HERO",
        "productGeometrySources": [{
            "sourceRef": "synthetic catalogue image", "derivesFromExactProduct": True,
            "isAvatarFrame": False, "isGenericCategoryImagery": False,
            "isDifferentColourway": False, "coversLockCategories": list(LOCKS),
        }],
        "productWearReference": {"referenceRef": "synthetic wear frame",
                                 "authoritativeForGeometry": False,
                                 "informsPlacementOnly": True},
        "productLocks": [{"lockId": l, "engaged": True} for l in LOCKS],
        "creativeFreedoms": ["environment", "lighting", "world physics"],
        "riskClassification": {"clothingWornOnBody": False, "riskLevel": "LOW"},
        "productConfidence": "HIGH",
        "knownUncertainties": [],
        "qaRequirements": [{"gateId": g, "mustEvaluateIfApplicable": True,
                            "numericThreshold": None} for g in GATES],
        "humanSubjects": [],
        "truthConstraints": {"productTruthMayBeTransformed": False,
                             "humanIdentityMayBeTransformed": False,
                             "worldPhysicsMayBreak": True},
        "executionLayer": {"provider": "SYNTHETIC_EXECUTION_LAYER", "isAuthoritative": False,
                           "mayProduce": ["GENERATED_OUTPUT"]},
    }


def clothing_package():
    """A body-worn clothing package the contract must accept."""
    p = json.loads(json.dumps(valid_package()))
    p["riskClassification"] = {"clothingWornOnBody": True, "riskLevel": "HIGH"}
    p["clothingFitEvidence"] = {"garmentGeometryEvidencePresent": True,
                                "wearFitEvidencePresent": True,
                                "avatarWardrobeUsedAsGarmentAuthority": False}
    return p


def mutate(fn, base=None):
    pkg = json.loads(json.dumps(base if base is not None else valid_package()))
    fn(pkg)
    return pkg


def main():
    print("PINK MALL — Product Creative Contract (02) validator\n")

    # ── A. documents and identity ────────────────────────────────────────────
    print("A. documents and identity")
    for path in (JSON_PATH, SCHEMA_PATH, OBJECT_PATH, MD_PATH, PARENT_PATH, DEP_PATH):
        if not os.path.exists(path):
            print(f"  FAIL  missing required file {os.path.basename(path)}")
            print("PRODUCT CREATIVE CONTRACT: FAIL (cannot continue)")
            sys.exit(1)
    try:
        c = load(JSON_PATH)
        schema = load(SCHEMA_PATH)
        obj = load(OBJECT_PATH)
        parent = load(PARENT_PATH)
        dep = load(DEP_PATH)
        check("1. contract, both schemas, parent and dependency all parse", True)
    except Exception as exc:
        check("1. contract, both schemas, parent and dependency all parse", False, str(exc))
        print("PRODUCT CREATIVE CONTRACT: FAIL (cannot continue)")
        sys.exit(1)
    with open(MD_PATH, encoding="utf-8") as fh:
        md = fh.read()
    # Emphasis markers must not be able to defeat a prose check.
    md_plain = " ".join(md.replace("*", "").replace("`", "").replace("_", " ").split())

    check("2. contractId is the expected id", c.get("contractId") == EXPECTED_CONTRACT_ID,
          str(c.get("contractId")))
    check("3. contractNumber is 02", c.get("contractNumber") == EXPECTED_NUMBER,
          str(c.get("contractNumber")))
    # Counting dots would call "foo.bar.baz" a semantic version, so apply the
    # pattern the schema specifies rather than a shape heuristic.
    check("4. version is a semantic version", bool(SEMVER.fullmatch(str(c.get("version", "")))),
          str(c.get("version")))
    check("    the schema expresses the same version rule",
          schema.get("properties", {}).get("version", {}).get("pattern") == SEMVER.pattern)
    check("    that pattern and this validator accept the same strings",
          all(bool(re.fullmatch(schema["properties"]["version"]["pattern"], v))
              == bool(SEMVER.fullmatch(v))
              for v in ("1.0.0", "foo.bar.baz", "1.0", "1.0.0.0", "v1.0.0", "1.0.x")))
    check("5. status is a declared provenance value",
          c.get("status") in ("CANDIDATE", "CANONICAL", "SUPERSEDED"), str(c.get("status")))
    check("6. parentContract is the System Authority Contract",
          c.get("parentContract") == EXPECTED_PARENT_ID, str(c.get("parentContract")))
    deps = {d.get("contractId"): d for d in c.get("dependsOn", [])}
    check("7. depends explicitly on the Campaign Context Contract",
          EXPECTED_DEP_ID in deps, str(sorted(deps)))
    check("    the dependency records contract 01's number", 
          deps.get(EXPECTED_DEP_ID, {}).get("contractNumber") == "01")
    check("8. the human-readable contract states the same id and version",
          c["contractId"] in md and c["version"] in md)
    check("9. inheritance forbids contradicting the parent",
          "MUST NOT contradict" in c.get("inheritance", ""))
    check("    inheritance states status is provenance, not permission",
          "provenance" in c.get("inheritance", "").lower())

    # ── B. reserved identity and non-duplication ─────────────────────────────
    print("\nB. registry position and non-duplication")
    slots = parent.get("contractSequence", {}).get("slots", [])
    slot = next((s for s in slots if s.get("contractNumber") == EXPECTED_NUMBER), None)
    check("10. contract 00 reserves slot 02 for this contract id",
          slot is not None and slot.get("contractId") == EXPECTED_CONTRACT_ID, str(slot))
    check("11. contract 00 was not bumped to accommodate contract 02",
          parent.get("version") == "1.0.1", str(parent.get("version")))
    check("12. contract 01 already anticipated this dependency",
          any(f.get("contractNumber") == "02" for f in dep.get("futureDependencies", [])))
    check("13. product roles are owned by contract 01, not redefined here",
          c.get("productRoleInteraction", {}).get("rolesOwnedBy") == EXPECTED_DEP_ID)
    dep_roles = [r.get("roleId") for r in dep.get("productRoles", [])]
    check("14. contract 01 still defines all four roles including NONE",
          set(dep_roles) == {"NONE", "DETAIL", "SUPPORTING", "HERO"}, str(dep_roles))
    check("15. HERO is not globally required",
          c.get("productRoleInteraction", {}).get("heroRequiredGlobally") is False
          and all(r.get("required") is False for r in dep.get("productRoles", [])))
    check("16. contract 02 applies at DETAIL, SUPPORTING and HERO",
          c.get("productRoleInteraction", {}).get("appliesWhenRoleIsAnyOf")
          == PRODUCT_ROLES_HERE)
    check("17. NONE remains valid because not every campaign is product-led",
          c.get("productRoleInteraction", {}).get("noneRemainsValid") is True)
    check("18. the media taxonomy is not redefined here",
          c.get("mediaClassBoundary", {}).get("redefinedHere") is False
          and c.get("mediaClassBoundary", {}).get("taxonomyOwnedBy") == EXPECTED_PARENT_ID)

    # ── C. the constitutional rules ──────────────────────────────────────────
    print("\nC. product and human truth")
    cp = c.get("corePrinciple", {})
    check("19. product truth may not be transformed",
          cp.get("productTruthMayBeTransformed") is False)
    check("20. human identity may not be transformed",
          cp.get("humanIdentityMayBeTransformed") is False)
    check("21. world physics may break", cp.get("worldPhysicsMayBreak") is True)
    check("    the core principle is inherited, not reinvented",
          "creativeFreedomPrinciple" in cp.get("inheritedFrom", ""))
    check("    it matches the parent's wording",
          cp.get("statement", "").strip().rstrip(".").lower()
          == parent.get("creativeFreedomPrinciple", {}).get("statement", "")
          .strip().rstrip(".").lower(),
          f"{cp.get('statement')!r}")

    pt = c.get("productTruthAuthority", {})
    check("22. a creative system may read Product Truth",
          pt.get("creativeSystemMayRead") is True)
    check("23. a creative system may NOT write Product Truth",
          pt.get("creativeSystemMayWrite") is False)
    check("24. a generated image is not evidence that Product Truth changed",
          pt.get("generatedImageIsEvidenceOfTruthChange") is False)
    owned = {o.get("fact") for o in pt.get("ownedElsewhere", [])}
    check("25. SKU, price, sizes, variant and canonical media stay owned elsewhere",
          len(owned) >= 5 and any("SKU" in o for o in owned)
          and any("price" in o for o in owned) and any("size" in o for o in owned)
          and any("variant" in o for o in owned) and any("media" in o for o in owned),
          str(sorted(owned)))
    check("26. the contract does not become a second product database",
          "MUST NOT become a second product database" in pt.get("rule", ""))

    pf = c.get("productFidelity", {})
    check("27. 1:1 fidelity is defined honestly, not as pixel identity",
          pf.get("isNotPixelIdentity") is True
          and "NOT mean" in pf.get("honestDefinition", ""))
    check("28. the generator receives no authority to redesign the product",
          "NO authority to redesign" in pf.get("honestDefinition", ""))
    keep = " ".join(pf.get("mustRemainTheSame", [])).lower()
    for term in ("sku", "variant", "silhouette", "geometry", "construction", "proportions",
                 "logo", "hardware"):
        check(f"    fidelity preserves {term}", term in keep)
    check("29. unestablished attributes must not be invented",
          "MUST NOT be invented" in pf.get("mustNotInvent", ""))
    check("30. the fidelity rule cites existing repository precedent",
          "03-media-policy" in pf.get("repositoryPrecedent", {}).get("source", ""))

    # ── D. evidence, locks, clothing, dual lock, execution ───────────────────
    print("\nD. evidence, locks and boundaries")
    roles = {r.get("roleId"): r for r in c.get("evidenceRoles", [])}
    check("31. productGeometrySource is authoritative for geometry",
          roles.get("productGeometrySource", {}).get("authoritativeForGeometry") is True)
    check("32. productGeometrySource must derive from the exact product",
          roles.get("productGeometrySource", {}).get("mustDeriveFromExactProduct") is True)
    check("33. productWearReference is NOT authoritative for geometry",
          roles.get("productWearReference", {}).get("authoritativeForGeometry") is False)
    check("34. the two evidence roles are distinct and both present",
          set(roles) == {"productGeometrySource", "productWearReference"}, str(sorted(roles)))
    never = " ".join(c.get("neverGeometryAuthority", [])).lower()
    for term in ("avatar", "generic", "similar", "colourway", "generated"):
        check(f"    {term} evidence is never geometry authority", term in never)

    lock_ids = [l.get("lockId") for l in c.get("productLockCategories", [])]
    check("35. all nine core product locks are present exactly once",
          all(lock_ids.count(l) == 1 for l in LOCKS) and len(lock_ids) == len(LOCKS),
          str(lock_ids))
    check("36. every core lock is marked core and unweakenable",
          all(l.get("core") is True and l.get("mayBeWeakenedByLaterContract") is False
              for l in c.get("productLockCategories", [])))
    check("37. a later contract may add locks but not weaken core ones",
          any("MUST NOT silently weaken" in r for r in c.get("productLockRules", [])))

    ce = c.get("creativeEnvelope", {})
    check("38. creative freedom applies to the world, product lock to the product",
          "WORLD" in ce.get("principle", "") and "PRODUCT" in ce.get("principle", ""))
    check("39. the world may transform", len(ce.get("mayTransform", [])) >= 10)
    check("40. the product itself may not be redesigned",
          "MUST NOT intentionally redesign" in ce.get("rule", ""))
    check("41. PINK MALL is not narrowed into one visual style",
          "MUST NOT be narrowed" in ce.get("styleIsNotNarrowed", ""))

    pc = c.get("productConfidence", {})
    check("42. product confidence is qualitative, not invented numeric scoring",
          pc.get("states") == ["HIGH", "MEDIUM", "LOW"]
          and pc.get("numericScoringDefined") is False)
    downs = {d.get("condition"): d.get("result") for d in pc.get("mandatoryDowngrades", [])}
    check("43. no geometry source means product confidence LOW",
          any("no productGeometrySource" in k and v == "LOW" for k, v in downs.items()))
    check("44. a similar SKU or different colourway is a STOP, not a downgrade",
          sum(1 for k, v in downs.items()
              if ("similar SKU" in k or "different colourway" in k) and v == "STOP") == 2,
          str(downs))
    check("45. an uncertain product is not reported as grounded",
          "MUST NOT be reported as fully grounded" in pc.get("honesty", ""))
    # LOW confidence describes grounding. It is not a licence to generate.
    gr = c.get("generationReadiness", {})
    check("    confidence is explicitly not permission to generate",
          pc.get("confidenceIsNotPermissionToGenerate") is True
          and "NOT permission to generate" in pc.get("rule", ""))
    check("    generation readiness is a separate judgement from confidence",
          gr.get("states") == ["READY", "BLOCKED"] and gr.get("distinctFromConfidence") is True)
    check("    no package may be emitted while readiness is BLOCKED",
          gr.get("packageMayBeEmittedWhenBlocked") is False)
    blocked = " ".join(gr.get("blockedWhen", [])).lower()
    for term in ("exact-product", "similar sku", "different colourway", "garment-geometry"):
        check(f"    readiness is BLOCKED when evidence is {term}", term in blocked)
    check("    Avatar v1.3's LOW-confidence mapping is preserved, not replaced",
          "productConfidence LOW" in gr.get("avatarCompatibility", "")
          and "preserved verbatim" in gr.get("avatarCompatibility", ""))

    hr = c.get("highRiskProductClasses", [])
    clothing = next((h for h in hr if h.get("classId") == "CLOTHING_WORN_ON_BODY"), None)
    check("46. clothing worn on a body is a HIGH-risk product class",
          clothing is not None and clothing.get("riskLevel") == "HIGH")
    check("47. preserved colour is not evidence of preserved geometry",
          clothing is not None and clothing.get("colourPreservationIsNotFidelity") is True)
    attrs = " ".join(clothing.get("silentlyChangeableAttributes", [])).lower() if clothing else ""
    for term in ("cut", "length", "neckline", "sleeve", "waist", "drape", "seams", "closures"):
        check(f"    clothing risk names {term}", term in attrs)
    check("48. a full per-category risk taxonomy is NOT invented here",
          any("MUST NOT" in r or "remain OPEN" in r for r in c.get("highRiskRules", [])))

    cf = c.get("clothingFitProtocol", {})
    kinds = {k.get("kindId"): k for k in cf.get("evidenceKinds", [])}
    check("49. the Clothing Fit Protocol exists and is not implemented",
          cf.get("protocolId") == "CLOTHING_FIT_PROTOCOL"
          and cf.get("implementationStatus") == "PLANNED")
    check("50. garment geometry evidence is authoritative and exact-product",
          kinds.get("GARMENT_GEOMETRY_EVIDENCE", {}).get("authoritativeForGarment") is True
          and kinds.get("GARMENT_GEOMETRY_EVIDENCE", {})
          .get("mustDeriveFromExactProduct") is True)
    check("51. wear/fit evidence is NOT garment authority",
          kinds.get("WEAR_FIT_EVIDENCE", {}).get("authoritativeForGarment") is False)
    fitrules = " ".join(cf.get("rules", [])).lower()
    check("52. body and avatar references are never garment-geometry authority",
          "avatar references are never garment-geometry authority" in fitrules)
    check("53. calibration-photograph wardrobe is never styling authority",
          "calibration-photograph wardrobe is never styling authority" in fitrules)
    check("54. a similar garment is not evidence for the real SKU",
          "similar garment is not evidence" in fitrules)
    check("55. fit evidence may inform but may not redesign the garment",
          "may inform" in fitrules and "must not redesign" in fitrules)
    check("56. absent fit evidence is declared, not invented",
          "declared rather than invented" in fitrules)
    check("57. fit outcomes are PASS / FAIL / UNRESOLVED",
          [o.get("outcomeId") for o in cf.get("outcomes", [])] == FIT_OUTCOMES)
    check("58. UNRESOLVED is never a silent PASS", cf.get("unresolvedIsNotPass") is True)
    check("59. the fit protocol invents no numeric thresholds",
          cf.get("numericThresholdsDefined") is False)
    check("60. the fit protocol cites the wardrobe-authority precedent",
          "WARDROBE_AUTHORITY" in cf.get("wardrobePrecedent", ""))

    dl = c.get("dualLock", {})
    check("61. human and product locks operate simultaneously",
          dl.get("operateSimultaneously") is True
          and dl.get("locks") == ["HUMAN_IDENTITY_LOCK", "PRODUCT_LOCK"])
    check("62. neither lock may be sacrificed for the other",
          dl.get("eitherMayBeSacrificed") is False)
    check("63. an unsatisfiable pair rejects the candidate",
          dl.get("onConflict") == "REJECT_CANDIDATE")
    forb = " ".join(dl.get("forbiddenResolutions", [])).lower()
    for term in ("sister", "product", "sku", "colourway", "simplifying"):
        check(f"    conflict may not be resolved by changing the {term}", term in forb)

    cons = c.get("consent", {})
    check("64. consent references the existing gate and does not resolve it",
          cons.get("resolvedHere") is False and "CONSENT_AND_PROVENANCE" in cons.get("authority", ""))
    check("65. internal validation and commercial publication are different",
          cons.get("internalValidationAndPublicationAreDifferent") is True)
    # Caching mutable authority state here is how a contract goes stale the
    # moment the owner resolves consent at its real authority.
    check("    consent state is NOT owned or cached by this contract",
          cons.get("stateOwnedHere") is False
          and cons.get("readCurrentStateFromAuthority") is True)
    check("    no consent state value is frozen into the contract",
          not any(isinstance(v, str) and "OWNER_CONFIRMATION_REQUIRED" in v
                  for v in cons.values()),
          str({k: v for k, v in cons.items()
               if isinstance(v, str) and "OWNER_CONFIRMATION_REQUIRED" in v}))
    check("    the consent authority file exists in this lineage",
          os.path.exists(os.path.join(ROOT, cons.get("authority", ""))),
          cons.get("authority"))

    gos = c.get("generatedOutputStatus", {})
    check("66. generated output starts as GENERATED_OUTPUT / CANDIDATE",
          gos.get("initialTruthClass") == "GENERATED_OUTPUT"
          and gos.get("initialState") == "CANDIDATE")
    check("67. generation success is not validation success",
          gos.get("generationSuccessIsValidationSuccess") is False)
    check("68. generated output is not fact, canonical media, approval or publication",
          gos.get("isNotOnGeneration")
          == ["FACT", "CANONICAL_PRODUCT_MEDIA", "APPROVAL", "PUBLISHED"])
    check("69. approval and publication states belong to contract 06",
          gos.get("statesOutsideThisContractBelongTo") == "06"
          and set(gos.get("statesOutsideThisContract", [])) == set(FORBIDDEN_STATES))
    check("70. contract 02 expresses no approved or published state",
          not (set(gos.get("allowedStates", [])) & set(FORBIDDEN_STATES)))

    mb = c.get("mediaClassBoundary", {})
    check("71. canonical commerce media may not be generatively altered",
          mb.get("canonicalCommerceMediaGenerativeAlterationAllowed") is False)
    check("72. campaign media cannot become canonical commerce media",
          mb.get("campaignMediaMayBecomeCanonicalCommerceMedia") is False)
    check("73. looking convincing does not promote media into Product Truth",
          mb.get("promotionOnConvincingAppearance") is False)
    pm = {m.get("classId"): m for m in parent.get("mediaClasses", [])}
    check("    this agrees with contract 00's own media rules",
          pm.get("CANONICAL_COMMERCE_MEDIA", {}).get("generativeAlterationAllowed") is False
          and pm.get("CAMPAIGN_MEDIA", {}).get("generativeAlterationAllowed") is True)

    gate_ids = [g.get("gateId") for g in c.get("qaGates", [])]
    check("74. all ten QA gates are present exactly once",
          all(gate_ids.count(g) == 1 for g in GATES) and len(gate_ids) == len(GATES),
          str(gate_ids))
    check("75. every gate returns PASS / FAIL / UNRESOLVED with no numeric threshold",
          all(g.get("resultVocabulary") == ["PASS", "FAIL", "UNRESOLVED"]
              and g.get("numericThreshold") is None for g in c.get("qaGates", [])))
    check("76. UNRESOLVED must not be recorded as PASS",
          any("MUST NOT be recorded as PASS" in r for r in c.get("qaRules", [])))
    qs = c.get("qaSemantics", {})
    check("    applicability and result are separate dimensions",
          qs.get("resultVocabulary") == ["PASS", "FAIL", "UNRESOLVED"]
          and qs.get("notApplicableMarker") == NOT_APPLICABLE)
    check("    NOT_APPLICABLE is not a fourth evaluation result",
          qs.get("notApplicableIsEvaluationResult") is False)
    check("    NOT_APPLICABLE is not in the result vocabulary",
          NOT_APPLICABLE not in qs.get("resultVocabulary", []))
    check("    an applicable gate may not be marked NOT_APPLICABLE to bypass it",
          "MUST NOT be marked NOT_APPLICABLE" in qs.get("mustNotBypass", ""))
    check("    the result vocabulary applies to a generated depiction",
          "depiction" in qs.get("appliesTo", "") and "after generation" in qs.get("appliesTo", ""))
    check("    every gate declares whether it can be NOT_APPLICABLE",
          all(isinstance(g.get("mayBeNotApplicable"), bool) for g in c.get("qaGates", [])))
    check("    every gate is registered for evaluation",
          qs.get("everyGateIsRegisteredForEvaluation") is True)
    check("    a pre-generation package may not waive a gate",
          qs.get("packageMayWaiveAGate") is False)
    check("    the obligation field is named and is not an applicability result",
          qs.get("evaluationObligationField") == "mustEvaluateIfApplicable"
          and qs.get("obligationIsNotAnApplicabilityResult") is True)
    check("    the obligation rule defers applicability to after generation",
          "after generation" in qs.get("obligationRule", "")
          and "MUST NOT waive" in qs.get("obligationRule", ""))
    check("    the conditional gates are the ones marked not-always-applicable",
          {g["gateId"] for g in c.get("qaGates", []) if g.get("mayBeNotApplicable")}
          >= {"CLOTHING_FIT_INTEGRITY", "HUMAN_TRUTH_INTEGRITY"})
    check("77. the contract defines no numeric threshold and says so",
          c.get("numericThresholdsDefinedHere") is False
          and "NOT promoted into this contract" in c.get("numericThresholdNote", ""))

    fail_ids = [f.get("failureId") for f in c.get("hardFailures", [])]
    check("78. all ten hard failures are present exactly once",
          all(fail_ids.count(f) == 1 for f in FAILURES) and len(fail_ids) == len(FAILURES),
          str(fail_ids))
    sev = {f.get("failureId"): f.get("severity") for f in c.get("hardFailures", [])}
    check("79. unresolved clothing fit and generator-claimed authority are STOPs",
          all(sev.get(f) == "STOP" for f in STOP_FAILURES), str(sev))
    check("80. every other named failure is a HARD_FAIL",
          all(sev.get(f) == "HARD_FAIL" for f in FAILURES if f not in STOP_FAILURES))

    rs = c.get("retrySemantics", {})
    check("81. a failed generation does not rewrite Product Truth",
          any("rewrite Product Truth" in x for x in rs.get("failedGenerationIsNot", [])))
    check("82. a failed generation does not weaken a Product Lock",
          any("weaken a Product Lock" in x for x in rs.get("failedGenerationIsNot", [])))
    check("83. a failure is not proof the canonical reference is wrong",
          any("canonical product reference is wrong" in x
              for x in rs.get("failedGenerationIsNot", [])))
    check("84. a retry preserves the same Product Truth",
          rs.get("retryPreservesProductTruth") is True)
    check("85. no credit ceiling is defined here; spend belongs to contract 06",
          rs.get("creditCeilingsDefinedHere") is False and rs.get("spendAuthority") == "06")
    check("    the retry rule cites the avatar-skill precedent",
          "failed generation is evidence" in rs.get("precedent", "").lower())

    el = c.get("executionLayer", {})
    check("86. the execution layer may not assert facts", el.get("mayAssertFacts") is False)
    check("87. it produces GENERATED_OUTPUT and nothing else",
          el.get("mayProduce") == ["GENERATED_OUTPUT"])
    notauth = " ".join(el.get("mustNotBeAuthoritativeFor", [])).lower()
    for term in ("product identity", "product geometry", "product truth", "human truth",
                 "approvals", "publication"):
        check(f"    it is not authority for {term}", term in notauth)
    # Whether a provider was called in one authoring session is an operational
    # fact about that session, not durable policy, and belongs in its report.
    check("88. the contract carries no phase-execution audit facts",
          not any(k in el for k in ("calledInThisPhase", "creditsSpent",
                                    "subscriptionAssumed", "apiAssumed")),
          str([k for k in ("calledInThisPhase", "creditsSpent", "subscriptionAssumed",
                           "apiAssumed") if k in el]))
    check("    the contract's validity assumes no subscription",
          el.get("contractAssumesSubscription") is False)
    check("    the contract's validity assumes no specific API",
          el.get("contractAssumesSpecificApi") is False)
    check("    the authority boundary holds whether or not a provider is connected",
          el.get("contractValidityDependsOnProvider") is False
          and "whether or not a provider is connected" in el.get("rule", ""))
    check("    contract 00 agrees the studio may not assert facts",
          next((s for s in parent.get("sourceTypes", [])
                if s.get("sourceId") == "CYBERNINJAS_STUDIO"), {}).get("mayAssertFacts") is False)

    ag = c.get("authorityGrants", {})
    check("89. no publication authority is granted",
          ag.get("publicationAuthorityGranted") is False)
    check("90. no spend authority is granted", ag.get("spendAuthorityGranted") is False)
    check("91. no approval authority is granted", ag.get("approvalAuthorityGranted") is False)
    check("92. no Product-Truth write authority is granted",
          ag.get("productTruthWriteAuthorityGranted") is False)

    prp = c.get("productReferencePackage", {})
    check("93. the reference package is a generation input, not a truth record",
          prp.get("isGenerationInput") is True and prp.get("isProductTruthRecord") is False)
    check("94. its builder is not implemented and instances are not committed",
          prp.get("builderImplemented") is False and prp.get("committed") is False)
    check("95. no Product Creative Engine exists",
          c.get("scope", {}).get("implementationStatus") == "PLANNED"
          and "No Product Creative Engine exists" in c.get("scope", {}).get("note", ""))

    priv = " ".join(c.get("privacyRules", []))
    check("96. the contract states this repository is PUBLIC", "PUBLIC" in priv)
    check("97. credentials and provider tokens must not be committed",
          "Credentials" in priv and "token" in priv.lower())
    check("98. PINK-MALL-OPS remains PLANNED and must not be created",
          "PINK-MALL-OPS" in priv and "MUST NOT be created" in priv)
    check("99. open items are declared undecided and may not be invented",
          len(c.get("openItems", [])) >= 13
          and "MUST NOT be answered by invention" in c.get("openItemsRule", ""))
    opens = " ".join(c.get("openItems", [])).lower()
    for term in ("numeric geometry tolerances", "numeric colour tolerances",
                 "computer-vision qa method", "per-category risk taxonomy",
                 "automatic retry policy", "clothing fit implementation"):
        check(f"    still open: {term}", term in opens)

    # ── E. the schemas structurally ENCODE these rules ───────────────────────
    print("\nE. schema structure (read from the schema documents, not their prose)")

    def _rules(node, key):
        """allOf entries whose `contains` pins `key` to a const, split by shape.

        An identity rule constrains the key alone and carries min=max=1, proving
        the id appears exactly once. A binding rule additionally pins a second
        field and carries minContains only: paired with the identity rule it
        proves THE one record with that id carries that value. maxContains on a
        binding rule would be weaker, not stronger, because a non-matching
        duplicate would satisfy it.
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

    sp = schema.get("properties", {})
    check("100. contract schema is closed to unknown top-level keys",
          schema.get("additionalProperties") is False)
    check("101. contract schema requires every governed key",
          set(sp) == set(schema.get("required", [])) and set(sp) == set(c),
          f"schema-only={sorted(set(sp) - set(c))} contract-only={sorted(set(c) - set(sp))}")
    ok, d = exactly_once(sp.get("productLockCategories", {}), "lockId", LOCKS)
    check("102. contract schema requires each product lock exactly once", ok, d)
    ok, d = binds(sp.get("productLockCategories", {}), "lockId", "core",
                  {l: True for l in LOCKS})
    check("    contract schema pins every lock as core", ok, d)
    ok, d = binds(sp.get("productLockCategories", {}), "lockId",
                  "mayBeWeakenedByLaterContract", {l: False for l in LOCKS})
    check("    contract schema forbids weakening any core lock", ok, d)
    ok, d = exactly_once(sp.get("qaGates", {}), "gateId", GATES)
    check("103. contract schema requires each QA gate exactly once", ok, d)
    ok, d = exactly_once(sp.get("hardFailures", {}), "failureId", FAILURES)
    check("104. contract schema requires each hard failure exactly once", ok, d)
    ok, d = binds(sp.get("hardFailures", {}), "failureId", "severity",
                  {f: ("STOP" if f in STOP_FAILURES else "HARD_FAIL") for f in FAILURES})
    check("    contract schema pins each failure's severity", ok, d)
    ok, d = exactly_once(sp.get("evidenceRoles", {}), "roleId",
                         ["productGeometrySource", "productWearReference"])
    check("105. contract schema requires both evidence roles exactly once", ok, d)
    ok, d = binds(sp.get("evidenceRoles", {}), "roleId", "authoritativeForGeometry",
                  {"productGeometrySource": True, "productWearReference": False})
    check("    contract schema pins which role is geometry authority", ok, d)
    ok, d = binds(sp.get("evidenceRoles", {}), "roleId", "mustDeriveFromExactProduct",
                  {"productGeometrySource": True, "productWearReference": False})
    check("    contract schema pins which role must be the exact product", ok, d)
    cfp = sp.get("clothingFitProtocol", {}).get("properties", {})
    ok, d = binds(cfp.get("evidenceKinds", {}), "kindId", "authoritativeForGarment",
                  {"GARMENT_GEOMETRY_EVIDENCE": True, "WEAR_FIT_EVIDENCE": False})
    check("106. contract schema pins garment-geometry authority", ok, d)
    ok, d = exactly_once(cfp.get("outcomes", {}), "outcomeId", FIT_OUTCOMES)
    check("    contract schema requires all three fit outcomes exactly once", ok, d)
    check("    contract schema pins UNRESOLVED as never a PASS",
          cfp.get("unresolvedIsNotPass", {}).get("const") is True)
    ok, d = binds(sp.get("highRiskProductClasses", {}), "classId", "riskLevel",
                  {"CLOTHING_WORN_ON_BODY": "HIGH"})
    check("107. contract schema pins body-worn clothing as HIGH risk", ok, d)
    for key, sub, want in (("corePrinciple", "productTruthMayBeTransformed", False),
                           ("corePrinciple", "humanIdentityMayBeTransformed", False),
                           ("corePrinciple", "worldPhysicsMayBreak", True),
                           ("productTruthAuthority", "creativeSystemMayWrite", False),
                           ("productTruthAuthority", "generatedImageIsEvidenceOfTruthChange", False),
                           ("mediaClassBoundary", "canonicalCommerceMediaGenerativeAlterationAllowed", False),
                           ("mediaClassBoundary", "campaignMediaMayBecomeCanonicalCommerceMedia", False),
                           ("executionLayer", "mayAssertFacts", False),
                           ("executionLayer", "contractAssumesSubscription", False),
                           ("executionLayer", "contractAssumesSpecificApi", False),
                           ("executionLayer", "contractValidityDependsOnProvider", False),
                           ("consent", "stateOwnedHere", False),
                           ("consent", "readCurrentStateFromAuthority", True),
                           ("qaSemantics", "notApplicableIsEvaluationResult", False),
                           ("qaSemantics", "everyGateIsRegisteredForEvaluation", True),
                           ("qaSemantics", "packageMayWaiveAGate", False),
                           ("qaSemantics", "obligationIsNotAnApplicabilityResult", True),
                           ("generationReadiness", "distinctFromConfidence", True),
                           ("generationReadiness", "packageMayBeEmittedWhenBlocked", False),
                           ("productConfidence", "confidenceIsNotPermissionToGenerate", True),
                           ("authorityGrants", "publicationAuthorityGranted", False),
                           ("authorityGrants", "spendAuthorityGranted", False),
                           ("productConfidence", "numericScoringDefined", False),
                           ("productRoleInteraction", "heroRequiredGlobally", False),
                           ("productRoleInteraction", "noneRemainsValid", True)):
        check(f"    contract schema pins {key}.{sub} = {want}",
              sp.get(key, {}).get("properties", {}).get(sub, {}).get("const") is want)
    # Closing consent is the mechanism that keeps a cached consent state out;
    # an open object would let one back in with every const still satisfied.
    check("    contract schema closes the consent object",
          sp.get("consent", {}).get("additionalProperties") is False)
    check("    contract schema declares no consent-state property",
          not any("state" in k.lower() and k not in
                  ("stateOwnedHere", "readCurrentStateFromAuthority")
                  for k in sp.get("consent", {}).get("properties", {})),
          str(sorted(sp.get("consent", {}).get("properties", {}))))
    # Every governed sub-object must be closed for the same reason.
    open_objs = [k for k, v in sp.items()
                 if isinstance(v, dict) and v.get("type") == "object"
                 and v.get("additionalProperties") is not False]
    check("    every governed contract sub-object is closed", not open_objs, str(open_objs))
    check("108. contract schema pins the contract-02 number and parent",
          sp.get("contractNumber", {}).get("const") == "02"
          and sp.get("parentContract", {}).get("const") == EXPECTED_PARENT_ID)
    ok, d = exactly_once(sp.get("dependsOn", {}), "contractId", [EXPECTED_DEP_ID])
    check("    contract schema requires the contract-01 dependency exactly once", ok, d)

    op = obj.get("properties", {})
    check("109. object schema is closed to unknown top-level keys",
          obj.get("additionalProperties") is False)
    open_items = [k for k, v in op.items()
                  if isinstance(v, dict) and v.get("type") == "object"
                  and v.get("additionalProperties") is not False]
    check("    every governed package sub-object is closed", not open_items, str(open_items))

    ok, d = exactly_once(op.get("productLocks", {}), "lockId", LOCKS)
    check("110. object schema requires each product lock exactly once", ok, d)
    ok, d = binds(op.get("productLocks", {}), "lockId", "engaged", {l: True for l in LOCKS})
    check("    object schema requires every lock to be engaged", ok, d)
    ok, d = exactly_once(op.get("qaRequirements", {}), "gateId", GATES)
    check("111. object schema requires each QA gate exactly once", ok, d)
    ok, d = binds(op.get("qaRequirements", {}), "gateId", "numericThreshold",
                  {g: None for g in GATES})
    check("    object schema pins every QA threshold to null", ok, d)
    # A free boolean here would let a package waive a mandatory gate while every
    # other rule still passed.
    ok, d = binds(op.get("qaRequirements", {}), "gateId", "mustEvaluateIfApplicable",
                  {g: True for g in GATES})
    check("    object schema pins the evaluation obligation on every gate", ok, d)
    qa_item = op.get("qaRequirements", {}).get("items", {})
    qa_props = qa_item.get("properties", {})
    check("    object schema states the obligation as a const, not a free boolean",
          qa_props.get("mustEvaluateIfApplicable", {}).get("const") is True
          and "type" not in qa_props.get("mustEvaluateIfApplicable", {}))
    check("    object schema requires the obligation on every QA record",
          {"gateId", "mustEvaluateIfApplicable", "numericThreshold"}
          == set(qa_item.get("required", [])), str(qa_item.get("required")))
    check("    object schema no longer carries the waivable `required` field",
          "required" not in qa_props, str(sorted(qa_props)))
    check("    object schema closes the QA record",
          qa_item.get("additionalProperties") is False)
    # Test what the schema ADMITS, not what its prose mentions: a description
    # explaining that NOT_APPLICABLE belongs elsewhere must not trip this.
    def _admits(node, token):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ("description", "$comment", "title"):
                    continue
                if k in ("const", "enum", "required", "default") and token in json.dumps(v):
                    return True
                if _admits(v, token):
                    return True
        elif isinstance(node, list):
            return any(_admits(x, token) for x in node)
        return False

    check("    the package schema admits no NOT_APPLICABLE value",
          not _admits(op, NOT_APPLICABLE),
          "applicability is resolved after generation, not in the input package")
    check("    the package schema admits no QA result value",
          not any(_admits(op, v) for v in FIT_OUTCOMES),
          "PASS/FAIL/UNRESOLVED are outcomes about a depiction, not properties of its inputs")
    check("    the contract still owns applicability via mayBeNotApplicable",
          all("mayBeNotApplicable" in g for g in c.get("qaGates", [])))
    gsrc = op.get("productGeometrySources", {})
    gprops = gsrc.get("items", {}).get("properties", {})
    check("112. object schema requires at least one geometry source",
          gsrc.get("minItems") == 1)
    check("    object schema requires it to derive from the exact product",
          gprops.get("derivesFromExactProduct", {}).get("const") is True)
    check("    object schema forbids an avatar frame as geometry",
          gprops.get("isAvatarFrame", {}).get("const") is False)
    check("    object schema forbids generic imagery as geometry",
          gprops.get("isGenericCategoryImagery", {}).get("const") is False)
    check("    object schema forbids a different colourway as geometry",
          gprops.get("isDifferentColourway", {}).get("const") is False)
    pid_props = op.get("productIdentity", {}).get("properties", {})
    check("113. object schema requires an exact SKU and variant",
          {"pmId", "manufacturerItemNumber", "variant"}
          <= set(op.get("productIdentity", {}).get("required", [])))
    check("    object schema pins the PM id format",
          pid_props.get("pmId", {}).get("pattern") == r"^PM-\d{3}$")
    check("    object schema forbids the creative system writing truth",
          pid_props.get("mayBeWrittenByCreativeSystem", {}).get("const") is False)
    check("114. object schema excludes role NONE from a package",
          op.get("productRole", {}).get("enum") == PRODUCT_ROLES_HERE)
    # ── body-worn clothing: every rule the checker enforces, proved present ──
    bw = [r for r in obj.get("allOf", [])
          if r.get("if", {}).get("properties", {}).get("riskClassification", {})
          .get("properties", {}).get("clothingWornOnBody", {}).get("const") is True]
    then = bw[0].get("then", {}) if bw else {}
    then_props = then.get("properties", {})
    check("115. object schema conditions on body-worn clothing at all", bool(bw))
    check("    object schema binds body-worn clothing to riskLevel HIGH",
          then_props.get("riskClassification", {}).get("properties", {})
          .get("riskLevel", {}).get("const") == "HIGH")
    check("    object schema requires the pre-generation fit-evidence object",
          "clothingFitEvidence" in then.get("required", []))
    check("    object schema requires garment geometry evidence",
          then_props.get("clothingFitEvidence", {}).get("properties", {})
          .get("garmentGeometryEvidencePresent", {}).get("const") is True
          and "garmentGeometryEvidencePresent"
          in then_props.get("clothingFitEvidence", {}).get("required", []))
    check("    object schema forbids avatar wardrobe becoming garment authority",
          then_props.get("clothingFitEvidence", {}).get("properties", {})
          .get("avatarWardrobeUsedAsGarmentAuthority", {}).get("const") is False)
    # Both directions, or the parity claim is false. The checker rejects fit
    # evidence on a non-clothing package, so the schema must forbid it too.
    els = bw[0].get("else", {}) if bw else {}
    check("    object schema FORBIDS fit evidence when clothing is not body-worn",
          "clothingFitEvidence" in els.get("not", {}).get("required", []),
          str(els))
    check("    the body-worn rule encodes both branches, not only the true half",
          bool(bw) and "then" in bw[0] and "else" in bw[0],
          str([k for k in (bw[0] if bw else {}) if k in ("if", "then", "else")]))
    cfe = op.get("clothingFitEvidence", {})
    cfo = cfe.get("properties", {})
    check("    object schema pins avatar wardrobe false on the evidence object itself",
          cfo.get("avatarWardrobeUsedAsGarmentAuthority", {}).get("const") is False)
    check("    object schema states wear/fit evidence as a boolean, not a verdict",
          cfo.get("wearFitEvidencePresent", {}).get("type") == "boolean")
    # ── no post-generation vocabulary may enter a pre-generation package ─────
    check("116. object schema carries no clothing-fit RESULT in the input package",
          "fitStatus" not in cfo and not any("fitStatus" in str(v) for v in cfo.values()),
          str(sorted(cfo)))
    check("    the fit-evidence object is closed, which is what keeps fitStatus out",
          cfe.get("additionalProperties") is False)
    check("117. object schema carries no generated-output status",
          "outputStatus" not in op and "outputStatus" not in obj.get("required", []))
    check("    the package is closed, which is what keeps outputStatus out",
          obj.get("additionalProperties") is False)
    check("    the schema names what may not appear in a pre-generation package",
          set(obj.get("x-notPermittedInPackage", {})) >= {"outputStatus", "fitStatus"})
    check("    PASS/FAIL/UNRESOLVED appear nowhere in the package schema properties",
          not any(v in json.dumps(op) for v in ("\"PASS\"", "\"FAIL\"", "\"UNRESOLVED\"")))
    # The normative contract must still own the post-generation vocabulary.
    check("118. the normative contract still defines the generated-output states",
          c.get("generatedOutputStatus", {}).get("initialTruthClass") == "GENERATED_OUTPUT"
          and c.get("generatedOutputStatus", {}).get("allowedStates") == OUTPUT_STATES)
    check("119. the normative Clothing Fit Protocol still owns PASS/FAIL/UNRESOLVED",
          [o.get("outcomeId") for o in c.get("clothingFitProtocol", {}).get("outcomes", [])]
          == FIT_OUTCOMES)
    check("    approval and publication states remain outside contract 02",
          not (set(c.get("generatedOutputStatus", {}).get("allowedStates", []))
               & set(FORBIDDEN_STATES)))
    tco = op.get("truthConstraints", {}).get("properties", {})
    check("116. object schema pins product truth untransformable",
          tco.get("productTruthMayBeTransformed", {}).get("const") is False)
    check("117. object schema pins human identity untransformable",
          tco.get("humanIdentityMayBeTransformed", {}).get("const") is False)
    check("    object schema permits world physics to break",
          tco.get("worldPhysicsMayBreak", {}).get("const") is True)
    check("120. object schema records the states contract 02 may not express",
          obj.get("x-notPermittedStates") == FORBIDDEN_STATES)
    check("121. object schema pins the execution layer non-authoritative",
          op.get("executionLayer", {}).get("properties", {})
          .get("isAuthoritative", {}).get("const") is False)
    check("122. object schema pins the package as not a truth record",
          op.get("isProductTruthRecord", {}).get("const") is False)
    check("    object schema records that it defines no numeric threshold",
          obj.get("x-numericThresholdsDefined") is False)
    check("    object schema records the states contract 02 may not express",
          obj.get("x-notPermittedStates") == FORBIDDEN_STATES)

    # ── F. synthetic runtime fixtures (targeted semantic checker) ────────────
    print("\nF. synthetic runtime fixtures — targeted semantic checker, NOT a JSON Schema engine")
    errs = check_package(valid_package())
    check("123. a valid exact-product handoff is ACCEPTED", not errs, str(errs[:4]))
    cerrs = check_package(clothing_package())
    check("124. a body-worn clothing handoff with fit evidence is ACCEPTED",
          not cerrs, str(cerrs[:4]))

    def rejects(label, fn, needle=None, base=None):
        e = check_package(mutate(fn, base))
        ok = bool(e) and (needle is None or any(needle in x for x in e))
        check(label, ok, f"errors={e[:3]}")

    rejects("125. a wrong SKU (unnamed item number) is REJECTED",
            lambda p: p["productIdentity"].__setitem__("manufacturerItemNumber", ""),
            "manufacturerItemNumber")
    rejects("126. a substituted similar SKU is REJECTED",
            lambda p: p["productIdentity"].__setitem__("similarSkuSubstituted", True),
            "WRONG_PRODUCT")
    rejects("127. a wrong variant (unnamed) is REJECTED",
            lambda p: p["productIdentity"].__setitem__("variant", ""), "variant is required")
    rejects("128. a malformed PM id is REJECTED",
            lambda p: p["productIdentity"].__setitem__("pmId", "SKU-1"), "PM-NNN")
    rejects("129. an absent productGeometrySource for a product-led case is REJECTED",
            lambda p: p.__setitem__("productGeometrySources", []), "at least one exact-product")
    rejects("130. geometry evidence not from the exact product is REJECTED",
            lambda p: p["productGeometrySources"][0]
            .__setitem__("derivesFromExactProduct", False), "exact product")
    rejects("131. an avatar frame used as geometry authority is REJECTED",
            lambda p: p["productGeometrySources"][0].__setitem__("isAvatarFrame", True),
            "avatar frame is never")
    rejects("132. generic category imagery as geometry authority is REJECTED",
            lambda p: p["productGeometrySources"][0]
            .__setitem__("isGenericCategoryImagery", True), "generic category imagery")
    rejects("133. a different colourway as geometry authority is REJECTED",
            lambda p: p["productGeometrySources"][0]
            .__setitem__("isDifferentColourway", True), "different colourway")
    rejects("134. a wear reference claiming geometry authority is REJECTED",
            lambda p: p["productWearReference"]
            .__setitem__("authoritativeForGeometry", True), "wear reference is never")
    rejects("135. an omitted GEOMETRY lock is REJECTED",
            lambda p: p.__setitem__("productLocks",
                                    [l for l in p["productLocks"] if l["lockId"] != "GEOMETRY"]),
            "GEOMETRY is omitted")
    rejects("    an omitted VARIANT lock is REJECTED",
            lambda p: p.__setitem__("productLocks",
                                    [l for l in p["productLocks"] if l["lockId"] != "VARIANT"]),
            "VARIANT is omitted")
    rejects("    a disengaged lock is REJECTED",
            lambda p: p["productLocks"][4].__setitem__("engaged", False), "not engaged")
    rejects("136. an outputStatus field in a PRE-GENERATION package is REJECTED",
            lambda p: p.__setitem__("outputStatus",
                                    {"truthClass": "GENERATED_OUTPUT", "state": "CANDIDATE",
                                     "mediaClass": "CAMPAIGN_MEDIA"}),
            "post-generation state")
    rejects("    generated media marked canonical commerce media is REJECTED, as an "
            "outputStatus field that cannot be here at all",
            lambda p: p.__setitem__("outputStatus",
                                    {"mediaClass": "CANONICAL_COMMERCE_MEDIA"}),
            "post-generation state")
    rejects("137. an execution layer marked authoritative is REJECTED",
            lambda p: p["executionLayer"].__setitem__("isAuthoritative", True),
            "never authoritative")
    rejects("    an execution layer claiming to produce facts is REJECTED",
            lambda p: p["executionLayer"].__setitem__("mayProduce", ["FACT"]),
            "GENERATED_OUTPUT and nothing else")
    rejects("138. product truth marked transformable is REJECTED",
            lambda p: p["truthConstraints"]
            .__setitem__("productTruthMayBeTransformed", True), "productTruthMayBeTransformed")
    rejects("139. human truth marked transformable is REJECTED",
            lambda p: p["truthConstraints"]
            .__setitem__("humanIdentityMayBeTransformed", True),
            "humanIdentityMayBeTransformed")
    rejects("140. body-worn clothing without fit evidence is REJECTED",
            lambda p: p.pop("clothingFitEvidence"), "requires clothingFitEvidence",
            base=clothing_package())
    rejects("    body-worn clothing without garment geometry evidence is REJECTED",
            lambda p: p["clothingFitEvidence"]
            .__setitem__("garmentGeometryEvidencePresent", False),
            "requires garment geometry evidence", base=clothing_package())
    rejects("    body-worn clothing not classified HIGH risk is REJECTED",
            lambda p: p["riskClassification"].__setitem__("riskLevel", "LOW"),
            "HIGH-risk", base=clothing_package())
    rejects("141. avatar wardrobe used as garment geometry authority is REJECTED",
            lambda p: p["clothingFitEvidence"]
            .__setitem__("avatarWardrobeUsedAsGarmentAuthority", True),
            "avatar wardrobe is never", base=clothing_package())
    rejects("    fit evidence on a NON-body-worn package is REJECTED",
            lambda p: p.__setitem__("clothingFitEvidence",
                                    {"garmentGeometryEvidencePresent": True,
                                     "wearFitEvidencePresent": True,
                                     "avatarWardrobeUsedAsGarmentAuthority": False}),
            "only meaningful for body-worn")
    rejects("142. an unsupported numeric QA threshold is REJECTED",
            lambda p: p["qaRequirements"][3].__setitem__("numericThreshold", 8),
            "invented numeric threshold")
    gi = {g: i for i, g in enumerate(GATES)}
    rejects("    waiving PRODUCT_IDENTITY evaluation is REJECTED",
            lambda p: p["qaRequirements"][gi["PRODUCT_IDENTITY"]]
            .__setitem__("mustEvaluateIfApplicable", False), "may not waive a gate")
    rejects("    waiving CLOTHING_FIT_INTEGRITY evaluation is REJECTED",
            lambda p: p["qaRequirements"][gi["CLOTHING_FIT_INTEGRITY"]]
            .__setitem__("mustEvaluateIfApplicable", False), "may not waive a gate")
    rejects("    waiving GEOMETRY_CONSTRUCTION evaluation is REJECTED",
            lambda p: p["qaRequirements"][gi["GEOMETRY_CONSTRUCTION"]]
            .__setitem__("mustEvaluateIfApplicable", False), "may not waive a gate")
    rejects("    an omitted evaluation obligation is REJECTED",
            lambda p: p["qaRequirements"][0].pop("mustEvaluateIfApplicable"),
            "does not register the obligation")
    rejects("    the removed `required` field reintroduced is REJECTED",
            lambda p: p["qaRequirements"][2].__setitem__("required", False),
            "removed `required` field")
    rejects("    NOT_APPLICABLE resolved inside the package is REJECTED",
            lambda p: p["qaRequirements"][5].__setitem__("numericThreshold", "NOT_APPLICABLE"),
            "resolves applicability")
    rejects("    a duplicated QA gate is REJECTED",
            lambda p: p["qaRequirements"].append(
                json.loads(json.dumps(p["qaRequirements"][0]))), "must be exactly once")
    rejects("    an unknown QA record key is REJECTED",
            lambda p: p["qaRequirements"][1].__setitem__("skipBecauseSlow", True),
            "unknown key skipBecauseSlow")
    rejects("143. a PUBLISHED state in the package is REJECTED",
            lambda p: p.__setitem__("outputStatus", {"state": "PUBLISHED"}),
            "post-generation state")
    rejects("    an APPROVED_SPEND state is REJECTED",
            lambda p: p.__setitem__("outputStatus", {"state": "APPROVED_SPEND"}),
            "post-generation state")
    rejects("    a clothingFit RESULT object in the package is REJECTED",
            lambda p: p.__setitem__("clothingFit", {"fitStatus": "PASS"}),
            "post-generation state")
    rejects("    a bare fitStatus in the package is REJECTED",
            lambda p: p.__setitem__("fitStatus", "PASS"), "post-generation state")
    rejects("    a fitStatus smuggled into the evidence object is REJECTED",
            lambda p: p["clothingFitEvidence"].__setitem__("fitStatus", "PASS"),
            "unknown key fitStatus", base=clothing_package())
    rejects("144. a package claiming to be a Product Truth record is REJECTED",
            lambda p: p.__setitem__("isProductTruthRecord", True), "generation input")
    rejects("    a creative system claiming truth-write authority is REJECTED",
            lambda p: p["productIdentity"]
            .__setitem__("mayBeWrittenByCreativeSystem", True), "never write Product Truth")
    rejects("145. an omitted QA gate is REJECTED",
            lambda p: p.__setitem__("qaRequirements",
                                    [q for q in p["qaRequirements"]
                                     if q["gateId"] != "HUMAN_TRUTH_INTEGRITY"]),
            "HUMAN_TRUTH_INTEGRITY")
    rejects("146. product role NONE in a package is REJECTED",
            lambda p: p.__setitem__("productRole", "NONE"), "productRole")
    rejects("147. an unknown top-level key is REJECTED",
            lambda p: p.__setitem__("autoPublish", True), "autoPublish")
    rejects("    an unknown human subject is REJECTED",
            lambda p: p.__setitem__("humanSubjects", ["MOTHER"]), "unknown human subject")
    check("148. a DUO package with both locks is ACCEPTED",
          not check_package(mutate(lambda p: p.__setitem__("humanSubjects", ["DUO"]))))
    check("    a DETAIL-role package is ACCEPTED",
          not check_package(mutate(lambda p: p.__setitem__("productRole", "DETAIL"))))
    check("149. the accepted fixture uses only keys the object schema declares",
          set(valid_package()) <= set(op), str(set(valid_package()) - set(op)))
    check("    the clothing fixture uses only keys the object schema declares",
          set(clothing_package()) <= set(op))
    check("    a generation-ready package with no geometry source is REJECTED",
          bool(check_package(mutate(lambda p: p.__setitem__("productGeometrySources", [])))),
          "readiness must be BLOCKED without exact-product geometry evidence")

    # ── G. registry bookkeeping ──────────────────────────────────────────────
    print("\nG. registry bookkeeping")
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, encoding="utf-8") as fh:
            index = fh.read()
        # Emphasis markers and line wrapping must not defeat a prose check.
        index_plain = " ".join(index.replace("*", "").replace("`", "").split()).lower()
        marker = "## Planned contracts"
        head, _, tail = index.partition(marker)
        above = [ln for ln in head.splitlines() if ln.strip().startswith("| 02 ")]
        below = [ln for ln in tail.splitlines() if ln.strip().startswith("| 02 ")]
        check("150. the index lists contract 02 in its current set",
              len(above) == 1 and "PRODUCT_CREATIVE" in above[0].upper(), str(above))
        check("151. the index no longer lists 02 as NOT YET CREATED",
              bool(marker in index) and not below, str(below))
        check("    contracts 00 and 01 remain in the current set",
              all(any(ln.strip().startswith(f"| 0{i} ") for ln in head.splitlines())
                  for i in (0, 1)))
        # This once read "contracts 03-08 remain NOT YET CREATED" over a
        # hard-coded range(3, 9). That was true before contract 03 existed and
        # was guaranteed to fail the moment it did. The durable rule is that the
        # index's current/planned split agrees with which contract files are
        # actually on disk, so the check can never become the stale thing it
        # exists to catch.
        misplaced = []
        for i in range(3, 9):
            num = f"0{i}"
            in_current = any(ln.strip().startswith(f"| {num} ") for ln in head.splitlines())
            in_planned = any(ln.strip().startswith(f"| {num} ") for ln in tail.splitlines())
            exists = bool(glob.glob(os.path.join(CDIR, f"{num}_*_CONTRACT.json")))
            if exists and not (in_current and not in_planned):
                misplaced.append(f"{num}: files exist but index has it "
                                 f"current={in_current} planned={in_planned}")
            if not exists and not (in_planned and not in_current):
                misplaced.append(f"{num}: no files but index has it "
                                 f"current={in_current} planned={in_planned}")
        check("152. the index's current/planned split matches which contract files exist",
              not misplaced, str(misplaced))
        check("    the index names the contract-02 validator",
              "product_creative_contract.py" in index)
        check("    the index does not treat file existence as canonicality",
              "existence does not make it canonical" in index.lower()
              or "does not assert" in index.lower())
        check("    the index records that no Product Creative Engine exists",
              "product creative engine" in index_plain
              and "does not exist" in index_plain)
        check("    the index states product onboarding authority is unchanged",
              "may read product truth" in index_plain
              and "never write it" in index_plain)
    else:
        check("150. the contract index exists", False, INDEX_PATH)

    if os.path.exists(MATRIX_PATH):
        with open(MATRIX_PATH, encoding="utf-8") as fh:
            matrix = fh.read()
        mlow = matrix.lower()
        check("153. the matrix records the Product Creative row",
              "product creative" in mlow)
        check("154. the matrix defers canonicality to the four conditions",
              "four conditions" in mlow and "not a canonicality test" in mlow)
        check("    the matrix preserves all eight locked interview domains",
              all(f"### {i}." in matrix for i in range(1, 9)),
              str([i for i in range(1, 9) if f"### {i}." not in matrix]))
        check("    the matrix still keeps the three states apart",
              "awaiting canonical contract" in mlow and "genuinely open" in mlow)

        # A global "still awaiting" statement that contradicts a per-domain row
        # is how a reader who scrolls least far gets the wrong answer. The
        # expectation is derived from which contract files actually exist, so
        # this guard never becomes the stale thing it exists to catch.
        matrix_plain = " ".join(matrix.replace("*", "").replace("`", "")
                                .replace("\u2013", "-").replace("\u2014", "-").split()).lower()
        authored = sorted(n for n in (f"{i:02d}" for i in range(9))
                          if glob.glob(os.path.join(CDIR, f"{n}_*_CONTRACT.json")))
        awaiting = [n for n in (f"{i:02d}" for i in range(9)) if n not in authored]
        records_02 = ("product creative" in matrix_plain
                      and ("authored" in matrix_plain or "exist in this lineage" in matrix_plain))
        # Any global range that would sweep an authored contract into "awaiting",
        # in either the domain or contract phrasing, with an en-dash or a hyphen.
        stale = [f"{lead} {n}-08 {tail}"
                 for n in authored if n != "00"
                 for lead in ("domains", "contracts", "domain", "contract")
                 for tail in ("are still awaiting", "still awaiting", "are awaiting",
                              "still await", "await")
                 if f"{lead} {n}-08 {tail}" in matrix_plain]
        check("155. the matrix makes no global claim that an authored contract is still awaiting",
              not (records_02 and stale), f"stale={stale[:3]}")
        first_awaiting = awaiting[0] if awaiting else None
        check("    the matrix names every authored contract as authored",
              all(f"contract {n}" in matrix_plain or f" {n} -" in matrix_plain
                  for n in authored if n != "00"),
              f"authored={authored}")
        check("    only the genuinely unwritten contracts are described as awaiting",
              first_awaiting is None or f"{first_awaiting}-08" in matrix_plain,
              f"expected the awaiting range to start at {first_awaiting}")
        # Prose claims only: a markdown table legitimately holds "authored" cells
        # and "03-08" target cells in the same block, so scanning it as one
        # sentence is a false positive. The table gets its own row-wise check.
        prose = " ".join(ln for ln in matrix.splitlines() if not ln.strip().startswith("|"))
        prose_plain = " ".join(prose.replace("*", "").replace("`", "")
                               .replace("\u2013", "-").replace("\u2014", "-").split()).lower()
        # A sentence that says a domain is PARTIALLY authored, or that names a
        # contract precisely to say it does not exist, is not a claim that the
        # contract is authored. Excluding those forms keeps the guard narrow
        # instead of disabling it: "Contract 04 is authored" is still caught.
        PARTIAL_FORMS = ("partially authored", "not fully authored", "partial",
                         "does not exist", "do not exist", "still await", "awaiting",
                         "until contract", "yet to be")
        claim_sentences = [seg for seg in re.split(r"(?<=[.;:])\s+", prose_plain)
                           if "authored" in seg and "contract" in seg
                           and "await" not in seg and "incrementally" not in seg
                           and not any(f in seg for f in PARTIAL_FORMS)]
        wrongly_claimed = sorted({n for seg in claim_sentences for n in awaiting
                                  if re.search(rf"(?<!\d){n}(?!\d)", seg)})
        check("    the matrix prose does not name an unwritten contract as authored",
              not wrongly_claimed,
              f"claimed-but-absent={wrongly_claimed} awaiting={awaiting}")
        # The summary table, row by row: the created column must agree with disk.
        rows, bad_rows = [], []
        for ln in matrix.splitlines():
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 5 and cells[0].isdigit():
                # A row may target more than one contract, e.g. "03, 04".
                targets = re.findall(r"\d{2}", cells[4])
                if targets:
                    rows.append((cells[0], targets, cells[3].lower()))
        # A domain may target more than one contract, so its state is not
        # binary. Domain 4 targets 03 and 04: with only 03 authored it is
        # neither AUTHORED nor AWAITING, and forcing it into either would make
        # the matrix lie in one direction or the other.
        PARTIAL_WORDS = ("partial", "not fully authored", "partially authored")
        for row_no, targets, created in rows:
            n_exist = sum(1 for t in targets if t in authored)
            if n_exist == len(targets):
                expected = "AUTHORED"
            elif n_exist == 0:
                expected = "AWAITING"
            else:
                expected = "PARTIAL"
            says_partial = any(w in created for w in PARTIAL_WORDS)
            says_authored = "authored" in created and not says_partial
            says_awaiting = ("awaiting" in created or "await" in created) and not says_partial
            actual = ("PARTIAL" if says_partial else
                      "AUTHORED" if says_authored else
                      "AWAITING" if says_awaiting else "UNREADABLE")
            if actual != expected:
                bad_rows.append(f"row {row_no} -> {targets}: table reads {actual} "
                                f"({created!r}), {n_exist}/{len(targets)} files exist "
                                f"so it should read {expected}")
        check("    every summary row agrees with which contract files exist",
              len(rows) == 8 and not bad_rows, f"rows={len(rows)}/8 bad={bad_rows}")
    else:
        check("153. the decision-coverage matrix exists", False, MATRIX_PATH)

    # ── H. human-readable agreement ──────────────────────────────────────────
    print("\nH. human-readable agreement")
    check("155. the markdown states the core principle",
          "world physics may break" in md_plain.lower()
          and "product truth may not" in md_plain.lower())
    check("156. the markdown names every product lock",
          all(l in md for l in LOCKS), str([l for l in LOCKS if l not in md]))
    check("157. the markdown names every QA gate concept and failure",
          all(f in md for f in FAILURES), str([f for f in FAILURES if f not in md]))
    check("158. the markdown states 1:1 fidelity is not pixel identity",
          "does not mean" in md_plain.lower() and "pixel-identical" in md_plain.lower())
    check("159. the markdown separates geometry source from wear reference",
          "productGeometrySource" in md and "productWearReference" in md)
    check("160. the markdown states clothing on body is high risk",
          "high-risk" in md_plain.lower() and "clothing worn on body" in md_plain.lower())
    check("161. the markdown states UNRESOLVED is never a silent PASS",
          "never a silent" in md_plain.lower())
    check("162. the markdown states neither lock may be sacrificed",
          "neither may be sacrificed" in md_plain.lower())
    check("163. the markdown states generation success is not validation success",
          "generation success is not validation success" in md_plain.lower())
    check("164. the markdown does not claim a Product Creative Engine exists",
          "no product creative engine exists" in md_plain.lower())
    # This once asserted "no CyberNinjas service was called in this phase" — a
    # fact about one authoring session, which has no place in a normative
    # contract. The durable claim is that the contract does not depend on a
    # provider at all, so that is what the markdown must say.
    check("165. the markdown states the contract does not depend on a provider",
          "does not depend on a provider" in md_plain.lower()
          and "whether or not a provider is connected" in md_plain.lower())
    # Test for the ASSERTIVE forms only. The contract's own sentence explaining
    # why such facts are excluded necessarily names them, and must not trip this.
    check("    the markdown asserts no phase-execution audit fact",
          not any(claim in md_plain.lower() for claim in
                  ("no credits were spent", "no cyberninjas service was called",
                   "no service was called in this phase", "no subscription is assumed")),
          str([claim for claim in ("no credits were spent",
                                   "no cyberninjas service was called",
                                   "no service was called in this phase",
                                   "no subscription is assumed")
               if claim in md_plain.lower()]))
    check("166. the markdown separates applicability from result",
          "not a fourth evaluation result" in md_plain.lower())
    check("167. the markdown states confidence is not permission to generate",
          "not permission to generate" in md_plain.lower())
    check("168. the markdown separates fit evidence from a fit result",
          "clothingFitEvidence" in md and "never" in md_plain.lower()
          and "fitStatus" in md)
    check("    the markdown states a package may not waive a gate",
          "must not waive a gate" in md_plain.lower())
    check("    the markdown states the fit-evidence rule runs both ways",
          "forbidden when it is false" in md_plain.lower()
          and "both directions" in md_plain.lower())
    check("169. the markdown states the package carries no outputStatus",
          "no outputStatus" in md_plain or "no `outputStatus`" in md)
    check("170. the markdown states consent state is not recorded here",
          "not recorded here" in md_plain.lower()
          and "read from the authority" in md_plain.lower())
    check("    the markdown caches no consent state value",
          "OWNER_CONFIRMATION_REQUIRED" not in md)
    check("171. the markdown declares open items rather than inventing answers",
          "Open items" in md and "MUST NOT" in md)

    print(f"\n{len(c.get('productLockCategories', []))} product locks, "
          f"{len(c.get('qaGates', []))} QA gates, "
          f"{len(c.get('hardFailures', []))} hard failures, "
          f"{len(c.get('openItems', []))} open items")
    print("Runtime fixtures were checked by a targeted semantic checker, not a JSON Schema "
          "engine; section E proves the same rules are encoded in the schema documents.")
    print(f"PRODUCT CREATIVE CONTRACT: {'PASS' if not failed else 'FAIL'} "
          f"({passed} passed, {failed} failed)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
