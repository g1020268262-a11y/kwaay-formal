# Tamarin V6 Results

## 结论

`tamarin/kwaay_splitkem_batch_dynamic_v6.spthy` 已完成 selected lemma verification。

V6 在 V5 的固定两槽 lifecycle 模型基础上，加入 dynamic batch skeleton：

```text
AddSlot -> SealBatch -> ProcessSlot -> Complete / Fail
```

一句话：

```text
V5: 固定两槽 lifecycle
V6: 动态 batch 添加、封口、处理、关闭骨架
```

## V6 和 V5 的区别

### V5 解决的问题

V5 使用固定两槽模型：

```text
Slot1Token
Slot2Token
Slot1DoneFact
Slot2DoneFact
```

V5 证明：

```text
BatchComplete 必须等待两个 slot 都 done。
BatchComplete / BatchFail 后不会再有 slot accept。
```

### V6 新增的问题

V6 不再固定为 Slot1 / Slot2，而是加入更接近 batch 生命周期的结构：

```text
AddSlot
SealBatch
ProcessPendingSlot
CompleteSealedBatch
FailSealedBatch
```

V6 使用：

```text
PendingSlot
DoneSlot
BatchSealedFact
```

表达 slot 生命周期。

## V6 核心设计

V6 的 batch 生命周期是：

```text
CreateBatch
AddSlot
SealBatch
ProcessPendingSlot
CompleteSealedBatch / FailSealedBatch
```

核心 facts / events：

| name | meaning |
|---|---|
| `AddSlotToken` | 限制可添加 slot 数量 |
| `PendingSlot` | 已加入但未处理的 slot |
| `DoneSlot` | 已处理完成的 slot |
| `SealBatchEvent` | batch 被 sealed |
| `BatchSealedFact` | sealed 后允许 process / close |
| `BatchEndToken` | 保证 batch 只能 complete 或 fail 一次 |

注意：

```text
V6 仍是 bounded dynamic skeleton。
```

`AddSlotToken` 当前限制 slot 添加数量，避免无限 AddSlot。

## 验证策略

V6 使用 selected lemma verification，不使用 full `--prove` 作为成功标准。

原因：

```text
Tamarin 对复杂模型可能证明、给反例，也可能不终止。
复杂协议证明通常需要拆分 lemma 和控制 proof search。
```

## Selected lemma 结果

| lemma | result | meaning |
|---|---|---|
| `executable_add_slot` | verified | slot add trace 可达 |
| `executable_seal_batch` | verified | seal batch trace 可达 |
| `executable_process_slot` | verified | process slot trace 可达 |
| `executable_batch_complete` | verified | batch complete trace 可达 |
| `executable_batch_fail` | verified | batch fail trace 可达 |
| `process_requires_slot_added` | verified | process slot 必须来自已 add 的 slot |
| `process_requires_seal` | verified | process slot 必须发生在 seal 之后 |
| `complete_requires_seal` | verified | complete 必须发生在 seal 之后 |
| `fail_requires_seal` | verified | fail 必须发生在 seal 之后 |
| `batch_complete_consumes_state` | verified | complete 会消费 receiver state |
| `batch_fail_consumes_state` | verified | fail 会消费 receiver state |
| `batch_end_token_single_use` | verified | batch 只能结束一次 |
| `batch_fail_complete_exclusive` | verified | 同一 batch 不能既 fail 又 complete |
| `slot_origin_without_early_compromise` | verified | 无提前 compromise 时 accepted slot 有 sender origin |
| `slot_key_known_requires_exception` | verified | attacker-known slot key 必须有 exception 解释 |
| `partnered_slot_key_not_attacker_known_without_early_compromise` | verified | 无提前 compromise 时 partnered slot key 不会 attacker-known |

## 核心 lemma 含义

### `process_requires_slot_added`

```text
任何被处理的 slot 都必须先被 AddSlot 加入 batch。
```

### `process_requires_seal`

```text
slot processing 只能发生在 SealBatch 之后。
```

### `complete_requires_seal`

```text
BatchComplete 只能发生在 SealBatch 之后。
```

### `fail_requires_seal`

```text
BatchFail 只能发生在 SealBatch 之后。
```

### `batch_fail_complete_exclusive`

```text
同一个 batch 不能既 complete 又 fail。
```

## 当前意义

V6 证明了：

```text
动态 batch skeleton 可以表达 AddSlot / SealBatch / ProcessSlot / CloseBatch 的生命周期顺序。
```

这比 V5 多了一层：

```text
V5: 固定两槽 close ordering
V6: 动态 batch 生命周期骨架
```

同时保留了关键性质：

```text
batch complete / fail 消费 receiver state
batch 只能结束一次
slot-level origin / exception 成立
```

## 边界

V6 不是完整 BatchReceive。

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

尤其注意：

```text
V6 不证明 all pending slots done -> complete。
```

这个性质已经在 V5 的固定两槽模型中验证过 bounded 版本。

## 下一步

当前 Tamarin 阶段可以先收束。

下一步建议创建：

```text
docs/tamarin/tamarin-stage-summary.md
```

总结 V0-V6：

```text
V0: component origin / state ordering
V1: receiver-side exception candidate
V2: batch slot
V3: batch abort
V4: batch-level state consumption
V5: fixed two-slot lifecycle
V6: dynamic batch skeleton
```

然后再决定是否进入论文写作整理或 CryptoVerif / computational proof。
