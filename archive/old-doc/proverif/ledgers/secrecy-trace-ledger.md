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

## ST-006: receiver_skem_sk compromise 下的 session key secrecy

### Trace ID

ST-006

### 模型文件

`proverif/kwaay-core-public-channel-leak-rskemsk.pv`

### 实验条件

攻击者获得 B 的 receiver split-KEM secret state：

```text
out(c, receiverSkB)
event CompromiseReceiverSkemState(B)
```

没有泄露：

```text
sig_sk
kem_sk
ekem_sk
sender_skem_sk
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
receiver-side secrecy: false
```

### Classification

sender-side 符号化保密性成立；receiver-side 在 receiver_skem_sk compromise 下失败，分类为 expected receiver-side bad case

### Explanation

在修正长期公钥公开后，单独泄露 B 的 receiver split-KEM secret state `receiverSkB` 不会泄露 honest sender-side session key，因此 sender-side secrecy 仍然为 true。

但是 receiver-side secrecy 变为 false。原因是 public-channel attacker 可以构造 receiver 接收的消息，并且在获得 `receiverSkB` 后控制或恢复 split-KEM 部分的 `K_s`。由于 public-channel 中长期公钥和 prekey 都是公开信息，攻击者可以诱导 receiver 输出一个 unpartnered receiver session key，并且该 key 可被攻击者推出。

因此，这不是 honest sender-side key 泄露，而是 receiver-side unpartnered session 在 receiver_skem_sk compromise 下的 expected bad case。

### Next action

后续在 compromise exception 设计中，需要区分 sender-side key secrecy 和 receiver-side unpartnered session secrecy。

## ST-007: kem_sk + ekem_sk compromise 下的 session key secrecy

### Trace ID

ST-007

### 模型文件

`proverif/kwaay-core-public-channel-leak-kemsk-ekemsk.pv`

### 实验条件

攻击者获得 B 的长期 KEM 私钥和 receiver ephemeral KEM 私钥：

```text
out(c, kskB)
out(c, ekskB)
event CompromiseKemSk(B)
event CompromiseReceiverEkemState(B)
```

没有泄露：

```text
sig_sk
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

在当前模型中，同时泄露 B 的 `kem_sk` 和 `ekem_sk` 不会让攻击者直接获得 session key。

攻击者获得 `kskB` 后，可以从 `ct_l` 恢复 `K_l`。攻击者获得 `ekskB` 后，可以从 `ct_k` 恢复 `K_k`。但是当前 session key 由以下输入派生：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

攻击者如果只获得 `K_l` 和 `K_k`，仍然缺少 `K_s`，因此无法恢复完整 session key。

因此，在当前 Figure 7 core symbolic model 中，`kem_sk + ekem_sk` 组合泄露不破坏 sender-side 或 receiver-side session-key secrecy。

这个结论不等价于完整 computational security proof，也不说明所有组合泄露下仍然安全。

### Next action

下一步测试三个 receiver-side decapsulation secrets 同时泄露：

```text
kskB + ekskB + receiverSkB
```

该组合预计会导致 session-key secrecy 失败，并应分类为 normal bad case。

## ST-008: kem_sk + ekem_sk + receiver_skem_sk compromise 下的 session key secrecy

### Trace ID

ST-008

### 模型文件

`proverif/kwaay-core-public-channel-leak-all-receiver-secrets.pv`

### 实验条件

攻击者获得 B 侧恢复三个 KDF 输入所需的全部 secret：

```text
out(c, kskB)
out(c, ekskB)
out(c, receiverSkB)
event CompromiseKemSk(B)
event CompromiseReceiverEkemState(B)
event CompromiseReceiverSkemState(B)
```

没有泄露：

```text
sig_sk
sender_skem_sk
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
sender-side secrecy: false
receiver-side secrecy: false
```

### Classification

normal bad case

### Explanation

在当前模型中，攻击者同时获得 `kskB`、`ekskB` 和 `receiverSkB` 后，可以恢复 receiver 侧 decapsulation 所需的三个 KDF 输入：

```text
K_l
K_k
K_s
```

由于长期公钥和 sid 相关公开材料也已经在 public channel 中公开，攻击者可以构造完整的：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

因此 sender-side 和 receiver-side session-key secrecy 都变为 false。

这个结果属于 normal bad case，因为攻击者已经获得恢复完整 session key 所需的全部核心 secret。

### Next action

后续需要把该情况作为 compromise exception / normal bad case 记录，而不是作为协议漏洞。

## ST-009: sender-side exception necessity under optional compromise

### Trace ID

ST-009

### 模型文件

`proverif/kwaay-core-public-channel-exception-choice.pv`

### 实验条件

该模型允许攻击者自由选择是否泄露 B 侧三个 decapsulation secrets：

```text
kskB
ekskB
receiverSkB
```

每个泄露通过独立 public-channel 分支触发：

```proverif
event CompromiseKemSk(B);
out(c, kskB)

event CompromiseReceiverEkemState(B);
out(c, ekskB)

event CompromiseReceiverSkemState(B);
out(c, receiverSkB)
```

攻击者可以选择触发任意子集，而不是固定全泄露。

### 查询对象

sender-side exception necessity query。

### 原始 secrecy 结果

```text
sender-side secrecy: false
receiver-side secrecy: false
```

### Exception Query

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k))
  ==> event(CompromiseKemSk(B))
   && event(CompromiseReceiverEkemState(B))
   && event(CompromiseReceiverSkemState(B)).
```

### Exception Result

```text
true
```

### Classification

sender-side secrecy failure requires full receiver-side decapsulation compromise in the current symbolic model

### Explanation

这个实验比 fixed all-leak model 更强。

在 fixed all-leak model 中，三个 compromise event 本来就无条件发生，因此 exception query 为 true 只能说明 full receiver secret compromise 可以解释 key leakage。

而在当前 optional compromise model 中，攻击者可以选择触发 0 个、1 个、2 个或 3 个 compromise。ProVerif 证明：

```text
attacker(k) && event(SenderKey(A,B,s,k))
```

发生时，以下三个事件必须都已经发生：

```text
event(CompromiseKemSk(B))
event(CompromiseReceiverEkemState(B))
event(CompromiseReceiverSkemState(B))
```

因此，在当前 Figure 7 core symbolic model 中，sender-side session key 泄露必须伴随 B 侧三个 decapsulation secrets 全部 compromise。

这个结论仍然不是最终 theorem。它还没有覆盖：

```text
sender_skem_sk compromise
receiver-side exception
partnered / unpartnered session
full BatchReceive
adaptive compromise ordering
computational KIND game
```

### Next action

下一步补充 split-KEM component authenticity query，用组件级 correspondence 替代过强的 full-message exact agreement query。

## ST-010: sender_skem_sk compromise 下的 session key secrecy

### Trace ID

ST-010

### 模型文件

`proverif/kwaay-core-public-channel-leak-sskemsk.pv`

### 实验条件

攻击者获得 A 的 sender split-KEM secret state：

```text
out(c, senderSkA)
event CompromiseSenderSkemState(A)
```

没有泄露：

```text
sig_sk
kem_sk
ekem_sk
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
receiver-side secrecy: false
```

### Classification

sender-side 符号化保密性成立；receiver-side 在 sender_skem_sk compromise 下失败，分类为 expected receiver-side bad case

### Explanation

在当前模型中，单独泄露 A 的 sender split-KEM secret state `senderSkA` 不会泄露 honest sender-side session key，因此 sender-side secrecy 仍然为 true。

但是 receiver-side secrecy 变为 false。原因是 public-channel attacker 可以构造 receiver 接收的消息，并且在获得 `senderSkA` 后构造 split-KEM 组件，使 receiver 输出一个 attacker 也能推出的 unpartnered receiver session key。

因此，这不是 honest sender-side key 泄露，而是 receiver-side unpartnered session 在 sender_skem_sk compromise 下的 expected bad case。

这个结果进一步说明 receiver-side exception 不能只用 `CompromiseReceiverSkemState(B)` 表达，因为 `CompromiseSenderSkemState(A)` 也可能导致 receiver-side secrecy false。

### Next action

后续 receiver-side exception 需要同时考虑 sender_skem_sk compromise、receiver_skem_sk compromise，以及 partnered / unpartnered session 语义。

## 总结

当前 secrecy 查询结果：

| ID | Query target | Result | Classification |
|---|---|---|---|
| ST-001 | SenderKey(A,B,s,k) | true | 符号化保密性成立 |
| ST-002 | ReceiverKey(B,A,s,k) | true | 符号化保密性成立 |
| ST-003 | sig_sk compromise | true | 符号化保密性成立 |
| ST-004 | kem_sk compromise | true | 符号化保密性成立 |
| ST-005 | ekem_sk compromise | true | 符号化保密性成立 |
| ST-006 | receiver_skem_sk compromise | sender true / receiver false | expected receiver-side bad case |
| ST-007 | kem_sk + ekem_sk compromise | true | 符号化保密性成立 |
| ST-008 | kem_sk + ekem_sk + receiver_skem_sk compromise | false | normal bad case |

当前结论：

- sender-side session key secrecy 在当前 symbolic model 下成立。
- receiver-side session key secrecy 在当前 symbolic model 下成立。
- 单独的 `sig_sk` compromise 在当前 symbolic model 下不破坏 sender-side 或 receiver-side session-key secrecy。
- 单独的 `kem_sk` compromise 在当前 symbolic model 下不破坏 sender-side 或 receiver-side session-key secrecy。
- 单独的 `ekem_sk` compromise 在当前 symbolic model 下不破坏 sender-side 或 receiver-side session-key secrecy。
- 单独的 `receiver_skem_sk` compromise 不泄露 honest sender-side key，但 receiver-side unpartnered session secrecy 会失败。
- `kem_sk + ekem_sk` 组合泄露在当前 symbolic model 下不破坏 sender-side 或 receiver-side session-key secrecy。
- `kem_sk + ekem_sk + receiver_skem_sk` 组合泄露导致 sender-side 和 receiver-side session-key secrecy 都失败，分类为 normal bad case。
- exact receiver agreement 仍然作为 diagnostic false 保留。
- 不通过加入 AEAD/MAC/tag/key confirmation 来改变 Figure 7 core。
