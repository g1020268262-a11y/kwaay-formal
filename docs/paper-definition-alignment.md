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
