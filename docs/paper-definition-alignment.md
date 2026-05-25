# Paper Definition Alignment

## 目的

这个文件记录 K-Waay 论文定义与当前 ProVerif symbolic analysis query 之间的对应关系。

当前目标不是继续增加 ProVerif 实验，而是确认：

- 哪些 query 对齐论文安全目标；
- 哪些 query 只是 diagnostic；
- 哪些结果只能作为 symbolic proxy；
- 哪些问题后续需要 Tamarin 或 CryptoVerif。

## 当前模型边界

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

长期公钥材料已经显式公开：

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

## 对齐 1: KIND 不等于 full-message exact agreement

当前 ProVerif diagnostic query：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

当前结果：

```text
false
```

对齐判断：

该 query 不应作为 K-Waay Figure 7 core 的主安全目标。

原因：

该 query 要求 receiver 输出的完整 `sid` 和完整 `session_key` 必须对应某个 honest sender 输出的完整 `sid` 和完整 `session_key`。

这更接近 explicit full-message agreement。

而当前 Figure 7 core 的论文目标更接近 key indistinguishability / KIND，不是简单的 full-message exact correspondence。

因此，该 query 保留为 diagnostic query，用于观察 unpartnered receiver session trace，但不作为当前主安全结论。

## 对齐 2: 三输入 KDF 结构与 Figure 7 core 对齐

当前 ProVerif 模型中 session key 由以下输入派生：

```text
K_l
K_k
K_s
sid
```

即：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

对齐判断：

这与 Figure 7 core 中 long-term KEM、ephemeral KEM、split-KEM 三个 shared secret 共同进入 key derivation 的结构基本对齐。

注意：

论文图示中的顺序可能写作：

```text
K_l
K_s
K_k
```

当前文档中常写作：

```text
K_l
K_k
K_s
```

只要 ProVerif sender 和 receiver 使用相同顺序，符号模型内部是一致的。为了避免误解，后续文字尽量写成：

```text
K_l / K_k / K_s 三个 KDF 输入
```

而不是强调某个顺序。

## 对齐 3: full-message exact agreement 降级为 diagnostic

当前结果：

```text
RecvDone ==> SendDone: false
```

当前解释：

该 false 不应直接表述为协议漏洞。

更准确地说，它说明当前 Figure 7 core public-channel symbolic model 不满足 full-message exact receiver agreement。

这与当前模型边界一致，因为我们故意没有加入：

```text
AEAD
MAC
tag
key confirmation
```

因此，不能通过修改 `m = (ct_l, ct_k, ct_s)` 来让该 query 变 true。

## 对齐 4: split-KEM component authenticity 更接近 sender authentication 语义

当前 split-KEM component query：

```proverif
query A: agent, B: agent, cts: skem_ct, Ks: shared_secret;
  event(SplitKemAccepted(B,A,cts,Ks))
  ==> event(SenderSplitKemComponent(A,B,cts,Ks)).
```

当前结果：

```text
true
```

对齐判断：

该 query 比 full-message exact agreement 更接近 K-Waay Figure 7 core 中 split-KEM 承载 sender authentication 的语义。

原因：

它不要求整条消息：

```text
m = (ct_l, ct_k, ct_s)
```

完全对应某个 honest sender session。

它只检查 receiver 接受的 split-KEM 组件：

```text
ct_s
K_s
```

是否由 honest sender 生成过。

因此，该 query 可以作为当前 ProVerif 阶段的 main authentication query 之一。

限制：

该 query 不能等同于完整协议认证，也不能等同于 computational KIND proof。

## 对齐 5: sender-side secrecy 是 KIND 的 symbolic proxy

当前 sender-side secrecy query：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k)) ==> false.
```

baseline 结果：

```text
true
```

对齐判断：

该 query 可以作为 sender test-session key indistinguishability 的 symbolic proxy。

限制：

它只说明当前 symbolic model 下 attacker 不能推出 `SenderKey` 标记的 session key。

它不等价于 computational indistinguishability，也不等价于完整 KIND theorem。

## 对齐 6: receiver-side secrecy 是单独的 symbolic proxy

当前 receiver-side secrecy query：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

baseline 结果：

```text
true
```

对齐判断：

该 query 可以作为 receiver test-session key indistinguishability 的 symbolic proxy。

但是 receiver-side secrecy 和 sender-side secrecy 必须分开解释。

原因：

在以下 compromise 条件下：

```text
receiver_skem_sk
sender_skem_sk
```

实验结果都是：

```text
sender-side secrecy: true
receiver-side secrecy: false
```

这说明 receiver-side false 不等于 honest sender-side key 泄露。

它更像 split-KEM state compromise 下的 receiver-side unpartnered session bad case。

## 对齐 7: receiver-side exception 暂缓

当前不写统一 receiver-side exception query。

暂不采用：

```proverif
attacker(k) && event(ReceiverKey(B,A,s,k))
==> event(CompromiseReceiverSkemState(B)).
```

原因：

该 query 太粗。

当前已经观察到：

```text
CompromiseReceiverSkemState(B)
```

和：

```text
CompromiseSenderSkemState(A)
```

都可能导致 receiver-side secrecy false。

因此 receiver-side exception 需要先明确 partnered / unpartnered session 语义。

在此之前，receiver-side false 通过 ledger 分类记录，不写最终 exception theorem。

## 对齐 8: sender-side exception sanity check 当前成立

当前 optional compromise model：

```text
proverif/kwaay-core-public-channel-exception-choice.pv
```

当前 sender-side exception query：

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

对齐判断：

在当前 optional compromise symbolic model 中，如果 attacker 知道 sender-side session key，则必须已经发生 B 侧三个 decapsulation secret compromise。

限制：

该结果只在当前 symbolic compromise 选择空间内成立，不是最终 computational theorem。

它尚未覆盖：

```text
receiver-side exception
partnered / unpartnered session
full BatchReceive
adaptive compromise ordering
computational KIND game
```

## 对齐 9: split-KEM state compromise 下的 receiver-side false 是 expected bad case 候选

当前两个实验结果：

```text
receiver_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false
```

```text
sender_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false
```

对齐判断：

这两个 false 不应表述为 honest sender-side key 泄露。

更准确地说，它们表示 split-KEM state compromise 下，public-channel attacker 可以诱导 receiver 输出 attacker 可知的 unpartnered receiver session key。

该分类后续需要和论文中的 state exposure / partnered / unpartnered session 定义继续对齐。

## 对齐 10: KIND oracle / freshness 与当前 ProVerif 模型的关系

论文中的 KIND game 不是简单的 secrecy query。

KIND game 的核心是：

```text
TEST session key: real key vs random key
```

攻击者需要区分挑战者返回的 key 是真实 session key 还是随机 key。攻击者优势 negligible 时，DAKE 才满足 KIND。

当前 ProVerif 模型没有直接建模 real-or-random `TEST`。当前使用的是 symbolic secrecy proxy：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k)) ==> false.

query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

因此，当前 `SenderKey secrecy` 和 `ReceiverKey secrecy` 只能作为 KIND 的 symbolic proxy，不能等同于完整 computational KIND proof。

### Oracle 对齐表

| KIND oracle / 机制 | 论文语义 | 当前 ProVerif 近似 | 当前是否完整 |
|---|---|---|---|
| `EXEC` | 攻击者驱动协议执行，并可以注入消息 | public channel `c`，攻击者可拦截、替换、重放 | 部分对齐 |
| `LTK` | 长期密钥泄露 | `sig_sk` / `kem_sk` compromise experiment | 部分对齐 |
| `REGISTER` | 攻击者注册恶意公钥 | 当前未建模恶意注册 oracle | 未建模 |
| `STATE` | session state exposure | `sender_skem_sk`、`receiver_skem_sk`、`ekem_sk` compromise experiment | 部分对齐 |
| `KEY` | session key exposure | 当前没有完整 KEY oracle，只用 `attacker(k)` secrecy query | 未完整建模 |
| `TEST` | 返回真实 key 或随机 key | 当前没有 real-or-random test，只做 symbolic secrecy | 未建模 |
| freshness predicates | 排除 trivial attacks | 当前用 exception / normal bad case 分类近似 | 未完整建模 |
| partnering identifiers | 定义 sender / receiver session 如何匹配 | 当前只有 `SendDone` / `RecvDone`，未完整建模 partnered / unpartnered | 未完整建模 |
| receiver vector identifiers | 支持 `BatchReceive` 中一个 receiver session 对应多个 sender component | 当前 single receive approximation，未建模 vector partnering | 未建模 |

### Freshness 与当前 compromise 结果的关系

当前 ProVerif 结果不能简单解释为：

```text
攻击者永远不能知道任何 key
```

更准确的解释是：

```text
在当前 symbolic model 和当前 compromise 分类下，某些 key 泄露属于 normal bad case 或 receiver-side expected bad case。
```

例如：

```text
kem_sk + ekem_sk + receiver_skem_sk compromise:
sender-side secrecy: false
receiver-side secrecy: false
```

该结果应分类为 normal bad case，因为攻击者已经获得恢复 `K_l / K_k / K_s` 所需的全部 receiver-side decapsulation secrets。

又例如：

```text
receiver_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false

sender_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false
```

这两个结果不表示 honest sender-side key 泄露。它们更像 split-KEM state compromise 下的 receiver-side unpartnered session bad case。

### 当前不能完成的 freshness 对齐

当前 ProVerif 模型还不能完整表达论文 KIND 中的 freshness predicates。

尤其还没有表达：

```text
KEY reveal 之后哪些 session 不再 fresh
STATE reveal 之前 / 之后对 TEST session 的影响
LTK reveal 与 session freshness 的关系
partnered receiver session 与 unpartnered receiver session 的区分
BatchReceive 中 receiver partner/key identifiers 的向量语义
```

因此，当前 receiver-side exception 继续暂缓。

不能直接写成：

```proverif
attacker(k) && event(ReceiverKey(B,A,s,k))
==> event(CompromiseReceiverSkemState(B)).
```

原因是该 query 无法表达完整 freshness，也无法区分 receiver-side partnered / unpartnered session。

### 对当前 ProVerif 结论的影响

当前可以说：

```text
SenderKey secrecy / ReceiverKey secrecy 是 KIND 的 symbolic proxy。
```

当前不能说：

```text
已经证明 K-Waay 满足 computational KIND。
```

当前可以说：

```text
optional compromise model 下，sender-side key 泄露必须伴随 B 侧三个 decapsulation secret compromise。
```

当前不能说：

```text
已经完成所有 freshness exception theorem。
```

### 后续工具边界

如果后续要精确表达 freshness、state exposure ordering、partnered / unpartnered session 和 BatchReceive vector identifiers，优先考虑 Tamarin。

如果后续要逼近论文 computational KIND game，优先考虑 CryptoVerif 或手工 computational proof。

## 对齐 11: partner / key identifiers 与 receiver vector semantics

论文中的 partner identifiers 和 key identifiers 用于定义 session 之间如何匹配。

直观上：

```text
partner identifier = 当前 session 认为自己在和谁通信
key identifier     = 当前 session key 绑定哪份 transcript / 哪个 component
```

在普通一对一 AKE 中，一个 sender session 通常对应一个 receiver session，因此 partner / key identifiers 可以被理解成标量。

但是 K-Waay 支持 `BatchReceive`。receiver 可以一次处理一组输入消息，并输出一组 session keys。因此 receiver 侧的 partner identifiers 和 key identifiers 可能是向量。

例如，一个 receiver batch session 可以处理：

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

其中每个 `sid_i` 对应 batch 中的一个 component。

### 对当前 ProVerif query 的影响

当前 diagnostic query：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

隐含了一个较强的一对一标量匹配关系：

```text
entire receiver session <-> one sender session
```

但是论文中的 `BatchReceive` 语义更接近：

```text
sender session <-> receiver batch component
```

也就是说，一个 sender session 可能只对应 receiver batch session 中的某一个 component，而不是对应整个 receiver session。

因此，`RecvDone ==> SendDone` 作为 full-message exact receiver agreement 对当前 Figure 7 core 来说过强。它保留为 diagnostic query，但不作为主安全目标。

### 与 split-KEM component authenticity query 的关系

当前 ProVerif 中新增的 split-KEM component query 是：

```proverif
query A: agent, B: agent, cts: skem_ct, Ks: shared_secret;
  event(SplitKemAccepted(B,A,cts,Ks))
  ==> event(SenderSplitKemComponent(A,B,cts,Ks)).
```

该 query 不要求整个 receiver session 与整个 sender session 完全匹配。

它只检查：

```text
receiver 接受的 split-KEM component
是否对应 honest sender 生成过的 split-KEM component
```

因此，它比 full-message exact agreement 更接近论文中的 component-level partnering 直觉。

但是，该 query 仍然只是当前 ProVerif symbolic approximation。它还没有完整表达：

```text
BatchReceive vector input
receiver vector partner identifiers
receiver vector key identifiers
batch slot index
one-time state consumption
partnered / unpartnered session freshness
```

### 当前对齐判断

当前可以说：

```text
SplitKemAccepted ==> SenderSplitKemComponent
```

是 K-Waay split-KEM component-level authenticity 的 ProVerif proxy。

当前不能说：

```text
当前 ProVerif model 已经完整表达论文中的 BatchReceive vector partnering。
```

### 后续影响

如果后续继续研究 receiver-side authentication、partnered / unpartnered session、BatchReceive 或 state consumption，应优先考虑 Tamarin。

原因是这些语义需要表达：

```text
batch slot
receiver vector identifiers
time ordering
state consumption
compromise before / after accept
```

这些在 ProVerif 中可以近似，但不自然。

## 对齐 12: UNF-1KMA 与 split-KEM component authenticity

论文指出，split-KEM 的不可区分性定义只关注保密性，不足以保证发送方真实性。

也就是说，旧的 split-KEM 安全定义可以说明密文中的密钥不容易被区分或恢复，但它不能保证：

```text
只有诚实发送方才能生成诚实解封装方会接受的 split-KEM 密文
```

因此，论文引入 UNF-1KMA，即：

```text
Unforgeability against one known-message attacks
```

其直观目标是：

```text
攻击者即使看过一个合法 split-KEM 密文和对应密钥，
也不能伪造另一个新的密文，
使对应的诚实解封装方成功解封装。
```

### UNF-1KMA 的正确角色关系

需要注意，UNF-1KMA 不能和 deniability game 混淆。

在 UNF-1KMA game 中，攻击者看到：

```text
pkA
pkB
ct
KB
```

其中 `ct` 和 `KB` 来自一次合法封装。

攻击者的目标是输出一个新的密文：

```text
ct' != ct
```

并让对应的诚实解封装方对 `ct'` 解封装成功。

用论文 Figure 4 的抽象方向可以理解为：

```text
pkA, skA <- KeyGenA
pkB, skB <- KeyGenB
KB, ct <- Encaps(pkA, skB)
ct' <- adversary(pkA, pkB, ct, KB)
KA <- Decaps(pkB, skA, ct')
```

攻击者成功条件是：

```text
ct' != ct
KA != bottom
```

也就是说，攻击者不知道解封装密钥 `skA`，但仍试图伪造一个新的 `ct'`，让诚实解封装方成功接受。

如果攻击者已经知道解封装方的密钥，那么很多性质会退化，这不是 UNF-1KMA 正常挑战要表达的内容。

### 与 deniability game 的区别

论文中的 deniability game 是另一件事。

在 deniability game 中，攻击者可能会得到：

```text
pkA
pkB
skA
K
ct
```

这里攻击者知道 `skA`，目标是区分真实生成和模拟生成。

因此：

```text
UNF-1KMA 攻击者不知道 skA。
deniability game 攻击者可以知道 skA。
```

这两个安全游戏不能混在一起。

### 当前 ProVerif 符号代理

当前 ProVerif split-KEM 组件 query 是：

```proverif
query A: agent, B: agent, cts: skem_ct, Ks: shared_secret;
  event(SplitKemAccepted(B,A,cts,Ks))
  ==> event(SenderSplitKemComponent(A,B,cts,Ks)).
```

其中：

```proverif
event SenderSplitKemComponent(agent, agent, skem_ct, shared_secret).
event SplitKemAccepted(agent, agent, skem_ct, shared_secret).
```

当前结果：

```text
true
```

该 query 的含义是：

```text
如果接收方接受了声称来自 A 的 split-KEM 组件 cts，并得到 Ks，
那么诚实发送方 A 之前确实生成过同一个 cts 和 Ks。
```

因此，该 query 可以作为 UNF-1KMA 直觉的 ProVerif 符号代理。

### 角色方向的注意事项

需要注意，论文 Figure 4 中 `Encaps(pkA, skB)` / `Decaps(pkB, skA, ct')` 是 split-KEM 抽象安全游戏的记号。

而在 K-Waay Figure 7 的协议方向中，我们通常叙述为：

```text
发送方 A 生成 split-KEM 组件 ct_s
接收方 B 解封装 ct_s
```

因此，不应把 Figure 4 中的 A/B 名字直接粗暴等同于 K-Waay Figure 7 中的发送方 A / 接收方 B。

更稳妥的说法是：

```text
UNF-1KMA 是 split-KEM 抽象层的不可伪造性安全游戏。
它保证攻击者不能在看到一个合法密文和密钥后，
伪造新的密文，使对应诚实解封装方接受。
```

在 K-Waay Figure 7 的协议方向中，我们用：

```text
SplitKemAccepted(B,A,cts,Ks) ==> SenderSplitKemComponent(A,B,cts,Ks)
```

作为这个直觉的符号代理。

### 为什么它比 RecvDone ==> SendDone 更合适

当前 diagnostic query：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

要求的是：

```text
完整 sid 一样
完整 session_key 一样
完整 m = (ct_l, ct_k, ct_s) 一样
```

这更接近完整消息精确一致性。

但是 UNF-1KMA 关注的是 split-KEM 组件是否可伪造：

```text
ct_s
K_s
```

因此，`SplitKemAccepted ==> SenderSplitKemComponent` 比 `RecvDone ==> SendDone` 更接近论文中 split-KEM 承载发送方真实性的组件级语义。

### 限制

当前 ProVerif query 不是完整 UNF-1KMA 证明。

原因包括：

```text
UNF-1KMA 是计算型安全游戏
当前 query 是符号对应关系
当前 query 没有建模完整攻击者挑战游戏
当前 query 没有给出可忽略优势证明
当前 query 没有覆盖完整 BatchReceive
当前 query 没有完整表达状态泄露顺序
当前 query 没有完整表达已知消息攻击游戏
```

因此，当前只能说：

```text
SplitKemAccepted ==> SenderSplitKemComponent
是 UNF-1KMA 直觉的符号代理
```

不能说：

```text
ProVerif 已经证明 split-KEM 满足计算型 UNF-1KMA
```

### 与接收方侧泄露结果的关系

当前实验中：

```text
receiver_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false
```

以及：

```text
sender_skem_sk compromise:
sender-side secrecy: true
receiver-side secrecy: false
```

这些结果说明 split-KEM 状态泄露会破坏接收方侧保密性，但不等于诚实发送方侧密钥泄露。

这些结果应理解为：

```text
split-KEM 状态泄露下的接收方侧未配对会话异常情形
```

而不是：

```text
完整协议认证失败
```

### 当前对齐判断

当前可以说：

```text
SplitKemAccepted ==> SenderSplitKemComponent
```

是当前 ProVerif 阶段用于刻画 split-KEM 组件级真实性的主要 query。

当前不能说：

```text
该 query 已经证明完整 UNF-1KMA。
```

当前也不能说：

```text
该 query 已经证明完整 K-Waay 认证。
```

### 后续影响

后续如果要更严格对齐 UNF-1KMA，需要考虑：

```text
计算型安全游戏
已知消息攻击结构
新鲜性 / 状态泄露顺序
BatchReceive 中的组件复用
接收方向量标识符
```

这些内容可能需要后续结合 CryptoVerif、Tamarin 或手工证明继续分析。

## 对齐 13: IND-1BatchCCA / BatchReceive 与 single receive approximation

论文中的 `BatchReceive` 不是普通单条接收。

它用于处理接收方离线，或接收方 split-KEM 临时公钥被多个发送方复用的情况。接收方上线后，可以把一组使用同一个接收方侧 split-KEM 状态的消息放入一个批次中统一处理。

直观上，`BatchReceive` 输入的是一组消息：

```text
(pk_1, prekey_1, m_1)
(pk_2, prekey_2, m_2)
...
(pk_d, prekey_d, m_d)
```

输出的是一组会话密钥：

```text
k_1
k_2
...
k_d
```

其中每个输出密钥对应批次中的一个组件。

### IND-1BatchCCA 的直觉

`IND-1BatchCCA` 是 split-KEM 的计算型保密性安全游戏。

它不是认证 query，而是密钥不可区分性 / 保密性安全游戏。

直观目标是：

```text
即使攻击者获得一次批量解封装能力，
也不能区分挑战 split-KEM 密钥是真实密钥还是随机密钥。
```

其中 `1Batch` 的意思是：

```text
攻击者最多获得一次批量解封装 query。
```

批量解封装的特点是：

```text
如果批次中任意一个解封装失败，
整个批次返回 bottom。
```

这和普通逐条解封装不同。它避免攻击者从每个密文的独立成功 / 失败结果中获得额外信息。

### 为什么 K-Waay 需要 IND-1BatchCCA

K-Waay 的接收方 split-KEM 临时公钥可能被多个发送方使用。

这会产生批量复用场景：

```text
多个发送方使用同一个接收方 split-KEM 公钥
接收方后续用同一个接收方 split-KEM 秘密状态批量解封装
```

因此，普通 split-KEM 保密性定义不足以覆盖这种批量复用场景。

论文使用 `IND-1BatchCCA` 来表达：

```text
在一次批量解封装能力存在的情况下，
split-KEM 挑战密钥仍应保持不可区分。
```

### 与 UNF-1KMA 的分工

`UNF-1KMA` 和 `IND-1BatchCCA` 关注不同性质。

```text
UNF-1KMA:
组件级真实性 / 不可伪造性。
攻击者不能伪造新的 split-KEM 密文，使诚实解封装方接受。

IND-1BatchCCA:
组件级保密性 / 不可区分性。
攻击者即使获得一次批量解封装能力，也不能区分挑战密钥是真实还是随机。
```

因此，K-Waay split-KEM 层面同时需要：

```text
UNF-1KMA
IND-1BatchCCA
```

前者支撑发送方认证的 split-KEM 组件级语义，后者支撑 split-KEM 共享秘密的保密性。

### 当前 ProVerif 模型的近似

当前 ProVerif 模型没有完整建模 `BatchReceive`。

当前接收方侧更接近单条接收近似：

```proverif
in(c, mFromNet);
let ctLFromNet = get_lkem_ct(mFromNet) in
let ctEFromNet = get_ekem_ct(mFromNet) in
let ctSFromNet = get_skem_ct(mFromNet) in
...
event RecvDone(B,A,sidBA,kRecv);
event ReceiverKey(B,A,sidBA,kRecv);
```

当前模型只处理一条消息：

```text
m = (ct_l, ct_k, ct_s)
```

它还没有表达：

```text
批次输入向量
批次输出向量
批次位置索引
接收方向量配对标识符
接收方向量密钥标识符
如果任意组件解封装失败则整个批次返回 bottom
同一个接收方 split-KEM 状态被多个发送方组件使用
状态消耗 / 一次性使用
完整 BatchReceive 复用语义
```

因此，当前 ProVerif 模型不能声称已经完整表达 `IND-1BatchCCA` 或完整 `BatchReceive`。

### 当前 ProVerif 保密性 query 的位置

当前 ProVerif 保密性 query：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k)) ==> false.

query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

可以作为 KIND / 会话密钥保密性的符号代理。

但是它不是 `IND-1BatchCCA` 证明。

原因：

```text
IND-1BatchCCA 是计算型 real-or-random 安全游戏
当前 query 是符号攻击者可知性 query
IND-1BatchCCA 允许一次批量解封装 query
当前模型没有批量解封装调用机制
IND-1BatchCCA 涉及挑战密钥不可区分性
当前模型只检查 attacker 是否可推出会话密钥
```

因此，当前只能说：

```text
当前 ProVerif 保密性 query 是会话密钥保密性的符号近似。
```

不能说：

```text
当前 ProVerif 已经证明 split-KEM 满足 IND-1BatchCCA。
```

### 对 RecvDone ==> SendDone 的影响

`BatchReceive` 进一步说明：

```proverif
event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k))
```

这个完整消息精确一致性 query 对当前 Figure 7 core 来说过强。

原因是，在完整 `BatchReceive` 语义中，一个接收方批次会话可能处理多个发送方组件，并输出多个密钥。

也就是说，真实结构更接近：

```text
发送方会话 <-> 接收方批次组件
```

而不是：

```text
整个接收方会话 <-> 一个发送方会话
```

因此，`RecvDone ==> SendDone` 继续保留为诊断 query，不作为当前主安全目标。

### 当前对齐判断

当前可以说：

```text
当前 ProVerif 模型覆盖了 Figure 7 core 的单条接收近似。
```

当前不能说：

```text
当前 ProVerif 模型已经完整覆盖 BatchReceive。
```

当前可以说：

```text
SplitKemAccepted ==> SenderSplitKemComponent
是 UNF-1KMA 直觉的符号代理。
```

当前不能说：

```text
当前 ProVerif 已经证明 IND-1BatchCCA。
```

### 后续影响

如果后续要完整对齐 `IND-1BatchCCA` 和 `BatchReceive`，需要考虑：

```text
批次输入向量
批次输出向量
批次中止行为
批次位置索引
接收方向量配对标识符
接收方向量密钥标识符
接收方 split-KEM 状态复用
状态消耗
一次性预密钥语义
```

这些语义在 ProVerif 中可以近似，但不自然。

后续如果继续研究完整 `BatchReceive`，优先考虑 Tamarin。

如果后续要研究计算型 `IND-1BatchCCA`，需要考虑 CryptoVerif 或手工计算型证明。

## 当前 query 分类

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

## 当前仍未完成的对齐问题

当前仍未完成：

1. `partnered / unpartnered session` 的论文定义与 ProVerif trace 分类之间的精确对应。
2. `receiver-side exception` 的最终形式。
3. `full BatchReceive` 的状态语义。
4. `one-time prekey / state consumption` 的建模。
5. `adaptive compromise ordering`。
6. `computational KIND game` 与 symbolic secrecy query 的精确关系。
7. `UNF-1KMA` 到 ProVerif component correspondence 的严格对应。

## 工具边界

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

### CryptoVerif 或 computational proof 后续更适合做

- computational KIND game
- key indistinguishability
- game-based proof

## 当前结论

当前 ProVerif symbolic analysis 与论文定义的对齐结论是：

1. `RecvDone ==> SendDone` 不应作为主安全目标。
2. `SenderKey secrecy` 和 `ReceiverKey secrecy` 可以作为 KIND 的 symbolic proxy，但不能等同于 computational proof。
3. split-KEM component authenticity query 更贴近 Figure 7 core 中 sender authentication 的组件级语义。
4. split-KEM state compromise 下的 receiver-side secrecy false 应分类为 receiver-side unpartnered session bad case 候选。
5. receiver-side exception 暂缓，等待 partnered / unpartnered session 语义更清楚。
6. sender-side exception sanity check 在当前 optional compromise symbolic model 中成立。
