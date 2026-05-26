# Exception Query Plan for K-Waay Core

## 目的

这个文件用于设计 K-Waay Figure 7 core ProVerif public-channel model 中的 compromise exception query。

当前我们已经完成 no-compromise secrecy 和若干 compromise 实验。下一步如果要写带 exception 的 secrecy query，需要先明确哪些 compromise 条件属于 normal bad case，哪些 false 仍然值得怀疑。

## 当前模型边界

- 模型文件: proverif/kwaay-core-public-channel.pv
- 协议目标: 原始 K-Waay Figure 7 core
- 消息结构: m = (ct_l, ct_k, ct_s)
- 长期公钥材料 `spkA/kpkA/pkA/spkB/kpkB/pkB` 已显式输出到 public channel
- 不加入 AEAD
- 不加入 MAC
- 不加入 tag
- 不加入 key confirmation
- 暂不加入 full BatchReceive
- 暂不建模 deniability
- 当前攻击者: public-channel attacker plus selected compromise outputs

## 当前已知结果

### No-compromise baseline

```text
sender-side secrecy: true
receiver-side secrecy: true
```

### 单独泄露 `sig_sk`

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

`sig_sk` 影响 prekey signature 的伪造能力，但不直接提供 `K_l`、`K_k`、`K_s`。

### 单独泄露 `kem_sk`

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

攻击者最多恢复 `K_l`，仍缺少 `K_k` 和 `K_s`。

### 单独泄露 `ekem_sk`

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

攻击者最多恢复 `K_k`，仍缺少 `K_l` 和 `K_s`。

### 单独泄露 `receiver_skem_sk`

```text
sender-side secrecy: true
receiver-side secrecy: false
```

解释：

该结果不是 honest sender-side key 泄露。它表示在 `receiverSkB` 泄露后，public-channel attacker 可以诱导 receiver 输出一个攻击者可知的 unpartnered receiver session key。

### 组合泄露 `kem_sk + ekem_sk`

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

攻击者可以恢复 `K_l` 和 `K_k`，但仍缺少 `K_s`。

### 组合泄露 `kem_sk + ekem_sk + receiver_skem_sk`

```text
sender-side secrecy: false
receiver-side secrecy: false
```

解释：

攻击者获得恢复三个 KDF 输入所需的全部 secret，可以计算：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

因此这是 normal bad case。

## Exception 设计原则

### 原则 1: 不把所有 compromise 都一概作为 exception

不是所有 compromise 都应该自动排除。

例如，单独泄露 `sig_sk`、`kem_sk`、`ekem_sk` 时，secrecy 仍然 true，所以不需要作为当前 secrecy exception。

### 原则 2: sender-side 和 receiver-side exception 要分开

当前结果显示：

```text
receiver_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false
```

所以 receiver-side exception 不能简单复制到 sender-side。

### 原则 3: unpartnered receiver session 要单独处理

`receiverSkB` 泄露后，receiver-side secrecy false 的核心不是 honest sender key 泄露，而是 attacker 可以制造 receiver-side unpartnered key。

因此后续 exception query 应该区分：

- sender-side key secrecy
- receiver-side key secrecy
- receiver-side unpartnered session

### 原则 4: full receiver decapsulation compromise 是 normal bad case

当攻击者获得：

```text
kskB
ekskB
receiverSkB
```

它可以恢复：

```text
K_l
K_k
K_s
```

因此 session-key secrecy false 是 normal bad case。

## Candidate exception events

### E1: ReceiverSkemCompromised(agent)

含义：

receiver split-KEM secret state 被泄露。

对应当前 event：

```proverif
event CompromiseReceiverSkemState(agent).
```

用途：

可能作为 receiver-side secrecy 的 exception，特别是 unpartnered receiver session。

### E2: ReceiverAllDecapsulationSecretsCompromised(agent)

含义：

receiver 侧恢复三个 KDF 输入所需的 secret 全部泄露。

可由以下事件组合表示：

```proverif
event(CompromiseKemSk(B))
event(CompromiseReceiverEkemState(B))
event(CompromiseReceiverSkemState(B))
```

用途：

作为 sender-side 和 receiver-side secrecy 的 normal bad case exception。

### E3: SignatureKeyCompromised(agent)

含义：

长期签名私钥泄露。

对应：

```proverif
event CompromiseSigSk(agent).
```

当前用途：

暂不作为 session-key secrecy exception，因为单独泄露 `sig_sk` 没有导致 secrecy false。

## Candidate exception query shapes

注意：以下是查询设计草图，不一定是最终 ProVerif 语法。

### Sender-side secrecy with exception

目标：

如果 sender-side session key 被 attacker 知道，则必须存在完整 receiver decapsulation secret compromise。

草图：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k))
  ==> event(CompromiseKemSk(B))
      && event(CompromiseReceiverEkemState(B))
      && event(CompromiseReceiverSkemState(B)).
```

直觉解释：

sender-side key 泄露只有在 receiver 侧恢复三个 KDF 输入所需 secret 全部泄露时才被视为 normal bad case。

### Receiver-side secrecy with exception

目标：

如果 receiver-side session key 被 attacker 知道，则可能是以下之一：

1. receiver split-KEM state 泄露导致 unpartnered receiver session；
2. receiver 侧三个 decapsulation secrets 全部泄露。

草图：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k))
  ==> event(CompromiseReceiverSkemState(B)).
```

更强版本可能要求区分 partnered 和 unpartnered session，但当前 public-channel core 还没有明确 partnered predicate，因此先不实现。

## 当前暂不直接实现的原因

ProVerif 对 query 中的否定、合取、析取和 exception 写法较敏感。

当前更稳的做法是：

1. 先保留原始 secrecy query；
2. 对 false trace 做 ledger 分类；
3. 再逐步设计带 exception 的 correspondence-style query；
4. 不要一次写复杂的 `not event(...)` 或 OR 条件。

## 实施计划

### Step 1: 明确 normal bad case 事件

先考虑是否新增一个显式事件：

```proverif
event NormalBadCaseReceiverAllSecrets(agent).
```

在测试模型中，当同时泄露：

```text
kskB
ekskB
receiverSkB
```

时触发该事件。

### Step 2: 尝试 sender-side exception query

先只做 sender-side，因为它更清楚：

```proverif
attacker(k) && event(SenderKey(A,B,s,k)) ==> event(NormalBadCaseReceiverAllSecrets(B)).
```

如果该 query 能通过，说明所有 sender-side key 泄露都被 normal bad case 解释。

### Step 3: receiver-side exception query 分开处理

receiver-side 更复杂，因为 `receiverSkB` 单独泄露已经可以导致 unpartnered receiver key 泄露。

需要额外讨论是否引入：

```proverif
event ReceiverUnpartnered(B,A,s,k).
```

或者用现有 Q1-exact false 的 trace 进行分类，而不是强行写一个统一 query。

### Step 4: 不改变 Figure 7 core

任何 exception query 都不能通过改变协议消息结构实现。

禁止加入：

- AEAD
- MAC
- tag
- key confirmation

## 当前开放问题

1. 是否需要显式建模 `Partnered(A,B,s,k)`？
2. receiver-side unpartnered session 是否应该有单独 event？
3. `CompromiseReceiverSkemState(B)` 是否足以作为 receiver-side secrecy exception？
4. sender-side exception 是否只需要 full receiver decapsulation compromise？
5. 这些 exception query 是否应留在 ProVerif 阶段，还是后续交给 Tamarin / CryptoVerif？

## 下一步

先不要直接改 `.pv`。

下一步应该是：

1. 人工确认本文件中的 exception 分类是否合理；
2. 再决定是否新增 `NormalBadCaseReceiverAllSecrets(agent)` 事件；
3. 如果新增，先在专门的 experiment `.pv` 文件中测试，不直接修改 baseline model。
