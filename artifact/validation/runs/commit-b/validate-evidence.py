#!/usr/bin/env python3
"""Mechanically validate the generated M5 Commit B evidence bundle."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
COMMIT_A = "776f757e05fd2c5e1b3d3f50ba1cef880fe21804"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_blob(reference: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "blob", reference],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(
            f"git cat-file failed for {reference}: "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    return proc.stdout


def validate_schema(rows: list[dict[str, str]]) -> None:
    schema = json.loads(
        (ROOT / "artifact/schema/actual-results.schema.json").read_text(
            encoding="utf-8"
        )
    )
    required = schema["required"]
    properties = schema["properties"]
    for index, row in enumerate(rows, start=1):
        if set(row) != set(required) or set(row) != set(properties):
            raise ValueError(f"actual schema fields differ at row {index}")
        for field, rules in properties.items():
            value = row[field]
            if rules.get("type") == "string" and not isinstance(value, str):
                raise ValueError(f"actual schema type failure: row={index} field={field}")
            if "const" in rules and value != rules["const"]:
                raise ValueError(f"actual schema const failure: row={index} field={field}")
            if "enum" in rules and value not in rules["enum"]:
                raise ValueError(f"actual schema enum failure: row={index} field={field}")
            if len(value) < rules.get("minLength", 0):
                raise ValueError(
                    f"actual schema minLength failure: row={index} field={field}"
                )


def validate_checksums() -> tuple[int, int]:
    path = ROOT / "artifact/manifest/git-blob-SHA256SUMS.txt"
    lines = path.read_text(encoding="utf-8").splitlines()
    references = []
    frozen = 0
    infrastructure = 0
    for line in lines:
        digest, separator, reference = line.partition("  ")
        if not separator or len(digest) != 64:
            raise ValueError(f"malformed checksum line: {line!r}")
        if hashlib.sha256(git_blob(reference)).hexdigest() != digest:
            raise ValueError(f"Git-blob checksum mismatch: {reference}")
        references.append(reference)
        if reference.startswith(f"{COMMIT_A}:"):
            infrastructure += 1
        else:
            frozen += 1
    if references != sorted(references):
        raise ValueError("checksum references are not sorted")
    if len(references) != len(set(references)):
        raise ValueError("checksum references are duplicated")
    if any(reference.endswith(":artifact/manifest/git-blob-SHA256SUMS.txt") for reference in references):
        raise ValueError("checksum manifest includes itself")
    return frozen, infrastructure


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--actual-run-1", required=True, type=Path)
    parser.add_argument("--actual-run-2", required=True, type=Path)
    args = parser.parse_args()

    run1 = args.actual_run_1.read_bytes()
    run2 = args.actual_run_2.read_bytes()
    committed = (ROOT / "artifact/results/actual-results.tsv").read_bytes()
    if run1 != run2 or run1 != committed:
        raise ValueError("actual generation bytes differ")
    actual_sha256 = hashlib.sha256(committed).hexdigest()

    actual = read_tsv(ROOT / "artifact/results/actual-results.tsv")
    expected = read_tsv(ROOT / "artifact/results/expected-results.tsv")
    claims = read_tsv(ROOT / "artifact/results/claim-evidence.tsv")
    inventory = read_tsv(ROOT / "artifact/manifest/artifact-inventory.tsv")
    raw_summary = read_tsv(ROOT / "artifact/results/raw-to-summary.tsv")
    claim_matrix = read_tsv(ROOT / "artifact/results/claim-matrix.tsv")
    validate_schema(actual)

    tamarin = [row for row in actual if row["tool"] == "tamarin-prover"]
    inherited = [
        row for row in actual
        if row["tool"] == "proverif" and row["direct_or_inherited"] == "inherited"
    ]
    scope = [row for row in actual if row["execution_scope"] == "tamarin-only"]
    mismatches = [row for row in actual if row["expected_match"] != "MATCH"]
    conflicts = [row for row in actual if row["terminal_conflict"] != "false"]
    invalid = [row for row in actual if row["provenance_valid"] != "true"]
    unresolved = [row for row in tamarin if row["terminal"] != "true"]
    fallback = [row for row in tamarin if row["selected_run"] == "run2"]

    if (len(expected), len(actual), len(tamarin), len(inherited), len(scope)) != (
        405,
        405,
        296,
        89,
        20,
    ):
        raise ValueError("result classification counts differ from contract")
    if mismatches or conflicts or invalid or unresolved or len(fallback) != 2:
        raise ValueError("actual result validity counts differ from contract")
    if any(
        row["actual_status"] != "not_run_out_of_scope"
        or row["terminal"] != "false"
        or row["evidence_storage"] != "scope-declaration"
        for row in scope
    ):
        raise ValueError("M4 ProVerif scope declaration differs from contract")
    if any(
        row["evidence_commit"] != "740666a3abd6937b52818d0f4acaf8ea0d023c58"
        or row["evidence_storage"] != "committed-git"
        or len(row["evidence_manifest_sha256"]) != 64
        for row in tamarin
    ):
        raise ValueError("Tamarin committed provenance differs from contract")

    original = [row for row in inherited if row["suite"] == "proverif-original"]
    hmac = [row for row in inherited if row["suite"] == "proverif-hmac"]
    if any(
        row["model_commit"] != "ff93107cd7911fbd22b66c45391eff2aecf51b9f"
        or row["evidence_commit"] != "ff93107cd7911fbd22b66c45391eff2aecf51b9f"
        or row["evidence_storage"] != "committed-git"
        for row in original
    ):
        raise ValueError("original ProVerif provenance differs from contract")
    if any(
        row["model_commit"] != "9c18a64aa304639cea2ee7239ce1d3692ae2bd19"
        or row["evidence_commit"] != "9c18a64aa304639cea2ee7239ce1d3692ae2bd19"
        or row["evidence_storage"] != "committed-git"
        for row in hmac
    ):
        raise ValueError("HMAC ProVerif provenance differs from contract")

    if (len(inventory), len(raw_summary), len(claim_matrix), len(claims)) != (
        66,
        405,
        18,
        18,
    ):
        raise ValueError("derived view row counts differ from contract")
    if any(
        row["expected_status"] != row["actual_status"]
        or row["expected_match"] != "MATCH"
        for row in claim_matrix
    ):
        raise ValueError("claim matrix status join differs from contract")

    required_claims = {
        "tam-original-replay-one_send_two_accepts_exists": "verified",
        "tam-original-replay-same_message_accepted_at_most_once": "falsified",
        "tam-original-impact-one_send_two_accepts_two_installs_exists": "verified",
        "tam-original-impact-unique_install_within_completed_consumer": "falsified",
        "tam-fixed-replay-one_send_two_accepts_exists": "falsified",
        "m4-pv-original-baseline-q02": "not_run_out_of_scope",
    }
    matrix_by_property = {row["property_id"]: row for row in claim_matrix}
    for property_id, status in required_claims.items():
        if matrix_by_property[property_id]["actual_status"] != status:
            raise ValueError(f"required claim result differs: {property_id}")

    frozen_checksums, infrastructure_checksums = validate_checksums()
    if (frozen_checksums, infrastructure_checksums) != (66, 26):
        raise ValueError("checksum group counts differ from contract")

    print(f"actual_sha256={actual_sha256}")
    print("actual_generation_reproducibility=MATCH")
    print("actual_schema=PASS")
    print(
        "expected_rows=405 actual_rows=405 tamarin_rows=296 "
        "inherited_proverif_rows=89 m4_scope_rows=20"
    )
    print(
        "m4_fallback=2 terminal_conflicts=0 unresolved=0 "
        "mismatches=0 provenance_invalid=0"
    )
    print("artifact_inventory_rows=66 raw_to_summary_rows=405 claim_matrix_rows=18")
    print("claim_status_join=PASS model_path_join=PASS required_claims=PASS")
    print(
        "frozen_checksum_entries=66 failures=0 "
        "commit_a_infrastructure_checksum_entries=26 failures=0"
    )
    print("evidence_validation=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
