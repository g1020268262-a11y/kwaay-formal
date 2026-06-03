# Tamarin V0 Results

## 结论

`tamarin/kwaay_splitkem_state_v0.spthy` 已跑通。

V0 只验证 split-KEM component、receiver state lifecycle 和 compromise ordering 的最小骨架。

## 模型边界

V0 建模：

- opaque split-KEM component；
- `ComponentKey(A,B,rst,cts,Ks)` 抽象 decapsulation relation；
- receiver state linear consumption；
- receiver/sender state compromise；
- forged receiver accept bad cases。

V0 不建模：

- 完整 K-Waay；
- 完整 KEM；
- 完整 KDF；
- 签名；
- full BatchReceive；
- computational KIND；
- UNF-1KMA / IND-1BatchCCA computational proof。

## 验证结果

| lemma | result | meaning |
|---|---|---|
| `executable_honest_accept` | verified | honest receiver accept trace 存在 |
| `receiver_state_single_use` | verified | 同一个 receiver state 不能被消费两次 |
| `component_origin_without_early_compromise` | verified | 无提前 state compromise 时，accepted component 必须有 sender origin |
| `forged_accept_requires_early_compromise` | verified | forged accept 必须有提前 receiver/sender state compromise |
| `executable_receiver_compromise_bad_case` | verified | receiver state compromise bad case 可达 |
| `executable_sender_compromise_bad_case` | verified | sender state compromise bad case 可达 |

## 当前意义

V0 证明了：

- receiver state consumption 可以用 Tamarin 表达；
- compromise before accept 可以用时间顺序表达；
- split-KEM component origin 可以做成带时间条件的 lemma；
- sender/receiver state compromise 下的 forged receiver accept 可以作为 bad case 建模。

## 下一步

进入 V1：

- 加 `ReceiverKey`；
- 加 `AttackerKnowsKey` 抽象事件；
- 加 `Partnered` / `UnpartneredReceiver` 候选事件；
- 开始设计 receiver-side exception candidate。

V1 仍然不做 full BatchReceive。
