# Formal Decision Memo

## 目的

这个文件记录当前 K-Waay Figure 7 core ProVerif symbolic analysis 中已经确认的研究决策。

它不是最终论文结论，而是后续建模、查询设计和实验记录的统一口径。

## 当前模型边界

- 协议目标: K-Waay Figure 7 core
- 消息结构: m = (ct_l, ct_k, ct_s)
- 长期公钥材料已显式公开到 public channel
- 不加入 AEAD
- 不加入 MAC
- 不加入 tag
- 不加入 key confirmation
- 不加入 full BatchReceive
- 当前工具: ProVerif
- 当前分析类型: symbolic analysis
- 当前攻击者: public-channel attacker with selected compromise experiments

## 决策 1: full-message exact agreement 只作为 diagnostic

当前 query:

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

当前结果:

```text
false
```

决策:

该 query 不作为当前 Figure 7 core 的主安全目标，只作为 diagnostic query 保留。

原因:

该 query 要求 receiver 输出的完整 `sid` 和完整 `session_key` 必须对应某个 honest sender 的完整 `sid` 和完整 `session_key`。

这比当前 Figure 7 core 的目标更强，更接近 explicit full-message agreement。当前模型故意不加入 AEAD、MAC、tag、key confirmation，因此不应该为了让该 query 成立而改变 Figure 7 core。

## 决策 2: prekey verification structural queries 保留为 main checks

当前保留以下 structural queries:

```proverif
event(RecvDone(B,A,s,k)) ==> event(SenderPrekeyVerified(B,A,sp)).
```

```proverif
event(RecvDone(B,A,s,k)) ==> event(ReceiverPrekeyVerified(A,B,rp)).
```

当前结果均为:

```text
true
```

决策:

这两条保留为 main structural authentication checks。

原因:

它们检查的是当前模型是否保留了 Figure 7 core 中 prekey verification 的结构，不要求 full-message exact agreement。

## 决策 3: sender-side secrecy 和 receiver-side secrecy 分开处理

当前 secrecy queries:

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k)) ==> false.
```

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

决策:

SenderKey secrecy 和 ReceiverKey secrecy 必须分开解释、分开记录、分开设计 exception。

原因:

在 `receiver_skem_sk` compromise 下，当前结果为:

```text
sender-side secrecy: true
receiver-side secrecy: false
```

这说明 receiver-side false 不等于 honest sender-side key 泄露。

## 决策 4: receiver-side exception 暂缓

决策:

暂时不写统一的 receiver-side exception query。

最新补充实验显示，单独泄露 A 的 sender split-KEM secret state `senderSkA` 时，结果为：

```text
sender-side secrecy: true
receiver-side secrecy: false
```

这说明 receiver-side secrecy false 不只可能来自 `CompromiseReceiverSkemState(B)`，也可能来自 `CompromiseSenderSkemState(A)`。

暂不采用:

```proverif
attacker(k) && event(ReceiverKey(B,A,s,k))
==> event(CompromiseReceiverSkemState(B)).
```

原因:

该 query 会漏掉 `sender_skem_sk` compromise 导致的 receiver-side unpartnered session key leakage。

receiver-side exception 暂缓的原因包括:

- `receiver_skem_sk` compromise 会导致 receiver-side secrecy false；
- `sender_skem_sk` compromise 也会导致 receiver-side secrecy false；
- 两种情况都不破坏 honest sender-side secrecy；
- 当前这些 false 更像 receiver-side unpartnered session under split-KEM state compromise；
- 在没有明确 partnered / unpartnered session 语义之前，不应写统一 receiver-side exception query。

当前更合理的解释是：`receiverSkB` 泄露后，public-channel attacker 可以诱导 receiver 输出一个 attacker 可知的 unpartnered receiver session key。

在 partnered / unpartnered session 语义明确之前，receiver-side false 先通过 ledger 分类，不写最终 exception query。

## 决策 5: sender-side exception 可以先做 ProVerif sanity check

当前 optional compromise model:

```text
proverif/kwaay-core-public-channel-exception-choice.pv
```

当前 sender-side exception query:

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k))
  ==> event(CompromiseKemSk(B))
   && event(CompromiseReceiverEkemState(B))
   && event(CompromiseReceiverSkemState(B)).
```

当前结果:

```text
true
```

决策:

该 query 可以作为当前 ProVerif symbolic model 下的 sender-side exception sanity check。

含义:

在 attacker 可自由选择触发 0 个、1 个、2 个或 3 个 receiver-side decapsulation secret compromise 的模型中，只要 attacker 能知道 sender-side session key，就必须已经发生:

```text
CompromiseKemSk(B)
CompromiseReceiverEkemState(B)
CompromiseReceiverSkemState(B)
```

限制:

该结论仍不是最终 theorem，因为尚未覆盖:

```text
sender_skem_sk compromise
receiver-side exception
partnered / unpartnered session
full BatchReceive
adaptive compromise ordering
computational KIND game
```

## 决策 6: split-KEM component authenticity 作为新的 main authentication query

当前 split-KEM component query:

```proverif
query A: agent, B: agent, cts: skem_ct, Ks: shared_secret;
  event(SplitKemAccepted(B,A,cts,Ks))
  ==> event(SenderSplitKemComponent(A,B,cts,Ks)).
```

当前结果:

```text
true
```

决策:

该 query 作为当前 Figure 7 core 中更贴近 split-KEM sender authentication 语义的 main authentication query。

原因:

它不要求整条消息 `m = (ct_l, ct_k, ct_s)` 或完整 `session_key` exact agreement。

它只检查 receiver 接受的 split-KEM 组件 `ct_s` 和对应 `K_s` 是否由 honest sender 生成过。

这比 `RecvDone ==> SendDone` 更贴近当前 Figure 7 core 中 split-KEM 承载 sender authentication 的语义。

## 决策 7: 暂不在 baseline 中加入 Partnered / UnpartneredReceiver event

决策:

暂不在 ProVerif baseline 中加入:

```proverif
event Partnered(...).
event UnpartneredReceiver(...).
```

原因:

如果定义不好，这些 event 可能只是把待证明性质换个名字，形成循环定义。

当前阶段中，partnered / unpartnered 先作为 trace-ledger 和 authentication-query-ledger 中的解释分类。

后续如果需要精细表达 state、ordering、partnering，可以转向 Tamarin。

## 决策 8: 工具分工

当前工具分工如下:

### ProVerif

继续用于:

- Figure 7 core symbolic model
- no-compromise secrecy
- selected compromise secrecy
- sender-side exception sanity check
- prekey verification structural checks
- split-KEM component correspondence

### Tamarin

后续用于:

- partnered / unpartnered session
- receiver-side state
- one-time prekey consumption
- full BatchReceive
- compromise ordering

### CryptoVerif

后续用于:

- computational KIND-style proof
- key indistinguishability
- game-based security argument

## 当前 main queries

当前 main queries 包括:

1. HonestRun reachability
2. SenderKey secrecy
3. ReceiverKey secrecy
4. SenderPrekeyVerified structural query
5. ReceiverPrekeyVerified structural query
6. split-KEM component authenticity query
7. sender-side exception sanity query in optional compromise model

## 当前 diagnostic queries

当前 diagnostic queries 包括:

1. full-message exact receiver agreement:

```proverif
event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

该 query 保留用于观察 trace，但不作为当前 Figure 7 core 的主安全目标。

## 当前暂缓事项

当前暂缓:

- receiver-side exception query
- receiver-side exception 需要同时考虑 `CompromiseReceiverSkemState(B)` 和 `CompromiseSenderSkemState(A)`
- receiver-side exception 需要先明确 partnered / unpartnered session 语义
- Partnered / UnpartneredReceiver event
- full BatchReceive
- Tamarin model
- CryptoVerif proof
- AEAD/MAC/tag/key confirmation
- 修改 Figure 7 core message structure

## 下一步实施计划

下一步短期目标:

1. 确认 `authentication-query-ledger.md` 已记录 split-KEM component authenticity。
2. 确认 `secrecy-trace-ledger.md` 已记录 optional compromise sender-side exception。
3. 更新 `analysis-summary.md`，确保上述决策已经反映在总总结中。
4. 暂停新增文档，开始清理和稳定当前 `.pv` 文件。
5. 已补测 `sender_skem_sk compromise`。
6. 下一步应同步更新 `analysis-summary.md` 和 `secrecy-trace-ledger.md`，记录 `sender_skem_sk compromise` 的结果。
7. receiver-side exception 继续暂缓。
8. 后续如果要继续处理 receiver-side，需要优先研究 split-KEM state compromise 下的 unpartnered receiver session 分类。
