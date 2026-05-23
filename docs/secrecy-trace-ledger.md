# Secrecy Trace Ledger

## 目的

这个文件用于记录当前 K-Waay Figure 7 core ProVerif public-channel 模型中的 session-key secrecy 查询结果。

这里的 secrecy query 是 ProVerif symbolic model 下的近似分析，不等价于论文中的完整 computational KIND game。

## 当前模型边界

- 模型文件: proverif/kwaay-core-public-channel.pv
- 协议目标: 原始 K-Waay Figure 7 core
- 消息结构: m = (ct_l, ct_k, ct_s)
- 不加入 AEAD
- 不加入 MAC
- 不加入 tag
- 不加入 key confirmation
- 不加入 full BatchReceive
- 当前没有 compromise exceptions

## ST-001: sender-side session key secrecy

### Trace ID

ST-001

### 查询对象

sender 侧由 `SenderKey(A,B,s,k)` 标记的 session key。

### Query

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k)) ==> false.
```

### Result

```text
true
```

### Classification

符号化保密性成立

### Explanation

在当前 no-compromise public-channel 模型下，ProVerif 没有找到攻击者同时满足以下两个条件的 trace：

```text
event(SenderKey(A,B,s,k))
attacker(k)
```

因此，当前 symbolic model 中 sender 侧生成的 session key 没有泄露给攻击者。

这个结论只适用于当前 Figure 7 core symbolic model，不等价于完整 computational key indistinguishability 证明。

### Next action

后续如果加入 compromise events，需要重新测试 sender-side secrecy，并区分哪些泄露属于正常坏情况。

## ST-002: receiver-side session key secrecy

### Trace ID

ST-002

### 查询对象

receiver 侧由 `ReceiverKey(B,A,s,k)` 标记的 session key。

### Query

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

### Result

```text
true
```

### Classification

符号化保密性成立

### Explanation

在当前 no-compromise public-channel 模型下，即使存在 unpartnered receiver session，ProVerif 仍然没有找到攻击者同时满足以下两个条件的 trace：

```text
event(ReceiverKey(B,A,s,k))
attacker(k)
```

因此，当前 symbolic model 中 receiver 侧输出的 session key 也没有泄露给攻击者。

这个结果说明：exact receiver agreement 的 false 并不自动意味着 receiver-side secrecy 失败。

### Next action

后续需要继续研究 receiver-side unpartnered session 与论文 KIND game 中 unpartnered receiver case 的关系。

## ST-003: sig_sk compromise 下的 session key secrecy

### Trace ID

ST-003

### 模型文件

`proverif/kwaay-core-public-channel-leak-sigsk.pv`

### 实验条件

攻击者获得 A 和 B 的长期签名私钥：

```text
out(c, sskA)
out(c, sskB)
event CompromiseSigSk(A)
event CompromiseSigSk(B)
```

没有泄露：

```text
kem_sk
ekem_sk
sender_skem_sk
receiver_skem_sk
```

### 查询对象

sender-side 和 receiver-side session key secrecy。

### Query

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k)) ==> false.

query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

### Result

```text
sender-side secrecy: true
receiver-side secrecy: true
```

### Classification

符号化保密性成立

### Explanation

在当前模型中，单独泄露长期签名私钥 `sig_sk` 不会让攻击者直接获得 session key。

这符合当前直觉：`sig_sk` 主要影响 prekey signature 的伪造能力和认证语义，但 session key 由以下输入派生：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

攻击者如果只获得 `sig_sk`，仍然没有直接获得 `K_l`、`K_k`、`K_s`。

因此，在当前 Figure 7 core symbolic model 中，单独的 `sig_sk` compromise 不破坏 sender-side 或 receiver-side session-key secrecy。

这个结论不等价于完整 computational security proof，也不说明 authentication 在 `sig_sk` 泄露后仍然保持强安全性。

### Next action

下一步测试单独泄露长期 KEM 私钥 `kem_sk` 对 session-key secrecy 的影响。

## ST-004: kem_sk compromise 下的 session key secrecy

### Trace ID

ST-004

### 模型文件

`proverif/kwaay-core-public-channel-leak-kemsk.pv`

### 实验条件

攻击者获得 B 的长期 KEM 私钥：

```text
out(c, kskB)
event CompromiseKemSk(B)
```

没有泄露：

```text
sig_sk
ekem_sk
sender_skem_sk
receiver_skem_sk
```

### 查询对象

sender-side 和 receiver-side session key secrecy。

### Query

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k)) ==> false.

query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

### Result

```text
sender-side secrecy: true
receiver-side secrecy: true
```

### Classification

符号化保密性成立

### Explanation

在当前模型中，单独泄露 B 的长期 KEM 私钥 `kem_sk` 不会让攻击者直接获得 session key。

攻击者获得 `kskB` 后，理论上可以从 `ct_l` 恢复 `K_l`。但是当前 session key 由以下输入派生：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

攻击者如果只获得 `K_l`，仍然缺少 `K_k` 和 `K_s`，因此无法恢复完整 session key。

因此，在当前 Figure 7 core symbolic model 中，单独的 `kem_sk` compromise 不破坏 sender-side 或 receiver-side session-key secrecy。

这个结论不等价于完整 computational security proof，也不说明更多组合泄露下仍然安全。

### Next action

下一步测试单独泄露 receiver ephemeral KEM 私钥 `ekem_sk` 对 session-key secrecy 的影响。

## ST-005: ekem_sk compromise 下的 session key secrecy

### Trace ID

ST-005

### 模型文件

`proverif/kwaay-core-public-channel-leak-ekemsk.pv`

### 实验条件

攻击者获得 B 的 receiver ephemeral KEM 私钥：

```text
out(c, ekskB)
event CompromiseReceiverEkemState(B)
```

没有泄露：

```text
sig_sk
kem_sk
sender_skem_sk
receiver_skem_sk
```

### 查询对象

sender-side 和 receiver-side session key secrecy。

### Query

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k)) ==> false.

query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

### Result

```text
sender-side secrecy: true
receiver-side secrecy: true
```

### Classification

符号化保密性成立

### Explanation

在当前模型中，单独泄露 B 的 receiver ephemeral KEM 私钥 `ekem_sk` 不会让攻击者直接获得 session key。

攻击者获得 `ekskB` 后，理论上可以从 `ct_k` 恢复 `K_k`。但是当前 session key 由以下输入派生：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

攻击者如果只获得 `K_k`，仍然缺少 `K_l` 和 `K_s`，因此无法恢复完整 session key。

因此，在当前 Figure 7 core symbolic model 中，单独的 `ekem_sk` compromise 不破坏 sender-side 或 receiver-side session-key secrecy。

这个结论不等价于完整 computational security proof，也不说明更多组合泄露下仍然安全。

### Next action

下一步测试单独泄露 receiver split-KEM secret state `receiver_skem_sk` 对 session-key secrecy 的影响。

## 总结

当前 secrecy 查询结果：

| ID | Query target | Result | Classification |
|---|---|---|---|
| ST-001 | SenderKey(A,B,s,k) | true | 符号化保密性成立 |
| ST-002 | ReceiverKey(B,A,s,k) | true | 符号化保密性成立 |
| ST-003 | sig_sk compromise | true | 符号化保密性成立 |
| ST-004 | kem_sk compromise | true | 符号化保密性成立 |
| ST-005 | ekem_sk compromise | true | 符号化保密性成立 |

当前结论：

- sender-side session key secrecy 在当前 symbolic model 下成立。
- receiver-side session key secrecy 在当前 symbolic model 下成立。
- 单独的 `sig_sk` compromise 在当前 symbolic model 下不破坏 sender-side 或 receiver-side session-key secrecy。
- 单独的 `kem_sk` compromise 在当前 symbolic model 下不破坏 sender-side 或 receiver-side session-key secrecy。
- 单独的 `ekem_sk` compromise 在当前 symbolic model 下不破坏 sender-side 或 receiver-side session-key secrecy。
- exact receiver agreement 仍然作为 diagnostic false 保留。
- 不通过加入 AEAD/MAC/tag/key confirmation 来改变 Figure 7 core。
