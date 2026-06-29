# Tamarin V2 Results

## 结论

`tamarin/kwaay_splitkem_batch_v2.spthy` 已跑通。

V2 在 V1 基础上加入 batch slot 坐标，将 receiver accept 从 single accept 级别推进到 batch slot 级别。

一句话：

```text
V1: sender component <-> receiver accept
V2: sender component <-> receiver batch slot
```

## V2 和 V1 的区别

### V1 解决的问题

V1 关注 receiver-side key 泄露分类：

- `ReceiverKey`
- `AttackerKnowsKey`
- `Partnered`
- `UnpartneredReceiver`

V1 的语义仍然是 single accept：

一个 receiver accept 对应一个 receiver-side key。

### V2 新增的问题

V2 关注 batch slot 级别的配对：

一个 receiver batch 中的某个 slot 对应一个 sender component。

因此 V2 新增：

- `bid`
- `idx`
- `BatchCreated`
- `BatchSlot`
- `BatchSlotAccept`
- `PartneredSlot`
- `UnpartneredReceiverSlot`

其中：

- `bid` = batch identifier，表示一次 batch receive 实例
- `idx` = slot identifier，表示该 batch 中的某个位置

`bid` 不是 slot 数量。

## V2 新增内容

V2 将 V1 的 receiver-side key 事件扩展为带 batch 坐标：

```text
ReceiverKey(B,A,bid,idx,rst,cts,Ks,k)
```

V2 将 partnered / unpartnered 分类扩展为 slot 级别：

```text
PartneredSlot(A,B,bid,idx,rst,cts,Ks)
UnpartneredReceiverSlot(B,A,bid,idx,rst,cts,Ks,k)
```

V2 新增 batch slot 事件：

```text
BatchCreated(B,bid,rst)
BatchSlot(B,bid,idx,A,cts)
BatchSlotAccept(B,bid,idx,A,rst,cts,Ks)
```

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

## 核心 lemma 含义

### slot_origin_without_early_compromise

含义：

如果某个 batch slot 被接受，并且 accept 前没有 sender / receiver state compromise，那么该 slot 的 component 必须有 sender origin。

### slot_key_known_requires_exception

含义：

如果某个 batch slot 的 receiver-side key 被 attacker-known，那么它必须属于以下之一：

1. `UnpartneredReceiverSlot`；
2. receiver state 在 accept 前泄露；
3. sender state 在 accept 前泄露。

### partnered_slot_key_not_attacker_known_without_early_compromise

含义：

如果某个 slot 是 partnered slot，并且 accept 前没有 sender / receiver state compromise，那么该 slot 的 key 不会 attacker-known。

## 当前意义

V2 证明了：

receiver-side exception candidate 可以从 single accept 级别提升到 batch slot 级别。

这比 V1 多了一层：

```text
V1: receiver-side key leakage 的分类解释。
V2: receiver-side slot key leakage 的分类解释。
```

V2 对应论文中的核心直觉：

```text
sender session / component <-> receiver batch component
```

而不是：

```text
sender session <-> entire receiver session
```

## 边界

V2 不是完整 BatchReceive。

V2 不建模：

- batch abort
- 多个 slot 同时完成
- batch-level state consumption
- 完整 vector semantics
- 完整 KEM
- 完整 KDF
- 签名
- computational KIND
- UNF-1KMA / IND-1BatchCCA computational proof

## 下一步

进入 V3：batch abort / batch fail 语义设计。

V3 目标：

表达如果 batch 中某个 slot fail，则整个 batch fail。

V3 暂时仍不做完整 computational proof。
