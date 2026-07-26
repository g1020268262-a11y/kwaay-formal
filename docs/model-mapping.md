# K-Waay 模型映射说明

## 目的

本文档用于说明 K-Waay 论文中的协议对象，当前如何被抽象到 ProVerif 和 Tamarin 模型中。

这个文件属于 WP1：最终模型整理阶段。

它主要回答：

```text
建模了什么
如何建模
哪些地方是抽象
哪些地方还没有建模
```

## 当前分析范围

当前形式化分析覆盖的是 K-Waay Figure 7 core 的部分 symbolic properties。

当前范围：

```text
ProVerif:
  Figure 7 core 的 no-batch / single-receive symbolic abstraction
  HMAC confirmation 的独立 no-batch 变体

Tamarin:
  V6 split-KEM / receiver state / dynamic batch skeleton
  V7 fixed four-slot terminal lifecycle
  replay original 的 fixed two-slot duplicate-input 模型
  HMAC-only replay bridge 的 fixed two-slot confirmed-message 模型
  M2 original impact/composition fixed two-slot C_install-v2 consumer
  M3 fixed replay 的 fixed two-slot batch-local atomic dedup 模型
  M3 fixed impact 的 fixed two-slot dedup + C_install-v2 consumer
  M4 HMAC+dedup combined replay 的 fixed two-slot confirmed-message + atomic dedup 模型
  M4 HMAC+dedup combined impact 的 fixed two-slot C_install-v2 consumer 模型
  preliminary deniability diff models
```

当前不声称完整证明 K-Waay computational security。

## 协议对象映射

| K-Waay 对象 | ProVerif 抽象 | Tamarin V6/V7 | Tamarin replay / impact artifacts | 状态 |
|---|---|---|---|---|
| sender identity `A` | symbolic name / process parameter | agent variable `$A` | agent variable `$A` | 已建模 |
| receiver identity `B` | symbolic name / process parameter | agent variable `$B` | agent variable `$B` | 已建模 |
| long-term KEM ciphertext `ct_l` | abstract KEM ciphertext term | 未显式建模 | private constructor `ct_l(A,B,rst,r_l)` | replay 显式符号建模 |
| ephemeral KEM ciphertext `ct_k` | abstract KEM ciphertext term | 未显式建模 | private constructor `ct_k(A,B,rst,r_k)` | replay 显式符号建模 |
| split-KEM component `ct_s` | abstract component / ciphertext | opaque `cts` / `ComponentKey` relation | private constructor `ct_s(A,B,sst,rst,r_s)` | 两类 Tamarin 抽象不同 |
| long-term KEM secret `K_l` | symbolic shared secret | 未显式建模 | `secret_l(A,B,rst,r_l)` | replay 显式符号建模 |
| ephemeral KEM secret `K_k` | symbolic shared secret | 未显式建模 | `secret_k(A,B,rst,r_k)` | replay 显式符号建模 |
| split-KEM secret `K_s` | symbolic shared secret | `Ks` in `ComponentKey(A,B,rst,cts,Ks)` | `secret_s(A,B,sst,rst,r_s)` | 抽象建模 |
| complete message `m` | tuple `(ct_l,ct_k,ct_s)` | 没有完整三 ciphertext message | `m=<ct_l,ct_k,ct_s>` in `SenderCreatesMessage` | replay 显式构造 |
| session id `sid` | symbolic transcript/session identifier | 没有完整 transcript-based `sid`；`bid/idx/rst` 是 lifecycle/occurrence context，不是 `sid` | `session_id(A,B,pkA,pkB,prekeyA,prekeyB,m)` | replay 显式构造 |
| session key `k` | `KDF(K_l,K_k,K_s,sid)` abstraction | V6: `rkey(B,A,rst,cts,Ks)`；V7: component/lifecycle abstraction，无 replay-style full key | `session_key(K_l,K_k,K_s,sid)` | 各 artifact 分别解释 |
| sender protocol event | `SendDone(A,B,sid,k)` | `SenderComponent(A,B,rst,cts,Ks)` 等 component/lifecycle event | `SenderSession(A,B,m,sid,k)` | 事件不自动等价 |
| receiver protocol event | `RecvDone(B,A,sid,k)` | `BatchSlotAccept` / `ReceiverKey` 等 slot/component event | `ReceiverAccept(B,A,bid,idx,rst,m,sid,k)` | 事件不自动等价 |
| sender split-KEM state | symbolic sender state | `SenderState(A,sst)` | `SenderState(A,sst)` | 抽象建模 |
| receiver split-KEM state | symbolic receiver state | `ReceiverState(B,rst)` | `ReceiverState(B,rst)` | 已建模 |
| receiver public prekey/state | public input to sender | `!ReceiverPublicState(B,rst)` | `!ReceiverPublicState(B,rst)` | 已建模 |
| BatchReceive | no-batch approximation | V6: bounded dynamic lifecycle skeleton；V7: fixed four-slot terminal lifecycle | fixed two-slot duplicate-input abstraction | 分别限定范围 |
| batch identifier | 未显式建模 | `bid` | `bid` | Tamarin 中建模 |
| batch slot | 未显式建模 | `idx`, `PendingSlot`, `BatchSlotAccept` | `idx`, fixed `AddedSlot1/2`, `ReceiverAccept` | Tamarin 中建模 |
| batch fail | 未显式建模 | `BatchFail`, `BatchSlotFail` | `BatchFail`, fixed-slot failure rules | 抽象建模 |
| batch complete | 未显式建模 | `BatchComplete` | `BatchComplete` after two processed slots | 抽象建模 |
| state compromise | explicit compromise event | `CompromiseReceiverState`, `CompromiseSenderState` | 同名 compromise events；P2 witness 排除二者全程出现 | 已建模但 theorem 范围不同 |
| HMAC key confirmation | `proverif/variants/hmac-confirmation/` 独立 no-batch 变体 | 未建模 | HMAC-only bridge 中 `tag=hmac(confirm_key(k),sid)`，public confirmed message 为 `<m,tag>` | ProVerif P1 baseline 与 Tamarin M1 replay bridge 均已建模；证据角色不同 |
| HMAC+dedup combined accept | no-batch ProVerif HMAC evidence inherited；M4 未重跑 ProVerif | 未建模 | M4 combined replay/impact 中 `ConfirmedSend`, `HmacValidated`, `ConfirmedReceiverAccept` 使用 base message `m` 和 tag `hmac(confirm_key(k),sid)` | M4 Tamarin-only evidence；ProVerif 5 targets 本轮 out of scope |
| duplicate input / replay | no batch slot，不能表达 | 不是 V6/V7 的专门攻击目标 | original 与 HMAC-only 都把同一完整 message 放入 fixed two-slot batch；相应 one-send-two-accept witness verified | original 与 HMAC-only same-batch/same-state 反例已建模 |
| batch-local dedup decision | 未建模 | 未建模 | fixed replay/impact and M4 combined replay/impact 中 `DedupPending` + `DedupDecisionToken` 在线性状态上进行一次决定 | M3/M4 fixed two-slot、同一 `B,bid,rst` |
| duplicate decision outcome | 未建模 | 未建模 | `DuplicateDetected` 后原子产生 `BatchFail/BatchClosed/ConsumeReceiverState`，不开放 processing | exact complete base message `m` identity；不是 full `<m,tag>`，也不是全局 cache |
| distinct decision outcome | 未建模 | 未建模 | `DedupPassed` 产生 `CheckedSlot1/2`，之后才允许 `ProcessSlot1/2` | processing 前 pre-scan；distinct 正常/失败路径均保留 |
| accepted output occurrence | 未建模 | 未建模 | original/fixed/M4 impact artifacts 中 `aid` / `AcceptOutputCreated` / linear `AcceptedOutput`；replay-only artifacts 不含该层 | M2 original、M3 fixed impact、M4 combined impact 建模 |
| session installation | 未建模 | 无 `InstallSession` / local handle event | original/fixed/M4 impact 中 `InstallFromAccept` + `InstallSession`；replay-only artifacts 不含该层 | 条件化建模；不代表 deployed implementation |
| local installation handle | 未建模 | 未建模 | original/fixed impact 中 fresh `h` | 仅 symbolic composition object |
| upper-layer consumer | 未建模 | 未建模 | original/fixed impact 中 `ConsumerStage0/1/2`, `ConsumerComplete`, `ClosedConsumer` | fixed two-output conditional abstraction |
| deniability | 未建模 | 不在 V6/V7；由 core/malicious/negative `--diff` 独立 artifacts 建模 | 未建模 | preliminary symbolic evidence；非完整 deniability |
| computational KIND | 未建模 | 未建模 | 未建模 | 后续 CryptoVerif / hand proof |

## 安全目标映射

| 目标 / 性质 | 唯一 artifact | query / lemma | 含义 | 限制 |
|---|---|---|---|---|
| P0-S sender-side secrecy | ProVerif final core — original Figure-7 no-batch abstraction | `not attacker(k)` with `SenderKey` | baseline 下攻击者不能推出 sender-side key | symbolic only |
| P0-S receiver-side secrecy | ProVerif final core — original Figure-7 no-batch abstraction | `not attacker(k)` with `ReceiverKey` | baseline 下攻击者不能推出 receiver-side key | symbolic only |
| P0-O split-KEM component origin | ProVerif final core — original Figure-7 no-batch abstraction | `SplitKemAccepted ==> SenderSplitKemComponent` | accepted split-KEM component 有 sender origin | component-level only；仅有 cross-target non-vacuity support |
| P1 original full-parameter non-injective correspondence | ProVerif final core — original Figure-7 no-batch abstraction | `RecvDone ==> SendDone` | exact `(A,B,sid,k)` receiver completion 必须存在 sender completion | core baseline 为 false；无 slot/occurrence 语义 |
| P1 HMAC full-parameter non-injective correspondence | ProVerif HMAC confirmation — no-batch abstraction | `RecvDone ==> SendDone` | HMAC check 后的 exact `(A,B,sid,k)` correspondence | HMAC baseline 为 true；仅 A sig-key leak target 为 false |
| receiver-side exception | Tamarin V6 | `slot_key_known_requires_exception` | attacker-known receiver key 必须有 unpartnered / early compromise 解释 | universal classification verified；各 exception branch reachability 未独立检查 |
| batch slot origin | Tamarin V6 | `slot_origin_without_early_compromise` | 无 early compromise 时 accepted slot 有 sender origin | bounded dynamic abstraction |
| batch abort | Tamarin V6/V7 | `batch_fail_complete_exclusive` | 同一 batch 不能同时 fail 和 complete | abstract fail model |
| batch-level state consumption | Tamarin V6/V7 | `batch_complete_consumes_state`, `batch_fail_consumes_state` | receiver state 在 batch close 时消费 | symbolic lifecycle |
| dynamic batch lifecycle | Tamarin V6 | `process_requires_slot_added`, `process_requires_seal` | processed slot 必须先 add，且 batch 必须先 seal | bounded skeleton；不证明 arbitrary-length batch |
| fixed four-slot terminal lifecycle | Tamarin V7 | `complete_requires_all_slots_done`, `no_slot_accept_after_close` | 建模的四个 slot 全部完成后才能 complete，close 后无 accept | fixed four-slot only |
| P2 matching existence/order | Tamarin replay original — fixed two-slot replay abstraction | `receiver_accept_has_sender` | 每个 `ReceiverAccept(B,A,bid,idx,rst,m,sid,k)` 有更早、在 `(A,B,m,sid,k)` 上 matching 的 `SenderSession` | verified |
| P2 sender-occurrence uniqueness / matching disambiguation | Tamarin replay original — fixed two-slot replay abstraction | `full_message_unique_send` | 完整 sender tuple `(A,B,m,sid,k)` 在当前 artifact 中唯一确定一个 `SenderSession` occurrence | verified；不是 P2 injectivity，也不是 replay prevention |
| P2 occurrence injectivity | Tamarin replay original — fixed two-slot replay abstraction | `injective_receiver_accept` | 同一 `bid`、同一 `rst`、可能不同 `idx1/idx2` 下，一个 sender occurrence 不能匹配两个 accept occurrences | falsified；same-batch/same-state 子范围反例足以否定 global P2，但不是 positive global theorem |
| P2 matching-accept executability / non-vacuity | Tamarin replay original — fixed two-slot replay abstraction | `normal_single_accept` | 至少一个 honest `SenderSession` 及其更晚 matching `ReceiverAccept` 的路径可达 | verified exists-trace；does not exclude additional `ReceiverAccept` events；不是 universal theorem |
| P2 lifecycle sanity | Tamarin replay original — fixed two-slot replay abstraction | `normal_batch_complete` | 正常 accept 路径可到 batch complete | verified exists-trace；不是 universal theorem |
| P2 attack witness | Tamarin replay original — fixed two-slot replay abstraction | `one_send_two_accepts_exists` | 无 compromise 时，同一 `bid/rst` 中 one send 可产生两个不同 slot accepts | verified exists-trace；不是 universal theorem |
| HMAC bridge matching existence/order | Tamarin HMAC-only replay bridge | `confirmed_receiver_accept_has_sender` | 每个 confirmed accept 有更早 matching send | verified；因接收规则依赖 `HonestSession`，主要是结构性来源映射 |
| HMAC bridge sender occurrence disambiguation | Tamarin HMAC-only replay bridge | `confirmed_message_unique_send` | 相同 `(A,B,m,sid,k,tag)` 只对应一个 send timepoint | verified；不是 injectivity 或 replay prevention |
| HMAC bridge P2 occurrence injectivity | Tamarin HMAC-only replay bridge | `injective_confirmed_receiver_accept` | same `bid/rst` 下一个 matching send 不应对应两个 accept occurrences | falsified；same-batch/same-state |
| HMAC bridge normal-path non-vacuity | Tamarin HMAC-only replay bridge | `normal_confirmed_single_accept`, `normal_confirmed_batch_complete` | matching accept 与 normal batch completion 均可达 | verified exists-trace |
| HMAC bridge attack witness | Tamarin HMAC-only replay bridge | `one_confirmed_send_two_accepts_exists` | 同一 confirmed message 在两个不同 slot 通过同一 HMAC gate | verified；无 sender/receiver state compromise |
| HMAC bridge lifecycle regressions | Tamarin HMAC-only replay bridge | selected 11 lifecycle/state lemmas | add/seal/process/close/state-consumption 语义未因 bridge 退化 | 全部 verified |
| P3 under `C_install-v2` unique session installation | `tamarin/impact/kwaay_impact_original.spthy` | `one_send_two_accepts_two_installs_exists`; `unique_install_within_completed_consumer`; `install_session_has_interface_origin`; `install_from_accept_has_session`; `accept_output_installed_at_most_once`; `consumer_complete_requires_all_outputs_installed`; `distinct_accept_sources_have_distinct_handles` | fixed two-slot conditional consumer 中，original duplicate acceptance 是否传播为相同 peer/sid/key、不同 symbolic local handles | conditional witness verified；unique installation falsified；不声称 real implementation/session/Double Ratchet |
| M3 fixed replay batch-local P2 | `tamarin/replay/kwaay_replay_fixed.spthy` | `one_send_two_accepts_exists`; `same_message_accepted_at_most_once`; `injective_receiver_accept`; `duplicate_batch_fail_exists`; `duplicate_batch_has_no_accept`; `normal_distinct_batch_complete` | 同一 `B,bid,rst` 中按 exact complete `m` 在任何 `ProcessSlot` 前原子去重 | duplicate witness falsified；at-most-once/injectivity/duplicate failure/distinct completion verified；不是 global replay theorem |
| M3 fixed impact P3 under `C_install-v2` | `tamarin/impact/kwaay_impact_fixed.spthy` | `one_send_two_accepts_two_installs_exists`; `unique_install_within_completed_consumer`; `normal_consumer_complete`; `normal_distinct_consumer_complete`; `duplicate_batch_has_no_accept_output`; `duplicate_batch_has_no_install` | batch-local duplicate rejection是否阻断 accepted output 与 conditional installation，同时保留 distinct consumer | duplicate-install witness与 frozen legacy same-message normal target falsified；unique installation/no duplicate output or install/distinct consumer verified |
| M4 combined replay batch-local P2 | `tamarin/replay/kwaay_replay_hmac_dedup.spthy` | `one_confirmed_send_two_accepts_exists`; `confirmed_message_accepted_at_most_once`; `confirmed_base_message_accepted_at_most_once`; `injective_confirmed_receiver_accept`; `duplicate_same_base_different_tag_fail_exists`; `normal_two_distinct_valid_confirmed_accepts_complete` | HMAC-confirmed accept + exact base-message dedup in the same fixed `B,bid,rst` two-slot batch | duplicate confirmed accept witness falsified；same confirmed/base message at-most-once and injectivity verified；different-tag same-base duplicate rejected；normal distinct completion verified |
| M4 combined impact P3 under `C_install-v2` | `tamarin/impact/kwaay_impact_hmac_dedup.spthy` | `one_confirmed_send_two_accepts_two_installs_exists`; `unique_install_within_completed_consumer`; `duplicate_batch_has_no_accept_output`; `duplicate_batch_has_no_install`; `normal_two_distinct_valid_confirmed_outputs_consumer_complete`; `hmac_failure_slot2_after_prior_accept_exists` | confirmed accepted output and symbolic local installation under the bounded consumer | duplicate accepted output/install blocked；distinct valid confirmed outputs can complete consumer；slot-2 mismatch after slot-1 accept remains reachable |

P1 与 P2 使用不同 event vocabulary。ProVerif 的
`SendDone(A,B,sid,k)`/`RecvDone(B,A,sid,k)` 不包含 occurrence、slot、batch
或 receiver state；replay 的 `SenderSession`/`ReceiverAccept` 显式包含完整
message 和 receiver-side occurrence context。二者不能自动视为等价事件。

Replay original 的参数级 matching 依赖 `full_message_unique_send` 将完整
sender tuple 唯一化为一个 sender occurrence。M1 HMAC-only bridge 对
`(A,B,m,sid,k,tag)` 使用 fresh ciphertext randomness 与
`confirmed_message_unique_send` 完成同样的 occurrence 消歧。两者都不能把
该 lemma 解释成 injectivity 或 replay prevention。未来 fixed/combined artifact
若继续按 tuple matching，需要保留等价的消歧证明，或加入明确的
occurrence/session identifier；不能无条件把 tuple equality 当作 occurrence
equality。

只有在同一 artifact instantiation、相同事件语义和相同参数元组下，才允许
写 `P2 => P1`。

## ProVerif 模型边界

当前 ProVerif 主模型是 K-Waay Figure 7 core 的 no-batch / single-receive
symbolic abstraction；HMAC confirmation 位于独立变体目录，不是原始 Figure 7
core 的组成部分。

它建模：

```text
m = (ct_l, ct_k, ct_s)
sender / receiver roles
symbolic KEM secrets
symbolic KDF
sender / receiver key events
agreement diagnostic query
component authenticity query
selected compromise experiments
```

它不建模：

```text
full BatchReceive vector
real KEM algorithms
real KDF security
real signature scheme
computational KIND game
batch slot / duplicate acceptance / injectivity
session installation
deniability
```

## Tamarin 模型边界

当前 Tamarin artifact 必须按职责分别解释。

### V6/V7 lifecycle artifacts

V6/V7 建模：

```text
receiver state lifecycle
sender / receiver state compromise ordering
receiver-side exception classification
batch slot
batch abort
batch-level state consumption
V6 bounded dynamic AddSlot / SealBatch / ProcessSlot skeleton
V7 fixed four-slot terminal lifecycle
```

V6/V7 不显式建模完整 `ct_l`、`ct_k`、三 ciphertext message、完整
transcript-based `sid`，也不使用 replay 的
`session_key(K_l,K_k,K_s,sid)` 构造。V6 的 `rkey(B,A,rst,cts,Ks)` 只是在
其 component/lifecycle abstraction 中使用的 receiver-key term。

### Replay original artifact

`tamarin/replay/kwaay_replay_original.spthy` 显式建模：

```text
private ct_l/4, ct_k/4, ct_s/5 constructors
m = <ct_l,ct_k,ct_s>
session_id(A,B,pkA,pkB,prekeyA,prekeyB,m)
session_key(K_l,K_k,K_s,sid)
SenderSession(A,B,m,sid,k)
ReceiverAccept(B,A,bid,idx,rst,m,sid,k)
fixed two-slot same-batch duplicate-input trace
```

这些仍是 free symbolic constructors，不是 concrete KEM/KDF security。Replay
original 不建模真实 vector traversal、真实 decapsulation failure、HMAC、去重
修复或 session installation。

### HMAC-only replay bridge

`tamarin/replay/kwaay_replay_hmac_only.spthy` 复用 fixed two-slot lifecycle，
显式加入：

```text
tag = hmac(confirm_key(k),sid)
confirmed message = <m,tag>
ConfirmedSend(A,B,m,sid,k,tag)
ConfirmedReceiverAccept(B,A,bid,idx,rst,m,sid,k,tag)
```

它验证 confirmed-message matching、sender occurrence 消歧、正常路径和
lifecycle，并给出 same-batch/same-state duplicate acceptance 反例。
`HonestSession` 是接收规则的持久来源关系，因此 matching existence 主要为
结构性结果；该模型的职责是 replay/occurrence 分析。具体 HMAC P1 的主要独立
证据仍来自 ProVerif HMAC baseline。

### M2 original impact/composition artifact

`tamarin/impact/kwaay_impact_original.spthy` 从 frozen replay original 派生，
但保持为独立 theory。它保留 lower-layer 事件语义和 18 条 frozen lower-layer
lemma 的完整公式，并在其上加入 `C_install-v2` 条件化 consumer。

新增对象与事件：

```text
aid = fresh accepted-output occurrence identifier
h   = fresh symbolic local installation handle
AcceptOutputCreated(aid,B,A,bid,idx,rst,m,sid,k)
InstallFromAccept(aid,B,h,A,bid,idx,rst,m,sid,k)
InstallSession(B,h,A,sid,k)
ConsumerStage0 / ConsumerStage1 / ConsumerStage2
ConsumerComplete(B,bid,rst)
ClosedConsumer(B,bid,rst)
```

`aid` 不进入协议 message、`sid` 或 key；`h` 不是协议 session identifier。
`InstallFromAccept` 保存完整 output provenance，`InstallSession` 是条件化组合
事件。consumer 只由 successful `BatchComplete` 启动；failure paths 不创建
consumer。两个 linear accepted-output tokens 可按任意顺序被独立消费，两个
install 都完成后才产生 `ConsumerComplete`。

C7 假定 consumer 不按 `sid`、message、peer 或 key 合并/去重，而是独立安装
每个 successful output；C8 明确 C7 只是 composition assumption。仓库没有规范
或实现证据证明 deployed K-Waay upper layer 遵循该行为。

该 theory 有 19 条 composition lemmas 和 18 条 frozen lower-layer lemmas。
正式 evidence 为：

```text
logs/tamarin-impact-original/aggregate-results.tsv
logs/tamarin-impact-original/proofs/
logs/tamarin-impact-original/attack-trace.out
logs/tamarin-impact-original/unique-install-trace.out
logs/tamarin-impact-original/frozen-formula-comparison.txt
logs/tamarin-impact-original/lower-layer-result-comparison.txt
logs/tamarin-impact-original/SHA256SUMS.txt
```

实际 composition profile 为 18 verified / 1 falsified；总计 37 条终态为
34 verified / 3 falsified。`one_send_two_accepts_two_installs_exists` verified，
`unique_install_within_completed_consumer` falsified；两个核心 trace 都是 28
steps。18/18 frozen formula 和 18/18 lower-layer result comparison 均 MATCH。

### M3 fixed replay and fixed impact artifacts

`tamarin/replay/kwaay_replay_fixed.spthy` 在 original fixed two-slot lifecycle
中加入线性、单次使用的 dedup decision：

```text
OpenStage2 + AddedSlot1 + AddedSlot2
  -> DedupPending + DedupDecisionToken

exact duplicate m:
  -> DuplicateDetected + BatchFail + BatchClosed + ConsumeReceiverState

distinct m1,m2:
  -> DedupPassed + CheckedSlot1 + CheckedSlot2
  -> ProcessSlot1 / ProcessSlot2
```

scope 是同一 `B,bid,rst`，identity 是 exact complete public message `m`，决定
发生在两个 slot 收集并 seal 后、任何 `ProcessSlot` 前。duplicate branch 不产生
`ReceiverAccept`；distinct branch 仍可 complete，且原抽象 FailSlot1/FailSlot2
路径仍可达。该模型不提供 cross-batch cache、rollback protection 或
arbitrary-length theorem。

`tamarin/impact/kwaay_impact_fixed.spthy` 保留 M2 `C_install-v2` 的三个 frozen
consumer rules 和完整 provenance chain。由于 duplicate branch 在 processing 前
关闭 batch，它不能产生 `AcceptOutputCreated` / linear `AcceptedOutput`，不能产生
`ConsumerStarted`，因而不能到达 `InstallFromAccept` 或 `InstallSession`。distinct
messages 仍可产生两个 outputs、两个 installations 和 `ConsumerComplete`。

实际 evidence 位于 `logs/tamarin-m3-closeout/`，是两次同 A3/inputs/tool
versions 的完整、manifest-valid 运行组成的 transparent composite evidence。
196/196 composite statuses 匹配 expected vector，0 terminal conflicts，0
mismatches；两次运行各在不同目标出现一次 intermittent source-saturation
`<<loop>>`，没有一次单独 invocation 达到 196/196 terminal。

### M4 HMAC+dedup combined replay and impact artifacts

`tamarin/replay/kwaay_replay_hmac_dedup.spthy` combines the HMAC confirmation
vocabulary from the HMAC-only bridge with the sealed, batch-local dedup decision
from M3. Successful lower-layer acceptance is represented by
`ConfirmedReceiverAccept(B,A,bid,idx,rst,m,sid,k,tag)`, and the tag must be the
exact `hmac(confirm_key(k),sid)` for a matching `HonestSession`.

The dedup identity is the exact complete base message `m`, not the confirmed
full message `<m,tag>`, not `tag`, and not global seen-message state. Duplicate
same-base wrappers, including different-tag duplicates, take the atomic
duplicate branch before processing; distinct wrappers take the checked branch
and retain normal completion and explicit HMAC mismatch paths.

`tamarin/impact/kwaay_impact_hmac_dedup.spthy` adds the bounded `C_install-v2`
consumer to the combined lower layer. It maps confirmed lower-layer acceptance
to tag-free accepted outputs through `AcceptOutputCreated` and linear
`AcceptedOutput`; `InstallFromAccept` and `InstallSession` remain conditional
symbolic consumer events, not deployed implementation events.

The replay theory has exactly 38 lemmas. The impact theory has exactly 62
lemmas: the 38 combined lower-layer properties, 19 mechanically mapped
composition properties, and 5 impact-only properties. The Tamarin-only
evidence is `logs/tamarin-m4-hmac-dedup/`: two complete `VALID` source runs and
a transparent composite result with 296/296 terminal, 296/296 MATCH, 0
terminal conflicts, 0 unresolved rows, and 0 mismatches.

The five ProVerif targets in full 301-target mode were not run for M4 Evidence
Commit B. ProVerif core/HMAC results are inherited from the previously committed
summaries under `logs/final/proverif/` and
`logs/variants/hmac-confirmation/proverif/`.

### Independent deniability artifacts

独立 core/malicious/negative `--diff` 模型提供 preliminary symbolic
deniability evidence；它们不属于 V6/V7 lifecycle 或 replay original。

整个 Tamarin 分支当前仍不建模：

```text
computational security
complete malicious / Big Brother / computational deniability
```

receiver output → symbolic local installation 已在 M2 original、M3 fixed impact
和 M4 combined impact artifacts 中条件化建模，但没有真实 session database、
Double Ratchet、application action 或 deployed implementation mapping。

## 当前主要解释

当前形式化分析支持下面这个解释：

```text
K-Waay Figure 7 core 可以满足 symbolic secrecy-style properties，
但不满足 `(A,B,sid,k)` full-parameter non-injective correspondence；
HMAC confirmation 在 ProVerif no-compromise baseline 中恢复该 correspondence；
HMAC-only Tamarin bridge 进一步表明 confirmation 本身不提供
same-batch/same-state replay prevention 或 occurrence injectivity；
该 bridge 的 matching existence 在 `HonestSession` 下主要是结构性结果；
original 与 HMAC-only replay 反例都足以否定 global one-send-one-accept；
在 C_install-v2 条件化 consumer 下，original duplicate acceptance 可传播为
两个不同 symbolic local handles，unique installation 被 falsified；
M3 fixed two-slot dedup-only 模型在同一 B/bid/rst 中按 exact complete m
于 processing 前拒绝 duplicate，使 two-accept witness falsified、at-most-once 与
injectivity verified；fixed impact 在 C_install-v2 下阻断对应 duplicate outputs
和 installations，同时保留 distinct-message consumer completion；
M4 combined replay/impact 同时要求 HMAC confirmation 与 batch-local atomic
dedup，阻断 same-base confirmed duplicate accept、duplicate accepted output 和
duplicate installation，同时保留 distinct confirmed-message batch / consumer
completion。
```

这些 M2/M3/M4 conditional impact 结论不证明 deployed K-Waay session cloning。
它们依赖 fixed two-output consumer 独立消费 outputs 的 C7/C8 边界，不包含真实
session database、Double Ratchet 或 application behavior。

`RecvDone ==> SendDone` 为 false 不应解释成 key-recovery attack。

它应解释成：

```text
KIND-style secrecy 和 explicit key confirmation / exact agreement 之间的安全目标边界。
```

也就是说：

```text
攻击者不能推出 baseline session key；
但 receiver accept 不一定对应完整 exact sender session。
```

## 当前不能声称的内容

当前模型不能证明：

```text
full K-Waay security
computational KIND
UNF-1KMA
IND-1BatchCCA
full deniability
full BatchReceive vector correctness
real KEM decapsulation failure behavior
HMAC 已阻止 duplicate acceptance
duplicate ReceiverAccept 在没有显式 C_install-v2 composition assumptions 时，
不能自行推出 duplicate installation
C_install-v2 是 deployed K-Waay 的实际 upper-layer behavior
真实 session cloning / Double Ratchet duplication
application exploit
arbitrary-length impact
global/cross-batch/rollback replay prevention
M4 Tamarin-only evidence 重新运行了 ProVerif 5 targets
single M4 source run reached 296/296 terminal
```

## M0 claim 与后续里程碑

P0-S、P0-O、P1、P2 与 P3 under `C_install` 的性质图、状态、证据与非主张见：

```text
docs/claim-hierarchy.md
docs/threat-compromise-matrix.md
```

当前真实模型入口是：

```text
proverif/kwaay_core_final.cpp.pv
proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv
tamarin/kwaay_splitkem_batch_dynamic_v6.spthy
tamarin/kwaay_splitkem_batch_dynamic_v7.spthy
tamarin/replay/kwaay_replay_original.spthy
tamarin/replay/kwaay_replay_hmac_only.spthy
tamarin/impact/kwaay_impact_original.spthy
tamarin/replay/kwaay_replay_fixed.spthy
tamarin/impact/kwaay_impact_fixed.spthy
tamarin/replay/kwaay_replay_hmac_dedup.spthy
tamarin/impact/kwaay_impact_hmac_dedup.spthy
```

后续里程碑不得把预期结果写成实际结果：

```text
M1: ✅ HMAC-only replay bridge completed with raw evidence
M2: ✅ original conditional impact/composition evidence
M3: ✅ fixed two-slot batch-local atomic dedup with transparent composite evidence
M4: ✅ HMAC + dedup combined Tamarin-only transparent composite evidence
M5: current unique next — final artifact/result freeze
```

## 根 README 同步建议（本轮未修改）

根 `README.md` 仍把仓库描述为“first symbolic ProVerif model ... without
batching”，不能反映当前 ProVerif、HMAC、Tamarin lifecycle、replay 和
deniability 分支。为避免在未确认信息架构前大幅重写，本轮只冻结以下建议：

1. 将仓库定位改为 K-Waay Figure 7 core 的多模型 symbolic formal analysis，
   而不是单一早期 no-batch ProVerif 模型。
2. 列出真实入口：ProVerif final core、HMAC variant、Tamarin V6/V7、replay
   original、HMAC-only replay bridge、M2 original impact/composition artifact、
   M3 fixed replay/impact artifacts、M4 HMAC+dedup replay/impact artifacts，
   以及 preliminary deniability diff models；模型索引至少加入：

   ```text
   tamarin/replay/kwaay_replay_hmac_only.spthy
   tamarin/impact/kwaay_impact_original.spthy
   tamarin/replay/kwaay_replay_hmac_dedup.spthy
   tamarin/impact/kwaay_impact_hmac_dedup.spthy
   ```

3. 用 P0-S/P0-O/P1/P2/P3 under `C_install-v2` 的性质图链接到
   `docs/claim-hierarchy.md` 和 `docs/threat-compromise-matrix.md`，并标明
   M2/M3/M4 impact 都只有 conditional consumer result，不是 deployed behavior。
4. 明确 symbolic/computational 边界与已知 timeout；
   replay original 尚缺独立、专用的 standalone evidence bundle；
   不过 M2 evidence 已提交完整 original regression raw output：

   ```text
   logs/tamarin-impact-original/original-regression.out
   ```

在确认 README 的目标读者、安装说明和统一运行入口之前，不应把上述建议扩写
成完整 artifact README。
