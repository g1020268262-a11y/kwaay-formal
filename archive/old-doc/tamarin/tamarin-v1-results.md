# Tamarin V1 Results

## 结论

`tamarin/kwaay_splitkem_state_v1.spthy` 已跑通。

V1 在 V0 的基础上，把 "receiver 接受 split-KEM component" 进一步提升为 "receiver 输出 receiver-side key"，并开始分类 receiver-side key 泄露的原因。

一句话：

```text
V0 证明 component origin / state ordering。
V1 证明 attacker-known receiver key 必须落入 unpartnered bad case 或 early state compromise。
```

## V1 和 V0 的区别

### V0 解决的问题

V0 关注：

- receiver 接受的 split-KEM component 从哪里来？
- receiver state 有没有被重复使用？
- forged accept 是否必须由提前 state compromise 解释？

V0 的核心是：

- `ReceiverAcceptsComponent`
- `SenderComponent`
- `CompromiseReceiverState`
- `CompromiseSenderState`

V0 还没有显式表达：

- receiver-side key
- attacker-known key
- partnered / unpartnered receiver session

### V1 新增的问题

V1 关注：

如果 receiver-side key 被攻击者知道，它应该如何分类？

也就是说，V1 不再只看 component 是否被接受，而是把接受后的结果抽象成 receiver-side key：

```text
ReceiverAcceptsComponent -> ReceiverKey
```

然后区分：

- 正常 partnered receiver key
- 攻击者知道的 unpartnered receiver key

## V1 新增内容

V1 新增函数：

- `rkey/5`

含义：

```text
rkey(B,A,rst,cts,Ks)
```

表示 B 根据 accepted component 派生出的抽象 receiver-side key。

V1 新增事件：

| event | meaning |
|---|---|
| `ReceiverKey` | B 输出 receiver-side key |
| `AttackerKnowsKey` | 当前 toy model 中攻击者知道该 receiver-side key |
| `Partnered` | honest component 对应的 receiver key |
| `UnpartneredReceiver` | forged / bad-case receiver key |

注意：

- `AttackerKnowsKey` 是抽象事件，不是完整 Dolev-Yao secrecy proof。
- `Partnered` / `UnpartneredReceiver` 是当前 toy model 分类，不是最终论文定义。

## V1 建模思想

honest accept 产生：

- `ReceiverKey`
- `Partnered`

但不产生：

- `AttackerKnowsKey`

forged accept 产生：

- `ReceiverKey`
- `AttackerKnowsKey`
- `UnpartneredReceiver`

含义：

正常路径下，receiver key 是 partnered。

state compromise bad-case 下，receiver key 可以是 attacker-known，并被分类为 unpartnered receiver bad case。

这对应 ProVerif 中看到的现象：

```text
receiver_skem_sk compromise:
sender-side secrecy true
receiver-side secrecy false

sender_skem_sk compromise:
sender-side secrecy true
receiver-side secrecy false
```

V1 的作用是把这种 receiver-side false 分类为：

- unpartnered bad case
- early state compromise

而不是把它误解为 honest sender-side key 泄露。

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

## 核心 lemma 含义

### receiver_key_known_requires_exception

含义：

如果 receiver-side key 被标记为 attacker-known，那么它必须属于以下之一：

1. `UnpartneredReceiver`；
2. receiver state 在 accept 前泄露；
3. sender state 在 accept 前泄露。

这是 V1 的核心 receiver-side exception candidate。

### partnered_key_not_attacker_known_without_early_compromise

含义：

如果 receiver key 是 partnered，并且 accept 前没有 sender / receiver state compromise，那么该 key 不会 attacker-known。

这说明正常 partnered receiver key 在当前 toy model 中不会泄露。

## 当前意义

V1 证明了：

receiver-side key leakage 不是无条件发生的。

它必须被解释为 unpartnered bad case 或 early state compromise。

这比 V0 多了一层：

```text
V0: component accept 的来源解释。
V1: receiver-side key leakage 的分类解释。
```

## 边界

V1 不是完整 K-Waay 证明。

V1 不建模：

- 完整 KEM
- 完整 KDF
- 签名
- full BatchReceive
- computational KIND
- UNF-1KMA / IND-1BatchCCA computational proof
- 真实 attacker(k) secrecy

## 下一步

进入 V2：Batch slot model。

V2 目标：

把 partnered / unpartnered 从单条 receiver accept 推进到 batch slot 级别。

核心关系从：

```text
sender component <-> receiver accept
```

推进到：

```text
sender session <-> receiver batch slot
```

V2 暂时仍不做 full BatchReceive。
