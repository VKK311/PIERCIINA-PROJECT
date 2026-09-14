#!/usr/bin/env python3
"""PINK MALL Avatar Skill v1.2 validator.

Checks the v1.1 structural baseline AND the v1.2 hardening rules.
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
]
MD_FILES = [
    "SKILL.md", "REFERENCE_SELECTION_RULES.md", "PROMPT_ASSEMBLY_RULES.md",
    "CREATIVE_GUARDRAILS.md", "WORKFLOW_5_STEP.md",
    "IMAGE_LIBRARY_INTEGRATION_POLICY.md", "README.md", "CHANGELOG.md",
]

data = {}
for name in JSON_FILES:
    try:
        data[name] = load(name)
        check(f"JSON parses: {name}", True)
    except Exception as exc:                                   # noqa: BLE001
        check(f"JSON parses: {name}", False, str(exc))
if FAILS:
    print("\n".join(PASSES + FAILS)); sys.exit(1)

for name in MD_FILES:
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
check("v1.2: SKILL.md declares version 1.2", "version: 1.2" in skill)

print("\n".join(PASSES))
if FAILS:
    print()
    print("\n".join(FAILS))
    print(f"\nVALIDATION FAIL — {len(PASSES)} passed, {len(FAILS)} failed")
    sys.exit(1)
print(f"\nVALIDATION PASS — PINK MALL Avatar Skill v1.2 ({len(PASSES)} checks)")
