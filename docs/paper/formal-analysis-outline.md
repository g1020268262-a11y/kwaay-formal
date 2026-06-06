# Formal Analysis Outline

## 1. Research Question

本文关注 K-Waay Figure 7 core 的形式化分析边界。

核心问题：

```text
K-Waay Figure 7 core 在 symbolic model 下能证明什么？
哪些性质属于 KIND-style secrecy？
哪些性质属于 explicit agreement / key confirmation？
BatchReceive 的 state / ordering / slot lifecycle 如何建模？
```

本文不声称完整证明 K-Waay computational security。

## 2. Analysis Scope

本文分析对象：

```text
K-Waay Figure 7 core
public-channel symbolic model
split-KEM component
receiver-side BatchReceive lifecycle
```

当前不覆盖：

```text
完整 K-Waay implementation
完整 KDF computational proof
完整 KEM IND-CCA proof
UNF-1KMA computational proof
IND-1BatchCCA computational proof
Theorem 1 advantage bound
```

## 3. Tool Split

本文使用两个 symbolic tools：

```text
ProVerif:
  secrecy / correspondence / agreement boundary

Tamarin:
  state consumption / compromise ordering / BatchReceive slot lifecycle
```

ProVerif 适合快速验证 symbolic secrecy 和 correspondence queries。

Tamarin 适合建模 stateful protocols、事件顺序、linear facts 和 batch lifecycle。

## 4. ProVerif Model

### 4.1 Model Target

ProVerif 阶段分析：

```text
K-Waay Figure 7 core
m = (ct_l, ct_k, ct_s)
single receive approximation
public-channel attacker
```

没有加入：

```text
AEAD
MAC
tag
key confirmation
full BatchReceive
```

### 4.2 Main Queries

ProVerif 查询包括：

```text
SenderKey secrecy
ReceiverKey secrecy
RecvDone ==> SendDone
SenderPrekeyVerified
ReceiverPrekeyVerified
SplitKemAccepted ==> SenderSplitKemComponent
compromise experiments
sender-side exception sanity query
```

### 4.3 Main Findings

ProVerif baseline 结果：

```text
SenderKey secrecy: true
ReceiverKey secrecy: true
RecvDone ==> SendDone: false
SplitKemAccepted ==> SenderSplitKemComponent: true
```

解释：

```text
baseline secrecy 成立；
full-message exact agreement 不成立；
split-KEM component-level authenticity 成立。
```

### 4.4 Agreement Boundary

`RecvDone ==> SendDone` false 不表示 attacker learns key。

它表示：

```text
Figure 7 core 不提供 full-message exact receiver agreement / explicit key confirmation。
```

但 baseline 中：

```text
attacker(k) 仍不成立。
```

因此该结果应解释为：

```text
KIND secrecy 和 explicit agreement 的安全目标边界。
```

而不是：

```text
K-Waay key-recovery break。
```

## 5. Tamarin Model

### 5.1 Why Tamarin

ProVerif 不自然表达：

```text
state consumption
compromise ordering
partnered / unpartnered receiver session
BatchReceive slot
batch abort
batch lifecycle
```

Tamarin 阶段补充这些 state / ordering / lifecycle 语义。

### 5.2 Tamarin Model Evolution

| version | purpose |
|---|---|
| V0 | component origin / state ordering |
| V1 | receiver-side exception candidate |
| V2 | batch slot |
| V3 | batch abort |
| V4 | batch-level state consumption |
| V5 | fixed two-slot lifecycle |
| V6 | dynamic batch skeleton |

### 5.3 V0: Component Origin

V0 验证：

```text
无 early sender/receiver state compromise 时，
accepted split-KEM component 必须有 sender origin。
```

意义：

```text
把 ProVerif 的 split-KEM component authenticity query 转成带时间顺序的 Tamarin lemma。
```

### 5.4 V1: Receiver-side Exception

V1 新增：

```text
ReceiverKey
AttackerKnowsKey
Partnered
UnpartneredReceiver
```

V1 验证：

```text
receiver-side key 如果 attacker-known，
必须属于 unpartnered bad case 或 early sender/receiver state compromise。
```

意义：

```text
把 receiver-side secrecy false 分类为 exception case。
```

### 5.5 V2: Batch Slot

V2 把 receiver accept 坐标化为：

```text
BatchSlot(B,bid,idx,A,cts)
BatchSlotAccept(B,bid,idx,A,rst,cts,Ks)
```

核心关系：

```text
sender component <-> receiver batch slot
```

而不是：

```text
sender session <-> entire receiver session
```

### 5.6 V3: Batch Abort

V3 验证：

```text
slot fail -> BatchFail
BatchFail 和 BatchComplete 互斥
```

意义：

```text
表达 BatchReceive 中任意 slot fail 导致 batch fail 的最小抽象。
```

### 5.7 V4: Batch-level State Consumption

V4 验证：

```text
一个 batch 内多个 slot 可以共享同一个 receiver state；
batch complete / fail 时统一消费 receiver state；
同一个 receiver state 不能被重复最终消费。
```

意义：

```text
receiver state consumption 从 slot-level 移到 batch-level。
```

### 5.8 V5: Fixed Two-slot Lifecycle

V5 使用 bounded two-slot model：

```text
Slot1Token
Slot2Token
Slot1DoneFact
Slot2DoneFact
```

V5 验证：

```text
BatchComplete 必须等待两个 slot 都 done；
BatchComplete / BatchFail 后不会再出现新的 slot accept。
```

意义：

```text
在 bounded model 中验证 batch close ordering。
```

### 5.9 V6: Dynamic Batch Skeleton

V6 新增：

```text
AddSlot
SealBatch
ProcessPendingSlot
CompleteSealedBatch
FailSealedBatch
PendingSlot
DoneSlot
BatchSealedFact
```

V6 selected lemmas 验证：

```text
slot processing 必须来自 added slot；
slot processing 必须发生在 seal 之后；
complete / fail 必须发生在 seal 之后；
batch complete / fail 消费 receiver state；
同一 batch 不能既 complete 又 fail；
slot-level origin / exception 仍成立。
```

意义：

```text
把 V5 的 bounded lifecycle 推进为 AddSlot -> SealBatch -> ProcessSlot -> Complete/Fail 的 dynamic skeleton。
```

## 6. Main Claims

本文可以声称：

```text
1. ProVerif baseline 下 sender/receiver secrecy 成立。
2. ProVerif 显示 Figure 7 core 不满足 full-message exact agreement。
3. 该 agreement false 不等于 key-recovery break。
4. split-KEM component-level authenticity 在 symbolic model 下成立。
5. Tamarin 将 receiver-side key leakage 分类为 unpartnered bad case 或 early state compromise。
6. Tamarin 验证 batch slot origin / exception properties。
7. Tamarin 验证 batch abort、batch-level state consumption 和 lifecycle ordering 的 selected lemmas。
```

## 7. Non-Claims

本文不能声称：

```text
1. 完整 K-Waay 协议已证明安全。
2. computational KIND 已证明。
3. UNF-1KMA / IND-1BatchCCA computational security 已证明。
4. Theorem 1 advantage bound 已形式化完成。
5. Tamarin / ProVerif symbolic result 等价于 CryptoVerif computational proof。
6. V6 证明了任意长度 BatchReceive 的 all pending slots done -> complete。
7. AEAD 是原始 Figure 7 core 的一部分。
```

## 8. Paper Contribution Framing

推荐论文贡献表述：

```text
We provide a symbolic formal analysis of the K-Waay Figure 7 core.
Our ProVerif model separates KIND-style secrecy from explicit agreement.
Our Tamarin models complement ProVerif by analyzing receiver-side state consumption,
compromise ordering, batch-slot pairing, batch abort, and batch lifecycle properties.
```

中文表述：

```text
本文对 K-Waay Figure 7 core 进行 symbolic formal analysis。
ProVerif 部分澄清 KIND-style secrecy 与 explicit agreement 的目标边界。
Tamarin 部分补充分析 state consumption、compromise ordering、receiver-side exception、
BatchReceive slot pairing、batch abort 和 batch lifecycle。
```

## 9. Suggested Paper Structure

### Section 1: Introduction

重点：

```text
K-Waay 使用 split-KEM 和 BatchReceive。
现有论文主要给出 computational theorem。
本文从 symbolic verification 角度分析 Figure 7 core 的安全目标边界。
```

### Section 2: Background

包含：

```text
K-Waay Figure 7 core
split-KEM
BatchReceive
KIND
symbolic verification
ProVerif
Tamarin
```

### Section 3: ProVerif Analysis

写：

```text
model boundary
queries
baseline secrecy
agreement diagnostic
compromise experiments
split-KEM component authenticity
```

### Section 4: Tamarin Analysis

写：

```text
why Tamarin
state model
batch slot model
receiver-side exception
batch abort
state consumption
lifecycle refinement
```

### Section 5: Discussion

写：

```text
KIND secrecy vs explicit agreement
receiver-side exception interpretation
symbolic vs computational proof
AEAD / key confirmation optional branch
```

### Section 6: Limitations and Future Work

写：

```text
CryptoVerif / hand proof
computational KIND
UNF-1KMA
IND-1BatchCCA
advantage bound
full vector BatchReceive
```

## 10. Future Work

后续路线：

```text
1. CryptoVerif / hand computational proof:
   KIND real-or-random game
   KDF 3PRF hybrid
   primitive reduction map
   Theorem 1 advantage bound

2. Stronger BatchReceive model:
   arbitrary-length vector
   all pending slots done -> complete
   real decapsulation fail

3. Optional AEAD / key confirmation branch:
   explicit agreement hardening
   not part of Figure 7 core
```

## 11. Final Position

当前最稳的论文定位：

```text
This work is not a complete computational proof of K-Waay.
It is a symbolic formal analysis that clarifies the boundary between
KIND-style secrecy, explicit agreement, receiver-side exceptions,
and BatchReceive state/lifecycle semantics.
```
