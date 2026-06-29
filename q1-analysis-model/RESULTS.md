# Q1 分层诊断结果

最后一次验证命令：

```bash
TIMEOUT_SECONDS=240 bash q1-analysis-model/run-q1-triage.sh
```

验证摘要：

```text
KWAAY_LIKE:       OK
ATTACKER_KEY_BAD: OK
AUTHZ_BAD:        OK
CONFIRMED_FIX:    OK
```

完整日志位于：

```text
logs/q1-analysis-model/summary.txt
logs/q1-analysis-model/out/
logs/q1-analysis-model/generated/
```

## 结果表

| 目标 | Q1 | 接收方 key secrecy | 认证分量来源 | 受保护数据保密 | 发送方授权副作用 | 结论 |
|---|---:|---:|---:|---:|---:|---|
| `KWAAY_LIKE` | false | true | true | true | 未建模为副作用 | 有 Q1，但在该抽象中无害 |
| `ATTACKER_KEY_BAD` | false | false | true | false | 未建模为副作用 | 有 Q1，且导致机密性攻击 |
| `AUTHZ_BAD` | false | true | true | true | false | 有 Q1，且导致授权语义攻击 |
| `CONFIRMED_FIX` | true | true | true | true | 不适用 | 确认标签修复 Q1 |

## 关键解释

`KWAAY_LIKE` 的 Q1 查询为 `false`，表示攻击者可以制造一个接收方完成事件，使其没有匹配的发送方完成事件。这对应 K-Waay 风格的重组攻击：攻击者复用真实发送方生成的认证分量 `ctS`，但替换未认证的 `ctL` 和 `ctE`，导致接收方计算出新的 `sid/key`。

这个场景下密钥查询仍为 `true`，原因是最终 `key` 依赖 `KS`。`KS` 来自发送方认证 KEM 分量，攻击者只能复用它，不能计算它。因此攻击者能改变接收方最终得到哪个会话密钥，但不能知道该密钥。

`ATTACKER_KEY_BAD` 的密钥查询为 `false`，原因是该目标故意把最终 key 改为只依赖 `KL` 和 `KE`。这两个分量可以由攻击者用公开公钥和自选随机数构造，所以接收方 key 泄露，进而用该 key 保护的 `protectedPayload` 也泄露。

`AUTHZ_BAD` 的 key secrecy 仍为 `true`，但 `AuthorizedAction ==> SendDone` 为 `false`。这说明只证明 key secrecy 不够。如果协议或应用把接收方接受直接解释为发送方授权，则 Q1 缺口会变成真正的语义攻击。

`CONFIRMED_FIX` 中，接收方必须验证由 `key` 和 `sid` 绑定得到的确认标签，才触发 `RecvDone`。攻击者无法为重组后的 `sid/key` 构造有效确认标签，因此 `RecvDone ==> SendDone` 恢复为 `true`。

## 对论文/报告写法的建议

建议不要把 K-Waay 的结论写成“没有 Q1”。更严谨的写法是：

```text
The symbolic model admits a receiver-to-sender exact-agreement gap: a receiver
may complete with a session identifier and key for which no matching sender
completion exists. However, in the K-Waay-like abstraction this gap does not
give the adversary the receiver's session key, does not break confidentiality
of data protected under that key, and the authenticated sender component still
has honest sender origin. Therefore the gap is harmless only under the stated
usage condition that receiver acceptance is not itself treated as a sender
authorization event.
```

中文表述可以写成：

```text
模型中存在接收方到发送方的 exact-agreement 缺口，但该缺口在 K-Waay 风格抽象中并不导致会话密钥泄露或受保护数据泄露；其安全性依赖于最终密钥包含发送方认证分量，并且上层应用不能把 RecvDone 本身解释为发送方授权。
```

