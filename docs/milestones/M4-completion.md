# M4 Completion Record — HMAC confirmation + batch-local atomic dedup

完成日期：2026-07-27

状态：✅ complete — Tamarin-only transparent composite evidence

## 1. 冻结版本

Commit A（最终 M4 模型、runner、Tamarin-only 证据模式基准）：

```text
commit: 96010c72e71defc775c7c2ee99c937ff700a3227
parent: d77e4ae7a1ce04f307d72debd81bcd5e020ffb0b
tree:   3ef9d77f1fbb969ba6f3cff14eae9bab229f59c8
```

Evidence Commit B（只包含 M4 Tamarin-only composite evidence）：

```text
commit: 740666a3abd6937b52818d0f4acaf8ea0d023c58
parent: 96010c72e71defc775c7c2ee99c937ff700a3227
tree:   a7e10871cbad98027494b76fa333ec15b503fd96
```

本 record 解释 Commit A 的冻结模型/runner 和 Evidence Commit B 的已提交
evidence。它不修改模型、lemma、expected vector、runner 或正式日志。

## 2. Artifact 与 evidence 路径

- `tamarin/replay/kwaay_replay_hmac_dedup.spthy`
- `tamarin/replay/README-hmac-dedup.md`
- `tamarin/impact/kwaay_impact_hmac_dedup.spthy`
- `tamarin/impact/README-hmac-dedup.md`
- `tamarin/milestones/run-m4-hmac-dedup.sh`
- `logs/tamarin-m4-hmac-dedup/`

Evidence Commit B 中的正式证据目录包含：

```text
logs/tamarin-m4-hmac-dedup/source-run1/
logs/tamarin-m4-hmac-dedup/source-run2/
logs/tamarin-m4-hmac-dedup/composite-summary.txt
logs/tamarin-m4-hmac-dedup/composite-selection.tsv
logs/tamarin-m4-hmac-dedup/composite-result-vector.tsv
logs/tamarin-m4-hmac-dedup/SHA256SUMS.txt
```

`source-run1/` 和 `source-run2/` 是两次完整、manifest-valid 的 Tamarin-only
source run。顶层 composite 采用 Run 1 primary、Run 2 fallback 的 transparent
selection policy。

## 3. M4 组合模型语义

M4 把两条已经冻结的修复主线组合到同一 fixed two-slot 模型中：

```text
HMAC confirmation:
  successful accept requires HonestSession(A,B,rst,m,sid,k)
  and exact tag hmac(confirm_key(k),sid)

batch-local atomic dedup:
  scope    = same B, bid, rst
  identity = exact complete base message m
  decision = after both slots are sealed, before any ProcessSlot
```

成功 lower-layer event 是：

```text
ConfirmedSend(A,B,m,sid,k,tag)
ConfirmedReceiverAccept(B,A,bid,idx,rst,m,sid,k,tag)
```

M4 deliberately distinguishes:

- confirmed full message `<m,tag>`;
- base message `m`;
- accept occurrence / slot occurrence;
- accepted output `aid`;
- conditional local installation handle `h`.

The replay model has no `AcceptedOutput`, `InstallFromAccept`, or
`InstallSession` layer. The impact model adds that layer only through the
bounded `C_install-v2` consumer.

## 4. Replay 与 impact 模型职责

Replay model: `tamarin/replay/kwaay_replay_hmac_dedup.spthy`

- exactly 38 uniquely named lemmas;
- owns lower-layer confirmed send/accept, HMAC validation, explicit mismatch
  paths, sealed two-slot dedup, duplicate rejection, and distinct-batch
  reachability;
- proves no duplicate confirmed accept for the same base message within the
  fixed `(B,bid,rst)` batch-local scope;
- proves duplicate same-base messages, even with different tags, do not produce
  a confirmed accept;
- keeps slot-2 mismatch after slot-1 accept reachable, so the model does not
  claim all failed batches have no partial lower-layer output.

Impact model: `tamarin/impact/kwaay_impact_hmac_dedup.spthy`

- exactly 62 uniquely named lemmas;
- includes the 38 combined lower-layer properties, 19 mechanically mapped
  composition properties, and 5 impact-only properties;
- adds `AcceptOutputCreated`, linear `AcceptedOutput`, `InstallFromAccept`,
  `InstallSession`, and `ConsumerComplete`;
- proves duplicate accepted output and duplicate installation are blocked under
  the bounded `C_install-v2` consumer;
- preserves normal distinct-message consumer reachability with two distinct
  accepted-output ids and two distinct symbolic handles.

## 5. Source Run statistics

Both source runs record:

```text
evidence_scope=tamarin-only
canonical_target_count=296
proverif_targets=not_run_out_of_scope
parse_failures=0
trace_total=5
trace_failures=0
structural_failures=0
source-run-status=VALID
```

Run 1:

```text
invoked=296
terminal=294
nonterminal=2
mismatch=2
memory_max_mb=16384
memory_swap_max=0
```

Run 2:

```text
invoked=296
terminal=291
nonterminal=5
mismatch=5
memory_max_mb=49152
memory_swap_max=0
```

No single source run is described as a 296/296 terminal run. The 296/296
terminal result is a transparent composite result.

## 6. Nonterminal rows and fallback selection

Run 1 nonterminal rows:

| suite | target | expected | event | exit |
|---|---|---:|---|---:|
| combined-impact | `confirmed_receiver_accept_has_unique_output` | verified | oom_kill | 137 |
| combined-impact | `duplicate_batch_has_no_accept_output` | verified | oom_kill | 137 |

Both Run 1 nonterminal rows are terminal verified in Run 2 and are therefore
legitimate Run 2 fallback rows in `composite-selection.tsv`.

Run 2 nonterminal rows:

| suite | target | expected | event | exit |
|---|---|---:|---|---:|
| combined-impact | `process_requires_dedup_pass` | verified | timeout | 124 |
| combined-impact | `dedup_outcomes_exclusive` | verified | timeout | 124 |
| combined-impact | `normal_distinct_batch_complete` | verified | timeout | 124 |
| combined-impact | `normal_distinct_fail_slot2_exists` | verified | timeout | 124 |
| combined-impact | `hmac_failure_slot1_exists` | verified | timeout | 124 |

All five Run 2 timeout targets have valid Run 1 terminal results, so they do not
produce unresolved composite rows.

## 7. Transparent composite result

`logs/tamarin-m4-hmac-dedup/composite-summary.txt` records:

```text
classification=transparent composite; evidence_scope=tamarin-only; canonical 296-target matrix; Run 1 primary
evidence_scope=tamarin-only
canonical_target_count=296
proverif_targets=not_run_out_of_scope
terminal_conflicts=0
unresolved=0
mismatches=0
```

`composite-result-vector.tsv` has exactly 296 result rows:

```text
terminal=296/296
MATCH=296/296
verified=281
falsified=15
```

The two `selected_run=run2` rows are:

- `combined-impact / confirmed_receiver_accept_has_unique_output`;
- `combined-impact / duplicate_batch_has_no_accept_output`.

## 8. Trace witnesses

Both source runs validate all five frozen trace witnesses:

- `duplicate`;
- `normal-replay`;
- `slot1-mismatch`;
- `slot2-mismatch`;
- `normal-consumer`.

These traces support non-vacuity and structural sanity for duplicate rejection,
normal distinct operation, explicit mismatch paths, and the conditional
consumer. They do not broaden M4 beyond the fixed two-slot, batch-local scope.

## 9. Tool and resource environment

The source-run provenance records:

```text
OS: Ubuntu 24.04.4 LTS
Tamarin Prover: 1.12.0
Maude: 3.5.1
timeout: 300 seconds per target
memory limit: systemd-run --user transient service cgroup
Run 1 MemoryMax: 16384 MB
Run 2 MemoryMax: 49152 MB
MemorySwapMax: 0
```

`proverif_executable=not_required_for_tamarin_only` and
`proverif_version=not_run_out_of_scope` are intentional for this evidence
scope.

## 10. ProVerif scope

M4 Evidence Commit B is Tamarin-only and does not rerun the five ProVerif
targets from the full 301-target runner mode. The ProVerif facts used by the
paper story remain the previously committed and reviewed original core and
HMAC confirmation artifacts:

- `logs/final/proverif/summary.txt`;
- `logs/variants/hmac-confirmation/proverif/summary.txt`.

M4 may cite those previous ProVerif results as already-existing baseline
evidence. It must not claim that Evidence Commit B reran ProVerif.

## 11. Allowed claims

Within the frozen fixed two-slot, same `B,bid,rst`, exact complete base-message
scope, M4 supports the following claims:

- HMAC-confirmed accept requires a matching `HonestSession` and exact
  confirmation tag;
- duplicate same-base messages, even with different tags, cannot produce
  confirmed accept;
- repeated confirmed accept of the same base message is blocked;
- duplicate input is rejected atomically before accepted output or installation;
- under the conditional `C_install-v2` consumer, duplicate accepted output and
  duplicate installation are blocked;
- two distinct valid confirmed messages can still complete the batch and the
  conditional consumer;
- explicit slot-1 and slot-2 HMAC mismatch paths are reachable;
- slot-2 failure can occur after slot-1 accept, so failed batches may have
  partial lower-layer output.

## 12. Prohibited claims

M4 does not establish:

- global or cross-batch replay prevention;
- rollback or restart protection;
- arbitrary-length batch theorem;
- deployed implementation proof;
- computational security;
- that every invalid tag necessarily emits `HmacValidationFailed`;
- that every `BatchFail` has no partial output;
- that `C_install-v2` is the deployed upper-layer behavior;
- that this evidence reran the five ProVerif targets;
- that either single source run individually reached 296/296 terminal.

## 13. Assumptions and limitations

- The batch model is fixed two-slot.
- Dedup identity is the exact complete public base message `m`.
- Dedup state is batch-local to the same `(B,bid,rst)`.
- `HonestSession` is the successful reconstruction/HMAC-confirmation
  abstraction.
- The impact layer is a bounded symbolic `C_install-v2` consumer.
- Material-specific compromise is not expanded in M4; this is primarily a
  no-compromise combined baseline plus state/timing boundary result.

## 14. Current unique next step

M4 is complete. The current unique next step is M5: freeze the final
reproducible artifact/result table and paper-facing artifact bundle. M5 is not
started by this record.
