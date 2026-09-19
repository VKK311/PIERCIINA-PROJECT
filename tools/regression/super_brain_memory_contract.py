#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
CONTRACT=ROOT/"docs/pink-mall/system-contracts/07_SUPER_BRAIN_MEMORY_CONTRACT.json"
SCHEMA=ROOT/"docs/pink-mall/system-contracts/07_SUPER_BRAIN_MEMORY_CONTRACT.schema.json"
def main():
    c=json.loads(CONTRACT.read_text(encoding="utf-8")); s=json.loads(SCHEMA.read_text(encoding="utf-8"))
    checks=[
      ("contract id",c["contractId"]=="PINK_MALL_SUPER_BRAIN_MEMORY_CONTRACT"),
      ("version",c["version"]=="1.0.0"),("status",c["status"]=="CANDIDATE"),("number",c["contractNumber"]=="07"),
      ("parent",c["parentContract"]=="PINK_MALL_SYSTEM_AUTHORITY_CONTRACT"),
      ("structured clusters",c["architecture"]["structuredClusters"] is True),
      ("free graph",c["architecture"]["freeGraphRelationships"] is True),
      ("campaign memory after campaigns",c["campaignMemory"]["writtenAfterCampaigns"] is True),
      ("durability bases",set(c["durableLearning"]["bases"])=={"REPEATED_EVIDENCE","SUFFICIENT_SIGNAL","OWNER_CONFIRMATION"}),
      ("viral result not automatic",c["durableLearning"]["oneViralResultAutomaticallyDurable"] is False),
      ("drift states",c["preferenceDrift"]["states"]==["STABLE","EMERGING","DECLINING","RETIRED"]),
      ("maintenance required",c["maintenance"]["required"] is True and c["maintenance"]["periodic"] is True),
      ("factual authority",c["authorityBoundaries"]["factualAuthority"]=="CANONICAL_REPOSITORY"),
      ("non-authority set",set(c["authorityBoundaries"]["nonAuthoritativeFor"])=={"PM_IDS","PRICES","SIZES","AVAILABILITY","CANONICAL_PRODUCT_IDENTITY","APPROVAL_STATE","BRANCH_OR_COMMIT_HASH","CAMPAIGN_SPEND","PUBLICATION_STATE"}),
      ("no raw metric authority",c["socialBoundary"]["superBrainRawMetricAuthority"] is False),
      ("no story mutation",c["storyBoundary"]["memoryMayMutateStoryState"] is False),
      ("real-time target only",c["realTimeKnowledge"]["target"] is True and c["realTimeKnowledge"]["currentCapability"] is False),
      ("private memory not public",c["publicPrivate"]["privateMemoryContentPublic"] is False),
      ("runtime not created",all(v is False for k,v in c["scope"].items() if k.startswith("creates"))),
      ("hard failures",len(c["hardFailures"])==15),
      ("schema required keys",set(s["required"])==set(c.keys())),
      ("schema additionalProperties false",s["additionalProperties"] is False),
    ]
    bad=[name for name,ok in checks if not ok]
    if bad: raise AssertionError("; ".join(bad))
    print(f"Contract 07 regression: {len(checks)}/{len(checks)} PASS")
if __name__=="__main__":
    try: main()
    except Exception as e:
        print(f"Contract 07 regression: FAIL — {e}",file=sys.stderr); raise
