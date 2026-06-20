# K-Waay AEAD confirmation 分支

本目录保存的是 **K-Waay core 协议的 AEAD/key-confirmation 增强版模型**。

注意：
本目录中的模型 **不是原始 K-Waay core 协议模型**。
原始 baseline 模型仍然保存在：

```text
proverif/kwaay-core-public-channel.pv
```

本分支的目标是：
在不修改原始 baseline 的前提下，单独建立一个加入 AEAD confirmation 的 K-Waay 变体模型，并与原始模型进行对比验证。

---

## 1. 为什么需要这个 AEAD 分支？

在原始 K-Waay core 模型中，接收方 B 的接受逻辑大致是：

```text
收到核心消息 m = (ctL, ctE, ctS)

解封装得到 KL2, KE2, KS2

计算 sidBA

计算 kRecv

触发 ReceiverKey

触发 RecvDone
```

也就是说，原始 core 中的接收方逻辑是：

```text
B 只要本地计算出 kRecv，就直接接受该会话。
```

这会导致一个重要的 diagnostic query 失败：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

该查询可以理解为：

```text
如果接收方 B 接受了一个声称来自 A 的 session key k，
那么发送方 A 应该已经完成过同一个 sid 和同一个 key 的发送会话。
```

原始 K-Waay core 中，这个查询可能为 `false`。

其原因是：
攻击者可以修改核心 KEM ciphertext，例如 `ctL`、`ctE` 或 `ctS`，使接收方 B 计算出一个新的 `sidBA` 和 `kRecv`，并触发：

```proverif
event RecvDone(B, A, sidBA, kRecv)
```

但是发送方 A 并没有对应的：

```proverif
event SendDone(A, B, sidBA, kRecv)
```

因此，原始 core 存在的是：

```text
explicit receiver agreement / explicit key confirmation 缺失
```

而不是：

```text
session key recovery
```

也就是说，这个问题不表示攻击者一定知道 `kRecv`。
它表示的是：接收方可能接受一个没有 exact matching sender session 的会话。

---

## 2. 本分支解决的是什么问题？

本分支要解决的是：

```text
receiver accepts unpartnered exact-session key
```

也就是：

```text
接收方 B 接受了某个 sid 和 key，
但发送方 A 没有完成对应的 SendDone(A,B,sid,key)。
```

本分支不声称原始 K-Waay core 的 secrecy 被攻破。
本分支的定位是：

```text
extension / hardening layer
```

即：

```text
在原始 K-Waay core 之外，加入显式 key confirmation，
使接收方接受语义和发送方完成语义对齐。
```

---

## 3. 原始设计与 AEAD 设计的主要区别

### 3.1 原始 K-Waay core

原始 core 的消息结构可以抽象为：

```text
m = (ctL, ctE, ctS)
```

发送方 A：

```text
1. 生成 ctL, ctE, ctS
2. 构造 m
3. 计算 sidAB
4. 计算 kSend
5. 发送 m
6. 触发 SendDone
```

接收方 B：

```text
1. 收到 m
2. 解封装 ctL, ctE, ctS
3. 计算 sidBA
4. 计算 kRecv
5. 触发 ReceiverKey
6. 触发 RecvDone
```

核心问题是：

```text
RecvDone 只依赖 B 本地算出 kRecv，
不需要验证 A 是否也知道同一个 k。
```

---

### 3.2 AEAD confirmation 分支

AEAD 分支将原始核心消息拆成两层：

```text
mCore = core_msg(ctL, ctE, ctS)

kc = aead_tag(kSend, sidAB)

m = confirmed_msg(mCore, kc)
```

其中：

```text
mCore
```

表示原始 K-Waay core transcript。

```text
kc
```

表示由发送方使用当前 session key 和 sid 生成的 AEAD confirmation tag。

完整网络消息变成：

```text
confirmed_msg(mCore, kc)
```

接收方 B 不再是“算出 kRecv 就接受”，而是必须验证：

```text
aead_verify(kRecv, sidBA, kcFromNet) = aead_ok
```

验证成功后，才能触发：

```proverif
event AeadConfirmed(B, A, sidBA, kRecv);
event ReceiverKey(B, A, sidBA, kRecv);
event RecvDone(B, A, sidBA, kRecv);
```

---

## 4. 固定后的 AEAD 建模方式

本分支采用简化后的 sid-bound AEAD tag confirmation。

### 4.1 新增类型

```proverif
type core_message.
type confirmed_message.
type aead_ct.
type verification_result.

free aead_ok: verification_result.
```

含义：

```text
core_message
```

表示原始核心 transcript，即：

```text
(ctL, ctE, ctS)
```

```text
confirmed_message
```

表示加入 AEAD confirmation 后的完整网络消息。

```text
aead_ct
```

表示 AEAD confirmation tag。

```text
verification_result
```

表示验证结果。

```text
aead_ok
```

表示 AEAD tag 验证成功。

---

### 4.2 核心消息与完整消息

```proverif
fun core_msg(kem_ct, ekem_ct, skem_ct): core_message.
fun confirmed_msg(core_message, aead_ct): confirmed_message.
```

含义：

```text
core_msg(ctL, ctE, ctS)
```

表示原始 K-Waay core 消息。

```text
confirmed_msg(mCore, kc)
```

表示加入 AEAD confirmation 后的完整消息。

---

### 4.3 AEAD tag 与验证

```proverif
fun aead_tag(session_key, sid_t): aead_ct.
fun aead_verify(session_key, sid_t, aead_ct): verification_result.

reduc forall k: session_key, s: sid_t;
  aead_verify(k, s, aead_tag(k, s)) = aead_ok.
```

含义：

```text
aead_tag(k, sid)
```

表示使用当前 session key 和 sid 生成确认 tag。

```text
aead_verify(k, sid, kc)
```

表示使用当前 session key 和 sid 验证收到的 tag。

只有当 `kc` 是由同一个 `k` 和同一个 `sid` 生成时，验证才返回：

```text
aead_ok
```

---

## 5. 为什么不使用 confirm_payload / confirm_context / kc_ok？

本分支不使用：

```text
confirm_payload(A, B, sid, mCore)
confirm_context(A, B, sid, mCore)
kc_ok
```

原因是为了避免冗余建模。

在本模型中：

```proverif
sidAB = sid_of(A, B, pkA, pkB,
               senderPrekeyA,
               receiverPrekeyFromNet,
               mCore)
```

`sidAB` 已经绑定了：

```text
A
B
pkA
pkB
sender prekey
receiver prekey
mCore = (ctL, ctE, ctS)
```

因此，如果再写：

```text
confirm_payload(A, B, sidAB, mCore)
```

或者：

```text
confirm_context(A, B, sidAB, mCore)
```

就会重复绑定 `A`、`B`、`mCore`。

本分支采用更简洁的设计：

```text
kc = aead_tag(kSend, sidAB)
```

也就是说：

```text
sid 作为当前 transcript/context 的压缩表示；
AEAD tag 只绑定 k 和 sid。
```

这样既保持了 transcript-bound key confirmation 的语义，又避免了过度冗余。

---

## 6. 为什么 sid 不绑定 kc？

本分支中，`sid_of` 只绑定：

```text
mCore = core_msg(ctL, ctE, ctS)
```

而不绑定：

```text
kc
```

原因是 `kc` 本身依赖 `sid`：

```text
sid -> k -> kc
```

如果反过来让 `sid` 绑定 `kc`，就会形成循环依赖：

```text
sid depends on kc
kc depends on sid
```

因此正确顺序是：

```text
mCore -> sid -> k -> kc -> confirmed_msg(mCore, kc)
```

错误顺序是：

```text
confirmed_msg(mCore, kc) -> sid -> k -> kc
```

所以本分支要求：

```proverif
sid_of(..., mCore)
```

而不是：

```proverif
sid_of(..., confirmed_msg(mCore, kc))
```

---

## 7. 发送方流程

AEAD 分支中的发送方流程如下：

```text
1. 生成 ctL, ctE, ctS。

2. 构造：

   mCore = core_msg(ctL, ctE, ctS)

3. 计算：

   sidAB = sid_of(A, B, pkA, pkB,
                  senderPrekeyA,
                  receiverPrekeyFromNet,
                  mCore)

4. 计算：

   kSend = kdf(KL, KE, KS, sidAB)

5. 生成 AEAD confirmation tag：

   kc = aead_tag(kSend, sidAB)

6. 构造完整网络消息：

   m = confirmed_msg(mCore, kc)

7. 发送：

   out(c, m)

8. 触发：

   event SenderKey(A, B, sidAB, kSend);
   event SendDone(A, B, sidAB, kSend);
```

发送方新增的核心操作是：

```text
kc = aead_tag(kSend, sidAB)
```

这表示：

```text
A 使用自己派生出的 session key，
对当前 sid 生成一个显式 key confirmation tag。
```

---

## 8. 接收方流程

AEAD 分支中的接收方流程如下：

```text
1. 接收完整消息：

   in(c, mFromNet: confirmed_message)

2. 拆分消息：

   mCoreFromNet = get_core(mFromNet)

   kcFromNet = get_key_confirmation(mFromNet)

3. 从 mCoreFromNet 中取出：

   ctLFromNet
   ctEFromNet
   ctSFromNet

4. 解封装得到：

   KL2
   KE2
   KS2

5. 计算：

   sidBA = sid_of(A, B, pkA, pkB,
                  senderPrekeyFromNet,
                  receiverPrekeyFromNet,
                  mCoreFromNet)

6. 计算：

   kRecv = kdf(KL2, KE2, KS2, sidBA)

7. 触发中间事件：

   event RecvComputed(B, A, sidBA, kRecv)

8. 验证 AEAD confirmation：

   aead_verify(kRecv, sidBA, kcFromNet) = aead_ok

9. 验证成功后触发：

   event AeadConfirmed(B, A, sidBA, kRecv);
   event ReceiverKey(B, A, sidBA, kRecv);
   event RecvDone(B, A, sidBA, kRecv);
```

关键变化是：

```text
ReceiverKey 和 RecvDone 被移动到 AEAD 验证之后。
```

也就是说，B 不再因为“自己算出 kRecv”就接受。
B 只有在确认 `kcFromNet` 能被 `kRecv` 和 `sidBA` 验证后，才正式接受。

---

## 9. 安全优势

### 9.1 修复 Q1 exact receiver agreement gap

原始模型中，攻击者可以修改核心 ciphertext，使 B 计算出新的：

```text
sidBA'
kRecv'
```

并直接触发：

```proverif
event RecvDone(B, A, sidBA', kRecv')
```

但 A 没有对应的：

```proverif
event SendDone(A, B, sidBA', kRecv')
```

因此 Q1 可以为 `false`。

AEAD 分支中，攻击者即使修改 `ctL`、`ctE` 或 `ctS`，也只能让 B 计算出新的：

```text
sidBA'
kRecv'
```

但是攻击者无法生成：

```text
aead_tag(kRecv', sidBA')
```

所以接收方无法通过：

```proverif
let (=aead_ok) = aead_verify(kRecv', sidBA', kcFromNet) in
```

因此 B 无法触发：

```proverif
event RecvDone(B, A, sidBA', kRecv')
```

攻击者最多只能让 B 到达：

```proverif
event RecvComputed(B, A, sidBA', kRecv')
```

但不能让 B 正式接受。

---

### 9.2 对齐 sender 与 receiver 的安全语义

原始 core 中：

```text
sender side:
A 计算 kSend 后触发 SendDone。

receiver side:
B 计算 kRecv 后触发 RecvDone。
```

这导致 receiver 的接受语义偏弱：

```text
B 本地算出 key = B 接受
```

AEAD 分支中：

```text
B 本地算出 key
+
B 验证发送方生成的 AEAD confirmation tag
=
B 接受
```

因此 receiver 的接受语义被增强为：

```text
B 接受前，必须确认发送方也知道当前 sid 对应的 session key。
```

这使得：

```text
RecvDone(B,A,s,k)
```

更接近：

```text
存在对应的 SendDone(A,B,s,k)
```

---

### 9.3 不改变原始 secrecy 结论

本分支不是为了证明原始 K-Waay core 泄露 key。
原始模型中的 secrecy query 仍然应该单独保留和分析。

AEAD 分支的作用是增强：

```text
explicit key confirmation
explicit receiver agreement
receiver-side robustness
```

而不是声称原始协议存在 key recovery attack。

---

### 9.4 低开销

AEAD 分支只额外增加：

```text
1. 一个 AEAD confirmation tag：kc
2. 发送方一次 aead_tag 生成
3. 接收方一次 aead_verify 验证
4. 一个 confirmed_message 包装层
```

消息从：

```text
(ctL, ctE, ctS)
```

变成：

```text
((ctL, ctE, ctS), kc)
```

核心 KEM 结构、`kdf` 结构和 `sid` 结构基本保持不变。

---

## 10. 与原始模型的关系

本目录中的模型应被理解为：

```text
K-Waay core + AEAD confirmation extension
```

而不是：

```text
原始 K-Waay core
```

论文或报告中应避免写成：

```text
K-Waay 原始协议就是这样设计的。
```

更准确的表述是：

```text
We propose and verify an AEAD-confirmed variant of the K-Waay core protocol.
```

或者：

```text
We add a sid-bound AEAD confirmation layer as an extension to the Figure 7 core.
```

---

## 11. 预期验证结果

baseline：

```text
文件：
proverif/kwaay-core-public-channel.pv

预期：
Q1 exact receiver agreement: false
```

AEAD confirmation 分支：

```text
文件：
proverif/variants/aead-confirmation/kwaay-core-public-channel-aead.pv

预期：
Q1 exact receiver agreement: true
```

其中 Q1 是：

```proverif
query A: agent, B: agent, s: sid_t, k: session_key;
  event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k)).
```

如果 AEAD 分支中 Q1 仍然为 `false`，需要检查：

```text
1. ReceiverKey 和 RecvDone 是否仍然在 aead_verify 之前触发。
2. sid_of 是否错误地绑定了 confirmed_message。
3. aead_verify 是否没有使用 kRecv 和 sidBA。
4. 发送方是否没有使用 kSend 和 sidAB 生成 kc。
5. 攻击者是否可以构造 aead_ok。
```

---

## 12. 运行方式

进入本目录：

```bash
cd proverif/variants/aead-confirmation
```

运行 AEAD 分支模型：

```bash
proverif kwaay-core-public-channel-aead.pv
```

如果配置了 `run.sh`，可以运行：

```bash
./run.sh
```

运行后建议查看：

```text
results/baseline.out
results/aead.out
results/comparison.md
```

---

## 13. 建议的结果记录方式

建议将 ProVerif 的原始输出保存到：

```text
results/
```

例如：

```text
results/baseline.out
results/aead.out
```

建议将人工分析写到：

```text
analysis/
```

例如：

```text
analysis/q1-gap.md
analysis/aead-fix.md
analysis/comparison-notes.md
```

其中：

```text
results/
```

用于保存机器输出。

```text
analysis/
```

用于保存人对结果的解释、论文素材和安全语义分析。

---

## 14. 总结

本 AEAD 分支的核心结论是：

```text
原始 K-Waay core 可以满足 secrecy-oriented 目标，
但在 Figure 7 core 层面缺少 explicit receiver agreement / key confirmation。

通过加入 sid-bound AEAD tag confirmation，
接收方必须先验证发送方确实知道当前 sid 对应的 session key，
然后才能触发 RecvDone。

因此，该增强层可以用于修复 Q1 exact receiver agreement 的 false 结果，
并使 sender 和 receiver 的接受语义更加对齐。
```
