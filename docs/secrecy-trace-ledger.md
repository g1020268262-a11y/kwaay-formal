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

## 总结

当前 secrecy 查询结果：

| ID | Query target | Result | Classification |
|---|---|---|---|
| ST-001 | SenderKey(A,B,s,k) | true | 符号化保密性成立 |
| ST-002 | ReceiverKey(B,A,s,k) | true | 符号化保密性成立 |

当前结论：

- sender-side session key secrecy 在当前 symbolic model 下成立。
- receiver-side session key secrecy 在当前 symbolic model 下成立。
- exact receiver agreement 仍然作为 diagnostic false 保留。
- 不通过加入 AEAD/MAC/tag/key confirmation 来改变 Figure 7 core。
