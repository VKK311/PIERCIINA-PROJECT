#!/usr/bin/env python3
"""Complete contract gate: semantic regressions + JSON Schema + negative controls.

Install requirements-contracts.txt first. These tests are offline after dependency
installation; they do not execute a campaign, call a provider, or spend credits.
"""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

try:
    from jsonschema import Draft202012Validator
except ImportError:
    raise SystemExit("Install tools/regression/requirements-contracts.txt before running this gate.")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTRACTS = ROOT / "docs/pink-mall/system-contracts"
PACKET = ROOT / "docs/pink-mall/workstation/WORKSTATION_2_BUILD_PACKET.json"
VALIDATORS = (
    "system_authority_contract", "campaign_context_contract",
    "product_creative_contract", "character_story_contract",
    "social_intelligence_contract", "workstation_operating_contract",
    "automation_approval_contract", "super_brain_memory_contract",
    "hq_blueprint_contract", "workstation_build_packet",
)
CASES = (
    ("05", "workstation_operating_contract", ("truthBoundaries", "canonicalCommerceMediaMayBeReplacedByCampaignMedia"), True),
    ("05", "workstation_operating_contract", ("checkpoints", 0, "requiresPriorOwnerIdeaApproval"), False),
    ("06", "automation_approval_contract", ("authorityGrants", "productTruth"), True),
    ("07", "super_brain_memory_contract", ("scope", "implementationProvidedByThisContract"), True),
    ("08", "hq_blueprint_contract", ("authorityGrants",), ["COMMERCIAL_PUBLICATION"]),
    ("packet", "workstation_build_packet", ("logicalFlow", 3), "AUTO_PUBLISH"),
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    failed = 0
    for name in VALIDATORS:
        result = subprocess.run([sys.executable, str(HERE / f"{name}.py")],
                                cwd=ROOT, capture_output=True, text=True, timeout=120)
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        failed += result.returncode != 0

    schemas = sorted(CONTRACTS.glob("*.schema.json")) + [PACKET.with_suffix(".schema.json")]
    schema_count = 0
    for path in schemas:
        try:
            Draft202012Validator.check_schema(load(path))
            schema_count += 1
        except Exception as exc:
            failed += 1
            print(f"FAIL schema syntax {path.name}: {exc}")
    print(f"SCHEMA SYNTAX: {schema_count}/{len(schemas)} PASS")

    documents = sorted(CONTRACTS.glob("*_CONTRACT.json")) + [PACKET]
    document_count = 0
    for path in documents:
        errors = list(Draft202012Validator(load(path.with_suffix(".schema.json"))).iter_errors(load(path)))
        if errors:
            failed += 1
            for error in errors:
                print(f"FAIL {path.name} at {list(error.path)}: {error.message}")
        else:
            document_count += 1
    print(f"FULL SCHEMA CONFORMANCE: {document_count}/{len(documents)} PASS")

    mutation_count = 0
    for number, name, keys, value in CASES:
        path = PACKET if number == "packet" else next(CONTRACTS.glob(f"{number}_*_CONTRACT.json"))
        data = copy.deepcopy(load(path))
        target = data
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        schema_errors = list(Draft202012Validator(load(path.with_suffix(".schema.json"))).iter_errors(data))
        spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            mutated = Path(directory) / "mutated.json"
            mutated.write_text(json.dumps(data), encoding="utf-8")
            setattr(module, "CONTRACT" if hasattr(module, "CONTRACT") else "C", mutated)
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    result = module.main()
                rejected = result not in (None, 0)
            except AssertionError:
                rejected = True
            # Unexpected exceptions propagate: a crash is not a valid rejection.
        ok = rejected and bool(schema_errors)
        mutation_count += ok
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'} adversarial {number}.{'.'.join(map(str, keys))}: "
              f"targeted_rejected={rejected}, schema_rejected={bool(schema_errors)}")
    print(f"ADVERSARIAL CONTROLS: {mutation_count}/{len(CASES)} PASS")
    print(f"SYSTEM CONTRACT SUITE: {'FAIL' if failed else 'PASS'} ({failed} failed gates)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
