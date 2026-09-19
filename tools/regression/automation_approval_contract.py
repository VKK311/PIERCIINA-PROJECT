#!/usr/bin/env python3
"""Public-safe regression validator for Contract 06 — Automation & Approval."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"docs/pink-mall/system-contracts"
CONTRACT=BASE/"06_AUTOMATION_AND_APPROVAL_CONTRACT.json"
SCHEMA=BASE/"06_AUTOMATION_AND_APPROVAL_CONTRACT.schema.json"
MD=BASE/"06_AUTOMATION_AND_APPROVAL_CONTRACT.md"
SEMVER=re.compile(r"^\d+\.\d+\.\d+$")
def check(label,ok,detail=""):
    print(("PASS" if ok else "FAIL")+f" {label}"+(f": {detail}" if detail else ""))
    return ok
def main():
    c=json.loads(CONTRACT.read_text(encoding="utf-8"))
    s=json.loads(SCHEMA.read_text(encoding="utf-8"))
    md=MD.read_text(encoding="utf-8")
    checks=[
      check("identity",c["contractId"]=="PINK_MALL_AUTOMATION_AND_APPROVAL_CONTRACT" and c["contractNumber"]=="06"),
      check("version",bool(SEMVER.fullmatch(c["version"]))),
      check("candidate lifecycle",c["status"] in {"CANDIDATE","CANONICAL","SUPERSEDED"}),
      check("specification only",all(v is False for v in c["scope"].values())),
      check("locked approval model",c["lockedOperatingModel"]["ownerApprovesIdeaAndBudgetMode"] and c["lockedOperatingModel"]["approvalMayAuthorizeFirstBatchSpend"] and c["lockedOperatingModel"]["additionalCorrectionSpendAfterFailedQAFailsRequiresOwnerReview"]),
      check("human publication default",c["commercialPublication"]["humanApprovalCurrentDefault"] and not c["commercialPublication"]["autoPublishAuthorised"]),
      check("budget modes",c["budgetModes"]["modes"]==["ECONOMY","STANDARD","PREMIUM"] and all(c["budgetModes"][k] is False for k in ["creditCeilingsDefined","currencyCeilingsDefined","perBatchLimitsDefined","providerPricesDefined","correctionSpendAmountsDefined","numericAutonomyThresholdsDefined"])),
      check("approval states",c["approvalStates"]==["PENDING","APPROVED","REVOKED","EXPIRED"]),
      check("silence is not approval",c["approvalRecord"]["silenceIsApproval"] is False),
      check("first batch bounded",c["firstBatchSpend"]["approvalMayAuthorise"] and not c["firstBatchSpend"]["unbounded"] and c["firstBatchSpend"]["requiresApplicableNumericCeiling"] and not c["firstBatchSpend"]["missingCeilingMayBeInvented"]),
      check("correction review",c["correctionSpend"]["additionalPaidCorrectionSpendRequiresOwnerReview"] and not c["correctionSpend"]["failedBatchCreatesUnlimitedRetryPermission"]),
      check("capability-specific autonomy",c["autonomy"]["model"]=="CAPABILITY_SPECIFIC_AND_EARNED" and not c["autonomy"]["globalFlagAllowed"] and c["autonomy"]["defaultAuthorisedCapabilities"]==[]),
      check("approval != autonomy",c["approvalVersusAutonomy"]["distinct"] and not c["approvalVersusAutonomy"]["approvalBecomesPermanentAutonomy"] and not c["approvalVersusAutonomy"]["autonomyBecomesBlanketApproval"]),
      check("campaign registry not fabricated",c["campaignOperationalState"]["authority"]=="CAMPAIGN_REGISTRY" and not c["campaignOperationalState"]["runtimeExistsClaimed"] and not c["campaignOperationalState"]["operationalFactsMayBeFabricated"]),
      check("authority boundaries",c["authorityBoundaries"]["approvalAuthority"]=="OWNER" and c["authorityBoundaries"]["paidGenerationAuthority"]=="OWNER" and c["authorityBoundaries"]["publicationAuthority"]=="OWNER" and c["authorityBoundaries"]["autonomousAuthorityDefault"]=="NONE"),
      check("no inferred delegation",c["delegation"]["currentlyDelegated"] is False and c["delegation"]["inferredDelegationAllowed"] is False),
      check("public/private boundary",all(v is False for k,v in c["publicPrivate"].items() if k!="repositoryPublic")),
      check("open decisions preserved",len(c["openDecisions"])==9),
      check("schema identity",s["properties"]["contractId"]["const"]==c["contractId"] and s["properties"]["contractNumber"]["const"]=="06"),
      check("markdown preserves locks",all(p.lower() in md.lower() for p in ["campaign idea","budget mode","correction spend","human approval","auto-publish","capability-specific and earned","Silence is never approval"])),
    ]
    raw=json.dumps(c).lower()
    forbidden=["credit ceiling: 0","budget ceiling: 0","spend limit: 0","autonomy threshold: 0"]
    checks.append(check("no invented numeric ceiling",not any(x in raw for x in forbidden)))
    ok=all(checks)
    print(f"\nAUTOMATION & APPROVAL CONTRACT: {'PASS' if ok else 'FAIL'} — {sum(checks)}/{len(checks)} checks")
    return 0 if ok else 1
if __name__=="__main__": sys.exit(main())
