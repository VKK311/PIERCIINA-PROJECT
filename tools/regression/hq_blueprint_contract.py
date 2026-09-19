#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
C=ROOT/"docs/pink-mall/system-contracts/08_HQ_BLUEPRINT_CONTRACT.json"
S=ROOT/"docs/pink-mall/system-contracts/08_HQ_BLUEPRINT_CONTRACT.schema.json"
def main():
 c=json.loads(C.read_text(encoding="utf-8")); s=json.loads(S.read_text(encoding="utf-8"))
 checks=[
 ("identity",c["contractId"]=="PINK_MALL_HQ_BLUEPRINT_CONTRACT" and c["contractNumber"]=="08" and c["status"]=="CANDIDATE"),
 ("locked surface",len(c["lockedSurface"])==11),
 ("role",c["role"]=="READ_COORDINATE_VISIBILITY"),
 ("runtime false",c["runtimeExists"] is False),
 ("no independent authority",len(c["noIndependentAuthority"])==9),
 ("authority map",len(c["authorityMap"])==10),
 ("hybrid surface",c["hybridSurface"]["simpleCreativeOverview"] and c["hybridSurface"]["expandableTechnicalAuditDetail"]),
 ("workstation checkpoints",c["workstationRelationship"]["checkpoints"]==["CONCEPT","IMAGES","VIDEO_IF_APPLICABLE","FINAL"]),
 ("private data blocked",c["publicPrivate"]["privateOperationalDataPublic"] is False and c["publicPrivate"]["realSpendPublic"] is False),
 ("open decisions",len(c["openImplementationDecisions"])==15),
 ("hard failures",len(c["hardFailures"])==18),
 ("scope no runtime",all(v is False for k,v in c["scope"].items() if k.startswith("creates"))),
 ("schema keys",set(s["required"])==set(c.keys())),
 ("schema closed",s["additionalProperties"] is False),
 ]
 bad=[n for n,ok in checks if not ok]
 if bad: raise AssertionError("; ".join(bad))
 print(f"Contract 08 regression: {len(checks)}/{len(checks)} PASS")
if __name__=="__main__":
 try: main()
 except Exception as e:
  print(f"Contract 08 regression: FAIL — {e}",file=sys.stderr); raise
