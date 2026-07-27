#!/usr/bin/env python3
"""Exercise the permanent verifier in real branch/detached descendant checkouts."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def run(cwd: Path, *command: str, expect: int = 0) -> subprocess.CompletedProcess[bytes]:
    proc = subprocess.run(
        list(command),
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if proc.returncode != expect:
        raise RuntimeError(
            f"{' '.join(command)} returned {proc.returncode}, expected {expect}:\n"
            f"{proc.stdout.decode('utf-8', 'replace')}"
        )
    return proc


def verify(repo: Path, python: str, *, accepted: bool) -> None:
    proc = subprocess.run(
        [python, "-B", "scripts/artifact/verify_contract.py"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if accepted and proc.returncode != 0:
        raise RuntimeError(proc.stdout.decode("utf-8", "replace"))
    if not accepted and proc.returncode == 0:
        raise RuntimeError("dirty checkout was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--python", default="python")
    args = parser.parse_args()
    source = args.source.resolve()
    with tempfile.TemporaryDirectory(prefix="kwaay-portable-checkouts-") as temporary:
        repo = Path(temporary) / "repo"
        run(Path(temporary), "git", "clone", "--quiet", "--no-checkout", str(source), str(repo))
        run(repo, "git", "config", "user.name", "M5 synthetic validation")
        run(repo, "git", "config", "user.email", "m5-validation@example.invalid")

        run(repo, "git", "checkout", "--quiet", "-B", "codex/m5-paper-artifact", args.commit)
        verify(repo, args.python, accepted=True)
        print("portable_checkout[commit-a-branch]=PASS")

        run(repo, "git", "checkout", "--quiet", "-B", "main-like", args.commit)
        verify(repo, args.python, accepted=True)
        print("portable_checkout[main-like-branch]=PASS")

        run(repo, "git", "checkout", "--quiet", "--detach", args.commit)
        verify(repo, args.python, accepted=True)
        print("portable_checkout[detached]=PASS")

        run(repo, "git", "checkout", "--quiet", "-b", "synthetic-descendant")
        run(repo, "git", "commit", "--quiet", "--allow-empty", "-m", "synthetic descendant")
        verify(repo, args.python, accepted=True)
        print("portable_checkout[descendant]=PASS")

        dirty = repo / "artifact" / "validation" / "synthetic-dirty.tmp"
        dirty.write_text("temporary validation fixture\n", encoding="utf-8")
        verify(repo, args.python, accepted=False)
        print("portable_checkout[dirty-rejected]=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
