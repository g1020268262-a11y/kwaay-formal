#!/usr/bin/env python3
"""Safe isolated target execution for the paper artifact."""

from __future__ import annotations

import argparse
import datetime as dt
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from contract import (
    BASE_COMMIT,
    M2_BASELINE,
    M3_BASELINE,
    M4_BASELINE,
    ContractError,
    classify_tamarin,
    ensure_new_output,
    git_blob,
    parse_proverif_output,
    repo_root,
    run_git,
    terminal,
    write_tsv,
)
from source_runs import (
    AGGREGATE_HEADER,
    TARGET_HEADER,
    assemble_runs,
    contract_bindings,
    expected_rows,
    mode_rows,
    model_commit_for_expected,
    target_matrix,
    validate_source_run,
    write_manifest,
    write_provenance,
)


def baseline_for(row: dict[str, str]) -> str:
    return model_commit_for_expected(row)


def version_lines() -> list[str]:
    commands = [
        ["tamarin-prover", "--version"], ["maude", "--version"],
        ["proverif", "--version"], ["bash", "--version"], ["git", "--version"],
        [sys.executable, "--version"], ["systemd-run", "--version"],
    ]
    lines = []
    for command in commands:
        try:
            proc = subprocess.run(command, capture_output=True, text=True, timeout=10)
            text = (proc.stdout or proc.stderr).splitlines()
            observed = text[0] if text else f"exit={proc.returncode}"
        except (OSError, subprocess.TimeoutExpired) as exc:
            observed = f"unavailable:{type(exc).__name__}"
        lines.append(f"{command[0]}\t{observed}")
    return lines


def _run_command(command: list[str], timeout: int) -> tuple[int, bytes]:
    try:
        proc = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout, check=False,
        )
        return proc.returncode, proc.stdout
    except subprocess.TimeoutExpired as exc:
        return 124, (exc.stdout or b"") + b"\nM5 wrapper timeout\n"
    except OSError as exc:
        return 127, f"tool launch failed: {exc}\n".encode()


def execute(mode: str, output: Path) -> int:
    root = repo_root()
    if str(run_git(root, "status", "--porcelain")):
        raise ContractError("formal run requires a clean worktree and index")
    output = ensure_new_output(root, output)
    selected = mode_rows(expected_rows(root), mode)
    matrix = target_matrix(root, selected)
    write_tsv(output / "target-matrix.tsv", TARGET_HEADER, matrix)
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    head = str(run_git(root, "rev-parse", "HEAD"))
    tree = str(run_git(root, "rev-parse", "HEAD^{tree}"))
    (output / "versions.tsv").write_text(
        "tool\tobserved\n" + "\n".join(version_lines()) + "\n",
        encoding="utf-8", newline="\n",
    )
    commands: list[str] = []
    aggregate: list[dict[str, str]] = []
    order = {row["property_id"]: index for index, row in enumerate(matrix)}
    pv_groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in matrix:
        if row["tool"] == "proverif":
            pv_groups.setdefault((row["suite"], row["target_id"]), []).append(row)
            continue
        contract = next(item for item in selected if item["property_id"] == row["property_id"])
        commit = baseline_for(contract)
        input_path = output / "inputs" / commit / row["model_path"]
        input_path.parent.mkdir(parents=True, exist_ok=True)
        input_path.write_bytes(git_blob(root, commit, row["model_path"]))
        raw_rel = f"raw/{row['suite']}/{row['property_id']}.out"
        raw = output / raw_rel
        raw.parent.mkdir(parents=True, exist_ok=True)
        if shutil.which("systemd-run") is None:
            command = ["tamarin-prover", str(input_path), f"--prove={row['query_or_lemma']}"]
            exit_status, raw_bytes = 127, b"systemd-run unavailable; Tamarin not started\n"
        else:
            command = [
                "systemd-run", "--user", "--scope", "--wait", "--collect", "--pipe",
                "--quiet", "-p", "MemoryMax=48G", "-p", "MemorySwapMax=0",
                "tamarin-prover", str(input_path), f"--prove={row['query_or_lemma']}",
                "+RTS", "-M48G", "-RTS",
            ]
            exit_status, raw_bytes = _run_command(command, int(contract["timeout_seconds"]))
        raw.write_bytes(raw_bytes)
        actual, event = classify_tamarin(raw_bytes.decode("utf-8", "replace"), exit_status)
        commands.append(
            f"{row['property_id']}\t{commit}\t{subprocess.list2cmdline(command)}"
        )
        aggregate.append({
            "property_id": row["property_id"], "tool": row["tool"],
            "suite": row["suite"], "target_id": row["target_id"],
            "query_index": row["query_index"], "actual_status": actual,
            "expected_status": row["expected_status"],
            "exit_status": str(exit_status), "resource_event": event,
            "raw_output": raw_rel,
        })
    for (suite, target), group in pv_groups.items():
        contract = next(
            item for item in selected
            if item["suite"] == suite and item["target_id"] == target
        )
        commit = baseline_for(contract)
        input_path = output / "inputs" / commit / contract["model_path"]
        input_path.parent.mkdir(parents=True, exist_ok=True)
        input_path.write_bytes(git_blob(root, commit, contract["model_path"]))
        raw_rel = f"raw/{suite}/{target}__queries.out"
        raw = output / raw_rel
        raw.parent.mkdir(parents=True, exist_ok=True)
        command = ["proverif", str(input_path)]
        exit_status, raw_bytes = _run_command(command, int(contract["timeout_seconds"]))
        raw.write_bytes(raw_bytes)
        statuses = []
        if exit_status == 0:
            try:
                statuses = parse_proverif_output(raw_bytes)
            except ContractError:
                statuses = []
        commands.append(
            f"{suite}:{target}\t{commit}\t{subprocess.list2cmdline(command)}"
        )
        for row in group:
            index = int(row["query_index"])
            if exit_status == 124:
                actual, event = "timeout", "timeout"
            elif exit_status == 137:
                actual, event = "oom", "oom_or_sigkill"
            elif exit_status != 0 or index > len(statuses):
                actual, event = "incomplete", "tool_or_parse_failure"
            else:
                actual, event = statuses[index - 1], "none"
            aggregate.append({
                "property_id": row["property_id"], "tool": row["tool"],
                "suite": row["suite"], "target_id": row["target_id"],
                "query_index": row["query_index"], "actual_status": actual,
                "expected_status": row["expected_status"],
                "exit_status": str(exit_status), "resource_event": event,
                "raw_output": raw_rel,
            })
    aggregate.sort(key=lambda row: order[row["property_id"]])
    write_tsv(output / "aggregate.tsv", AGGREGATE_HEADER, aggregate)
    (output / "commands.tsv").write_text(
        "property_id_or_target\tsource_commit\tcommand\n"
        + "\n".join(commands) + "\n",
        encoding="utf-8", newline="\n",
    )
    valid = all(
        terminal(row["actual_status"])
        and row["actual_status"] == row["expected_status"]
        and row["exit_status"] == "0"
        for row in aggregate
    )
    (output / "run-status.txt").write_text(
        "VALID\n" if valid else "INVALID\n", encoding="utf-8", newline="\n"
    )
    write_provenance(output / "provenance.txt", {
        "mode": mode, "run_id": output.name, "source_head": head,
        "source_tree": tree, "target_count": str(len(matrix)),
        "start_utc": start, "end_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "tool_versions_file": "versions.tsv",
        "resource_policy": "systemd-run cgroup-v2 MemoryMax=48G MemorySwapMax=0",
        **contract_bindings(root),
    })
    write_manifest(output)
    validate_source_run(root, output, mode, allow_invalid=not valid)
    return 0 if valid else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for mode in ("smoke", "paper-core", "m4-tamarin", "full"):
        item = sub.add_parser(mode)
        item.add_argument("--output", required=True, type=Path)
    item = sub.add_parser("assemble-only")
    item.add_argument("--mode", required=True, choices=["smoke", "paper-core", "m4-tamarin", "full"])
    item.add_argument("--run1", required=True, type=Path)
    item.add_argument("--run2", required=True, type=Path)
    item.add_argument("--output", required=True, type=Path)
    item.add_argument("--policy", choices=["run1-primary", "run2-primary"], default="run1-primary")
    args = parser.parse_args()
    if args.command == "assemble-only":
        assemble_runs(
            repo_root(), args.run1.resolve(), args.run2.resolve(),
            args.output, args.mode, policy=args.policy,
        )
        return 0
    return execute(args.command, args.output)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
