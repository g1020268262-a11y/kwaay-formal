# K-Waay ProVerif 分析总结

## 目的

这个文件总结当前 K-Waay Figure 7 core 在 ProVerif public-channel 符号模型下的阶段性分析结果。

当前结果用于指导后续建模，不等价于完整论文安全证明。

## 当前模型

- 模型文件: proverif/kwaay-core-public-channel.pv
- 协议目标: 原始 K-Waay Figure 7 core
- 消息结构: m = (ct_l, ct_k, ct_s)
- 工具: ProVerif
- 模型类型: 符号模型
- 攻击者模型: public-channel attacker
- 长期公钥材料 `spkA/kpkA/pkA/spkB/kpkB/pkB` 已显式输出到 public channel。
- 不包含 full BatchReceive
- 不包含 compromise exceptions
- 不包含 AEAD
- 不包含 MAC
- 不包含 tag
- 不包含 key confirmation

这个修正很重要，因为 `sid` 包含长期公钥元组。如果长期公钥没有公开，攻击者可能无法构造完整 `sid`，从而导致 secrecy query 过强地保持 true。

## 当前已验证或记录的查询

### Q0: Honest-run reachability

Query:

```proverif
query k: session_key; event(HonestRun(k)).
```

结果:

```text
Query not event(HonestRun(k)) is false.
```

解释:

`not event(HonestRun(k))` 为 false，表示 `HonestRun(k)` 可达。也就是说，当前模型存在一条正常诚实执行路径。

### Q1-exact: exact receiver agreement

Query:

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

结果:

```text
false
```

分类:

diagnostic false / expected false

解释:

这个 exact correspondence 对 Figure 7 core 来说过强。攻击者可以替换某个 KEM ciphertext，例如 ct_k，使 receiver 输出一个 unpartnered receiver session key。这个现象不通过加入 AEAD/MAC/tag/key confirmation 来修复，因为当前模型必须保持 Figure 7 core 的消息结构。

### Q1a: receiver implies sender prekey verification

Query:

```proverif
query A: agent, B: agent, sp: sender_prekey_bundle, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SenderPrekeyVerified(B,A,sp)).
```

结果:

```text
true
```

解释:

如果 receiver 触发 `RecvDone(B,A,s,k)`，那么模型中已经发生过对应的 `SenderPrekeyVerified(B,A,sp)`。

### Q1b: receiver implies receiver prekey verification

Query:

```proverif
query A: agent, B: agent, rp: receiver_prekey_bundle, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(ReceiverPrekeyVerified(A,B,rp)).
```

结果:

```text
true
```

解释:

如果 receiver 触发 `RecvDone(B,A,s,k)`，那么模型中已经发生过对应的 `ReceiverPrekeyVerified(A,B,rp)`。

### Q2-S1: sender-side session key secrecy

Query:

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(SenderKey(A,B,s,k)) ==> false.
```

结果:

```text
true
```

解释:

在当前 no-compromise public-channel 符号模型中，攻击者无法同时满足 `event(SenderKey(A,B,s,k))` 和 `attacker(k)`。因此 sender 侧生成的 session key 在当前模型下保持符号化保密性。

### Q2-S2: receiver-side session key secrecy

Query:

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

结果:

```text
true
```

解释:

在当前 no-compromise public-channel 符号模型中，攻击者无法同时满足 `event(ReceiverKey(B,A,s,k))` 和 `attacker(k)`。因此 receiver 侧输出的 session key 在当前模型下保持符号化保密性。

这也说明：`Q1-exact` 的 false 不自动意味着 receiver-side secrecy 失败。

## Authentication / correspondence 查询更新

当前 full-message exact receiver agreement 查询为 false：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

结果：

```text
false
```

当前解释：

该 query 要求 receiver 输出的完整 `sid` 和 `session_key` 必须与某个 honest sender 的完整 `sid` 和 `session_key` 一致。

这个要求对当前 Figure 7 core public-channel model 来说过强。它更接近 explicit full-message agreement，而不是论文 KIND 目标本身。因此该 query 保留为 diagnostic false，不作为当前 core 的主认证结论。

### Split-KEM component authenticity

模型文件：

`proverif/kwaay-core-public-channel-splitkem-component.pv`

新增事件：

```proverif
event SenderSplitKemComponent(agent, agent, skem_ct, shared_secret).
event SplitKemAccepted(agent, agent, skem_ct, shared_secret).
```

查询：

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

该查询不要求整条消息 `m = (ct_l, ct_k, ct_s)` 或完整 `session_key` exact agreement。

它只检查 receiver 接受的 split-KEM 组件 `ct_s` 和对应 `K_s` 是否由 honest sender 生成过。

结果为 true 说明：虽然 full-message exact agreement 不成立，但 split-KEM component-level authenticity 在当前 Figure 7 core symbolic model 下成立。

这个查询更接近当前论文中 split-KEM 承载 sender authentication 的语义。

## Compromise 实验结果

当前已测试以下 compromise 条件。

### 单独泄露 `sig_sk`

模型文件：

`proverif/kwaay-core-public-channel-leak-sigsk.pv`

结果：

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

单独泄露长期签名私钥不会直接泄露 `K_l`、`K_k`、`K_s`，因此当前 symbolic model 下 session key secrecy 仍然成立。

### 单独泄露 `kem_sk`

模型文件：

`proverif/kwaay-core-public-channel-leak-kemsk.pv`

结果：

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

单独泄露 B 的长期 KEM 私钥最多帮助攻击者恢复 `K_l`，但还缺少 `K_k` 和 `K_s`。

### 单独泄露 `ekem_sk`

模型文件：

`proverif/kwaay-core-public-channel-leak-ekemsk.pv`

结果：

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

单独泄露 B 的 receiver ephemeral KEM 私钥最多帮助攻击者恢复 `K_k`，但还缺少 `K_l` 和 `K_s`。

### 单独泄露 `receiver_skem_sk`

模型文件：

`proverif/kwaay-core-public-channel-leak-rskemsk.pv`

结果：

```text
sender-side secrecy: true
receiver-side secrecy: false
```

解释：

单独泄露 B 的 receiver split-KEM secret state 不会泄露 honest sender-side session key，因此 sender-side secrecy 仍然成立。

但是 receiver-side secrecy 失败。原因是 public-channel attacker 可以替换 receiver 接收的消息，并在获得 `receiverSkB` 后诱导 receiver 输出一个攻击者也能推出的 unpartnered receiver session key。

该结果应分类为 expected receiver-side bad case，而不是 honest sender-side key 泄露。

### 组合泄露 `kem_sk + ekem_sk`

模型文件：

`proverif/kwaay-core-public-channel-leak-kemsk-ekemsk.pv`

结果：

```text
sender-side secrecy: true
receiver-side secrecy: true
```

解释：

攻击者可以恢复 `K_l` 和 `K_k`，但仍然缺少 `K_s`，因此当前 symbolic model 下 session key secrecy 仍然成立。

### 组合泄露 `kem_sk + ekem_sk + receiver_skem_sk`

模型文件：

`proverif/kwaay-core-public-channel-leak-all-receiver-secrets.pv`

结果：

```text
sender-side secrecy: false
receiver-side secrecy: false
```

解释：

攻击者获得 B 侧恢复三个 KDF 输入所需的全部 secret 后，可以恢复：

```text
K_l
K_k
K_s
```

由于长期公钥和 `sid` 相关公开材料也已经公开，攻击者可以计算：

```text
session_key = KDF(K_l, K_k, K_s, sid)
```

因此 sender-side 和 receiver-side secrecy 都失败。这个结果属于 normal bad case。

## 当前结论

当前 Figure 7 core public-channel 符号模型得到以下阶段性结论：

- honest-run 可达。
- 长期公钥必须在 public-channel model 中显式公开，否则 secrecy 结果可能过强。
- exact receiver agreement query 过强，作为 diagnostic false 保留。
- `RecvDone ==> SendDone` 作为 full-message exact agreement 查询为 false，仅保留为 diagnostic。
- 该 false 不应通过加入 AEAD/MAC/tag/key confirmation 来修复，因为当前模型故意保持 Figure 7 core。
- receiver 侧接受前存在 sender prekey verification。
- receiver 侧接受前存在 receiver prekey verification。
- split-KEM component authenticity query 为 true。
- 当前 authentication 解释应区分 full-message exact agreement、prekey verification structural checks 和 split-KEM component-level authenticity。
- sender-side session key secrecy 在当前 no-compromise 符号模型下成立。
- receiver-side session key secrecy 在当前 no-compromise 符号模型下成立。
- 单独泄露 `sig_sk`、`kem_sk`、`ekem_sk` 不破坏当前 session-key secrecy。
- 单独泄露 `receiver_skem_sk` 会破坏 receiver-side unpartnered session secrecy，但不破坏 honest sender-side secrecy。
- 泄露 `kem_sk + ekem_sk` 仍不足以恢复 session key。
- 泄露 `kem_sk + ekem_sk + receiver_skem_sk` 属于 normal bad case，会破坏 session-key secrecy。
- 不通过改变 m 的结构来让 exact agreement query 变 true。

## 当前不能声称的内容

当前结果不能说明：

- 已经证明完整 K-Waay 协议安全。
- 已经证明 full BatchReceive 安全。
- 已经证明带 compromise 的安全性。
- 已经证明 deniability。
- 已经完成 computational key indistinguishability 证明。
- ProVerif symbolic secrecy 等价于论文 computational KIND game。
- Figure 7 core 满足 explicit full-message agreement。
- split-KEM component authenticity 等同于完整协议认证。
- ProVerif component correspondence 等同于论文完整 computational KIND proof。
- 不能把 `receiver_skem_sk` compromise 下的 receiver-side secrecy false 直接表述为 K-Waay 协议漏洞。
- 不能把 full receiver-side state compromise 下的 secrecy false 表述为协议漏洞，因为这是 normal bad case。
- 不能把当前 ProVerif compromise 实验等同于完整 adaptive compromise security proof。

## 下一步候选任务

1. 给当前模型加入受控 compromise events，并观察哪些 secrecy/correspondence query 会变 false。
2. 设计 normal bad case / exception ledger，用于记录允许的泄露条件。
3. 研究 unpartnered receiver session 与论文 KIND game 中 unpartnered receiver case 的对应关系。
4. 准备从 no-batch core 转向 full BatchReceive / receiver-side prekey reuse。
5. 后续考虑 Tamarin state model。
6. 后续考虑 CryptoVerif computational proof abstraction。
