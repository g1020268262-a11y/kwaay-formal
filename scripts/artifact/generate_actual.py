#!/usr/bin/env python3
"""Generate actual-results.tsv only from revalidated raw evidence."""

from __future__ import annotations

import argparse
import re
import sys
from functools import lru_cache
from pathlib import Path

from contract import (
    ACTUAL_HEADER,
    BASE_COMMIT,
    ContractError,
    ensure_new_output,
    git_blob,
    git_blob_metadata,
    parse_key_values,
    parse_manifest,
    parse_proverif_summary,
    read_git_tsv,
    read_tsv,
    repo_root,
    run_git,
    sha256,
    terminal,
    validate_json_row,
    write_tsv,
)
from source_runs import (
    TARGET_HEADER,
    model_commit_for_expected,
    rederive_aggregate,
    validate_source_run,
)
from verify_contract import verify_expected, verify_m4_composite, verify_proverif_evidence

M1_EVIDENCE = "aeb66939af5e4b229f14f1444e19b559a4f98181"
M2_MODEL = "841feabd908a01bdc68669ad99253a6755820389"
M2_EVIDENCE = "e216a86e1ac7113013e58b17cb0217374ea95ca2"
M3_MODEL = "282532fd922f3a7f7928f3772b3325fe06785730"
M3_EVIDENCE = "b0ff0b23977614deea8375cb95c0909be71e5c71"
M4_MODEL = "96010c72e71defc775c7c2ee99c937ff700a3227"
M4_EVIDENCE = "740666a3abd6937b52818d0f4acaf8ea0d023c58"
PV_ORIGINAL = "ff93107cd7911fbd22b66c45391eff2aecf51b9f"
PV_HMAC = "9c18a64aa304639cea2ee7239ce1d3692ae2bd19"


@lru_cache(maxsize=16)
def tree(root: Path, commit: str) -> str:
    return str(run_git(root, "rev-parse", f"{commit}^{{tree}}"))


def model_commit(row: dict[str, str]) -> str:
    return model_commit_for_expected(row)


def blank_row() -> dict[str, str]:
    return {field: "" for field in ACTUAL_HEADER}


def validate_actual_provenance(row: dict[str, str]) -> None:
    storage = row["evidence_storage"]
    if storage == "external-manifest":
        if row["evidence_commit"] or row["evidence_tree"]:
            raise ContractError("external evidence must not claim a Git commit/tree")
        if not re.fullmatch(r"[0-9a-f]{64}", row["evidence_manifest_sha256"]):
            raise ContractError("external evidence manifest SHA-256 is missing")
    elif storage == "committed-git":
        if not re.fullmatch(r"[0-9a-f]{40}", row["evidence_commit"]):
            raise ContractError("committed evidence commit is invalid")
        if not re.fullmatch(r"[0-9a-f]{40}", row["evidence_tree"]):
            raise ContractError("committed evidence tree is invalid")
        manifest = row["evidence_manifest_sha256"]
        if manifest and not re.fullmatch(r"[0-9a-f]{64}", manifest):
            raise ContractError("committed evidence manifest SHA-256 is invalid")
    elif storage != "scope-declaration":
        raise ContractError(f"unknown evidence storage: {storage}")


def committed_rows(root: Path) -> list[dict[str, str]]:
    expected = verify_expected(root)
    verify_m4_composite(root, expected)
    verify_proverif_evidence(root, expected)
    m4_manifest_sha = sha256(
        git_blob(root, M4_EVIDENCE, "logs/tamarin-m4-hmac-dedup/SHA256SUMS.txt")
    )
    selection_rows = read_git_tsv(
        root, BASE_COMMIT, "logs/tamarin-m4-hmac-dedup/composite-selection.tsv",
        ["suite", "target", "expected", "run1", "run2", "selected_run",
         "selected_status", "reason"],
    )
    selection = {(row["suite"], row["target"]): row for row in selection_rows}
    source = {}
    for run in ("run1", "run2"):
        rows = read_git_tsv(
            root, BASE_COMMIT,
            f"logs/tamarin-m4-hmac-dedup/source-{run}/aggregate.tsv",
            ["suite", "target", "actual_status", "expected_status", "exit_status",
             "loop", "raw_output"],
        )
        source[run] = {(row["suite"], row["target"]): row for row in rows}
    summaries = {
        "proverif-original": parse_proverif_summary(
            git_blob(root, BASE_COMMIT, "logs/final/proverif/summary.txt")
        ),
        "proverif-hmac": parse_proverif_summary(
            git_blob(root, BASE_COMMIT, "logs/variants/hmac-confirmation/proverif/summary.txt")
        ),
    }
    pv_index: dict[tuple[str, str], int] = {}
    raw_paths = []
    for row in expected:
        if row["tool"] == "tamarin-prover":
            selected = selection[(row["suite"], row["target_id"])]["selected_run"]
            raw = source[selected][(row["suite"], row["target_id"])]["raw_output"]
            raw_paths.append(f"logs/tamarin-m4-hmac-dedup/source-{selected}/{raw}")
        elif row["execution_scope"] == "inherited":
            prefix = (
                "logs/final/proverif/out"
                if row["suite"] == "proverif-original"
                else "logs/variants/hmac-confirmation/proverif/out"
            )
            raw_paths.append(f"{prefix}/{row['target_id']}.out")
    unique_raw = list(dict.fromkeys(raw_paths))
    metadata = git_blob_metadata(root, BASE_COMMIT, unique_raw)
    source_manifests = {}
    for run in ("run1", "run2"):
        source_manifests[run] = {
            relative: digest
            for digest, relative in parse_manifest(
                git_blob(
                    root, BASE_COMMIT,
                    f"logs/tamarin-m4-hmac-dedup/source-{run}/SHA256SUMS.txt",
                )
            )
        }
    digests = []
    for path in unique_raw:
        match = re.match(
            r"logs/tamarin-m4-hmac-dedup/source-(run[12])/(.+)", path
        )
        if match:
            run, relative = match.groups()
            try:
                digests.append(source_manifests[run][relative])
            except KeyError as exc:
                raise ContractError(
                    f"selected raw output absent from committed source manifest: {path}"
                ) from exc
        else:
            digests.append(sha256(git_blob(root, BASE_COMMIT, path)))
    raw_info = {
        path: (oid, digest)
        for path, (oid, _), digest in zip(unique_raw, metadata, digests, strict=True)
    }
    result = []
    for expected_row in expected:
        row = blank_row()
        model = model_commit(expected_row)
        row.update({
            "schema_version": "1", "run_id": "committed-paper-artifact",
            "property_id": expected_row["property_id"],
            "tool": expected_row["tool"], "suite": expected_row["suite"],
            "target_id": expected_row["target_id"],
            "evidence_class": expected_row["expected_evidence_class"],
            "execution_scope": expected_row["execution_scope"],
            "model_commit": model, "model_tree": tree(root, model),
            "provenance_valid": "true", "terminal_conflict": "false",
        })
        if expected_row["tool"] == "tamarin-prover":
            evidence = M4_EVIDENCE
            choice = selection[(expected_row["suite"], expected_row["target_id"])]
            selected = choice["selected_run"]
            aggregate = source[selected][(expected_row["suite"], expected_row["target_id"])]
            raw_path = (
                f"logs/tamarin-m4-hmac-dedup/source-{selected}/"
                f"{aggregate['raw_output']}"
            )
            oid, digest = raw_info[raw_path]
            row.update({
                "actual_status": choice["selected_status"], "terminal": "true",
                "expected_match": (
                    "MATCH" if choice["selected_status"] == expected_row["expected_status"]
                    else "MISMATCH"
                ),
                "direct_or_inherited": "direct",
                "source_commit": evidence, "source_tree": tree(root, evidence),
                "evidence_commit": evidence, "evidence_tree": tree(root, evidence),
                "evidence_storage": "committed-git",
                "evidence_manifest_sha256": m4_manifest_sha,
                "source_run": selected, "selected_run": selected,
                "selection_reason": choice["reason"],
                "exit_status": aggregate["exit_status"], "resource_event": "none",
                "raw_path": raw_path, "raw_blob": oid, "raw_sha256": digest,
                "summary_path": "logs/tamarin-m4-hmac-dedup/composite-summary.txt",
            })
        elif expected_row["execution_scope"] == "inherited":
            evidence = PV_ORIGINAL if expected_row["suite"] == "proverif-original" else PV_HMAC
            key = (expected_row["suite"], expected_row["target_id"])
            index = pv_index.get(key, 0)
            pv_index[key] = index + 1
            actual = summaries[expected_row["suite"]][expected_row["target_id"]][index]
            prefix = (
                "logs/final/proverif/out"
                if expected_row["suite"] == "proverif-original"
                else "logs/variants/hmac-confirmation/proverif/out"
            )
            raw_path = f"{prefix}/{expected_row['target_id']}.out"
            oid, digest = raw_info[raw_path]
            row.update({
                "actual_status": actual, "terminal": "true",
                "expected_match": "MATCH" if actual == expected_row["expected_status"] else "MISMATCH",
                "direct_or_inherited": "inherited",
                "source_commit": evidence, "source_tree": tree(root, evidence),
                "evidence_commit": evidence, "evidence_tree": tree(root, evidence),
                "evidence_storage": "committed-git",
                "evidence_manifest_sha256": "",
                "source_run": "prior-committed-proverif", "selected_run": "inherited",
                "selection_reason": "M4 did not rerun ProVerif",
                "exit_status": "0", "resource_event": "none",
                "raw_path": raw_path, "raw_blob": oid, "raw_sha256": digest,
                "summary_path": (
                    "logs/final/proverif/summary.txt"
                    if expected_row["suite"] == "proverif-original"
                    else "logs/variants/hmac-confirmation/proverif/summary.txt"
                ),
            })
        else:
            evidence = M4_EVIDENCE
            row.update({
                "actual_status": "not_run_out_of_scope", "terminal": "false",
                "expected_match": "MATCH", "direct_or_inherited": "direct",
                "source_commit": evidence, "source_tree": tree(root, evidence),
                "evidence_commit": evidence, "evidence_tree": tree(root, evidence),
                "evidence_storage": "scope-declaration",
                "evidence_manifest_sha256": "",
                "source_run": "not_run_out_of_scope", "selected_run": "none",
                "selection_reason": "M4 five-target ProVerif scope declared Tamarin-only",
                "exit_status": "not_run", "resource_event": "none",
                "summary_path": "logs/tamarin-m4-hmac-dedup/composite-summary.txt",
            })
        result.append(row)
    if any(row["expected_match"] == "MISMATCH" for row in result):
        raise ContractError("committed actual table contains an expected mismatch")
    for row in result:
        validate_actual_provenance(row)
    return result


def new_source_rows(root: Path, source: Path, mode: str) -> list[dict[str, str]]:
    aggregate = validate_source_run(root, source, mode)
    derived = rederive_aggregate(source, aggregate)
    provenance = parse_key_values((source / "provenance.txt").read_bytes())
    matrix = {
        row["property_id"]: row
        for row in read_tsv(source / "target-matrix.tsv", TARGET_HEADER)
    }
    manifest_sha = sha256((source / "SHA256SUMS.txt").read_bytes())
    result = []
    for item in derived:
        raw_path = source / item["raw_output"]
        actual = item["actual_status"]
        row = blank_row()
        row.update({
            "schema_version": "1", "run_id": provenance["run_id"],
            "property_id": item["property_id"], "tool": item["tool"],
            "suite": item["suite"], "target_id": item["target_id"],
            "actual_status": actual, "terminal": "true" if terminal(actual) else "false",
            "expected_match": "MATCH" if actual == item["expected_status"] else "MISMATCH",
            "evidence_class": "new-reproduction", "execution_scope": mode,
            "direct_or_inherited": "direct",
            "source_commit": provenance["source_head"],
            "source_tree": provenance["source_tree"],
            "model_commit": matrix[item["property_id"]]["model_commit"],
            "model_tree": matrix[item["property_id"]]["model_tree"],
            "evidence_commit": "",
            "evidence_tree": "",
            "evidence_storage": "external-manifest",
            "evidence_manifest_sha256": manifest_sha,
            "source_run": str(source), "selected_run": "single",
            "selection_reason": "single raw-revalidated source invocation",
            "exit_status": item["exit_status"], "resource_event": item["resource_event"],
            "raw_path": item["raw_output"], "raw_sha256": sha256(raw_path.read_bytes()),
            "summary_path": str(source / "run-status.txt"),
            "provenance_valid": "true", "terminal_conflict": "false",
        })
        validate_actual_provenance(row)
        result.append(row)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--committed-m4", action="store_true")
    group.add_argument("--source-run", type=Path)
    parser.add_argument("--mode", choices=["smoke", "paper-core", "m4-tamarin", "full"])
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = repo_root()
    output = ensure_new_output(root, args.output)
    if args.committed_m4:
        rows = committed_rows(root)
    else:
        if not args.mode:
            raise ContractError("--mode is required with --source-run")
        rows = new_source_rows(root, args.source_run.resolve(), args.mode)
    schema = root / "artifact/schema/actual-results.schema.json"
    for row in rows:
        validate_json_row(schema, row)
    write_tsv(output / "actual-results.tsv", ACTUAL_HEADER, rows)
    print(f"actual_rows={len(rows)} output={output / 'actual-results.tsv'}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
