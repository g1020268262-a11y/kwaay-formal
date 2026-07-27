#!/usr/bin/env python3
"""Validate LF attributes and immutable log bytes in a fresh local clone."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

BASE = "211ffd0a8ed8a7051d12dcc165566a66e64ab970"


def git(cwd: Path, *args: str, input_text: str | None = None) -> str:
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        input=None if input_text is None else input_text.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    return proc.stdout.decode("utf-8").rstrip("\r\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    with tempfile.TemporaryDirectory(prefix="kwaay-m5-fresh-") as temporary:
        clone = Path(temporary) / "repo"
        subprocess.run(
            ["git", "clone", "--quiet", "--no-checkout", str(source), str(clone)],
            check=True,
        )
        git(clone, "config", "core.autocrlf", "true")
        git(clone, "checkout", "--quiet", "--detach", args.commit)
        git(clone, "diff", "--quiet", BASE, args.commit, "--", "logs")
        paths = git(clone, "ls-files", "--", "logs").splitlines()
        index_rows = git(
            clone, "ls-files", "--format=%(objectname)%x09%(path)", "--", "logs"
        ).splitlines()
        index = {
            path: oid
            for oid, path in (line.split("\t", 1) for line in index_rows)
        }
        worktree_oids = git(
            clone, "hash-object", "--no-filters", "--stdin-paths",
            input_text="".join(path + "\n" for path in paths),
        ).splitlines()
        missing_index_paths = [path for path in paths if path not in index]
        if missing_index_paths:
            raise RuntimeError(
                f"fresh-checkout index map is incomplete: "
                f"missing={missing_index_paths[:3]!r} sample={index_rows[:1]!r}"
            )
        mismatches = [
            path for path, oid in zip(paths, worktree_oids, strict=True)
            if index[path] != oid
        ]
        if mismatches:
            raise RuntimeError(
                f"fresh-checkout log bytes differ from Git blobs: {mismatches[:3]}"
            )
        eol = git(
            clone, "ls-files", "--eol", "--", "*.sh", "artifact/**/*.tsv",
            "artifact/**/*.json", "artifact/**/*.md",
        ).splitlines()
        bad_eol = [
            line for line in eol
            if not line.startswith("i/lf    w/lf")
        ]
        if bad_eol:
            raise RuntimeError(f"fresh-checkout LF policy failed: {bad_eol[:3]}")
        log_attrs = git(
            clone, "check-attr", "--stdin", "text",
            input_text="".join(path + "\n" for path in paths),
        ).splitlines()
        if any(not line.endswith(": unset") for line in log_attrs):
            raise RuntimeError("logs/** is not consistently -text")
        print(f"fresh_checkout_commit={args.commit}")
        print(f"log_blob_bytes_match={len(paths)}/{len(paths)}")
        print(f"lf_policy_paths={len(eol)}/{len(eol)}")
        print("fresh_checkout=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
