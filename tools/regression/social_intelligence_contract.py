#!/usr/bin/env python3
"""Validator for the PINK MALL Social Intelligence Contract (contract 04).

    python tools/regression/social_intelligence_contract.py

This contract implements no engine and no connector; it is what a future Social
Intelligence Engine will be held to. The failure it guards against is specific:
a measured number quietly promoting itself into a conclusion, and a conclusion
quietly promoting itself into an action nobody authorised — a missing metric
becoming a zero, a winner becoming a permanent rule, engagement becoming
approval, a recommendation becoming a story transition.

HONEST LIMIT, two directions. The runtime section below is a TARGETED SEMANTIC
CHECKER, not a JSON Schema engine: it enforces the governance-bearing subset of
the snapshot rules directly in Python, because this repository takes no
dependency and the standard library ships no validator. It is therefore not
proof of full schema conformance, which is why every shape rule it enforces is
ALSO proved present in the schema documents by the structural checks in
section H.

The converse also holds, and matters more. SCHEMA CONFORMANCE IS NOT SUFFICIENT
EITHER. Draft 2020-12 has no keyword for cross-record resolution or for
uniqueness by an arbitrary identifier property — `uniqueItems` compares whole
items, so two records differing in any other field satisfy it while sharing an
id. So a snapshot is accepted only when BOTH layers pass: the schema for the
shape of each record, and semantic reference-integrity validation for the fact
that every reference resolves to exactly one present record of a permitted kind
and that no two records answer to the same identifier.

Every fixture here is SYNTHETIC. No real account metric, no real campaign
performance, no private audience history and no credential appears in this file
or anywhere in this repository.

Standard library only, by design.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CDIR = os.path.join(ROOT, "docs", "pink-mall", "system-contracts")

JSON_PATH   = os.path.join(CDIR, "04_SOCIAL_INTELLIGENCE_CONTRACT.json")
SCHEMA_PATH = os.path.join(CDIR, "04_SOCIAL_INTELLIGENCE_CONTRACT.schema.json")
OBJECT_PATH = os.path.join(CDIR, "04_SOCIAL_INTELLIGENCE_OBJECT.schema.json")
MD_PATH     = os.path.join(CDIR, "04_SOCIAL_INTELLIGENCE_CONTRACT.md")
PARENT_PATH = os.path.join(CDIR, "00_SYSTEM_AUTHORITY_CONTRACT.json")
DEP01_PATH  = os.path.join(CDIR, "01_CAMPAIGN_CONTEXT_CONTRACT.json")
DEP03_PATH  = os.path.join(CDIR, "03_CHARACTER_STORY_CONTRACT.json")
INDEX_PATH  = os.path.join(CDIR, "SYSTEM_CONTRACT_INDEX.md")
MATRIX_PATH = os.path.join(CDIR, "DECISION_COVERAGE_MATRIX.md")

EXPECTED_CONTRACT_ID = "PINK_MALL_SOCIAL_INTELLIGENCE_CONTRACT"
EXPECTED_PARENT_ID   = "PINK_MALL_SYSTEM_AUTHORITY_CONTRACT"
EXPECTED_NUMBER      = "04"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

ARCS = ["CONTINUE", "EVOLVE", "PAUSE", "CLOSE", "REVIVE"]
PRIORITY = ["SHARES", "DM_SENDS", "COMMENTS", "DMS", "FOLLOWER_GROWTH",
            "SAVES", "PROFILE_INTEREST", "LIKES", "VIEWS"]
TIERS = {"TIER_PRIMARY":     ["SHARES", "DM_SENDS"],
         "TIER_NEXT":        ["COMMENTS", "DMS", "FOLLOWER_GROWTH", "SAVES", "PROFILE_INTEREST"],
         "TIER_CONTEXTUAL":  ["LIKES", "VIEWS"]}
AVAIL = ["AVAILABLE", "UNKNOWN", "UNAVAILABLE", "NOT_APPLICABLE", "NOT_MEASURED"]
RAW_AUTHORITIES = {"SOCIAL_PLATFORM_API", "CANONICAL_REPOSITORY"}
LAYERS = ["RAW_SOCIAL_METRIC", "DERIVED_METRIC", "SOCIAL_INTERPRETATION", "RECOMMENDATION",
          "APPROVAL", "STORY_CANON", "PUBLICATION"]
SUBJECT_TYPES = {"CAMPAIGN", "CREATIVE_ASSET", "STORY_MECHANISM", "CONTENT_UNIT",
                 "CREATIVE_MECHANISM", "CHARACTER_TEAM_MECHANIC"}

SNAP_REQUIRED = ["schemaVersion", "snapshotRef", "subjectRef", "subjectType", "observationWindowRef",
                 "rawEvidence", "interpretations", "creativeMechanismAssessments",
                 "fatigueAssessment", "recommendations", "knownLimitations", "provenance",
                 "assertionsOutsideAuthority"]
RAW_REQUIRED = ["evidenceRef", "metricIdentity", "availability", "sourceAuthority", "truthClass",
                "subjectRef", "observationWindowRef"]
RAW_OPTIONAL = ["observedValue", "sourceRef", "derivationRuleRef", "limitations"]
INT_REQUIRED = ["interpretationRef", "kind", "statement", "truthClass", "evidenceRefs"]
INT_OPTIONAL = ["confidence", "limitations"]
MECH_REQUIRED = ["assessmentRef", "mechanismRef", "truthClass", "assessment", "evidenceRefs",
                 "exploitationRecommended", "exploitationIsTemporary",
                 "establishesPermanentCreativeRule", "establishesProductTruth",
                 "establishesHumanIdentityTruth", "altersStoryState"]
MECH_OPTIONAL = ["limitations"]
REC_REQUIRED = ["recommendationRef", "targetRef", "recommendedAction", "truthClass",
                "authorityClaimed", "evidenceRefs"]
REC_OPTIONAL = ["storyAction", "limitations"]

# Which record kinds a reference may point at. These sets preserve the reviewed
# base exactly: this correction adds RESOLUTION of references, not a change to
# which kinds may be cited. An interpretation is drawn FROM measurement, so it
# cites raw evidence. An assessment and a recommendation may also rest on a
# recorded interpretation. Nothing may cite a recommendation — a proposal is not
# support — and nothing may cite a mechanism assessment, because the reviewed
# base did not permit it and widening that set is not needed to repair a
# resolution defect.
RAW, INTERP, MECH, REC = ("RAW_EVIDENCE", "INTERPRETATION",
                          "CREATIVE_MECHANISM_ASSESSMENT", "RECOMMENDATION")
REF_TARGETS = {
    "interpretations":               (RAW,),
    "creativeMechanismAssessments":  (RAW, INTERP),
    "fatigueAssessment":             (RAW, INTERP),
    "recommendations":               (RAW, INTERP),
}
# The identifier field each record kind carries. All four share ONE identifier
# space inside a snapshot, so a reference can never resolve to two records.
ID_FIELDS = {"rawEvidence": ("evidenceRef", RAW),
             "interpretations": ("interpretationRef", INTERP),
             "creativeMechanismAssessments": ("assessmentRef", MECH),
             "recommendations": ("recommendationRef", REC)}

# Keys whose presence would carry private operational data into a public artefact.
PRIVATE_KEYS = {"accountHandle", "accountId", "messageBody", "dmContent", "customerId",
                "userId", "email", "phone", "accessToken", "apiKey", "apiSecret",
                "credential", "password", "followerList", "audienceMember"}
# Keys that would turn the qualitative hierarchy into arithmetic.
WEIGHT_KEYS = {"weight", "weights", "score", "scores", "ratio", "points", "multiplier",
               "coefficient", "threshold", "cooldown", "cooldownDays", "weighting"}

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


def walk_keys(node, path="$"):
    if isinstance(node, dict):
        for k, v in node.items():
            yield k, f"{path}.{k}"
            yield from walk_keys(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_keys(v, f"{path}[{i}]")


def walk_values(node, path="$"):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_values(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_values(v, f"{path}[{i}]")
    else:
        yield node, path


# ─────────────────────────────────────────────────────────────────────────────
# Targeted semantic checker for a Social Intelligence Snapshot.
# Read the honest-limit note in the module docstring before trusting this.
# ─────────────────────────────────────────────────────────────────────────────
def check_snapshot(sn):
    """Return a list of violation strings. Empty list means the subset passes."""
    e = []
    if not isinstance(sn, dict):
        return ["snapshot is not an object"]

    for k in SNAP_REQUIRED:
        if k not in sn:
            e.append(f"missing required key {k}")
    for k in sn:
        if k not in SNAP_REQUIRED:
            e.append(f"unknown top-level field {k}")

    if not SEMVER.fullmatch(str(sn.get("schemaVersion", ""))):
        e.append("schemaVersion is not a semantic version")
    if sn.get("subjectType") not in SUBJECT_TYPES:
        e.append(f"unknown subjectType {sn.get('subjectType')!r}")
    for k in ("snapshotRef", "subjectRef", "observationWindowRef"):
        if not isinstance(sn.get(k), str) or not sn.get(k):
            e.append(f"{k} must be a non-empty opaque reference")

    # ---- identifier index, built before anything is resolved ----
    # A reference is only meaningful if exactly one record answers to it. Two
    # records sharing an id make every reference to that id ambiguous, and the
    # ambiguity is silent: both readings look valid. So uniqueness is checked
    # across the WHOLE snapshot, not per array — an interpretation named after a
    # piece of evidence is the same defect as two pieces of evidence sharing a name.
    # `x or []` passes a non-list straight through, so a collection that is not a
    # list reaches enumerate() and raises. The per-collection loops below already
    # report that as a violation; this pre-pass must not crash before they run,
    # because a checker that raises tells a caller nothing about what is wrong.
    def records(key):
        value = sn.get(key)
        return value if isinstance(value, list) else []

    id_index = {}
    for arr, (field, kind) in ID_FIELDS.items():
        for i, rec in enumerate(records(arr)):
            if not isinstance(rec, dict):
                continue
            rid = rec.get(field)
            if not isinstance(rid, str) or not rid:
                e.append(f"{arr}[{i}] has no usable {field}")
                continue
            if rid in id_index:
                prev_arr, prev_i, prev_kind = id_index[rid]
                e.append(f"ambiguous record identifier {rid!r}: {prev_arr}[{prev_i}] "
                         f"({prev_kind}) and {arr}[{i}] ({kind}) both answer to it")
            else:
                id_index[rid] = (arr, i, kind)

    def resolve(refs, where, arr_key):
        """Every reference must resolve to exactly one record of a permitted kind."""
        permitted = REF_TARGETS[arr_key]
        if not isinstance(refs, list) or not refs:
            e.append(f"{where} is unsupported — no supporting reference at all")
            return
        for ref in refs:
            if not isinstance(ref, str) or not ref:
                e.append(f"{where} carries a reference that is not a usable identifier")
                continue
            target = id_index.get(ref)
            if target is None:
                e.append(f"{where} references {ref!r}, which resolves to no record in "
                         f"this snapshot — a non-empty string is not evidence")
                continue
            if target[2] not in permitted:
                e.append(f"{where} references {ref!r}, which is a {target[2]}; this record "
                         f"may only cite {', '.join(permitted)}")
                continue
            # Citing a conclusion is only support if that conclusion is itself
            # grounded. Under the target rules above this is REDUNDANT — an
            # interpretation that rests on nothing is already rejected on its own
            # account, so this branch never fires alone. It is kept deliberately:
            # it makes the guarantee local rather than emergent, so relaxing the
            # interpretation target set later cannot silently lose it.
            if target[2] == INTERP:
                cited_all = records("interpretations")
                cited = cited_all[target[1]] if target[1] < len(cited_all) else {}
                cited_refs = cited.get("evidenceRefs") if isinstance(cited, dict) else None
                grounded = [r for r in (cited_refs if isinstance(cited_refs, list) else [])
                            if isinstance(r, str) and id_index.get(r, (None, None, None))[2] == RAW]
                if not grounded:
                    e.append(f"{where} references interpretation {ref!r}, which is not itself "
                             f"grounded in any resolvable raw evidence")

    # ---- raw evidence: measurement, kept apart from conclusion ----
    ev_ids = set()
    raw = sn.get("rawEvidence")
    if not isinstance(raw, list):
        e.append("rawEvidence must be an array")
        raw = []
    for i, r in enumerate(raw):
        if not isinstance(r, dict):
            e.append(f"rawEvidence[{i}] is not an object"); continue
        for k in RAW_REQUIRED:
            if k not in r:
                e.append(f"rawEvidence[{i}] missing {k}")
        for k in r:
            if k not in RAW_REQUIRED + RAW_OPTIONAL:
                e.append(f"rawEvidence[{i}] unknown field {k}")
        ev_ids.add(r.get("evidenceRef"))

        mi = r.get("metricIdentity")
        if not isinstance(mi, dict):
            e.append(f"rawEvidence[{i}] metricIdentity must be an object")
        else:
            has_p = "prioritySignalId" in mi
            has_n = "sourceNativeMetricId" in mi
            if has_p == has_n:
                e.append(f"rawEvidence[{i}] must carry exactly one of "
                         f"prioritySignalId / sourceNativeMetricId")
            if has_p and mi["prioritySignalId"] not in PRIORITY:
                e.append(f"rawEvidence[{i}] unknown prioritySignalId {mi['prioritySignalId']!r}")
            tier = mi.get("priorityTierRef")
            if has_n and tier is not None:
                e.append(f"rawEvidence[{i}] an open source-native metric was placed in tier "
                         f"{tier!r} with no published mapping rule")
            if has_p and tier is not None:
                expected = next((t for t, sigs in TIERS.items()
                                 if mi["prioritySignalId"] in sigs), None)
                if tier != expected:
                    e.append(f"rawEvidence[{i}] {mi['prioritySignalId']} belongs to "
                             f"{expected}, not {tier!r}")
            for k in mi:
                if k not in ("prioritySignalId", "sourceNativeMetricId", "priorityTierRef"):
                    e.append(f"rawEvidence[{i}] metricIdentity unknown field {k}")

        av = r.get("availability")
        if av not in AVAIL:
            e.append(f"rawEvidence[{i}] unknown availability {av!r}")
        # The rule that stops a missing metric becoming a number.
        if av == "AVAILABLE" and "observedValue" not in r:
            e.append(f"rawEvidence[{i}] is AVAILABLE but carries no observedValue")
        if av != "AVAILABLE" and "observedValue" in r:
            e.append(f"rawEvidence[{i}] availability {av!r} MUST NOT carry an observedValue "
                     f"({r.get('observedValue')!r}) — missing is not zero")

        sa = r.get("sourceAuthority")
        if sa not in RAW_AUTHORITIES:
            e.append(f"rawEvidence[{i}] source authority {sa!r} is not a raw-metric authority")
        tc = r.get("truthClass")
        if tc not in ("FACT", "DERIVED_FACT"):
            e.append(f"rawEvidence[{i}] truthClass {tc!r} is not measured evidence")
        if tc == "DERIVED_FACT" and not r.get("derivationRuleRef"):
            e.append(f"rawEvidence[{i}] DERIVED_FACT with no published derivation rule")
        if tc != "DERIVED_FACT" and r.get("derivationRuleRef"):
            e.append(f"rawEvidence[{i}] derivationRuleRef on a non-derived record")

    # ---- interpretations: conclusions, referencing their evidence ----
    int_ids = set()
    ints = sn.get("interpretations")
    if not isinstance(ints, list):
        e.append("interpretations must be an array"); ints = []
    for i, it in enumerate(ints):
        if not isinstance(it, dict):
            e.append(f"interpretations[{i}] is not an object"); continue
        for k in INT_REQUIRED:
            if k not in it:
                e.append(f"interpretations[{i}] missing {k}")
        for k in it:
            if k not in INT_REQUIRED + INT_OPTIONAL:
                e.append(f"interpretations[{i}] unknown field {k}")
        int_ids.add(it.get("interpretationRef"))
        if it.get("truthClass") != "INTERPRETATION":
            e.append(f"interpretations[{i}] truthClass {it.get('truthClass')!r} — a conclusion "
                     f"MUST NOT be recorded as fact or approval")
        resolve(it.get("evidenceRefs"), f"interpretations[{i}]", "interpretations")

    # ---- creative mechanism assessments: a winner is a reading, never a rule ----
    exploiting = False
    mechs = sn.get("creativeMechanismAssessments")
    if not isinstance(mechs, list):
        e.append("creativeMechanismAssessments must be an array"); mechs = []
    for i, m in enumerate(mechs):
        if not isinstance(m, dict):
            e.append(f"creativeMechanismAssessments[{i}] is not an object"); continue
        for k in MECH_REQUIRED:
            if k not in m:
                e.append(f"creativeMechanismAssessments[{i}] missing {k}")
        for k in m:
            if k not in MECH_REQUIRED + MECH_OPTIONAL:
                e.append(f"creativeMechanismAssessments[{i}] unknown field {k}")
        if m.get("truthClass") != "INTERPRETATION":
            e.append(f"creativeMechanismAssessments[{i}] a winner reading must be INTERPRETATION")
        if m.get("exploitationIsTemporary") is not True:
            e.append(f"creativeMechanismAssessments[{i}] exploitation must be temporary")
        for k in ("establishesPermanentCreativeRule", "establishesProductTruth",
                  "establishesHumanIdentityTruth", "altersStoryState"):
            if m.get(k) is not False:
                e.append(f"creativeMechanismAssessments[{i}] {k} must be false — one strong "
                         f"result MUST NOT become permanent truth")
        resolve(m.get("evidenceRefs"), f"creativeMechanismAssessments[{i}]",
                "creativeMechanismAssessments")
        if m.get("exploitationRecommended") is True:
            exploiting = True

    # ---- recommendations: proposals, never authority ----
    recs = sn.get("recommendations")
    if not isinstance(recs, list):
        e.append("recommendations must be an array"); recs = []
    for i, rc in enumerate(recs):
        if not isinstance(rc, dict):
            e.append(f"recommendations[{i}] is not an object"); continue
        for k in REC_REQUIRED:
            if k not in rc:
                e.append(f"recommendations[{i}] missing {k}")
        for k in rc:
            if k not in REC_REQUIRED + REC_OPTIONAL:
                e.append(f"recommendations[{i}] unknown field {k}")
        if rc.get("truthClass") != "PROPOSAL":
            e.append(f"recommendations[{i}] truthClass {rc.get('truthClass')!r} — a "
                     f"recommendation is a PROPOSAL and never an approval, a fact or canon")
        if rc.get("authorityClaimed") != "NONE":
            e.append(f"recommendations[{i}] claims authority {rc.get('authorityClaimed')!r}")
        resolve(rc.get("evidenceRefs"), f"recommendations[{i}]", "recommendations")
        sa = rc.get("storyAction")
        if sa is not None:
            if not isinstance(sa, dict):
                e.append(f"recommendations[{i}] storyAction is not an object")
            else:
                if sa.get("action") not in ARCS:
                    e.append(f"recommendations[{i}] story action {sa.get('action')!r} is not "
                             f"in contract 03's vocabulary")
                for k in ("redefinesNarrativeMeaning", "isStoryStateTransition",
                          "transitionAuthorityGranted"):
                    if sa.get(k) is not False:
                        e.append(f"recommendations[{i}] storyAction {k} must be false — "
                                 f"recommendation does not equal transition")
                for k in sa:
                    if k not in ("action", "redefinesNarrativeMeaning", "isStoryStateTransition",
                                 "transitionAuthorityGranted"):
                        e.append(f"recommendations[{i}] storyAction unknown field {k}")
                if sa.get("action") == "CONTINUE":
                    exploiting = True

    # ---- fatigue: considered before repetitive continuation ----
    fa = sn.get("fatigueAssessment")
    if not isinstance(fa, dict):
        e.append("fatigueAssessment must be an object")
    else:
        for k in ("considered", "truthClass", "assessment", "evidenceRefs", "uncertainty"):
            if k not in fa:
                e.append(f"fatigueAssessment missing {k}")
        for k in fa:
            if k not in ("considered", "truthClass", "assessment", "evidenceRefs", "uncertainty"):
                e.append(f"fatigueAssessment unknown field {k}")
        if fa.get("considered") is not True:
            e.append("fatigueAssessment.considered must be true — fatigue MUST be tracked")
        if fa.get("truthClass") != "INTERPRETATION":
            e.append("fatigueAssessment is an interpretation, not a raw metric")
        if exploiting and not fa.get("evidenceRefs"):
            e.append("repetitive continuation is recommended with no fatigue evidence considered")
        if fa.get("evidenceRefs"):
            resolve(fa.get("evidenceRefs"), "fatigueAssessment", "fatigueAssessment")

    # ---- the snapshot asserts nothing outside its authority ----
    aoa = sn.get("assertionsOutsideAuthority")
    if not isinstance(aoa, list):
        e.append("assertionsOutsideAuthority must be an array")
    elif aoa:
        e.append(f"snapshot asserts {len(aoa)} thing(s) outside its authority: {aoa!r}")

    pr = sn.get("provenance")
    if not isinstance(pr, dict):
        e.append("provenance must be an object")
    else:
        if pr.get("generatedBy") != "SOCIAL_INTELLIGENCE_ENGINE":
            e.append(f"provenance.generatedBy {pr.get('generatedBy')!r} unexpected")
        if pr.get("generatedByIsRawMetricAuthority") is not False:
            e.append("the emitter of a snapshot is not the authority for its measurements")
        if pr.get("rawMetricAuthority") != "SOCIAL_PLATFORM_API":
            e.append(f"provenance.rawMetricAuthority {pr.get('rawMetricAuthority')!r} unexpected")
        for k in pr:
            if k not in ("generatedBy", "generatedByIsRawMetricAuthority", "rawMetricAuthority"):
                e.append(f"provenance unknown field {k}")

    # ---- private data and smuggled arithmetic, anywhere in the document ----
    for k, path in walk_keys(sn):
        if k in PRIVATE_KEYS:
            e.append(f"private operational field {k} at {path}")
        if k.lower() in {w.lower() for w in WEIGHT_KEYS}:
            e.append(f"numeric weighting field {k} at {path} — no numeric weighting is authorised")
    return e


def valid_snapshot():
    """Public-safe synthetic snapshot. Opaque references, no real account or campaign."""
    return {
        "schemaVersion": "1.0.0",
        "snapshotRef": "synthetic-snapshot-a",
        "subjectRef": "synthetic-subject-a",
        "subjectType": "CREATIVE_MECHANISM",
        "observationWindowRef": "synthetic-window-a",
        "rawEvidence": [
            {   # Tier 1
                "evidenceRef": "ev-shares",
                "metricIdentity": {"prioritySignalId": "SHARES", "priorityTierRef": "TIER_PRIMARY"},
                "availability": "AVAILABLE", "observedValue": 12,
                "sourceAuthority": "SOCIAL_PLATFORM_API", "sourceRef": "synthetic-platform-a",
                "truthClass": "FACT",
                "subjectRef": "synthetic-subject-a", "observationWindowRef": "synthetic-window-a"},
            {   # Tier 2
                "evidenceRef": "ev-saves",
                "metricIdentity": {"prioritySignalId": "SAVES", "priorityTierRef": "TIER_NEXT"},
                "availability": "AVAILABLE", "observedValue": 7,
                "sourceAuthority": "SOCIAL_PLATFORM_API", "sourceRef": "synthetic-platform-a",
                "truthClass": "FACT",
                "subjectRef": "synthetic-subject-a", "observationWindowRef": "synthetic-window-a"},
            {   # Tier 3, and deliberately NOT MEASURED: no value, not a zero.
                "evidenceRef": "ev-views",
                "metricIdentity": {"prioritySignalId": "VIEWS", "priorityTierRef": "TIER_CONTEXTUAL"},
                "availability": "NOT_MEASURED",
                "sourceAuthority": "SOCIAL_PLATFORM_API", "truthClass": "FACT",
                "subjectRef": "synthetic-subject-a", "observationWindowRef": "synthetic-window-a",
                "limitations": ["no observation was taken for this window"]},
            {   # An open provider metric, recorded with its native name and NO tier.
                "evidenceRef": "ev-native",
                "metricIdentity": {"sourceNativeMetricId": "synthetic_native_metric"},
                "availability": "AVAILABLE", "observedValue": 3,
                "sourceAuthority": "SOCIAL_PLATFORM_API", "truthClass": "FACT",
                "subjectRef": "synthetic-subject-a", "observationWindowRef": "synthetic-window-a"}],
        "interpretations": [
            {"interpretationRef": "int-resonance", "kind": "resonance",
             "statement": "the passing-on behaviour suggests this mechanism resonates",
             "truthClass": "INTERPRETATION",
             "evidenceRefs": ["ev-shares", "ev-saves"],
             "confidence": {"qualitative": "supported by tier-1 and tier-2 signals only"},
             "limitations": ["views were not measured for this window"]}],
        "creativeMechanismAssessments": [
            {"assessmentRef": "mech-a", "mechanismRef": "synthetic-mechanism-a",
             "truthClass": "INTERPRETATION",
             "assessment": "reads as a winner for this window",
             "evidenceRefs": ["ev-shares"],
             "exploitationRecommended": True, "exploitationIsTemporary": True,
             "establishesPermanentCreativeRule": False, "establishesProductTruth": False,
             "establishesHumanIdentityTruth": False, "altersStoryState": False}],
        "fatigueAssessment": {
            "considered": True, "truthClass": "INTERPRETATION",
            "assessment": "no repetition signal yet in the evidence considered",
            "evidenceRefs": ["ev-shares", "ev-saves"],
            "uncertainty": "one window only; no trend is claimed"},
        "recommendations": [
            {"recommendationRef": "rec-a", "targetRef": "synthetic-arc-a",
             "recommendedAction": "continue the arc for one further window",
             "truthClass": "PROPOSAL", "authorityClaimed": "NONE",
             "evidenceRefs": ["int-resonance", "ev-shares"],
             "storyAction": {"action": "CONTINUE", "redefinesNarrativeMeaning": False,
                             "isStoryStateTransition": False, "transitionAuthorityGranted": False}}],
        "knownLimitations": ["a single synthetic window", "one synthetic surface only"],
        "provenance": {"generatedBy": "SOCIAL_INTELLIGENCE_ENGINE",
                       "generatedByIsRawMetricAuthority": False,
                       "rawMetricAuthority": "SOCIAL_PLATFORM_API"},
        "assertionsOutsideAuthority": []}


def mutate(fn, base=None):
    sn = json.loads(json.dumps(base if base is not None else valid_snapshot()))
    fn(sn)
    return sn


def main():
    print("PINK MALL — SOCIAL INTELLIGENCE CONTRACT (04)\n")
    print("A. identity and inheritance")
    try:
        c = load(JSON_PATH); schema = load(SCHEMA_PATH); obj = load(OBJECT_PATH)
        parent = load(PARENT_PATH); dep01 = load(DEP01_PATH); dep03 = load(DEP03_PATH)
        check("1. contract, both schemas, parent and both dependency contracts parse", True)
    except Exception as exc:
        check("1. contract, both schemas, parent and both dependency contracts parse", False, str(exc))
        print("SOCIAL INTELLIGENCE CONTRACT: FAIL (cannot continue)")
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
    check("4. contractNumber is 04", c.get("contractNumber") == EXPECTED_NUMBER,
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

    print("\nB. the reserved slot and sibling boundaries")
    slots = parent.get("contractSequence", {}).get("slots", [])
    slot = next((s for s in slots if s.get("contractNumber") == EXPECTED_NUMBER), None)
    check("8. contract 00 reserves slot 04 with this exact contract id",
          slot is not None and slot.get("contractId") == EXPECTED_CONTRACT_ID,
          str(slot))
    check("    and titles it Social Intelligence",
          slot is not None and slot.get("title") == "Social Intelligence")
    check("    contract 00 was not edited to record that contract 04 now exists",
          "does NOT record which contracts currently exist"
          in parent.get("contractSequence", {}).get("rule", ""))
    deps = {d.get("contractNumber"): d for d in c.get("dependsOn", [])}
    check("9. contract 04 declares its dependency on 01 and 03", set(deps) == {"01", "03"},
          str(sorted(deps)))
    check("    01 is named as the campaign-context owner",
          deps.get("01", {}).get("contractId") == dep01.get("contractId"))
    check("    03 is named as the story-vocabulary owner",
          deps.get("03", {}).get("contractId") == dep03.get("contractId"))
    db = {b.get("contractNumber"): b for b in c.get("deferredBoundaries", [])}
    check("10. responsibilities are deferred to 05, 06, 07 and 08",
          set(db) == {"05", "06", "07", "08"}, str(sorted(db)))
    check("    every boundary disclaims owning whether that contract exists",
          all(b.get("existenceOwnedHere") is False for b in db.values()))
    check("    and points existence at the contract index",
          all(b.get("existenceRecordedIn", "").endswith("SYSTEM_CONTRACT_INDEX.md")
              for b in db.values()))
    check("    no boundary states whether the receiving contract exists",
          all("exists" not in b.get("boundary", "") for b in db.values()))
    check("    the deferral rule says authoring 05-08 later must not edit this contract",
          "MUST NOT require editing this contract" in c.get("deferredBoundaryRule", ""))

    print("\nC. the core separation")
    cs = c.get("coreSeparation", {})
    layers = cs.get("layers", [])
    check("11. all seven layers are present in order",
          [l.get("layerId") for l in layers] == LAYERS,
          str([l.get("layerId") for l in layers]))
    expected_tc = {"RAW_SOCIAL_METRIC": "FACT", "DERIVED_METRIC": "DERIVED_FACT",
                   "SOCIAL_INTERPRETATION": "INTERPRETATION", "RECOMMENDATION": "PROPOSAL",
                   "APPROVAL": "APPROVAL", "STORY_CANON": "FACT", "PUBLICATION": "APPROVAL"}
    check("    each layer carries its expected truth class",
          all(l.get("truthClass") == expected_tc[l["layerId"]] for l in layers),
          str([(l["layerId"], l.get("truthClass")) for l in layers
               if l.get("truthClass") != expected_tc.get(l["layerId"])]))
    expected_au = {"RAW_SOCIAL_METRIC": "SOCIAL_PLATFORM_API", "DERIVED_METRIC": "SOCIAL_PLATFORM_API",
                   "SOCIAL_INTERPRETATION": "SOCIAL_INTELLIGENCE_ENGINE",
                   "RECOMMENDATION": "SOCIAL_INTELLIGENCE_ENGINE", "APPROVAL": "OWNER",
                   "STORY_CANON": "STORY_STATE_ENGINE", "PUBLICATION": "OWNER"}
    check("    each layer names its expected authority",
          all(l.get("authority") == expected_au[l["layerId"]] for l in layers))
    check("    no layer is owned by this contract",
          all(l.get("ownedHere") is False for l in layers))
    check("12. the layers may not be collapsed into one", cs.get("collapsePermitted") is False)
    check("    the markdown states the same seven-layer separation",
          all(t in low for t in ("raw social metric", "derived metric", "social interpretation",
                                 "recommendation", "approval", "story canon", "publication")))

    print("\nD. raw metrics versus interpretation")
    rm = c.get("rawMetricsAuthority", {})
    pdom = next((d for d in parent.get("authorityDomains", [])
                 if d.get("domainId") == "SOCIAL_RAW_METRICS"), {})
    check("13. raw-metric authority is SOCIAL_PLATFORM_API",
          rm.get("primaryAuthority") == "SOCIAL_PLATFORM_API", str(rm.get("primaryAuthority")))
    check("    and it is inherited from contract 00 rather than redefined",
          pdom.get("primaryAuthority") == [rm.get("primaryAuthority")]
          and rm.get("inheritedFrom", "").endswith("SOCIAL_RAW_METRICS"))
    check("14. the Social Intelligence Engine is NOT raw-metric authority",
          rm.get("socialIntelligenceEngineIsRawMetricAuthority") is False
          and "SOCIAL_INTELLIGENCE_ENGINE" in rm.get("nonAuthoritative", []))
    check("    Super Brain is not raw-metric authority either",
          rm.get("superBrainIsRawMetricAuthority") is False
          and "SUPER_BRAIN" in rm.get("nonAuthoritative", []))
    check("    chat history is not raw-metric authority either",
          "CHAT_HISTORY" in rm.get("nonAuthoritative", []))
    check("    Super Brain may not overwrite a raw metric fact",
          rm.get("superBrainMayOverwriteRawMetric") is False)
    check("    contract 00 agrees on who is non-authoritative for raw metrics",
          {"SUPER_BRAIN", "SOCIAL_INTELLIGENCE_ENGINE", "CHAT_HISTORY"}
          <= set(pdom.get("nonAuthoritative", [])))

    ia = c.get("interpretationAuthority", {})
    idom = next((d for d in parent.get("authorityDomains", [])
                 if d.get("domainId") == "SOCIAL_INTERPRETATION"), {})
    check("15. interpretation authority is the Social Intelligence Engine",
          ia.get("primaryAuthority") == "SOCIAL_INTELLIGENCE_ENGINE")
    check("    inherited from contract 00, with Super Brain as secondary evidence",
          idom.get("primaryAuthority") == [ia.get("primaryAuthority")]
          and ia.get("secondaryEvidence") == ["SUPER_BRAIN"]
          and idom.get("secondaryEvidence") == ["SUPER_BRAIN"])
    check("16. raw metrics and interpretation are separate domains",
          rm.get("domain") == "SOCIAL_RAW_METRICS" and ia.get("domain") == "SOCIAL_INTERPRETATION"
          and rm.get("primaryAuthority") != ia.get("primaryAuthority"))
    rv = c.get("rawVersusInterpretation", {})
    check("    evidence, conclusion and suggested action may not share a field",
          rv.get("mayBeCollapsed") is False
          and rv.get("separateStructuresRequired")
          == ["rawEvidence", "interpretations", "recommendations"])
    kinds = {x.get("kind"): x.get("truthClass") for x in rv.get("examples", [])}
    check("    the worked examples class each statement correctly",
          kinds == {"RAW_SOCIAL_METRIC": "FACT", "SOCIAL_INTERPRETATION": "INTERPRETATION",
                    "RECOMMENDATION": "PROPOSAL"}, str(kinds))
    check("17. no Social Intelligence authority over Product Truth",
          ia.get("authorityOverProductTruth") is False)
    check("18. no Social Intelligence authority over Human Identity",
          ia.get("authorityOverHumanIdentity") is False)
    check("19. no direct Story State authority",
          ia.get("authorityOverStoryState") is False)
    check("20. no approval, publication or spend authority",
          ia.get("authorityOverApproval") is False
          and ia.get("authorityOverPublication") is False
          and ia.get("authorityOverSpend") is False)
    check("    nor authority over canonical repository state",
          ia.get("authorityOverCanonicalRepositoryState") is False)
    ag = c.get("authorityGrants", {})
    check("    and the grant block denies every one of them",
          all(v is False for v in ag.values() if isinstance(v, bool)) and len(
              [v for v in ag.values() if isinstance(v, bool)]) == 9,
          str([k for k, v in ag.items() if v is True]))

    print("\nE. response priority, winner and fatigue")
    rp = c.get("responsePriority", {})
    tiers = {t.get("tierId"): t for t in rp.get("tiers", [])}
    check("21. the response-priority hierarchy exists and is locked",
          rp.get("status") == "LOCKED" and rp.get("kind") == "QUALITATIVE_PRIORITY"
          and len(tiers) == 3, str(sorted(tiers)))
    for tid, sigs in TIERS.items():
        check(f"    {tid} membership is exactly {sigs}",
              tiers.get(tid, {}).get("signals") == sigs, str(tiers.get(tid, {}).get("signals")))
    check("    the three tiers partition the nine locked signals with no overlap",
          sorted(s for t in tiers.values() for s in t.get("signals", [])) == sorted(PRIORITY))
    check("    tier order is stated without arithmetic",
          tiers.get("TIER_PRIMARY", {}).get("rankedAbove") == ["TIER_NEXT", "TIER_CONTEXTUAL"]
          and tiers.get("TIER_NEXT", {}).get("rankedAbove") == ["TIER_CONTEXTUAL"]
          and tiers.get("TIER_CONTEXTUAL", {}).get("rankedAbove") == [])
    # 22 — the whole point of the hierarchy: priority without a number.
    nums = [p for v, p in walk_values(rp)
            if isinstance(v, (int, float)) and not isinstance(v, bool)]
    check("22. no numeric value appears anywhere in the hierarchy", not nums, str(nums))
    wkeys = [p for k, p in walk_keys(rp) if k.lower() in {w.lower() for w in WEIGHT_KEYS}]
    check("    and no weight, score, ratio or points key appears either", not wkeys, str(wkeys))
    check("    qualitative priority is locked while numeric weighting stays open",
          rp.get("qualitativePriorityIsLocked") is True
          and rp.get("numericWeightingIsOpen") is True
          and rp.get("numericWeightsDefined") is False
          and rp.get("scoresDefined") is False and rp.get("ratiosDefined") is False)
    nw = c.get("numericWeighting", {})
    check("    every numeric question is recorded as undefined",
          all(v is False for v in nw.values() if isinstance(v, bool))
          and len([v for v in nw.values() if isinstance(v, bool)]) == 9,
          str([k for k, v in nw.items() if v is True]))

    mv = c.get("metricVocabulary", {})
    check("23. the priority-signal vocabulary is closed and exactly the nine locked signals",
          mv.get("prioritySignalIdIsClosed") is True
          and mv.get("prioritySignalIds") == PRIORITY, str(mv.get("prioritySignalIds")))
    check("    the source-native vocabulary is deliberately open",
          mv.get("sourceNativeMetricIdIsClosed") is False)
    check("    an unknown source metric may not be silently tiered",
          mv.get("unknownSourceMetricMayBeTieredSilently") is False)

    cm = c.get("creativeMechanismModel", {})
    check("24. a winner reading is interpretation, not truth",
          cm.get("assessmentIsInterpretation") is True
          and cm.get("assessmentTruthClass") == "INTERPRETATION")
    check("    a winning mechanism may be exploited temporarily",
          cm.get("winnerMayBeExploitedTemporarily") is True
          and cm.get("exploitationIsTemporary") is True)
    check("25. one result may not establish a permanent rule",
          cm.get("oneResultEstablishesPermanentRule") is False
          and cm.get("winnerBecomesPermanentCreativeTruth") is False)
    check("    a winner is not Product Truth, not Human Identity and does not alter Story State",
          cm.get("winnerIsProductTruth") is False
          and cm.get("winnerIsHumanIdentityTruth") is False
          and cm.get("winnerAltersStoryStateAutomatically") is False)
    check("    no numeric winner score is required or defined",
          cm.get("numericWinnerScoreRequired") is False
          and cm.get("numericWinnerScoreDefined") is False)

    fm = c.get("fatigueModel", {})
    check("26. fatigue MUST be tracked before repetitive continuation",
          fm.get("trackingRequiredBeforeRepetitiveContinuation") is True)
    check("    fatigue is interpretation, not a raw metric",
          fm.get("fatigueIsInterpretation") is True
          and fm.get("fatigueTruthClass") == "INTERPRETATION"
          and fm.get("fatigueIsRawMetric") is False)
    check("27. no numeric fatigue threshold is invented",
          fm.get("numericThresholdDefined") is False)
    check("28. no cooldown duration is invented", fm.get("cooldownDurationDefined") is False)
    check("    and no closed fatigue taxonomy is invented for schema convenience",
          fm.get("closedStatusTaxonomyDefined") is False)
    fatigue_nums = [p for v, p in walk_values(fm)
                    if isinstance(v, (int, float)) and not isinstance(v, bool)]
    check("    no number appears anywhere in the fatigue model", not fatigue_nums,
          str(fatigue_nums))

    print("\nF. story actions, audience, interfaces and automation")
    sar = c.get("storyActionRecommendation", {})
    check("29. story actions are contract 03's exact vocabulary",
          sar.get("actions") == ARCS, str(sar.get("actions")))
    dep03_actions = [a.get("actionId") for a in dep03.get("storyArcActions", [])]
    check("    and they match contract 03's own list, read from contract 03",
          sar.get("actions") == dep03_actions, str(dep03_actions))
    check("    contract 03 is named as their owner",
          sar.get("actionVocabularyOwnedBy") == "03"
          and sar.get("actionVocabularyOwnerContract") == dep03.get("contractId"))
    check("    contract 04 does not redefine their narrative meaning",
          sar.get("vocabularyRedefinedHere") is False
          and sar.get("narrativeMeaningDefinedHere") is False)
    check("30. recommendation is not a Story State transition",
          sar.get("mayRecommendAction") is True and sar.get("mayPerformTransition") is False
          and sar.get("recommendationIsTransition") is False
          and sar.get("storyTransitionAuthorityGranted") is False
          and sar.get("truthClassOfRecommendation") == "PROPOSAL")

    ab = c.get("audienceToCanonBoundary", {})
    check("31. audience evidence may support a proposal",
          ab.get("maySupportProposal") is True and ab.get("mayRecommendStoryAction") is True
          and ab.get("mayIdentifySupportForDevelopment") is True)
    check("    and may never directly mutate canon",
          ab.get("mayDirectlyRewriteStoryState") is False
          and ab.get("audienceVotingIsAutomaticallyBinding") is False
          and ab.get("thresholdBasedCanonPromotionDefined") is False)
    check("    engagement is not approval", ab.get("engagementIsApproval") is False)
    dep03_id = dep03.get("contractId", "")
    check("    the boundary is inherited from contract 03 rather than reinvented",
          bool(dep03_id) and ab.get("inheritedFrom", "").startswith(dep03_id)
          and dep03.get("audienceInfluence", {}).get("maySilentlyMutateCanon") is False
          and dep03.get("audienceInfluence", {}).get("mayAffectLaterCanon")
          == ab.get("audienceEvidenceMayAffectLaterCanon"))
    check("    contract 03 deferred exactly this to contract 04",
          dep03.get("audienceInfluence", {}).get("deferredTo") == "04")

    ci = c.get("campaignContextInterface", {})
    check("32. the campaign-context handoff stays evidence and proposal",
          ci.get("outputTruthClasses") == ["INTERPRETATION", "PROPOSAL"]
          and ci.get("outputClass") == "SOCIAL_OR_CULTURAL_SIGNAL")
    check("    it becomes neither truth, approval nor publication authority",
          ci.get("becomesProductTruth") is False and ci.get("becomesHumanIdentityTruth") is False
          and ci.get("becomesApproval") is False
          and ci.get("becomesPublicationAuthority") is False)
    check("    and contract 01 is not modified",
          ci.get("modifiesContract01") is False
          and "MUST NOT be treated as authority" in " ".join(dep01.get("signalRules", [])))
    sb = c.get("superBrainInterface", {})
    check("33. Super Brain is secondary evidence for interpretation only",
          sb.get("superBrainIsSecondaryEvidenceForInterpretation") is True
          and sb.get("superBrainIsRawMetricAuthority") is False
          and sb.get("superBrainMayOverwriteRawMetricFact") is False)
    check("    memory schema and write policy are deferred to contract 07",
          sb.get("deferredTo") == "07"
          and sb.get("memorySchemaDefinedHere") is False
          and sb.get("memoryGraphDefinedHere") is False
          and sb.get("durableLearningWritePolicyDefinedHere") is False
          and sb.get("preferenceDriftImplementationDefinedHere") is False)
    au = c.get("automationBoundary", {})
    check("34. priority informs interpretation and authorises no action",
          all(au.get(k) is False for k in
              ("priorityImpliesAutomation", "automaticStoryChangeAuthorised",
               "automaticCampaignSelectionAuthorised", "automaticPublicationAuthorised",
               "automaticSpendAuthorised", "automaticRetryAuthorised",
               "automaticBudgetEscalationAuthorised")),
          str([k for k, v in au.items() if v is True]))
    check("    autonomy is owned by contract 06", au.get("autonomyOwnedBy") == "06")

    print("\nG. missingness, normalisation, provenance and privacy")
    mm = c.get("missingnessModel", {})
    check("35. availability distinguishes zero from every kind of absence",
          mm.get("availabilityStates") == AVAIL, str(mm.get("availabilityStates")))
    check("36. a missing metric may not silently become zero",
          mm.get("missingMayBecomeZero") is False and mm.get("zeroMeansMeasuredZero") is True
          and mm.get("valuePermittedOnlyWhenAvailable") is True)
    check("    and nothing may be fabricated in its place",
          mm.get("fabricationPermitted") is False)
    check("    every availability state carries a definition",
          [d.get("state") for d in mm.get("stateDefinitions", [])] == AVAIL)
    nm = c.get("normalisationModel", {})
    check("37. cross-platform normalisation is left open, not pretended",
          nm.get("crossPlatformNormalisationDefined") is False
          and nm.get("shareOnOnePlatformEqualsSendOnAnother") is False)
    check("    a derived fact requires a published deterministic rule",
          nm.get("derivedFactRequiresPublishedDeterministicRule") is True
          and nm.get("derivedWithoutPublishedRuleIs") == "INTERPRETATION")
    check("    source-native metrics and their provenance are preserved",
          nm.get("sourceNativeMetricsPreserved") is True and nm.get("provenanceRetained") is True)

    prov = " ".join(c.get("provenanceRules", []))
    check("38. provenance is mandatory for every raw metric",
          all(t in prov for t in ("which authority produced it", "which subject it refers to",
                                  "which metric it represents", "which observation or window")))
    check("39. an interpretation must reference its evidence",
          "Every interpretation MUST reference the evidence" in prov)
    check("    a recommendation must reference its interpretations or evidence",
          "Every recommendation MUST reference the interpretations or evidence" in prov)
    check("    an unsupported recommendation may not be recorded",
          "no supporting reference MUST NOT be recorded" in prov)
    check("    a reference is explicitly not a grant of authority",
          "not a grant of authority" in prov)
    check("    every reference must resolve to exactly one record in the same snapshot",
          "MUST resolve to exactly one record present in the same snapshot" in prov)
    check("    and a non-empty string is explicitly not evidence",
          "non-empty string is not evidence" in prov)

    ri = c.get("referenceIntegrity", {})
    check("39a. identifiers share one space per snapshot and are unique across it",
          ri.get("identifierSpace") == "SNAPSHOT_GLOBAL"
          and ri.get("identifiersUniqueWithinSnapshot") is True)
    check("    identifiers stay opaque and no global format is defined",
          ri.get("referencesAreOpaque") is True and ri.get("identifierFormatDefined") is False)
    idf = {x.get("recordKind"): x for x in ri.get("identifierFields", [])}
    check("    all four record kinds declare their collection and identifier field",
          {k: (v.get("collection"), v.get("identifierField")) for k, v in idf.items()}
          == {kind: (arr, field) for arr, (field, kind) in ID_FIELDS.items()},
          str(sorted(idf)))
    pt = {x.get("referringRecordKind"): x.get("mayReference") for x in ri.get("permittedTargets", [])}
    check("39b. the permitted reference targets match what the checker enforces",
          pt == {"INTERPRETATION": [RAW], "CREATIVE_MECHANISM_ASSESSMENT": [RAW, INTERP],
                 "FATIGUE_ASSESSMENT": [RAW, INTERP],
                 "RECOMMENDATION": [RAW, INTERP]}, str(pt))
    check("    and they are unchanged from the reviewed base: this correction adds "
          "resolution, not a wider target set",
          all(tuple(pt[k]) == REF_TARGETS[a] for a, k in
              (("interpretations", "INTERPRETATION"),
               ("creativeMechanismAssessments", "CREATIVE_MECHANISM_ASSESSMENT"),
               ("fatigueAssessment", "FATIGUE_ASSESSMENT"),
               ("recommendations", "RECOMMENDATION"))), str(pt))
    check("    nothing may rest on a recommendation or on a mechanism assessment",
          ri.get("referenceToRecommendationPermitted") is False
          and ri.get("referenceToMechanismAssessmentPermitted") is False
          and all(REC not in v and MECH not in v for v in pt.values()))
    check("    a cited interpretation must itself be grounded in raw evidence",
          ri.get("citedInterpretationMustBeGrounded") is True)
    check("    an unresolved reference is not permitted",
          ri.get("unresolvedReferencePermitted") is False
          and ri.get("nonEmptyStringIsSufficientEvidence") is False)

    vm = c.get("validationModel", {})
    check("39c. snapshot acceptance requires BOTH validation layers",
          vm.get("snapshotAcceptanceRequires")
          == ["JSON_SCHEMA_VALIDATION", "SEMANTIC_REFERENCE_INTEGRITY_VALIDATION"]
          and vm.get("schemaValidationAloneIsSufficient") is False)
    # The contract must not overclaim what a schema engine can do for it.
    check("    and the contract does NOT claim JSON Schema enforces resolution or uniqueness",
          vm.get("jsonSchemaEnforcesCrossRecordResolution") is False
          and vm.get("jsonSchemaEnforcesIdentifierUniqueness") is False
          and ri.get("enforceableByJsonSchemaAlone") is False)
    check("    the committed validator stays standard-library only",
          vm.get("committedValidatorUsesStandardLibraryOnly") is True)
    check("    the object schema states its own scope rather than implying completeness",
          "NECESSARY BUT NOT SUFFICIENT" in obj.get("description", "")
          and "cross-record resolution" in obj.get("description", ""))
    for f in ("UNRESOLVED_EVIDENCE_REFERENCE", "AMBIGUOUS_RECORD_IDENTIFIER",
              "REFERENCE_TO_INAPPROPRIATE_RECORD_KIND"):
        check(f"    named as a hard failure: {f}",
              f in {x.get("failureId") for x in c.get("hardFailures", [])})

    priv = " ".join(c.get("privacyRules", []))
    check("40. the contract states this repository is PUBLIC", "PUBLIC" in priv)
    for term, label in (("Real social account metrics", "real account metrics"),
                        ("campaign performance history", "real performance history"),
                        ("private audience history", "private audience history"),
                        ("Direct message contents", "DM contents"),
                        ("customer or user identity", "customer identity"),
                        ("credentials", "credentials and tokens"),
                        ("private ops layer", "private-ops content kept out of this repo")):
        check(f"    barred: {label}", term in priv)
    check("41. a real snapshot is barred from this public repository by standing policy",
          "MUST NOT be persisted in this public repository" in priv)
    sio = c.get("socialIntelligenceObject", {})
    check("    the object block states the same policy and exempts synthetic fixtures",
          sio.get("publicRepositoryInstancePersistenceAllowed") is False
          and "standing policy" in sio.get("note", "")
          and "Synthetic fixtures" in sio.get("note", ""))
    check("    the snapshot is not a product-truth, identity or story-state record",
          sio.get("isProductTruthRecord") is False and sio.get("isHumanIdentityRecord") is False
          and sio.get("isStoryStateRecord") is False)
    check("    references are opaque and no persistent ID format is defined here",
          sio.get("referencesAreOpaque") is True and sio.get("persistentIdFormatDefined") is False)
    # Deliberately a KEY scan, not a grep of the serialized document: a privacy
    # rule that forbids credentials necessarily contains the word, and a document
    # saying "MUST NOT" must never read as the thing being present.
    priv_hits = [p for k, p in walk_keys(c) if k in PRIVATE_KEYS]
    check("42. no private operational field is carried by this contract set",
          not priv_hits, str(priv_hits))
    fails = {f.get("failureId") for f in c.get("hardFailures", [])}
    for f in ("MISSING_METRIC_RECORDED_AS_ZERO", "UNSUPPORTED_RECOMMENDATION",
              "PRIVATE_PERFORMANCE_DATA_IN_PUBLIC_STATE", "ENGAGEMENT_TREATED_AS_APPROVAL",
              "WINNER_TREATED_AS_PERMANENT_RULE", "INVENTED_NUMERIC_THRESHOLD"):
        check(f"    named as a hard failure: {f}", f in fails)
    check("    every hard failure is HARD_FAIL",
          all(f.get("severity") == "HARD_FAIL" for f in c.get("hardFailures", [])))

    print("\nH. schema structure (read from the schema documents, not their prose)")

    def _rules(node, key):
        """allOf entries whose `contains` pins `key`, split by shape.

        An identity rule constrains the key alone with min=max=1, proving the id
        appears exactly once. A binding rule pins a second field with minContains
        only: paired with the identity rule it proves THE one record with that id
        carries that value. maxContains on a binding rule would be weaker, not
        stronger, because a non-matching duplicate would satisfy it.
        """
        ids, binds = {}, {}
        for rule in node.get("allOf", []) if isinstance(node, dict) else []:
            con = rule.get("contains", {})
            props = con.get("properties", {})
            if key not in props or "const" not in props[key]:
                continue
            val = props[key]["const"]
            others = [p for p in props if p != key]
            if not others and rule.get("minContains") == 1 and rule.get("maxContains") == 1:
                ids[val] = True
            elif others and rule.get("minContains") == 1 and "maxContains" not in rule:
                binds.setdefault(val, {})[others[0]] = props[others[0]]
        return ids, binds

    def admits(node, token):
        """True if the schema node ALLOWS `token` as a value.

        Deliberately blind to description, title and $comment: a description
        explaining that a value is forbidden must not read as the value being
        allowed, which is exactly the false positive that made an earlier
        json.dumps grep useless here.
        """
        if not isinstance(node, dict):
            return False
        if node.get("const") == token:
            return True
        if token in (node.get("enum") or []):
            return True
        if node.get("default") == token:
            return True
        return any(admits(v, token) for k, v in node.items()
                   if k not in ("description", "title", "$comment")
                   and isinstance(v, (dict, list)))\
            or any(admits(v, token) for v in node.values() if isinstance(v, list)
                   for v in v if isinstance(v, dict))

    sp = schema.get("properties", {})
    check("43. the contract schema governs exactly the contract's own keys",
          sorted(sp) == sorted(c) and sorted(schema.get("required", [])) == sorted(c),
          f"schema-only={sorted(set(sp) - set(c))} contract-only={sorted(set(c) - set(sp))}")
    check("    and is closed at the top level", schema.get("additionalProperties") is False)
    # `contains`, `if`, `then`, `else` and `not` are APPLICATOR positions: they
    # constrain a shape rather than define an object, so they are supposed to stay
    # open. Only real object definitions must be closed.
    APPLICATOR = (".contains", ".if", ".then", ".else", ".not")

    def open_objects(node, path="$", acc=None):
        acc = [] if acc is None else acc
        if isinstance(node, dict):
            if "properties" in node and node.get("additionalProperties") is not False \
               and not any(a in path for a in APPLICATOR):
                acc.append(path)
            for k, v in node.items():
                open_objects(v, f"{path}.{k}", acc)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                open_objects(v, f"{path}[{i}]", acc)
        return acc
    open_c = open_objects(schema)
    check("    every governed object in the contract schema is closed", not open_c, str(open_c[:4]))
    open_o = open_objects(obj)
    check("    every governed object in the object schema is closed too", not open_o, str(open_o[:4]))

    tier_ids, tier_binds = _rules(sp.get("responsePriority", {}).get("properties", {})
                                  .get("tiers", {}), "tierId")
    check("44. the schema pins all three tiers by identity", sorted(tier_ids) == sorted(TIERS),
          str(sorted(tier_ids)))
    for tid, sigs in TIERS.items():
        sig_rule = tier_binds.get(tid, {}).get("signals", {})
        got = [r.get("contains", {}).get("const") for r in sig_rule.get("allOf", [])]
        check(f"    the schema binds {tid} to exactly {sigs}",
              sorted(got) == sorted(sigs) and sig_rule.get("minItems") == len(sigs)
              and sig_rule.get("maxItems") == len(sigs), str(sorted(got)))
    layer_ids, layer_binds = _rules(sp.get("coreSeparation", {}).get("properties", {})
                                    .get("layers", {}), "layerId")
    check("45. the schema pins all seven separation layers by identity",
          sorted(layer_ids) == sorted(LAYERS), str(sorted(layer_ids)))
    check("    and binds each layer's truth class and authority",
          all("truthClass" in layer_binds.get(l, {}) and "authority" in layer_binds.get(l, {})
              for l in LAYERS),
          str([l for l in LAYERS if "truthClass" not in layer_binds.get(l, {})]))
    check("    and binds every layer to ownedHere false",
          all(layer_binds.get(l, {}).get("ownedHere", {}).get("const") is False for l in LAYERS))

    op = obj.get("properties", {})
    raw_item = op.get("rawEvidence", {}).get("items", {})
    int_item = op.get("interpretations", {}).get("items", {})
    mech_item = op.get("creativeMechanismAssessments", {}).get("items", {})
    rec_item = op.get("recommendations", {}).get("items", {})
    check("46. the object schema separates evidence, interpretation and recommendation",
          all(k in op for k in ("rawEvidence", "interpretations", "recommendations"))
          and all(k in obj.get("required", []) for k in
                  ("rawEvidence", "interpretations", "recommendations")))
    sa_node = raw_item.get("properties", {}).get("sourceAuthority", {})
    check("47. a raw metric may not name the Social Intelligence Engine as its authority",
          not admits(sa_node, "SOCIAL_INTELLIGENCE_ENGINE")
          and sorted(sa_node.get("enum", [])) == sorted(RAW_AUTHORITIES),
          str(sa_node.get("enum")))
    check("    nor Super Brain, nor chat history",
          not admits(sa_node, "SUPER_BRAIN") and not admits(sa_node, "CHAT_HISTORY"))
    tc_node = raw_item.get("properties", {}).get("truthClass", {})
    check("48. raw evidence cannot be labelled INTERPRETATION",
          not admits(tc_node, "INTERPRETATION")
          and sorted(tc_node.get("enum", [])) == ["DERIVED_FACT", "FACT"], str(tc_node.get("enum")))
    av_node = raw_item.get("properties", {}).get("availability", {})
    check("49. the object schema carries all five availability states",
          sorted(av_node.get("enum", [])) == sorted(AVAIL), str(av_node.get("enum")))
    # The rule that keeps a missing metric from becoming a number: BOTH directions.
    branches = raw_item.get("allOf", [])
    avail_branch = next((b for b in branches
                         if b.get("if", {}).get("properties", {})
                         .get("availability", {}).get("const") == "AVAILABLE"), None)
    check("50. AVAILABLE requires an observed value",
          avail_branch is not None
          and "observedValue" in avail_branch.get("then", {}).get("required", []))
    check("    and every other availability state FORBIDS one outright",
          avail_branch is not None
          and avail_branch.get("else", {}).get("not", {}).get("required") == ["observedValue"],
          "the else branch is what makes missing != zero structural")
    deriv_branch = next((b for b in branches
                         if b.get("if", {}).get("properties", {})
                         .get("truthClass", {}).get("const") == "DERIVED_FACT"), None)
    check("51. a DERIVED_FACT requires its published derivation rule",
          deriv_branch is not None
          and "derivationRuleRef" in deriv_branch.get("then", {}).get("required", []))
    mi = raw_item.get("properties", {}).get("metricIdentity", {})
    check("52. a record carries exactly one of the closed or the open metric id",
          len(mi.get("oneOf", [])) == 2)
    check("    the closed vocabulary is exactly the nine locked signals",
          sorted(mi.get("properties", {}).get("prioritySignalId", {}).get("enum", []))
          == sorted(PRIORITY))
    native_branch = next((b for b in mi.get("allOf", [])
                          if b.get("if", {}).get("required") == ["sourceNativeMetricId"]), None)
    check("53. an open provider metric may not be placed in a priority tier",
          native_branch is not None
          and native_branch.get("then", {}).get("not", {}).get("required") == ["priorityTierRef"])
    tier_branches = {b.get("then", {}).get("properties", {}).get("priorityTierRef", {}).get("const"):
                     b.get("if", {}).get("properties", {}).get("prioritySignalId", {}).get("enum")
                     for b in mi.get("allOf", []) if "then" in b
                     and "priorityTierRef" in b.get("then", {}).get("properties", {})}
    check("    and a known signal is bound to its own tier, not any tier",
          all(sorted(tier_branches.get(t) or []) == sorted(s) for t, s in TIERS.items()),
          str(tier_branches))
    check("54. an interpretation is closed to INTERPRETATION",
          int_item.get("properties", {}).get("truthClass", {}).get("const") == "INTERPRETATION")
    check("    and cannot be labelled FACT, APPROVAL or STORY_CANON",
          not any(admits(int_item.get("properties", {}).get("truthClass", {}), t)
                  for t in ("FACT", "DERIVED_FACT", "APPROVAL", "STORY_CANON")))
    check("    and must reference at least one piece of evidence",
          int_item.get("properties", {}).get("evidenceRefs", {}).get("minItems") == 1
          and "evidenceRefs" in int_item.get("required", []))
    def constrains(node, *keys):
        """Whether the schema STRUCTURALLY uses any of `keys`, ignoring prose.

        A description explaining that a closed taxonomy is deliberately absent
        contains the words "enum" and "number"; grepping the serialized node
        therefore reports the opposite of the truth.
        """
        if isinstance(node, dict):
            if any(k in node for k in keys):
                return True
            return any(constrains(v, *keys) for k, v in node.items()
                       if k not in ("description", "title", "$comment"))
        if isinstance(node, list):
            return any(constrains(v, *keys) for v in node)
        return False

    def numeric_typed(node):
        """Whether the schema admits a numeric value anywhere, prose ignored."""
        if isinstance(node, dict):
            if node.get("type") in ("number", "integer"):
                return True
            return any(numeric_typed(v) for k, v in node.items()
                       if k not in ("description", "title", "$comment"))
        if isinstance(node, list):
            return any(numeric_typed(v) for v in node)
        return False
    conf = int_item.get("properties", {}).get("confidence", {})
    check("    confidence stays extensible rather than a closed taxonomy or a number",
          bool(conf.get("properties")) and not constrains(conf, "enum")
          and not numeric_typed(conf),
          str(list(conf.get("properties", {}))))
    check("55. a recommendation is closed to PROPOSAL",
          rec_item.get("properties", {}).get("truthClass", {}).get("const") == "PROPOSAL")
    check("    and cannot be labelled APPROVAL, FACT, STORY_CANON or PUBLICATION",
          not any(admits(rec_item.get("properties", {}).get("truthClass", {}), t)
                  for t in ("APPROVAL", "FACT", "DERIVED_FACT", "STORY_CANON", "PUBLICATION")))
    check("    it claims no authority, explicitly rather than by silence",
          rec_item.get("properties", {}).get("authorityClaimed", {}).get("const") == "NONE")
    check("56. a recommendation must carry provenance",
          rec_item.get("properties", {}).get("evidenceRefs", {}).get("minItems") == 1
          and "evidenceRefs" in rec_item.get("required", []))
    sa_item = rec_item.get("properties", {}).get("storyAction", {})
    check("57. a story recommendation uses contract 03's five actions and nothing else",
          sorted(sa_item.get("properties", {}).get("action", {}).get("enum", [])) == sorted(ARCS),
          str(sa_item.get("properties", {}).get("action", {}).get("enum")))
    check("    and is structurally barred from being a transition",
          sa_item.get("properties", {}).get("isStoryStateTransition", {}).get("const") is False
          and sa_item.get("properties", {}).get("transitionAuthorityGranted", {}).get("const") is False
          and sa_item.get("properties", {}).get("redefinesNarrativeMeaning", {}).get("const") is False)
    mp = mech_item.get("properties", {})
    check("58. a winner assessment is interpretation and temporary",
          mp.get("truthClass", {}).get("const") == "INTERPRETATION"
          and mp.get("exploitationIsTemporary", {}).get("const") is True)
    check("    and structurally cannot establish permanent truth",
          all(mp.get(k, {}).get("const") is False for k in
              ("establishesPermanentCreativeRule", "establishesProductTruth",
               "establishesHumanIdentityTruth", "altersStoryState")))
    fa_node = op.get("fatigueAssessment", {})
    check("59. fatigue is required and cannot record that it was skipped",
          "fatigueAssessment" in obj.get("required", [])
          and fa_node.get("properties", {}).get("considered", {}).get("const") is True)
    check("    fatigue carries no threshold or cooldown field",
          not any(k.lower() in {w.lower() for w in WEIGHT_KEYS}
                  for k in fa_node.get("properties", {})),
          str(list(fa_node.get("properties", {}))))
    exploit_branch = [b for b in obj.get("allOf", [])
                      if "fatigueAssessment" in json.dumps(b.get("then", {}))]
    check("60. recommending continued exploitation requires fatigue evidence",
          any("exploitationRecommended" in json.dumps(b.get("if", {})) for b in exploit_branch))
    check("    and a CONTINUE story recommendation requires it too",
          any('"CONTINUE"' in json.dumps(b.get("if", {})) for b in exploit_branch))
    # These descriptions drifted out of agreement with REF_TARGETS once already,
    # silently, because nothing compared them. Check them against the one source
    # of truth rather than re-reading them by eye.
    _DESC_SITES = {
        "interpretations": op.get("interpretations", {}).get("items", {})
                             .get("properties", {}).get("evidenceRefs", {}),
        "creativeMechanismAssessments": op.get("creativeMechanismAssessments", {}).get("items", {})
                             .get("properties", {}).get("evidenceRefs", {}),
        "fatigueAssessment": op.get("fatigueAssessment", {})
                             .get("properties", {}).get("evidenceRefs", {}),
        "recommendations": op.get("recommendations", {}).get("items", {})
                             .get("properties", {}).get("evidenceRefs", {}),
    }
    _drift = []
    for _arr, _node in _DESC_SITES.items():
        _d = _node.get("description", "")
        _permits_interp = "OR one interpretation record" in _d
        if _permits_interp != (INTERP in REF_TARGETS[_arr]):
            _drift.append(f"{_arr}: description permits interpretation={_permits_interp}, "
                          f"REF_TARGETS says {INTERP in REF_TARGETS[_arr]}")
        if "creative mechanism assessment or a recommendation" not in _d and \
           "may NOT cite another interpretation, a creative mechanism assessment" not in _d:
            _drift.append(f"{_arr}: description does not bar citing an assessment or a recommendation")
    check("60a. the object schema's reference descriptions agree with REF_TARGETS",
          not _drift, str(_drift))
    check("    and every one of them states that resolution is semantic-only",
          all("checked by semantic reference-integrity validation" in n.get("description", "")
              for n in _DESC_SITES.values()),
          str([a for a, n in _DESC_SITES.items()
               if "checked by semantic reference-integrity validation" not in n.get("description", "")]))

    check("61. the snapshot asserts nothing outside its authority",
          op.get("assertionsOutsideAuthority", {}).get("maxItems") == 0
          and "assertionsOutsideAuthority" in obj.get("required", []))
    check("    and the object schema is closed at the top level",
          obj.get("additionalProperties") is False)

    print("\nI. synthetic runtime fixtures — targeted semantic checker, NOT a JSON Schema engine")
    base = valid_snapshot()
    errs = check_snapshot(base)
    check("62. the synthetic positive snapshot is accepted", not errs, str(errs[:3]))
    check("    it carries a tier-1, a tier-2 and a lower-priority signal",
          {"SHARES"} <= {r["metricIdentity"].get("prioritySignalId") for r in base["rawEvidence"]}
          and {"SAVES"} <= {r["metricIdentity"].get("prioritySignalId") for r in base["rawEvidence"]}
          and {"VIEWS"} <= {r["metricIdentity"].get("prioritySignalId") for r in base["rawEvidence"]})
    check("    it carries an untiered source-native metric",
          any("sourceNativeMetricId" in r["metricIdentity"] and "priorityTierRef" not in r["metricIdentity"]
              for r in base["rawEvidence"]))
    check("    it carries one interpretation, one mechanism assessment and one proposal",
          len(base["interpretations"]) == 1 and len(base["creativeMechanismAssessments"]) == 1
          and len(base["recommendations"]) == 1
          and base["recommendations"][0]["truthClass"] == "PROPOSAL")
    check("    fatigue is explicitly considered with evidence",
          base["fatigueAssessment"]["considered"] is True
          and bool(base["fatigueAssessment"]["evidenceRefs"]))
    check("    every reference in it resolves", not [r for r in base["interpretations"][0]["evidenceRefs"]
          if r not in {e["evidenceRef"] for e in base["rawEvidence"]}])
    check("    it contains no private account, message or credential field",
          not any(k in PRIVATE_KEYS for k, _ in walk_keys(base)))

    def rejects(label, fn, needle=None, base_doc=None):
        e = check_snapshot(mutate(fn, base_doc))
        ok = bool(e) and (needle is None or any(needle in x for x in e))
        check(label, ok, "ACCEPTED" if not e else f"wrong reason: {e[:2]}")

    def set_auth(sn):    sn["rawEvidence"][0]["sourceAuthority"] = "SOCIAL_INTELLIGENCE_ENGINE"
    def raw_interp(sn):  sn["rawEvidence"][0]["truthClass"] = "INTERPRETATION"
    def int_fact(sn):    sn["interpretations"][0]["truthClass"] = "FACT"
    def rec_appr(sn):    sn["recommendations"][0]["truthClass"] = "APPROVAL"
    def rec_canon(sn):   sn["recommendations"][0]["truthClass"] = "STORY_CANON"
    def rec_noev(sn):    sn["recommendations"][0]["evidenceRefs"] = []
    def miss_zero(sn):   sn["rawEvidence"][2]["observedValue"] = 0
    def weight_share(sn):sn["rawEvidence"][0]["weight"] = 10
    def weight_like(sn):
        sn["rawEvidence"][2]["metricIdentity"]["prioritySignalId"] = "LIKES"
        sn["rawEvidence"][2]["weight"] = 1
    def tier_unknown(sn):sn["rawEvidence"][3]["metricIdentity"]["priorityTierRef"] = "TIER_PRIMARY"
    def tier_wrong(sn):  sn["rawEvidence"][1]["metricIdentity"]["priorityTierRef"] = "TIER_PRIMARY"
    def bad_action(sn):  sn["recommendations"][0]["storyAction"]["action"] = "RETCON"
    def canon_auth(sn):  sn["recommendations"][0]["storyAction"]["isStoryStateTransition"] = True
    def fatigue_skip(sn):sn["fatigueAssessment"]["evidenceRefs"] = []
    def fatigue_off(sn): sn["fatigueAssessment"]["considered"] = False
    def fatigue_thr(sn): sn["fatigueAssessment"]["threshold"] = 3
    def cooldown(sn):    sn["fatigueAssessment"]["cooldownDays"] = 7
    def winner_perm(sn): sn["creativeMechanismAssessments"][0]["establishesPermanentCreativeRule"] = True
    def prod_truth(sn):  sn["creativeMechanismAssessments"][0]["establishesProductTruth"] = True
    def human_id(sn):    sn["creativeMechanismAssessments"][0]["establishesHumanIdentityTruth"] = True
    def private_f(sn):   sn["rawEvidence"][0]["accountHandle"] = "synthetic-handle"
    def unknown_top(sn): sn["socialApiExists"] = False
    def assert_out(sn):  sn["assertionsOutsideAuthority"] = ["PM-038 price is wrong"]
    def emitter_auth(sn):sn["provenance"]["generatedByIsRawMetricAuthority"] = True

    rejects("63. raw metric authority = SOCIAL_INTELLIGENCE_ENGINE", set_auth, "not a raw-metric authority")
    rejects("64. raw evidence labelled INTERPRETATION", raw_interp, "not measured evidence")
    rejects("65. interpretation labelled FACT", int_fact, "MUST NOT be recorded as fact")
    rejects("66. recommendation labelled APPROVAL", rec_appr, "never an approval")
    rejects("67. recommendation labelled STORY_CANON", rec_canon, "never an approval")
    rejects("68. recommendation with no evidence reference", rec_noev, "unsupported")
    rejects("69. a missing metric carrying a zero", miss_zero, "missing is not zero")
    rejects("70. a numeric weight attached to SHARES", weight_share, "numeric weighting field")
    rejects("71. a numeric weight attached to LIKES", weight_like, "numeric weighting field")
    rejects("72. an unknown source metric placed in tier 1", tier_unknown, "no published mapping rule")
    rejects("    a known signal placed in the wrong tier", tier_wrong, "belongs to")
    rejects("73. a story recommendation with an unknown action", bad_action, "not in contract 03")
    rejects("74. an audience recommendation asserting a canon transition", canon_auth,
            "does not equal transition")
    rejects("75. fatigue bypassed on a repetitive winning mechanism", fatigue_skip,
            "no fatigue evidence considered")
    rejects("    fatigue recorded as not considered", fatigue_off, "MUST be tracked")
    rejects("76. an invented numeric fatigue threshold", fatigue_thr, "numeric weighting field")
    rejects("77. an invented cooldown duration", cooldown, "numeric weighting field")
    rejects("78. a winner establishing a permanent creative rule", winner_perm,
            "MUST NOT become permanent truth")
    rejects("79. Product Truth overridden by social interpretation", prod_truth,
            "MUST NOT become permanent truth")
    rejects("80. Human Identity changed by social evidence", human_id,
            "MUST NOT become permanent truth")
    rejects("81. a private account field inserted", private_f, "private operational field")
    rejects("82. an unknown top-level field", unknown_top, "unknown top-level field")
    rejects("    the snapshot asserting something outside its authority", assert_out,
            "outside its authority")
    rejects("    the emitter claiming to be the measurement authority", emitter_auth,
            "not the authority for its measurements")
    # ---- reference integrity: the review found all of these accepted ----
    import copy as _copy

    def dup_evidence(sn):
        d = _copy.deepcopy(sn["rawEvidence"][0]); d["observedValue"] = 0
        sn["rawEvidence"].append(d)

    def dup_interpretation(sn):
        d = _copy.deepcopy(sn["interpretations"][0]); d["statement"] = "the opposite conclusion"
        sn["interpretations"].append(d)

    def collide_namespaces(sn):
        sn["interpretations"][0]["interpretationRef"] = "ev-shares"
        sn["recommendations"][0]["evidenceRefs"] = ["ev-shares"]

    rejects("84. a mechanism assessment citing a reference that resolves to nothing",
            lambda sn: sn["creativeMechanismAssessments"][0].__setitem__(
                "evidenceRefs", ["missing-evidence"]), "resolves to no record")
    rejects("    an interpretation citing a reference that resolves to nothing",
            lambda sn: sn["interpretations"][0].__setitem__(
                "evidenceRefs", ["missing-evidence"]), "resolves to no record")
    rejects("    a recommendation citing a reference that resolves to nothing",
            lambda sn: sn["recommendations"][0].__setitem__(
                "evidenceRefs", ["missing-evidence"]), "resolves to no record")
    rejects("    fatigue citing a reference that resolves to nothing",
            lambda sn: sn["fatigueAssessment"].__setitem__(
                "evidenceRefs", ["missing-evidence"]), "resolves to no record")
    rejects("85. two raw evidence records answering to one identifier",
            dup_evidence, "ambiguous record identifier")
    rejects("    two interpretations answering to one identifier",
            dup_interpretation, "ambiguous record identifier")
    rejects("86. an interpretation named after a piece of evidence",
            collide_namespaces, "ambiguous record identifier")
    rejects("87. an interpretation resting on another interpretation",
            lambda sn: sn["interpretations"][0].__setitem__(
                "evidenceRefs", ["int-resonance"]), "may only cite RAW_EVIDENCE")
    rejects("88. a recommendation resting on another recommendation",
            lambda sn: sn["recommendations"][0].__setitem__(
                "evidenceRefs", ["rec-a"]), "is a RECOMMENDATION")
    # The reviewed base rejected this. Permitting it would widen the target set,
    # which no normative rule in that base supports and no reported defect needs.
    rejects("    a recommendation resting on a mechanism assessment",
            lambda sn: sn["recommendations"][0].__setitem__(
                "evidenceRefs", ["mech-a"]), "is a CREATIVE_MECHANISM_ASSESSMENT")
    # Grounding: asserted as a PROPERTY, not as a unique counterexample. Every
    # shape of un-grounded interpretation is already rejected by the rule above,
    # so no fixture isolates this branch; what matters is that the guarantee holds.
    for _shape, _refs in (("empty", []), ("unresolved", ["nope"]),
                          ("cites an interpretation", ["int-resonance"]),
                          ("cites a recommendation", ["rec-a"])):
        _sn = mutate(lambda sn, r=_refs: (
            sn["interpretations"].append(
                {"interpretationRef": "int-ungrounded", "kind": "resonance",
                 "statement": "ungrounded reading", "truthClass": "INTERPRETATION",
                 "evidenceRefs": r}),
            sn["fatigueAssessment"].__setitem__("evidenceRefs", ["int-ungrounded"]))[0] and None)
        _e = check_snapshot(_sn)
        check(f"    an interpretation grounded in nothing ({_shape}) cannot be cited as support",
              bool(_e) and any("not itself grounded" in x for x in _e), str(_e[:1]))
    check("    every interpretation cited as support rests on resolvable raw evidence",
          all(any(r in {x["evidenceRef"] for x in valid_snapshot()["rawEvidence"]}
                  for r in it["evidenceRefs"])
              for it in valid_snapshot()["interpretations"]))
    rejects("    a reference that is not a usable identifier",
            lambda sn: sn["interpretations"][0].__setitem__("evidenceRefs", [""]),
            "not a usable identifier")
    rejects("    a record with no usable identifier of its own",
            lambda sn: sn["rawEvidence"][0].__setitem__("evidenceRef", ""),
            "no usable evidenceRef")

    # ---- positive controls: the rules must not over-reject ----
    def accepts(label, fn):
        e = check_snapshot(mutate(fn))
        check(label, not e, str(e[:2]))

    accepts("89. distinct identifiers across all four collections are accepted",
            lambda sn: None)
    accepts("    several records citing the SAME valid evidence are accepted",
            lambda sn: [sn["interpretations"][0].__setitem__("evidenceRefs",
                        ["ev-shares", "ev-shares", "ev-saves"]),
                        sn["creativeMechanismAssessments"][0].__setitem__(
                            "evidenceRefs", ["ev-shares"])] and None)
    accepts("    a legitimate missing-data record is still accepted",
            lambda sn: sn["rawEvidence"][2].__setitem__("availability", "UNAVAILABLE"))
    accepts("    an untiered source-native metric may be cited as evidence",
            lambda sn: sn["interpretations"][0].__setitem__("evidenceRefs", ["ev-native"]))
    # The exact case the reviewed base accepted and an earlier draft of this
    # correction wrongly rejected. It stays accepted, and the cited interpretation
    # is required to be grounded in real evidence.
    accepts("    fatigue may rest on a recorded interpretation (reviewed-base case)",
            lambda sn: sn["fatigueAssessment"].__setitem__("evidenceRefs", ["int-resonance"]))
    accepts("    a mechanism assessment may rest on a recorded interpretation",
            lambda sn: sn["creativeMechanismAssessments"][0].__setitem__(
                "evidenceRefs", ["int-resonance"]))
    accepts("    a recommendation may rest on an interpretation (reviewed-base case)",
            lambda sn: sn["recommendations"][0].__setitem__("evidenceRefs", ["int-resonance"]))
    accepts("    a recommendation may rest on evidence directly",
            lambda sn: sn["recommendations"][0].__setitem__("evidenceRefs", ["ev-shares"]))
    # A checker that raises tells a caller nothing about what is wrong. The
    # identifier pre-pass and the grounding walk both iterate collections, so a
    # collection that is not a list must still come back as a violation list.
    def returns_violations(label, fn):
        try:
            e = check_snapshot(mutate(fn))
        except Exception as exc:
            check(label, False, f"raised {type(exc).__name__}: {exc}")
            return
        check(label, bool(e), "accepted a malformed snapshot")

    for _coll in ("rawEvidence", "interpretations", "creativeMechanismAssessments",
                  "recommendations"):
        returns_violations(f"    {_coll} is not a list -> violations, not an exception",
                           lambda sn, c=_coll: sn.__setitem__(c, 1))
    returns_violations("    interpretations[0].evidenceRefs is not a list -> violations, "
                       "not an exception",
                       lambda sn: sn["interpretations"][0].__setitem__("evidenceRefs", 1))
    returns_violations("    fatigueAssessment.evidenceRefs is not a list -> violations, "
                       "not an exception",
                       lambda sn: sn["fatigueAssessment"].__setitem__("evidenceRefs", 1))
    returns_violations("    a cited interpretation with a non-list evidenceRefs -> violations",
                       lambda sn: (sn["interpretations"][0].__setitem__("evidenceRefs", 1),
                                   sn["fatigueAssessment"].__setitem__(
                                       "evidenceRefs", ["int-resonance"]))[0] and None)

    check("90. the identifier space is exactly the four record kinds the contract declares",
          sorted(k for _, (_, k) in ID_FIELDS.items()) == sorted(["RAW_EVIDENCE", "INTERPRETATION",
          "CREATIVE_MECHANISM_ASSESSMENT", "RECOMMENDATION"]))

    check("83. the positive control still passes after every negative", not check_snapshot(valid_snapshot()))

    print("\nJ. registry bookkeeping")
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, encoding="utf-8") as fh:
            index = fh.read()
        index_plain = " ".join(index.replace("*", "").replace("`", "").split()).lower()
        marker = "## Planned contracts"
        head, _, tail = index.partition(marker)
        above = [ln for ln in head.splitlines() if ln.strip().startswith("| 04 ")]
        below = [ln for ln in tail.splitlines() if ln.strip().startswith("| 04 ")]
        check("84. the index lists contract 04 in its current set",
              len(above) == 1 and "SOCIAL" in above[0].upper(), str(above))
        check("85. the index no longer lists 04 as NOT YET CREATED",
              bool(marker in index) and not below, str(below))
        check("    contracts 00-03 remain in the current set",
              all(any(ln.strip().startswith(f"| 0{i} ") for ln in head.splitlines())
                  for i in (0, 1, 2, 3)))
        # Derived from disk, never a hard-coded range: this check must not fail
        # merely because a later contract is authored.
        misplaced = []
        for i in range(5, 9):
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
        check("86. the index's current/planned split matches which contract files exist",
              not misplaced, str(misplaced))
        check("    the index names the contract-04 validator",
              "social_intelligence_contract.py" in index)
        check("    the index does not treat file existence as canonicality",
              "existence does not make it canonical" in index_plain
              or "does not assert" in index_plain)
        # Deliberately not asserted: that the index says the engine "does not exist".
        # That is a lifecycle fact the index owns and may correct the day the engine
        # is built; requiring it here would make contract 04 fail for someone else's
        # change. What must hold is the durable boundary: 04 authors, it does not build.
        check("87. the index records contract 04 as authoring only, not an implementation",
              "social intelligence" in index_plain and "authoring only" in index_plain)
    else:
        check("84. the contract index exists", False, INDEX_PATH)

    if os.path.exists(MATRIX_PATH):
        with open(MATRIX_PATH, encoding="utf-8") as fh:
            matrix = fh.read()
        mp_ = " ".join(matrix.replace("*", "").replace("`", "").replace("–", "-")
                       .replace("—", "-").split()).lower()
        authored = sorted(n for n in (f"{i:02d}" for i in range(9))
                          if glob.glob(os.path.join(CDIR, f"{n}_*_CONTRACT.json")))
        awaiting = [n for n in (f"{i:02d}" for i in range(9)) if n not in authored]
        stale = [f"{lead} {n}-08 {t}" for n in authored if n != "00"
                 for lead in ("domains", "contracts", "domain", "contract")
                 for t in ("are still awaiting", "still awaiting", "are awaiting",
                           "still await", "await")
                 if f"{lead} {n}-08 {t}" in mp_]
        check("88. the matrix makes no global claim that an authored contract is awaiting",
              not stale, f"stale={stale[:3]}")
        first = awaiting[0] if awaiting else None
        check("89. the awaiting range starts at the first genuinely unwritten contract",
              first is None or f"{first}-08" in mp_, f"expected the range to start at {first}")
        check("90. the Story Engine + Social Intelligence domain is fully authored when both exist",
              ("04" in authored and "03" in authored)
              == ("not fully authored" not in mp_.split("### 4.")[-1][:900]
                  if "### 4." in matrix else True),
              f"authored={authored}")
        check("    the matrix's own account of 04 matches disk",
              ("04" in authored) == ("04 have been authored" in mp_
                                     or "03 and 04" in mp_ or "and 04 have been" in mp_),
              f"authored={authored}")
        check("91. all eight locked interview domains are preserved",
              all(f"### {i}." in matrix for i in range(1, 9)),
              str([i for i in range(1, 9) if f"### {i}." not in matrix]))
        check("    the three states are still kept apart",
              "awaiting canonical contract" in mp_ and "genuinely open" in mp_)
        check("92. the locked Domain 4 decisions are preserved verbatim in substance",
              all(t in mp_ for t in ("remain separate", "response-priority hierarchy exists",
                                     "may be exploited temporarily", "fatigue must be tracked")),
              str([t for t in ("remain separate", "response-priority hierarchy exists",
                               "may be exploited temporarily", "fatigue must be tracked")
                   if t not in mp_]))
        check("    the private performance-history deferral is preserved",
              "private detail deferred to private ops layer" in mp_)
        check("    the genuinely open numeric questions are still recorded as open",
              all(t in mp_ for t in ("exact metric weights", "fatigue thresholds",
                                     "exploration/exploitation ratio")))
        check("93. fully authored is not confused with canonical",
              "canonical" in mp_ and ("four conditions" in mp_ or "all four" in mp_))
    else:
        check("88. the decision coverage matrix exists", False, MATRIX_PATH)

    print("\nK. lifecycle-state purity (this contract is not a census of the repository)")
    # The rule, learned the hard way in phase 1D:
    #   A contract MAY say  "this contract does not implement X".
    #   A contract MAY NOT say "X does not exist today".
    # The first is durable. The second is a cached fact a later phase falsifies.
    BANNED_KEYS = ("engineExists", "engineImplemented", "engineImplementationStatus",
                   "currentImplementationStatus", "socialApiExists", "contract05Exists",
                   "contract06Exists", "contract07Exists", "contract08Exists",
                   "privateOpsExists", "instanceCommittedHere", "instanceExists")
    SELF_SCOPED = ("implementationProvidedByThisContract", "contract04ImplementsEngine",
                   "contract04ActivatesEngine")
    ckeys = list(walk_keys(c))
    skeys = [(k, p) for k, p in walk_keys(schema) if ".properties." in p]
    okeys = [(k, p) for k, p in walk_keys(obj) if ".properties." in p]
    hits = [p for k, p in ckeys if k in BANNED_KEYS]
    check("94. the contract caches no lifecycle or existence key at any depth", not hits, str(hits))
    check("    neither schema re-admits one either",
          not [p for k, p in skeys + okeys if k in BANNED_KEYS],
          str([p for k, p in skeys + okeys if k in BANNED_KEYS]))
    SHAPE = re.compile(r"(?i)(exists|implemented|implementationstatus|iscreated|wascreated|isbuilt)")
    SHAPE_OK = {
        "$.scope.implementationProvidedByThisContract",
        "$.interpretationAuthority.contract04ImplementsEngine",
        "$.interpretationAuthority.contract04ActivatesEngine",
        "$.interpretationAuthority.implementationStateOwnedHere",
        "$.rawMetricsAuthority.implementationStateOwnedHere",
        "$.implementationStatus",                       # the block that DISCLAIMS ownership
        "$.implementationStatus.statesOwnedHere",
        "$.implementationStatus.anyImplementedHere",
        "$.implementationStatus.systemsThisContractDoesNotImplement",
        "$.responsePriority.status",                    # LOCKED, an owner decision state
    } | {f"$.deferredBoundaries[{i}].{f}" for i in range(4)
         for f in ("existenceOwnedHere", "existenceRecordedIn")}
    shaped = sorted({p for k, p in ckeys if SHAPE.search(k)} - SHAPE_OK)
    check("    every existence-shaped key is self-scoped and accounted for", not shaped, str(shaped))
    check("    the self-scoped implementation facts are present and false",
          c.get("scope", {}).get("implementationProvidedByThisContract") is False
          and c.get("interpretationAuthority", {}).get("contract04ImplementsEngine") is False
          and c.get("interpretationAuthority", {}).get("contract04ActivatesEngine") is False
          and all(any(k == s for k, _ in ckeys) for s in SELF_SCOPED))
    check("95. lifecycle state is read from contract 00, not owned here",
          c.get("implementationStatus", {}).get("statesOwnedHere") is False
          and c.get("implementationStatus", {}).get("readCurrentStatesFrom")
          == "PINK_MALL_SYSTEM_AUTHORITY_CONTRACT.sourceTypes"
          and c.get("rawMetricsAuthority", {}).get("implementationStateOwnedHere") is False
          and c.get("interpretationAuthority", {}).get("implementationStateOwnedHere") is False)
    check("    this contract implements none of the systems it names",
          c.get("implementationStatus", {}).get("anyImplementedHere") is False
          and {"SOCIAL_INTELLIGENCE_ENGINE", "SOCIAL_PLATFORM_API", "SUPER_BRAIN",
               "STORY_STATE_ENGINE", "PRIVATE_OPS_STORE"}
          <= set(c.get("implementationStatus", {}).get("systemsThisContractDoesNotImplement", [])))
    # Contract 00 owns the lifecycle VALUE. This validator deliberately asserts
    # nothing about which value it holds: requiring PLANNED would turn building
    # the engine into a contract-04 failure.
    check("96. contract 00 is the registry that owns each named system's lifecycle value",
          all(any(s.get("sourceId") == sid for s in parent.get("sourceTypes", []))
              for sid in ("SOCIAL_PLATFORM_API", "SOCIAL_INTELLIGENCE_ENGINE", "SUPER_BRAIN")),
          "values intentionally unconstrained")
    LIFECYCLE = ("PLANNED", "ACTIVE", "PARTIAL", "DEPRECATED", "NOT YET CREATED")
    frozen = sorted({p for s, p in walk_values(c) if isinstance(s, str)
                     and any(re.search(rf"\b{re.escape(w)}\b", s) for w in LIFECYCLE)})
    check("97. no lifecycle value is frozen into any contract string", not frozen, str(frozen))
    # 98 — the same purity rule for the prose. These patterns match ASSERTIONS of
    # current absence, and deliberately not the disclaiming forms the contract keeps.
    FORBIDDEN_PROSE = (
        (r"no social intelligence engine exists",     "asserts the engine is absent today"),
        (r"remains planned",                          "caches a PLANNED lifecycle value"),
        (r"not yet created",                          "caches a not-created state"),
        (r"current repository state",                 "reports a snapshot of the repo"),
        (r"must not be created",                      "freezes a phase instruction as a permanent bar"),
        (r"\bno (?:contract 0\d|social platform api|super brain|story state engine|"
         r"social intelligence engine|private ops layer|pink-mall-ops)\b[^.]{0,30}\bexists\b",
                                                      "asserts a named system is absent today"),
        (r"\bcontract 0\d does not exist",            "asserts a sibling contract is absent"),
        (r"\bis (?:still )?(?:planned|unbuilt|not built)\b", "asserts an unbuilt lifecycle state"),
        (r"\bnothing (?:here )?is implemented\b",      "asserts global non-implementation"),
        (r"\bhas not (?:yet )?been (?:created|built|authored|implemented)\b",
                                                      "asserts a system has not been built yet"),
    )
    prose_hits = [why for rx, why in FORBIDDEN_PROSE if re.search(rx, low)]
    check("98. the markdown asserts no system's current lifecycle state", not prose_hits,
          str(prose_hits))
    check("    it states its own non-implementation instead",
          "this contract implements nothing" in low)
    check("    and delegates lifecycle questions to contract 00's source registry",
          "contract 00's source registry" in low)
    check("    and delegates sibling existence to the contract index",
          "system contract index.md" in low)
    check("    the private ops boundary is durable, not a creation ban",
          "does not create that layer and does not record its lifecycle state" in low)
    check("99. the existence disclaimers keep schema apart from engine",
          any("schema existing is NOT a Social Intelligence Engine existing" in d
              for d in c.get("existenceDisclaimers", []))
          and any("records no system's current lifecycle state" in d
                  for d in c.get("existenceDisclaimers", [])))

    print("\nL. human-readable agreement")
    check("100. the markdown states the core separation without collapsing it",
          "raw evidence is not a conclusion" in low and "recommendation is not approval" in low)
    check("101. the markdown names every locked priority signal", all(s in md for s in PRIORITY))
    check("102. the markdown names every story action", all(a in md for a in ARCS))
    check("103. the markdown names every hard failure",
          all(f.get("failureId") in md for f in c.get("hardFailures", [])))
    check("104. the markdown states no numeric weighting is authorised",
          "no numeric weighting is authorised" in low)
    check("    and keeps qualitative priority locked while weight stays open",
          "qualitative priority" in low and "locked" in low and "numeric weight" in low)
    check("105. the markdown states zero is a measurement and absence is not",
          "zero is a measurement" in low)
    check("106. the markdown states a schema is not an engine", "a schema is not an engine" in low)
    check("107. the markdown states recommendation does not equal transition",
          "recommendation does not equal transition" in low)
    check("108. the markdown declares open items rather than inventing answers",
          "open items" in low and "MUST NOT" in md)
    check("    and keeps the response-priority hierarchy out of the open list",
          "response-priority hierarchy is deliberately not among them" in low)
    check("109. the markdown states a non-empty string is not evidence",
          "a non-empty string is not evidence" in low)
    check("    and that every reference must resolve to exactly one record",
          "must resolve to exactly one record present in the same snapshot" in low)
    check("    and that identifiers share one space per snapshot",
          "one identifier space per snapshot" in low)
    check("    and that nothing may cite a recommendation",
          "nothing may cite a recommendation" in low)
    check("110. the markdown states both validation layers are required",
          "accepted only when both layers pass" in low)
    check("    and does NOT claim JSON Schema alone enforces resolution or uniqueness",
          "json schema alone does not enforce cross-record resolution or uniqueness" in low)
    check("    and explains why uniqueItems does not provide it",
          "uniqueitems compares whole items" in low)

    print(f"\n{len(PRIORITY)} locked priority signals in {len(TIERS)} tiers, "
          f"{len(c.get('hardFailures', []))} hard failures, "
          f"{len(c.get('nonAuthoritativeSources', []))} non-authoritative sources, "
          f"{len(c.get('openItems', []))} open items")
    print("Runtime fixtures were checked by a targeted semantic checker, not a JSON Schema engine.")
    print("Section H proves the SHAPE rules are encoded in the schema documents: required fields, "
          "closed vocabularies,")
    print("closed objects and the availability-to-value binding. Reference RESOLUTION, permitted "
          "target kind and")
    print("identifier UNIQUENESS are semantic-only — Draft 2020-12 has no keyword for them, so "
          "schema conformance")
    print("alone does not establish them and a snapshot is accepted only when both layers pass.")
    print(f"SOCIAL INTELLIGENCE CONTRACT: {'PASS' if not failed else 'FAIL'} "
          f"({passed} passed, {failed} failed)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
