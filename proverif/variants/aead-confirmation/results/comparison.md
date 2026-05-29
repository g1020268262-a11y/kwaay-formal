# ProVerif 结果对比

本文根据 `baseline.out` 和 `aead.out` 中的 `Verification summary` 整理。ProVerif 的 reachability query 采用反向输出形式：例如 `Query not event(HonestRun(k)) is false` 表示 `HonestRun(k)` 可达，而不是坏结果。

## 1. 模型文件

| 模型 | 文件 | 说明 |
|---|---|---|
| baseline | `proverif/kwaay-core-public-channel.pv` | 原始 K-Waay core public-channel baseline。 |
| AEAD confirmation | `proverif/variants/aead-confirmation/kwaay-core-public-channel-aead.pv` | 加入 sid-bound AEAD/key-confirmation 的增强分支。 |

## 2. Verification summary 总览

| 验证目标 | baseline | AEAD confirmation | 解释 |
|---|---:|---:|---|
| HonestRun reachability: `not event(HonestRun(k))` | false | false | `Query not event(HonestRun(k)) is false` 表示 `HonestRun(k)` 在两个模型中都可达。 |
| Q1: `RecvDone ==> SendDone` | false | true | baseline 中 Q1 exact receiver agreement 失败；AEAD 分支中 Q1 成立。 |
| `RecvDone ==> AeadConfirmed` | 不适用 | true | baseline 没有运行该 AEAD 专用 query；AEAD 中 `RecvDone` 必须经过 `AeadConfirmed` 门控。 |
| `AeadConfirmed ==> SendDone` | 不适用 | true | baseline 没有运行该 AEAD 专用 query；AEAD 中确认事件对应发送方已完成。 |
| RecvComputed reachability: `not event(RecvComputed(...))` | 不适用 | false | AEAD 中 `Query not event(RecvComputed(...)) is false` 表示 `RecvComputed` 可达。baseline 未运行该 reachability query。 |
| AeadConfirmed reachability: `not event(AeadConfirmed(...))` | 不适用 | false | AEAD 中 `Query not event(AeadConfirmed(...)) is false` 表示 `AeadConfirmed` 可达。baseline 没有该 AEAD 确认事件 query。 |
| `RecvDone ==> SenderPrekeyVerified` | true | true | 两个模型中，`RecvDone` 均对应已验证的 sender prekey。 |
| `RecvDone ==> ReceiverPrekeyVerified` | true | true | 两个模型中，`RecvDone` 均对应已验证的 receiver prekey。 |
| SenderKey secrecy | true | true | `not (event(SenderKey(...)) && attacker(k))` 在 baseline 与 AEAD 中均为 true。 |
| ReceiverKey secrecy | true | true | `not (event(ReceiverKey(...)) && attacker(k))` 在 baseline 与 AEAD 中均为 true。 |

## 3. 核心结论

baseline 中 Q1 为 false：

  `event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k))`

AEAD 分支中 Q1 为 true。并且 AEAD 分支额外证明：

  `event(RecvDone(B,A,s,k)) ==> event(AeadConfirmed(B,A,s,k))`

以及：

  `event(AeadConfirmed(B,A,s,k)) ==> event(SendDone(A,B,s,k))`

因此 AEAD 修复形成如下证明链：

  `RecvDone ==> AeadConfirmed ==> SendDone`

这解释了为什么加入 AEAD/key-confirmation 后，Q1 exact receiver agreement 从 false 变为 true。

同时，SenderKey secrecy 和 ReceiverKey secrecy 在 baseline 与 AEAD 分支中均为 true。因此该结果不表示 key recovery attack；更准确地说，baseline 暴露的是 receiver-side exact agreement / key-confirmation gap。

## 4. 模型差异表

| 方面 | baseline | AEAD confirmation |
|---|---|---|
| 网络消息 | `m = msg(ctL, ctE, ctS)` | `m = confirmed_msg(mCore, kc)` |
| `sid_of` 输入 | 绑定原始核心消息 `m` | 绑定 `mCore`，不把 `kc` 放入 `sid_of` |
| 新增认证字段 | 无 | `kc = aead_tag(kSend, sidAB)` |
| 接收方接受条件 | 接收方计算出 `kRecv` 后直接触发 `ReceiverKey` 和 `RecvDone` | 接收方必须先验证 `aead_verify(kRecv, sidBA, kcFromNet) = aead_ok` |
| `RecvDone` 位置 | 位于本地 key derivation 之后 | 位于 `AeadConfirmed` 之后 |
| 攻击效果 | 攻击者可导致 receiver 接受 unpartnered session，因此 Q1 为 false | 攻击者无法绕过 AEAD confirmation 到达 `RecvDone`，因此 Q1 为 true |

## 5. 论文可用表述

中文：

原始 K-Waay core public-channel baseline 中，SenderKey secrecy 和 ReceiverKey secrecy 查询均为 true，但 Q1 exact receiver agreement 查询为 false。这说明攻击并不是 key recovery attack，而是 receiver-side exact agreement / key-confirmation gap。AEAD confirmation 分支加入 sid-bound confirmation 后，`RecvDone ==> AeadConfirmed ==> SendDone` 的证明链成立，使 Q1 从 false 变为 true，同时 secrecy 查询仍保持 true。

English:

In the public-channel ProVerif baseline, the K-Waay core preserves the modeled SenderKey and ReceiverKey secrecy properties, but the Q1 exact receiver agreement query is false. This should not be interpreted as a key-recovery attack; rather, it indicates a receiver-side exact agreement / key-confirmation gap. In the AEAD confirmation variant, the proof chain `RecvDone ==> AeadConfirmed ==> SendDone` holds, making Q1 true while preserving the modeled secrecy properties.
