# Authentication Query Ledger

## 目的

这个文件记录 K-Waay Figure 7 core ProVerif public-channel model 中的 authentication / correspondence 查询结果。

当前重点是区分：

- full-message exact agreement
- structural prekey verification
- split-KEM component authenticity

## 当前模型边界

- 协议目标: K-Waay Figure 7 core
- 消息结构: m = (ct_l, ct_k, ct_s)
- 长期公钥材料已显式输出到 public channel
- 不加入 AEAD
- 不加入 MAC
- 不加入 tag
- 不加入 key confirmation
- 不加入 full BatchReceive

## AQ-001: full-message exact receiver agreement

### 模型文件

`proverif/kwaay-core-public-channel.pv`

### Query

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

### Result

```text
false
```

### Classification

diagnostic false / query too strong for Figure 7 core

### Explanation

该 query 要求 receiver 的完整 `sid` 和 `session_key` 必须对应某个 honest sender 的完整 `sid` 和 `session_key`。

但是当前 Figure 7 core 的 public-channel model 中，攻击者可以替换 `ct_l` 或 `ct_k`，诱导 receiver 输出一个 unpartnered receiver session key。

因此该 query 不应作为当前 core 的主认证目标，只作为 diagnostic query 保留。

## AQ-002: receiver implies sender prekey verification

### Query

```proverif
query A: agent, B: agent, sp: sender_prekey_bundle, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SenderPrekeyVerified(B,A,sp)).
```

### Result

```text
true
```

### Classification

structural authentication check holds

### Explanation

如果 receiver 触发 `RecvDone(B,A,s,k)`，那么模型中已经发生过 `SenderPrekeyVerified(B,A,sp)`。

这说明 receiver 不是在完全没有验证 sender prekey 的情况下接受。

## AQ-003: receiver implies receiver prekey verification

### Query

```proverif
query A: agent, B: agent, rp: receiver_prekey_bundle, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(ReceiverPrekeyVerified(A,B,rp)).
```

### Result

```text
true
```

### Classification

structural authentication check holds

### Explanation

如果 receiver 触发 `RecvDone(B,A,s,k)`，那么模型中已经发生过 `ReceiverPrekeyVerified(A,B,rp)`。

这说明 sender 侧曾经验证过 receiver prekey。

## AQ-004: split-KEM component authenticity

### 模型文件

`proverif/kwaay-core-public-channel-splitkem-component.pv`

### Query

```proverif
query A: agent, B: agent, cts: skem_ct, Ks: shared_secret;
  event(SplitKemAccepted(B,A,cts,Ks))
  ==> event(SenderSplitKemComponent(A,B,cts,Ks)).
```

### Result

```text
true
```

### Classification

split-KEM component-level authenticity holds

### Explanation

该 query 不要求整条消息 `m = (ct_l, ct_k, ct_s)` 或完整 `session_key` exact agreement。

它只检查 receiver 接受的 split-KEM 组件 `ct_s` 和对应 `K_s` 是否由 honest sender 生成过。

结果为 true 说明：虽然 full-message exact agreement 不成立，但 split-KEM component-level authenticity 在当前 Figure 7 core symbolic model 下成立。

这更接近当前论文中 split-KEM 承载 sender authentication 的语义。

## 当前结论

当前 authentication / correspondence 结果可以总结为：

- full-message exact receiver agreement 不成立，只作为 diagnostic false 保留。
- prekey verification structural queries 成立。
- split-KEM component-level authenticity 成立。
- 当前不通过加入 AEAD/MAC/tag/key confirmation 来让 full-message exact agreement 变 true。
