#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
C=ROOT/"docs/pink-mall/workstation/WORKSTATION_2_BUILD_PACKET.json"
S=ROOT/"docs/pink-mall/workstation/WORKSTATION_2_BUILD_PACKET.schema.json"
def main():
 c=json.loads(C.read_text(encoding="utf-8")); s=json.loads(S.read_text(encoding="utf-8"))
 checks=[
 ("identity",c["packetId"]=="PINK_MALL_WORKSTATION_2_BUILD_PACKET" and c["status"]=="PRE_BUILD_SPECIFICATION"),
 ("runtime false",c["runtimeCreated"] is False),
 ("logical flow",len(c["logicalFlow"])==9),
 ("checkpoints",c["checkpoints"]==["CONCEPT","IMAGES","VIDEO_OPTIONAL","FINAL"]),
 ("image range",c["initialImageVariants"]["min"]==2 and c["initialImageVariants"]["max"]==3),
 ("states",len(c["outputStates"])==6),
 ("qa",c["qaDispositions"]==["PASS","FAIL","UNRESOLVED"]),
 ("budget",c["budgetModes"]==["ECONOMY","STANDARD","PREMIUM"] and c["numericBudgetDefined"] is False),
 ("provenance",len(c["requiredProvenance"])==9),
 ("prebuild checks",len(c["cyberninjaPreBuildChecks"])==10),
 ("no authority",c["authorityGrants"]==[]),
 ("private data blocked",c["privateDataAllowed"] is False),
 ("runtime evidence",c["runtimeEvidenceRequired"] is True),
 ("schema",s["additionalProperties"] is False and set(s["required"])==set(c.keys())),
 ]
 bad=[n for n,ok in checks if not ok]
 if bad: raise AssertionError("; ".join(bad))
 print(f"Workstation build packet regression: {len(checks)}/{len(checks)} PASS")
if __name__=="__main__": main()
