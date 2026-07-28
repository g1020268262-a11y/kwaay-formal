#!/usr/bin/env python3
"""Generate and verify the Commit B Git-blob SHA-256 manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
COMMIT_A = "776f757e05fd2c5e1b3d3f50ba1cef880fe21804"
FROZEN_PATH = ROOT / "artifact/manifest/frozen-inputs.tsv"
OUTPUT_PATH = ROOT / "artifact/manifest/git-blob-SHA256SUMS.txt"


def git(*args: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    return proc.stdout


def frozen_rows() -> list[dict[str, str]]:
    with FROZEN_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def infrastructure_paths() -> list[str]:
    names = git(
        "ls-tree",
        "-r",
        "--name-only",
        COMMIT_A,
        "--",
        ".gitattributes",
        "artifact",
        "scripts/run-paper-artifact.sh",
        "scripts/artifact",
    ).decode("utf-8").splitlines()
    return sorted(set(names))


def manifest_bytes() -> tuple[bytes, int, int]:
    references: dict[str, str] = {}
    frozen_count = 0
    for row in frozen_rows():
        reference = f"{row['source_commit']}:{row['path']}"
        blob_oid = git("rev-parse", reference).decode("ascii").strip()
        if blob_oid != row["git_blob"]:
            raise ValueError(f"frozen Git blob mismatch: {reference}")
        digest = hashlib.sha256(git("cat-file", "blob", reference)).hexdigest()
        if digest != row["blob_sha256"]:
            raise ValueError(f"frozen SHA-256 mismatch: {reference}")
        if reference in references:
            raise ValueError(f"duplicate checksum reference: {reference}")
        references[reference] = digest
        frozen_count += 1

    infrastructure = infrastructure_paths()
    for path in infrastructure:
        reference = f"{COMMIT_A}:{path}"
        if reference in references:
            raise ValueError(f"duplicate checksum reference: {reference}")
        references[reference] = hashlib.sha256(
            git("cat-file", "blob", reference)
        ).hexdigest()

    lines = [
        f"{references[reference]}  {reference}\n"
        for reference in sorted(references)
    ]
    return "".join(lines).encode("utf-8"), frozen_count, len(infrastructure)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="regenerate in a temporary directory and compare exact bytes",
    )
    args = parser.parse_args()
    content, frozen_count, infrastructure_count = manifest_bytes()
    if args.check:
        with tempfile.TemporaryDirectory(prefix="kwaay-m5-commit-b-checksums-") as tmp:
            candidate = Path(tmp) / OUTPUT_PATH.name
            candidate.write_bytes(content)
            if not OUTPUT_PATH.exists() or OUTPUT_PATH.read_bytes() != candidate.read_bytes():
                raise ValueError("Git-blob SHA-256 manifest is stale")
    else:
        OUTPUT_PATH.write_bytes(content)
    print(f"frozen_checksum_entries={frozen_count} failures=0")
    print(
        f"commit_a_infrastructure_checksum_entries={infrastructure_count} failures=0"
    )
    print(
        f"git_blob_checksum_entries={frozen_count + infrastructure_count} "
        "duplicates=0 match=100%"
    )
    print(f"checksum_stale_check={'PASS' if args.check else 'NOT_RUN'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
