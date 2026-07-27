#!/usr/bin/env python3
"""Tamper a real synthetic source-run and invoke the production validator."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/artifact"))

from contract import (  # noqa: E402
    BASE_TREE,
    ContractError,
    read_tsv,
    run_git,
    validate_repository_facts,
    write_tsv,
)
from generate_actual import new_source_rows  # noqa: E402
from source_runs import (  # noqa: E402
    AGGREGATE_HEADER,
    SELECTION_HEADER,
    TARGET_HEADER,
    assemble_runs,
    create_synthetic_source_run,
    validate_composite,
    validate_source_run,
    write_manifest,
)


def opposite(status: str) -> str:
    return "falsified" if status == "verified" else (
        "verified" if status == "falsified" else (
            "false" if status == "true" else "true"
        )
    )


def rewrite_rows(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    write_tsv(path, header, rows)


def mutate_raw_to_opposite(run: Path, row: dict[str, str]) -> str:
    changed = opposite(row["expected_status"])
    raw = run / row["raw_output"]
    if row["tool"] == "proverif":
        raw.write_text(
            f"RESULT synthetic_query_1 is {changed}.\n",
            encoding="utf-8",
            newline="\n",
        )
    else:
        raw.write_text(
            f"{row['target_id']} {changed} (1 steps)\n",
            encoding="utf-8",
            newline="\n",
        )
    return changed


def make_run(base: Path, name: str, mode: str = "smoke") -> Path:
    run = base / name
    create_synthetic_source_run(ROOT, run, mode, run_id=name)
    validate_source_run(ROOT, run, mode)
    return run


def reject_source(run: Path, mode: str = "smoke") -> None:
    validate_source_run(ROOT, run, mode)


def replace_provenance(run: Path, key: str, value: str) -> None:
    lines = (run / "provenance.txt").read_text(encoding="utf-8").splitlines()
    found = False
    updated = []
    for line in lines:
        if line.startswith(f"{key}="):
            updated.append(f"{key}={value}")
            found = True
        else:
            updated.append(line)
    if not found:
        updated.append(f"{key}={value}")
    (run / "provenance.txt").write_text(
        "\n".join(updated) + "\n", encoding="utf-8", newline="\n"
    )


def execute(case: str, base: Path) -> None:
    if case == "dirty-worktree":
        validate_repository_facts(
            base_tree=BASE_TREE, base_is_ancestor=True, status=" M artifact/x", allow_dirty=False
        )
        return
    if case == "base-not-ancestor":
        validate_repository_facts(
            base_tree=BASE_TREE, base_is_ancestor=False, status="", allow_dirty=False
        )
        return
    if case == "wrong-base-tree":
        validate_repository_facts(
            base_tree="0" * 40, base_is_ancestor=True, status="", allow_dirty=False
        )
        return

    if case in {"illegal-fallback", "run-expected-disagreement", "terminal-conflict",
                "assembly-missing-target"}:
        one = make_run(base, "run1")
        two = make_run(base, "run2")
        if case == "illegal-fallback":
            out = base / "composite"
            assemble_runs(ROOT, one, two, out, "smoke")
            rows = read_tsv(out / "composite-selection.tsv", SELECTION_HEADER)
            rows[0]["selected_run"] = "run2"
            rewrite_rows(out / "composite-selection.tsv", SELECTION_HEADER, rows)
            write_manifest(out)
            validate_composite(ROOT, out, one, two, "smoke", "run1-primary")
            return
        rows = read_tsv(two / "aggregate.tsv", AGGREGATE_HEADER)
        if case == "run-expected-disagreement":
            matrix = read_tsv(two / "target-matrix.tsv", TARGET_HEADER)
            matrix[0]["expected_status"] = opposite(matrix[0]["expected_status"])
            rows[0]["expected_status"] = matrix[0]["expected_status"]
            rewrite_rows(two / "target-matrix.tsv", TARGET_HEADER, matrix)
        elif case == "terminal-conflict":
            rows[0]["actual_status"] = mutate_raw_to_opposite(two, rows[0])
            (two / "run-status.txt").write_text("INVALID\n", encoding="utf-8", newline="\n")
        else:
            rows.pop()
        rewrite_rows(two / "aggregate.tsv", AGGREGATE_HEADER, rows)
        write_manifest(two)
        assemble_runs(ROOT, one, two, base / "composite", "smoke")
        return

    mode = "m4-tamarin" if case in {"false-m4-proverif-rerun", "partial-valid"} else "smoke"
    run = make_run(base, "run", mode)
    aggregate = read_tsv(run / "aggregate.tsv", AGGREGATE_HEADER)
    matrix = read_tsv(run / "target-matrix.tsv", TARGET_HEADER)
    tamarin_row = next(row for row in matrix if row["tool"] == "tamarin-prover")
    proverif_row = next(
        (row for row in matrix if row["tool"] == "proverif"), None
    )
    input_path = (
        run / "inputs" / tamarin_row["model_commit"] / tamarin_row["model_path"]
    )

    if case == "formula-hash-tamper":
        matrix[0]["formula_sha256"] = "0" * 64
        rewrite_rows(run / "target-matrix.tsv", TARGET_HEADER, matrix)
        write_manifest(run)
    elif case == "input-byte-tamper-with-regenerated-manifest":
        input_path.write_bytes(input_path.read_bytes() + b"\n/* tampered input */\n")
        write_manifest(run)
    elif case == "missing-declared-input":
        input_path.unlink()
        write_manifest(run)
    elif case == "extra-undeclared-input":
        extra = run / "inputs" / "undeclared-model.pv"
        extra.write_text("free x:bitstring.\n", encoding="utf-8", newline="\n")
        write_manifest(run)
    elif case == "input-model-commit-tamper":
        tamarin_row["model_commit"] = "0" * 40
        rewrite_rows(run / "target-matrix.tsv", TARGET_HEADER, matrix)
        write_manifest(run)
    elif case == "input-model-path-tamper":
        tamarin_row["model_path"] = "tamarin/no-such-model.spthy"
        rewrite_rows(run / "target-matrix.tsv", TARGET_HEADER, matrix)
        write_manifest(run)
    elif case == "input-model-blob-tamper":
        tamarin_row["model_blob"] = "0" * 40
        rewrite_rows(run / "target-matrix.tsv", TARGET_HEADER, matrix)
        write_manifest(run)
    elif case == "input-model-sha256-tamper":
        tamarin_row["model_sha256"] = "0" * 64
        rewrite_rows(run / "target-matrix.tsv", TARGET_HEADER, matrix)
        write_manifest(run)
    elif case == "input-formula-mismatch":
        tamarin_row["formula_sha256"] = "0" * 64
        rewrite_rows(run / "target-matrix.tsv", TARGET_HEADER, matrix)
        write_manifest(run)
    elif case == "proverif-query-index-mismatch":
        assert proverif_row is not None
        proverif_row["query_index"] = "2"
        rewrite_rows(run / "target-matrix.tsv", TARGET_HEADER, matrix)
        write_manifest(run)
    elif case == "proverif-query-text-mismatch":
        assert proverif_row is not None
        proverif_row["query_or_lemma"] += " tampered"
        rewrite_rows(run / "target-matrix.tsv", TARGET_HEADER, matrix)
        write_manifest(run)
    elif case == "source-head-contract-missing":
        replace_provenance(run, "source_head", "211ffd0a8ed8a7051d12dcc165566a66e64ab970")
        replace_provenance(run, "source_tree", BASE_TREE)
        write_manifest(run)
    elif case == "source-head-contract-blob-mismatch":
        replace_provenance(run, "artifact_contract_blob", "0" * 40)
        write_manifest(run)
    elif case == "source-head-not-descendant-of-base":
        root_commit = str(run_git(ROOT, "rev-list", "--max-parents=0", "HEAD")).splitlines()[0]
        root_tree = str(run_git(ROOT, "rev-parse", f"{root_commit}^{{tree}}"))
        replace_provenance(run, "source_head", root_commit)
        replace_provenance(run, "source_tree", root_tree)
        write_manifest(run)
    elif case == "expected-actual-mismatch":
        aggregate[0]["actual_status"] = mutate_raw_to_opposite(run, aggregate[0])
        (run / "run-status.txt").write_text("INVALID\n", encoding="utf-8", newline="\n")
        rewrite_rows(run / "aggregate.tsv", AGGREGATE_HEADER, aggregate)
        write_manifest(run)
    elif case == "actual-generator-tamper":
        mutate_raw_to_opposite(run, aggregate[0])
        write_manifest(run)
        new_source_rows(ROOT, run, mode)
        return
    elif case == "false-m4-proverif-rerun":
        matrix[0]["tool"] = "proverif"
        aggregate[0]["tool"] = "proverif"
        rewrite_rows(run / "target-matrix.tsv", TARGET_HEADER, matrix)
        rewrite_rows(run / "aggregate.tsv", AGGREGATE_HEADER, aggregate)
        write_manifest(run)
    elif case == "partial-valid":
        removed = aggregate.pop()
        matrix.pop()
        raw = run / removed["raw_output"]
        raw.unlink()
        rewrite_rows(run / "target-matrix.tsv", TARGET_HEADER, matrix)
        rewrite_rows(run / "aggregate.tsv", AGGREGATE_HEADER, aggregate)
        write_manifest(run)
    elif case == "missing-manifest":
        (run / "SHA256SUMS.txt").unlink()
    elif case == "manifest-hash-tamper":
        (run / aggregate[0]["raw_output"]).write_text("tampered\n", encoding="utf-8")
    elif case == "aggregate-raw-mismatch":
        aggregate[0]["actual_status"] = opposite(aggregate[0]["actual_status"])
        rewrite_rows(run / "aggregate.tsv", AGGREGATE_HEADER, aggregate)
        write_manifest(run)
    elif case in {"aggregate-tool-tamper", "aggregate-suite-tamper",
                  "aggregate-target-tamper"}:
        field = case.removeprefix("aggregate-").removesuffix("-tamper")
        field = "target_id" if field == "target" else field
        aggregate[0][field] = f"tampered-{field}"
        rewrite_rows(run / "aggregate.tsv", AGGREGATE_HEADER, aggregate)
        write_manifest(run)
    elif case == "contract-hash-tamper":
        provenance = (run / "provenance.txt").read_text(encoding="utf-8")
        provenance = provenance.replace(
            "expected_results_sha256=", "expected_results_sha256=" + "0" * 64 + "#"
        )
        (run / "provenance.txt").write_text(provenance, encoding="utf-8", newline="\n")
        write_manifest(run)
    elif case == "raw-path-traversal":
        aggregate[0]["raw_output"] = "../escape.out"
        rewrite_rows(run / "aggregate.tsv", AGGREGATE_HEADER, aggregate)
        write_manifest(run)
    elif case == "missing-target":
        aggregate.pop()
        rewrite_rows(run / "aggregate.tsv", AGGREGATE_HEADER, aggregate)
        write_manifest(run)
    elif case == "duplicate-property":
        aggregate.append(dict(aggregate[0]))
        rewrite_rows(run / "aggregate.tsv", AGGREGATE_HEADER, aggregate)
        write_manifest(run)
    elif case == "wrong-mode":
        reject_source(run, "full")
        return
    elif case == "wrong-provenance":
        lines = (run / "provenance.txt").read_text(encoding="utf-8").splitlines()
        (run / "provenance.txt").write_text(
            "\n".join(line for line in lines if not line.startswith("source_tree=")) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        write_manifest(run)
    else:
        raise ValueError(f"unknown fixture: {case}")
    reject_source(run, mode)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="kwaay-artifact-negative-") as tmp:
        try:
            execute(args.case, Path(tmp))
        except ContractError as exc:
            print(f"production_rejection={type(exc).__name__}: {exc}", file=sys.stderr)
            return 1
    print(f"fixture unexpectedly accepted: {args.case}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
