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
- 不包含 full BatchReceive
- 不包含 compromise exceptions
- 不包含 AEAD
- 不包含 MAC
- 不包含 tag
- 不包含 key confirmation

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

## 当前结论

当前 Figure 7 core public-channel 符号模型得到以下阶段性结论：

- honest-run 可达。
- exact receiver agreement query 过强，作为 diagnostic false 保留。
- receiver 侧接受前存在 sender prekey verification。
- receiver 侧接受前存在 receiver prekey verification。
- sender-side session key secrecy 在当前 no-compromise 符号模型下成立。
- receiver-side session key secrecy 在当前 no-compromise 符号模型下成立。
- 不通过改变 m 的结构来让 exact agreement query 变 true。

## 当前不能声称的内容

当前结果不能说明：

- 已经证明完整 K-Waay 协议安全。
- 已经证明 full BatchReceive 安全。
- 已经证明带 compromise 的安全性。
- 已经证明 deniability。
- 已经完成 computational key indistinguishability 证明。
- ProVerif symbolic secrecy 等价于论文 computational KIND game。

## 下一步候选任务

1. 给当前模型加入受控 compromise events，并观察哪些 secrecy/correspondence query 会变 false。
2. 设计 normal bad case / exception ledger，用于记录允许的泄露条件。
3. 研究 unpartnered receiver session 与论文 KIND game 中 unpartnered receiver case 的对应关系。
4. 准备从 no-batch core 转向 full BatchReceive / receiver-side prekey reuse。
5. 后续考虑 Tamarin state model。
6. 后续考虑 CryptoVerif computational proof abstraction。
