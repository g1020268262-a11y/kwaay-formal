# Tamarin Stage Summary

## 结论

Tamarin 阶段当前收束到 V6。

当前 Tamarin 主线已经覆盖：

```text
V0: component origin / state ordering
V1: receiver-side exception candidate
V2: batch slot
V3: batch abort
V4: batch-level state consumption
V5: fixed two-slot lifecycle
V6: dynamic batch skeleton
```

推荐论文主线使用：

```text
V6 dynamic batch skeleton
```

并把 V5 作为 bounded lifecycle 补充。

## 为什么需要 Tamarin

ProVerif 阶段已经完成 K-Waay Figure 7 core 的 symbolic analysis。

但 ProVerif 不自然表达：

```text
state consumption
compromise ordering
partnered / unpartnered receiver session
BatchReceive slot
batch abort
batch lifecycle
```

Tamarin 阶段用于补这些状态和时间顺序问题。

## 模型演化

| version | model file | purpose |
|---|---|---|
| V0 | `kwaay_splitkem_state_v0.spthy` | split-KEM component origin / receiver state ordering |
| V1 | `kwaay_splitkem_state_v1.spthy` | receiver-side key / attacker-known key / exception candidate |
| V2 | `kwaay_splitkem_batch_v2.spthy` | receiver accept 坐标化为 batch slot |
| V3 | `kwaay_splitkem_batch_abort_v3.spthy` | slot fail -> batch fail，fail / complete 互斥 |
| V4 | `kwaay_splitkem_batch_state_v4.spthy` | batch-level receiver state consumption |
| V5 | `kwaay_splitkem_batch_lifecycle_v5.spthy` | fixed two-slot lifecycle refinement |
| V6 | `kwaay_splitkem_batch_dynamic_v6.spthy` | AddSlot / SealBatch / ProcessSlot / Complete-Fail dynamic skeleton |

## V0: component origin / state ordering

V0 验证：

```text
receiver accept 的 split-KEM component 在无提前 compromise 时必须有 sender origin。
receiver state 不能被重复消费。
forged accept 必须由 early sender/receiver state compromise 解释。
```

核心意义：

```text
把 ProVerif 中的 component authenticity query 转成带时间顺序的 Tamarin lemma。
```

## V1: receiver-side exception candidate

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

核心意义：

```text
把 ProVerif 中 receiver-side false 分类为 receiver-side exception candidate，
而不是误解为 honest sender-side key 泄露。
```

## V2: batch slot

V2 新增：

```text
bid
idx
BatchSlot
BatchSlotAccept
PartneredSlot
UnpartneredReceiverSlot
```

V2 验证：

```text
sender component <-> receiver batch slot
```

而不是：

```text
sender session <-> entire receiver session
```

核心意义：

```text
开始对齐 K-Waay BatchReceive 的 slot 级语义。
```

## V3: batch abort

V3 新增：

```text
BatchSlotFail
BatchFail
BatchComplete
```

V3 验证：

```text
slot fail 会导致 BatchFail。
同一个 batch 不能既 BatchFail 又 BatchComplete。
```

核心意义：

```text
表达 BatchReceive 中任意 slot fail 导致 batch fail 的最小抽象。
```

## V4: batch-level state consumption

V4 修正 V3 的 slot-level state consumption。

V4 验证：

```text
一个 batch 内多个 slot 可以共享同一个 receiver state。
batch complete / fail 时统一消费 receiver state。
同一个 receiver state 不能被重复最终消费。
slot-level origin / exception 仍成立。
```

核心意义：

```text
receiver state 的消费点从 slot 级移动到 batch 结束级。
```

## V5: fixed two-slot lifecycle

V5 使用固定两槽模型：

```text
Slot1Token
Slot2Token
Slot1DoneFact
Slot2DoneFact
```

V5 验证：

```text
BatchComplete 必须等待两个 slot 都 done。
BatchComplete / BatchFail 后不会再出现新的 slot accept。
```

核心意义：

```text
在 bounded model 中验证 batch close ordering。
```

注意：

```text
固定两槽只是 bounded lifecycle toy model。
不表示 K-Waay batch 只能有两个 slot。
```

## V6: dynamic batch skeleton

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

V6 验证 selected lemmas：

```text
slot add trace 可达
seal batch trace 可达
process slot trace 可达
batch complete / fail trace 可达
process slot 必须来自已 add 的 slot
process slot 必须发生在 seal 之后
complete / fail 必须发生在 seal 之后
batch complete / fail 消费 receiver state
batch 只能结束一次
同一 batch 不能既 complete 又 fail
slot-level origin / exception 仍成立
```

核心意义：

```text
把 V5 的固定两槽 lifecycle 推进为 AddSlot -> SealBatch -> ProcessSlot -> Complete/Fail 的动态 batch 骨架。
```

## 推荐论文使用方式

论文正文建议主推：

```text
V6 dynamic batch skeleton
```

说明它验证：

```text
AddSlot / SealBatch / ProcessSlot / Complete-Fail lifecycle
slot-level origin
receiver-side exception classification
batch close exclusivity
batch complete/fail state consumption
```

V5 可以作为补充：

```text
V5 gives a bounded two-slot validation of all-slots-done before complete and no accept after close.
```

V0-V4 可以作为模型演化和 sanity checks，不需要在正文展开太多。

## 可以声称的结论

可以谨慎声称：

```text
1. Tamarin 补充了 ProVerif 不自然表达的 state / ordering / batch-slot 语义。
2. 无 early sender/receiver state compromise 时，accepted slot 有 sender origin。
3. attacker-known receiver-side slot key 必须有 unpartnered slot 或 early state compromise 解释。
4. BatchFail 和 BatchComplete 互斥。
5. batch complete / fail 会消费 receiver state。
6. V5 bounded model 中，complete 必须等待两个 slot done，close 后无 slot accept。
7. V6 dynamic skeleton 中，slot processing 必须来自 added slot，且必须发生在 seal 之后。
```

## 不能声称的内容

不能声称：

```text
1. 已经证明完整 K-Waay 协议安全。
2. 已经证明 computational KIND。
3. 已经证明 UNF-1KMA / IND-1BatchCCA computational security。
4. 已经建模完整 KEM / KDF / 签名。
5. 已经证明任意长度 BatchReceive 的 all pending slots done -> complete。
6. 已经证明真实 KEM decapsulation fail 条件。
7. Tamarin 结果等价于 CryptoVerif / game-based computational proof。
```

## 当前边界

V6 仍然是 dynamic skeleton，不是完整 BatchReceive。

V6 不建模：

```text
任意长度 batch
真实 counter +1 / -1
所有 PendingSlot 都 Done 后才能 complete
PendingSlot 不存在性判断
完整 vector traversal
真实 KEM decapsulation fail
完整 KEM
完整 KDF
签名
computational KIND
UNF-1KMA / IND-1BatchCCA computational proof
```

## 下一步

Tamarin 阶段可以先收束。

后续方向：

```text
1. 论文整理：
   把 ProVerif + Tamarin 的结论整理成 formal analysis section。

2. CryptoVerif / hand proof：
   处理 computational KIND、KDF hybrid、UNF-1KMA、IND-1BatchCCA、advantage bound。

3. 可选扩展：
   AEAD / key confirmation 分支只作为 optional hardening，不覆盖 Figure 7 core 主线。
```
