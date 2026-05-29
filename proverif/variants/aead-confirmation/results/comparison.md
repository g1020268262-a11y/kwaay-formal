# ProVerif 结果对比

本文根据以下两个已运行输出文件的 `Verification summary` 更新：

- `proverif/variants/aead-confirmation/results/baseline.out`
- `proverif/variants/aead-confirmation/results/aead.out`

注意：`Query not event(HonestRun(k)) is false` 的含义是 `HonestRun(k)` 可达，不是协议失败。

## 已运行 query 结果表

| query / 验证目标 | baseline 结果 | AEAD confirmation 结果 | 解释 |
|---|---:|---:|---|
| `not event(HonestRun(k))` | false | false | 两个模型中 `HonestRun(k)` 都可达。 |
| Q1: `event(RecvDone(B,A,s,k)) ==> event(SendDone(A,B,s,k))` | false | true | baseline 中 receiver exact agreement 失败；AEAD 分支中 Q1 成立。 |
| `event(RecvDone(B,A,s,k)) ==> event(SenderPrekeyVerified(B,A,sp))` | true | true | 两个模型都能保证 `RecvDone` 前存在对应的 sender prekey verification。 |
| `event(RecvDone(B,A,s,k)) ==> event(ReceiverPrekeyVerified(A,B,rp))` | true | true | 两个模型都能保证 `RecvDone` 前存在对应的 receiver prekey verification。 |
| `not (event(SenderKey(A,B,s,k)) && attacker(k))` | true | true | 两个模型中 SenderKey secrecy 都成立。 |
| `not (event(ReceiverKey(B,A,s,k)) && attacker(k))` | true | true | 两个模型中 ReceiverKey secrecy 都成立。 |

当前还没有在模型中加入以下 AEAD 专用 query，因此不记录为已验证结论，只标记为待补充：

- `RecvDone ==> AeadConfirmed`：待补充
- `AeadConfirmed ==> SendDone`：待补充
- `RecvComputed` reachability：待补充
- `AeadConfirmed` reachability：待补充

## 模型差异表

| 方面 | baseline | AEAD confirmation |
|---|---|---|
| 模型文件 | `proverif/kwaay-core-public-channel.pv` | `proverif/variants/aead-confirmation/kwaay-core-public-channel-aead.pv` |
| 网络消息 | `m = msg(ctL, ctE, ctS)` | `m = confirmed_msg(mCore, kc)` |
| 核心 transcript | `m` 直接包含三个 KEM ciphertext | `mCore = core_msg(ctL, ctE, ctS)` |
| `sid_of` 绑定对象 | 原始消息 `m` | 只绑定 `mCore`，不绑定 `kc` |
| key derivation | `k = kdf(KL, KE, KS, sid)` | `k = kdf(KL, KE, KS, sid)` |
| key confirmation | 无显式确认层 | 使用 sid-bound AEAD tag confirmation |
| 接收方接受条件 | 计算出 `kRecv` 后即可触发 `ReceiverKey` 和 `RecvDone` | 必须先通过 AEAD verification，之后才触发 `ReceiverKey` 和 `RecvDone` |
| Q1 结果 | false | true |
| SenderKey secrecy | true | true |
| ReceiverKey secrecy | true | true |

## 核心结论

baseline 中 Q1 exact receiver agreement 为 false，而 AEAD 分支中 Q1 为 true。同时，baseline 和 AEAD 分支中的 SenderKey secrecy、ReceiverKey secrecy 都为 true。

因此，这组结果不应解释为 key recovery attack。更准确的解释是：原始 K-Waay core public-channel baseline 存在 receiver-side agreement / key-confirmation gap；AEAD confirmation 分支通过显式 key confirmation 阻止 receiver 接受 unpartnered session。
