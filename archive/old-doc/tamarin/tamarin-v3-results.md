# Tamarin V3 Results

## 结论

`tamarin/kwaay_splitkem_batch_abort_v3.spthy` 已跑通。

V3 在 V2 的 batch slot 模型基础上，加入 batch abort / batch fail 的最小抽象。

一句话：

```text
V2: sender component <-> receiver batch slot
V3: slot fail -> batch fail，且同一个 batch 不能既 fail 又 complete
```

## V3 和 V2 的区别

### V2 解决的问题

V2 关注 batch slot 坐标化：

```text
BatchSlot
BatchSlotAccept
PartneredSlot
UnpartneredReceiverSlot
```

V2 表达的是：

```text
某个 sender component 对应 receiver batch 中的某个 slot。
```

但 V2 还没有表达：

- batch 是否整体成功
- batch 是否因为某个 slot 失败而整体失败

### V3 新增的问题

V3 关注 batch abort：

```text
如果某个 slot fail，则整个 batch fail。
```

因此 V3 新增：

```text
BatchSlotFail
BatchFail
BatchComplete
OpenBatch
ClosedBatch
```

其中：

```text
OpenBatch = batch 尚未 fail / complete
ClosedBatch = batch 已经结束
```

BatchFail 和 BatchComplete 都会结束同一个 OpenBatch，因此同一个 batch 不能同时 fail 和 complete。

## V3 新增内容

V3 新增事件：

```text
BatchSlotFail(B,bid,idx,A,rst,cts)
BatchFail(B,bid,rst)
BatchComplete(B,bid,rst)
```

V3 新增状态 fact：

```text
OpenBatch(B,bid,rst)
ClosedBatch(B,bid,rst)
```

V3 新增 rule：

```text
BatchSlotFail
CompleteOpenBatch
FailOpenBatch
```

注意：

V3 的 fail 是抽象 fail rule。
它不证明真实 KEM decapsulation fail 条件。

## 验证结果

| lemma | result | meaning |
|---|---|---|
| `executable_honest_accept` | verified | honest accept trace 存在 |
| `receiver_state_single_use` | verified | receiver state 不能重复消费 |
| `component_origin_without_early_compromise` | verified | 无提前 compromise 时 accepted component 有 sender origin |
| `forged_accept_requires_early_compromise` | verified | forged accept 需要提前 state compromise |
| `executable_receiver_compromise_bad_case` | verified | receiver state compromise bad case 可达 |
| `executable_sender_compromise_bad_case` | verified | sender state compromise bad case 可达 |
| `executable_partnered_receiver_key` | verified | partnered receiver key trace 存在 |
| `executable_unpartnered_attacker_known_key` | verified | unpartnered attacker-known receiver key bad case 可达 |
| `receiver_key_known_requires_exception` | verified | attacker-known receiver key 必须有 exception 解释 |
| `partnered_key_not_attacker_known_without_early_compromise` | verified | 无提前 compromise 时 partnered key 不会 attacker-known |
| `executable_honest_batch_slot_accept` | verified | honest batch slot accept 可达 |
| `executable_unpartnered_attacker_known_slot` | verified | unpartnered attacker-known slot bad case 可达 |
| `slot_origin_without_early_compromise` | verified | 无提前 compromise 时 accepted slot 有 sender origin |
| `slot_key_known_requires_exception` | verified | attacker-known slot key 必须有 exception 解释 |
| `partnered_slot_key_not_attacker_known_without_early_compromise` | verified | 无提前 compromise 时 partnered slot key 不会 attacker-known |
| `executable_batch_slot_fail` | verified | failed slot trace 可达 |
| `executable_batch_complete` | verified | batch complete trace 可达 |
| `slot_fail_causes_batch_fail` | verified | slot fail 会导致 BatchFail |
| `batch_fail_complete_exclusive` | verified | 同一个 batch 不能既 fail 又 complete |

## 核心 lemma 含义

### slot_fail_causes_batch_fail

含义：

如果某个 batch slot fail，
那么同一个 batch 会产生 BatchFail。

### batch_fail_complete_exclusive

含义：

同一个 B,bid,rst 不能同时出现 BatchFail 和 BatchComplete。

这是 V3 的核心结果。

## 当前意义

V3 证明了：

```text
batch abort 语义可以在 Tamarin 中用 OpenBatch / ClosedBatch 建模。
```

这比 V2 多了一层：

```text
V2: slot 级 accept / key / exception
V3: slot fail 导致 batch fail，且 fail / complete 互斥
```

## 边界

V3 不是完整 BatchReceive。

V3 不建模：

- 完整 batch vector 遍历
- 多个 slot 全部成功才 complete
- batch-level receiver state final consumption
- 真实 KEM decapsulation fail
- 完整 KEM
- 完整 KDF
- 签名
- computational KIND
- UNF-1KMA / IND-1BatchCCA computational proof

## 下一步

进入 V4：batch-level state consumption。

V4 目标：

```text
一个 batch 内多个 slot 共享同一个 receiver state；
batch complete / fail 后统一消费 receiver state。
```

V4 要修正当前 V0-V3 的简化点：

```text
当前是 slot accept 消耗 ReceiverState。
V4 应改成 batch 生命周期结束时消耗 ReceiverState。
```
