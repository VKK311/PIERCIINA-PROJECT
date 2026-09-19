#!/usr/bin/env python3
"""Public-safe regression validator for Contract 05 — Workstation Operating."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"docs/pink-mall/system-contracts"
CONTRACT=BASE/"05_WORKSTATION_OPERATING_CONTRACT.json"
SCHEMA=BASE/"05_WORKSTATION_OPERATING_CONTRACT.schema.json"
MD=BASE/"05_WORKSTATION_OPERATING_CONTRACT.md"
EXPECTED_ID="PINK_MALL_WORKSTATION_OPERATING_CONTRACT"
EXPECTED_NUMBER="05"
SEMVER=re.compile(r"^\d+\.\d+\.\d+$")
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def check(label, ok, detail=""):
    print(("PASS" if ok else "FAIL")+f" {label}"+(f": {detail}" if detail else ""))
    return ok
def main():
    c=load(CONTRACT); s=load(SCHEMA); md=MD.read_text(encoding="utf-8")
    checks=[]
    checks.append(check("contractId",c.get("contractId")==EXPECTED_ID,str(c.get("contractId"))))
    checks.append(check("version",bool(SEMVER.fullmatch(c.get("version",""))),c.get("version","")))
    checks.append(check("contractNumber",c.get("contractNumber")==EXPECTED_NUMBER,str(c.get("contractNumber"))))
    checks.append(check("parentContract",c.get("parentContract")=="PINK_MALL_SYSTEM_AUTHORITY_CONTRACT"))
    checks.append(check("status",c.get("status") in {"CANDIDATE","CANONICAL","SUPERSEDED"}))
    checks.append(check("scope is specification-only",c["scope"]["implementationProvidedByThisContract"] is False))
    checks.append(check("master + per-campaign stations locked",c["operatingModel"]["masterStation"]=="PINK_MALL_HQ_MASTER_STATION" and c["operatingModel"]["campaignStation"]=="ONE_SEPARATE_STATION_PER_CAMPAIGN" and c["operatingModel"]["approvedIdeaAllowsStationConstructionWithoutSecondArchitectureApproval"] is True))
    checks.append(check("checkpoint order",c["checkpointOrder"]==["CONCEPT","IMAGES","VIDEO","FINAL"]))
    checks.append(check("image exploration 2–3",c["initialImageExploration"]["normalVariantCountMin"]==2 and c["initialImageExploration"]["normalVariantCountMax"]==3 and c["initialImageExploration"]["meaningfullyDifferentRequired"] is True))
    checks.append(check("Claude selects model",c["modelSelection"]["decisionOwner"]=="CLAUDE"))
    checks.append(check("budget modes",c["budgetModes"]["modes"]==["ECONOMY","STANDARD","PREMIUM"] and not any(c["budgetModes"][k] for k in ("numericCeilingsDefined","creditsDefined","correctionSpendDefined","providerPricesDefined"))))
    checks.append(check("candidate state boundary",c["states"]["generationStartsAs"]=="GENERATED_OUTPUT" and c["states"]["generatedOutputMayAutoBecomeApproved"] is False and c["states"]["generatedOutputMayAutoBecomePublished"] is False))
    checks.append(check("QA dispositions",c["qaBoundary"]["dispositions"]==["PASS","FAIL","UNRESOLVED"] and c["qaBoundary"]["failedCandidateMayBeSilentlyPromoted"] is False))
    checks.append(check("rework preserves lineage",c["rework"]["allowed"] is True and c["rework"]["failedAttemptMustRemainTraceable"] is True))
    rb=c["runtimeBoundary"]; checks.append(check("runtime not fabricated",all(rb[k] is False for k in ("runtimeExistsClaimed","stationTemplateExistsClaimed","cyberninjasGraphExistsClaimed","automatedPaidRunnerExistsClaimed","campaignInstanceExistsClaimed"))))
    checks.append(check("no authority grants",all(v is False for v in c["authorityGrants"].values())))
    checks.append(check("deferred 06/07/08",sorted(x["contractNumber"] for x in c["deferredBoundaries"])==["06","07","08"]))
    checks.append(check("public/private boundary",c["provenance"]["privateDataInPublicRepo"] is False))
    checks.append(check("schema identity",s["properties"]["contractId"]["const"]==EXPECTED_ID and s["properties"]["contractNumber"]["const"]==EXPECTED_NUMBER))
    required_phrases=["ECONOMY","STANDARD","PREMIUM","CONCEPT","IMAGES","FINAL","Claude selects","PLANNED","Product Truth","Human Identity"]
    checks.append(check("markdown preserves locked operating decisions",all(p.lower() in md.lower() for p in required_phrases)))
    # Detect forbidden numeric budget invention in contract data.
    forbidden={"creditCeiling","budgetCeiling","spendLimit","correctionSpendAmount","numericBudgetWeight"}
    found=[k for k in forbidden if k in json.dumps(c)]
    checks.append(check("no unauthorised numeric budget fields",not found,str(found)))
    ok=all(checks)
    print(f"\nWORKSTATION OPERATING CONTRACT: {'PASS' if ok else 'FAIL'} — {sum(checks)}/{len(checks)} checks")
    return 0 if ok else 1
if __name__=="__main__": sys.exit(main())
