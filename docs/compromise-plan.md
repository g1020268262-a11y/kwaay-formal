# Compromise Plan for K-Waay Core

## 目的

这个文件用于设计 K-Waay Figure 7 core ProVerif public-channel model 中的 compromise / normal bad case 分析。

当前目标不是马上把所有泄露都加入 `.pv`，而是先定义每种泄露的现实含义、预期影响和测试顺序。

## 当前模型边界

- 模型文件: proverif/kwaay-core-public-channel.pv
- 协议目标: 原始 K-Waay Figure 7 core
- 消息结构: m = (ct_l, ct_k, ct_s)
- 不加入 AEAD
- 不加入 MAC
- 不加入 tag
- 不加入 key confirmation
- 暂不加入 full BatchReceive
- 暂不加入 compromise exceptions
- 当前攻击者: public-channel attacker

## 已有 no-compromise 结果

| Query | Result | 说明 |
|---|---|---|
| Q0 HonestRun | reachable | 诚实执行可达 |
| Q1 exact agreement | false | diagnostic / expected false |
| Q1a SenderPrekeyVerified | true | RecvDone 前发生 sender prekey verification |
| Q1b ReceiverPrekeyVerified | true | RecvDone 前发生 receiver prekey verification |
| Q2-S1 SenderKey secrecy | true | sender 侧 session key 未泄露 |
| Q2-S2 ReceiverKey secrecy | true | receiver 侧 session key 未泄露 |

## Compromise events 候选

### C1: CompromiseSigSk(agent)

现实含义：

攻击者获得某个参与方的长期签名私钥 `sig_sk`。

可能影响：

- 攻击者可能伪造该参与方的 prekey bundle 签名。
- 可能影响 authentication / prekey verification。
- 不一定直接泄露已有 session key，除非还能构造相关 KEM secrets。

初始预期：

- structural prekey verification 可能仍然 true，但意义变弱，因为攻击者能伪造签名。
- exact agreement 仍然可能 false。
- session-key secrecy 是否 false 需要实验。

### C2: CompromiseKemSk(agent)

现实含义：

攻击者获得某个参与方的长期 KEM 私钥 `kem_sk`。

可能影响：

- 如果泄露 B 的 `kem_sk`，攻击者可能 decapsulate `ct_l` 得到 `K_l`。
- 但 session key 还依赖 `K_k`、`K_s` 和 `sid`。
- 仅长期 KEM 私钥泄露是否足以得到 full session key，需要实验。

初始预期：

- 如果只泄露 `kem_sk`，session key 不一定立即泄露。
- 如果再结合 receiver ephemeral secret 或 split-KEM state，可能形成正常坏情况。

### C3: CompromiseSenderSkemState(agent)

现实含义：

攻击者获得 sender split-KEM secret state。

可能影响：

- 攻击者可能参与或模拟 sender-side split-KEM computation。
- 可能影响 `K_s`。
- 对 authentication 和 secrecy 的影响需要实验。

初始预期：

- 单独泄露 sender split-KEM state 不一定足以恢复完整 session key。
- 结合其他泄露时可能导致 session key 泄露。

### C4: CompromiseReceiverSkemState(agent)

现实含义：

攻击者获得 receiver split-KEM secret state。

可能影响：

- 攻击者可能 decapsulate `ct_s` 得到 `K_s`。
- 如果再获得其他 KDF 输入，可能恢复 session key。

初始预期：

- 单独泄露 receiver split-KEM state 不一定足以泄露 full session key。
- 与 `kem_sk` 或 `ekem_sk` 泄露组合时需要重点测试。

### C5: CompromiseReceiverEkemState(agent)

现实含义：

攻击者获得 receiver ephemeral KEM secret key `ekem_sk`。

可能影响：

- 攻击者可能 decapsulate `ct_k` 得到 `K_k`。
- 如果再获得其他 KDF 输入，可能恢复 session key。

初始预期：

- 单独泄露 `ekem_sk` 不一定足以恢复完整 session key。
- 结合 `kem_sk` 和 receiver split-KEM state 时可能导致 session key 泄露。

## Normal bad case 初始分类

### NB-001: 所有 KDF 输入都被攻击者获得

如果攻击者获得：

```text
K_l
K_k
K_s
sid
```

那么获得 session key 是正常坏情况。

原因：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

这里 `sid` 通常是公开绑定值，关键是三个 shared secret。

### NB-002: receiver 侧全部 decapsulation secrets 泄露

如果攻击者获得 B 的：

```text
kem_sk
ekem_sk
receiver_skem_sk
```

并且看到公开 message：

```text
m = (ct_l, ct_k, ct_s)
```

则攻击者可能计算：

```text
K_l
K_k
K_s
```

然后得到 receiver-side session key。

这应当分类为正常坏情况。

### NB-003: 仅签名私钥泄露

如果只泄露 `sig_sk`，攻击者可以伪造 prekey signature，但不一定能恢复已有 session key。

如果 ProVerif 显示 session key 泄露，需要检查 trace，不能直接当作正常坏情况。

### NB-004: 单个 KEM secret 泄露

如果只泄露一个 decapsulation secret，例如：

```text
kem_sk
```

或者：

```text
ekem_sk
```

或者：

```text
receiver_skem_sk
```

则攻击者只能得到一个 KDF input。

如果 session key 泄露，需要检查是否模型中 KDF 或 destructor 过强。

## 测试顺序

### Step 1: 只加入事件，不输出 secret

先在 `.pv` 中加入 compromise events，但不真的泄露 secret：

```proverif
event CompromiseSigSk(agent).
event CompromiseKemSk(agent).
event CompromiseSenderSkemState(agent).
event CompromiseReceiverSkemState(agent).
event CompromiseReceiverEkemState(agent).
```

目的：

确认事件不会影响 no-compromise 查询结果。

### Step 2: 单独泄露 sig_sk

加入一个可选 process 输出某方 `sig_sk`，测试：

- prekey verification queries
- sender-side secrecy
- receiver-side secrecy

### Step 3: 单独泄露 kem_sk

输出 B 的 `kem_sk`，测试 session-key secrecy 是否仍然成立。

### Step 4: 单独泄露 receiver ekem_sk

输出 B 的 `ekem_sk`，测试 session-key secrecy 是否仍然成立。

### Step 5: 单独泄露 receiver_skem_sk

输出 B 的 receiver split-KEM secret state，测试 session-key secrecy 是否仍然成立。

### Step 6: 组合泄露

逐步测试组合：

```text
kem_sk + ekem_sk
kem_sk + receiver_skem_sk
ekem_sk + receiver_skem_sk
kem_sk + ekem_sk + receiver_skem_sk
```

预期：

最后一个组合很可能是正常坏情况，因为它覆盖 receiver 侧恢复三个 shared secrets 所需的主要 secret state。

## Query 更新原则

不要一开始就在 secrecy query 里加入复杂 exceptions。

先做两类测试：

1. 原始 secrecy query 在 compromise 下是否 false。
2. 如果 false，读 trace 并记录到 trace-ledger。

之后再考虑把 query 改成带 exception 的形式，例如：

```proverif
attacker(k) && event(SenderKey(A,B,s,k)) && not event(NormalBadCase(...)) ==> false.
```

注意：

具体 ProVerif 语法后续再定，不在本文件中直接实现。

## 记录规则

每次出现 false query，需要记录：

- Trace ID
- Model file
- Query
- Result
- Classification
- Compromise condition
- 是否属于 normal bad case
- 是否需要修改模型
- 是否需要修改 query

记录位置：

```text
docs/trace-ledger.md
docs/secrecy-trace-ledger.md
```

## 当前不做的事情

当前不做：

- full BatchReceive
- Tamarin state model
- CryptoVerif proof
- deniability
- AEAD/MAC/tag/key confirmation
- 改变 Figure 7 core message structure

## 下一步

先从 Step 1 开始：

在 `.pv` 中加入 compromise events 的占位，不输出任何 secret，确认当前所有 no-compromise query 结果保持不变。
