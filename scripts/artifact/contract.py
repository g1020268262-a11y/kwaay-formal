#!/usr/bin/env python3
"""Shared, dependency-free mechanics for the K-Waay paper artifact."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Mapping, Sequence

BASE_COMMIT = "211ffd0a8ed8a7051d12dcc165566a66e64ab970"
BASE_TREE = "58225429c034bbe2804f735646b3fa0dd2aa9919"
M2_BASELINE = "841feabd908a01bdc68669ad99253a6755820389"
M3_BASELINE = "282532fd922f3a7f7928f3772b3325fe06785730"
M4_BASELINE = "96010c72e71defc775c7c2ee99c937ff700a3227"
M4_TREE = "3ef9d77f1fbb969ba6f3cff14eae9bab229f59c8"
EXPECTED_HEADER = [
    "schema_version", "property_id", "claim_id", "milestone", "tool",
    "suite", "target_id", "model_path", "query_or_lemma", "formula_sha256",
    "property_kind", "expected_status", "expected_evidence_class",
    "execution_scope", "conditional_interface", "required",
    "timeout_seconds", "memory_policy", "expectation_source_path",
    "expectation_source_commit", "expectation_source_blob",
    "regression_matrix_path", "regression_matrix_commit",
    "regression_matrix_blob", "notes",
]
ACTUAL_HEADER = [
    "schema_version", "run_id", "property_id", "tool", "suite", "target_id",
    "actual_status", "terminal", "expected_match", "evidence_class",
    "execution_scope", "direct_or_inherited", "source_commit", "source_tree",
    "model_commit", "model_tree", "evidence_commit", "evidence_tree",
    "evidence_storage", "evidence_manifest_sha256",
    "source_run", "selected_run", "selection_reason", "exit_status",
    "resource_event", "steps", "raw_path", "raw_blob", "raw_sha256",
    "summary_path", "provenance_valid", "terminal_conflict",
]
PAPER_HEADER = [
    "artifact_id", "path", "artifact_class", "milestone", "paper_role",
    "authoritative_or_generated", "evidence_path", "freeze_status",
    "known_limitation",
]
FROZEN_HEADER = [
    "path", "source_commit", "git_blob", "blob_sha256", "content_role",
]
CLAIM_HEADER = [
    "claim_id", "paper_class", "property_id", "evidence_role", "model_path",
    "evidence_path", "assumptions_ref", "limitations_ref",
    "allowed_statement_ref", "prohibited_statement_ref", "status",
]


class ContractError(RuntimeError):
    """A contract violation that must propagate to a nonzero exit."""


def run_git(root: Path, *args: str, binary: bool = False) -> str | bytes:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise ContractError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    return proc.stdout if binary else proc.stdout.decode("utf-8").rstrip("\r\n")


def repo_root(start: Path | None = None) -> Path:
    start = (start or Path(__file__).resolve()).resolve()
    base = start if start.is_dir() else start.parent
    return Path(str(run_git(base, "rev-parse", "--show-toplevel"))).resolve()


@lru_cache(maxsize=4096)
def git_blob(root: Path, commit: str, path: str) -> bytes:
    return run_git(root, "cat-file", "blob", f"{commit}:{path}", binary=True)  # type: ignore[return-value]


@lru_cache(maxsize=4096)
def git_blob_oid(root: Path, commit: str, path: str) -> str:
    return str(run_git(root, "rev-parse", f"{commit}:{path}"))


def git_blobs(root: Path, commit: str, paths: Sequence[str]) -> list[bytes]:
    specs = [f"{commit}:{path}" for path in paths]
    proc = subprocess.run(
        ["git", "-C", str(root), "cat-file", "--batch"],
        input=("".join(spec + "\n" for spec in specs)).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise ContractError(
            f"git cat-file --batch failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    output = proc.stdout
    position = 0
    blobs: list[bytes] = []
    for spec in specs:
        newline = output.find(b"\n", position)
        if newline < 0:
            raise ContractError(f"truncated git cat-file header for {spec}")
        header = output[position:newline].decode("ascii", "replace").split()
        position = newline + 1
        if len(header) == 2 and header[1] == "missing":
            raise ContractError(f"Git blob missing: {spec}")
        if len(header) != 3 or header[1] != "blob":
            raise ContractError(f"unexpected git cat-file header for {spec}: {header}")
        size = int(header[2])
        blob = output[position:position + size]
        if len(blob) != size or output[position + size:position + size + 1] != b"\n":
            raise ContractError(f"truncated git blob for {spec}")
        blobs.append(blob)
        position += size + 1
    return blobs


def verify_git_objects_exist(root: Path, commit: str, paths: Sequence[str]) -> None:
    proc = subprocess.run(
        ["git", "-C", str(root), "cat-file", "--batch-check"],
        input=("".join(f"{commit}:{path}\n" for path in paths)).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise ContractError(f"git cat-file --batch-check failed ({proc.returncode})")
    lines = proc.stdout.decode("utf-8", "replace").splitlines()
    if len(lines) != len(paths):
        raise ContractError("git batch-check response count mismatch")
    for path, line in zip(paths, lines, strict=True):
        fields = line.split()
        if len(fields) != 3 or fields[1] != "blob":
            raise ContractError(f"Git blob missing or not a blob: {path}")


def git_blob_metadata(root: Path, commit: str, paths: Sequence[str]) -> list[tuple[str, int]]:
    proc = subprocess.run(
        ["git", "-C", str(root), "cat-file", "--batch-check"],
        input=("".join(f"{commit}:{path}\n" for path in paths)).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise ContractError(f"git cat-file --batch-check failed ({proc.returncode})")
    lines = proc.stdout.decode("utf-8", "replace").splitlines()
    if len(lines) != len(paths):
        raise ContractError("git batch-check response count mismatch")
    result = []
    for path, line in zip(paths, lines, strict=True):
        fields = line.split()
        if len(fields) != 3 or fields[1] != "blob":
            raise ContractError(f"Git blob missing or not a blob: {path}")
        result.append((fields[0], int(fields[2])))
    return result


def git_blob_sha256s(root: Path, commit: str, paths: Sequence[str]) -> list[str]:
    proc = subprocess.Popen(
        ["git", "-C", str(root), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None and proc.stdout is not None
    digests: list[str] = []
    try:
        for path in paths:
            proc.stdin.write(f"{commit}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("ascii", "replace").split()
            if len(header) != 3 or header[1] != "blob":
                raise ContractError(f"Git blob missing or not a blob: {path}")
            remaining = int(header[2])
            digest = hashlib.sha256()
            while remaining:
                chunk = proc.stdout.read(min(1024 * 1024, remaining))
                if not chunk:
                    raise ContractError(f"truncated Git blob: {path}")
                digest.update(chunk)
                remaining -= len(chunk)
            if proc.stdout.read(1) != b"\n":
                raise ContractError(f"missing Git batch delimiter: {path}")
            digests.append(digest.hexdigest())
        proc.stdin.close()
        if proc.wait() != 0:
            stderr = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
            raise ContractError(f"git cat-file --batch failed: {stderr.strip()}")
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
    return digests


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_tsv_bytes(data: bytes, expected_header: Sequence[str] | None = None) -> list[dict[str, str]]:
    text = data.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    if reader.fieldnames is None:
        raise ContractError("TSV has no header")
    if expected_header is not None and reader.fieldnames != list(expected_header):
        raise ContractError(
            f"TSV header mismatch: {reader.fieldnames!r} != {list(expected_header)!r}"
        )
    rows = list(reader)
    if any(None in row for row in rows):
        raise ContractError("TSV row has extra fields")
    return rows


def read_tsv(path: Path, expected_header: Sequence[str] | None = None) -> list[dict[str, str]]:
    return read_tsv_bytes(path.read_bytes(), expected_header)


def write_tsv(path: Path, header: Sequence[str], rows: Iterable[Mapping[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(header), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for row in rows:
            if set(row) != set(header):
                raise ContractError(f"row keys differ from header for {path}")
            if any("\t" in value or "\n" in value or "\r" in value for value in row.values()):
                raise ContractError(f"TSV value contains a forbidden control character: {path}")
            writer.writerow(row)


def normalize_formula(text: str) -> str:
    """Match M4's comment removal followed by deletion of all whitespace."""
    text = re.sub(r"/\*(?:[^*]|\*+[^*/])*\*/", "", text)
    text = re.sub(r"//.*$", "", text, flags=re.MULTILINE)
    return re.sub(r"\s+", "", text)


def extract_tamarin_lemma(model: bytes, lemma: str) -> str:
    text = model.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines()
    head = f"lemma {lemma}:"
    starts = [index for index, line in enumerate(lines) if line == head]
    if len(starts) != 1:
        raise ContractError(f"lemma {lemma!r} occurs {len(starts)} times")
    block: list[str] = []
    for line in lines[starts[0] :]:
        if block and (
            re.match(r"^(?:rule|lemma) [A-Za-z0-9_]+:", line)
            or line.startswith("/*")
            or line == "end"
        ):
            break
        block.append(line)
    normalized = normalize_formula("\n".join(block) + "\n")
    if not normalized:
        raise ContractError(f"lemma {lemma!r} has an empty normalized formula")
    return normalized


def extract_proverif_queries(model: bytes) -> list[str]:
    text = model.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\(\*.*?\*\)", "", text, flags=re.DOTALL)
    queries = [
        normalize_formula(match.group(0))
        for match in re.finditer(r"(?m)^[ \t]*query\b.*?\.", text, flags=re.DOTALL)
    ]
    if not queries or any(not query for query in queries):
        raise ContractError("generated ProVerif model has no usable queries")
    if len(set(queries)) != len(queries):
        raise ContractError("generated ProVerif model has duplicate normalized queries")
    return queries


def formula_sha(text: str) -> str:
    return sha256(text.encode("utf-8"))


def parse_proverif_summary(data: bytes) -> dict[str, list[str]]:
    current = ""
    result: dict[str, list[str]] = {}
    for line in data.decode("utf-8").splitlines():
        if line.startswith("TARGET: "):
            current = line.removeprefix("TARGET: ").strip()
            result[current] = []
        elif line.startswith("RESULT ") and current:
            match = re.search(r" is (true|false)\.$", line)
            if not match:
                raise ContractError(f"unrecognized ProVerif result: {line}")
            result[current].append(match.group(1))
    return result


def parse_proverif_output(data: bytes) -> list[str]:
    statuses = []
    for line in data.decode("utf-8", "replace").splitlines():
        if line.startswith("RESULT "):
            match = re.search(r" is (true|false)\.$", line)
            if not match:
                raise ContractError(f"unrecognized ProVerif RESULT line: {line}")
            statuses.append(match.group(1))
    if not statuses:
        raise ContractError("ProVerif raw output has no RESULT lines")
    return statuses


def require_unique(rows: Sequence[Mapping[str, str]], fields: Sequence[str], label: str) -> None:
    seen: set[tuple[str, ...]] = set()
    for row in rows:
        key = tuple(row[field] for field in fields)
        if key in seen:
            raise ContractError(f"duplicate {label}: {key}")
        seen.add(key)


def validate_json_row(schema_path: Path, row: Mapping[str, str]) -> None:
    """Small in-repo validator for the schema subset used here."""
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = schema["required"]
    if set(row) != set(required):
        raise ContractError(f"row fields differ from {schema_path.name}")
    for field, rules in schema["properties"].items():
        value = row[field]
        if "const" in rules and value != rules["const"]:
            raise ContractError(f"{field} violates const")
        if "enum" in rules and value not in rules["enum"]:
            raise ContractError(f"{field} has invalid value {value!r}")
        if "pattern" in rules and not re.fullmatch(rules["pattern"], value):
            raise ContractError(f"{field} violates pattern")
        if rules.get("minLength", 0) and not value:
            raise ContractError(f"{field} must not be empty")


def terminal(status: str) -> bool:
    return status in {"verified", "falsified", "true", "false", "MATCH"}


def parse_manifest(data: bytes) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in data.decode("utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise ContractError(f"invalid SHA256SUMS line: {line!r}")
        entries.append((match.group(1), match.group(2).replace("\\", "/")))
    require_unique(
        [{"path": path} for _, path in entries], ["path"], "manifest path"
    )
    return entries


def verify_git_manifest(root: Path, commit: str, prefix: str, manifest_path: str) -> int:
    entries = parse_manifest(git_blob(root, commit, manifest_path))
    base = prefix.rstrip("/")
    paths = [f"{base}/{relative}" if base else relative for _, relative in entries]
    digests = git_blob_sha256s(root, commit, paths)
    for (expected, _), path, actual in zip(entries, paths, digests, strict=True):
        if actual != expected:
            raise ContractError(f"manifest hash mismatch: {path}")
    return len(entries)


def read_git_tsv(
    root: Path, commit: str, path: str, header: Sequence[str] | None = None
) -> list[dict[str, str]]:
    return read_tsv_bytes(git_blob(root, commit, path), header)


def ensure_new_output(root: Path, output: Path) -> Path:
    output = output.expanduser().resolve()
    root = root.resolve()
    if output.exists():
        raise ContractError(f"output already exists: {output}")
    try:
        output.relative_to(root)
    except ValueError:
        pass
    else:
        raise ContractError("output must be outside the repository")
    output.mkdir(parents=True)
    return output


def classify_tamarin(raw: str, exit_status: int) -> tuple[str, str]:
    if exit_status == 124:
        return "timeout", "timeout"
    if exit_status == 137:
        return "oom", "oom_or_sigkill"
    if "<<loop>>" in raw:
        return "loop", "loop"
    if re.search(r"\bverified\b", raw):
        return "verified", "none"
    if re.search(r"\bfalsified\b", raw):
        return "falsified", "none"
    if re.search(r"well.?formedness|parse error|guarded formula", raw, re.I):
        return "incomplete", "parse_or_wellformedness"
    return "incomplete", "unknown"


def parse_key_values(data: bytes) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in data.decode("utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if key in values:
                raise ContractError(f"duplicate key {key}")
            values[key] = value
    return values


def assert_clean_branch(root: Path, allow_dirty: bool = False) -> tuple[str, str, str]:
    branch = str(run_git(root, "branch", "--show-current"))
    head = str(run_git(root, "rev-parse", "HEAD"))
    tree = str(run_git(root, "rev-parse", "HEAD^{tree}"))
    status = str(run_git(root, "status", "--porcelain"))
    validate_repository_state(root, head, tree, status, allow_dirty)
    return branch, head, tree


def validate_repository_state(
    root: Path,
    head: str,
    tree: str,
    status: str,
    allow_dirty: bool = False,
) -> None:
    try:
        base_tree = str(run_git(root, "rev-parse", f"{BASE_COMMIT}^{{tree}}"))
    except ContractError as exc:
        raise ContractError("frozen BASE_COMMIT object is missing") from exc
    ancestor = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", BASE_COMMIT, head],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    validate_repository_facts(
        base_tree=base_tree,
        base_is_ancestor=ancestor.returncode == 0,
        status=status,
        allow_dirty=allow_dirty,
    )


def validate_repository_facts(
    *,
    base_tree: str,
    base_is_ancestor: bool,
    status: str,
    allow_dirty: bool = False,
) -> None:
    """Validate branch-independent facts collected by validate_repository_state."""
    if base_tree != BASE_TREE:
        raise ContractError(f"wrong frozen base tree: {base_tree}")
    if not base_is_ancestor:
        raise ContractError("BASE_COMMIT is not an ancestor of HEAD")
    if status and not allow_dirty:
        raise ContractError("worktree or index is dirty")


def validate_review_state(
    branch: str, head: str, parent: str, expected_head: str
) -> None:
    """Review-only helper; deliberately not part of verify-committed."""
    if branch != "codex/m5-paper-artifact":
        raise ContractError(f"wrong review branch: {branch}")
    if head != expected_head:
        raise ContractError(f"wrong review HEAD: {head}")
    if parent != BASE_COMMIT:
        raise ContractError(f"wrong review parent: {parent}")
