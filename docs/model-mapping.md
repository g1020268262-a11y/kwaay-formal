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

Tamarin:
  split-KEM component
  receiver state
  batch slot
  batch abort
  batch-level state consumption
  dynamic batch skeleton
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
| AEAD / key confirmation | separate branch only | 当前 core model 中不建模 | 可选扩展 |
| deniability | 尚未建模 | 尚未建模 | 后续工作 |
| computational KIND | 未建模 | 未建模 | 后续 CryptoVerif / hand proof |

## 安全目标映射

| 目标 / 性质 | 工具 | query / lemma | 含义 | 限制 |
|---|---|---|---|---|
| sender-side secrecy | ProVerif | `not attacker(k)` with `SenderKey` | baseline 下攻击者不能推出 sender-side key | symbolic only |
| receiver-side secrecy | ProVerif | `not attacker(k)` with `ReceiverKey` | baseline 下攻击者不能推出 receiver-side key | symbolic only |
| full-message exact agreement | ProVerif | `RecvDone ==> SendDone` | receiver accept 必须存在 exact sender partner | 当前 core 中为 false |
| split-KEM component authenticity | ProVerif | `SplitKemAccepted ==> SenderSplitKemComponent` | accepted split-KEM component 有 sender origin | component-level only |
| receiver-side exception | Tamarin | `slot_key_known_requires_exception` | attacker-known receiver key 必须有 unpartnered / early compromise 解释 | 抽象模型 |
| batch slot origin | Tamarin | `slot_origin_without_early_compromise` | 无 early compromise 时 accepted slot 有 sender origin | symbolic abstraction |
| batch abort | Tamarin | `batch_fail_complete_exclusive` | 同一 batch 不能同时 fail 和 complete | abstract fail model |
| batch-level state consumption | Tamarin | `batch_complete_consumes_state`, `batch_fail_consumes_state` | receiver state 在 batch close 时消费 | symbolic lifecycle |
| dynamic batch lifecycle | Tamarin | `process_requires_slot_added`, `process_requires_seal` | processed slot 必须先 add，且 batch 必须先 seal | 不证明 all pending slots done |

## ProVerif 模型边界

当前 ProVerif 模型是 K-Waay Figure 7 core 的 no-batch / single-receive symbolic abstraction。

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
deniability
```

## Tamarin 模型边界

当前 Tamarin 模型主要关注 state 和 batch semantics。

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
```

它不建模：

```text
full LKEM / EKEM / split-KEM composition
full KDF over K_l, K_k, K_s, sid
real vector traversal
real decapsulation failure condition
computational security
deniability
```

## 当前主要解释

当前形式化分析支持下面这个解释：

```text
K-Waay Figure 7 core 可以满足 symbolic secrecy-style properties，
但不满足 full-message exact receiver agreement。
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
```

## WP1 后续任务

完成本文件后，下一步需要冻结最终入口模型：

```text
proverif/kwaay_core_final.pv
tamarin/kwaay_batch_state_final.spthy
```

这些文件应作为论文和 artifact README 中引用的主模型。

同时保留历史版本：

```text
tamarin/versions/
proverif/experiments/
```

历史版本用于说明模型演化，但论文正文不应把所有版本都作为主结果。
