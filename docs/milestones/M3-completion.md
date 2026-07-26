# M3 Completion Record — Batch-local atomic dedup

完成日期：2026-07-19

状态：✅ complete — transparent composite evidence

## 1. 冻结版本

Commit A3（固定模型、README 和 evidence runner）：

```text
commit: 282532fd922f3a7f7928f3772b3325fe06785730
tree:   077ba2fa6bb64f49edff9478a45a66f838ea62e8
```

Commit B（只包含 M3 closeout evidence）：

```text
commit: b0ff0b23977614deea8375cb95c0909be71e5c71
tree:   9bfcf4c342b17a769816402ff47a1989be70c2e2
parent: 282532fd922f3a7f7928f3772b3325fe06785730
```

冻结 artifact provenance：

```text
fixed replay model blob:
493568857492e9c17b896dfb2ab3692f7b48d365

fixed replay model SHA-256:
ae040141a099953dc237bb44ee0f88d55b5ea396cc2019475a5fb3a72eaf36ec

fixed impact model blob:
3a707c022594ce84f23c2f39623715fe3c3f47e2

fixed impact model SHA-256:
0c46643fb278598d45b91dc2ce4a963ab1a7f3336581a5afe599cc888b9bd808

runner blob:
1b2bcd06448b832663b4534dcfc5074ac3c9e683

runner SHA-256:
410ec3a46e0829238b00ee1972580aa3631d94394fa92f83a20562d923b1216c

tool binding:
Tamarin Prover 1.12.0
Maude 3.5.1
ProVerif 2.05
```

本 record 只解释 A3 的冻结模型和 Commit B 的已提交证据，不改变模型、
lemma、expected vector 或 runner。

## 2. Artifact 与 evidence 路径

- `tamarin/replay/kwaay_replay_fixed.spthy`
- `tamarin/replay/README-fixed.md`
- `tamarin/impact/kwaay_impact_fixed.spthy`
- `tamarin/impact/README-fixed.md`
- `tamarin/milestones/run-m3-dedup.sh`
- `logs/tamarin-m3-closeout/`

`logs/tamarin-m3-closeout/source-run1/` 和 `source-run2/` 是两次完整运行的
原始 evidence 副本；各自的嵌套 manifest 与外层 `SHA256SUMS.txt` 均已机械
验证。`composite-selection.tsv` 记录每个目标的两次状态、选择来源和理由，
`composite-result-vector.tsv` 是机械生成的 196 项最终向量。

## 3. 修复语义

```text
batch bound:     fixed two-slot
dedup scope:     same B, bid, rst
dedup identity:  exact complete public message m
decision point:  both slots collected and sealed, before any ProcessSlot
```

`SealBatch` 产生线性的 `DedupPending` 和 `DedupDecisionToken`，而不直接开放
处理状态。duplicate 分支消费该决定状态并产生 `DuplicateDetected`、
`BatchFail`、`BatchClosed` 和 `ConsumeReceiverState`；它不产生
`ReceiverAccept`、`AcceptedOutput`、`ConsumerStarted` 或 `InstallSession`。

distinct 分支产生 `DedupPassed`、`CheckedSlot1/2`，之后两个不同消息仍可依次
处理并到达 `BatchComplete`；在 fixed impact 中，`C_install-v2` consumer 仍可
安装两个 distinct outputs 并到达 `ConsumerComplete`。原抽象 distinct-message
`FailSlot1/2` 路径仍可达，因此“无 partial output”只适用于
`DuplicateDetected` 分支，而不是所有 `BatchFail`。

## 4. Fixed replay 实际结果

| Lemma | Actual result |
|---|---|
| `one_send_two_accepts_exists` | falsified |
| `same_message_accepted_at_most_once` | verified |
| `injective_receiver_accept` | verified |
| `duplicate_batch_fail_exists` | verified |
| `duplicate_batch_has_no_accept` | verified |
| `normal_distinct_batch_complete` | verified |
| `normal_distinct_fail_slot1_exists` | verified |
| `normal_distinct_fail_slot2_exists` | verified |

Fixed replay 的 30/30 目标均有预期终态。

## 5. Fixed impact 实际结果

| Lemma | Actual result |
|---|---|
| `one_send_two_accepts_two_installs_exists` | falsified |
| `unique_install_within_completed_consumer` | verified |
| `normal_consumer_complete` | falsified |
| `normal_distinct_consumer_complete` | verified |
| `duplicate_batch_has_no_accept_output` | verified |
| `duplicate_batch_has_no_install` | verified |
| `no_consumer_after_failed_batch` | verified |

`normal_consumer_complete` 是冻结的 legacy same-message two-output
exists-trace；fixed impact 中的预期 `falsified` 不表示正常 consumer 不可执行。
distinct-message consumer 的非空性由 `normal_distinct_consumer_complete`
verified 建立。Fixed impact 的 53/53 目标均有预期终态。

## 6. 两次完整运行与 composite 选择

Run 1：196/196 invoked，195 terminal；唯一 missing 是 fixed-impact
`install_has_prior_accept`，其 source saturation 输出 `tamarin-prover:
<<loop>>`。其余 195 个目标均符合 expected vector，V6
`executable_seal_batch` verified，manifest valid，runner exit 1。

Run 2：196/196 invoked，195 terminal；`install_has_prior_accept` verified（18
steps），唯一 missing 是 V6 `executable_seal_batch`，其 source saturation
输出 `tamarin-prover: <<loop>>`。其余 195 个目标均符合 expected vector，
fixed replay 30/30、fixed impact 53/53 terminal，manifest valid，runner exit 1。

Composite 对每个目标优先使用 Run 2；只有 Run 2 nonterminal 且 Run 1 具有相同
冻结 expected 的合法终态时才选择 Run 1。因此唯一 Run 1 fallback 是
`v6/executable_seal_batch`。结果为：

```text
targets:             196
selected terminal:   196
vector mismatches:   0
terminal conflicts:  0
unresolved:          0
```

证据分类为：**transparent composite evidence assembled from two complete,
manifest-validated runs over the same committed models, inputs, tool versions,
HEAD and tree.** 没有一次单独 runner invocation 达到 196/196 terminal；loop
本身没有被解释为 verified，也没有修改模型、lemma 或 expected vector 来选择
有利结果。

两次不同目标上的 source-saturation `<<loop>>` 是当前工具链上的偶发现象；它
不是反例，也不构成关于 Tamarin 的一般性 bug 声明。

## 7. 结构、回归与 trace

```text
frozen formulas:                  55/55 MATCH
replay/impact constructors:       MATCH
consumer rules:                   3/3 MATCH
original replay vector:           MATCH
HMAC-only replay vector:          MATCH
original M2 impact vector:        MATCH
V6 composite vector:              MATCH
V7 vector:                        MATCH
ProVerif four targets:             MATCH
traces:                            5/5 valid
```

五组 trace 为 `duplicate-fail`、`distinct-complete`、
`distinct-fail-slot1`、`distinct-fail-slot2` 和 `distinct-consumer`，每组均保留
text/JSON/DOT artifacts。

## 8. Assumptions 和 limitations

- batch-local，不是跨 batch 的全局 replay cache；
- 不证明 rollback、restart 或 receiver-state 恢复后的 replay protection；
- fixed two-slot，不是 arbitrary-length batch theorem；
- dedup identity 是 exact complete message `m`；
- 不包含 HMAC confirmation，也不恢复 original ProVerif P1；
- `C_install-v2` 仍是条件化上层 consumer abstraction；
- 不证明真实部署实现、真实 session database 或 Double Ratchet 行为；
- 不证明 authentication-key/KEM-material compromise 条件下的性质；
- 不证明 computational security。

## 9. Allowed claim

> 在 fixed two-slot 模型中，处理前的 batch-local atomic duplicate rejection
> 阻止同一完整消息在同一 `B,bid,rst` 中产生两个 `ReceiverAccept`；在显式
> `C_install-v2` 条件下，也阻止相应的 duplicate accepted outputs 和
> duplicate installations。

## 10. Prohibited claims

不得把 M3 表述为：

- global replay prevention；
- cross-batch replay protection；
- rollback/restart protection；
- implementation proof；
- HMAC authentication repair；
- real session cloning prevention theorem；
- arbitrary-length 或 computational-security theorem。

## 11. 唯一后继任务

M3 已完成。M4 后续也已完成，见
`docs/milestones/M4-completion.md`。当前唯一下一步是 M5：冻结最终可复现
artifact/result table。不能把 M4 的 Tamarin-only evidence 写成 full 301-target
run，也不能声称本轮重新运行了 ProVerif 5 targets。
