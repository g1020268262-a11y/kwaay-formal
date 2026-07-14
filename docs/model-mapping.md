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
  preliminary deniability diff models
```

当前不声称完整证明 K-Waay computational security。

## 协议对象映射

| K-Waay 对象 | ProVerif 抽象 | Tamarin V6/V7 | Tamarin replay original | 状态 |
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
| HMAC key confirmation | `proverif/variants/hmac-confirmation/` 独立变体 | 未建模 | 未建模；HMAC-only replay bridge 尚未建立 | ProVerif baseline 已建模；M1 bridge 缺失 |
| duplicate input / replay | no batch slot，不能表达 | 不是 V6/V7 的专门攻击目标 | same message 被加入 fixed two-slot batch；`one_send_two_accepts_exists` | original 反例已建模 |
| session installation | 未建模 | 无 `InstallSession` / local handle event | 无 `InstallSession` / local handle event | P3 under `C_install` 未建模；M2 负责 |
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
| P3 under `C_install` unique session installation | 尚无 impact/composition model | 尚无 `InstallSession` / `unique_install` | 命名组合假设下 receiver output 到 fresh local handle 的条件化性质 | not modeled；M2 负责实现 |

P1 与 P2 使用不同 event vocabulary。ProVerif 的
`SendDone(A,B,sid,k)`/`RecvDone(B,A,sid,k)` 不包含 occurrence、slot、batch
或 receiver state；replay 的 `SenderSession`/`ReceiverAccept` 显式包含完整
message 和 receiver-side occurrence context。二者不能自动视为等价事件。

Replay original 的参数级 matching 还依赖 `full_message_unique_send` 将完整
sender tuple 唯一化为一个 sender occurrence。未来 positive occurrence
injectivity artifact 必须证明相应 tuple 唯一性，或在事件中使用明确的 sender
occurrence/session identifier；这不是要求当前 M1 修改事件。

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

### Independent deniability artifacts

独立 core/malicious/negative `--diff` 模型提供 preliminary symbolic
deniability evidence；它们不属于 V6/V7 lifecycle 或 replay original。

整个 Tamarin 分支当前仍不建模：

```text
HMAC-only replay bridge
batch-local duplicate rejection / repaired injectivity
receiver output -> upper-layer session installation
computational security
complete malicious / Big Brother / computational deniability
```

## 当前主要解释

当前形式化分析支持下面这个解释：

```text
K-Waay Figure 7 core 可以满足 symbolic secrecy-style properties，
但不满足 `(A,B,sid,k)` full-parameter non-injective correspondence；
HMAC confirmation 在 no-compromise baseline 中恢复该 correspondence；
original BatchReceive replay abstraction 在 same-batch/same-receiver-state
子范围内产生 injectivity 反例，该反例足以否定 global one-send-one-accept；
P3 under C_install 的上层 unique session installation 尚未建模。
```

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
P3 under C_install / concrete session cloning impact
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
```

后续里程碑不得把预期结果写成实际结果：

```text
M1: HMAC-only replay bridge
M2: implement the named C_install impact/composition interface
M3: fixed batch-local atomic dedup
M4: HMAC + dedup combined regression
M5: artifact/result freeze
```

## 根 README 同步建议（本轮未修改）

根 `README.md` 仍把仓库描述为“first symbolic ProVerif model ... without
batching”，不能反映当前 ProVerif、HMAC、Tamarin lifecycle、replay 和
deniability 分支。为避免在未确认信息架构前大幅重写，本轮只冻结以下建议：

1. 将仓库定位改为 K-Waay Figure 7 core 的多模型 symbolic formal analysis，
   而不是单一早期 no-batch ProVerif 模型。
2. 列出真实入口：ProVerif final core、HMAC variant、Tamarin V6/V7、replay
   original，以及 preliminary deniability diff models。
3. 用 P0-S/P0-O/P1/P2/P3 under `C_install` 的性质图链接到
   `docs/claim-hierarchy.md` 和 `docs/threat-compromise-matrix.md`，并标明
   P3 under `C_install` 尚未建模。
4. 明确 symbolic/computational 边界、已知 timeout，以及 replay original
   尚缺 committed raw result log 的 artifact 限制。

在确认 README 的目标读者、安装说明和统一运行入口之前，不应把上述建议扩写
成完整 artifact README。
