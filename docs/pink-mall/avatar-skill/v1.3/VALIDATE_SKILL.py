#!/usr/bin/env python3
"""PINK MALL Avatar Skill v1.3 validator.

Checks the v1.1 baseline, the v1.2 hardening rules AND the v1.3 failure-learning rules.
Dependency-light: standard library only. Run from the skill directory.

    python VALIDATE_SKILL.py
"""
import json, os, re, sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS, PASSES = [], []

def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return json.load(fh)

def check(label, ok, detail=""):
    (PASSES if ok else FAILS).append(
        f"{'PASS' if ok else 'FAIL'}: {label}" + (f" ({detail})" if detail else ""))

JSON_FILES = [
    "AVATAR_LIBRARY_MANIFEST.json", "CANONICAL_PACKS.json",
    "INA_AVATAR_BIBLE.json", "SIS_AVATAR_BIBLE.json", "DUO_LIBRARY.json",
    "BRAND_DNA.json", "SISTER_STYLE_PROFILES.json", "CAMPAIGN_STYLE_PRESETS.json",
    "TEST_SCENARIOS.json", "TEST_EVALUATION_RUBRIC.json",
    "CONSENT_AND_PROVENANCE.json",
    "PIERCIINA_HERITAGE_DNA.json", "IDENTITY_COLLISION_PROTOCOL.json",
    "WARDROBE_AUTHORITY.json", "FAILURE_TAXONOMY.json",
    "CURRENT_PINK_MALL_FASHION_CONTEXT.schema.json",
]
MD_FILES = [
    "SKILL.md", "REFERENCE_SELECTION_RULES.md", "PROMPT_ASSEMBLY_RULES.md",
    "CREATIVE_GUARDRAILS.md", "WORKFLOW_5_STEP.md",
    "IMAGE_LIBRARY_INTEGRATION_POLICY.md", "README.md", "CHANGELOG.md",
]
PY_FILES = ["build_fashion_context.py"]

data = {}
for name in JSON_FILES:
    try:
        data[name] = load(name)
        check(f"JSON parses: {name}", True)
    except Exception as exc:                                   # noqa: BLE001
        check(f"JSON parses: {name}", False, str(exc))
if FAILS:
    print("\n".join(PASSES + FAILS)); sys.exit(1)

for name in MD_FILES + PY_FILES:
    check(f"present: {name}", os.path.exists(os.path.join(HERE, name)))

M   = data["AVATAR_LIBRARY_MANIFEST.json"]
CP  = data["CANONICAL_PACKS.json"]
DU  = data["DUO_LIBRARY.json"]
PR  = data["CAMPAIGN_STYLE_PRESETS.json"]
TS  = data["TEST_SCENARIOS.json"]
RB  = data["TEST_EVALUATION_RUBRIC.json"]
CO  = data["CONSENT_AND_PROVENANCE.json"]
INA = data["INA_AVATAR_BIBLE.json"]
SIS = data["SIS_AVATAR_BIBLE.json"]

# ── v1.1 structural baseline, preserved ───────────────────────────────
recs = M["records"]
check("manifest record count = 190", len(recs) == 190, len(recs))
counts = {}
for r in recs:
    counts[r["subject"]] = counts.get(r["subject"], 0) + 1
check("subject counts = 77 INA / 76 SIS / 37 DUO",
      counts == {"INA": 77, "SIS": 76, "DUO": 37}, counts)
paths = [r["relativePath"] for r in recs]
check("manifest relative paths unique", len(set(paths)) == 190)
check("manifest ids unique", len({r["id"] for r in recs}) == 190)
check("every record carries a sha256",
      all(re.fullmatch(r"[0-9a-f]{64}", r.get("sha256", "") or "") for r in recs))
check("sha256 values unique", len({r["sha256"] for r in recs}) == 190)
check("manifest subject matches folder label",
      all(r["relativePath"].split("/")[0] == r["subject"] for r in recs))

by_path = {r["relativePath"]: r for r in recs}
IMG = re.compile(r"\.(jpe?g|png|webp)$", re.I)

def tokens(obj, acc=None):
    acc = [] if acc is None else acc
    if isinstance(obj, str):
        acc.append(obj)
    elif isinstance(obj, list):
        for item in obj:
            tokens(item, acc)
    elif isinstance(obj, dict):
        for item in obj.values():
            tokens(item, acc)
    return acc

resolved, unresolved, crossed = 0, [], []
for label in ("INA", "SIS", "DUO"):
    for tok in tokens(CP[label]):
        if not IMG.search(tok):
            continue
        rec = by_path.get(tok)
        if rec is None:
            unresolved.append((label, tok)); continue
        resolved += 1
        if rec["subject"] != label:
            crossed.append((label, tok, rec["subject"]))
for comp in DU["compositions"].values():
    for tok in tokens(comp):
        if not IMG.search(tok):
            continue
        rec = by_path.get(tok)
        if rec is None:
            unresolved.append(("DUO_LIBRARY", tok)); continue
        resolved += 1
        if rec["subject"] != "DUO":
            crossed.append(("DUO_LIBRARY", tok, rec["subject"]))
check("all canonical/duo references resolve", not unresolved, unresolved[:3])
check("no INA/SIS/DUO cross-label contamination", not crossed, crossed[:3])
check("canonical/duo references resolved = 103", resolved == 103, resolved)

check("INA bible unchanged: CURATED_FOUNDATION_CANDIDATE / INA_v1.0",
      INA["status"] == "CURATED_FOUNDATION_CANDIDATE" and INA["identityVersion"] == "INA_v1.0")
check("SIS bible unchanged: CURATED_FOUNDATION_CANDIDATE / SIS_v1.0",
      SIS["status"] == "CURATED_FOUNDATION_CANDIDATE" and SIS["identityVersion"] == "SIS_v1.0")

presets = set(PR["presets"])
used = {t["preset"] for t in TS["tests"]}
check("every scenario preset exists", used <= presets, sorted(used - presets))
check("6 test scenarios", len(TS["tests"]) == 6, len(TS["tests"]))
weights = sum(Decimal(str(c["weight"])) for c in RB["criteria"])
check("evaluation weights sum to exactly 1", weights == Decimal("1"), weights)

# ── v1.2 hardening rules ──────────────────────────────────────────────
check("v1.2: metric renamed to frameLaplacianVar",
      all("frameLaplacianVar" in r for r in recs))
check("v1.2: old sharpnessLaplacianVar name is gone",
      not any("sharpnessLaplacianVar" in r for r in recs))
metrics = M.get("metrics", {}).get("frameLaplacianVar", {})
check("v1.2: metric scope documented as FULL_FRAME", metrics.get("scope") == "FULL_FRAME")
check("v1.2: metric marked not comparable across captureType",
      "captureType" in metrics.get("notComparableAcross", []))
check("v1.2: metric forbidden for ranking identity masters",
      any("rank" in u for u in metrics.get("doNotUseFor", [])))

check("v1.2: candidatePool vs runtimePack terminology defined",
      {"candidatePool", "runtimePack"} <= set(CP.get("terminology", {})))
rs = CP.get("runtimeSelection", {})
check("v1.2: single-subject cap 4-6",
      rs.get("singleSubject", {}).get("min") == 4 and rs.get("singleSubject", {}).get("max") == 6)
check("v1.2: duo cap 6-8",
      rs.get("duo", {}).get("min") == 6 and rs.get("duo", {}).get("max") == 8)
check("v1.2: selection is role-ordered", bool(rs.get("roleOrder")))

for s in ("INA", "SIS"):
    check(f"v1.2: {s} CORE_FACE preserved (5)", len(CP[s]["CORE_FACE"]["candidates"]) == 5)
    check(f"v1.2: {s} CORE_BODY preserved (6)", len(CP[s]["CORE_BODY"]["candidates"]) == 6)
    fp = CP[s]["FASHION_POSE"]
    check(f"v1.2: {s} FASHION_POSE ranked without loss",
          len(fp["preferred"]) + len(fp["secondary"]) == fp["count"],
          f"{len(fp['preferred'])}+{len(fp['secondary'])} vs {fp['count']}")
    check(f"v1.2: {s} FASHION_POSE preferred is a small set", 2 <= len(fp["preferred"]) <= 4,
          len(fp["preferred"]))
    for pool in ("EYEWEAR", "HEADWEAR"):
        check(f"v1.2: {s} {pool} marked WEAR_REFERENCE_ONLY",
              CP[s][pool].get("productAuthority") == "WEAR_REFERENCE_ONLY")

check("v1.2: SIS IDENTITY_DETAILS gap state is notCaptured",
      CP["SIS"]["IDENTITY_DETAILS"].get("state") == "notCaptured")
check("v1.2: SIS IDENTITY_DETAILS has no borrowed candidates",
      CP["SIS"]["IDENTITY_DETAILS"]["candidates"] == [])
check("v1.2: INA IDENTITY_DETAILS still present (2)",
      len(CP["INA"]["IDENTITY_DETAILS"]["candidates"]) == 2)

check("v1.2: DUO commercial default is BLAZER_EDITORIAL",
      CP["DUO"].get("commercialDefault") == "BLAZER_EDITORIAL")
check("v1.2: FOUNDATION_STORY is not a hero default",
      CP["DUO"]["FOUNDATION_STORY"].get("notForHeroDefault") is True
      and CP["DUO"]["FOUNDATION_STORY"].get("heroDefault") is False)
check("v1.2: known library limits recorded", bool(CP.get("knownLibraryLimits")))

for name in ("hero_banner", "sister_battle", "story_vertical"):
    cs = PR["presets"][name].get("compositionSafety", {})
    check(f"v1.2: {name} has measurable compositionSafety",
          bool(cs.get("aspectRatios")) and "textSafeRegion" in cs and "edgeMargin" in cs)
check("v1.2: composition safety flagged as test defaults",
      PR.get("compositionSafetyStatus") == "TEST_DEFAULTS_NOT_PERMANENT_BRAND_TRUTH")

check("v1.2: compositionUsable is a required gate",
      RB["gates"].get("compositionUsableRequired") is True)
check("v1.2: compositionUsable definition present with fail conditions",
      bool(RB.get("compositionUsable", {}).get("failIfAny")))
check("v1.2: gate rule states score cannot override compositionUsable",
      "compositionUsable" in RB["gates"].get("rule", ""))
check("v1.2: rubric review fields include compositionUsable",
      "compositionUsable" in RB.get("reviewFields", []))

check("v1.2: scenarios carry three expected confidences",
      all({"identityConfidence", "compositionConfidence", "productConfidence"}
          <= set(t.get("expectedConfidence", {})) for t in TS["tests"]))
t02 = next(t for t in TS["tests"] if t["id"] == "T02_SIS_ACCESSORY")
check("v1.2: product-led scenario separates geometry from wear reference",
      "productGeometrySource" in t02 and "productWearReference" in t02)

REQ = "OWNER_CONFIRMATION_REQUIRED"
check("v1.2: consent file status is unset", CO.get("status") == REQ)
check("v1.2: consent not invented for any subject",
      all(CO["subjects"][s]["writtenAuthorisationOnFile"] == REQ for s in ("INA", "SIS", "DUO")))
check("v1.2: consent covers ownership, expiry and revocation",
      all(k in CO["subjects"]["INA"] for k in
          ("sourceOwnership", "expiryOrReviewDate", "revocationPath")))
check("v1.2: consent records allowed-use status",
      "allowedUse" in CO["subjects"]["INA"])
check("v1.2: consent marks public repository exposure prohibited",
      CO["library"].get("publicRepositoryExposure") == "PROHIBITED")
check("v1.2: consent gate blocks commercial publication while unset",
      REQ in CO.get("gate", {}).get("rule", ""))

policy = open(os.path.join(HERE, "IMAGE_LIBRARY_INTEGRATION_POLICY.md"), encoding="utf-8").read()
check("v1.2: policy states the repository is public", "public repository" in policy.lower())
check("v1.2: policy withdraws Git LFS for the public repo",
      "lfs" in policy.lower() and "not" in policy.lower())
check("v1.2: policy offers private storage options",
      "private" in policy.lower())

skill = open(os.path.join(HERE, "SKILL.md"), encoding="utf-8").read()
for field in ("identityConfidence", "compositionConfidence", "productConfidence",
              "productGeometrySource", "productWearReference"):
    check(f"v1.2: SKILL.md documents {field}", field in skill)
check("v1.3: SKILL.md declares version 1.3", "version: 1.3" in skill)

# ── v1.3 failure-learning rules ───────────────────────────────────────
HD  = data["PIERCIINA_HERITAGE_DNA.json"]
ICP = data["IDENTITY_COLLISION_PROTOCOL.json"]
WA  = data["WARDROBE_AUTHORITY.json"]
FT  = data["FAILURE_TAXONOMY.json"]
FC  = data["CURRENT_PINK_MALL_FASHION_CONTEXT.schema.json"]
rules = open(os.path.join(HERE, "PROMPT_ASSEMBLY_RULES.md"), encoding="utf-8").read()
guard = open(os.path.join(HERE, "CREATIVE_GUARDRAILS.md"), encoding="utf-8").read()
selrules = open(os.path.join(HERE, "REFERENCE_SELECTION_RULES.md"), encoding="utf-8").read()

# A. identity collision
GROUPS = ["GROUP_INA_IDENTITY", "GROUP_SIS_IDENTITY", "GROUP_DUO_STAGING"]
check("v1.3: collision protocol defines three labelled groups",
      ICP["referenceGrouping"]["groups"] == GROUPS)
check("v1.3: DUO references barred from identity authority",
      "NEVER identity authority" in ICP["authorityRules"]["DUO"])
check("v1.3: identityCollisionDetected defined", "identityCollisionDetected" in ICP["detection"])
check("v1.3: subjectRoleSwapDetected defined", "subjectRoleSwapDetected" in ICP["detection"])
check("v1.3: escalation has LEVEL_1 and LEVEL_2",
      {"LEVEL_1", "LEVEL_2"} <= set(ICP["escalation"]))
check("v1.3: LEVEL_2 is sequential identity lock",
      "sequential identity lock" in ICP["escalation"]["LEVEL_2"]["name"])
check("v1.3: rewriting canonical refs after one collision is prohibited",
      any("Rewriting canonical" in x for x in ICP["escalation"]["prohibited"]))
for g in GROUPS:
    check(f"v1.3: {g} documented in SKILL.md and assembly rules",
          g in skill and g in rules)

# B. wardrobe authority
check("v1.3: referencePhotoWardrobe = IGNORE_FOR_STYLING",
      WA["referencePhotoWardrobe"] == "IGNORE_FOR_STYLING")
check("v1.3: identityReference vs wardrobeAuthority distinguished",
      {"identityReference", "wardrobeAuthority"} <= set(WA["coreDistinction"]))
check("v1.3: wardrobe priority is catalogue -> approved reference -> trend brief",
      [x["source"] for x in WA["wardrobeSourcePriority"]] ==
      ["CURRENT_PINK_MALL_CATALOGUE", "APPROVED_CAMPAIGN_WARDROBE_REFERENCE",
       "OWNER_APPROVED_TREND_BRIEF"])
check("v1.3: avatar clothing barred as fallback",
      "NEVER a fallback" in WA["forbiddenFallback"]["rule"])
for f in ("wardrobeSource", "wardrobeConfidence", "wardrobeLocks", "wardrobeWarnings"):
    check(f"v1.3: {f} defined and documented", f in WA["fields"] and f in skill)
check("v1.3: missing authority forces wardrobeConfidence LOW",
      "LOW" in WA["fields"]["wardrobeConfidence"]["rule"])
check("v1.3: canonical pools flagged non-authoritative for wardrobe",
      CP.get("referencePhotoWardrobe") == "IGNORE_FOR_STYLING")

# C. runtime fashion context
check("v1.3: fashion context is a schema, not frozen data",
      FC.get("doNotCommitInstances") is True and "schema" in FC["purpose"].lower())
check("v1.3: fashion context names its generator",
      FC.get("generator") == "build_fashion_context.py")
check("v1.3: fashion context has a staleness policy", bool(FC.get("staleness")))
check("v1.3: no committed fashion context instance",
      not os.path.exists(os.path.join(HERE, "CURRENT_PINK_MALL_FASHION_CONTEXT.json")))

# D. Pierciina heritage
REQUIRED_ANCHORS = ["retro/disco lineage", "deep magenta / magenta", "cream",
                    "warm gold accent", "retro display typography",
                    "marquee / signage language", "stars and sparkles",
                    "vintage boutique / editorial poster energy",
                    "playful handmade imperfection",
                    "Y2K as an evolution of Pierciina, not a replacement of it"]
check("v1.3: all ten heritage anchors present",
      HD["requiredAnchors"] == REQUIRED_ANCHORS,
      set(REQUIRED_ANCHORS) - set(HD["requiredAnchors"]))
check("v1.3: heritage derived from project source, not assumptions",
      HD["status"] == "DERIVED_FROM_PROJECT_SOURCE" and "PINKMALL.html" in HD["provenance"]["extractedFrom"])
for forbidden in ("generic futuristic pink mall", "generic luxury shopping centre",
                  "Barbie-like pink", "anonymous chrome-heavy AI-fashion aesthetic",
                  "visual language disconnected from Pierciina"):
    check(f"v1.3: heritage forbids {forbidden!r}", forbidden in HD["forbidden"])
check("v1.3: design target is 70/30",
      HD["designTarget"]["premiumEcommerceUsability"] == 0.70
      and HD["designTarget"]["strangeSisterChaosY2K"] == 0.30)
check("v1.3: heritage palette carries magenta, cream and gold",
      all(k in HD["palette"]["heritageCore"] for k in ("magenta", "cream", "gold")))

# E. assembly order
ORDER = ["identity", "current wardrobe authority", "Pierciina heritage",
         "PINK MALL campaign layer", "composition", "creative flourish"]
pos = [skill.find(step) for step in ORDER]
check("v1.3: SKILL.md states the new assembly order",
      all(p_ >= 0 for p_ in pos) and pos == sorted(pos), pos)
check("v1.3: conflict priority includes wardrobe and heritage",
      "wardrobe authority > Pierciina heritage" in skill
      and "wardrobe authority > Pierciina heritage" in rules)

# F. failure taxonomy
CODES = ["F01_IDENTITY_COLLISION", "F02_WARDROBE_LEAKAGE", "F03_BRAND_HERITAGE_DRIFT",
         "F04_PRODUCT_GEOMETRY_DRIFT", "F05_COMPOSITION_FAILURE", "F06_SUBJECT_ROLE_SWAP",
         "F07_REFERENCE_OVERFIT", "F08_GENERIC_FASHION_DRIFT"]
check("v1.3: all eight failure codes defined", list(FT["codes"]) == CODES,
      set(CODES) ^ set(FT["codes"]))
run = FT["runLog"][0]
check("v1.3: T04 run 001 recorded as FAIL", run["result"] == "FAIL")
check("v1.3: T04 run 001 records F01/F02/F03 as FAIL",
      all(run["codes"][c] == "FAIL" for c in CODES[:3]))
check("v1.3: T04 failure does not implicate identity pools",
      run["identityPoolsImplicated"] is False and run["canonicalReferencesChanged"] == "none")
check("v1.3: doctrine keeps failures off the identity system",
      "never permission to rewrite the identity system" in FT["doctrine"].lower())

# G. new hard gates
G = RB["gates"]
check("v1.3: sisterDistinctnessRequired gate", G.get("sisterDistinctnessRequired") is True)
check("v1.3: identityCollisionDetected gate must be false", G.get("identityCollisionDetected") is False)
check("v1.3: subjectRoleSwapDetected gate must be false", G.get("subjectRoleSwapDetected") is False)
check("v1.3: wardrobeSourceValid gate must be true", G.get("wardrobeSourceValid") is True)
check("v1.3: brandHeritageMatchMinimum set", isinstance(G.get("brandHeritageMatchMinimum"), int))
check("v1.3: gate rule covers collision, wardrobe and heritage",
      all(k in G["rule"] for k in ("identityCollisionDetected", "wardrobeSourceValid", "brandHeritageMatch")))
check("v1.3: brandHeritageMatch is a scored criterion",
      any(c["key"] == "brandHeritageMatch" for c in RB["criteria"]))
check("v1.3: rubric review fields carry the new signals",
      all(f in RB["reviewFields"] for f in
          ("identityCollisionDetected", "subjectRoleSwapDetected", "wardrobeSource", "failureCodes")))

# scenarios
check("v1.3: DUO scenarios require a collision check",
      all(t.get("requiresIdentityCollisionCheck") for t in TS["tests"] if t["subject"] == "DUO"))
check("v1.3: scenarios carry wardrobe authority expectations",
      all("requiresWardrobeAuthority" in t for t in TS["tests"]))
t04s = next(t for t in TS["tests"] if t["id"] == "T04_SISTER_BATTLE")
check("v1.3: T04 records its prior failed run",
      bool(t04s.get("priorRuns")) and t04s["priorRuns"][0]["result"] == "FAIL")
check("v1.3: T04 does not auto-retry", "Do not auto-retry" in t04s.get("retryPolicy", ""))

# guardrail + selection propagation
check("v1.3: guardrails carry the 7-level priority order",
      "Wardrobe authority" in guard and "Pierciina heritage" in guard)
check("v1.3: guardrails state beauty cannot rescue a failed gate",
      "beautiful image still FAILS" in guard)
check("v1.3: selection rules mandate labelled DUO groups",
      all(g in selrules for g in GROUPS))

# untouched foundations
check("v1.3: manifest still 190 records", len(recs) == 190)
check("v1.3: identity masters untouched",
      INA["status"] == "CURATED_FOUNDATION_CANDIDATE" and SIS["status"] == "CURATED_FOUNDATION_CANDIDATE")
check("v1.3: privacy policy unchanged in substance",
      "public repository" in policy.lower() and "PROHIBITED" == CO["library"]["publicRepositoryExposure"])

print("\n".join(PASSES))
if FAILS:
    print()
    print("\n".join(FAILS))
    print(f"\nVALIDATION FAIL — {len(PASSES)} passed, {len(FAILS)} failed")
    sys.exit(1)
print(f"\nVALIDATION PASS — PINK MALL Avatar Skill v1.3 ({len(PASSES)} checks)")
