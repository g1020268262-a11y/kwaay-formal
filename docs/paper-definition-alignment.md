# Paper Definition Alignment

## 目的

这个文件记录 K-Waay 论文定义与当前 ProVerif symbolic analysis query 之间的对应关系。

当前目标不是给出完整论文证明，而是明确：

- 哪些 ProVerif query 可以作为论文安全目标的 symbolic proxy；
- 哪些 query 只是 diagnostic；
- 哪些定义当前没有完整建模；
- 哪些问题后续更适合 Tamarin / CryptoVerif / 手工证明。

## 1. 当前模型边界

当前 ProVerif 分析对象是 K-Waay Figure 7 core。

当前消息结构保持：

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
```

长期公钥材料已显式公开：

```text
spkA
kpkA
pkA
spkB
kpkB
pkB
```

当前模型是 public-channel symbolic model。攻击者可以拦截、替换、重放消息。

当前分析不是完整 computational KIND proof。

## 2. 核心对齐结论

### 2.1 KIND 不等于 full-message exact agreement

当前 diagnostic query：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

当前结果：

```text
false
```

该 query 要求 receiver 输出的完整 `sid` 和完整 `session_key` 必须对应某个 honest sender 输出的完整 `sid` 和完整 `session_key`。

这更接近 full-message exact agreement，不是 KIND 的主目标。

KIND 的核心是：

```text
对于 fresh TEST session，攻击者不能区分真实 session key 和随机 key。
```

因此，`RecvDone ==> SendDone` 保留为 diagnostic query，不作为当前 Figure 7 core 的主安全目标。

### 2.2 KDF 三输入结构与 Figure 7 core 对齐

当前 ProVerif 模型中：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

其中：

```text
K_l: long-term KEM shared secret
K_k: ephemeral KEM shared secret
K_s: split-KEM shared secret
```

这与 Figure 7 core 中 long-term KEM、ephemeral KEM、split-KEM 三个 shared secret 共同进入 key derivation 的结构对齐。

注意：论文图示和当前文档中的 `K_l / K_k / K_s` 顺序可能不同。只要 ProVerif sender 和 receiver 使用相同顺序，符号模型内部是一致的。后续文字尽量写成：

```text
K_l / K_k / K_s 三个 KDF 输入
```

避免强调某个顺序。

### 2.3 SenderKey / ReceiverKey secrecy 是 KIND 的 symbolic proxy

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

这可以作为 KIND 的 symbolic proxy：

```text
attacker 无法推出 SenderKey / ReceiverKey 标记的 session key
```

但它不等价于 computational real-or-random indistinguishability，也不等价于完整 KIND theorem。

### 2.4 Receiver-side secrecy 必须和 sender-side secrecy 分开解释

在以下 compromise 条件下：

```text
receiver_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false

sender_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false
```

这说明 receiver-side secrecy false 不等于 honest sender-side key 泄露。

更准确地说，它们是 split-KEM state compromise 下的 receiver-side unpartnered session bad case 候选。

因此，当前不写统一 receiver-side exception query。

暂不采用：

```proverif
attacker(k) && event(ReceiverKey(B,A,s,k))
==> event(CompromiseReceiverSkemState(B)).
```

原因是该 query 太粗，且会漏掉 `CompromiseSenderSkemState(A)` 导致的 receiver-side false。

### 2.5 Sender-side exception sanity check 当前成立

当前 optional compromise model：

```text
proverif/kwaay-core-public-channel-exception-choice.pv
```

当前 query：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k))
  ==> event(CompromiseKemSk(B))
   && event(CompromiseReceiverEkemState(B))
   && event(CompromiseReceiverSkemState(B)).
```

当前结果：

```text
true
```

含义：

在当前 optional compromise symbolic model 中，如果 attacker 知道 sender-side session key，则必须已经发生 B 侧三个 decapsulation secret compromise。

限制：

该结果只在当前 symbolic compromise 选择空间内成立，不是最终 computational theorem。它尚未覆盖：

```text
receiver-side exception
partnered / unpartnered session
full BatchReceive
adaptive compromise ordering
computational KIND game
```

## 3. KIND oracle / freshness 对齐

论文 KIND game 不是简单 secrecy query。它包含：

```text
EXEC
LTK
REGISTER
STATE
KEY
TEST
freshness predicates
partnering identifiers
```

当前 ProVerif 只做部分 symbolic approximation。

| KIND oracle / 机制 | 论文语义 | 当前 ProVerif 近似 | 当前是否完整 |
|---|---|---|---|
| `EXEC` | 攻击者驱动协议执行、注入消息 | public channel `c` | 部分对齐 |
| `LTK` | 长期密钥泄露 | `sig_sk` / `kem_sk` compromise files | 部分对齐 |
| `REGISTER` | 注册恶意公钥 | 当前未建模 | 未建模 |
| `STATE` | session state exposure | `sender_skem_sk` / `receiver_skem_sk` / `ekem_sk` compromise files | 部分对齐 |
| `KEY` | session key exposure | 当前没有完整 KEY oracle | 未完整建模 |
| `TEST` | real key vs random key | 当前只做 symbolic secrecy | 未建模 |
| freshness predicates | 排除 trivial attacks | 当前用 exception / normal bad case 分类近似 | 未完整建模 |
| partnering identifiers | 定义 sender / receiver session 如何匹配 | 当前未完整建模 partnered / unpartnered | 未完整建模 |
| receiver vector identifiers | 支持 BatchReceive vector semantics | 当前是 single receive approximation | 未建模 |

当前可以说：

```text
SenderKey secrecy / ReceiverKey secrecy 是 KIND 的 symbolic proxy。
```

当前不能说：

```text
已经证明 K-Waay 满足 computational KIND。
```

## 4. Partner / key identifiers 与 BatchReceive

论文中的 partner identifiers 和 key identifiers 用于定义 session 之间如何匹配。

直观上：

```text
partner identifier = 当前 session 认为自己在和谁通信
key identifier     = 当前 session key 绑定哪份 transcript / 哪个 component
```

普通一对一 AKE 中，这些 identifier 可以近似看作标量。

但 K-Waay 支持 `BatchReceive`。receiver 可以一次处理一组输入消息，并输出一组 session keys。

例如：

```text
message from A -> k1
message from C -> k2
message from D -> k3
```

此时 receiver 的 partner identifiers 可以理解为：

```text
[A, C, D]
```

receiver 的 key identifiers 可以理解为：

```text
[sid_1, sid_2, sid_3]
```

因此完整语义更接近：

```text
sender session <-> receiver batch component
```

而不是：

```text
entire receiver session <-> one sender session
```

这进一步解释了为什么：

```proverif
event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k))
```

对当前 Figure 7 core 来说过强。

## 5. Split-KEM assumptions 与当前 ProVerif proxy

K-Waay split-KEM 层面依赖两个核心性质：

```text
UNF-1KMA
IND-1BatchCCA
```

### 5.1 UNF-1KMA

`UNF-1KMA` 是 split-KEM 的组件级不可伪造性游戏。

它的直觉是：

```text
攻击者即使看过一个合法 split-KEM ciphertext 和对应 key，
也不能伪造另一个新的 ciphertext，
使对应 honest decapsulation party 成功 decapsulate。
```

注意：`UNF-1KMA` 不能和 deniability game 混淆。

在 `UNF-1KMA` game 中，攻击者看到：

```text
pkA
pkB
ct
KB
```

攻击者不知道 honest decapsulation party 的 secret key。

而 deniability game 中，攻击者可能会得到：

```text
pkA
pkB
skA
K
ct
```

因此：

```text
UNF-1KMA adversary 不知道 skA。
deniability game adversary 可以知道 skA。
```

当前 ProVerif symbolic proxy 是：

```proverif
query A: agent, B: agent, cts: skem_ct, Ks: shared_secret;
  event(SplitKemAccepted(B,A,cts,Ks))
  ==> event(SenderSplitKemComponent(A,B,cts,Ks)).
```

当前结果：

```text
true
```

该 query 说明：

```text
如果 receiver 接受了 alleged from A 的 split-KEM component cts，并得到 Ks，
那么 honest sender A 之前确实生成过同一个 cts 和 Ks。
```

因此，它可以作为 UNF-1KMA 直觉的 symbolic proxy。

限制：

```text
当前 query 是 symbolic correspondence，不是 computational UNF-1KMA proof。
```

### 5.2 IND-1BatchCCA

`IND-1BatchCCA` 是 split-KEM 的 computational secrecy game。

它的直觉是：

```text
即使攻击者获得一次 batch decapsulation 能力，
也不能区分 challenge split-KEM key 是真实 key 还是随机 key。
```

其中 `1Batch` 表示：

```text
攻击者最多获得一次 batch decapsulation query。
```

batch decapsulation 的特点是：

```text
如果 batch 中任意一个 decapsulation 失败，整个 batch 返回 bottom。
```

当前 ProVerif 没有完整建模 `IND-1BatchCCA`。当前模型只是 single receive approximation：

```proverif
in(c, mFromNet);
let ctLFromNet = get_lkem_ct(mFromNet) in
let ctEFromNet = get_ekem_ct(mFromNet) in
let ctSFromNet = get_skem_ct(mFromNet) in
...
event RecvDone(B,A,sidBA,kRecv);
event ReceiverKey(B,A,sidBA,kRecv);
```

当前没有完整表达：

```text
batch input vector
batch output vector
batch slot index
receiver vector identifiers
batch abort behavior
state consumption
one-time prekey semantics
```

因此，当前不能说：

```text
ProVerif 已经证明 split-KEM 满足 IND-1BatchCCA。
```

## 6. Theorem 1 proof sketch 对齐摘要

Theorem 1 proof sketch 不需要在当前文档中展开完整 proof cases，因为前面小节已经分别对齐了证明所依赖的核心定义和假设。

它的核心直觉是：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

只要 freshness 条件保证攻击者无法同时恢复 `K_l / K_k / K_s` 的全部来源，那么攻击者至少缺少一个 KDF 输入。

KDF 将该隐藏输入混入 session key 后，真实 session key 应当对攻击者不可区分。

因此：

```text
RecvDone ==> SendDone 为 false 不表示 Theorem 1 proof sketch 失败。
```

因为 `RecvDone ==> SendDone` 是 full-message exact agreement diagnostic，而不是 KIND 的主证明目标。

## 7. 当前 query 分类

### Main queries

当前 main queries 包括：

1. `HonestRun` reachability
2. `SenderKey` secrecy
3. `ReceiverKey` secrecy
4. `SenderPrekeyVerified` structural query
5. `ReceiverPrekeyVerified` structural query
6. `SplitKemAccepted ==> SenderSplitKemComponent`
7. sender-side exception sanity query in optional compromise model

### Diagnostic queries

当前 diagnostic queries 包括：

```proverif
event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

该 query 保留用于 trace 观察，不作为当前 Figure 7 core 主安全目标。

## 8. 当前仍未完成的对齐问题

当前仍未完成：

1. `partnered / unpartnered session` 的论文定义与 ProVerif trace 分类之间的精确对应。
2. `receiver-side exception` 的最终形式。
3. `full BatchReceive` 的状态语义。
4. `one-time prekey / state consumption` 的建模。
5. `adaptive compromise ordering`。
6. `computational KIND game` 与 symbolic secrecy query 的精确关系。
7. `UNF-1KMA` 到 ProVerif component correspondence 的严格对应。
8. `IND-1BatchCCA` 到 ProVerif / CryptoVerif / hand proof 的严格对应。

## 9. 工具边界

### ProVerif 当前适合继续做

- Figure 7 core symbolic sanity check
- secrecy query
- structural correspondence query
- split-KEM component-level authenticity
- sender-side exception sanity check

### Tamarin 后续更适合做

- partnered / unpartnered session
- receiver-side state
- full BatchReceive
- one-time prekey consumption
- compromise ordering
- batch slot / vector identifiers

### CryptoVerif 或 computational proof 后续更适合做

- computational KIND game
- key indistinguishability
- `UNF-1KMA`
- `IND-1BatchCCA`
- game-based proof

## 10. 当前结论

当前 ProVerif symbolic analysis 与论文定义的对齐结论是：

1. `RecvDone ==> SendDone` 不应作为主安全目标，只作为 diagnostic query。
2. `SenderKey secrecy` 和 `ReceiverKey secrecy` 可以作为 KIND 的 symbolic proxy，但不能等同于 computational proof。
3. `SplitKemAccepted ==> SenderSplitKemComponent` 是 split-KEM component authenticity 的 symbolic proxy。
4. split-KEM state compromise 下的 receiver-side secrecy false 应分类为 receiver-side unpartnered session bad case 候选。
5. receiver-side exception 暂缓，等待 partnered / unpartnered session 语义更清楚。
6. sender-side exception sanity check 在当前 optional compromise symbolic model 中成立。
7. 当前模型是 Figure 7 core 的 single receive approximation，不是完整 BatchReceive model。
