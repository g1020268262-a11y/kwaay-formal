#!/usr/bin/env python3
"""Positive contract checks plus production-path tamper rejection tests."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/artifact"))

from contract import BASE_TREE, read_tsv, sha256, validate_repository_facts  # noqa: E402
from generate_actual import committed_rows, new_source_rows  # noqa: E402
from source_runs import (  # noqa: E402
    assemble_runs,
    create_synthetic_source_run,
    TARGET_HEADER,
    validate_composite,
    validate_manifest,
    validate_source_run,
)

FIXTURE = Path(__file__).with_name("negative_fixture.py")
NEGATIVE_CASES = [
    "formula-hash-tamper",
    "expected-actual-mismatch",
    "actual-generator-tamper",
    "illegal-fallback",
    "false-m4-proverif-rerun",
    "partial-valid",
    "missing-manifest",
    "manifest-hash-tamper",
    "aggregate-raw-mismatch",
    "aggregate-tool-tamper",
    "aggregate-suite-tamper",
    "aggregate-target-tamper",
    "contract-hash-tamper",
    "raw-path-traversal",
    "run-expected-disagreement",
    "terminal-conflict",
    "missing-target",
    "duplicate-property",
    "wrong-mode",
    "wrong-provenance",
    "assembly-missing-target",
    "dirty-worktree",
    "base-not-ancestor",
    "wrong-base-tree",
    "input-byte-tamper-with-regenerated-manifest",
    "missing-declared-input",
    "extra-undeclared-input",
    "input-model-commit-tamper",
    "input-model-path-tamper",
    "input-model-blob-tamper",
    "input-model-sha256-tamper",
    "input-formula-mismatch",
    "proverif-query-index-mismatch",
    "proverif-query-text-mismatch",
    "source-head-contract-missing",
    "source-head-contract-blob-mismatch",
    "source-head-not-descendant-of-base",
]


def positive_repository_portability() -> None:
    for checkout in ("commit-a", "descendant", "main-like", "detached"):
        validate_repository_facts(
            base_tree=BASE_TREE,
            base_is_ancestor=True,
            status="",
            allow_dirty=False,
        )
        print(f"repository_checkout[{checkout}]=PASS")


def positive_source_and_actual() -> None:
    with tempfile.TemporaryDirectory(prefix="kwaay-artifact-positive-") as tmp:
        base = Path(tmp)
        one, two = base / "run1", base / "run2"
        create_synthetic_source_run(ROOT, one, "smoke", run_id="positive-1")
        create_synthetic_source_run(ROOT, two, "smoke", run_id="positive-2")
        rows = validate_source_run(ROOT, one, "smoke")
        if len(rows) != 2:
            raise AssertionError(f"smoke row count differs: {len(rows)}")
        actual = new_source_rows(ROOT, one, "smoke")
        if len(actual) != len(rows) or any(row["expected_match"] != "MATCH" for row in actual):
            raise AssertionError("source actual generation is not raw-revalidated")
        matrix = read_tsv(one / "target-matrix.tsv", TARGET_HEADER)
        manifest = validate_manifest(one)
        expected_inputs = {
            f"inputs/{row['model_commit']}/{row['model_path']}" for row in matrix
        }
        actual_inputs = {path for path in manifest if path.startswith("inputs/")}
        if expected_inputs != actual_inputs:
            raise AssertionError("synthetic frozen input set differs from target matrix")
        if any(
            row["evidence_commit"] or row["evidence_tree"]
            or row["evidence_storage"] != "external-manifest"
            or row["evidence_manifest_sha256"]
            != sha256((one / "SHA256SUMS.txt").read_bytes())
            for row in actual
        ):
            raise AssertionError("external evidence incorrectly claims Git storage")
        composite = base / "composite"
        assembled = assemble_runs(ROOT, one, two, composite, "smoke")
        validated = validate_composite(
            ROOT, composite, one, two, "smoke", "run1-primary"
        )
        if assembled != 2 or validated != 2:
            raise AssertionError("smoke composite count differs")
        print("synthetic_source_run=PASS manifest_valid complete raw_revalidated")
        print(
            f"synthetic_inputs=PASS unique_models={len(expected_inputs)} "
            "git_blob_bytes formula query source_head_contract"
        )
        print("synthetic_actual_generator=PASS")
        print("synthetic_actual_storage=PASS external_manifest uncommitted_evidence")
        print("synthetic_assemble=PASS property_id_keyed")


def positive_committed_actual() -> None:
    rows = committed_rows(ROOT)
    inherited = [row for row in rows if row["direct_or_inherited"] == "inherited"]
    scope = [row for row in rows if row["evidence_class"] == "scope-declaration"]
    if not inherited or any(row["evidence_commit"] == rows[0]["evidence_commit"] for row in inherited):
        raise AssertionError("inherited ProVerif evidence provenance was flattened")
    if not scope or any(
        row["actual_status"] != "not_run_out_of_scope"
        or row["terminal"] != "false"
        or row["expected_match"] != "MATCH"
        or row["direct_or_inherited"] != "direct"
        for row in scope
    ):
        raise AssertionError("M4 ProVerif scope rows are not explicit")
    if any(row["evidence_storage"] != "committed-git" for row in inherited):
        raise AssertionError("inherited ProVerif storage is not committed-git")
    original = [row for row in inherited if row["suite"] == "proverif-original"]
    if any(
        row["model_commit"] != "ff93107cd7911fbd22b66c45391eff2aecf51b9f"
        or row["evidence_commit"] != "ff93107cd7911fbd22b66c45391eff2aecf51b9f"
        for row in original
    ):
        raise AssertionError("original ProVerif model/evidence snapshot is not exact")
    if any(row["evidence_storage"] != "scope-declaration" for row in scope):
        raise AssertionError("scope evidence storage is not scope-declaration")
    print(
        f"committed_actual=PASS rows={len(rows)} inherited={len(inherited)} "
        f"scope={len(scope)}"
    )


def negative_fixtures() -> None:
    failures = 0
    for case in NEGATIVE_CASES:
        proc = subprocess.run(
            [sys.executable, "-B", str(FIXTURE), case],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            print(f"negative_fixture[{case}]=FAIL accepted")
            failures += 1
        elif "production_rejection=ContractError:" not in proc.stderr:
            print(
                f"negative_fixture[{case}]=FAIL non-contract error "
                f"rc={proc.returncode} stderr={proc.stderr.strip()}"
            )
            failures += 1
        else:
            reason = proc.stderr.strip().split("production_rejection=", 1)[1]
            print(f"negative_fixture[{case}]=PASS {reason}")
    if failures:
        raise AssertionError(f"negative fixture failures: {failures}")


def repository_status() -> str:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode:
        raise AssertionError(f"git status failed: {proc.stderr.strip()}")
    return proc.stdout


def bytecode_paths() -> list[str]:
    found = []
    for base in (ROOT / "scripts", ROOT / "artifact"):
        for path in base.rglob("*"):
            if path.is_dir() and path.name == "__pycache__":
                found.append(path.relative_to(ROOT).as_posix() + "/")
            elif path.is_file() and path.suffix in {".pyc", ".pyo"}:
                found.append(path.relative_to(ROOT).as_posix())
    return sorted(found)


def wrapper_cleanliness() -> None:
    if repository_status():
        raise AssertionError("wrapper regression requires a clean repository")
    before = bytecode_paths()
    if before:
        raise AssertionError(f"bytecode exists before wrapper regression: {before}")
    environment = os.environ.copy()
    environment.pop("PYTHONDONTWRITEBYTECODE", None)
    proc = subprocess.run(
        ["bash", "scripts/run-paper-artifact.sh", "verify-committed"],
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if proc.returncode:
        raise AssertionError(
            f"production wrapper verify-committed failed ({proc.returncode}):\n"
            f"{proc.stdout}"
        )
    if "verify_committed=PASS" not in proc.stdout:
        raise AssertionError("production wrapper did not report verify_committed=PASS")
    if repository_status():
        raise AssertionError("production wrapper dirtied the repository")
    after = bytecode_paths()
    if after:
        raise AssertionError(f"production wrapper wrote bytecode: {after}")
    print("wrapper_verify_committed=PASS")
    print("wrapper_bytecode_cleanliness=PASS")


def main() -> int:
    positive_repository_portability()
    positive_source_and_actual()
    positive_committed_actual()
    negative_fixtures()
    wrapper_cleanliness()
    print(f"negative_fixtures={len(NEGATIVE_CASES)} failures=0")
    print("artifact_validation=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
