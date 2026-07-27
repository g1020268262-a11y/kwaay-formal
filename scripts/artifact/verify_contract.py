#!/usr/bin/env python3
"""Verify committed paper artifact inputs without running a prover."""

from __future__ import annotations

import argparse
import collections
import re
import subprocess
import sys
from pathlib import Path
from typing import Mapping, Sequence

from contract import (
    BASE_COMMIT,
    CLAIM_HEADER,
    EXPECTED_HEADER,
    FROZEN_HEADER,
    M4_BASELINE,
    PAPER_HEADER,
    ContractError,
    assert_clean_branch,
    extract_proverif_queries,
    extract_tamarin_lemma,
    formula_sha,
    git_blob,
    git_blob_oid,
    verify_git_objects_exist,
    parse_key_values,
    parse_proverif_summary,
    read_git_tsv,
    read_tsv,
    repo_root,
    require_unique,
    run_git,
    sha256,
    terminal,
    validate_json_row,
    verify_git_manifest,
)

ALLOWED_PREFIXES = (
    ".gitattributes",
    ".gitignore",
    "artifact/",
    "scripts/run-paper-artifact.sh",
    "scripts/artifact/",
)


def snapshot_changed_paths(root: Path) -> int:
    return len(str(run_git(root, "diff", "--name-only", BASE_COMMIT, "HEAD", "--")).splitlines())


def verify_paper_and_frozen(root: Path) -> tuple[list[dict[str, str]], int]:
    paper = read_tsv(root / "artifact/manifest/paper-mainline.tsv", PAPER_HEADER)
    frozen = read_tsv(root / "artifact/manifest/frozen-inputs.tsv", FROZEN_HEADER)
    require_unique(paper, ["artifact_id"], "artifact ID")
    require_unique(paper, ["path"], "paper-mainline path")
    require_unique(frozen, ["path"], "frozen path")
    if {row["path"] for row in paper} != {row["path"] for row in frozen}:
        raise ContractError("paper-mainline and frozen-input path sets differ")
    schema = root / "artifact/schema/paper-mainline.schema.json"
    for row in paper:
        validate_json_row(schema, row)
    for row in frozen:
        if row["source_commit"] != BASE_COMMIT:
            raise ContractError(f"unexpected frozen source commit: {row['path']}")
        blob = git_blob(root, row["source_commit"], row["path"])
        if git_blob_oid(root, row["source_commit"], row["path"]) != row["git_blob"]:
            raise ContractError(f"frozen Git blob mismatch: {row['path']}")
        if sha256(blob) != row["blob_sha256"]:
            raise ContractError(f"frozen SHA-256 mismatch: {row['path']}")
    return paper, len(frozen)


def verify_expected(root: Path) -> list[dict[str, str]]:
    rows = read_tsv(root / "artifact/results/expected-results.tsv", EXPECTED_HEADER)
    require_unique(rows, ["property_id"], "property ID")
    require_unique(rows, ["property_id", "formula_sha256"], "property/formula binding")
    schema = root / "artifact/schema/expected-results.schema.json"
    model_cache: dict[str, bytes] = {}
    query_cache: dict[str, list[str]] = {}
    for row in rows:
        validate_json_row(schema, row)
        source_blob = git_blob_oid(
            root, row["expectation_source_commit"], row["expectation_source_path"]
        )
        if source_blob != row["expectation_source_blob"]:
            raise ContractError(f"expectation source blob mismatch: {row['property_id']}")
        regression_blob = git_blob_oid(
            root, row["regression_matrix_commit"], row["regression_matrix_path"]
        )
        if regression_blob != row["regression_matrix_blob"]:
            raise ContractError(f"regression matrix blob mismatch: {row['property_id']}")
        model_path = row["model_path"]
        model_cache.setdefault(model_path, git_blob(root, BASE_COMMIT, model_path))
        if row["tool"] == "tamarin-prover":
            formula = extract_tamarin_lemma(model_cache[model_path], row["query_or_lemma"])
        else:
            query_cache.setdefault(model_path, extract_proverif_queries(model_cache[model_path]))
            query = row["query_or_lemma"]
            if query_cache[model_path].count(query) != 1:
                raise ContractError(
                    f"ProVerif query is not unique in exact model: {row['property_id']}"
                )
            formula = query
        if formula_sha(formula) != row["formula_sha256"]:
            raise ContractError(f"formula hash mismatch: {row['property_id']}")
    inherited_pv = [
        row for row in rows
        if row["tool"] == "proverif" and row["execution_scope"] == "inherited"
    ]
    m4_pv = [
        row for row in rows
        if row["tool"] == "proverif" and row["milestone"] == "M4"
    ]
    target_manifest = read_tsv(
        root / "artifact/manifest/proverif-targets.tsv",
        ["family", "suite", "target_id", "model_path", "query_count",
         "inherited", "m4_execution_scope"],
    )
    require_unique(target_manifest, ["suite", "target_id"], "ProVerif target manifest")
    inherited_expected = sum(
        int(row["query_count"]) for row in target_manifest if row["inherited"] == "true"
    )
    m4_expected = sum(
        int(row["query_count"]) for row in target_manifest
        if row["m4_execution_scope"] == "true"
    )
    inherited_targets = {(row["suite"], row["target_id"]) for row in inherited_pv}
    manifest_inherited_targets = {
        (row["suite"], row["target_id"]) for row in target_manifest
        if row["inherited"] == "true"
    }
    m4_targets = {(row["suite"], row["target_id"]) for row in m4_pv}
    manifest_m4_targets = {
        (row["suite"], row["target_id"]) for row in target_manifest
        if row["m4_execution_scope"] == "true"
    }
    if len(inherited_pv) != inherited_expected or inherited_targets != manifest_inherited_targets:
        raise ContractError("ProVerif inherited rows differ from explicit target manifest")
    if len(m4_pv) != m4_expected or m4_targets != manifest_m4_targets:
        raise ContractError("M4 ProVerif rows differ from explicit five-target scope manifest")
    for row in m4_pv:
        if (
            row["expected_status"] != "not_run_out_of_scope"
            or row["execution_scope"] != "tamarin-only"
            or row["expectation_source_commit"] != M4_BASELINE
            or row["property_kind"] != "scope_declaration"
        ):
            raise ContractError(f"M4 ProVerif scope violation: {row['property_id']}")
    inherited_key = {
        (row["suite"], row["target_id"], row["formula_sha256"]) for row in inherited_pv
    }
    for row in m4_pv:
        if (row["suite"], row["target_id"], row["formula_sha256"]) not in inherited_key:
            raise ContractError(f"M4 ProVerif row has no independent inherited evidence: {row['property_id']}")
    semantics = read_tsv(
        root / "artifact/manifest/property-semantics.tsv",
        ["property_id", "tool", "suite", "target_id", "query_or_lemma",
         "property_kind", "expected_status"],
    )
    if semantics != [
        {field: row[field] for field in semantics[0].keys()} for row in rows
    ]:
        raise ContractError("property-semantics.tsv is stale or differs from expected contract")
    return rows


def _index_aggregate(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    require_unique(rows, ["suite", "target"], "aggregate suite/target")
    return {(row["suite"], row["target"]): row for row in rows}


def verify_m4_composite(root: Path, expected: Sequence[Mapping[str, str]]) -> dict[str, int]:
    base = "logs/tamarin-m4-hmac-dedup"
    matrix = read_git_tsv(
        root, BASE_COMMIT, f"{base}/source-run1/canonical-target-matrix.tsv",
        ["suite", "target", "expected_status"],
    )
    run1_rows = read_git_tsv(
        root, BASE_COMMIT, f"{base}/source-run1/aggregate.tsv",
        ["suite", "target", "actual_status", "expected_status", "exit_status", "loop", "raw_output"],
    )
    run2_rows = read_git_tsv(
        root, BASE_COMMIT, f"{base}/source-run2/aggregate.tsv",
        ["suite", "target", "actual_status", "expected_status", "exit_status", "loop", "raw_output"],
    )
    selection = read_git_tsv(
        root, BASE_COMMIT, f"{base}/composite-selection.tsv",
        ["suite", "target", "expected", "run1", "run2", "selected_run", "selected_status", "reason"],
    )
    vector = read_git_tsv(
        root, BASE_COMMIT, f"{base}/composite-result-vector.tsv",
        ["suite", "target", "actual_status", "expected_status", "selected_run", "match"],
    )
    if not all(len(rows) == 296 for rows in (matrix, run1_rows, run2_rows, selection, vector)):
        raise ContractError("M4 tables are not complete 296-row invocations")
    run1, run2 = _index_aggregate(run1_rows), _index_aggregate(run2_rows)
    selections = _index_aggregate(selection)
    vectors = _index_aggregate(vector)
    expected_tamarin = {
        (row["suite"], row["target_id"]): row["expected_status"]
        for row in expected if row["tool"] == "tamarin-prover"
    }
    conflicts = unresolved = mismatches = fallback = 0
    selected_raw_paths: list[str] = []
    for item in matrix:
        key = (item["suite"], item["target"])
        if expected_tamarin.get(key) != item["expected_status"]:
            raise ContractError(f"M4 matrix/expected conflict: {key}")
        a, b, selected, result = run1[key], run2[key], selections[key], vectors[key]
        a_status, b_status, wanted = a["actual_status"], b["actual_status"], item["expected_status"]
        if terminal(a_status):
            chosen, selected_run = a_status, "run1"
            if terminal(b_status) and b_status != a_status:
                conflicts += 1
        elif terminal(b_status):
            chosen, selected_run = b_status, "run2"
            fallback += 1
        else:
            chosen, selected_run = "nonterminal", "none"
            unresolved += 1
        if chosen != wanted:
            mismatches += 1
        if (
            selected["run1"] != a_status
            or selected["run2"] != b_status
            or selected["selected_run"] != selected_run
            or selected["selected_status"] != chosen
            or result["actual_status"] != chosen
            or result["expected_status"] != wanted
            or result["selected_run"] != selected_run
            or result["match"] != ("MATCH" if chosen == wanted else "MISMATCH")
        ):
            raise ContractError(f"M4 selection/vector cannot be mechanically reconstructed: {key}")
        raw = a["raw_output"] if selected_run == "run1" else b["raw_output"]
        if selected_run != "none":
            selected_raw_paths.append(
                f"{base}/{selected_run.replace('run', 'source-run')}/{raw}"
            )
    verify_git_objects_exist(root, BASE_COMMIT, selected_raw_paths)
    if (conflicts, unresolved, mismatches, fallback) != (0, 0, 0, 2):
        raise ContractError(
            f"M4 composite counts differ: conflicts={conflicts} unresolved={unresolved} "
            f"mismatches={mismatches} fallback={fallback}"
        )
    for run_name, rows, terminal_count, event_count in (
        ("source-run1", run1_rows, 294, 2),
        ("source-run2", run2_rows, 291, 5),
    ):
        if git_blob(root, BASE_COMMIT, f"{base}/{run_name}/source-run-status.txt") != b"VALID\n":
            raise ContractError(f"{run_name} is not VALID")
        terminals = sum(terminal(row["actual_status"]) for row in rows)
        nonterminals = len(rows) - terminals
        if (terminals, nonterminals) != (terminal_count, event_count):
            raise ContractError(f"{run_name} terminal/nonterminal count mismatch")
        binding_rows = read_git_tsv(
            root, BASE_COMMIT, f"{base}/{run_name}/binding.tsv", ["key", "value"]
        )
        binding = {row["key"]: row["value"] for row in binding_rows}
        if binding.get("git_head") != M4_BASELINE:
            raise ContractError(f"{run_name} binding does not identify M4 Commit A")
    summary = parse_key_values(git_blob(root, BASE_COMMIT, f"{base}/composite-summary.txt"))
    required_summary = {
        "evidence_scope": "tamarin-only",
        "canonical_target_count": "296",
        "proverif_targets": "not_run_out_of_scope",
        "terminal_conflicts": "0",
        "unresolved": "0",
        "mismatches": "0",
    }
    if any(summary.get(key) != value for key, value in required_summary.items()):
        raise ContractError("M4 composite summary scope/count mismatch")
    source1_manifest = verify_git_manifest(
        root, BASE_COMMIT, f"{base}/source-run1", f"{base}/source-run1/SHA256SUMS.txt"
    )
    source2_manifest = verify_git_manifest(
        root, BASE_COMMIT, f"{base}/source-run2", f"{base}/source-run2/SHA256SUMS.txt"
    )
    outer_manifest = verify_git_manifest(
        root, BASE_COMMIT, base, f"{base}/SHA256SUMS.txt"
    )
    return {
        "targets": len(matrix),
        "fallback": fallback,
        "source1_manifest": source1_manifest,
        "source2_manifest": source2_manifest,
        "outer_manifest": outer_manifest,
    }


def verify_m3_composite(root: Path) -> int:
    base = "logs/tamarin-m3-closeout"
    selection = read_git_tsv(
        root, BASE_COMMIT, f"{base}/composite-selection.tsv",
        ["suite", "lemma", "expected_status", "run1_status", "run1_exit", "run1_loop",
         "run2_status", "run2_exit", "run2_loop", "selected_run",
         "selected_raw_output", "selection_reason"],
    )
    vector = read_git_tsv(
        root, BASE_COMMIT, f"{base}/composite-result-vector.tsv",
        ["suite", "lemma", "actual_status", "expected_status", "selected_run", "match", "selected_raw_output"],
    )
    if len(selection) != 196 or len(vector) != 196:
        raise ContractError("M3 composite is not 196 rows")
    vindex = {(row["suite"], row["lemma"]): row for row in vector}
    require_unique(vector, ["suite", "lemma"], "M3 vector target")
    conflicts = unresolved = mismatches = fallback = 0
    for row in selection:
        key = (row["suite"], row["lemma"])
        a, b, wanted = row["run1_status"], row["run2_status"], row["expected_status"]
        if terminal(b):
            chosen, selected = b, "run2"
            if terminal(a) and a != b:
                conflicts += 1
        elif terminal(a):
            chosen, selected = a, "run1"
            fallback += 1
        else:
            chosen, selected = "nonterminal", "none"
            unresolved += 1
        if chosen != wanted:
            mismatches += 1
        actual = vindex[key]
        if (
            row["selected_run"] != selected
            or actual["actual_status"] != chosen
            or actual["expected_status"] != wanted
            or actual["selected_run"] != selected
            or actual["match"] != ("MATCH" if chosen == wanted else "MISMATCH")
        ):
            raise ContractError(f"M3 selection/vector cannot be reconstructed: {key}")
    if (conflicts, unresolved, mismatches, fallback) != (0, 0, 0, 1):
        raise ContractError("M3 composite policy/count mismatch")
    verify_git_manifest(root, BASE_COMMIT, "", f"{base}/SHA256SUMS.txt")
    return len(selection)


def verify_proverif_evidence(root: Path, expected: Sequence[Mapping[str, str]]) -> int:
    summaries = {
        "proverif-original": parse_proverif_summary(
            git_blob(root, BASE_COMMIT, "logs/final/proverif/summary.txt")
        ),
        "proverif-hmac": parse_proverif_summary(
            git_blob(root, BASE_COMMIT, "logs/variants/hmac-confirmation/proverif/summary.txt")
        ),
    }
    groups: dict[tuple[str, str], list[Mapping[str, str]]] = collections.defaultdict(list)
    for row in expected:
        if row["tool"] == "proverif" and row["execution_scope"] == "inherited":
            groups[(row["suite"], row["target_id"])].append(row)
    count = 0
    for (suite, target), rows in groups.items():
        rows = sorted(rows, key=lambda item: item["property_id"])
        statuses = summaries[suite].get(target)
        if statuses != [row["expected_status"] for row in rows]:
            raise ContractError(f"inherited ProVerif evidence mismatch: {suite}/{target}")
        if suite == "proverif-original":
            raw = f"logs/final/proverif/out/{target}.out"
        else:
            raw = f"logs/variants/hmac-confirmation/proverif/out/{target}.out"
        git_blob(root, BASE_COMMIT, raw)
        count += len(rows)
    return count


def verify_claims(root: Path, expected: Sequence[Mapping[str, str]]) -> int:
    rows = read_tsv(root / "artifact/results/claim-evidence.tsv", CLAIM_HEADER)
    expected_by_id = {row["property_id"]: row for row in expected}
    require_unique(rows, ["claim_id", "property_id", "evidence_role"], "claim evidence row")
    allowed_refs = {
        "docs/claim-hierarchy.md",
        "docs/threat-compromise-matrix.md",
        "docs/model-mapping.md",
    }
    roles = set()
    for row in rows:
        if row["property_id"] not in expected_by_id:
            raise ContractError(f"claim index references unknown property: {row['property_id']}")
        property_row = expected_by_id[row["property_id"]]
        if row["status"] != property_row["expected_status"]:
            raise ContractError(f"claim status differs from exact expected status: {row['property_id']}")
        if row["model_path"] != property_row["model_path"]:
            raise ContractError(f"claim model differs from exact expected model: {row['property_id']}")
        if not {
            row["assumptions_ref"], row["limitations_ref"],
            row["allowed_statement_ref"], row["prohibited_statement_ref"],
        }.issubset(allowed_refs):
            raise ContractError("claim index contains a non-authoritative prose reference")
        git_blob(root, BASE_COMMIT, row["model_path"])
        evidence_path = row["evidence_path"]
        if evidence_path == "artifact/results/expected-results.tsv":
            indexed = read_tsv(root / evidence_path, EXPECTED_HEADER)
            if sum(item["property_id"] == row["property_id"] for item in indexed) != 1:
                raise ContractError(f"scope evidence does not index exact property: {row['property_id']}")
        elif "proverif/summary.txt" in evidence_path:
            summary = parse_proverif_summary(git_blob(root, BASE_COMMIT, evidence_path))
            query_number = int(row["property_id"].rsplit("-q", 1)[1])
            statuses = summary.get(property_row["target_id"], [])
            if len(statuses) < query_number or statuses[query_number - 1] != row["status"]:
                raise ContractError(f"ProVerif evidence does not contain exact query result: {row['property_id']}")
        elif evidence_path.endswith("composite-result-vector.tsv"):
            evidence = read_git_tsv(root, BASE_COMMIT, evidence_path)
            target_field = "target" if "target" in evidence[0] else "lemma"
            matches = [
                item for item in evidence
                if item["suite"] == property_row["suite"]
                and item[target_field] == property_row["target_id"]
                and item["actual_status"] == row["status"]
            ]
            if len(matches) != 1:
                raise ContractError(f"evidence vector does not index exact property: {row['property_id']}")
        else:
            raise ContractError(f"unsupported claim evidence index: {evidence_path}")
        roles.add(row["evidence_role"])
    required_roles = {
        "direct theorem", "falsified universal property", "positive attack witness",
        "structural result", "non-vacuity result", "regression",
        "transparent composite", "inherited evidence",
        "conditional C_install-v2 result", "blocked attack witness regression",
        "scope declaration",
    }
    if not required_roles.issubset(roles):
        raise ContractError(f"claim evidence roles missing: {sorted(required_roles - roles)}")
    return len(rows)


def verify_tools(root: Path) -> int:
    header = [
        "tool", "required_or_observed_version", "executable", "evidence_source",
        "platform", "version_command", "exact_or_minimum", "notes",
    ]
    rows = read_tsv(root / "artifact/manifest/tool-versions.tsv", header)
    require_unique(rows, ["tool"], "tool-version entry")
    required = {
        "Tamarin Prover", "Maude", "ProVerif", "Bash", "Git", "Python",
        "cpp", "timeout", "sha256sum", "awk/gawk", "systemd/systemd-run",
        "OS", "cgroup mechanism",
    }
    if {row["tool"] for row in rows} != required:
        raise ContractError("tool-version coverage mismatch")
    if any("untested" not in row["notes"].lower() for row in rows):
        raise ContractError("tool compatibility must be explicitly untested")
    return len(rows)


def verify_generator_fresh(root: Path) -> None:
    proc = subprocess.run(
        [sys.executable, "-B", str(root / "scripts/artifact/build_contract.py"), "--check"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if proc.returncode:
        raise ContractError(f"contract generator stale-check failed: {proc.stdout.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-dirty", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    root = repo_root()
    branch, head, tree = assert_clean_branch(root, args.allow_dirty)
    verify_generator_fresh(root)
    changed = snapshot_changed_paths(root)
    _, frozen_count = verify_paper_and_frozen(root)
    expected = verify_expected(root)
    m4 = verify_m4_composite(root, expected)
    m3_count = verify_m3_composite(root)
    pv_count = verify_proverif_evidence(root, expected)
    claim_count = verify_claims(root, expected)
    tool_count = verify_tools(root)
    print(f"branch={branch}")
    print(f"head={head}")
    print(f"tree={tree}")
    print(f"changed_paths={changed}")
    print(f"frozen_blobs={frozen_count}")
    print(f"expected_rows={len(expected)}")
    print(f"inherited_proverif_rows={pv_count}")
    print(f"claim_evidence_rows={claim_count}")
    print(f"tool_rows={tool_count}")
    print(f"m3_composite_targets={m3_count}")
    print(
        "m4_composite_targets={targets} m4_fallback={fallback} "
        "m4_source1_manifest={source1_manifest} "
        "m4_source2_manifest={source2_manifest} "
        "m4_outer_manifest={outer_manifest}".format(**m4)
    )
    print("verify_committed=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"error: {exc}")
        raise SystemExit(1)
