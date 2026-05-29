# AEAD 分支如何阻断 baseline trace

## 1. 阻断点

baseline 中，B 算出 `k'` 后直接 `RecvDone`。AEAD 分支中，B 算出 `k'` 后只能先到 `RecvComputed`。B 必须验证 `aead_verify(k', sid', kcFromNet) = aead_ok`，验证成功后才可以 `RecvDone`。

## 2. honest sender 生成的 kc

honest sender A 对原始 `mCore` 计算：

```text
sid_original = sid_of(..., mCore)
k_original = kdf(..., sid_original)
kc_original = aead_tag(k_original, sid_original)
```

完整消息为：

```text
confirmed_msg(mCore, kc_original)
```

## 3. 攻击者篡改后的 mCore'

攻击者构造：

```text
mCore' = core_msg(ctL', ctE', ctS)
```

其中 `ctL'` 和 `ctE'` 是攻击者新构造的，`ctS` 是从 honest sender 原始消息中复用的。

B 对 `mCore'` 计算：

```text
sid' = sid_of(..., mCore')
k' = kdf(KL', KE', KS, sid')
```

## 4. 为什么旧 kc 不能通过验证

```text
kc_original = aead_tag(k_original, sid_original)
```

但 B 需要验证的是：

```text
aead_verify(k', sid', kc_original) = aead_ok
```

由于：

```text
sid' != sid_original
k' != k_original
```

所以：

```text
aead_verify(k', sid', kc_original)
```

不能归约为：

```text
aead_ok
```

因此 B 不能触发：

```text
AeadConfirmed
ReceiverKey
RecvDone
```

## 5. 攻击者为什么不能伪造新 kc

攻击者若想让 B 接受 `mCore'`，需要生成：

```text
kc' = aead_tag(k', sid')
```

但是 `k'` 是 B 根据解封装结果和 `sid'` 导出的 session key。在 no-compromise public-channel 模型下，攻击者不知道 `k'`，也不能破解 KDF 或 AEAD tag 构造。

因此攻击者无法生成有效的 `kc'`。

## 6. 事件链条

AEAD 分支验证结果已经证明：

```text
RecvDone(B,A,s,k) ==> AeadConfirmed(B,A,s,k)
```

并且：

```text
AeadConfirmed(B,A,s,k) ==> SendDone(A,B,s,k)
```

因此形成链条：

```text
RecvDone
  ==> AeadConfirmed
  ==> SendDone
```

这说明 AEAD 分支不是偶然让 Q1 变 true，而是通过 `AeadConfirmed` 这个门控点恢复了 receiver-to-sender exact agreement。

## 7. 一句话结论

AEAD 分支把 baseline 中“B 算出 key 就接受”的逻辑，改成“B 算出 key 后还必须验证 sender 对同一 sid 和 key 的 possession”，因此攻击者构造的 `mCore'` 会卡在 `aead_verify` 之前，无法触发 `RecvDone`。
