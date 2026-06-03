# Tamarin V1 Results

## 结论

`tamarin/kwaay_splitkem_state_v1.spthy` 已跑通。

V1 在 V0 基础上加入 receiver-side key、attacker-known key、partnered / unpartnered 分类，并验证 receiver-side exception candidate。

## V1 新增内容

V1 新增：

- `rkey/5`
- `ReceiverKey`
- `AttackerKnowsKey`
- `Partnered`
- `UnpartneredReceiver`
- receiver-side exception candidate lemma

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

## 核心结论

V1 证明：

- receiver-side key 如果 attacker-known，必须属于 unpartnered bad case 或 early state compromise；
- partnered receiver key 在无提前 sender / receiver state compromise 时不会 attacker-known；
- receiver-side exception candidate 在当前 toy model 中成立。

## 边界

V1 不是完整 K-Waay 证明。

V1 不建模：

- 完整 KEM；
- 完整 KDF；
- 签名；
- full BatchReceive；
- computational KIND；
- UNF-1KMA / IND-1BatchCCA computational proof。

## 下一步

进入 V2：Batch slot model。

V2 目标：

- 建模 receiver batch slot；
- 表达 `sender session <-> receiver batch component`；
- 不直接建完整 BatchReceive。
