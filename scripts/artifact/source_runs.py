#!/usr/bin/env python3
"""Manifest-bound source-run creation, validation, and composition."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path
from typing import Mapping, Sequence

from contract import (
    BASE_COMMIT,
    M2_BASELINE,
    M3_BASELINE,
    M4_BASELINE,
    ContractError,
    classify_tamarin,
    extract_proverif_queries,
    extract_tamarin_lemma,
    formula_sha,
    git_blob,
    git_blob_oid,
    parse_key_values,
    parse_proverif_output,
    read_tsv,
    repo_root,
    require_unique,
    run_git,
    sha256,
    terminal,
    validate_json_row,
    write_tsv,
)

TARGET_HEADER = [
    "property_id", "tool", "suite", "target_id", "model_path",
    "model_commit", "model_tree", "model_blob", "model_sha256",
    "query_index", "query_or_lemma", "formula_sha256", "expected_status",
]
AGGREGATE_HEADER = [
    "property_id", "tool", "suite", "target_id", "query_index",
    "actual_status", "expected_status", "exit_status", "resource_event",
    "raw_output",
]
SELECTION_HEADER = [
    "property_id", "tool", "suite", "target_id", "expected_status",
    "run1_status", "run2_status", "selected_run", "selected_status",
    "selection_reason",
]
VECTOR_HEADER = [
    "property_id", "tool", "suite", "target_id", "actual_status",
    "expected_status", "selected_run", "match",
]
REQUIRED_SOURCE_FILES = {
    "provenance.txt", "versions.tsv", "target-matrix.tsv", "aggregate.tsv",
    "commands.tsv", "run-status.txt",
}
M1_MODEL = "aeb66939af5e4b229f14f1444e19b559a4f98181"
PV_ORIGINAL_MODEL = "ff93107cd7911fbd22b66c45391eff2aecf51b9f"
PV_HMAC_MODEL = "9c18a64aa304639cea2ee7239ce1d3692ae2bd19"


def expected_rows(root: Path) -> list[dict[str, str]]:
    return read_tsv(root / "artifact/results/expected-results.tsv")


def mode_rows(rows: Sequence[dict[str, str]], mode: str) -> list[dict[str, str]]:
    inherited = [
        row for row in rows
        if row["execution_scope"] != "tamarin-only"
    ]
    tamarin = [row for row in rows if row["tool"] == "tamarin-prover"]
    if mode == "smoke":
        wanted = {
            "tam-combined-replay-normal_confirmed_single_accept",
            "pv-original-component-q01",
        }
        selected = [row for row in inherited if row["property_id"] in wanted]
    elif mode == "paper-core":
        selected = [
            row for row in inherited
            if row["suite"] in {"combined-replay", "combined-impact"}
            or row["tool"] == "proverif"
        ]
    elif mode == "m4-tamarin":
        selected = tamarin
    elif mode == "full":
        selected = inherited
    else:
        raise ContractError(f"unsupported source-run mode: {mode}")
    if not selected:
        raise ContractError(f"mode has no declared properties: {mode}")
    require_unique(selected, ["property_id"], f"{mode} property")
    return selected


def model_commit_for_expected(row: Mapping[str, str]) -> str:
    if row["tool"] == "proverif":
        return (
            PV_ORIGINAL_MODEL
            if row["suite"] == "proverif-original"
            else PV_HMAC_MODEL
        )
    if row["milestone"] == "M1":
        return M1_MODEL
    if row["milestone"] == "M2":
        return M2_BASELINE
    if row["milestone"] == "M3" or row["suite"] in {"v6", "v7"}:
        return M3_BASELINE
    return M4_BASELINE


def target_matrix(
    root: Path, rows: Sequence[Mapping[str, str]]
) -> list[dict[str, str]]:
    result = []
    per_target_index: dict[tuple[str, str], int] = {}
    tree_cache: dict[str, str] = {}
    model_cache: dict[tuple[str, str], tuple[str, str]] = {}
    for row in rows:
        key = (row["suite"], row["target_id"])
        if row["tool"] == "proverif":
            per_target_index[key] = per_target_index.get(key, 0) + 1
            query_index = str(per_target_index[key])
        else:
            query_index = "0"
        model_commit = model_commit_for_expected(row)
        if model_commit not in tree_cache:
            tree_cache[model_commit] = str(
                run_git(root, "rev-parse", f"{model_commit}^{{tree}}")
            )
        model_key = (model_commit, row["model_path"])
        if model_key not in model_cache:
            model_cache[model_key] = (
                git_blob_oid(root, model_commit, row["model_path"]),
                sha256(git_blob(root, model_commit, row["model_path"])),
            )
        model_blob, model_sha = model_cache[model_key]
        result.append({
            "property_id": row["property_id"],
            "tool": row["tool"],
            "suite": row["suite"],
            "target_id": row["target_id"],
            "model_path": row["model_path"],
            "model_commit": model_commit,
            "model_tree": tree_cache[model_commit],
            "model_blob": model_blob,
            "model_sha256": model_sha,
            "query_index": query_index,
            "query_or_lemma": row["query_or_lemma"],
            "formula_sha256": row["formula_sha256"],
            "expected_status": row["expected_status"],
        })
    return result


def file_binding(root: Path, relative: str) -> tuple[str, str]:
    data = (root / relative).read_bytes()
    oid = str(run_git(root, "hash-object", "--", relative))
    return oid, sha256(data)


def worktree_contract_bindings(root: Path) -> dict[str, str]:
    artifact_blob, artifact_sha = file_binding(root, "artifact/README.md")
    expected_blob, expected_sha = file_binding(
        root, "artifact/results/expected-results.tsv"
    )
    return {
        "artifact_contract_blob": artifact_blob,
        "artifact_contract_sha256": artifact_sha,
        "expected_results_blob": expected_blob,
        "expected_results_sha256": expected_sha,
    }


def contract_bindings(root: Path, source_head: str | None = None) -> dict[str, str]:
    source_head = source_head or str(run_git(root, "rev-parse", "HEAD"))
    result = {}
    for prefix, relative in (
        ("artifact_contract", "artifact/README.md"),
        ("expected_results", "artifact/results/expected-results.tsv"),
    ):
        result[f"{prefix}_blob"] = git_blob_oid(root, source_head, relative)
        result[f"{prefix}_sha256"] = sha256(git_blob(root, source_head, relative))
    return result


def manifest_entries(run: Path) -> dict[str, str]:
    entries = {}
    for path in sorted(run.rglob("*")):
        if path.is_symlink():
            raise ContractError(f"source run contains symlink: {path}")
        if path.is_file() and path.name != "SHA256SUMS.txt":
            relative = path.relative_to(run).as_posix()
            entries[relative] = sha256(path.read_bytes())
    return entries


def write_manifest(run: Path) -> None:
    entries = manifest_entries(run)
    (run / "SHA256SUMS.txt").write_text(
        "".join(f"{digest}  {path}\n" for path, digest in entries.items()),
        encoding="utf-8",
        newline="\n",
    )


def validate_manifest(run: Path) -> dict[str, str]:
    manifest = run / "SHA256SUMS.txt"
    if not manifest.is_file():
        raise ContractError("source run manifest is missing")
    recorded: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if len(line) < 67 or line[64:66] != "  ":
            raise ContractError(f"invalid source manifest line: {line!r}")
        digest, relative = line[:64], line[66:]
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ContractError("invalid source manifest digest")
        normalized = Path(relative.replace("\\", "/"))
        if normalized.is_absolute() or ".." in normalized.parts:
            raise ContractError(f"unsafe source manifest path: {relative}")
        key = normalized.as_posix()
        if key in recorded:
            raise ContractError(f"duplicate source manifest path: {key}")
        recorded[key] = digest
    actual = manifest_entries(run)
    if set(recorded) != set(actual):
        missing = sorted(set(actual) - set(recorded))
        extra = sorted(set(recorded) - set(actual))
        raise ContractError(f"source manifest coverage mismatch: missing={missing} extra={extra}")
    for path, digest in actual.items():
        if recorded[path] != digest:
            raise ContractError(f"source manifest hash mismatch: {path}")
    return recorded


def write_provenance(path: Path, values: Mapping[str, str]) -> None:
    path.write_text(
        "".join(f"{key}={value}\n" for key, value in values.items()),
        encoding="utf-8",
        newline="\n",
    )


def _safe_raw(run: Path, relative: str) -> Path:
    candidate = (run / relative).resolve()
    try:
        candidate.relative_to(run.resolve())
    except ValueError as exc:
        raise ContractError(f"raw path escapes source run: {relative}") from exc
    if not relative.startswith("raw/"):
        raise ContractError(f"raw path is not under raw/: {relative}")
    return candidate


def _derive_actual(
    run: Path,
    row: Mapping[str, str],
    pv_cache: dict[str, list[str]],
) -> tuple[str, str]:
    raw = _safe_raw(run, row["raw_output"])
    if not raw.is_file():
        raise ContractError(f"raw output missing: {row['raw_output']}")
    try:
        exit_status = int(row["exit_status"])
    except ValueError as exc:
        raise ContractError(f"invalid target exit status: {row['property_id']}") from exc
    if row["tool"] == "tamarin-prover":
        return classify_tamarin(raw.read_text(encoding="utf-8", errors="replace"), exit_status)
    if exit_status != 0:
        if exit_status == 124:
            return "timeout", "timeout"
        if exit_status == 137:
            return "oom", "oom_or_sigkill"
        return "incomplete", "tool_or_parse_failure"
    pv_cache.setdefault(row["raw_output"], parse_proverif_output(raw.read_bytes()))
    index = int(row["query_index"])
    statuses = pv_cache[row["raw_output"]]
    if index < 1 or index > len(statuses):
        raise ContractError(f"ProVerif RESULT index missing: {row['property_id']}")
    return statuses[index - 1], "none"


def rederive_aggregate(
    run: Path, aggregate: Sequence[Mapping[str, str]]
) -> list[dict[str, str]]:
    pv_cache: dict[str, list[str]] = {}
    result = []
    for row in aggregate:
        actual, event = _derive_actual(run.resolve(), row, pv_cache)
        derived = dict(row)
        derived["actual_status"] = actual
        derived["resource_event"] = event
        result.append(derived)
    return result


def _validate_source_head(
    root: Path, provenance: Mapping[str, str]
) -> dict[str, str]:
    source_head = provenance["source_head"]
    if not re.fullmatch(r"[0-9a-f]{40}", source_head):
        raise ContractError("source provenance HEAD is not a full Git object ID")
    try:
        recorded_tree = str(run_git(root, "rev-parse", f"{source_head}^{{tree}}"))
    except ContractError as exc:
        raise ContractError("source provenance HEAD object is unavailable") from exc
    if recorded_tree != provenance["source_tree"]:
        raise ContractError("source provenance HEAD/tree binding mismatch")
    ancestor = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", BASE_COMMIT, source_head],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if ancestor.returncode != 0:
        raise ContractError("source provenance HEAD is not a descendant of BASE_COMMIT")
    try:
        committed = contract_bindings(root, source_head)
    except ContractError as exc:
        raise ContractError("source HEAD artifact contract is missing") from exc
    for key, value in committed.items():
        if provenance.get(key) != value:
            raise ContractError(f"source HEAD artifact contract binding mismatch: {key}")
    current = worktree_contract_bindings(root)
    for key, value in current.items():
        if committed[key] != value:
            raise ContractError(
                f"source HEAD contract differs from current validation contract: {key}"
            )
    return committed


def _input_relative(model_commit: str, model_path: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", model_commit):
        raise ContractError(f"invalid input model commit: {model_commit}")
    normalized = Path(model_path.replace("\\", "/"))
    if normalized.is_absolute() or ".." in normalized.parts or model_path.startswith("/"):
        raise ContractError(f"unsafe input model path: {model_path}")
    if normalized.as_posix() != model_path:
        raise ContractError(f"non-canonical input model path: {model_path}")
    return f"inputs/{model_commit}/{model_path}"


def _validate_inputs_and_formulas(
    root: Path,
    run: Path,
    manifest: Mapping[str, str],
    matrix: Sequence[dict[str, str]],
) -> int:
    require_unique(matrix, ["property_id"], "source target-matrix property")
    groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in matrix:
        groups.setdefault((row["model_commit"], row["model_path"]), []).append(row)
    expected_inputs = {
        _input_relative(commit, path) for commit, path in groups
    }
    manifest_inputs = {path for path in manifest if path.startswith("inputs/")}
    if manifest_inputs != expected_inputs:
        raise ContractError(
            "source input set differs from target matrix: "
            f"missing={sorted(expected_inputs - manifest_inputs)} "
            f"extra={sorted(manifest_inputs - expected_inputs)}"
        )
    pv_groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = {}
    tree_cache: dict[str, str] = {}
    for (model_commit, model_path), rows in groups.items():
        relative = _input_relative(model_commit, model_path)
        actual_path = (run / relative).resolve()
        try:
            actual_path.relative_to(run.resolve())
        except ValueError as exc:
            raise ContractError(f"input path escapes source run: {relative}") from exc
        if not actual_path.is_file():
            raise ContractError(f"declared source input is missing: {relative}")
        if relative not in manifest:
            raise ContractError(f"declared source input is absent from manifest: {relative}")
        frozen = git_blob(root, model_commit, model_path)
        actual = actual_path.read_bytes()
        expected_blob = git_blob_oid(root, model_commit, model_path)
        expected_sha = sha256(frozen)
        actual_sha = sha256(actual)
        if actual != frozen:
            raise ContractError(f"source input bytes differ from frozen Git blob: {relative}")
        if model_commit not in tree_cache:
            tree_cache[model_commit] = str(
                run_git(root, "rev-parse", f"{model_commit}^{{tree}}")
            )
        for row in rows:
            if row["model_tree"] != tree_cache[model_commit]:
                raise ContractError(f"input model tree mismatch: {row['property_id']}")
            if row["model_blob"] != expected_blob:
                raise ContractError(f"input model blob mismatch: {row['property_id']}")
            if row["model_sha256"] != expected_sha or row["model_sha256"] != actual_sha:
                raise ContractError(f"input model SHA-256 mismatch: {row['property_id']}")
            if row["tool"] == "tamarin-prover":
                formula = extract_tamarin_lemma(actual, row["query_or_lemma"])
                if formula_sha(formula) != row["formula_sha256"]:
                    raise ContractError(
                        f"Tamarin input formula mismatch: {row['property_id']}"
                    )
            elif row["tool"] == "proverif":
                pv_groups.setdefault(
                    (row["suite"], row["target_id"], model_commit, model_path), []
                ).append(row)
            else:
                raise ContractError(f"unsupported source tool: {row['tool']}")
    for key, rows in pv_groups.items():
        model_commit, model_path = key[2], key[3]
        actual = (run / _input_relative(model_commit, model_path)).read_bytes()
        queries = extract_proverif_queries(actual)
        try:
            indexed = sorted((int(row["query_index"]), row) for row in rows)
        except ValueError as exc:
            raise ContractError(f"invalid ProVerif query index: {key[:2]}") from exc
        indices = [index for index, _ in indexed]
        if indices != list(range(1, len(queries) + 1)):
            raise ContractError(
                f"ProVerif query indexes are not complete and contiguous: {key[:2]}"
            )
        for index, row in indexed:
            query = queries[index - 1]
            if query != row["query_or_lemma"]:
                raise ContractError(f"ProVerif input query text mismatch: {row['property_id']}")
            if formula_sha(query) != row["formula_sha256"]:
                raise ContractError(f"ProVerif input formula mismatch: {row['property_id']}")
    return len(groups)


def validate_source_run(
    root: Path,
    run: Path,
    mode: str,
    contract_rows: Sequence[dict[str, str]] | None = None,
    *,
    allow_invalid: bool = False,
) -> list[dict[str, str]]:
    run = run.resolve()
    manifest = validate_manifest(run)
    if not REQUIRED_SOURCE_FILES.issubset(manifest):
        raise ContractError(
            f"source run required files missing from manifest: "
            f"{sorted(REQUIRED_SOURCE_FILES - set(manifest))}"
        )
    if not any(path.startswith("inputs/") for path in manifest):
        raise ContractError("source run has no manifest-covered inputs")
    provenance = parse_key_values((run / "provenance.txt").read_bytes())
    required_provenance = {
        "mode", "run_id", "source_head", "source_tree", "target_count",
        "start_utc", "end_utc", "tool_versions_file", "resource_policy",
        "artifact_contract_blob", "artifact_contract_sha256",
        "expected_results_blob", "expected_results_sha256",
    }
    if not required_provenance.issubset(provenance):
        raise ContractError(
            f"source provenance incomplete: "
            f"{sorted(required_provenance - set(provenance))}"
        )
    if provenance["mode"] != mode:
        raise ContractError(f"source run mode mismatch: {provenance['mode']} != {mode}")
    if provenance["tool_versions_file"] != "versions.tsv":
        raise ContractError("source provenance tool_versions_file is not versions.tsv")
    if not all(provenance[key] for key in required_provenance):
        raise ContractError("source provenance contains an empty required value")
    _validate_source_head(root, provenance)
    expected = mode_rows(list(contract_rows or expected_rows(root)), mode)
    matrix_expected = target_matrix(root, expected)
    if int(provenance["target_count"]) != len(expected):
        raise ContractError("source provenance target count mismatch")
    matrix = read_tsv(run / "target-matrix.tsv", TARGET_HEADER)
    for row in matrix:
        validate_json_row(
            root / "artifact/schema/source-run-target-matrix.schema.json", row
        )
    _validate_inputs_and_formulas(root, run, manifest, matrix)
    if matrix != matrix_expected:
        raise ContractError("source target matrix differs from declared mode contract")
    aggregate = read_tsv(run / "aggregate.tsv", AGGREGATE_HEADER)
    require_unique(aggregate, ["property_id"], "source aggregate property")
    if {row["property_id"] for row in aggregate} != {
        row["property_id"] for row in matrix_expected
    }:
        raise ContractError("source aggregate property set is partial or unexpected")
    expected_by_id = {row["property_id"]: row for row in matrix_expected}
    for row in aggregate:
        declared = expected_by_id[row["property_id"]]
        for field in ("tool", "suite", "target_id", "query_index", "expected_status"):
            if row[field] != declared[field]:
                raise ContractError(
                    f"aggregate {field} differs from contract: {row['property_id']}"
                )
        raw_key = Path(row["raw_output"].replace("\\", "/")).as_posix()
        raw = _safe_raw(run, raw_key)
        if raw_key not in manifest:
            raise ContractError(f"raw output absent from manifest: {raw_key}")
    derived_valid = True
    derived_rows = {
        row["property_id"]: row for row in rederive_aggregate(run, aggregate)
    }
    for row in aggregate:
        actual = derived_rows[row["property_id"]]["actual_status"]
        event = derived_rows[row["property_id"]]["resource_event"]
        if row["actual_status"] != actual:
            raise ContractError(f"aggregate actual differs from raw: {row['property_id']}")
        if row["resource_event"] != event:
            raise ContractError(f"aggregate resource event differs from raw/exit: {row['property_id']}")
        if not terminal(actual) or actual != row["expected_status"] or row["exit_status"] != "0":
            derived_valid = False
    recorded_status = (run / "run-status.txt").read_text(encoding="utf-8").strip()
    derived_status = "VALID" if derived_valid else "INVALID"
    if recorded_status != derived_status:
        raise ContractError(
            f"run-status is not a revalidated conclusion: {recorded_status} != {derived_status}"
        )
    if not derived_valid and not allow_invalid:
        raise ContractError("source run is complete but has nonterminal or mismatching results")
    return aggregate


def create_synthetic_source_run(
    root: Path, run: Path, mode: str, *, run_id: str
) -> list[dict[str, str]]:
    run.mkdir(parents=True)
    rows = mode_rows(expected_rows(root), mode)
    matrix = target_matrix(root, rows)
    write_tsv(run / "target-matrix.tsv", TARGET_HEADER, matrix)
    (run / "versions.tsv").write_text(
        "tool\tobserved\nsynthetic\tproduction-validator-fixture\n",
        encoding="utf-8", newline="\n",
    )
    (run / "commands.tsv").write_text(
        "property_id\tcommand\n"
        + "".join(f"{row['property_id']}\tsynthetic\n" for row in matrix),
        encoding="utf-8", newline="\n",
    )
    materialized: set[tuple[str, str]] = set()
    for row in matrix:
        key = (row["model_commit"], row["model_path"])
        if key in materialized:
            continue
        materialized.add(key)
        input_path = run / _input_relative(*key)
        input_path.parent.mkdir(parents=True, exist_ok=True)
        input_path.write_bytes(git_blob(root, *key))
    aggregate = []
    pv_groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in matrix:
        if row["tool"] == "proverif":
            pv_groups.setdefault((row["suite"], row["target_id"]), []).append(row)
            continue
        raw_rel = f"raw/{row['suite']}/{row['property_id']}.out"
        raw = run / raw_rel
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_text(
            f"{row['target_id']} {row['expected_status']} (1 steps)\n",
            encoding="utf-8", newline="\n",
        )
        aggregate.append({
            "property_id": row["property_id"], "tool": row["tool"],
            "suite": row["suite"], "target_id": row["target_id"],
            "query_index": row["query_index"],
            "actual_status": row["expected_status"],
            "expected_status": row["expected_status"], "exit_status": "0",
            "resource_event": "none", "raw_output": raw_rel,
        })
    for (suite, target), group in pv_groups.items():
        raw_rel = f"raw/{suite}/{target}__queries.out"
        raw = run / raw_rel
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_text(
            "".join(
                f"RESULT synthetic_query_{row['query_index']} is {row['expected_status']}.\n"
                for row in group
            ),
            encoding="utf-8", newline="\n",
        )
        for row in group:
            aggregate.append({
                "property_id": row["property_id"], "tool": row["tool"],
                "suite": row["suite"], "target_id": row["target_id"],
                "query_index": row["query_index"],
                "actual_status": row["expected_status"],
                "expected_status": row["expected_status"], "exit_status": "0",
                "resource_event": "none", "raw_output": raw_rel,
            })
    order = {row["property_id"]: index for index, row in enumerate(matrix)}
    aggregate.sort(key=lambda row: order[row["property_id"]])
    write_tsv(run / "aggregate.tsv", AGGREGATE_HEADER, aggregate)
    (run / "run-status.txt").write_text("VALID\n", encoding="utf-8", newline="\n")
    head = str(run_git(root, "rev-parse", "HEAD"))
    tree = str(run_git(root, "rev-parse", "HEAD^{tree}"))
    write_provenance(run / "provenance.txt", {
        "mode": mode, "run_id": run_id, "source_head": head,
        "source_tree": tree, "target_count": str(len(matrix)),
        "start_utc": "2000-01-01T00:00:00Z", "end_utc": "2000-01-01T00:00:01Z",
        "tool_versions_file": "versions.tsv",
        "resource_policy": "synthetic-no-prover",
        **contract_bindings(root, head),
    })
    write_manifest(run)
    return aggregate


def assemble_runs(
    root: Path,
    run1: Path,
    run2: Path,
    output: Path,
    mode: str,
    *,
    policy: str = "run1-primary",
) -> int:
    if output.exists():
        raise ContractError(f"composite output already exists: {output}")
    first = validate_source_run(root, run1, mode, allow_invalid=True)
    second = validate_source_run(root, run2, mode, allow_invalid=True)
    one = {row["property_id"]: row for row in first}
    two = {row["property_id"]: row for row in second}
    declared = mode_rows(expected_rows(root), mode)
    declared_ids = {row["property_id"] for row in declared}
    if set(one) != declared_ids or set(two) != declared_ids:
        raise ContractError("composite source property sets differ from requested mode")
    if mode == "m4-tamarin" and len(declared_ids) != 296:
        raise ContractError("M4 composite mode is not exactly 296 properties")
    if policy not in {"run1-primary", "run2-primary"}:
        raise ContractError(f"undeclared fallback policy: {policy}")
    primary_name, fallback_name = (
        ("run1", "run2") if policy == "run1-primary" else ("run2", "run1")
    )
    primary, fallback = (one, two) if policy == "run1-primary" else (two, one)
    selection = []
    vector = []
    conflicts = unresolved = mismatches = fallback_count = 0
    expected_by_id = {row["property_id"]: row for row in declared}
    for property_id in [row["property_id"] for row in declared]:
        a, b = one[property_id], two[property_id]
        expected = expected_by_id[property_id]["expected_status"]
        if a["expected_status"] != expected or b["expected_status"] != expected:
            raise ContractError(f"run1/run2 expected disagreement: {property_id}")
        a_status, b_status = a["actual_status"], b["actual_status"]
        if terminal(a_status) and terminal(b_status) and a_status != b_status:
            conflicts += 1
            selected_run, selected_status, reason = "none", "conflict", "terminal conflict"
        elif terminal(primary[property_id]["actual_status"]):
            selected_run = primary_name
            selected_status = primary[property_id]["actual_status"]
            reason = "primary terminal"
        elif terminal(fallback[property_id]["actual_status"]):
            selected_run = fallback_name
            selected_status = fallback[property_id]["actual_status"]
            reason = "primary nonterminal; declared fallback terminal"
            fallback_count += 1
        else:
            selected_run, selected_status, reason = "none", "incomplete", "both nonterminal"
            unresolved += 1
        if selected_status != expected:
            mismatches += 1
        selection.append({
            "property_id": property_id, "tool": a["tool"], "suite": a["suite"],
            "target_id": a["target_id"], "expected_status": expected,
            "run1_status": a_status, "run2_status": b_status,
            "selected_run": selected_run, "selected_status": selected_status,
            "selection_reason": reason,
        })
        vector.append({
            "property_id": property_id, "tool": a["tool"], "suite": a["suite"],
            "target_id": a["target_id"], "actual_status": selected_status,
            "expected_status": expected, "selected_run": selected_run,
            "match": "MATCH" if selected_status == expected else "MISMATCH",
        })
    if conflicts or unresolved or mismatches:
        raise ContractError(
            f"composite invalid: conflicts={conflicts} unresolved={unresolved} "
            f"mismatches={mismatches}"
        )
    output.mkdir(parents=True)
    write_tsv(output / "composite-selection.tsv", SELECTION_HEADER, selection)
    write_tsv(output / "composite-result-vector.tsv", VECTOR_HEADER, vector)
    (output / "composite-summary.txt").write_text(
        f"classification=transparent composite\nmode={mode}\npolicy={policy}\n"
        f"targets={len(selection)}\nfallback={fallback_count}\n"
        "terminal_conflicts=0\nunresolved=0\nmismatches=0\n",
        encoding="utf-8", newline="\n",
    )
    write_manifest(output)
    return len(selection)


def validate_composite(
    root: Path, output: Path, run1: Path, run2: Path, mode: str, policy: str
) -> int:
    validate_manifest(output)
    if policy not in {"run1-primary", "run2-primary"}:
        raise ContractError(f"undeclared fallback policy: {policy}")
    expected = mode_rows(expected_rows(root), mode)
    selection = read_tsv(output / "composite-selection.tsv", SELECTION_HEADER)
    vector = read_tsv(output / "composite-result-vector.tsv", VECTOR_HEADER)
    if len(selection) != len(expected) or len(vector) != len(expected):
        raise ContractError("composite output is partial")
    require_unique(selection, ["property_id"], "composite selection property")
    require_unique(vector, ["property_id"], "composite vector property")
    first = {row["property_id"]: row for row in validate_source_run(root, run1, mode, allow_invalid=True)}
    second = {row["property_id"]: row for row in validate_source_run(root, run2, mode, allow_invalid=True)}
    sindex = {row["property_id"]: row for row in selection}
    vindex = {row["property_id"]: row for row in vector}
    expected_ids = {row["property_id"] for row in expected}
    if set(sindex) != expected_ids or set(vindex) != expected_ids:
        raise ContractError("composite property set differs from requested mode")
    fallback_count = 0
    for declared in expected:
        property_id = declared["property_id"]
        row = sindex[property_id]
        primary = first if policy == "run1-primary" else second
        fallback = second if policy == "run1-primary" else first
        primary_name = "run1" if policy == "run1-primary" else "run2"
        fallback_name = "run2" if policy == "run1-primary" else "run1"
        a, b = first[property_id]["actual_status"], second[property_id]["actual_status"]
        if terminal(a) and terminal(b) and a != b:
            raise ContractError(f"terminal conflict: {property_id}")
        if terminal(primary[property_id]["actual_status"]):
            legal, status, reason = (
                primary_name, primary[property_id]["actual_status"], "primary terminal"
            )
        elif terminal(fallback[property_id]["actual_status"]):
            legal, status, reason = (
                fallback_name,
                fallback[property_id]["actual_status"],
                "primary nonterminal; declared fallback terminal",
            )
            fallback_count += 1
        else:
            legal, status, reason = "none", "incomplete", "both nonterminal"
        expected_selection = {
            "property_id": property_id,
            "tool": first[property_id]["tool"],
            "suite": first[property_id]["suite"],
            "target_id": first[property_id]["target_id"],
            "expected_status": declared["expected_status"],
            "run1_status": a,
            "run2_status": b,
            "selected_run": legal,
            "selected_status": status,
            "selection_reason": reason,
        }
        if row != expected_selection:
            raise ContractError(f"illegal fallback selection: {property_id}")
        expected_vector = {
            "property_id": property_id,
            "tool": first[property_id]["tool"],
            "suite": first[property_id]["suite"],
            "target_id": first[property_id]["target_id"],
            "actual_status": status,
            "expected_status": declared["expected_status"],
            "selected_run": legal,
            "match": "MATCH" if status == declared["expected_status"] else "MISMATCH",
        }
        if vindex[property_id] != expected_vector:
            raise ContractError(f"composite vector cannot be reconstructed: {property_id}")
    summary = parse_key_values((output / "composite-summary.txt").read_bytes())
    required_summary = {
        "classification": "transparent composite",
        "mode": mode,
        "policy": policy,
        "targets": str(len(expected)),
        "fallback": str(fallback_count),
        "terminal_conflicts": "0",
        "unresolved": "0",
        "mismatches": "0",
    }
    if any(summary.get(key) != value for key, value in required_summary.items()):
        raise ContractError("composite summary cannot be reconstructed")
    return len(selection)
