# Q1 分层诊断模型

> **LEGACY / INTERNAL DIAGNOSTIC**
>
> This reusable Q1 triage template is retained in place for historical
> diagnostic provenance and because its runner and committed logs use this
> path. It is not part of the active RQ-v2 main line. Its `.pv` model, runner,
> results, and historical interpretations are unchanged by the pre-RQ-v2
> cleanup.

这个文件夹给出一个可复用的 ProVerif 模板，用来回答两个层次的问题：

1. 协议是否存在 Q1 问题：接收方完成是否一定对应同一个 `sid` 和 `key` 的发送方完成。
2. 如果存在 Q1 问题，它是否只是一个无害的配对缺口，还是会进一步造成密钥泄露、受保护数据泄露，或错误触发发送方授权语义。

这里的 Q1 定义为接收方到发送方的 exact agreement：

```prolog
event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

这个模型不是完整的 K-Waay 证明，而是一个“诊断器”。它把 K-Waay 中类似 split-KEM 的三段密钥材料抽象成：

- `KL`：长期/普通 KEM 分量。
- `KE`：一次性/ephemeral KEM 分量。
- `KS`：带发送方隐式认证的 sender-authenticated KEM 分量。
- `sid`：绑定身份、公钥、预密钥和消息密文的会话标识。

## 文件

- `q1_triage.cpp.pv`：主模型，使用 `cpp -D TARGET` 选择不同协议形态。
- `run-q1-triage.sh`：批量运行脚本，会生成每个目标的 `.pv` 文件和 ProVerif 输出。

运行：

```bash
bash q1-analysis-model/run-q1-triage.sh
```

指定单个目标：

```bash
bash q1-analysis-model/run-q1-triage.sh KWAAY_LIKE
```

结果摘要在：

```text
logs/q1-analysis-model/summary.txt
```

## 目标场景

`KWAAY_LIKE` 表示 K-Waay 风格的情况：攻击者可以重组未认证的 `ctL` 和 `ctE`，再复用真实发送方产生的认证分量 `ctS`。因此接收方可能得到一个没有匹配发送方完成事件的 `sid/key`，Q1 查询失败。但是，因为最终密钥仍包含攻击者不知道的 `KS`，接收方密钥不泄露，受保护数据不泄露，并且被接收的认证分量确实来自发送方。

`ATTACKER_KEY_BAD` 表示一个危险协议变体：最终密钥只依赖攻击者可选择的 `KL` 和 `KE`，不依赖认证分量 `KS`。这种情况下 Q1 失败不再只是配对缺口，而会导致接收方密钥和用该密钥保护的数据泄露。

`AUTHZ_BAD` 表示另一类危险协议变体：密钥本身仍然安全，但协议或应用把 `RecvDone` 当成“发送方授权了某个副作用”。在这个语义下，即使攻击者不能知道密钥，Q1 失败仍然有害，因为接收方可以在没有匹配 `SendDone` 的情况下触发 `AuthorizedAction`。

`CONFIRMED_FIX` 表示加入 `sid/key` 绑定确认标签后的修复形态。接收方只有验证确认标签后才 `RecvDone`，因此 Q1 在这个抽象模型里恢复为真。

## 判定逻辑

第一层查询检测 Q1：

```prolog
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

如果这个查询为 `true`，说明该抽象模型没有发现 Q1 缺口。

如果这个查询为 `false`，继续看第二层 harmlessness 查询。

密钥是否泄露：

```prolog
query A: agent, B: agent, s: sid_t, k: session_key;
  attacker(k) && event(ReceiverKey(B,A,s,k)) ==> false.
```

认证分量是否确实来自发送方：

```prolog
query A: agent, B: agent, cts: skem_ct, Ks: shared_secret;
  event(AuthComponentAccepted(B,A,cts,Ks))
  ==> event(AuthComponentSent(A,B,cts,Ks)).
```

用接收方密钥保护的数据是否泄露：

```prolog
query A: agent, B: agent, s: sid_t, d: app_secret;
  attacker(d) && event(ProtectedData(B,A,s,d)) ==> false.
```

是否错误触发发送方授权副作用：

```prolog
query A: agent, B: agent, s: sid_t, k: session_key;
  event(AuthorizedAction(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

因此可以这样分类：

- Q1 为 `true`：没有发现接收方到发送方 exact agreement 缺口。
- Q1 为 `false`，但密钥保密、认证分量来源、受保护数据保密都为 `true`，且没有把 `RecvDone` 用作发送方授权副作用：Q1 在这个抽象中是 harmless agreement gap。
- Q1 为 `false`，且密钥保密或受保护数据保密为 `false`：Q1 会变成实际机密性攻击。
- Q1 为 `false`，且授权副作用查询为 `false`：Q1 会变成应用语义攻击，即使密钥仍不可知。

## 如何迁移到其他协议

把其他协议放进这个框架时，重点不是机械套 K-Waay 的三段 KEM，而是明确四个映射：

1. `SendDone(A,B,s,k)` 应该放在发送方已经固定 `sid` 和 `key`，并认为消息发给 `B` 的位置。
2. `RecvDone(B,A,s,k)` 应该放在接收方已经接受 `A`，并准备使用 `sid/key` 的位置。
3. `ReceiverKey(B,A,s,k)` 应该标记接收方实际会用于保护数据或上层协议的密钥。
4. 如果协议存在应用副作用，例如授权、扣款、状态提交、群组成员变更，应显式建 `AuthorizedAction` 或类似事件，不能只看 key secrecy。

对 K-Waay 这类协议，关键是不要把 Q1 简化成“攻击者能不能改 key”。更准确的结论是：

- 攻击者可以通过重组未认证分量让接收方得到一个没有匹配发送方完成事件的新 `sid/key`。
- 但如果最终密钥包含发送方认证分量，攻击者不能计算该 key。
- 如果接收方只把该 key 用作后续受认证/加密通道的密钥，且没有额外授权副作用，那么这个 Q1 缺口可以被论证为无害。
- 如果接收方把接受事件本身当成发送方授权，那么同样的 Q1 缺口就不再无害。
