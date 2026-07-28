# M5 Completion Record — Reproducible paper artifact freeze

完成日期：2026-07-29

状态：✅ complete — reviewed and merged into main

## 1. 里程碑目标

M5 不新增协议性质。它冻结并机械链接：

- paper mainline artifact index；
- expected result contract；
- committed actual result table；
- raw-to-summary provenance；
- paper claim mapping；
- frozen model/evidence Git blobs；
- reproducible validation entrypoints；
- known limitations and scope declarations。

## 2. Commit 结构

Commit A（artifact contract 与 validation infrastructure）：

```text
commit: 776f757e05fd2c5e1b3d3f50ba1cef880fe21804
tree:   caa3c5558001f57995a14553a6089b19772dabbe
parent: 211ffd0a8ed8a7051d12dcc165566a66e64ab970
```

Commit B（机械生成的 evidence freeze）：

```text
commit: c7f76ac7010776b1431c751ea76dca80091c9ecd
tree:   6792909ef3822ec4e3553eb2558a4aa468874235
parent: 776f757e05fd2c5e1b3d3f50ba1cef880fe21804
```

Commit C（documentation closeout）：

```text
commit: 876bcfb8a4e4e03bf54d1b084963e9e6fb29d622
tree:   b1dcb9b3030265c4b6b455279911bbc61b60b0bd
parent: c7f76ac7010776b1431c751ea76dca80091c9ecd
```

Commit A, Commit B, and Commit C are preserved linearly in `main`.

## 3. 主要路径

```text
scripts/run-paper-artifact.sh

artifact/README.md
artifact/manifest/paper-mainline.tsv
artifact/manifest/frozen-inputs.tsv
artifact/manifest/property-semantics.tsv
artifact/manifest/artifact-inventory.tsv
artifact/manifest/git-blob-SHA256SUMS.txt
artifact/manifest/tool-versions.tsv

artifact/results/expected-results.tsv
artifact/results/actual-results.tsv
artifact/results/claim-evidence.tsv
artifact/results/claim-matrix.tsv
artifact/results/raw-to-summary.tsv

artifact/validation/summary.md
artifact/validation/summary.tsv
artifact/validation/runs/commit-b/
```

## 4. Result contract

```text
expected=405
actual=405

Tamarin=296
inherited ProVerif=89
M4 ProVerif scope=20
```

The 89 inherited ProVerif rows represent previously committed ProVerif
evidence. The 20 M4 ProVerif scope rows record
`not_run_out_of_scope`. They are not duplicate executions and must not be
combined into a claim that M4 ran 109 ProVerif properties.

## 5. M4 transparent composite

```text
canonical Tamarin matrix=296
terminal=296
MATCH=296
verified=281
falsified=15
Run 2 fallbacks=2
terminal conflicts=0
unresolved=0
mismatches=0
provenance invalid=0
```

Source Run 1 and Source Run 2 are both complete 296-target invocations with
valid manifests. Run 1 has 294 terminal rows and two OOM rows; Run 2 has 291
terminal rows and five timeout rows. Neither single source run reaches 296/296
terminal. The 296/296 result is the transparent composite using Run 1 as
primary and Run 2 only for the two legal fallback rows.

## 6. 派生视图

```text
artifact inventory=66
raw-to-summary=405
claim matrix=18
```

These views are mechanical joins/projections from frozen source tables.
`artifact/validation/runs/commit-b/generate-views.py --check` regenerates them
in a temporary directory and compares their bytes exactly.

The claim matrix preserves the distinction between verified attack witnesses
and falsified blocked-attack witnesses: the former show reachability, while the
latter show that the named attack is unreachable in the repair model.

## 7. Git-blob freeze

```text
frozen inputs=66
Commit A infrastructure=26
total=92
duplicates=0
checksum failures=0
```

Each checksum is calculated from the bytes returned for an exact
`<commit>:<path>` Git blob, not from current worktree bytes.

## 8. Actual reproducibility

The frozen actual table SHA-256 is:

```text
914acd51e1a358645dec294f8b603e789086e68fcd41738d4ac0ebf31c1cc2f1
```

Two independent committed-M4 actual generations and the committed
`artifact/results/actual-results.tsv` were byte-identical.

## 9. 验证入口

```bash
bash scripts/run-paper-artifact.sh verify-committed
bash artifact/validation/run-tests.sh
python -B artifact/validation/runs/commit-b/generate-views.py --check
python -B artifact/validation/runs/commit-b/generate-checksums.py --check
```

These commands validate the committed artifact. They are not formal prover
reruns. The formal reproduction modes are separately listed by
`bash scripts/run-paper-artifact.sh list` and require explicit external output
directories.

## 10. Wrapper cleanliness

```text
negative fixtures=37/37
wrapper cleanliness=PASS
bytecode files=0
worktree remains clean
```

The production and test wrappers set `PYTHONDONTWRITEBYTECODE=1` and invoke
Python with `-B`.

## 11. M5 没有做什么

```text
M5 did not modify any ProVerif or Tamarin model.
M5 did not change any lemma or query.
M5 did not modify historical formal logs.
M5 did not rerun ProVerif or Tamarin.
M5 did not establish a new protocol property.
M5 did not add a license or citation author record.
```

## 12. License 与 citation 状态

Repository licensing and citation-author metadata are owner-level release
decisions and are intentionally deferred beyond M5.

Their absence does not change the formal result or artifact validation status,
but they should be resolved before a public archival release.

## 13. Allowed claims

- The repository has frozen a paper-facing symbolic artifact.
- Expected, actual, property, claim, and raw provenance can be checked
  mechanically.
- The M4 Tamarin transparent composite reaches 296/296 terminal and MATCH for
  the frozen canonical matrix.
- Previously committed ProVerif evidence is explicitly separated from M4 scope
  declarations.
- Frozen inputs and Commit A infrastructure are bound to Git-blob SHA-256
  values.
- The M0-M5 symbolic model/artifact gate is complete and paper writing may
  begin after review-branch closeout.

## 14. Prohibited claims

M5 does not support statements that:

- M5 re-proved all formal properties;
- M5 reran ProVerif or Tamarin;
- M4 ran 109 ProVerif properties;
- the transparent composite is one 296/296 terminal source run;
- fixed two-slot means arbitrary-length;
- batch-local dedup means global replay prevention;
- conditional installation means deployed session cloning;
- symbolic proof means computational proof;
- the repository has been published, archived, assigned a DOI, or accepted by
  a conference;
- the repository has adopted a license.

## 15. 完成判据

| Criterion | Status |
| --- | --- |
| contract/schema freeze | PASS |
| expected result table | PASS |
| actual result table | PASS |
| raw provenance mapping | PASS |
| paper claim mapping | PASS |
| Git-blob checksum binding | PASS |
| deterministic regeneration | PASS |
| negative tamper fixtures | PASS |
| wrapper cleanliness | PASS |
| scope/limitation documentation | PASS |
| README/roadmap synchronization | PASS |

M5 is complete, reviewed, and merged into `main`. Commit A, Commit B, and
Commit C remain three distinct linear commits in `main` history.
