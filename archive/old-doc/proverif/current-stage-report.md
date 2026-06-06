# Current Stage Report: K-Waay Figure 7 Core ProVerif Analysis

## 1. 当前分析目标

当前分析对象是 K-Waay Figure 7 core。

当前只分析 core message structure：

```text
m = (ct_l, ct_k, ct_s)
```

当前不加入：

```text
AEAD
MAC
tag
key confirmation
full BatchReceive
Tamarin state model
CryptoVerif computational proof
```

当前分析是 ProVerif symbolic analysis，不等价于论文完整 computational KIND game。

## 2. 当前模型边界

当前 baseline 文件：

```text
proverif/kwaay-core-public-channel.pv
```

攻击者模型：

- public-channel attacker
- 可以拦截、替换、重放消息
- 长期公钥材料显式公开
- 默认 no-compromise
- compromise 实验在独立 experiment files 中完成

长期公钥材料已经显式输出到 public channel：

```text
spkA
kpkA
pkA
spkB
kpkB
pkB
```

这个修正很重要，因为 `sid` 包含长期公钥元组。如果长期公钥没有公开，攻击者无法构造完整 `sid`，secrecy query 会得到过强结果。

## 3. Baseline 结果

baseline 模型：

```text
proverif/kwaay-core-public-channel.pv
```

结果：

```text
HonestRun: reachable
Q1 exact agreement: false
RecvDone ==> SenderPrekeyVerified: true
RecvDone ==> ReceiverPrekeyVerified: true
SenderKey secrecy: true
ReceiverKey secrecy: true
```

解释：

baseline 下 sender-side 和 receiver-side session-key secrecy 都成立。

Q1 exact agreement 为 false，但当前不把它作为协议漏洞，而是作为 diagnostic false。

## 4. Q1 exact agreement 的处理决定

当前 query：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

结果：

```text
false
```

当前决策：

该 query 只作为 diagnostic query 保留，不作为当前 Figure 7 core 的主安全目标。

原因：

该 query 要求 receiver 输出的完整 `sid` 和完整 `session_key` 必须对应某个 honest sender 的完整 `sid` 和完整 `session_key`。

这个要求更接近 explicit full-message agreement。当前 Figure 7 core 故意不加入 AEAD、MAC、tag、key confirmation，因此不应该通过改变 core message structure 来让该 query 变 true。

## 5. Structural authentication checks

当前保留两条 structural authentication checks。

### Sender prekey verification

```proverif
event(RecvDone(B,A,s,k)) ==> event(SenderPrekeyVerified(B,A,sp)).
```

结果：

```text
true
```

### Receiver prekey verification

```proverif
event(RecvDone(B,A,s,k)) ==> event(ReceiverPrekeyVerified(A,B,rp)).
```

结果：

```text
true
```

解释：

这两条 query 检查模型是否保留 Figure 7 core 中 prekey verification 的结构。

它们不要求 full-message exact agreement。

## 6. Session-key secrecy 结果

当前 secrecy queries：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k)) ==> false.

query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

baseline 结果：

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

在 no-compromise public-channel symbolic model 下，攻击者无法推出 sender-side 或 receiver-side session key。

## 6.5 实验结果总览

当前主要实验结果可以汇总如下：

| 模型 | 条件 | SenderKey secrecy | ReceiverKey secrecy | 分类 |
|---|---|---|---|---|
| `kwaay-core-public-channel.pv` | no compromise | true | true | baseline secrecy holds |
| `kwaay-core-public-channel-leak-sigsk.pv` | `sig_sk` | true | true | 不作为 secrecy exception |
| `kwaay-core-public-channel-leak-kemsk.pv` | `kem_sk` | true | true | 只获得 `K_l`，不足以恢复完整 session key |
| `kwaay-core-public-channel-leak-ekemsk.pv` | `ekem_sk` | true | true | 只获得 `K_k`，不足以恢复完整 session key |
| `kwaay-core-public-channel-leak-rskemsk.pv` | `receiver_skem_sk` | true | false | receiver-side expected bad case |
| `kwaay-core-public-channel-leak-sskemsk.pv` | `sender_skem_sk` | true | false | receiver-side expected bad case |
| `kwaay-core-public-channel-leak-kemsk-ekemsk.pv` | `kem_sk + ekem_sk` | true | true | 缺少 `K_s` |
| `kwaay-core-public-channel-leak-all-receiver-secrets.pv` | `kem_sk + ekem_sk + receiver_skem_sk` | false | false | normal bad case |
| `kwaay-core-public-channel-exception-choice.pv` | optional receiver-side compromises | false | false | sender-side exception query 为 true |

该表只总结当前 ProVerif symbolic model 中已经测试过的实验，不代表完整 K-Waay 协议或完整 computational KIND game 的安全结论。

## 7. Compromise 实验结果

### 单独泄露 `sig_sk`

模型：

```text
proverif/kwaay-core-public-channel-leak-sigsk.pv
```

结果：

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

`sig_sk` 泄露主要影响 signature/prekey authentication，不直接提供 `K_l`、`K_k`、`K_s`。

### 单独泄露 `kem_sk`

模型：

```text
proverif/kwaay-core-public-channel-leak-kemsk.pv
```

结果：

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

攻击者最多恢复 `K_l`，但缺少 `K_k` 和 `K_s`。

### 单独泄露 `ekem_sk`

模型：

```text
proverif/kwaay-core-public-channel-leak-ekemsk.pv
```

结果：

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

攻击者最多恢复 `K_k`，但缺少 `K_l` 和 `K_s`。

### 单独泄露 `receiver_skem_sk`

模型：

```text
proverif/kwaay-core-public-channel-leak-rskemsk.pv
```

结果：

```text
sender-side secrecy: true
receiver-side secrecy: false
```

解释：

该结果不是 honest sender-side key 泄露。

更准确地说，`receiverSkB` 泄露后，public-channel attacker 可以诱导 receiver 输出一个 attacker 可知的 unpartnered receiver session key。

### 单独泄露 `sender_skem_sk`

模型：

```text
proverif/kwaay-core-public-channel-leak-sskemsk.pv
```

结果：

```text
sender-side secrecy: true
receiver-side secrecy: false
```

解释：

该结果同样不是 honest sender-side key 泄露。

攻击者获得 `senderSkA` 后，可以构造 receiver 接受的 split-KEM 组件，从而诱导 receiver 输出 attacker 可知的 unpartnered receiver session key。

### 泄露 `kem_sk + ekem_sk`

模型：

```text
proverif/kwaay-core-public-channel-leak-kemsk-ekemsk.pv
```

结果：

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

攻击者可以恢复 `K_l` 和 `K_k`，但仍缺少 `K_s`。

### 泄露 `kem_sk + ekem_sk + receiver_skem_sk`

模型：

```text
proverif/kwaay-core-public-channel-leak-all-receiver-secrets.pv
```

结果：

```text
sender-side secrecy: false
receiver-side secrecy: false
```

解释：

攻击者获得 B 侧恢复三个 KDF 输入所需的全部 secret：

```text
K_l
K_k
K_s
```

因此可以计算：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

该结果属于 normal bad case。

## 8. Sender-side exception sanity check

模型：

```text
proverif/kwaay-core-public-channel-exception-choice.pv
```

该模型是 optional compromise model，攻击者可以选择触发 0 个、1 个、2 个或 3 个 receiver-side decapsulation secret compromise。

query：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k))
  ==> event(CompromiseKemSk(B))
   && event(CompromiseReceiverEkemState(B))
   && event(CompromiseReceiverSkemState(B)).
```

结果：

```text
true
```

解释：

在当前 optional compromise symbolic model 中，如果攻击者知道 sender-side session key，则必须已经发生 B 侧三个 decapsulation secret compromise：

```text
CompromiseKemSk(B)
CompromiseReceiverEkemState(B)
CompromiseReceiverSkemState(B)
```

需要注意，该结论只在当前 optional compromise model 的 compromise 选择空间内成立。该模型允许攻击者选择 B 侧三个 decapsulation secret 的任意子集：

```text
kskB
ekskB
receiverSkB
```

因此，该结果可以说明：在当前模型允许的这些 receiver-side compromise 组合中，sender-side key 泄露必须伴随三者全部 compromise。

但是，该结果不等价于覆盖所有现实 compromise 类型，也不等价于最终 computational theorem。特别是，它仍然没有处理 receiver-side exception、partnered / unpartnered session、full BatchReceive、adaptive compromise ordering 和 computational KIND game。

限制：

该结论仍不是最终 theorem。它尚未覆盖：

```text
receiver-side exception
partnered / unpartnered session
full BatchReceive
adaptive compromise ordering
computational KIND game
```

## 9. Split-KEM component authenticity

模型：

```text
proverif/kwaay-core-public-channel-splitkem-component.pv
```

新增事件：

```proverif
event SenderSplitKemComponent(agent, agent, skem_ct, shared_secret).
event SplitKemAccepted(agent, agent, skem_ct, shared_secret).
```

query：

```proverif
query A: agent, B: agent, cts: skem_ct, Ks: shared_secret;
  event(SplitKemAccepted(B,A,cts,Ks))
  ==> event(SenderSplitKemComponent(A,B,cts,Ks)).
```

结果：

```text
true
```

解释：

该 query 不要求整条消息 `m = (ct_l, ct_k, ct_s)` 或完整 `session_key` exact agreement。

它只检查 receiver 接受的 split-KEM 组件 `ct_s` 和对应 `K_s` 是否由 honest sender 生成过。

该结果说明：虽然 full-message exact agreement 不成立，但 split-KEM component-level authenticity 在当前 Figure 7 core symbolic model 下成立。

需要注意，split-KEM component authenticity 不等于完整协议认证。

该 query 只说明：在当前 symbolic abstraction 中，receiver 接受的 split-KEM 组件 `ct_s` 和对应 `K_s` 可以对应到 honest sender 生成的 split-KEM 组件。

它不能说明：

```text
完整 receiver agreement 成立
完整 session key agreement 成立
完整协议认证成立
computational KIND game 已经被证明
```

因此，该结果应被理解为 component-level authenticity，而不是 full-message explicit authentication。

## 10. 当前可以声称的内容

当前可以谨慎声称：

- 当前 Figure 7 core public-channel symbolic model 中，honest execution 可达。
- baseline 下 sender-side 和 receiver-side session-key secrecy 成立。
- full-message exact receiver agreement 不成立，但该 query 只作为 diagnostic。
- prekey verification structural checks 成立。
- split-KEM component-level authenticity 成立。
- 单独泄露 `sig_sk`、`kem_sk`、`ekem_sk` 不破坏当前 session-key secrecy。
- 单独泄露 `sender_skem_sk` 或 `receiver_skem_sk` 不破坏 honest sender-side secrecy，但会破坏 receiver-side secrecy。
- optional compromise model 下，sender-side key 泄露必须伴随 B 侧三个 decapsulation secret compromise。
- full receiver-side decapsulation compromise 属于 normal bad case。

## 11. 当前不能声称的内容

当前不能声称：

- 已经证明完整 K-Waay 协议安全。
- 已经证明 full BatchReceive 安全。
- 已经证明 computational KIND game。
- 已经证明 deniability。
- 已经证明 explicit full-message agreement。
- 已经完成 receiver-side exception theorem。
- receiver-side secrecy false 等同于 honest sender-side key 泄露。
- ProVerif symbolic result 等价于 CryptoVerif / computational proof。

## 12. 后续方向

短期：

- 稳定当前 `.pv` 文件和 docs。
- 暂停新增文档。
- 不继续随意扩展组合实验。

中期：

- 研究 receiver-side partnered / unpartnered session。
- 研究 split-KEM state compromise 下 receiver-side bad case 分类。
- 考虑用 Tamarin 表达 state、ordering、partnering、BatchReceive。

长期：

- 考虑用 CryptoVerif 或 computational proof 路线靠近论文 KIND game。

### 下一步优先任务

当前 ProVerif core 阶段已经基本稳定。下一步建议按照以下顺序推进：

1. 不再继续随意扩展 ProVerif compromise 组合矩阵。
2. 保持 `RecvDone ==> SendDone` 作为 diagnostic query，不尝试通过改变 Figure 7 core 让它变 true。
3. 继续把 `SenderKey secrecy`、`ReceiverKey secrecy`、prekey structural checks 和 split-KEM component authenticity 作为当前 ProVerif 阶段的主要结果。
4. 如果继续研究 receiver-side 问题，优先研究 partnered / unpartnered session 的定义。
5. 如果需要表达 receiver-side state、ordering、one-time prekey 或 full BatchReceive，优先考虑 Tamarin。
6. 如果需要接近论文 KIND game 的 computational indistinguishability，后续考虑 CryptoVerif 或手工 computational proof。
