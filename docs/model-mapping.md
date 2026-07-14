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

| K-Waay 对象 | ProVerif 抽象 | Tamarin 抽象 | 状态 |
|---|---|---|---|
| sender identity `A` | symbolic name / process parameter | agent variable `$A` | 已建模 |
| receiver identity `B` | symbolic name / process parameter | agent variable `$B` | 已建模 |
| long-term KEM ciphertext `ct_l` | abstract KEM ciphertext term | V6 中未完整显式建模 | ProVerif 中部分建模 |
| ephemeral KEM ciphertext `ct_k` | abstract KEM ciphertext term | V6 中未完整显式建模 | ProVerif 中部分建模 |
| split-KEM component `ct_s` | abstract component / ciphertext | opaque `cts` / `ComponentKey` relation | 抽象建模 |
| long-term KEM secret `K_l` | symbolic shared secret | V6 中未显式建模 | ProVerif 中建模 |
| ephemeral KEM secret `K_k` | symbolic shared secret | V6 中未显式建模 | ProVerif 中建模 |
| split-KEM secret `K_s` | symbolic shared secret | `Ks` in `ComponentKey(A,B,rst,cts,Ks)` | 抽象建模 |
| session id `sid` | symbolic transcript/session identifier | 由 `bid` / `idx` / `rst` 间接表达 | 部分建模 |
| session key `k` | `KDF(K_l,K_k,K_s,sid)` abstraction | `rkey(B,A,rst,cts,Ks)` abstraction | 抽象建模 |
| sender split-KEM state | symbolic sender state | `SenderState(A,sst)` | 抽象建模 |
| receiver split-KEM state | symbolic receiver state | `ReceiverState(B,rst)` | 已建模 |
| receiver public prekey/state | public input to sender | `!ReceiverPublicState(B,rst)` | 已建模 |
| BatchReceive | no-batch approximation | dynamic batch skeleton | 部分建模 |
| batch identifier | 未显式建模 | `bid` | Tamarin 中建模 |
| batch slot | 未显式建模 | `idx`, `PendingSlot`, `BatchSlotAccept` | Tamarin 中建模 |
| batch fail | 未显式建模 | `BatchFail`, `BatchSlotFail` | 抽象建模 |
| batch complete | 未显式建模 | `BatchComplete` | 抽象建模 |
| state compromise | explicit compromise event | `CompromiseReceiverState`, `CompromiseSenderState` | 已建模 |
| HMAC key confirmation | `proverif/variants/hmac-confirmation/` 独立变体 | HMAC-only replay bridge 尚未建立 | ProVerif baseline 已建模；batch bridge 缺失 |
| duplicate input / replay | no batch slot，不能表达 | `tamarin/replay/kwaay_replay_original.spthy` | original 反例已建模 |
| session installation | 未建模 | 无 `InstallSession` / local handle event | P3 under `C_install` 未建模；`C_install` 只是 M2 命名假设 |
| deniability | 未建模 | core/malicious/negative `--diff` 独立模型 | preliminary symbolic evidence；非完整 deniability |
| computational KIND | 未建模 | 未建模 | 后续 CryptoVerif / hand proof |

## 安全目标映射

| 目标 / 性质 | 唯一 artifact | query / lemma | 含义 | 限制 |
|---|---|---|---|---|
| P0-S sender-side secrecy | ProVerif final core — original Figure-7 no-batch abstraction | `not attacker(k)` with `SenderKey` | baseline 下攻击者不能推出 sender-side key | symbolic only |
| P0-S receiver-side secrecy | ProVerif final core — original Figure-7 no-batch abstraction | `not attacker(k)` with `ReceiverKey` | baseline 下攻击者不能推出 receiver-side key | symbolic only |
| P0-O split-KEM component origin | ProVerif final core — original Figure-7 no-batch abstraction | `SplitKemAccepted ==> SenderSplitKemComponent` | accepted split-KEM component 有 sender origin | component-level only；仅有 cross-target non-vacuity support |
| P1 original full-parameter non-injective correspondence | ProVerif final core — original Figure-7 no-batch abstraction | `RecvDone ==> SendDone` | exact `(A,B,sid,k)` receiver completion 必须存在 sender completion | core baseline 为 false；无 slot/occurrence 语义 |
| P1 HMAC full-parameter non-injective correspondence | ProVerif HMAC confirmation — no-batch abstraction | `RecvDone ==> SendDone` | HMAC check 后的 exact `(A,B,sid,k)` correspondence | HMAC baseline 为 true；仅 A sig-key leak target 为 false |
| receiver-side exception | Tamarin | `slot_key_known_requires_exception` | attacker-known receiver key 必须有 unpartnered / early compromise 解释 | 抽象模型 |
| batch slot origin | Tamarin | `slot_origin_without_early_compromise` | 无 early compromise 时 accepted slot 有 sender origin | symbolic abstraction |
| batch abort | Tamarin | `batch_fail_complete_exclusive` | 同一 batch 不能同时 fail 和 complete | abstract fail model |
| batch-level state consumption | Tamarin | `batch_complete_consumes_state`, `batch_fail_consumes_state` | receiver state 在 batch close 时消费 | symbolic lifecycle |
| dynamic batch lifecycle | Tamarin | `process_requires_slot_added`, `process_requires_seal` | processed slot 必须先 add，且 batch 必须先 seal | 不证明 all pending slots done |
| fixed four-slot terminal lifecycle | Tamarin V7 | `complete_requires_all_slots_done`, `no_slot_accept_after_close` | 建模的四个 slot 全部完成后才能 complete，close 后无 accept | fixed four-slot only |
| P2 matching existence/order | Tamarin replay original — fixed two-slot replay abstraction | `receiver_accept_has_sender` | 每个 `ReceiverAccept` 有更早的 matching `SenderSession` | verified |
| P2 occurrence injectivity | Tamarin replay original — fixed two-slot replay abstraction | `injective_receiver_accept` | 同一 sender occurrence 不能匹配两个不同 accept occurrences | falsified；P2 整体失败点 |
| P2 normal-path executability | Tamarin replay original — fixed two-slot replay abstraction | `normal_single_accept` | 正常 one-send-one-accept 路径可达 | verified exists-trace；不是 universal theorem |
| P2 lifecycle sanity | Tamarin replay original — fixed two-slot replay abstraction | `normal_batch_complete` | 正常 accept 路径可到 batch complete | verified exists-trace；不是 universal theorem |
| P2 attack witness | Tamarin replay original — fixed two-slot replay abstraction | `one_send_two_accepts_exists` | 无 compromise 时 one send 可产生两个 accepts | verified exists-trace |
| P3 under `C_install` unique session installation | 尚无 impact/composition model | 尚无 `InstallSession` / `unique_install` | 命名组合假设下 receiver output 到 fresh local handle 的条件化性质 | not modeled；M2 负责实现 |

P1 与 P2 使用不同 event vocabulary。ProVerif 的
`SendDone(A,B,sid,k)`/`RecvDone(B,A,sid,k)` 不包含 occurrence、slot、batch
或 receiver state；replay 的 `SenderSession`/`ReceiverAccept` 显式包含完整
message 和 receiver-side occurrence context。二者不能自动视为等价事件。

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

当前 Tamarin 模型分为三类职责：V6/V7 关注 state 与 batch lifecycle；
`tamarin/replay/` 关注 original duplicate-input / injectivity；独立 `--diff`
模型提供 preliminary symbolic deniability evidence。

它建模：

```text
receiver state lifecycle
sender / receiver state compromise ordering
receiver-side exception classification
batch slot
batch abort
batch-level state consumption
dynamic AddSlot / SealBatch / ProcessSlot skeleton
Strict Completion Semantics
fixed four-slot terminal lifecycle
fixed two-slot original duplicate-input trace
public-core transcript observational equivalence abstraction
```

它不建模：

```text
full LKEM / EKEM / split-KEM composition
full KDF over K_l, K_k, K_s, sid
real vector traversal
real decapsulation failure condition
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
original BatchReceive replay abstraction 不满足 injective one-send-one-accept；
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
