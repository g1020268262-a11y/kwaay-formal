# K-Waay 原始 M0--M5 研究路线恢复

## 1. 文件定位

本文恢复仓库中已经完成并冻结的 M0--M5 研究路线，不提出新的研究项目，
不改变任何模型、lemma、trace 或结果。证据解释以
`docs/claim-hierarchy.md`、`docs/model-mapping.md`、M1--M5 completion
record、`artifact/results/claim-matrix.tsv` 和原始日志为准。

当前 Stage 6 稿件只写入了 RQ-v2 的 R/M/P 两槽准入比较。它没有覆盖完整的
ProVerif 认证分析、HMAC confirmation、历史 replay/impact 模型、M3 修复和 M4
组合验证。因此，“恢复原始路线”应理解为恢复这些已完成贡献在后续论文中的
主线地位，而不是把它们重新列为待验证事项。

## 2. 恢复后的中心研究问题

原始路线研究的是一组相互区分但可组合的安全问题：

> 在 K-Waay Figure 7 core 的符号抽象中，密钥机密性、分量来源、完整参数对应
> 关系和批内发送--接受发生单射性分别成立到什么程度；显式 HMAC key
> confirmation 能修复哪一层性质、不能修复哪一层性质；当相同有效消息能够在
> 同一 `BatchReceive` 批次中重复进入处理时，重复接受是否可达、在明确的上层
> 消费假设下会产生什么条件化影响；处理前的批内原子去重能否阻断该路径，并与
> HMAC confirmation 组合而不破坏正常执行？

这不是一条“P0 到 P3 越来越强”的线性安全等级。冻结的性质结构为：

```text
P0-S  symbolic session-key secrecy                 独立性质
P0-O  split-KEM component origin                   独立性质
P1    full-parameter non-injective correspondence  artifact/event scoped
P2    matching existence/order + occurrence
      injectivity                                  artifact/event scoped
P3    unique installation under C_install-v2       条件化组合性质
```

只有在同一 artifact、同一事件语义和同一参数元组中才允许写 `P2 => P1`。
ProVerif 的 `SendDone/RecvDone`、Tamarin replay 的
`SenderSession/ReceiverAccept` 和 impact 模型的 `InstallSession` 不是可以直接
互换的事件。

## 3. 已完成的研究路径

### 3.1 M0：冻结性质、映射和主张边界

M0 已完成性质命名、证据角色和禁止推断的冻结。它把 K-Waay 分析拆成三个层次：

1. ProVerif 分析 Figure 7 core 的 symbolic secrecy、component origin 和
   full-parameter correspondence；
2. Tamarin 分析 receiver state、slot、batch lifecycle 和同批 occurrence
   injectivity；
3. 独立 impact theory 在显式 `C_install-v2` 下分析接受输出的条件化消费。

`full_message_unique_send` 只用于把完整发送元组消歧为一个 sender
occurrence；`normal_single_accept` 只证明正常匹配路径非空。二者均不等于
injectivity 或 replay prevention。

### 3.2 原始 Figure 7 core：机密性成立，但完整参数对应关系失败

模型：`proverif/kwaay_core_final.cpp.pv`。

`BASELINE` 的实际结果为：

- sender-side symbolic key secrecy：`true`；
- receiver-side symbolic key secrecy：`true`；
- `RecvDone(B,A,sid,k) ==> SendDone(A,B,sid,k)`：`false`；
- 两项 prekey correspondence：`true`；
- `HonestRun` 可达。

`COMPONENT` 中
`SplitKemAccepted(B,A,cts,Ks) ==> SenderSplitKemComponent(A,B,cts,Ks)` 为
`true`。因此，分量来源和密钥机密性不能替代完整消息的精确对应关系。

`logs/final/proverif/out/BASELINE.out` 中的反例是一个符号转录本重组：网络攻击者
复用诚实发送产生的 split-KEM 认证分量 `ct_s`，并用接收方公开材料构造新的
`ct_l`、`ct_k` 分量，形成一个不存在完整匹配 `SendDone` 的消息元组；接收方仍
可以触发相应 `RecvDone`。这证明的是 full-parameter non-injective
correspondence 失败，不是会话密钥被攻击者恢复。

### 3.3 HMAC confirmation：修复 P1，但不提供批内重放防护

ProVerif 模型：
`proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv`。

在 `HMAC_BASELINE` 无泄露目标中：

- `RecvDone ==> SendDone` 从原始 core 的 `false` 变为 `true`；
- sender/receiver symbolic secrecy 仍为 `true`；
- component-origin query 仍为 `true`；
- `HonestRun` 可达。

HMAC tag 为 `hmac(confirm_key(k),sid)`，它恢复的是当前 no-compromise
ProVerif 事件元组上的非单射对应关系。`HMAC_LEAK_SIGSK_A` 中同一对应关系为
`false`，所以仓库没有“所有 compromise 情形下均恢复”的结论。

M1 随后用 `tamarin/replay/kwaay_replay_hmac_only.spthy` 检查 HMAC-confirmed
消息的 replay/occurrence 行为。实际结果包括：

| 性质 | 结果 |
| --- | --- |
| `confirmed_receiver_accept_has_sender` | verified，16 steps |
| `confirmed_message_unique_send` | verified，2 steps |
| `normal_confirmed_single_accept` | verified，12 steps |
| `normal_confirmed_batch_complete` | verified，18 steps |
| `one_confirmed_send_two_accepts_exists` | verified，17 steps |
| `confirmed_message_accepted_at_most_once` | falsified，15 steps |
| `injective_confirmed_receiver_accept` | falsified，15 steps |

冻结 trace 位于
`logs/tamarin-replay-hmac-only/attack-trace.{out,json,dot}`。它包含一个匹配
`ConfirmedSend` 和同一 `B,bid,rst` 下两个不同 slot/timepoint 的
`ConfirmedReceiverAccept`；二者携带相同 `(A,B,m,sid,k,tag)`，均通过相同
symbolic HMAC gate，且没有 sender/receiver state compromise。由此得到关键分层：

```text
HMAC confirmation 修复 P1；
HMAC confirmation 不等于 freshness、dedup 或 P2 occurrence injectivity。
```

### 3.4 原始 BatchReceive 重复接受

模型：`tamarin/replay/kwaay_replay_original.spthy`。

冻结结果由 M3/M4 回归向量继续保存：

| 性质 | 结果 | 证据 |
| --- | --- | --- |
| `normal_single_accept` | verified，11 steps | `logs/tamarin-m3-closeout/source-run2/aggregate-original-replay.tsv` |
| `one_send_two_accepts_exists` | verified，15 steps | 同上及逐 lemma proof |
| `same_message_accepted_at_most_once` | falsified，13 steps | 同上 |
| `receiver_accept_has_sender` | verified | M4 composite result vector |
| `full_message_unique_send` | verified | M4 composite result vector |
| `injective_receiver_accept` | falsified，16 steps | M3 aggregate / M4 composite |

该 witness 的精确含义是：同一完整消息 `m` 被放入同一 `B,bid,rst` 的两个不同
slot，一个经完整元组消歧的 matching sender occurrence 对应两个不同的
`ReceiverAccept` occurrence，batch 仍可正常完成。它不是 forgery、key-recovery、
cross-batch replay、rollback 或 close 后重用。

这个批内重复输入不满足 K-Waay 已声明的 distinct-party input discipline。
因此它支持的是“当准入/集成边界未维持该条件时，重复接受可达”，不能写成
“满足原始前置条件的 K-Waay 执行存在该攻击”。

### 3.5 M2：`C_install-v2` 下的条件化影响

模型：`tamarin/impact/kwaay_impact_original.spthy`。

`C_install-v2` 建模一个固定两输出 consumer：成功 `BatchComplete` 后，每个
accepted-output token 被独立消费，不按 `sid`、message、peer 或 key 合并或去重，
每次安装创建 fresh local handle。C7 是显式组合假设，仓库没有把它证明为真实
K-Waay 部署行为。

核心结果：

| 性质 | 结果 |
| --- | --- |
| `one_send_two_accepts_two_installs_exists` | verified，28 steps |
| `unique_install_within_completed_consumer` | falsified，28 steps |
| `normal_one_accept_one_install` | verified，22 steps |
| `normal_consumer_complete` | verified，25 steps |

19 条 composition lemma 为 18 verified / 1 falsified；包含冻结 lower layer 的
完整 theory 为 37 条终态，34 verified / 3 falsified。正、负 trace 分别位于：

- `logs/tamarin-impact-original/attack-trace.{out,json,dot}`；
- `logs/tamarin-impact-original/unique-install-trace.{out,json,dot}`。

在该条件化 consumer 中，一个 matching sender occurrence 导致两个 accept、两个
fresh `aid`，继而产生具有相同 `A,B,sid,k`、不同 fresh handle 的两个
`InstallSession`。该结果是 conditional duplicate installation，不是真实会话克隆、
Double Ratchet duplication 或部署漏洞。

### 3.6 M3：批内原子去重修复

模型：

- `tamarin/replay/kwaay_replay_fixed.spthy`；
- `tamarin/impact/kwaay_impact_fixed.spthy`。

修复在固定两槽、同一 `B,bid,rst` 内，以 exact complete public message `m` 为
identity，在两个槽收集并 seal 后、任何 `ProcessSlot` 之前作一次线性原子决定。
重复分支关闭整个 batch，不产生 accept、accepted output 或 install；不同消息分支
继续正常处理。

关键结果：

| 层次 | 性质 | 结果 |
| --- | --- | --- |
| fixed replay | `one_send_two_accepts_exists` | falsified |
| fixed replay | `same_message_accepted_at_most_once` | verified |
| fixed replay | `injective_receiver_accept` | verified |
| fixed replay | `duplicate_batch_fail_exists` | verified |
| fixed replay | `duplicate_batch_has_no_accept` | verified |
| fixed replay | `normal_distinct_batch_complete` | verified |
| fixed impact | `one_send_two_accepts_two_installs_exists` | falsified |
| fixed impact | `unique_install_within_completed_consumer` | verified |
| fixed impact | `duplicate_batch_has_no_accept_output` | verified |
| fixed impact | `duplicate_batch_has_no_install` | verified |
| fixed impact | `normal_distinct_consumer_complete` | verified |

M3 transparent composite 为 196/196 expected terminal、0 conflict、0 mismatch；
五组 `duplicate-fail`、`distinct-complete`、`distinct-fail-slot1`、
`distinct-fail-slot2`、`distinct-consumer` trace 均有效。不存在一次单独
source run 达到 196/196 terminal，这一点不能在论文中省略。

### 3.7 M4：HMAC confirmation 与 dedup 组合验证

模型：

- `tamarin/replay/kwaay_replay_hmac_dedup.spthy`；
- `tamarin/impact/kwaay_impact_hmac_dedup.spthy`。

组合模型使用 confirmed event vocabulary，并按 base message `m` 去重，而不是按
`<m,tag>` 或 tag 去重。M4 实际支持：

- `confirmed_receiver_accept_has_sender`、
  `confirmed_message_accepted_at_most_once`、
  `confirmed_base_message_accepted_at_most_once` 和
  `injective_confirmed_receiver_accept` 均 verified；
- `one_confirmed_send_two_accepts_exists` falsified；
- `duplicate_same_base_different_tag_fail_exists` verified；
- `normal_two_distinct_valid_confirmed_accepts_complete` verified；
- impact 中 `one_confirmed_send_two_accepts_two_installs_exists` falsified；
- `unique_install_within_completed_consumer`、
  `duplicate_batch_has_no_accept_output`、`duplicate_batch_has_no_install` 和
  `normal_two_distinct_valid_confirmed_outputs_consumer_complete` verified。

M4 由两个完整且 manifest-valid 的 Tamarin-only source run 组成 transparent
composite：296/296 terminal、296/296 MATCH、281 verified、15 falsified、0
terminal conflict、0 unresolved、0 mismatch。M4 没有重跑 ProVerif；P0/P1 正面
结果继承自之前冻结的 ProVerif core/HMAC summaries。

组合修复的结论为：HMAC 负责 full-parameter confirmation/agreement，批内原子
去重负责 exact-message occurrence uniqueness；两者解决不同性质，组合后在当前
固定两槽范围内同时保持对应关系和重复拒绝，并保留不同有效 confirmed messages
的正常完成路径。

### 3.8 M5：可复现实验冻结

M5 没有增加协议性质，也没有重跑证明器。它冻结了：

- 405 行 expected / actual result contract；
- 296 行 M4 Tamarin transparent-composite 结果；
- 89 行 inherited ProVerif evidence；
- 20 行 M4 ProVerif `not_run_out_of_scope` 声明；
- 66 项 artifact inventory、405 行 raw-to-summary、18 行 claim matrix；
- 92 项 Git-blob/infrastructure checksum。

这使原始路线可以直接进入论文写作，不需要重新运行已冻结实验。

## 4. RQ-v2 的正确整合位置

RQ-v2 不应替代上述主线，也不能被用来重解释 M2。它提供一个重要修复边界：

```text
exact-message dedup 阻止同一 m 的批内重复接受；
但 exact-message dedup 不推出同一批次中的 party distinctness。
```

`tamarin/rq-v2-minimal/rqv2_message_dedup.spthy` 中
`same_party_different_messages_batch_exists` verified，说明同一参与方的两个不同
发送实例和不同消息可以各有匹配来源并在同批被接受。该见证不是 M0--M5 的
same-message replay，也没有 `InstallSession`，不能直接套用 M2 的
`C_install-v2` 结果。

论文中的正确作用是：

1. 说明 M3/M4 的 exact-message dedup 修复目标是 replay/occurrence
   uniqueness；
2. 说明该修复不替代 K-Waay 原有 distinct-party input discipline；
3. 把参与方准入保留为一个独立的 integration invariant，而不是把同方不同消息
   反例包装成重复消息攻击。

## 5. 恢复后的因果链

```text
原始 Figure 7 core
  -> symbolic secrecy / component origin 成立
  -> full-parameter non-injective correspondence 失败
  -> HMAC confirmation 在 no-compromise baseline 中恢复 P1

允许同一有效消息在同一 batch/state 的两个 slot 中重复出现
  -> HMAC gate 可被同一 confirmed message 合法通过两次
  -> matching existence 保持，但 occurrence injectivity 失败
  -> 在 C_install-v2 下，两个 accepts 条件化传播为两个 local installations

处理前 batch-local atomic exact-message dedup
  -> duplicate branch 在任何 accept/output/install 前关闭 batch
  -> one-send-two-accept 和 two-install witnesses 不再可达
  -> distinct-message normal paths 保持可达

HMAC + dedup
  -> 同时覆盖 P1 confirmation 和 batch-local P2/P3 修复
  -> 仍不替代 DistinctPartyPerBatch
```

## 6. 路线结论

M0--M5 已形成完整的“性质分层--反例--条件化影响--修复--组合验证--artifact
冻结”闭环。继续研究的重点不应是重跑这些结果，而是按正确边界恢复论文叙述。
只有当论文要声称真实 K-Waay 部署会逐输出安装、存在会话克隆或满足原始
distinct-party 前置条件的执行仍受同一重复攻击时，现有证据才不足。

