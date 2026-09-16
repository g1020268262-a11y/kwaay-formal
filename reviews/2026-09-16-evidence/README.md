# Independent reviewer verification — 2026-09-16

This is new reviewer-generated evidence, not a reconstruction or replacement of the original RQ-v2 execution record.

- Reviewed commit: `3ebf8855f6226d7ebef8a78f2a7fae4a27679d57` (`main`).
- The worktree was clean before and immediately after the prover executions.
- Tamarin 1.12.0, Maude 3.5.1, WSL Ubuntu-24.04.
- Three unchanged models were parsed and proved. All seven invocations, including version detection, exited 0.
- All 14 model–lemma outcomes and all 14 step counts match the manuscript and existing execution report: 13 verified, 1 falsified with a trace.
- All three prove transcripts report successful wellformedness checks.
- JSON files contain seven exported witness/counterexample graphs. They can include unrelated Send events; they are not minimal protocol traces.
- Both rejection graphs leave the rejected entry values independent of the preceding honest Send tuple(s), consistent with the weakness of those formulas.

The runner, exact invocations, timestamps, input hashes, exit codes, stdout/stderr hashes, and clean pre/post statuses are retained in `independent-rerun-manifest.json`. These files were generated in a separate Codex review workspace and copied byte-for-byte here. The manifest retains the original absolute trace-export locations; corresponding exported files are included in this directory. `SHA256SUMS.txt` covers the copied evidence files. No historical proof logs or model files were overwritten.

`kwaay-full-2024-120.pdf` is the official full paper downloaded from https://eprint.iacr.org/2024/120.pdf on 2026-09-16, by Daniel Collins, Loïs Huguenin-Dumittan, Ngoc Khanh Nguyen, Nicolas Rolin, and Serge Vaudenay. The ePrint record identifies its license as CC BY. The PDF has 62 pages, with cover date January 27, 2024. Its SHA-256 is `476f28594806f15f4baab6ce7d3785143db0a013f21fbcf590ac1666161660a8`. The ePrint record reports a revision on January 29, 2024. These dates are recorded separately rather than assumed to be the same version identifier.

The accompanying review distinguishes reproducibility of these abstract results from their connection to concrete K-Waay executions and from publication-level novelty. Reproduction does not authenticate the historical run or establish a protocol attack.
