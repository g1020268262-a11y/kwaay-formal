#!/usr/bin/env python3
"""Generate the deterministic Commit B paper-facing TSV views."""

from __future__ import annotations

import argparse
import csv
import io
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

PAPER_PATH = ROOT / "artifact/manifest/paper-mainline.tsv"
FROZEN_PATH = ROOT / "artifact/manifest/frozen-inputs.tsv"
EXPECTED_PATH = ROOT / "artifact/results/expected-results.tsv"
CLAIMS_PATH = ROOT / "artifact/results/claim-evidence.tsv"
ACTUAL_PATH = ROOT / "artifact/results/actual-results.tsv"

INVENTORY_PATH = ROOT / "artifact/manifest/artifact-inventory.tsv"
RAW_SUMMARY_PATH = ROOT / "artifact/results/raw-to-summary.tsv"
CLAIM_MATRIX_PATH = ROOT / "artifact/results/claim-matrix.tsv"

INVENTORY_FIELDS = [
    "artifact_id",
    "path",
    "artifact_class",
    "milestone",
    "paper_role",
    "authoritative_or_generated",
    "source_commit",
    "git_blob",
    "blob_sha256",
    "evidence_path",
    "freeze_status",
    "known_limitation",
]

RAW_SUMMARY_FIELDS = [
    "property_id",
    "tool",
    "suite",
    "target_id",
    "actual_status",
    "evidence_storage",
    "source_run",
    "selected_run",
    "raw_path",
    "raw_blob",
    "raw_sha256",
    "summary_path",
    "evidence_commit",
    "evidence_manifest_sha256",
]

CLAIM_MATRIX_FIELDS = [
    "claim_id",
    "paper_class",
    "property_id",
    "tool",
    "suite",
    "target_id",
    "property_kind",
    "expected_status",
    "actual_status",
    "expected_match",
    "evidence_role",
    "model_path",
    "evidence_path",
    "assumptions_ref",
    "limitations_ref",
    "allowed_statement_ref",
    "prohibited_statement_ref",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def unique_index(
    rows: list[dict[str, str]], field: str, label: str
) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row[field]
        if not key or key in result:
            raise ValueError(f"{label} has missing or duplicate {field}: {key!r}")
        result[key] = row
    return result


def tsv_bytes(fields: list[str], rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
    writer.writerow(fields)
    for row in rows:
        if set(row) != set(fields):
            raise ValueError("generated TSV row fields differ from header")
        values = [row[field] for field in fields]
        if values[-1] == "":
            line_buffer = io.StringIO(newline="")
            csv.writer(
                line_buffer, delimiter="\t", lineterminator="\n"
            ).writerow(values[:-1])
            buffer.write(line_buffer.getvalue()[:-1] + '\t""\n')
        else:
            writer.writerow(values)
    return buffer.getvalue().encode("utf-8")


def build_views() -> dict[Path, bytes]:
    paper = read_tsv(PAPER_PATH)
    frozen = read_tsv(FROZEN_PATH)
    expected = read_tsv(EXPECTED_PATH)
    claims = read_tsv(CLAIMS_PATH)
    actual = read_tsv(ACTUAL_PATH)

    frozen_by_path = unique_index(frozen, "path", "frozen inputs")
    paper_paths = [row["path"] for row in paper]
    if len(paper_paths) != len(set(paper_paths)):
        raise ValueError("paper mainline has duplicate paths")
    if set(paper_paths) != set(frozen_by_path):
        missing = sorted(set(paper_paths) - set(frozen_by_path))
        extra = sorted(set(frozen_by_path) - set(paper_paths))
        raise ValueError(f"paper/frozen path sets differ: missing={missing} extra={extra}")

    inventory = []
    for paper_row in paper:
        frozen_row = frozen_by_path[paper_row["path"]]
        inventory.append(
            {
                "artifact_id": paper_row["artifact_id"],
                "path": paper_row["path"],
                "artifact_class": paper_row["artifact_class"],
                "milestone": paper_row["milestone"],
                "paper_role": paper_row["paper_role"],
                "authoritative_or_generated": paper_row[
                    "authoritative_or_generated"
                ],
                "source_commit": frozen_row["source_commit"],
                "git_blob": frozen_row["git_blob"],
                "blob_sha256": frozen_row["blob_sha256"],
                "evidence_path": paper_row["evidence_path"],
                "freeze_status": paper_row["freeze_status"],
                "known_limitation": paper_row["known_limitation"],
            }
        )

    raw_summary = [
        {field: row[field] for field in RAW_SUMMARY_FIELDS}
        for row in actual
    ]

    expected_by_property = unique_index(expected, "property_id", "expected results")
    actual_by_property = unique_index(actual, "property_id", "actual results")
    if set(expected_by_property) != set(actual_by_property):
        raise ValueError("expected/actual property sets differ")

    claim_matrix = []
    for claim in claims:
        property_id = claim["property_id"]
        if property_id not in expected_by_property or property_id not in actual_by_property:
            raise ValueError(f"claim property is absent: {property_id}")
        expected_row = expected_by_property[property_id]
        actual_row = actual_by_property[property_id]
        if expected_row["expected_status"] != actual_row["actual_status"]:
            raise ValueError(f"expected/actual status mismatch: {property_id}")
        if actual_row["expected_match"] != "MATCH":
            raise ValueError(f"actual result is not MATCH: {property_id}")
        if claim["status"] != expected_row["expected_status"]:
            raise ValueError(f"claim/expected status mismatch: {property_id}")
        if claim["model_path"] != expected_row["model_path"]:
            raise ValueError(f"claim/expected model mismatch: {property_id}")
        claim_matrix.append(
            {
                "claim_id": claim["claim_id"],
                "paper_class": claim["paper_class"],
                "property_id": property_id,
                "tool": expected_row["tool"],
                "suite": expected_row["suite"],
                "target_id": expected_row["target_id"],
                "property_kind": expected_row["property_kind"],
                "expected_status": expected_row["expected_status"],
                "actual_status": actual_row["actual_status"],
                "expected_match": actual_row["expected_match"],
                "evidence_role": claim["evidence_role"],
                "model_path": claim["model_path"],
                "evidence_path": claim["evidence_path"],
                "assumptions_ref": claim["assumptions_ref"],
                "limitations_ref": claim["limitations_ref"],
                "allowed_statement_ref": claim["allowed_statement_ref"],
                "prohibited_statement_ref": claim["prohibited_statement_ref"],
            }
        )

    if len(inventory) != 66:
        raise ValueError(f"inventory row count differs from contract: {len(inventory)}")
    if len(raw_summary) != 405:
        raise ValueError(f"raw-to-summary row count differs from contract: {len(raw_summary)}")
    if len(claim_matrix) != 18:
        raise ValueError(f"claim matrix row count differs from contract: {len(claim_matrix)}")

    return {
        INVENTORY_PATH: tsv_bytes(INVENTORY_FIELDS, inventory),
        RAW_SUMMARY_PATH: tsv_bytes(RAW_SUMMARY_FIELDS, raw_summary),
        CLAIM_MATRIX_PATH: tsv_bytes(CLAIM_MATRIX_FIELDS, claim_matrix),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="regenerate in a temporary directory and compare exact bytes",
    )
    args = parser.parse_args()
    views = build_views()
    if args.check:
        with tempfile.TemporaryDirectory(prefix="kwaay-m5-commit-b-views-") as tmp:
            temporary = Path(tmp)
            for target, content in views.items():
                candidate = temporary / target.name
                candidate.write_bytes(content)
                if not target.exists() or target.read_bytes() != candidate.read_bytes():
                    raise ValueError(f"derived view is stale: {target.relative_to(ROOT)}")
    else:
        for target, content in views.items():
            target.write_bytes(content)
    print("artifact_inventory_rows=66 exact_join=PASS")
    print("raw_to_summary_rows=405 exact_derivation=PASS")
    print("claim_matrix_rows=18 exact_join=PASS")
    print(f"derived_view_stale_check={'PASS' if args.check else 'NOT_RUN'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
